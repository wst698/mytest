import streamlit as st

# ---------------------- 全局页面配置 ----------------------
st.set_page_config(
    page_title="宠物家园介绍系统",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------- 全局样式（侧边栏样式保留） ----------------------
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
        padding: 20px;
    }
    h1, h2, h3 {
        color: #e67e22;
    }
    p {
        font-size: 16px;
        line-height: 1.6;
        color: #34495e;
    }
    .sidebar .sidebar-content {
        background-color: #34495e;
        color: white;
    }
    .sidebar .sidebar-content a {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# 主页面欢迎语（中文）
st.title("🐾 宠物家园介绍系统")
st.write("请从左侧侧边栏选择需要查看的宠物家园相关页面")

# （可选）如果是自定义侧边栏，添加中文组件
st.sidebar.title("🐾 导航菜单")  # 侧边栏中文标题
st.sidebar.write("👇 选择你想查看的内容")  # 侧边栏中文提示