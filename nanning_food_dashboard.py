import streamlit as st
import pandas as pd
import numpy as np

# 页面基础配置（宽屏+标题+图标）
st.set_page_config(
    page_title="南宁美食数据仪表盘",
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
    
    /* 缩小地图标记点 */
    .leaflet-marker-icon {
        width: 15px !important;
        height: 15px !important;
        margin-left: -7.5px !important;
        margin-top: -7.5px !important;
    }
    .leaflet-marker-shadow {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------
# 1. 核心数据准备（替换为指定5家店铺+精准定位）
# --------------------------
# 基础店铺信息（西乡塘罗文大道15号周边精准坐标）
restaurants_data = {
    "餐厅": ["重庆小面", "兰州拉面", "塔斯汀", "KFC", "三品王"],
    "类型": ["中餐", "中餐", "快餐", "快餐", "快餐"],
    "评分": [4.3, 4.5, 4.2, 4.4, 4.1],
    "人均消费(元)": [12, 15, 18, 30, 16],
    "latitude": [22.806812, 22.805987, 22.807543, 22.808211, 22.806155],  # 罗文大道15号周边精准纬度
    "longitude": [108.203546, 108.204128, 108.202987, 108.205012, 108.203879],  # 罗文大道15号周边精准经度
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

# 新增：5家餐厅12个月价格走势数据（模拟真实波动，调整数值分层）
months = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
# 优化数值：让每条折线分层显示，避免堆叠（按价格区间梯度设计）
price_trend = pd.DataFrame({
    "月份": months,
    "重庆小面": [12, 12, 12, 13, 13, 13, 14, 14, 13, 13, 12, 12],          # 12-14元区间
    "兰州拉面": [15, 15, 16, 16, 16, 17, 17, 17, 16, 16, 15, 15],          # 15-17元区间
    "三品王": [16, 16, 16, 17, 17, 17, 18, 18, 17, 17, 16, 16],            # 16-18元区间
    "塔斯汀": [18, 18, 18, 19, 19, 20, 20, 20, 19, 19, 18, 18],            # 18-20元区间
    "KFC": [30, 30, 31, 32, 32, 33, 33, 33, 32, 32, 31, 30]               # 30-33元区间
}).set_index("月份")

# --------------------------
# 2. 主标题+核心可视化模块
# --------------------------
st.title("🍜 南宁西乡塘罗文大道美食数据仪表盘")

# 第一行：地图（精准定位） + 评分柱状图
col1, col2 = st.columns(2)
with col1:
    st.subheader("📍 餐厅位置分布（罗文大道15号）")
    # 地图聚焦罗文大道，zoom=15更精准
    st.map(df[["latitude", "longitude"]], zoom=15, use_container_width=True)

with col2:
    st.subheader("⭐ 餐厅评分排行")
    score_df = df.sort_values("评分", ascending=False).set_index("餐厅")["评分"]
    st.bar_chart(score_df, color="#8ECAE6", use_container_width=True)  # 马卡龙蓝

# 第二行：人均消费折线图 + 用餐高峰面积图
col3, col4 = st.columns(2)
with col3:
    st.subheader("💰 不同类型餐厅人均消费")
    consume_df = df.groupby("类型")["人均消费(元)"].mean()
    st.line_chart(consume_df, color="#219EBC", use_container_width=True)  # 深一点的马卡龙蓝

with col4:
    st.subheader("📈 用餐高峰时段（南宁本地）")
    st.area_chart(time_data, color="#A7C957", use_container_width=True)  # 辅助色（浅绿）

# 新增：第三行 - 5家餐厅12个月价格走势折线图
st.subheader("📊 5家餐厅12个月价格走势")
# 自定义马卡龙色系，每条折线颜色区分明显
line_colors = ["#8ECAE6", "#219EBC", "#6A994E", "#F2E8CF", "#BC4749"]
st.line_chart(
    price_trend,
    color=line_colors,  # 马卡龙色系
    use_container_width=True,
    height=400  # 增加高度，让分层折线更清晰
)

# --------------------------
# 3. 餐厅详情 + 可交互午餐推荐（兰州拉面配图）
# --------------------------
st.subheader("📋 餐厅详情与午餐推荐")
col5, col6 = st.columns([1, 1])

with col5:
    # 餐厅下拉选择框
    selected_rest = st.selectbox(
        "选择餐厅查看详情",
        options=df["餐厅"],
        index=1  # 默认选中兰州拉面
    )
    # 获取选中餐厅信息
    rest_info = df[df["餐厅"] == selected_rest].iloc[0]
    
    # 展示餐厅详情（马卡龙蓝配色）
    st.markdown(f"### {rest_info['餐厅']}")
    st.markdown(f"**评分**：{rest_info['评分']}/5.0")
    st.markdown(f"**人均消费**：{rest_info['人均消费(元)']}元")
    st.markdown(f"**地址**：南宁西乡塘区罗文大道15号")
    
    # 推荐菜品
    st.markdown("**推荐菜品：**")
    for dish in rest_info["推荐菜品"]:
        st.markdown(f"- {dish}")
    
    # 拥挤程度进度条
    st.markdown("### 当前拥挤程度")
    st.progress(rest_info["拥挤程度(%)"] / 100, text=f"{rest_info['拥挤程度(%)']}% 拥挤")

with col6:
    # 可交互午餐推荐按钮
    st.markdown("### 今日午餐推荐")
    lunch_click = st.button("帮我选午餐", use_container_width=True)
    
    # 按钮点击后显示推荐结果（马卡龙蓝提示）
    if lunch_click:
        st.success("✅ 为你推荐：兰州拉面（牛肉拉面）")
        st.markdown(f"""
        <div style="background-color: #8ECAE6; padding: 10px; border-radius: 8px; color: white; margin: 10px 0;">
            <strong>推荐理由</strong>：评分4.5分（最高），人均15元，拥挤度85%（适中），适合午餐！
        </div>
        """, unsafe_allow_html=True)
    
    # 兰州拉面配图（网络图，可替换为本地图）
    st.image(
        "https://img.zcool.cn/community/016f9058ac8598a801219c7df8e9833.jpg@1280w_1l_2o_100sh.jpg",
        caption="兰州拉面（南宁西乡塘罗文大道店）",
        use_container_width=True
    )
    st.caption("📍 地址：南宁西乡塘区罗文大道15号")