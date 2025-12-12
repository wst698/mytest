import streamlit as st

# 设置页面配置（标题、图标）
st.set_page_config(
    page_title="莫兰迪相册",
    page_icon="🖼️",
    layout="centered"
)

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

# 初始化图片索引（session_state存储）
if 'ind' not in st.session_state:
    st.session_state['ind'] = 0

# 图片列表（至少3张，包含url和图注）
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
current_img = images[st.session_state['ind']]
st.image(current_img['url'], use_column_width=True, caption=current_img['text'])

# 切换图片函数
def next_img():
    st.session_state['ind'] = (st.session_state['ind'] + 1) % len(images)

def prev_img():
    st.session_state['ind'] = (st.session_state['ind'] - 1) % len(images)

# 前后切换按钮
col1, col2 = st.columns(2)
with col1:
    st.button("上一张", on_click=prev_img)
with col2:
    st.button("下一张", on_click=next_img)