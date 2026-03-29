import streamlit as st
import pandas as pd

# 1. 页面配置与美化
st.set_page_config(page_title="MySukuSuku Ultra", page_icon="🇲🇾", layout="wide")

# 2. 增强版数据库 (加了脂肪 f 和详细营养)
ingredients = {
    "Protein (肉类/蛋白质)": {
        "Chicken Breast (鸡胸)": {"p": 31, "c": 0, "f": 3.6, "cal": 165},
        "Ikan Kembung (甘榜鱼)": {"p": 19, "c": 0, "f": 5, "cal": 125},
        "Salmon (三文鱼)": {"p": 20, "c": 0, "f": 13, "cal": 208},
        "Frozen Prawns (虾仁)": {"p": 24, "c": 0.2, "f": 0.3, "cal": 99},
        "Hard Boiled Eggs (鸡蛋/2只)": {"p": 13, "c": 1.1, "f": 11, "cal": 155}
    },
    "Carbs (碳水/主食)": {
        "Brown Rice (糙米)": {"p": 2.6, "c": 23, "f": 0.9, "cal": 111},
        "Sweet Potato (红薯)": {"p": 1.6, "c": 20, "f": 0.1, "cal": 86},
        "Roasted Pumpkin (南瓜)": {"p": 1, "c": 6.5, "f": 0.1, "cal": 26},
        "Baby Potatoes (小土豆)": {"p": 2, "c": 17, "f": 0.1, "cal": 77}
    },
    "Sauces (灵魂酱料)": {
        "Sambal (No Sugar)": {"p": 0.5, "c": 2, "cal": 20},
        "Teriyaki Sauce": {"p": 0.5, "c": 5, "cal": 25},
        "Thai Chili": {"p": 0.1, "c": 6, "cal": 25},
        "Black Pepper": {"p": 0.2, "c": 3, "cal": 22}
    }
}

# --- 侧边栏：目标设定 ---
st.sidebar.header("🎯 我的营养目标")
daily_protein_target = st.sidebar.number_input("每日蛋白质目标 (g)", 50, 250, 150)

# --- 主界面 ---
st.title("🔥 MySukuSuku Ultra: 马来西亚备餐大师")
st.markdown("---")

tab1, tab2 = st.tabs(["🏗️ 自由组装模块", "📅 自动生成5天计划"])

with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        p_name = st.selectbox("🥩 蛋白质模块", list(ingredients["Protein (肉类/蛋白质)"].keys()))
        p_g = st.slider("重量 (克)", 50, 300, 150, step=10, key="p1")
        
        c_name = st.selectbox("🍚 碳水模块", list(ingredients["Carbs (碳水/主食)"].keys()))
        c_g = st.slider("重量 (克)", 50, 300, 100, step=10, key="c1")
        
        s_name = st.radio("🌶️ 酱料选择", list(ingredients["Sauces (灵魂酱料)"].keys()), horizontal=True)

    with col2:
        st.subheader("📊 实时营养分析")
        # 计算逻辑
        p_stats = ingredients["Protein (肉类/蛋白质)"][p_name]
        c_stats = ingredients["Carbs (碳水/主食)"][c_name]
        s_stats = ingredients["Sauces (灵魂酱料)"][s_name]
        
        total_p = (p_stats['p'] * p_g / 100) + (c_stats['p'] * c_g / 100) + s_stats['p']
        total_cal = (p_stats['cal'] * p_g / 100) + (c_stats['cal'] * c_g / 100) + s_stats['cal']
        
        st.metric("总热量", f"{int(total_cal)} kcal")
        st.write(f"蛋白质完成度: {int(total_p)}g / {daily_protein_target}g")
        st.progress(min(total_p / daily_protein_target, 1.0))
        st.caption(f"这一餐贡献了你全天 {int(total_p/daily_protein_target*100)}% 的蛋白质目标！")

with tab2:
    st.subheader("📅 5天不重样备餐建议")
    if st.button("🪄 一键生成工作日方案"):
        import random
        plan_data = []
        for day in ["Mon", "Tue", "Wed", "Thu", "Fri"]:
            p = random.choice(list(ingredients["Protein (肉类/蛋白质)"].keys()))
            c = random.choice(list(ingredients["Carbs (碳水/主食)"].keys()))
            s = random.choice(list(ingredients["Sauces (灵魂酱料)"].keys()))
            plan_data.append({"日期": day, "蛋白质": p, "碳水": c, "酱料": s})
        
        df = pd.DataFrame(plan_data)
        st.table(df)
        
        st.subheader("🛒 建议购物清单 (Shopping List)")
        st.write(f"- **总肉类需求**: 约 0.75kg - 1.0kg")
        st.write(f"- **总碳水需求**: 约 0.5kg (干重)")
        st.write(f"- **蔬菜建议**: 购买 2 棵西兰花, 1 包羊角豆, 3 根胡萝卜")

st.markdown("---")
st.info("💡 记得视频里的建议：酱料在吃的时候再加，蔬菜盒底放厨房纸！ [00:02:57]")
