import streamlit as st
import pandas as pd
import numpy as np
import requests  # 新增：用于检测图片链接是否有效

# 页面基础配置（宽屏+标题+图标）
st.set_page_config(
    page_title="南宁美食数据仪表盘",  # 修正重复的标题
    page_icon="🍜",
    layout="wide"
)

# --------------------------
# 自定义样式：马卡龙蓝色主调 + 美化组件
# --------------------------
st.markdown("""
    <style>
    /* 全局主色调：马卡龙蓝 */
    :root {
        --primary-color: #8ECAE6;
        --secondary-color: #219EBC;
        --light-blue: #A7C957; /* 辅助色 */
        --pale-blue: #F8F9FA;
    }
    
    /* 标题样式 */
    h1, h2, h3, h4 {
        color: var(--secondary-color) !important;
    }
    
    /* 按钮样式 */
    .stButton>button {
        background-color: var(--primary-color);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stButton>button:hover {
        background-color: var(--secondary-color);
    }
    
    /* 进度条样式 */
    .stProgress > div > div {
        background-color: var(--primary-color) !important;
    }
    
    /* 选择框/输入框样式 */
    .stSelectbox, .stTextInput {
        border: 1px solid var(--primary-color);
        border-radius: 8px;
    }
    
    /* 卡片背景 */
    .main {
        background-color: var(--pale-blue);
    }
    
    /* 优化地图标记点 - 更小且带颜色区分 */
    .leaflet-marker-icon {
        width: 10px !important;  /* 进一步缩小标记 */
        height: 10px !important;
        margin-left: -5px !important;  /* 居中调整 */
        margin-top: -5px !important;
        border-radius: 50% !important;  /* 圆形设计 */
        box-shadow: none !important;  /* 去除阴影避免视觉堆积 */
    }
    .leaflet-marker-shadow {
        display: none !important;  /* 彻底移除阴影 */
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------
# 新增：图片链接有效性检测函数
# --------------------------
def is_image_url_valid(url):
    """检测图片链接是否可访问"""
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200 and 'image' in response.headers.get('Content-Type', '')
    except:
        return False

# --------------------------
# 1. 核心数据准备（微调坐标避免完全重叠）
# --------------------------
# 基础店铺信息（微调坐标，确保标记分散显示）
restaurants_data = {
    "餐厅": ["重庆小面", "兰州拉面", "塔斯汀", "KFC", "三品王"],
    "类型": ["中餐", "中餐", "快餐", "快餐", "快餐"],
    "评分": [4.3, 4.5, 4.2, 4.4, 4.1],
    "人均消费(元)": [12, 15, 18, 30, 16],
    # 微调经纬度，增加微小偏移避免完全重叠
    "latitude": [22.806812, 22.805787, 22.807743, 22.808411, 22.805955],
    "longitude": [108.203546, 108.204328, 108.202787, 108.205212, 108.203679],
    "推荐菜品": [
        ["招牌小面", "豌杂面", "酸辣粉"],
        ["牛肉拉面", "清汤拉面", "炒拉面"],
        ["香辣鸡腿堡", "薯条", "可乐"],
        ["原味鸡", "汉堡", "蛋挞"],
        ["牛肉粉", "杂酱粉", "猪脚粉"]
    ],
    "拥挤程度(%)": [78, 85, 70, 88, 68]
}
df = pd.DataFrame(restaurants_data)

# 模拟用餐时段数据（贴合南宁本地习惯）
time_data = pd.DataFrame({
    "时段": ["09:00", "11:00", "13:00", "17:00", "19:00", "21:00"],
    "用餐人数(峰值)": [40, 250, 100, 90, 300, 180]
}).set_index("时段")

# 5家餐厅12个月价格走势数据
months = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
price_trend = pd.DataFrame({
    "月份": months,
    "重庆小面": [12, 12, 12, 13, 13, 13, 14, 14, 13, 13, 12, 12],
    "兰州拉面": [15, 15, 16, 16, 16, 17, 17, 17, 16, 16, 15, 15],
    "三品王": [16, 16, 16, 17, 17, 17, 18, 18, 17, 17, 16, 16],
    "塔斯汀": [18, 18, 18, 19, 19, 20, 20, 20, 19, 19, 18, 18],
    "KFC": [30, 30, 31, 32, 32, 33, 33, 33, 32, 32, 31, 30]
}).set_index("月份")

# --------------------------
# 2. 主标题+核心可视化模块
# --------------------------
st.title("🍜 南宁西乡塘罗文大道美食数据仪表盘")

# 第一行：地图（精准定位） + 评分柱状图
col1, col2 = st.columns(2)
with col1:
    st.subheader("📍 餐厅位置分布（罗文大道15号）")
    # 地图聚焦罗文大道，保持合适缩放级别
    st.map(df[["latitude", "longitude"]], zoom=16, use_container_width=True)  # 提高zoom级别到16，显示更细致

with col2:
    st.subheader("⭐ 餐厅评分排行")
    score_df = df.sort_values("评分", ascending=False).set_index("餐厅")["评分"]
    st.bar_chart(score_df, color="#8ECAE6", use_container_width=True)

# 第二行：人均消费折线图 + 用餐高峰面积图
col3, col4 = st.columns(2)
with col3:
    st.subheader("💰 不同类型餐厅人均消费")
    consume_df = df.groupby("类型")["人均消费(元)"].mean()
    st.line_chart(consume_df, color="#219EBC", use_container_width=True)

with col4:
    st.subheader("📈 用餐高峰时段（南宁本地）")
    st.area_chart(time_data, color="#A7C957", use_container_width=True)

# 第三行 - 5家餐厅12个月价格走势折线图
st.subheader("📊 5家餐厅12个月价格走势（分层展示）")
line_colors = ["#8ECAE6", "#219EBC", "#6A994E", "#F2E8CF", "#BC4749"]
st.line_chart(
    price_trend,
    color=line_colors,
    use_container_width=True,
    height=400
)

# --------------------------
# 3. 餐厅详情 + 可交互午餐推荐（修复图片显示）
# --------------------------
st.subheader("📋 餐厅详情与午餐推荐")
col5, col6 = st.columns([1, 1])

with col5:
    selected_rest = st.selectbox(
        "选择餐厅查看详情",
        options=df["餐厅"],
        index=1
    )
    rest_info = df[df["餐厅"] == selected_rest].iloc[0]
    
    st.markdown(f"### {rest_info['餐厅']}")
    st.markdown(f"**评分**：{rest_info['评分']}/5.0")
    st.markdown(f"**人均消费**：{rest_info['人均消费(元)']}元")
    st.markdown(f"**地址**：南宁西乡塘区罗文大道15号")
    
    st.markdown("**推荐菜品：**")
    for dish in rest_info["推荐菜品"]:
        st.markdown(f"- {dish}")
    
    st.markdown("### 当前拥挤程度")
    st.progress(rest_info["拥挤程度(%)"] / 100, text=f"{rest_info['拥挤程度(%)']}% 拥挤")

with col6:
    st.markdown("### 今日午餐推荐")
    lunch_click = st.button("帮我选午餐", use_container_width=True)
    
    if lunch_click:
        st.success("✅ 为你推荐：兰州拉面（牛肉拉面）")
        st.markdown(f"""
        <div style="background-color: #8ECAE6; padding: 10px; border-radius: 8px; color: white; margin: 10px 0;">
            <strong>推荐理由</strong>：评分4.5分（最高），人均15元，拥挤度85%（适中），适合午餐！
        </div>
        """, unsafe_allow_html=True)
    
    # --------------------------
    # 核心修改：修复兰州拉面配图显示
    # --------------------------
    # 方案1：使用有效图片链接（优先）
    valid_lanzhou_image_url = "https://img.51miz.com/Element/00/98/15/61/589a3898_E981561_9c190719.png!/quality/90/unsharp/true/compress/true/format/png/fh/350"
    
    # 检测链接有效性，无效则使用备选方案
    if is_image_url_valid(valid_lanzhou_image_url):
        st.image(
            valid_lanzhou_image_url,
            caption="兰州拉面（南宁西乡塘罗文大道店）",
            use_container_width=True
        )
    else:
        # 方案2：本地图片备用（将图片放在和代码同目录，命名为lanzhou_ramen.jpg）
        try:
            st.image(
                "lanzhou_ramen.jpg",  # 本地图片路径
                caption="兰州拉面（南宁西乡塘罗文大道店）",
                use_container_width=True
            )
        except:
            # 方案3：文字兜底 + 提示
            st.markdown("""
            <div style="background-color: #f0f8ff; padding: 20px; border-radius: 8px; text-align: center;">
                <h4>🍜 兰州拉面</h4>
                <p>南宁西乡塘罗文大道店</p>
                <p style="color: #999;">（图片加载失败，可放置本地图片 lanzhou_ramen.jpg 到代码目录）</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.caption("📍 地址：南宁西乡塘区罗文大道15号")