import streamlit as st
import pandas as pd
import random

# 1. 网页全局配置
st.set_page_config(page_title="MySukuSuku Master Ultra", page_icon="🧬", layout="wide")

# 2. 核心数据库 (每 100g 营养数据)
db = {
    "Breakfast": {
        "2只大号水煮蛋 (Telur Rebus)": {"p": 13, "c": 1, "cal": 155, "price": 1.2},
        "希腊酸奶 + 坚果 (Yogurt)": {"p": 15, "c": 8, "cal": 180, "price": 4.5},
        "全麦面包 + 花生酱 (Roti)": {"p": 9, "c": 22, "cal": 240, "price": 1.5},
        "蛋白粉奶昔 (Whey Shake)": {"p": 24, "c": 3, "cal": 120, "price": 3.5}
    },
    "Protein": {
        "Chicken Breast (鸡胸)": {"p": 31, "c": 0, "cal": 165, "price": 2.2, "raw_ratio": 1.25},
        "Ikan Kembung (甘榜鱼)": {"p": 19, "c": 0, "cal": 125, "price": 1.8, "raw_ratio": 1.15},
        "Salmon (三文鱼)": {"p": 20, "c": 0, "cal": 208, "price": 8.5, "raw_ratio": 1.1},
        "Frozen Prawns (虾仁)": {"p": 24, "c": 0.2, "cal": 99, "price": 4.5, "raw_ratio": 1.05}
    },
    "Carbs": {
        "Brown Rice (糙米)": {"p": 2.6, "c": 23, "cal": 111, "price": 0.5},
        "Sweet Potato (红薯)": {"p": 1.6, "c": 20, "cal": 86, "price": 0.8},
        "Pumpkin (南瓜)": {"p": 1, "c": 6.5, "cal": 26, "price": 0.6},
        "Baby Potatoes (土豆)": {"p": 2, "c": 17, "cal": 77, "price": 1.2}
    },
    "Veggies": {
        "Broccoli (西兰花)": {"p": 2.8, "cal": 34, "price": 1.5},
        "Okra (羊角豆)": {"p": 1.9, "cal": 33, "price": 1.0},
        "Carrot (胡萝卜)": {"p": 0.9, "cal": 41, "price": 0.4},
        "Cabbage (包菜)": {"p": 1.3, "cal": 25, "price": 0.3}
    },
    "Sauces": {
        "Sambal (No Sugar)": {"p": 0.5, "cal": 20, "price": 0.2},
        "Teriyaki Sauce": {"p": 0.5, "cal": 25, "price": 0.3},
        "Thai Chili": {"p": 0.1, "cal": 25, "price": 0.2},
        "Black Pepper": {"p": 0.2, "cal": 22, "price": 0.3},
        "No Sauce (Dry)": {"p": 0, "cal": 0, "price": 0}
    }
}

# --- 科学计算逻辑：TDEE & BMI ---
st.sidebar.title("🧬 科学营养分析")
with st.sidebar.expander("输入身体指标 (必填)", expanded=True):
    weight = st.number_input("当前体重 (kg)", 40.0, 150.0, 75.0)
    height = st.number_input("当前身高 (cm)", 120.0, 220.0, 175.0)
    age = st.number_input("当前年龄", 15, 85, 25)
    gender = st.selectbox("性别", ["男", "女"])
    activity = st.selectbox("活动水平", [
        "久坐 (办公室/交易员)", 
        "轻度活动 (每周运动1-2天)", 
        "中度活动 (每周运动3-5天)", 
        "高度活动 (每天高强度运动)"
    ])
    user_goal = st.selectbox("核心目标", ["维持体重", "减脂 (Cut)", "增肌 (Bulk)"])

# 计算 BMI
bmi = weight / ((height/100)**2)

# 计算 BMR (Mifflin-St Jeor)
if gender == "男":
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
else:
    bmr = 10 * weight + 6.25 * height - 5 * age - 161

# TDEE 计算
activity_factors = {"久坐 (办公室/交易员)": 1.2, "轻度活动 (每周运动1-2天)": 1.375, "中度活动 (每周运动3-5天)": 1.55, "高度活动 (每天高强度运动)": 1.725}
tdee = bmr * activity_factors[activity]

# 根据目标科学分配热量与蛋白
if user_goal == "减脂 (Cut)":
    target_cal = tdee - 500
    target_p = weight * 2.0  # 减脂期高蛋白防掉肌肉
elif user_goal == "增肌 (Bulk)":
    target_cal = tdee + 300
    target_p = weight * 2.2
else:
    target_cal = tdee
    target_p = weight * 1.6

st.sidebar.divider()
st.sidebar.metric("建议每日热量", f"{int(target_cal)} kcal")
st.sidebar.metric("建议每日蛋白", f"{int(target_p)} g")
st.sidebar.write(f"当前 BMI: {bmi:.1f}")

# --- 辅助计算函数 ---
def calc_meal(p_n, p_g, c_n, c_g, v_list, s_n):
    rp, rc, rs = db["Protein"][p_n], db["Carbs"][c_n], db["Sauces"][s_n]
    tp = (rp['p']*p_g/100) + (rc['p']*c_g/100) + rs['p']
    tc = (rp['cal']*p_g/100) + (rc['cal']*c_g/100) + rs['cal']
    for v in v_list:
        vs = db["Veggies"][v]
        tp += vs['p']; tc += vs['cal']
    return tp, tc

# --- 主界面 ---
st.title("🔥 MySukuSuku Master: 全方位科学备餐系统")
st.info(f"📍 目标状态：{user_goal} | BMI：{bmi:.1f} | 建议总摄入：{int(target_cal)} kcal")

tab1, tab2, tab3 = st.tabs(["🏗️ 每日自由组装", "📅 5天自动计划", "👨‍🍳 烹饪备忘录"])

with tab1:
    st.subheader("🍳 早、午、晚三餐配置")
    bf_c = st.selectbox("选择快速早餐", list(db["Breakfast"].keys()))
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.write("**🍱 午餐设定**")
        lp = st.selectbox("蛋白质", list(db["Protein"].keys()), key="lp")
        lpg = st.slider("克数", 50, 350, 150, 10, key="lpg")
        lc = st.selectbox("碳水", list(db["Carbs"].keys()), key="lc")
        lcg = st.slider("克数", 50, 350, 100, 10, key="lcg")
        lv = st.multiselect("蔬菜", list(db["Veggies"].keys()), default=["Broccoli (西兰花)"], key="lv")
        ls = st.selectbox("酱料", list(db["Sauces"].keys()), key="ls")
        lp_p, lp_cal = calc_meal(lp, lpg, lc, lcg, lv, ls)

    with col_r:
        st.write("**🍽️ 晚餐设定**")
        dp = st.selectbox("蛋白质", list(db["Protein"].keys()), key="dp")
        dpg = st.slider("克数", 50, 350, 150, 10, key="dpg")
        dc = st.selectbox("碳水", list(db["Carbs"].keys()), key="dc")
        dcg = st.slider("克数", 50, 350, 50, 10, key="dcg")
        dv = st.multiselect("蔬菜", list(db["Veggies"].keys()), default=["Okra (羊角豆)"], key="dv")
        ds = st.selectbox("酱料", list(db["Sauces"].keys()), key="ds")
        dp_p, dp_cal = calc_meal(dp, dpg, dc, dcg, dv, ds)

    # 全天汇总分析
    st.divider()
    day_p = db["Breakfast"][bf_c]['p'] + lp_p + dp_p
    day_cal = db["Breakfast"][bf_c]['cal'] + lp_cal + dp_cal
    
    m1, m2, m3 = st.columns(3)
    m1.metric("今日总热量", f"{int(day_cal)} kcal", delta=f"{int(day_cal - target_cal)} vs 建议")
    m2.metric("今日总蛋白", f"{int(day_p)} g", delta=f"{int(day_p - target_p)} vs 建议")
    m3.write(f"蛋白达标率: {int(day_p/target_p*100)}%")
    m3.progress(min(day_p / target_p, 1.0))

with tab2:
    st.subheader("📅 工作日 5 天详细计划 (不单调版)")
    if st.button("🪄 生成动态 5 天方案"):
        plan_list = []
        shopping = {}
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
            p_n = random.choice(list(db["Protein"].keys()))
            c_n = random.choice(list(db["Carbs"].keys()))
            v_s = random.sample(list(db["Veggies"].keys()), 2)
            
            # 记录采购：假设每天两顿 150g 熟肉
            raw = 300 * db["Protein"][p_n].get("raw_ratio", 1.2)
            shopping[p_n] = shopping.get(p_n, 0) + raw
            
            with st.expander(f"📍 {day} 安排", expanded=True):
                ca, cb, cc = st.columns(3)
                ca.write(f"**🌅 早餐**\n\n{random.choice(list(db['Breakfast'].keys()))}")
                cb.write(f"**🍱 午餐**\n\n150g {p_n} + 100g {c_n}\n\n🥗 {v_s[0]}")
                cc.write(f"**🍽️ 晚餐**\n\n150g {p_n} + 🥗 {v_s[1]}\n\n(建议低碳)")

        st.info(f"🛒 **本周采购建议 (总生重)**: " + ", ".join([f"{k}: {v/1000:.2f}kg" for k, v in shopping.items()]))

with tab3:
    st.subheader("🍳 备餐科学流程指南")
    st.markdown("""
    - **1. 批量烘烤 (Bulk Roast)**：肉类/红薯入烤箱 220°C，20-25 分钟。
    - **2. 极速杀青 (Blanching)**：西兰花烫 60s，捞起必须晾干。
    - **3. 存储技术**：盒子底部垫厨房纸。
    """)
