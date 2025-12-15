import streamlit as st

# 页面配置：卡通蓝主题+猫和老鼠图标
st.set_page_config(
    page_title="猫和老鼠 - 经典剧集",
    page_icon="🐭",  # 杰瑞图标
    layout="centered"
)

# 自定义CSS：添加全局图片背景+样式优化
st.markdown("""
<style>
/* 全局页面背景：设置猫和老鼠主题图片背景 */
body {
    background-image: url("https://pic1.zhimg.com/v2-d512738bfdea04b3c37541b3da7bb9da_r.jpg?source=1940ef5c");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center center;
}

/* 内容容器：半透明背景增强可读性 */
.block-container {
    background-color: rgba(255, 255, 255, 0.9);  /* 提高白色透明度，避免遮挡背景 */
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 0 20px rgba(74, 144, 226, 0.4);
    margin: 20px auto;
    max-width: 800px;  /* 限制内容宽度，适配背景 */
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

/* 视频容器样式：增强边框与背景融合 */
div[data-testid="stVideo"] {
    border: 3px solid #FFD700;  /* 用金色边框匹配猫和老鼠卡通风格 */
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

# 猫和老鼠视频+剧情介绍列表（国内可访问MP4链接）
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

# 初始化会话状态
if "current_episode" not in st.session_state:
    st.session_state.current_episode = 0

# 切换剧集函数
def switch_episode(index):
    st.session_state.current_episode = index

# 页面标题
st.title("🐱🐭 猫和老鼠 - 经典剧集 🐭🐱")

# 播放当前选中的视频
current_video = video_list[st.session_state.current_episode]
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