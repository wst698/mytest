import streamlit as st
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

# ===================== 核心修复：注册中文字体 =====================
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

# ===================== 页面配置 & 样式 =====================
st.set_page_config(
    page_title="个人简历生成器",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

# ===================== 强制重置所有会话状态（核心修复） =====================
def force_reset_all():
    """强制重置所有会话状态，包括隐藏的临时状态"""
    # 清空所有会话状态
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    # 重新初始化默认值
    default_vals = {
        "name": "",
        "nickname": "",
        "phone": "",
        "email": "",
        "address": "",
        "id_card": "",
        "birth_date": datetime.date(2000, 1, 1),
        "gender": "女",
        "education": "本科",
        "skills": ["UI/UX设计", "新媒体运营"],
        "work_exp": 0,
        "salary_range": (8000, 12000),
        "grad_info": "2024届 某某大学 某某专业",
        "grad_info_custom": "",
        "job_intention": "新媒体运营",
        "job_intention_custom": "",
        "job_city": ["北京", "上海"],
        "custom_city": "",
        "arrival_time": "随时到岗",
        "experience": "",
        "intro": "",
        "avatar": None,
        "reset_confirm": False,
        "avatar_uploader_key": 0  # 强制重置上传器key
    }
    
    # 重新赋值所有默认值
    for key, val in default_vals.items():
        st.session_state[key] = val
    
    # 强制刷新页面（最高优先级）
    st.experimental_set_query_params(reset="true")
    st.toast("⚡ 所有信息已强制重置为默认值！", icon="🔥")

# ===================== 初始化会话状态 =====================
def init_session_state():
    """初始化所有表单项的默认值到会话状态"""
    default_vals = {
        "name": "",
        "nickname": "",
        "phone": "",
        "email": "",
        "address": "",
        "id_card": "",
        "birth_date": datetime.date(2000, 1, 1),
        "gender": "女",
        "education": "本科",
        "skills": ["UI/UX设计", "新媒体运营"],
        "work_exp": 0,
        "salary_range": (8000, 12000),
        "grad_info": "2024届 某某大学 某某专业",
        "grad_info_custom": "",
        "job_intention": "新媒体运营",
        "job_intention_custom": "",
        "job_city": ["北京", "上海"],
        "custom_city": "",
        "arrival_time": "随时到岗",
        "experience": "",
        "intro": "",
        "avatar": None,
        "reset_confirm": False,
        "avatar_uploader_key": 0
    }
    for key, val in default_vals.items():
        if key not in st.session_state:
            st.session_state[key] = val

# 执行初始化
init_session_state()

# ===================== PDF生成函数 =====================
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
            img_obj = Image(tmp_file_path, width=1.5*inch, height=1.5*inch)
            img_obj.hAlign = 'RIGHT'
            elements.append(img_obj)
            
            os.unlink(tmp_file_path)
        except Exception as e:
            st.warning(f"头像处理失败：{str(e)}")

    try:
        doc.build(elements)
    except Exception as e:
        st.error(f"PDF生成失败：{str(e)}")
        return None

    buffer.seek(0)
    return buffer

# ===================== 页面UI布局 =====================
st.title("👩‍🎓 个人简历生成器（女生版）")
st.caption("基于Streamlit的清新系简历制作工具")

# ===================== 一键重置按钮（核心修复） =====================
if st.button("⚡ 一键重置所有信息", type="primary", key="quick_reset", 
            help="强制清空所有内容，恢复初始状态", 
            use_container_width=True):
    force_reset_all()
    # 双重刷新确保生效
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

# 实时计算所有动态字段（确保重置后同步）
salary_min, salary_max = st.session_state.salary_range
grad_info = st.session_state.grad_info_custom if st.session_state.grad_info == "自定义" else st.session_state.grad_info
job_intention = st.session_state.job_intention_custom if st.session_state.job_intention == "自定义" else st.session_state.job_intention
job_city = [city for city in st.session_state.job_city if city != "其他"] + ([st.session_state.custom_city] if st.session_state.custom_city and "其他" in st.session_state.job_city else [])

col1, col2 = st.columns([1, 1.3])

with col1:
    st.subheader("📝 个人信息填写")
    
    # 所有输入框强制绑定会话状态（重置后立即同步）
    st.session_state.name = st.text_input("姓名", placeholder="请输入你的姓名", value=st.session_state.name, key="name_input")
    st.session_state.nickname = st.text_input("昵称/艺名", placeholder="可选，如：小桃、Lily", value=st.session_state.nickname, key="nickname_input")
    st.session_state.phone = st.text_input("📱 联系电话", placeholder="请输入常用手机号", value=st.session_state.phone, key="phone_input")
    st.session_state.email = st.text_input("✉️ 电子邮箱", placeholder="请输入常用邮箱", value=st.session_state.email, key="email_input")
    st.session_state.address = st.text_input("📍 居住地址", placeholder="如：XX市XX区XX路", value=st.session_state.address, key="address_input")
    st.session_state.id_card = st.text_input("🆔 身份证号", placeholder="可选，谨慎填写", value=st.session_state.id_card, key="id_card_input")
    
    st.session_state.birth_date = st.date_input(
        "🎂 出生日期", 
        value=st.session_state.birth_date,
        format="YYYY-MM-DD",
        key="birth_date_input"
    )
    
    st.session_state.gender = st.radio("👧 性别", ["女", "男", "其他"], horizontal=True, 
                                      index=["女", "男", "其他"].index(st.session_state.gender),
                                      key="gender_radio")
    
    st.session_state.education = st.selectbox(
        "🎓 最高学历", 
        ["本科", "专科", "硕士", "博士", "高中及以下"],
        index=["本科", "专科", "硕士", "博士", "高中及以下"].index(st.session_state.education),
        key="education_select"
    )
    
    st.session_state.skills = st.multiselect(
        "💻 掌握技能", 
        [
            "HTML/CSS", "JavaScript", "Python", "Java", 
            "数据分析", "UI/UX设计", "新媒体运营", "文案策划",
            "人力资源管理", "财务会计", "行政办公", "客户服务",
            "电商运营", "视频剪辑", "插画设计", "英语口译"
        ],
        default=st.session_state.skills,
        key="skills_multiselect"
    )
    
    st.session_state.work_exp = st.slider("💼 工作经验（年）", 0, 10, 
                                         value=st.session_state.work_exp,
                                         key="work_exp_slider")
    
    st.session_state.salary_range = st.slider(
        "💰 期望薪资范围（元/月）",
        min_value=3000,
        max_value=50000,
        value=st.session_state.salary_range,
        key="salary_slider"
    )
    
    st.session_state.grad_info = st.selectbox(
        "🎓 毕业院校及时间", 
        ["2024届 某某大学 某某专业", "2023届 某某大学 某某专业", "2022届 某某大学 某某专业", "自定义"],
        index=["2024届 某某大学 某某专业", "2023届 某某大学 某某专业", "2022届 某某大学 某某专业", "自定义"].index(st.session_state.grad_info),
        key="grad_info_select"
    )
    
    if st.session_state.grad_info == "自定义":
        st.session_state.grad_info_custom = st.text_input("请输入毕业院校及时间", 
                                                        placeholder="如：2024届 北京师范大学 汉语言文学", 
                                                        value=st.session_state.grad_info_custom,
                                                        key="grad_info_custom_input")
    
    st.subheader("🎯 求职意向")
    st.session_state.job_intention = st.selectbox(
        "意向岗位",
        [
            "新媒体运营", "UI/UX设计师", "行政专员", "人力资源专员",
            "电商运营", "文案策划", "财务会计", "客户服务",
            "视频剪辑师", "插画设计师", "英语翻译", "数据分析专员",
            "自定义"
        ],
        index=["新媒体运营", "UI/UX设计师", "行政专员", "人力资源专员",
               "电商运营", "文案策划", "财务会计", "客户服务",
               "视频剪辑师", "插画设计师", "英语翻译", "数据分析专员",
               "自定义"].index(st.session_state.job_intention),
        key="job_intention_select"
    )
    
    if st.session_state.job_intention == "自定义":
        st.session_state.job_intention_custom = st.text_input("请输入自定义意向岗位", 
                                                             placeholder="如：小红书内容运营、品牌策划", 
                                                             value=st.session_state.job_intention_custom,
                                                             key="job_intention_custom_input")
    
    st.session_state.job_city = st.multiselect(
        "意向工作城市",
        ["北京", "上海", "广州", "深圳", "杭州", "成都", "南京", "武汉", "重庆", "西安", "其他"],
        default=st.session_state.job_city,
        key="job_city_multiselect"
    )
    
    if "其他" in st.session_state.job_city:
        st.session_state.custom_city = st.text_input("请输入其他意向城市", 
                                                    placeholder="如：苏州、厦门", 
                                                    value=st.session_state.custom_city,
                                                    key="custom_city_input")
    
    st.session_state.arrival_time = st.selectbox(
        "期望到岗时间",
        ["随时到岗", "1周内", "2周内", "1个月内", "待定"],
        index=["随时到岗", "1周内", "2周内", "1个月内", "待定"].index(st.session_state.arrival_time),
        key="arrival_time_select"
    )
    
    st.markdown("---")
    st.subheader("📜 个人经历")
    st.session_state.experience = st.text_area(
        "工作/实习/项目经历",
        placeholder="请按以下格式填写（每行一条经历）：\n2023.07-2024.02 XX公司 新媒体运营 主要负责小红书内容创作，月均涨粉500+，策划爆款笔记10篇\n2022.09-2023.06 XX大学 学生会宣传部部长 组织校园文创活动，参与人数超500人...",
        height=150,
        value=st.session_state.experience,
        key="experience_textarea"
    )
    
    st.subheader("💬 个人简介")
    st.session_state.intro = st.text_area(
        "", 
        placeholder="请简要介绍你的专业背景、职业目标和个人特点～\n比如：擅长新媒体内容创作，有2年小红书运营经验，审美在线，执行力强...",
        height=120,
        value=st.session_state.intro,
        key="intro_textarea"
    )
    
    # 头像上传器强制重置key
    st.session_state.avatar = st.file_uploader(
        "🖼️ 上传个人照片（可选）", 
        type=["jpg", "jpeg", "png"],
        help="建议上传清晰的正面照/生活照，尺寸1:1最佳",
        key=f"avatar_uploader_{st.session_state['avatar_uploader_key']}"
    )

with col2:
    st.subheader("✨ 简历实时预览")
    with st.container(border=True):
        st.markdown('<div class="preview-card">', unsafe_allow_html=True)
        
        st.markdown(
            f"<h3 style='color:#8B6B89; margin-bottom: 8px;'>{st.session_state.name if st.session_state.name else '你的姓名'}</h3>", 
            unsafe_allow_html=True
        )
        st.caption(f"昵称：{st.session_state.nickname if st.session_state.nickname else '暂无'} | {st.session_state.birth_date.strftime('%Y年%m月')}出生")
        
        info_col1, info_col2 = st.columns([0.3, 0.7])
        with info_col1:
            if st.session_state.avatar:
                st.image(st.session_state.avatar, width=120, caption="个人照片")
            else:
                st.image(
                    "https://api.dicebear.com/7.x/avataaars-neutral/svg?seed=girl&accessories=round&hair=longStraight&clothes=blazerShirt",
                    width=120,
                    caption="头像占位"
                )
        with info_col2:
            st.markdown(f"<p>👧 性别：{st.session_state.gender}</p>", unsafe_allow_html=True)
            st.markdown(f"<p>🎓 学历：{st.session_state.education}</p>", unsafe_allow_html=True)
            st.markdown(f"<p>💼 工作经验：{st.session_state.work_exp}年</p>", unsafe_allow_html=True)
            st.markdown(f"<p>💰 期望薪资：{salary_min}-{salary_max}元/月</p>", unsafe_allow_html=True)
            st.markdown(f"<p>🎓 毕业信息：{grad_info}</p>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("🎯 求职意向", anchor=False)
        intention_col1, intention_col2, intention_col3 = st.columns(3)
        with intention_col1:
            st.markdown(f"<p><strong>意向岗位：</strong>{job_intention if job_intention else '暂无'}</p>", unsafe_allow_html=True)
        with intention_col2:
            st.markdown(f"<p><strong>意向城市：</strong>{', '.join(job_city) if job_city else '暂无'}</p>", unsafe_allow_html=True)
        with intention_col3:
            st.markdown(f"<p><strong>到岗时间：</strong>{st.session_state.arrival_time}</p>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("📞 联系方式", anchor=False)
        contact_col1, contact_col2 = st.columns(2)
        with contact_col1:
            st.write(f"电话：{st.session_state.phone if st.session_state.phone else '暂无'}")
            st.write(f"邮箱：{st.session_state.email if st.session_state.email else '暂无'}")
        with contact_col2:
            st.write(f"地址：{st.session_state.address if st.session_state.address else '暂无'}")
            st.write(f"身份证号：{st.session_state.id_card if st.session_state.id_card else '未填写'}")
        
        st.markdown("---")
        st.subheader("💻 专业技能", anchor=False)
        if st.session_state.skills:
            skill_tags = " ".join([
                f"<span style='background-color:#F0E0E6; color:#8B6B89; padding:4px 10px; border-radius:20px; margin:0 5px 5px 0; display:inline-block;'>{skill}</span>" 
                for skill in st.session_state.skills
            ])
            st.markdown(skill_tags, unsafe_allow_html=True)
        else:
            st.write("暂未填写技能信息，快去左侧选择吧～")
        
        st.markdown("---")
        st.subheader("📜 个人经历", anchor=False)
        if st.session_state.experience.strip():
            exp_lines = [line.strip() for line in st.session_state.experience.strip().split('\n') if line.strip()]
            for line in exp_lines:
                st.markdown(f"<div class='experience-card'>{line}</div>", unsafe_allow_html=True)
        else:
            st.write("暂未填写个人经历，快去左侧补充吧～")
        
        st.markdown("---")
        st.subheader("💬 个人简介", anchor=False)
        st.write(st.session_state.intro if st.session_state.intro else "✨ 这个人很温柔，还没有留下介绍哦～")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ===================== 底部操作按钮 =====================
st.markdown("---")
btn_col1, btn_col2 = st.columns([0.1, 0.9])

with btn_col1:
    if st.button("📥 导出简历", use_container_width=True):
        pdf_buffer = generate_resume_pdf(
            st.session_state.name, st.session_state.nickname, st.session_state.birth_date,
            st.session_state.gender, st.session_state.education, st.session_state.work_exp,
            salary_min, salary_max, grad_info, job_intention, job_city,
            st.session_state.arrival_time, st.session_state.phone, st.session_state.email,
            st.session_state.address, st.session_state.id_card, st.session_state.skills,
            st.session_state.experience, st.session_state.intro, st.session_state.avatar
        )
        
        if pdf_buffer:
            file_name = f"{st.session_state.name if st.session_state.name else '个人简历'}_{datetime.datetime.now().strftime('%Y%m%d')}.pdf"
            st.download_button(
                label="下载PDF简历",
                data=pdf_buffer,
                file_name=file_name,
                mime="application/pdf",
                use_container_width=True
            )
            st.success("✅ 简历已生成，点击按钮即可下载！")
        else:
            st.error("❌ PDF生成失败，请检查输入内容或稍后重试")

with btn_col2:
    # 保留带确认的重置按钮（备用）
    if not st.session_state.reset_confirm:
        if st.button("🔄 重置表单（确认）", use_container_width=True, type="secondary"):
            st.session_state.reset_confirm = True
            st.warning("⚠️ 是否确定要重置所有信息？此操作不可恢复！")
    else:
        conf_col1, conf_col2 = st.columns(2)
        with conf_col1:
            if st.button("✅ 确认重置", type="primary", use_container_width=True):
                force_reset_all()
                try:
                    st.rerun()
                except AttributeError:
                    st.experimental_rerun()
        with conf_col2:
            if st.button("❌ 取消", type="secondary", use_container_width=True):
                st.session_state.reset_confirm = False
                try:
                    st.rerun()
                except AttributeError:
                    st.experimental_rerun()