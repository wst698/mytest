import streamlit as st
import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io
from PIL import Image as PILImage

# 设置页面配置
st.set_page_config(
    page_title="个人简历生成器",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定义浅色系样式（莫兰迪色系，柔和清新）
st.markdown("""
    <style>
    /* 整体页面样式 */
    .stApp { 
        background-color: #F9F7F8; 
        color: #4A4A4A; 
        font-family: "Microsoft YaHei", sans-serif;
    }
    /* 输入框/下拉框样式 */
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
    /* 滑块样式 */
    .stSlider > div > div > div { color: #9D6588; }
    .stSlider [data-baseweb="slider"] { color: #D88FB9; }
    /* 按钮样式（柔和粉色） */
    .stButton > button { 
        background-color: #E899AF; 
        color: white; 
        border: none;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 500;
    }
    .stButton > button:hover { background-color: #D88FB9; }
    /* 单选框/多选框样式 */
    .stRadio > div > label, .stMultiSelect > div > label { color: #6B5B6B; }
    /* 预览卡片（米白底色+浅粉边框） */
    .preview-card { 
        background-color: #FFFFFF; 
        padding: 30px; 
        border-radius: 12px;
        border: 1px solid #F0E0E6;
        box-shadow: 0 2px 10px rgba(222, 200, 210, 0.1);
    }
    /* 标题样式 */
    h1, h2, h3 { color: #8B6B89; }
    .stCaption { color: #9A8B98; }
    /* 分割线样式 */
    hr { border-top: 1px solid #F0E0E6; }
    /* 经历卡片样式 */
    .experience-card {
        background-color: #F9F7F8;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 8px;
        border-left: 3px solid #D88FB9;
    }
    </style>
""", unsafe_allow_html=True)

# 生成PDF简历的函数
def generate_resume_pdf(name, nickname, birth_date, gender, education, work_exp, 
                       salary_min, salary_max, grad_info, job_intention, job_city, 
                       arrival_time, phone, email, address, id_card, skills, experience, intro, avatar):
    # 创建内存缓冲区
    buffer = io.BytesIO()
    
    # 创建PDF文档
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                           rightMargin=inch/2, leftMargin=inch/2,
                           topMargin=inch/2, bottomMargin=inch/2)
    elements = []
    styles = getSampleStyleSheet()
    
    # 自定义样式
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=10,
        textColor=colors.Color(139/255, 107/255, 137/255)  # #8B6B89
    )
    
    sub_title_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=8,
        textColor=colors.Color(139/255, 107/255, 137/255)
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=5,
        textColor=colors.Color(74/255, 74/255, 74/255)  # #4A4A4A
    )
    
    # 1. 姓名和基本信息
    name_text = name if name else "你的姓名"
    elements.append(Paragraph(name_text, title_style))
    
    # 基本信息行
    basic_info = f"昵称：{nickname if nickname else '暂无'} | {birth_date.strftime('%Y年%m月')}出生 | 性别：{gender} | 学历：{education}"
    elements.append(Paragraph(basic_info, normal_style))
    elements.append(Spacer(1, 10))
    
    # 2. 求职意向
    elements.append(Paragraph("求职意向", sub_title_style))
    intention_info = f"""
    意向岗位：{job_intention if job_intention else '暂无'}<br/>
    意向城市：{', '.join(job_city) if job_city else '暂无'}<br/>
    到岗时间：{arrival_time}<br/>
    期望薪资：{salary_min}-{salary_max}元/月 | 工作经验：{work_exp}年
    """
    elements.append(Paragraph(intention_info, normal_style))
    elements.append(Spacer(1, 10))
    
    # 3. 联系方式
    elements.append(Paragraph("联系方式", sub_title_style))
    contact_info = f"""
    电话：{phone if phone else '暂无'}<br/>
    邮箱：{email if email else '暂无'}<br/>
    地址：{address if address else '暂无'}<br/>
    身份证号：{id_card if id_card else '未填写'}
    """
    elements.append(Paragraph(contact_info, normal_style))
    elements.append(Spacer(1, 10))
    
    # 4. 毕业信息
    elements.append(Paragraph("毕业信息", sub_title_style))
    elements.append(Paragraph(f"毕业院校及时间：{grad_info}", normal_style))
    elements.append(Spacer(1, 10))
    
    # 5. 专业技能
    elements.append(Paragraph("专业技能", sub_title_style))
    if skills:
        skill_text = "、".join(skills)
    else:
        skill_text = "暂未填写"
    elements.append(Paragraph(skill_text, normal_style))
    elements.append(Spacer(1, 10))
    
    # 6. 个人经历
    elements.append(Paragraph("个人经历", sub_title_style))
    if experience.strip():
        exp_lines = [line.strip() for line in experience.strip().split('\n') if line.strip()]
        for line in exp_lines:
            elements.append(Paragraph(line, normal_style))
    else:
        elements.append(Paragraph("暂未填写", normal_style))
    elements.append(Spacer(1, 10))
    
    # 7. 个人简介
    elements.append(Paragraph("个人简介", sub_title_style))
    intro_text = intro if intro else "✨ 这个人很温柔，还没有留下介绍哦～"
    elements.append(Paragraph(intro_text, normal_style))
    
    # 生成PDF
    doc.build(elements)
    
    # 重置缓冲区指针
    buffer.seek(0)
    return buffer

# 页面标题
st.title("👩‍🎓 个人简历生成器（女生版）")
st.caption("基于Streamlit的清新系简历制作工具")

# 分栏：左侧表单（更紧凑），右侧预览（更精致）
col1, col2 = st.columns([1, 1.3])

with col1:
    st.subheader("📝 个人信息填写")
    
    # 基础信息（增加emoji装饰）
    name = st.text_input("姓名", placeholder="请输入你的姓名")
    nickname = st.text_input("昵称/艺名", placeholder="可选，如：小桃、Lily")
    phone = st.text_input("📱 联系电话", placeholder="请输入常用手机号")
    email = st.text_input("✉️ 电子邮箱", placeholder="请输入常用邮箱")
    address = st.text_input("📍 居住地址", placeholder="如：XX市XX区XX路")
    id_card = st.text_input("🆔 身份证号", placeholder="可选，谨慎填写")
    
    # 出生日期（默认2000年，样式更柔和）
    birth_date = st.date_input(
        "🎂 出生日期", 
        datetime.date(2000, 1, 1),
        format="YYYY-MM-DD"
    )
    
    # 性别、学历（选项更友好）
    gender = st.radio("👧 性别", ["女", "男", "其他"], horizontal=True)
    education = st.selectbox(
        "🎓 最高学历", 
        ["本科", "专科", "硕士", "博士", "高中及以下"],
        index=0
    )
    
    # 技能选择（增加女性求职高频技能）
    skills = st.multiselect(
        "💻 掌握技能", 
        [
            "HTML/CSS", "JavaScript", "Python", "Java", 
            "数据分析", "UI/UX设计", "新媒体运营", "文案策划",
            "人力资源管理", "财务会计", "行政办公", "客户服务",
            "电商运营", "视频剪辑", "插画设计", "英语口译"
        ],
        default=["UI/UX设计", "新媒体运营"]
    )
    
    # 工作经验（滑块范围调整，更贴合应届生/职场新人）
    work_exp = st.slider("💼 工作经验（年）", 0, 10, 0)
    
    # 薪资期望（范围滑块，默认更贴合女性求职区间）
    salary_min, salary_max = st.slider(
        "💰 期望薪资范围（元/月）",
        min_value=3000,
        max_value=50000,
        value=(8000, 12000)
    )
    
    # 毕业信息（样式优化）
    grad_info = st.selectbox(
        "🎓 毕业院校及时间", 
        ["2024届 某某大学 某某专业", "2023届 某某大学 某某专业", "2022届 某某大学 某某专业", "自定义"],
        index=0
    )
    if grad_info == "自定义":
        grad_info = st.text_input("请输入毕业院校及时间", placeholder="如：2024届 北京师范大学 汉语言文学")
    
    # 新增：求职意向模块
    st.subheader("🎯 求职意向")
    job_intention = st.selectbox(
        "意向岗位",
        [
            "新媒体运营", "UI/UX设计师", "行政专员", "人力资源专员",
            "电商运营", "文案策划", "财务会计", "客户服务",
            "视频剪辑师", "插画设计师", "英语翻译", "数据分析专员",
            "自定义"
        ],
        index=0
    )
    # 自定义意向岗位
    if job_intention == "自定义":
        job_intention = st.text_input("请输入自定义意向岗位", placeholder="如：小红书内容运营、品牌策划")
    
    # 意向工作城市
    job_city = st.multiselect(
        "意向工作城市",
        ["北京", "上海", "广州", "深圳", "杭州", "成都", "南京", "武汉", "重庆", "西安", "其他"],
        default=["北京", "上海"]
    )
    # 自定义工作城市
    custom_city = ""
    if "其他" in job_city:
        custom_city = st.text_input("请输入其他意向城市", placeholder="如：苏州、厦门")
        job_city = [city for city in job_city if city != "其他"] + ([custom_city] if custom_city else [])
    
    # 到岗时间
    arrival_time = st.selectbox(
        "期望到岗时间",
        ["随时到岗", "1周内", "2周内", "1个月内", "待定"],
        index=0
    )
    
    # 个人经历填写
    st.markdown("---")
    st.subheader("📜 个人经历")
    experience = st.text_area(
        "工作/实习/项目经历",
        placeholder="请按以下格式填写（每行一条经历）：\n2023.07-2024.02 XX公司 新媒体运营 主要负责小红书内容创作，月均涨粉500+，策划爆款笔记10篇\n2022.09-2023.06 XX大学 学生会宣传部部长 组织校园文创活动，参与人数超500人...",
        height=150
    )
    
    # 个人简介（提示语更温柔）
    intro = st.text_area(
        "💬 个人简介", 
        placeholder="请简要介绍你的专业背景、职业目标和个人特点～\n比如：擅长新媒体内容创作，有2年小红书运营经验，审美在线，执行力强...",
        height=120
    )
    
    # 头像上传（提示更友好）
    avatar = st.file_uploader(
        "🖼️ 上传个人照片（可选）", 
        type=["jpg", "jpeg", "png"],
        help="建议上传清晰的正面照/生活照，尺寸1:1最佳"
    )

with col2:
    st.subheader("✨ 简历实时预览")
    # 预览卡片（浅色系样式）
    with st.container(border=True):
        st.markdown('<div class="preview-card">', unsafe_allow_html=True)
        
        # 预览头部（更精致）
        st.markdown(
            f"<h3 style='color:#8B6B89; margin-bottom: 8px;'>{name if name else '你的姓名'}</h3>", 
            unsafe_allow_html=True
        )
        st.caption(f"昵称：{nickname if nickname else '暂无'} | {birth_date.strftime('%Y年%m月')}出生")
        
        # 头像+核心信息栏（布局更美观）
        info_col1, info_col2 = st.columns([0.3, 0.7])
        with info_col1:
            # 头像占位（女生风格头像）
            if avatar:
                st.image(avatar, width=120, caption="个人照片")
            else:
                st.image(
                    "https://api.dicebear.com/7.x/avataaars-neutral/svg?seed=girl&accessories=round&hair=longStraight&clothes=blazerShirt",
                    width=120,
                    caption="头像占位"
                )
        with info_col2:
            st.markdown(f"<p>👧 性别：{gender}</p>", unsafe_allow_html=True)
            st.markdown(f"<p>🎓 学历：{education}</p>", unsafe_allow_html=True)
            st.markdown(f"<p>💼 工作经验：{work_exp}年</p>", unsafe_allow_html=True)
            st.markdown(f"<p>💰 期望薪资：{salary_min}-{salary_max}元/月</p>", unsafe_allow_html=True)
            st.markdown(f"<p>🎓 毕业信息：{grad_info}</p>", unsafe_allow_html=True)
        
        # 新增：求职意向预览
        st.markdown("---")
        st.subheader("🎯 求职意向", anchor=False)
        intention_col1, intention_col2, intention_col3 = st.columns(3)
        with intention_col1:
            st.markdown(f"<p><strong>意向岗位：</strong>{job_intention if job_intention else '暂无'}</p>", unsafe_allow_html=True)
        with intention_col2:
            st.markdown(f"<p><strong>意向城市：</strong>{', '.join(job_city) if job_city else '暂无'}</p>", unsafe_allow_html=True)
        with intention_col3:
            st.markdown(f"<p><strong>到岗时间：</strong>{arrival_time}</p>", unsafe_allow_html=True)
        
        # 联系方式（排版更整洁）
        st.markdown("---")
        st.subheader("📞 联系方式", anchor=False)
        contact_col1, contact_col2 = st.columns(2)
        with contact_col1:
            st.write(f"电话：{phone if phone else '暂无'}")
            st.write(f"邮箱：{email if email else '暂无'}")
        with contact_col2:
            st.write(f"地址：{address if address else '暂无'}")
            st.write(f"身份证号：{id_card if id_card else '未填写'}")
        
        # 技能展示（标签化样式）
        st.markdown("---")
        st.subheader("💻 专业技能", anchor=False)
        if skills:
            # 技能标签化展示（更美观）
            skill_tags = " ".join([f"<span style='background-color:#F0E0E6; color:#8B6B89; padding:4px 10px; border-radius:20px; margin:0 5px 5px 0; display:inline-block;'>{skill}</span>" for skill in skills])
            st.markdown(skill_tags, unsafe_allow_html=True)
        else:
            st.write("暂未填写技能信息，快去左侧选择吧～")
        
        # 个人经历预览
        st.markdown("---")
        st.subheader("📜 个人经历", anchor=False)
        if experience.strip():
            # 按行拆分经历并格式化展示
            exp_lines = [line.strip() for line in experience.strip().split('\n') if line.strip()]
            for line in exp_lines:
                st.markdown(f"<div class='experience-card'>{line}</div>", unsafe_allow_html=True)
        else:
            st.write("暂未填写个人经历，快去左侧补充吧～")
        
        # 个人简介（样式优化）
        st.markdown("---")
        st.subheader("💬 个人简介", anchor=False)
        st.write(intro if intro else "✨ 这个人很温柔，还没有留下介绍哦～")
        
        st.markdown('</div>', unsafe_allow_html=True)

# 底部操作按钮（下载/重置）
st.markdown("---")
btn_col1, btn_col2 = st.columns([0.1, 0.9])
with btn_col1:
    # 生成PDF并提供下载
    if st.button("📥 导出简历", use_container_width=True):
        # 生成PDF文件
        pdf_buffer = generate_resume_pdf(
            name, nickname, birth_date, gender, education, work_exp,
            salary_min, salary_max, grad_info, job_intention, job_city,
            arrival_time, phone, email, address, id_card, skills,
            experience, intro, avatar
        )
        
        # 设置下载文件名
        file_name = f"{name if name else '个人简历'}_{datetime.datetime.now().strftime('%Y%m%d')}.pdf"
        
        # 提供下载按钮
        st.download_button(
            label="下载PDF简历",
            data=pdf_buffer,
            file_name=file_name,
            mime="application/pdf",
            use_container_width=True
        )
        st.success("✅ 简历已生成，点击按钮即可下载！")

with btn_col2:
    # 重置表单功能
    if st.button("🔄 重置表单", use_container_width=True):
        # 重置所有输入项（通过刷新页面实现）
        st.rerun()