import streamlit as st
import pandas as pd
import random
import urllib.parse
import math

# 1. 网页全局配置
st.set_page_config(page_title="MySukuSuku Master Ultra Pro", page_icon="🧬", layout="wide")

# 自定义 CSS：打造 Dashboard 高级感
st.markdown("""
    <style>
    /* 全局背景与字体 */
    .main { background-color: #f8f9fa; font-family: 'Inter', sans-serif; }
    
    /* 指标卡片美化 */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #f0f2f6;
    }
    
    /* Tab 样式美化 */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background-color: #ffffff;
        border-radius: 10px 10px 0 0;
        padding: 10px 30px;
        font-weight: 600;
        color: #495057;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ff4b4b !important;
        color: white !important;
    }

    /* WhatsApp 按钮高级感 */
    .whatsapp-button {
        display: inline-block;
        padding: 15px 30px;
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
        color: white !important;
        text-align: center;
        text-decoration: none !important;
        font-weight: bold;
        border-radius: 50px;
        box-shadow: 0 10px 20px rgba(37,211,102,0.2);
        transition: transform 0.3s ease;
    }
    .whatsapp-button:hover { transform: translateY(-3px); }
    </style>
    """, unsafe_allow_html=True)

# 2. 核心数据库
db = {
    "Breakfast": {
        "2只大号水煮蛋 (Telur Rebus)": {"p": 13, "c": 1, "cal": 155, "price": 1.2},
        "希腊酸奶 + 坚果 (Yogurt)": {"p": 15, "c": 8, "cal": 180, "price": 4.5},
        "全麦面包 + 花生酱 (Roti)": {"p": 9, "c": 22, "cal": 240, "price": 1.5},
        "蛋白粉奶昔 (Whey Shake)": {"p": 24, "c": 3, "cal": 120, "price": 3.5}
    },
    "Protein": {
        "Chicken Breast (鸡胸)": {"p": 23, "c": 0, "cal": 110, "price": 2.2, "raw_ratio": 1.4},
        "Ikan Kembung (甘榜鱼)": {"p": 18, "c": 0, "cal": 125, "price": 1.8, "raw_ratio": 1.15},
        "Salmon (三文鱼)": {"p": 20, "c": 0, "cal": 208, "price": 8.5, "raw_ratio": 1.1},
        "Frozen Prawns (虾仁)": {"p": 18, "c": 0.2, "cal": 90, "price": 4.5, "raw_ratio": 1.3}
    },
    "Healthy Fats": {
        "Extra Virgin Olive Oil (橄榄油)": {"p": 0, "f": 14, "cal": 120, "price": 0.5},
        "Avocado (牛油果)": {"p": 2, "f": 15, "cal": 160, "price": 5.0},
        "Mixed Nuts (混合坚果)": {"p": 5, "f": 14, "cal": 170, "price": 3.0},
        "No Extra Fat": {"p": 0, "f": 0, "cal": 0, "price": 0}
    },
    "Carbs": {
        "Brown Rice (糙米)": {"p": 2.6, "c": 23, "cal": 111, "price": 0.5},
        "Sweet Potato (红薯)": {"p": 1.6, "c": 20, "cal": 86, "price": 0.8},
        "Pumpkin (南瓜)": {"p": 1, "c": 6.5, "cal": 26, "price": 0.6},
        "Baby Potatoes (土豆)": {"p": 2, "c": 17, "cal": 77, "price": 1.2}
    },
    "Veggies": {
        "Spinach (菠菜)": {"p": 2.9, "cal": 23, "type": "leafy"},
        "Choy Sum (菜心)": {"p": 1.5, "cal": 13, "type": "leafy"},
        "Broccoli (西兰花)": {"p": 2.8, "cal": 34, "type": "fiber"},
        "Okra (羊角豆)": {"p": 1.9, "cal": 33, "type": "fiber"}
    },
    "Sauces": {
        "Sambal (No Sugar)": {"p": 0.5, "cal": 20, "price": 0.2},
        "Teriyaki Sauce": {"p": 0.5, "cal": 25, "price": 0.3},
        "Black Pepper": {"p": 0.2, "cal": 22, "price": 0.3},
        "No Sauce (Dry)": {"p": 0, "cal": 0, "price": 0}
    }
}

# --- 科学计算逻辑 ---
st.sidebar.title("🧬 核心生物指标")
with st.sidebar.expander("👤 身体参数设置", expanded=True):
    weight = st.number_input("体重 (kg)", 40.0, 150.0, 80.0)
    height = st.number_input("身高 (cm)", 120.0, 220.0, 175.0)
    age = st.number_input("年龄", 15, 85, 25)
    gender = st.selectbox("性别", ["男", "女"])
    activity = st.selectbox("活动水平", ["久坐", "轻度", "中度", "高度"])
    user_goal = st.selectbox("核心目标", ["维持体重", "减脂 (Cut)", "增肌 (Bulk)"], index=1)

# 计算逻辑 (保持原样)
bmi = weight / ((height/100)**2)
bmr = (10 * weight + 6.25 * height - 5 * age + 5) if gender == "男" else (10 * weight + 6.25 * height - 5 * age - 161)
act_map = {"久坐": 1.2, "轻度": 1.375, "中度": 1.55, "高度": 1.725}
tdee = bmr * act_map[activity]

if user_goal == "减脂 (Cut)":
    target_cal, target_p, target_f = tdee - 500, weight * 1.6, weight * 0.7
elif user_goal == "增肌 (Bulk)":
    target_cal, target_p, target_f = tdee + 300, weight * 1.8, weight * 0.8
else:
    target_cal, target_p, target_f = tdee, weight * 1.2, weight * 0.8

st.sidebar.divider()
st.sidebar.metric("🎯 目标每日热量", f"{int(target_cal)} kcal", delta=f"{int(target_cal - tdee)}", delta_color="inverse")
st.sidebar.progress(max(0, min(100, int((80 - weight) / 10 * 100))) / 100)
st.sidebar.caption(f"🏃‍♂️ 距离 70kg 目标进度")

# --- 辅助计算函数 ---
def calc_meal(p_n, p_g, c_n, c_g, v_list, s_n, f_n):
    rp, rc, rs, rf = db["Protein"][p_n], db["Carbs"][c_n], db["Sauces"][s_n], db["Healthy Fats"][f_n]
    tp = (rp['p']*p_g/100) + (rc['p']*c_g/100) + rs.get('p', 0)
    tc = (rp['cal']*p_g/100) + (rc['cal']*c_g/100) + rs['cal'] + rf['cal']
    for v in v_list: tc += db["Veggies"][v]['cal']
    return tp, tc

# --- 主界面 ---
st.title("🔥 MySukuSuku Master")
st.markdown(f"**📍 当前模式**: `{user_goal}` | **建议摄入**: `{int(target_cal)} kcal` | **目标人群**: `柔佛/本地交易员`")

tab1, tab2, tab3 = st.tabs(["🏗️ 自由组装", "📅 5天计划", "👨‍🍳 烹饪备忘录"])

with tab1:
    st.subheader("🍱 三餐科学配置")
    bf_c = st.selectbox("☀️ 早餐选择", list(db["Breakfast"].keys()))
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("#### 午餐设定")
        lp, lpg = st.selectbox("蛋白质", list(db["Protein"].keys()), key="lp"), st.slider("生重 (g)", 50, 400, 150, 10, key="lpg")
        lc, lcg = st.selectbox("碳水", list(db["Carbs"].keys()), key="lc"), st.slider("克数 (g)", 0, 350, 150, 10, key="lcg")
        lv = st.multiselect("蔬菜", list(db["Veggies"].keys()), default=["Choy Sum (菜心)"], key="lv")
        ls, lf = st.selectbox("酱料", list(db["Sauces"].keys()), key="ls"), st.selectbox("优质脂肪", list(db["Healthy Fats"].keys()), key="lf")
        lp_p, lp_cal = calc_meal(lp, lpg, lc, lcg, lv, ls, lf)
    with col_r:
        st.markdown("#### 晚餐设定")
        dp, dpg = st.selectbox("蛋白质", list(db["Protein"].keys()), key="dp"), st.slider("生重 (g)", 50, 400, 150, 10, key="dpg")
        dc, dcg = st.selectbox("碳水", list(db["Carbs"].keys()), key="dc"), st.slider("克数 (g)", 0, 350, 50, 10, key="dcg")
        dv = st.multiselect("添加蔬菜", list(db["Veggies"].keys()), default=["Okra (羊角豆)"], key="dv")
        df, ds = st.selectbox("优质脂肪", list(db["Healthy Fats"].keys()), key="df"), st.selectbox("调味酱料", list(db["Sauces"].keys()), key="ds")
        dp_p, dp_cal = calc_meal(dp, dpg, dc, dcg, dv, ds, df)
    
    st.divider()
    day_p = db["Breakfast"][bf_c]['p'] + lp_p + dp_p
    day_cal = db["Breakfast"][bf_c]['cal'] + lp_cal + dp_cal
    m1, m2, m3 = st.columns(3)
    m1.metric("今日总热量", f"{int(day_cal)} kcal", delta=f"{int(day_cal - target_cal)} vs 建议")
    m2.metric("今日蛋白质", f"{int(day_p)} g", delta=f"{int(day_p - target_p)} vs 建议")
    with m3:
        st.write(f"**蛋白达标率**: {int(day_p/target_p*100)}%")
        st.progress(min(day_p / target_p, 1.0))

with tab2:
    st.subheader("🗓️ 5天高效循环计划")
    col_opt1, col_opt2 = st.columns(2)
    with col_opt1: main_protein = st.multiselect("核心肉类 (建议选2)", list(db["Protein"].keys()), default=["Chicken Breast (鸡胸)", "Ikan Kembung (甘榜鱼)"])
    with col_opt2: main_carb = st.selectbox("核心碳水", list(db["Carbs"].keys()), index=0)

    if st.button("🪄 一键生成计划与采购单"):
        shopping = {}
        for i, day in enumerate(["周一", "周二", "周三", "周四", "周五"]):
            p_n, c_n = main_protein[i % len(main_protein)], main_carb
            raw_p = 300 * db["Protein"][p_n].get("raw_ratio", 1.2)
            shopping[p_n] = shopping.get(p_n, 0) + raw_p
            with st.expander(f"📍 {day} 安排", expanded=(i==0)):
                st.write(f"早: {list(db['Breakfast'].keys())[0]} | 午/晚: {p_n} + {c_n}")
        
        st.divider()
        st.subheader("🛒 柔佛 Pasar 采购清单 (生重)")
        wa_text = "🛒 我的减脂清单:\n"
        cols = st.columns(len(shopping))
        for i, (item, weight_g) in enumerate(shopping.items()):
            rounded = math.ceil(weight_g / 500) * 0.5
            cols[i].metric(item, f"{rounded:.2f} kg")
            wa_text += f"- {item}: {rounded:.2f}kg\n"
        st.markdown(f'<div style="text-align: center;"><a href="https://wa.me/?text={urllib.parse.quote(wa_text)}" class="whatsapp-button">📲 发送 WhatsApp</a></div>', unsafe_allow_html=True)

with tab3:
    st.markdown("### 👨‍🍳 科学备餐实验室")
    st.info("💡 **高效原则**：一次采购，三次处理，五分钟出餐。")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("""
        #### 🛠️ 工具链
        - **不粘平底锅** (减脂命根子)
        - **电饭煲** (粗粮处理中心)
        - **厨房秤** (精准掌控)
        ---
        > 视觉整洁提升下厨欲望。
        """)
    with col_b:
        st.markdown("""
        #### 🧂 0卡风味
        - **本地**: 生抽 + 陈醋 + 指天椒
        - **烧烤**: 孜然粉 + 辣椒粉 + 盐
        - **去腥**: 大姜片 + 白胡椒粉
        ---
        *注：远离美乃滋。*
        """)
    with col_c:
        st.markdown("""
        #### 🕒 时间管理
        - **蔬菜**: 水煮 2min 保持脆爽
        - **肉类**: 嫩煎 4min 锁住肉汁
        - **主食**: 饭上蒸菜，同步完成
        ---
        *建议：8 点前结束进食。*
        """)
    
    st.divider()
    with st.expander("📦 存储黑科技 & 🚨 身体调节"):
        c1, c2 = st.columns(2)
        c1.write("1. 冷却再盖盖防止蔬菜变黄。\n2. 底部垫纸巾保鲜更久。")
        c2.write("1. 脑雾/疲劳请补充坚果或大量饮水。\n2. 柔佛炎热，确保 3000ml 饮水。")
    st.success("✨ **祝你顺利通往 70kg！**")

st.divider()
st.caption("Built with ❤️ for your 80kg to 70kg Journey.")
