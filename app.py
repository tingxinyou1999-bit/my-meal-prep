import streamlit as st
import random

# 1. 网页配置：更有质感的外观
st.set_page_config(page_title="MySukuSuku Pro", page_icon="🍱", layout="wide")

# 2. 视频同款数据库：马来西亚本地化食材
proteins = {
    "烤鸡胸肉 (Ayam Dada)": {"p": 31, "f": 4, "c": 0, "img": "🍗"},
    "甘榜鱼 (Ikan Kembung)": {"p": 20, "f": 5, "c": 0, "img": "🐟"},
    "香煎三文鱼 (Salmon)": {"p": 25, "f": 13, "c": 0, "img": "🍣"},
    "蒜香冷冻虾 (Udang)": {"p": 24, "f": 1, "c": 0, "img": "🍤"}
}
veggies = {
    "西兰花 (Broccoli)": "🥦", "羊角豆 (Okra)": "🥒", 
    "长豆 (Long Bean)": "🎋", "胡萝卜 (Carrot)": "🥕", "包菜 (Cabbage)": "🥬"
}
carbs = {
    "糙米饭 (Brown Rice)": {"p": 3, "f": 1, "c": 25, "img": "🍚"},
    "烤红薯 (Sweet Potato)": {"p": 2, "f": 0, "c": 20, "img": "🍠"},
    "烤南瓜 (Pumpkin)": {"p": 1, "f": 0, "c": 7, "img": "🎃"},
    "小土豆 (Potatoes)": {"p": 2, "f": 0, "c": 17, "img": "🥔"}
}
sauces = ["🌶️ 低卡 Sambal", "🇯🇵 日式照烧汁", "🇹🇭 泰式酸辣汁", "🖤 黑胡椒酱", "🥑 牛油果酱"]

# --- 界面排版 ---
st.title("🍱 MySukuSuku Pro: 模块化备餐助手")
st.markdown("---")

# 创建三列：对应视频里的三个模块
col1, col2, col3 = st.columns(3)

with col1:
    st.header("1. 蛋白质模块")
    p_choice = st.selectbox("选择你的肉类", list(proteins.keys()))
    st.info(f"营养：{proteins[p_choice]['img']} 蛋白 {proteins[p_choice]['p']}g")

with col2:
    st.header("2. 蔬菜模块")
    v_choice = st.multiselect("选择2种蔬菜", list(veggies.keys()), default=list(veggies.keys())[:2])
    v_icons = "".join([veggies[v] for v in v_choice])
    st.info(f"组合：{v_icons} 膳食纤维 Up!")

with col3:
    st.header("3. 碳水模块")
    c_choice = st.selectbox("选择你的主食", list(carbs.keys()))
    st.info(f"营养：{carbs[c_choice]['img']} 碳水 {carbs[c_choice]['c']}g")

st.markdown("---")

# 4. 灵魂酱料选择
sauce_choice = st.select_slider("🍜 选择今天的灵魂酱料", options=sauces)

# 5. 生成今日份“健康餐”卡片
st.subheader("✅ 你的今日组合 (今日 Suku-Suku)")
total_p = proteins[p_choice]['p'] + carbs[c_choice]['p']
total_c = proteins[p_choice]['c'] + carbs[c_choice]['c']

st.success(f"""
### **{p_choice} + {" & ".join(v_choice)} + {c_choice}**
* **搭配酱料：** {sauce_choice}
* **估算营养：** 🚀 蛋白质 ~{total_p}g | 🍞 碳水 ~{total_c}g
""")

# 备餐金句
st.warning("💡 记住视频里的概念：周日花90分钟批量做熟这些模块，周一到周五只需‘排列组合’！")
