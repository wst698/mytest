import streamlit as st
import pandas as pd

# 页面配置：马卡龙风格
st.set_page_config(page_title="动物数字档案", layout="wide", initial_sidebar_state="collapsed")

# 自定义CSS：马卡龙色系（粉/蓝/黄/绿柔和色调）
st.markdown("""
    <style>
    .stApp {
        background-color: #f9f7f8;  /* 马卡龙浅底 */
        color: #4a4a4a;  /* 柔和文字色 */
    }
    .stMetric {
        background-color: #f0f8fb;  /* 浅蓝底 */
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #88c9e8;  /* 马卡龙蓝 */
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .stDataFrame {
        background-color: #fff9f2;  /* 浅黄底 */
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .stCode {
        background-color: #fef0f5 !important;  /* 浅粉底 */
        border-radius: 12px;
        border: 1px solid #f8d7e3;  /* 马卡龙粉 */
    }
    .css-1d391kg {
        background-color: #f5f9f7;  /* 浅绿底 */
    }
    .stProgress > div > div {
        background-color: #a8e6cf;  /* 马卡龙绿 */
    }
    h1, h2, h3 {
        color: #6b8e9e;  /* 马卡龙主色 */
    }
    </style>
""", unsafe_allow_html=True)

# 标题区域（动物主题）
st.title("🐾 动物 小橘 数字档案")

# 基础信息模块
st.header("📋 基础信息")
col1, col2, col3 = st.columns(3)
with col1:
    st.text("动物ID: ZOO-2025-008")
with col2:
    st.text("入园时间: 2025-01-15")
    st.markdown("健康状态: <span style='color: #66bb6a'>良好</span>", unsafe_allow_html=True)
with col3:
    st.text("品种: 橘猫 | 年龄: 2岁")
    st.text("饲养员: 李星")

# 能力矩阵模块（适配动物行为能力）
st.header("🐱 行为能力矩阵")
skill_cols = st.columns(3)
with skill_cols[0]:
    st.metric(label="攀爬能力", value="92%", delta="+5%")
with skill_cols[1]:
    st.metric(label="捕猎反应", value="85%", delta="+2%")
with skill_cols[2]:
    st.metric(label="社交互动", value="70%", delta="-3%")

# 训练进度
st.subheader("社会化训练进度")
st.progress(85)  # 对应85%的进度

# 日常记录模块（替换为动物日常）
st.header("📅 日常行为记录")
task_data = pd.DataFrame({
    "日期": ["2025-01-20", "2025-01-25", "2025-01-30"],
    "行为事件": ["使用猫抓板", "与其他猫咪互动", "完成进食训练"],
    "状态": ["✅ 已完成", "⚠️ 部分完成", "✅ 已完成"],
    "难度/评分": ["★★☆☆☆", "★★★☆☆", "★☆☆☆☆"]
})
st.dataframe(task_data, use_container_width=True)

# 行为分析代码（适配动物主题）
st.header("🐾 行为分析代码片段")
code_content = """
def analyze_cat_behavior(behavior_data):
    \"\"\"分析猫咪日常行为数据\"\"\"
    try:
        # 统计活跃时长
        active_hours = sum(behavior_data["active_minutes"]) / 60
        if active_hours > 4:
            return "🐱 活跃度高 | 状态良好"
        elif active_hours < 2:
            return "😿 活跃度低 | 需关注健康"
        else:
            return "😺 活跃度正常"
    except Exception as e:
        print(f"分析失败: {e}")
        return "❌ 行为分析异常"
"""
st.code(code_content, language="python")

# 饲养提示（Markdown格式）
st.markdown("---")
st.markdown("""
- **饲养提示**: 下周解锁新训练任务
- **任务**: 环境适应度提升训练
- **记录时间**: 2025-01-31 10:15:30
- **园区状态**: 温度25℃ | 湿度55% | 环境安全
""")

# 互动提议
st.markdown("---")
st.write("爱护动物，人人有责")