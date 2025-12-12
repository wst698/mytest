import streamlit as st
import random

# 1. 设置页面标题和图标
st.set_page_config(
    page_title="汪苏泷音乐播放器",
    page_icon="🎵",
    layout="centered"
)

# 2. 自定义CSS（莫兰迪灰粉色背景、样式优化）
st.markdown("""
    <style>
    /* 页面整体背景 */
    .stApp {
        background-color: #f0e8e6;  /* 莫兰迪灰粉色 */
    }
    
    /* 标题样式 */
    h1 {
        color: #8b7369;  /* 莫兰迪深棕色 */
        text-align: center;
    }
    
    /* 子标题样式 */
    h2 {
        color: #9d887e;
    }
    
    /* 文本样式 */
    p, div, span {
        color: #7a6b61;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background-color: #e0d2cd;
        color: #6d5c53;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    /* 按钮hover效果 */
    .stButton > button:hover {
        background-color: #d1c4be;
        color: #5c4b43;
    }
    
    /* 滑块样式 */
    .stSlider > div > div > div {
        background-color: #d1c4be;
    }
    
    /* 滑块进度条 */
    .stSlider > div > div > div > div {
        background-color: #b9a79e;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 页面标题与描述
st.title("🎵 汪苏泷 专属音乐播放器")
st.caption("使用Streamlit制作的简单音乐播放器 | 莫兰迪灰粉色主题 | 支持切歌和基本播放控制")

# 4. 定义汪苏泷的歌曲列表（包含封面、歌曲名、歌手、时长、播放链接）
music_list = [
    {
        "cover_url": "https://puui.qpic.cn/media_img/0/1087111581842036/0",
        "title": "年轮",
        "artist": "汪苏泷",
        "duration": "4:18",
        "audio_url": "https://music.163.com/song/media/outer/url?id=36966611.mp3"  # 示例链接
    },
    {
        "cover_url": "https://pic1.zhimg.com/50/v2-cc08e82965b5478be4dbb354733ddd84_hd.jpg?source=1940ef5c",
        "title": "不分手的恋爱",
        "artist": "汪苏泷",
        "duration": "3:50",
        "audio_url": "https://music.163.com/song/media/outer/url?id=506471182.mp3"  # 示例链接
    },
    {
        "cover_url": "https://www.360baike.com/uploads/202304/1681529925M6LOPzh4.jpg",
        "title": "大娱乐家",
        "artist": "汪苏泷",
        "duration": "3:25",
        "audio_url": "https://music.163.com/song/media/outer/url?id=1877241709.mp3"  # 示例链接
    }
]

# 5. 初始化session_state
if "current_music_idx" not in st.session_state:
    st.session_state.current_music_idx = 0  # 默认第一首
if "is_playing" not in st.session_state:
    st.session_state.is_playing = False  # 播放状态
if "progress" not in st.session_state:
    st.session_state.progress = 0  # 播放进度

# 6. 获取当前播放的音乐信息
current_music = music_list[st.session_state.current_music_idx]

# 7. 布局：左侧封面，右侧信息
col_cover, col_info = st.columns([1, 2])

with col_cover:
    # 显示专辑封面（圆角样式）
    st.markdown(f"""
        <div style="border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <img src="{current_music['cover_url']}" width="100%" style="display: block;">
        </div>
        <p style="text-align: center; margin-top: 8px; color: #8b7369;">专辑封面</p>
    """, unsafe_allow_html=True)

with col_info:
    # 显示歌曲信息
    st.subheader(f"{current_music['title']}")
    st.write(f"🎤 歌手: {current_music['artist']}")
    st.write(f"⏱️ 时长: {current_music['duration']}")

    # 8. 切歌按钮
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        def prev_song():
            # 上一首逻辑：循环切换
            st.session_state.current_music_idx = (st.session_state.current_music_idx - 1) % len(music_list)
            st.session_state.progress = 0  # 切换歌曲重置进度
        
        st.button("◀◀ 上一首", on_click=prev_song, use_container_width=True)
    
    with btn_col2:
        def next_song():
            # 下一首逻辑：循环切换
            st.session_state.current_music_idx = (st.session_state.current_music_idx + 1) % len(music_list)
            st.session_state.progress = 0  # 切换歌曲重置进度
        
        st.button("▶▶ 下一首", on_click=next_song, use_container_width=True)

# 9. 播放控制区域
st.markdown("---")  # 分隔线
col_play, col_progress, col_volume = st.columns([1, 5, 1])

with col_play:
    # 播放/暂停按钮逻辑
    def toggle_play():
        st.session_state.is_playing = not st.session_state.is_playing
    
    play_btn_label = "⏸️ 暂停" if st.session_state.is_playing else "▶️ 播放"
    st.button(play_btn_label, on_click=toggle_play, use_container_width=True)

with col_progress:
    # 播放进度条
    st.session_state.progress = st.slider(
        "",
        0, 100,
        st.session_state.progress,
        label_visibility="collapsed"
    )
    
    # 计算当前播放时间（模拟）
    total_seconds = int(current_music['duration'].split(':')[0]) * 60 + int(current_music['duration'].split(':')[1])
    current_seconds = int(total_seconds * st.session_state.progress / 100)
    current_time = f"{current_seconds//60}:{current_seconds%60:02d}"
    
    # 显示播放时间
    st.caption(f"{current_time} / {current_music['duration']}")

with col_volume:
    # 音量按钮
    st.button("🔊 音量", use_container_width=True)

# 10. 音频播放组件（实际播放音频）
st.markdown("---")
st.subheader("🎧 音频播放")
st.audio(current_music["audio_url"], format="audio/mp3")

# 11. 随机播放按钮（额外功能）
def random_play():
    st.session_state.current_music_idx = random.randint(0, len(music_list)-1)
    st.session_state.progress = 0

st.button("🔀 随机播放", on_click=random_play, use_container_width=True)

# 12. 显示歌曲列表
st.markdown("---")
st.subheader("📜 歌曲列表")
for idx, music in enumerate(music_list):
    active_tag = " 🟢 正在播放" if idx == st.session_state.current_music_idx else ""
    st.write(f"{idx+1}. {music['title']} - {music['artist']} {active_tag}")