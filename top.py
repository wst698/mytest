import streamlit as st
import pandas as pd
import numpy as np
import requests
import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import os
from PIL import Image as PILImage
import tempfile

# 页面配置：强制宽布局（适配电脑全屏）
st.set_page_config(
    page_title="宠物家园首页",
    page_icon="🐾",
    layout="wide",  # 全屏宽布局
    initial_sidebar_state="collapsed"  # 隐藏侧边栏，给选项卡更多空间
)

# 全局样式：优化标题、选项卡显示
st.markdown("""
    <style>
    /* 大标题样式 */
    .main-title {
        text-align: center;
        color: #FF8C42;
        font-size: 36px;
        font-weight: bold;
        margin: 20px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    /* 选项卡容器：确保全部横向显示 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;  /* 选项卡之间的间距 */
        justify-content: center;  /* 选项卡居中 */
        font-size: 18px;
    }
    /* 封面图容器 */
    .cover-img {
        width: 100%;
        max-width: 800px;
        margin: 0 auto;
    }
    </style>
""", unsafe_allow_html=True)

# 选项卡上方的大标题
st.markdown('<div class="main-title">宠物家园首页</div>', unsafe_allow_html=True)

# 创建5个横向选项卡（确保全部显示）
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "首页", 
    "南宁宠物美食推荐", 
    "宠物照片展示", 
    "宠物简历服务",
    "宠物趣味视频"
])

# ======================================
# 1. 首页 (tab1)：添加封面图+原有内容
# ======================================
with tab1:
    # 显示宠物家园封面图（请将路径替换为你的本地图片路径）
    # 提示：把封面图保存到代码同级目录，命名为"pet_home_cover.png"
    cover_img_path = "pet_home_cover.png"  # 替换为你的图片路径
    if os.path.exists(cover_img_path):
        st.markdown('<div class="cover-img">', unsafe_allow_html=True)
        st.image(cover_img_path, use_column_width=True, caption="宠物家园/封面图")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("请将封面图保存为 pet_home_cover.png 放到代码同级目录，即可显示封面~")

    # 原有首页介绍内容
    st.write("""
    ### 🐾 欢迎来到「毛孩子星球」—— 这里是爱宠人士的专属港湾，更是萌宠们的幸福乐园！

    无论是软萌粘人的猫咪、热情活力的狗狗，还是灵动可爱的小宠，我们始终相信，每一只毛孩子都是家庭中不可或缺的重要成员。在这里，你能找到一站式宠物生活解决方案：精选高性价比的用品好物（口粮、玩具、洗护、家居），解锁专业科学的养护知识（喂养指南、健康科普、行为训练），邂逅志同道合的宠友社群（晒娃分享、经验交流、线下聚会），更有贴心的本地服务推荐（宠物医院、寄养托管、美容洗护）。

    我们以「科学养宠、温暖陪伴」为初心，用专业与热爱，守护每一段人与宠物的美好缘分。愿每一只毛孩子都能健康快乐成长，每一份铲屎官的爱都能被温柔回应～ 现在就开启你的专属宠友之旅吧！🐱🐶🐰
    """)

# ======================================
# 以下是原有其他选项卡的内容（保持功能不变）
# ======================================
with tab2:
    # 南宁宠物美食推荐原代码（略，与之前一致）
    # 自定义样式：马卡龙蓝色主调 + 美化组件
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
        
        /* 优化地图标记点 */
        .leaflet-marker-icon {
            width: 10px !important;
            height: 10px !important;
            margin-left: -5px !important;
            margin-top: -5px !important;
            border-radius: 50% !important;
            box-shadow: none !important;
        }
        .leaflet-marker-shadow {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 图片链接有效性检测函数
    def is_image_url_valid(url):
        """检测图片链接是否可访问"""
        try:
            response = requests.head(url, timeout=5)
            return response.status_code == 200 and 'image' in response.headers.get('Content-Type', '')
        except:
            return False

    # 核心数据准备
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

    # 模拟用餐时段数据
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

    # 主标题+核心可视化模块
    st.title("🍜 南宁西乡塘罗文大道美食数据仪表盘")

    # 第一行：地图 + 评分柱状图
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📍 餐厅位置分布（罗文大道15号）")
        st.map(df[["latitude", "longitude"]], zoom=16, use_container_width=True)

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

    # 餐厅详情 + 可交互午餐推荐
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
        
        # 兰州拉面配图
        valid_lanzhou_image_url = "https://img.51miz.com/Element/00/98/15/61/589a3898_E981561_9c190719.png!/quality/90/unsharp/true/compress/true/format/png/fh/350"
        
        if is_image_url_valid(valid_lanzhou_image_url):
            st.image(
                valid_lanzhou_image_url,
                caption="兰州拉面（南宁西乡塘罗文大道店）",
                use_container_width=True
            )
        else:
            try:
                st.image(
                    "lanzhou_ramen.jpg",
                    caption="兰州拉面（南宁西乡塘罗文大道店）",
                    use_container_width=True
                )
            except:
                st.markdown("""
                <div style="background-color: #f0f8ff; padding: 20px; border-radius: 8px; text-align: center;">
                    <h4>🍜 兰州拉面</h4>
                    <p>南宁西乡塘罗文大道店</p>
                    <p style="color: #999;">（图片加载失败，可放置本地图片 lanzhou_ramen.jpg 到代码目录）</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.caption("📍 地址：南宁西乡塘区罗文大道15号")

with tab3:
    # 宠物照片展示原代码（略，与之前一致）
    # 自定义莫兰迪马卡龙蓝灰色背景样式
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #E0E5EC;  /* 莫兰迪蓝灰色 */
        }
        .stImage {
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .caption {
            font-size: 18px;
            color: #5A6A85;
            text-align: center;
            margin-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 初始化图片索引（使用带前缀的session_state键避免冲突）
    if 'pet_photo_ind' not in st.session_state:
        st.session_state['pet_photo_ind'] = 0

    # 图片列表
    images = [
        {
            'url': "https://images.unsplash.com/photo-1543466835-00a7907e9de1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            'text': "乖乖小狗"
        },
        {
            'url': "https://images.unsplash.com/photo-1507146426996-ef05306b995a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            'text': "小鸡毛"
        },
        {
            'url': "https://images.unsplash.com/photo-1535930891776-0c2dfb7fda1a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            'text': "大鸡毛"
        },
        {
            'url': "https://imgs.699pic.com/images/501/028/820.jpg!list1x.v2",
            'text': "贱兮兮柴犬"
        }
    ]

    # 标题
    st.title("莫兰迪马卡龙相册")

    # 显示当前图片和图注
    current_img = images[st.session_state['pet_photo_ind']]
    st.image(current_img['url'], use_column_width=True, caption=current_img['text'])

    # 切换图片函数
    def next_img():
        st.session_state['pet_photo_ind'] = (st.session_state['pet_photo_ind'] + 1) % len(images)

    def prev_img():
        st.session_state['pet_photo_ind'] = (st.session_state['pet_photo_ind'] - 1) % len(images)

    # 前后切换按钮
    col1, col2 = st.columns(2)
    with col1:
        st.button("上一张", on_click=prev_img)
    with col2:
        st.button("下一张", on_click=next_img)

with tab4:
    # 宠物简历服务原代码（略，与之前一致）
    # 注册中文字体
    def register_chinese_font():
        """注册中文字体，优先使用系统字体，备用本地字体"""
        font_configs = [
            {"name": "SimHei", "paths": ["C:/Windows/Fonts/simhei.ttf", "C:/Windows/Fonts/msyh.ttc"]},
            {"name": "PingFang", "paths": ["/System/Library/Fonts/PingFang.ttc", "/Library/Fonts/Arial Unicode.ttf"]},
            {"name": "DejaVuSans", "paths": ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]}
        ]
        
        for config in font_configs:
            for path in config["paths"]:
                if os.path.exists(path):
                    try:
                        pdfmetrics.registerFont(TTFont(config["name"], path))
                        return config["name"]
                    except:
                        continue
        return "Helvetica"

    chinese_font_name = register_chinese_font()

    # 自定义样式
    st.markdown("""
        <style>
        .stApp { 
            background-color: #F9F7F8; 
            color: #4A4A4A; 
            font-family: "Microsoft YaHei", sans-serif;
        }
        .stTextInput > div > div > input, 
        .stSelectbox > div > div > select, 
        .stTextArea > div > div > textarea,
        .stDateInput > div > div > input { 
            background-color: #FFFFFF; 
            color: #4A4A4A; 
            border: 1px solid #E8D5DE; 
            border-radius: 8px;
            padding: 8px 12px;
        }
        .stSlider > div > div > div { color: #9D6588; }
        .stSlider [data-baseweb="slider"] { color: #D88FB9; }
        .stButton > button { 
            background-color: #E899AF; 
            color: white; 
            border: none;
            border-radius: 8px;
            padding: 8px 20px;
            font-weight: 500;
        }
        .stButton > button:hover { background-color: #D88FB9; }
        .stRadio > div > label, .stMultiSelect > div > label { color: #6B5B6B; }
        .preview-card { 
            background-color: #FFFFFF; 
            padding: 30px; 
            border-radius: 12px;
            border: 1px solid #F0E0E6;
            box-shadow: 0 2px 10px rgba(222, 200, 210, 0.1);
        }
        h1, h2, h3 { color: #8B6B89; }
        .stCaption { color: #9A8B98; }
        hr { border-top: 1px solid #F0E0E6; }
        .experience-card {
            background-color: #F9F7F8;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 8px;
            border-left: 3px solid #D88FB9;
        }
        .quick-reset-btn {
            background-color: #FF5252 !important;
        }
        .quick-reset-btn:hover {
            background-color: #FF1744 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 强制重置所有会话状态
    def force_reset_all():
        """强制重置所有会话状态，包括隐藏的临时状态"""
        # 清空所有会话状态
        for key in list(st.session_state.keys()):
            if key.startswith('pet_resume_'):
                del st.session_state[key]
        
        # 重新初始化默认值
        default_vals = {
            "pet_resume_name": "",
            "pet_resume_nickname": "",
            "pet_resume_phone": "",
            "pet_resume_email": "",
            "pet_resume_address": "",
            "pet_resume_id_card": "",
            "pet_resume_birth_date": datetime.date(2000, 1, 1),
            "pet_resume_gender": "女",
            "pet_resume_education": "本科",
            "pet_resume_skills": ["UI/UX设计", "新媒体运营"],
            "pet_resume_work_exp": 0,
            "pet_resume_salary_range": (8000, 12000),
            "pet_resume_grad_info": "2024届 某某大学 某某专业",
            "pet_resume_grad_info_custom": "",
            "pet_resume_job_intention": "新媒体运营",
            "pet_resume_job_intention_custom": "",
            "pet_resume_job_city": ["北京", "上海"],
            "pet_resume_custom_city": "",
            "pet_resume_arrival_time": "随时到岗",
            "pet_resume_experience": "",
            "pet_resume_intro": "",
            "pet_resume_avatar": None,
            "pet_resume_reset_confirm": False,
            "pet_resume_avatar_uploader_key": 0
        }
        
        # 重新赋值所有默认值
        for key, val in default_vals.items():
            st.session_state[key] = val
        
        st.toast("⚡ 所有信息已强制重置为默认值！", icon="🔥")

    # 初始化会话状态
    def init_session_state():
        """初始化所有表单项的默认值到会话状态"""
        default_vals = {
            "pet_resume_name": "",
            "pet_resume_nickname": "",
            "pet_resume_phone": "",
            "pet_resume_email": "",
            "pet_resume_address": "",
            "pet_resume_id_card": "",
            "pet_resume_birth_date": datetime.date(2000, 1, 1),
            "pet_resume_gender": "女",
            "pet_resume_education": "本科",
            "pet_resume_skills": ["UI/UX设计", "新媒体运营"],
            "pet_resume_work_exp": 0,
            "pet_resume_salary_range": (8000, 12000),
            "pet_resume_grad_info": "2024届 某某大学 某某专业",
            "pet_resume_grad_info_custom": "",
            "pet_resume_job_intention": "新媒体运营",
            "pet_resume_job_intention_custom": "",
            "pet_resume_job_city": ["北京", "上海"],
            "pet_resume_custom_city": "",
            "pet_resume_arrival_time": "随时到岗",
            "pet_resume_experience": "",
            "pet_resume_intro": "",
            "pet_resume_avatar": None,
            "pet_resume_reset_confirm": False,
            "pet_resume_avatar_uploader_key": 0
        }
        for key, val in default_vals.items():
            if key not in st.session_state:
                st.session_state[key] = val

    # 执行初始化
    init_session_state()

    # PDF生成函数
    def generate_resume_pdf(
        name, nickname, birth_date, gender, education, work_exp,
        salary_min, salary_max, grad_info, job_intention, job_city,
        arrival_time, phone, email, address, id_card, skills, experience, intro, avatar
    ):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=inch/2,
            leftMargin=inch/2,
            topMargin=inch/2,
            bottomMargin=inch/2
        )
        elements = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontName=chinese_font_name,
            fontSize=20,
            spaceAfter=10,
            textColor=colors.HexColor("#8B6B89"),
            alignment=0
        )

        sub_title_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontName=chinese_font_name,
            fontSize=14,
            spaceAfter=8,
            textColor=colors.HexColor("#8B6B89"),
            alignment=0
        )

        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontName=chinese_font_name,
            fontSize=11,
            spaceAfter=5,
            textColor=colors.HexColor("#4A4A4A"),
            alignment=0,
            allowWidows=0,
            allowOrphans=0
        )

        name_text = name if name else "你的姓名"
        elements.append(Paragraph(name_text, title_style))
        
        basic_info = (
            f"昵称：{nickname if nickname else '暂无'} | "
            f"{birth_date.strftime('%Y年%m月')}出生 | "
            f"性别：{gender} | 学历：{education}"
        )
        elements.append(Paragraph(basic_info, normal_style))
        elements.append(Spacer(1, 10))

        elements.append(Paragraph("求职意向", sub_title_style))
        job_city_text = ', '.join(job_city) if job_city else '暂无'
        intention_info = (
            f"意向岗位：{job_intention if job_intention else '暂无'}\n"
            f"意向城市：{job_city_text}\n"
            f"到岗时间：{arrival_time}\n"
            f"期望薪资：{salary_min}-{salary_max}元/月 | 工作经验：{work_exp}年"
        )
        elements.append(Paragraph(intention_info, normal_style))
        elements.append(Spacer(1, 10))

        elements.append(Paragraph("联系方式", sub_title_style))
        contact_info = (
            f"电话：{phone if phone else '暂无'}\n"
            f"邮箱：{email if email else '暂无'}\n"
            f"地址：{address if address else '暂无'}\n"
            f"身份证号：{id_card if id_card else '未填写'}"
        )
        elements.append(Paragraph(contact_info, normal_style))
        elements.append(Spacer(1, 10))

        elements.append(Paragraph("毕业信息", sub_title_style))
        elements.append(Paragraph(f"毕业院校及时间：{grad_info}", normal_style))
        elements.append(Spacer(1, 10))

        elements.append(Paragraph("专业技能", sub_title_style))
        skill_text = "、".join(skills) if skills else "暂未填写"
        elements.append(Paragraph(skill_text, normal_style))
        elements.append(Spacer(1, 10))

        elements.append(Paragraph("个人经历", sub_title_style))
        if experience.strip():
            exp_lines = [line.strip() for line in experience.strip().split('\n') if line.strip()]
            exp_text = "\n".join(exp_lines)
            elements.append(Paragraph(exp_text, normal_style))
        else:
            elements.append(Paragraph("暂未填写", normal_style))
        elements.append(Spacer(1, 10))

        elements.append(Paragraph("个人简介", sub_title_style))
        intro_text = intro if intro else "✨ 这个人很温柔，还没有留下介绍哦～"
        elements.append(Paragraph(intro_text, normal_style))

        if avatar is not None:
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                    img = PILImage.open(avatar)
                    img.thumbnail((150, 150))
                    img.save(tmp_file, format='PNG')
                    tmp_file_path = tmp_file.name
                
                elements.append(Spacer(1, 15))
                elements.append(Image(tmp_file_path, width=1.5*inch, height=1.5*inch))
                os.unlink(tmp_file_path)  # 清理临时文件
            except Exception as e:
                st.warning(f"头像添加失败: {str(e)}")

        doc.build(elements)
        buffer.seek(0)
        return buffer

    # 页面标题
    st.title("🐾 宠物简历服务")
    st.write("填写以下信息，生成专业的宠物简历")

    # 表单布局
    col_left, col_right = st.columns([3, 2])

    with col_left:
        # 基本信息
        st.subheader("🐾 基本信息")
        st.text_input("宠物姓名", key="pet_resume_name")
        st.text_input("宠物昵称", key="pet_resume_nickname")
        
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.date_input("出生日期", key="pet_resume_birth_date")
        with col_b2:
            st.selectbox("性别", ["男", "女", "未知"], key="pet_resume_gender")
        
        st.selectbox("品种", ["金毛", "拉布拉多", "泰迪", "柯基", "其他"], key="pet_resume_education")
        st.slider("年龄（岁）", 0, 20, 2, key="pet_resume_work_exp")

        # 技能特长
        st.subheader("🐾 技能特长")
        st.multiselect(
            "掌握技能",
            ["握手", "坐下", "卧倒", "装死", "巡回", "叫", "安静", "其他"],
            key="pet_resume_skills"
        )
        st.text_input("其他技能", key="pet_resume_custom_skills")

        # 个人经历
        st.subheader("🐾 成长经历")
        st.text_area("请描述宠物的成长经历、性格特点等", key="pet_resume_experience", height=150)

        # 个人简介
        st.subheader("🐾 宠物简介")
        st.text_area("请简要介绍您的宠物", key="pet_resume_intro", height=100)

    with col_right:
        # 预览区域
        st.subheader("📋 简历预览")
        with st.container():
            st.markdown(f"""
            <div class='preview-card'>
                <h3>{st.session_state.pet_resume_name or '宠物姓名'}</h3>
                <p>昵称：{st.session_state.pet_resume_nickname or '未填写'} | 
                出生日期：{st.session_state.pet_resume_birth_date} | 
                性别：{st.session_state.pet_resume_gender}</p>
                <p>品种：{st.session_state.pet_resume_education} | 
                年龄：{st.session_state.pet_resume_work_exp}岁</p>
                
                <hr>
                <h4>技能特长</h4>
                <p>{', '.join(st.session_state.pet_resume_skills) or '未填写'}</p>
                
                <hr>
                <h4>简介</h4>
                <p>{st.session_state.pet_resume_intro or '暂无介绍'}</p>
            </div>
            """, unsafe_allow_html=True)

        # 上传头像
        st.subheader("🖼️ 上传宠物照片")
        st.file_uploader(
            "选择照片", 
            type=["jpg", "jpeg", "png"],
            key=f"pet_resume_avatar_uploader_{st.session_state.pet_resume_avatar_uploader_key}",
            on_change=lambda: setattr(st.session_state, "pet_resume_avatar", st.session_state[f"pet_resume_avatar_uploader_{st.session_state.pet_resume_avatar_uploader_key}"])
        )

        # 生成PDF按钮
        st.subheader("📥 生成简历")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            generate_pdf = st.button("生成PDF简历", use_container_width=True)
        with col_btn2:
            reset_btn = st.button("重置信息", use_container_width=True, type="secondary")

        if reset_btn:
            force_reset_all()

        if generate_pdf:
            with st.spinner("正在生成简历..."):
                pdf_buffer = generate_resume_pdf(
                    st.session_state.pet_resume_name,
                    st.session_state.pet_resume_nickname,
                    st.session_state.pet_resume_birth_date,
                    st.session_state.pet_resume_gender,
                    st.session_state.pet_resume_education,
                    st.session_state.pet_resume_work_exp,
                    st.session_state.pet_resume_salary_range[0],
                    st.session_state.pet_resume_salary_range[1],
                    st.session_state.pet_resume_grad_info,
                    st.session_state.pet_resume_job_intention,
                    st.session_state.pet_resume_job_city,
                    st.session_state.pet_resume_arrival_time,
                    st.session_state.pet_resume_phone,
                    st.session_state.pet_resume_email,
                    st.session_state.pet_resume_address,
                    st.session_state.pet_resume_id_card,
                    st.session_state.pet_resume_skills,
                    st.session_state.pet_resume_experience,
                    st.session_state.pet_resume_intro,
                    st.session_state.pet_resume_avatar
                )
                
                st.download_button(
                    label="下载PDF简历",
                    data=pdf_buffer,
                    file_name=f"{st.session_state.pet_resume_name or '宠物'}_简历.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

with tab5:
    # 宠物趣味视频原代码（略，与之前一致）
    # 自定义CSS
    st.markdown("""
    <style>
    /* 全局页面背景：设置猫和老鼠主题图片背景 */
    .stApp {
        background-image: url("https://pic1.zhimg.com/v2-d512738bfdea04b3c37541b3da7bb9da_r.jpg?source=1940ef5c");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center center;
    }

    /* 内容容器：半透明背景增强可读性 */
    .block-container {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(74, 144, 226, 0.4);
        margin: 20px auto;
        max-width: 800px;
    }

    /* 标题样式 */
    h1 {
        color: #2A76C8;
        text-align: center;
        font-family: "微软雅黑", sans-serif;
        font-weight: bold;
        text-shadow: 2px 2px 3px rgba(0, 0, 0, 0.15);
        margin-bottom: 20px;
    }

    /* 剧集按钮样式 */
    .stButton>button {
        background-color: #4A90E2;
        color: white;
        width: 100%;
        border-radius: 8px;
        margin: 5px 0;
        font-size: 16px;
        border: none;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    .stButton>button:hover {
        background-color: #357ABD;
        transform: scale(1.02);
    }

    /* 视频容器样式 */
    div[data-testid="stVideo"] {
        border: 3px solid #FFD700;
        border-radius: 10px;
        padding: 5px;
        background-color: white;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }

    /* 剧情介绍卡片样式 */
    .plot-card {
        background-color: #F0F8FF;
        border-left: 4px solid #4A90E2;
        padding: 10px 15px;
        margin-top: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    }

    h3, h4 {
        color: #2A76C8;
        font-family: "微软雅黑", sans-serif;
    }

    /* 移除默认空白背景 */
    .main {
        background: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # 猫和老鼠视频+剧情介绍列表
    video_list = [
        {
            "url": "https://www.w3school.com.cn/example/html5/mov_bbb.mp4",
            "title": "第1集：奶酪大作战",
            "episode": 1,
            "plot": "杰瑞偷偷潜入汤姆的厨房偷奶酪，汤姆布下重重陷阱想要抓住杰瑞，却屡次被聪明的杰瑞反套路，不仅没抓到杰瑞，还把厨房搞得一团糟，最后被主人训斥，杰瑞则抱着奶酪在洞里得意洋洋～"
        },
        {
            "url": "https://www.w3schools.com/html/movie.mp4",
            "title": "第2集：汤姆的陷阱",
            "episode": 2,
            "plot": "汤姆为了抓住总偷吃东西的杰瑞，精心设计了一个复杂的奶酪陷阱，本以为万无一失，结果陷阱却频频失灵，反而把自己困在里面，杰瑞还趁机捉弄汤姆，最后汤姆只能眼睁睁看着杰瑞带着奶酪溜走。"
        },
        {
            "url": "https://media.w3.org/2010/05/sintel/trailer.mp4",
            "title": "第3集：杰瑞的反击",
            "episode": 3,
            "plot": "汤姆被主人要求看好新买的鱼缸，却总想着抓杰瑞，不小心把鱼缸打翻，为了掩盖错误汤姆试图糊弄主人，杰瑞看穿后故意捣乱，让汤姆一次次出糗，最后杰瑞还帮主人找回了小鱼，汤姆则被罚打扫卫生。"
        },
        {
            "url": "https://v-cdn.zjol.com.cn/280446.mp4",
            "title": "第4集：猫狗联盟",
            "episode": 4,
            "plot": "家里来了一只凶巴巴的流浪狗，汤姆和杰瑞都被欺负得团团转，为了赶走这只狗，原本针锋相对的汤姆和杰瑞首次联手，想出各种妙招捉弄流浪狗，最后成功把它赶出门，不过刚消停，俩活宝又开始互相打闹～"
        },
        {
            "url": "https://v-cdn.zjol.com.cn/280447.mp4",
            "title": "第5集：太空大冒险",
            "episode": 5,
            "plot": "汤姆意外被送上了去往太空的火箭，杰瑞也不小心跟着溜上了船，在失重的太空舱里，汤姆依旧想抓杰瑞，结果闹出各种爆笑笑话，还不小心触发了火箭的各种按钮，最后俩家伙靠着误打误撞成功返回地球。"
        }
    ]

    # 初始化会话状态（使用带前缀的键避免冲突）
    if "pet_video_current_episode" not in st.session_state:
        st.session_state.pet_video_current_episode = 0

    # 切换剧集函数
    def switch_episode(index):
        st.session_state.pet_video_current_episode = index

    # 页面标题
    st.title("🐱🐭 猫和老鼠 - 经典剧集 🐭🐱")

    # 播放当前选中的视频
    current_video = video_list[st.session_state.pet_video_current_episode]
    st.info(f"正在播放：{current_video['title']}")
    st.video(
        data=current_video["url"],
        format="video/mp4",
        start_time=0,
        autoplay=False
    )

    # 显示当前剧集的剧情介绍
    st.markdown(f"""
    <div class='plot-card'>
        <h4>📖 剧情介绍</h4>
        <p>{current_video['plot']}</p>
    </div>
    """, unsafe_allow_html=True)

    # 剧集选择区域
    st.write("### 选择剧集")
    for idx, video in enumerate(video_list):
        st.button(
            label=video["title"],
            on_click=switch_episode,
            args=(idx,)
        )