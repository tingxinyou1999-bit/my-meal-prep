import streamlit as st
import pandas as pd
import random
import urllib.parse
import math

# 1. 网页全局配置
st.set_page_config(page_title="MySukuSuku Master Ultra Pro", page_icon="🧬", layout="wide")

# 自定义 CSS 提升 UI 质感 (保留并增强)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #f0f2f6; border-radius: 5px 5px 0 0; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #ff4b4b !important; color: white !important; }
    .whatsapp-button {
        display: inline-block;
        padding: 12px 24px;
        background-color: #25D366;
        color: white !important;
        text-align: center;
        text-decoration: none !important;
        font-weight: bold;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        cursor: pointer;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 核心数据库 (完全保留你的原始数据)
# 2. 核心数据库 (针对“幸存者偏差”修正蛋白含量为生重数据，并调高缩水率)
db = {
    "Breakfast": {
        "2只大号水煮蛋 (Telur Rebus)": {"p": 13, "c": 1, "cal": 155, "price": 1.2},
        "希腊酸奶 + 坚果 (Yogurt)": {"p": 15, "c": 8, "cal": 180, "price": 4.5},
        "全麦面包 + 花生酱 (Roti)": {"p": 9, "c": 22, "cal": 240, "price": 1.5},
        "蛋白粉奶昔 (Whey Shake)": {"p": 24, "c": 3, "cal": 120, "price": 3.5}
    },
    "Protein": {
        # 修正：100g 生鸡胸肉蛋白约 22-24g。raw_ratio 调至 1.4 (考虑到大马冷冻肉水分)
        "Chicken Breast (鸡胸)": {"p": 23, "c": 0, "cal": 110, "price": 2.2, "raw_ratio": 1.4},
        # 甘榜鱼生重蛋白约 18g，raw_ratio 维持 1.15
        "Ikan Kembung (甘榜鱼)": {"p": 18, "c": 0, "cal": 125, "price": 1.8, "raw_ratio": 1.15},
        # 三文鱼生重蛋白约 20g
        "Salmon (三文鱼)": {"p": 20, "c": 0, "cal": 208, "price": 8.5, "raw_ratio": 1.1},
        # 虾仁水分极高，raw_ratio 调高至 1.3
        "Frozen Prawns (虾仁)": {"p": 18, "c": 0.2, "cal": 90, "price": 4.5, "raw_ratio": 1.3}
    },
    "Healthy Fats": {
        "Extra Virgin Olive Oil (橄榄油)": {"p": 0, "f": 14, "cal": 120, "price": 0.5, "unit": "10ml"},
        "Avocado (牛油果)": {"p": 2, "f": 15, "cal": 160, "price": 5.0, "unit": "0.5个"},
        "Mixed Nuts (混合坚果)": {"p": 5, "f": 14, "cal": 170, "price": 3.0, "unit": "30g"},
        "No Extra Fat": {"p": 0, "f": 0, "cal": 0, "price": 0, "unit": "-"}
    },
    "Carbs": {
        "Brown Rice (糙米)": {"p": 2.6, "c": 23, "cal": 111, "price": 0.5},
        "Sweet Potato (红薯)": {"p": 1.6, "c": 20, "cal": 86, "price": 0.8},
        "Pumpkin (南瓜)": {"p": 1, "c": 6.5, "cal": 26, "price": 0.6},
        "Baby Potatoes (土豆)": {"p": 2, "c": 17, "cal": 77, "price": 1.2}
    },
    "Veggies": {
    # --- 深色叶菜 (微量元素之王) ---
    "Spinach (菠菜 - 高镁钾)": {"p": 2.9, "cal": 23, "price": 2.5, "type": "leafy"},
    "Choy Sum (菜心 - 本地推荐)": {"p": 1.5, "cal": 13, "type": "leafy"},
    "Kale (羽衣甘蓝 - 深度减脂)": {"p": 4.3, "cal": 49, "price": 8.5, "type": "leafy"},
    # --- 十字花科与根茎类 ---
    "Broccoli (西兰花)": {"p": 2.8, "cal": 34, "price": 1.5, "type": "cruciferous"},
    "Okra (羊角豆)": {"p": 1.9, "cal": 33, "price": 1.0, "type": "fiber"},
    "Cabbage (包菜)": {"p": 1.3, "cal": 25, "price": 0.3, "type": "fiber"},
    "Purple Cabbage (紫甘蓝)": {"p": 1.4, "cal": 31, "price": 1.2, "type": "antioxidant"}
    },
    "Sauces": {
        "Sambal (No Sugar)": {"p": 0.5, "cal": 20, "price": 0.2},
        "Teriyaki Sauce": {"p": 0.5, "cal": 25, "price": 0.3},
        "Thai Chili": {"p": 0.1, "cal": 25, "price": 0.2},
        "Black Pepper": {"p": 0.2, "cal": 22, "price": 0.3},
        "No Sauce (Dry)": {"p": 0, "cal": 0, "price": 0}
    }
}

# --- 科学计算逻辑 ---
st.sidebar.title("🧬 科学营养分析系统")
with st.sidebar.expander("👤 输入身体指标 (必填)", expanded=True):
    weight = st.number_input("当前体重 (kg)", 40.0, 150.0, 80.0)
    height = st.number_input("当前身高 (cm)", 120.0, 220.0, 175.0)
    age = st.number_input("当前年龄", 15, 85, 25)
    gender = st.selectbox("性别", ["男", "女"])
    activity = st.selectbox("活动水平", [
        "久坐 (办公室/交易员)", 
        "轻度活动 (每周运动1-2天)", 
        "中度活动 (每周运动3-5天)", 
        "高度活动 (每天高强度运动)"
    ])
    user_goal = st.selectbox("核心目标", ["维持体重", "减脂 (Cut)", "增肌 (Bulk)"], index=1)

bmi = weight / ((height/100)**2)
if gender == "男":
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
else:
    bmr = 10 * weight + 6.25 * height - 5 * age - 161

activity_factors = {"久坐 (办公室/交易员)": 1.2, "轻度活动 (每周运动1-2天)": 1.375, "中度活动 (每周运动3-5天)": 1.55, "高度活动 (每天高强度运动)": 1.725}
tdee = bmr * activity_factors[activity]

if user_goal == "减脂 (Cut)":
    target_cal = tdee - 500
    target_p = weight * 1.6 
    target_f = weight * 0.7  # 修正：设定脂肪底线，防止“变太监”
elif user_goal == "增肌 (Bulk)":
    target_cal = tdee + 300
    target_p = weight * 1.8
    target_f = weight * 0.8
else:
    target_cal = tdee
    target_p = weight * 1.2
    target_f = weight * 0.8

# --- 侧边栏视觉与逻辑增强 ---
st.sidebar.divider()
st.sidebar.subheader("🎯 每日营养目标")

# 使用列布局，让数据更紧凑
col_t1, col_t2 = st.sidebar.columns(2)
col_t1.metric("⚖️ 维持热量 (TDEE)", f"{int(tdee)}")
col_t2.metric("🔥 目标热量", f"{int(target_cal)}", delta=f"{int(target_cal - tdee)} kcal", delta_color="inverse")

# 完整显示三大营养素
st.sidebar.markdown(f"""
| 营养素 | 目标摄入量 | 备注 |
| :--- | :--- | :--- |
| 🥩 **蛋白质** | {int(target_p)}g | 维持肌肉，防止代谢下降 |
| 🥑 **优质脂肪** | {int(target_f)}g | **保护激素，防止出家** |
| 🍚 **净碳水** | {int((target_cal - target_p*4 - target_f*9)/4)}g | 训练/交易大脑供能 |
""")

st.sidebar.divider()

# BMI 状态增强版
if bmi >= 24:
    st.sidebar.warning(f"⚠️ 当前 BMI: {bmi:.1f} (超重) \n\n 离 70kg 目标还需减掉 {int(weight - 70)}kg！")
elif 18.5 <= bmi < 24:
    st.sidebar.success(f"✅ 当前 BMI: {bmi:.1f} (正常)")
else:
    st.sidebar.error(f"🚨 当前 BMI: {bmi:.1f} (偏瘦)")

# 增加一个简单的进度条：80kg -> 70kg
progress = max(0, min(100, int((80 - weight) / (80 - 70) * 100)))
st.sidebar.write(f"🏃‍♂️ 减脂总进度: {progress}%")
st.sidebar.progress(progress / 100)

# --- 辅助计算函数 (保留你的逻辑) ---
def calc_meal(p_n, p_g, c_n, c_g, v_list, s_n, f_n):
    rp, rc, rs, rf = db["Protein"][p_n], db["Carbs"][c_n], db["Sauces"][s_n], db["Healthy Fats"][f_n]
    tp = (rp['p']*p_g/100) + (rc['p']*c_g/100) + rs.get('p', 0) + rf.get('p', 0)
    tf = (rp.get('f', 0)*p_g/100) + rs.get('f', 0) + rf.get('f', 0)
    tc = (rp['cal']*p_g/100) + (rc['cal']*c_g/100) + rs['cal'] + rf['cal']
    for v in v_list:
        vs = db["Veggies"][v]
        tp += vs.get('p', 0)
        tc += vs['cal']
    return tp, tf, tc

# --- 主界面 ---
st.title("🔥 MySukuSuku Master: 全方位科学备餐系统")
st.info(f"📍 目标状态：{user_goal} | 建议摄入：{int(target_cal)} kcal | 地区建议：Johor/Local Market")

tab1, tab2, tab3 = st.tabs(["🏗️ 每日自由组装", "📅 5天自动计划", "👨‍🍳 烹饪备忘录"])

with tab1:
    st.subheader("🍳 早、午、晚三餐配置")
    bf_c = st.selectbox("☀️ 早餐选择", list(db["Breakfast"].keys()))
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.markdown("### 🍱 午餐设定")
        lp = st.selectbox("蛋白质", list(db["Protein"].keys()), key="lp")
        lpg = st.slider("生重 (g)", 50, 400, 150, 10, key="lpg")
        lc = st.selectbox("碳水", list(db["Carbs"].keys()), key="lc")
        lcg = st.slider("克数 (g)", 0, 350, 150, 10, key="lcg")
        
        # 蔬菜选择 + 脑雾逻辑预警
        lv = st.multiselect("蔬菜 (防脑雾必选深色叶菜)", list(db["Veggies"].keys()), default=["Choy Sum (菜心 - 本地推荐)"], key="lv")
        if not any(db["Veggies"][v].get("type") == "leafy" for v in lv):
            st.warning("⚠️ **脑雾预警**：检测到缺少深色叶菜！这会导致镁/钾不足，影响交易效率。")
            
        ls, lf = st.selectbox("酱料", list(db["Sauces"].keys()), key="ls"), st.selectbox("优质脂肪 (必选)", list(db["Healthy Fats"].keys()), key="lf")
        lp_p, lp_f, lp_cal = calc_meal(lp, lpg, lc, lcg, lv, ls, lf)
    with col_r:
        st.markdown("### 🍽️ 晚餐设定")
        dp = st.selectbox("选择蛋白质", list(db["Protein"].keys()), key="dp")
        dpg = st.slider("蛋白质克数", 50, 400, 150, 10, key="dpg")
        dc = st.selectbox("选择碳水", list(db["Carbs"].keys()), key="dc")
        dcg = st.slider("碳水克数", 0, 350, 50, 10, key="dcg")
        dv = st.multiselect("添加蔬菜", list(db["Veggies"].keys()), default=["Okra (羊角豆)"], key="dv")
        df = st.selectbox("选择优质脂肪 (晚餐)", list(db["Healthy Fats"].keys()), key="df")
        ds = st.selectbox("调味酱料", list(db["Sauces"].keys()), key="ds")
        dp_p, dp_f, dp_cal = calc_meal(dp, dpg, dc, dcg, dv, ds, df)
    st.divider()
    day_p = db["Breakfast"][bf_c]['p'] + lp_p + dp_p
    day_cal = db["Breakfast"][bf_c]['cal'] + lp_cal + dp_cal
    m1, m2, m3 = st.columns(3)
    m1.metric("今日总热量", f"{int(day_cal)} kcal", delta=f"{int(day_cal - target_cal)} vs 建议")
    m2.metric("今日总蛋白", f"{int(day_p)} g", delta=f"{int(day_p - target_p)} vs 建议")
    with m3:
        st.write(f"**蛋白达标率**: {int(day_p/target_p*100)}%")
        st.progress(min(day_p / target_p, 1.0))
        if day_cal > target_cal:
            st.warning("⚠️ 摄入超标，建议减少主食分量。")

with tab2:
    st.subheader("📅 工作日 5 天高效备餐计划 (拒接零碎采购)")
    
    # 1. 选择器：先定基调，再生成计划
    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        # 默认选中鸡胸和甘榜鱼，符合大马 Pasar 采购习惯
        main_protein = st.multiselect(
            "核心蛋白质 (建议选2种)", 
            list(db["Protein"].keys()), 
            default=["Chicken Breast (鸡胸)", "Ikan Kembung (甘榜鱼)"]
        )
    with col_opt2:
        main_carb = st.selectbox("核心碳水 (建议选1种)", list(db["Carbs"].keys()), index=0)

    # 2. 逻辑执行按钮
    if st.button("🪄 生成本周高效采购清单 & 计划"):
        if not main_protein:
            st.error("请至少选择一种蛋白质，否则你只能吃草了。")
        else:
            shopping = {}
            st.write("### 🗓️ 5天重复循环方案 (降低烹饪复杂度)")
            
            # 3. 循环生成 5 天安排
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            for i, day in enumerate(days):
                # 核心修改：通过取余 % 实现蛋白质交替，避免每天买不同肉
                p_n = main_protein[i % len(main_protein)]
                c_n = main_carb
                # 随机选2种蔬菜增加多样性
                v_s = random.sample(list(db["Veggies"].keys()), 2)
                
                # 计算生重并累加到采购清单
                # 300g 熟重对应的生重 = 300 * raw_ratio
                raw_p = 300 * db["Protein"][p_n].get("raw_ratio", 1.2)
                shopping[p_n] = shopping.get(p_n, 0) + raw_p
                
                # 碳水同样考虑缩水/吸水率
                raw_c = 200 * 1.1 
                shopping[c_n] = shopping.get(c_n, 0) + raw_c

                # 界面展示
                with st.expander(f"📍 {day} 安排", expanded=(i==0)):
                    ca, cb, cc = st.columns(3)
                    # 早餐固定为数据库第一项，减少思考成本
                    ca.success(f"**🌅 早餐**\n\n{list(db['Breakfast'].keys())[0]}") 
                    cb.info(f"**🍱 午餐**\n\n150g {p_n}\n\n150g {c_n}\n\n🥗 {v_s[0]}")
                    cc.warning(f"**🍽️ 晚餐**\n\n150g {p_n}\n\n🥗 {v_s[1]}\n\n(低碳模式)")

            st.divider()
            st.subheader("🛒 本周 Pasar 采购建议 (已自动取整)")
            
            # 4. 采购量取整逻辑 (0.5kg 为单位)
            shop_cols = st.columns(len(shopping))
            wa_text = "🛒 我的高效减脂采购清单 (Johor Market 版):\n\n"
            
            for i, (item, weight_g) in enumerate(shopping.items()):
                # 核心逻辑：向上取整到最接近的 0.5kg，方便 Pasar 大叔切肉
                rounded_weight = math.ceil(weight_g / 500) * 0.5
                shop_cols[i].metric(
                    item, 
                    f"{rounded_weight:.2f} kg", 
                    help="已根据缩水率计算生重，并向上取整至 0.5kg"
                )
                wa_text += f"- {item}: 约 {rounded_weight:.2f} kg\n"
            
            # 5. WhatsApp 导出功能
            encoded_wa = urllib.parse.quote(wa_text)
            st.markdown(
                f'''
                <div style="text-align: center;">
                    <a href="https://wa.me/?text={encoded_wa}" target="_blank" class="whatsapp-button">
                        📲 发送清单到 WhatsApp
                    </a>
                </div>
                ''', 
                unsafe_allow_html=True
            )
    st.subheader("🍳 备餐科学流程 (0 经验/无空气炸锅版)")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        ### 🛠️ 工具准备
        - **不粘平底锅** (最重要的武器)
        - **电饭煲** (煮糙米和蒸玉米/红薯)
        - **厨房秤** (保证不吃多)
        """)
    with col_b:
        st.markdown("""
        ### 👨‍🍳 核心烹饪法
        1. **水煮法**: 西兰花烫2分钟，淋生抽。
        2. **嫩煎法**: 鸡肉切片，小火抹薄油，两面2分钟。
        3. **蒸法**: 煮饭时顺便蒸玉米/红薯。
        """)

st.divider()
st.caption("Built with ❤️ for your 80kg to 70kg Journey.")
