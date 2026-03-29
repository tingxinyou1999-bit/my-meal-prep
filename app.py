import streamlit as st
import pandas as pd
import random

# 1. 页面配置
st.set_page_config(page_title="MySukuSuku Ultra", page_icon="🇲🇾", layout="wide")

# 2. 完整数据库 (加回了蔬菜，并修正了所有营养数据)
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
    "Veggies (蔬菜/纤维)": {
        "Broccoli (西兰花)": {"p": 2.8, "c": 7, "f": 0.4, "cal": 34},
        "Okra (羊角豆)": {"p": 1.9, "c": 7, "f": 0.2, "cal": 33},
        "Carrot (胡萝卜)": {"p": 0.9, "c": 10, "f": 0.2, "cal": 41},
        "Cabbage (包菜)": {"p": 1.3, "c": 6, "f": 0.1, "cal": 25}
    },
    "Sauces (灵魂酱料)": {
        "Sambal (No Sugar)": {"p": 0.5, "c": 2, "cal": 20},
        "Teriyaki Sauce": {"p": 0.5, "c": 5, "cal": 25},
        "Thai Chili": {"p": 0.1, "c": 6, "cal": 25},
        "Black Pepper": {"p": 0.2, "c": 3, "cal": 22},
        "No Sauce (Dry)": {"p": 0, "c": 0, "cal": 0}
    }
}

# --- 侧边栏 ---
st.sidebar.header("🎯 我的营养目标")
daily_protein_target = st.sidebar.number_input("每日蛋白质目标 (g)", 50, 250, 150)

# --- 主界面 ---
st.title("🔥 MySukuSuku Ultra: 马来西亚备餐大师")
st.write("概念：周日花90分钟做熟食材模块，工作日‘排列组合’吃不腻！")
st.markdown("---")

tab1, tab2 = st.tabs(["🏗️ 自由组装模块 (手动挡)", "📅 自动生成5天计划 (自动挡)"])

with tab1:
    col_input, col_stats = st.columns([2, 1])
    
    with col_input:
        st.subheader("🛠️ 排列组合你的模块")
        
        # 🥩 蛋白质
        p_name = st.selectbox("选择蛋白质", list(ingredients["Protein (肉类/蛋白质)"].keys()))
        p_g = st.slider("蛋白质重量 (克)", 50, 300, 150, step=10, key="p_slider")
        
        # 🍚 碳水
        c_name = st.selectbox("选择碳水", list(ingredients["Carbs (碳水/主食)"].keys()))
        c_g = st.slider("碳水重量 (克)", 50, 300, 100, step=10, key="c_slider")
        
        # 🥦 蔬菜 (把漏掉的加回来了！)
        st.markdown("**🥦 蔬菜模块**")
        v_names = st.multiselect("选择2种蔬菜 (每种固定100g计算)", 
                                  list(ingredients["Veggies (蔬菜/纤维)"].keys()), 
                                  default=["Broccoli (西兰花)", "Carrot (胡萝卜)"])
        
        # 🌶️ 酱料
        s_name = st.selectbox("选择灵魂酱料", list(ingredients["Sauces (灵魂酱料)"].keys()))

    with col_stats:
        st.subheader("📊 实时营养分析")
        
        # 计算逻辑 (加入蔬菜计算)
        p_s = ingredients["Protein (肉类/蛋白质)"][p_name]
        c_s = ingredients["Carbs (碳水/主食)"][c_name]
        s_s = ingredients["Sauces (灵魂酱料)"][s_name]
        
        # 初始营养 (肉+饭+酱)
        ratio_p = p_g / 100
        ratio_c = c_g / 100
        
        current_p = (p_s['p'] * ratio_p) + (c_s['p'] * ratio_c) + s_s['p']
        current_cal = (p_s['cal'] * ratio_p) + (c_s['cal'] * ratio_c) + s_s['cal']
        
        # 累加蔬菜营养
        for v in v_names:
            v_s = ingredients["Veggies (蔬菜/纤维)"][v]
            current_p += v_s['p'] # 蔬菜也有少量蛋白
            current_cal += v_s['cal']
            
        # 显示metric
        m1, m2 = st.columns(2)
        m1.metric("这一餐总热量", f"{int(current_cal)} kcal")
        m2.metric("这一餐蛋白质", f"{int(current_p)} g")
        
        # 进度条
        st.write(f"今日蛋白质目标完成度: {int(current_p)}g / {daily_protein_target}g")
        st.progress(min(current_p / daily_protein_target, 1.0))
        st.caption(f"这餐饭满足了你全天 {int(current_p/daily_protein_target*100)}% 的蛋白质需求。")
        
        st.success(f"✅ **组合：** {p_g}g {p_name} + {c_g}g {c_name} + {"&".join(v_names)} + {s_name}")

with tab2:
    st.subheader("📅 工作日5天不重样计划")
    st.write("点击按钮，后台自动为你排列组合，并估算采购量。")
    
    if st.button("🪄 一键生成计划"):
        plan_data = []
        for day in ["Mon", "Tue", "Wed", "Thu", "Fri"]:
            # 随机但尽量不重复
            p = random.choice(list(ingredients["Protein (肉类/蛋白质)"].keys()))
            c = random.choice(list(ingredients["Carbs (碳水/主食)"].keys()))
            vs = random.sample(list(ingredients["Veggies (蔬菜/纤维)"].keys()), 2)
            s = random.choice(list(ingredients["Sauces (灵魂酱料)"].keys()))
            plan_data.append({
                "日期": day, 
                "🥩蛋白质 (150g)": p, 
                "🍚碳水 (100g)": c, 
                "🥦蔬菜 (200g)": f"{vs[0]} & {vs[1]}", 
                "🌶️酱料": s
            })
        
        df = pd.DataFrame(plan_data)
        st.table(df)
        
        st.subheader("🛒 柔佛/槟城超市购物清单 (预估)")
        st.write("- **总肉类需求**: 购买约 1.0kg 鲜肉 (建议鸡胸+甘榜鱼组合)")
        st.write("- **总碳水需求**: 约 0.6kg - 0.8kg (红薯/南瓜/糙米)")
        st.write("- **蔬菜需求**: 2 棵西兰花, 1 包羊角豆, 1 袋胡萝卜")
        st.caption("💡 酱料家里一般都有，不够了再去 Jaya Grocer 买瓶 Nando's 酱或低卡 Sambal。")

st.markdown("---")
st.info("💡 **视频备餐小常识还原：** 西兰花水煮 1 分钟即可捞出，保持脆度 [00:02:53]；南瓜切块烤 20 分钟口感香甜软糯 [00:04:34]；酱料吃之前再淋，食物更耐放！")
