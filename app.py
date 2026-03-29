import streamlit as st
import pandas as pd
import random
import urllib.parse  # 新增库：用于处理 WhatsApp 链接编码

# 1. 网页全局配置
st.set_page_config(page_title="MySukuSuku Master Ultra Pro Max", page_icon="🧬", layout="wide")

# 自定义 CSS 提升 UI 质感 (保留原样)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #f0f2f6; border-radius: 5px 5px 0 0; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #ff4b4b !important; color: white !important; }
    /* 新增：WhatsApp 按钮样式 */
    .whatsapp-button {
        display: inline-block;
        padding: 10px 20px;
        background-color: #25D366;
        color: white !important;
        text-align: center;
        text-decoration: none !important;
        font-weight: bold;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 核心数据库 (保持原样)
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
st.sidebar.title("🧬 科学营养分析系统")
with st.sidebar.expander("👤 输入身体指标 (必填)", expanded=True):
    # 默认值设为你的数据：80kg, 175cm
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
    target_p = weight * 2.0  
elif user_goal == "增肌 (Bulk)":
    target_cal = tdee + 300
    target_p = weight * 2.2
else:
    target_cal = tdee
    target_p = weight * 1.6

st.sidebar.divider()
st.sidebar.metric("🔥 建议每日热量", f"{int(target_cal)} kcal")
st.sidebar.metric("🥩 建议每日蛋白", f"{int(target_p)} g")

# 增加 BMI 状态显示 (保留原样)
bmi_status = "正常" if 18.5 <= bmi < 24 else "超重" if bmi >= 24 else "偏瘦"
st.sidebar.info(f"当前 BMI: {bmi:.1f} ({bmi_status})")

# --- 辅助计算函数 ---
def calc_meal(p_n, p_g, c_n, c_g, v_list, s_n):
    rp, rc, rs = db["Protein"][p_n], db["Carbs"][c_n], db["Sauces"][s_n]
    tp = (rp['p']*p_g/100) + (rc['p']*c_g/100) + rs['p']
    tc = (rp['cal']*p_g/100) + (rc['cal']*c_g/100) + rs['cal']
    for v in v_list:
        vs = db["Veggies"][v]
        tp += vs['p'] if 'p' in vs else 0
        tc += vs['cal']
    return tp, tc

# --- 主界面 ---
st.title("🔥 MySukuSuku Master: 全方位科学备餐系统")
st.info(f"📍 目标状态：{user_goal} | 建议摄入：{int(target_cal)} kcal | 所在地区建议：Johor/Local Market")

tab1, tab2, tab3 = st.tabs(["🏗️ 每日自由组装", "📅 5天自动计划", "👨‍🍳 烹饪备忘录"])

with tab1:
    st.subheader("🍳 早、午、晚三餐配置")
    bf_c = st.selectbox("☀️ 选择快速早餐", list(db["Breakfast"].keys()))
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("### 🍱 午餐设定")
        lp = st.selectbox("选择蛋白质", list(db["Protein"].keys()), key="lp")
        lpg = st.slider("蛋白质克数", 50, 400, 150, 10, key="lpg")
        lc = st.selectbox("选择碳水", list(db["Carbs"].keys()), key="lc")
        lcg = st.slider("碳水克数", 0, 350, 150, 10, key="lcg")
        lv = st.multiselect("添加蔬菜", list(db["Veggies"].keys()), default=["Broccoli (西兰花)"], key="lv")
        ls = st.selectbox("调味酱料", list(db["Sauces"].keys()), key="ls")
        lp_p, lp_cal = calc_meal(lp, lpg, lc, lcg, lv, ls)

    with col_r:
        st.markdown("### 🍽️ 晚餐设定")
        dp = st.selectbox("选择蛋白质", list(db["Protein"].keys()), key="dp")
        dpg = st.slider("蛋白质克数", 50, 400, 150, 10, key="dpg")
        dc = st.selectbox("选择碳水 (减脂建议选低)", list(db["Carbs"].keys()), key="dc")
        dcg = st.slider("碳水克数", 0, 350, 50, 10, key="dcg")
        dv = st.multiselect("添加蔬菜", list(db["Veggies"].keys()), default=["Okra (羊角豆)"], key="dv")
        ds = st.selectbox("调味酱料", list(db["Sauces"].keys()), key="ds")
        dp_p, dp_cal = calc_meal(dp, dpg, dc, dcg, dv, ds)

    # 全天汇总分析
    st.divider()
    day_p = db["Breakfast"][bf_c]['p'] + lp_p + dp_p
    day_cal = db["Breakfast"][bf_c]['cal'] + lp_cal + dp_cal
    
    m1, m2, m3 = st.columns(3)
    m1.metric("今日总热量", f"{int(day_cal)} kcal", delta=f"{int(day_cal - target_cal)} vs 建议")
    m2.metric("今日总蛋白", f"{int(day_p)} g", delta=f"{int(day_p - target_p)} vs 建议")
    
    # 增加可视化进度条
    with m3:
        st.write(f"**蛋白达标率**: {int(day_p/target_p*100)}%")
        st.progress(min(day_p / target_p, 1.0))
        if day_cal > target_cal:
            st.warning("⚠️ 热量略微超标，晚餐减掉碳水试试？")

with tab2:
    st.subheader("📅 工作日 5 天详细计划 (不单调版)")
    if st.button("🪄 一键生成动态 5 天方案"):
        plan_list = []
        shopping = {}
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
            p_n = random.choice(list(db["Protein"].keys()))
            c_n = random.choice(list(db["Carbs"].keys()))
            v_s = random.sample(list(db["Veggies"].keys()), 2)
            
            # 记录采购量计算
            raw = 300 * db["Protein"][p_n].get("raw_ratio", 1.2)
            shopping[p_n] = shopping.get(p_n, 0) + raw
            
            with st.expander(f"📍 {day} 安排", expanded=True):
                ca, cb, cc = st.columns(3)
                ca.success(f"**🌅 早餐**\n\n{random.choice(list(db['Breakfast'].keys()))}")
                cb.info(f"**🍱 午餐**\n\n150g {p_n}\n\n150g {c_n}\n\n🥗 {v_s[0]}")
                cc.warning(f"**🍽️ 晚餐**\n\n150g {p_n}\n\n🥗 {v_s[1]}\n\n(建议低碳)")

        st.divider()
        st.subheader("🛒 本周采购建议 (总生重 - 周末去超市参考)")
        shop_cols = st.columns(len(shopping))
        
        # 新增：准备 WhatsApp 的清单文本
        whatsapp_list = "🛒 我的减脂采购清单 (生肉重):\n\n"
        
        for i, (item, weight_g) in enumerate(shopping.items()):
             shop_cols[i].metric(item, f"{weight_g/1000:.2f} kg")
             whatsapp_list += f"- {item}: {weight_g/1000:.2f} kg\n"
        
        # --- 新增部分：WhatsApp 导出功能 ---
        st.divider()
        st.subheader("📲 WhatsApp 一键导出清单")
        
        # 对清单文字进行网页编码
        encoded_text = urllib.parse.quote(whatsapp_list)
        whatsapp_url = f"https://wa.me/?text={encoded_text}"
        
        # 居中显示 WhatsApp 按钮
        st.markdown(
            f'''<div style="text-align: center;">
                <a href="{whatsapp_url}" target="_blank" class="whatsapp-button">
                    📲 发送清单到我的 WhatsApp
                </a>
            </div>''', 
            unsafe_allow_html=True
        )

with tab3:
    st.subheader("🍳 备餐科学流程 (0 经验/无空气炸锅版)")
    
    # 使用 Markdown 制作更漂亮的指南
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        ### 🛠️ 工具准备
        - **不粘平底锅** (最重要的武器)
        - **电饭煲** (煮糙米和蒸玉米/红薯)
        - **厨房秤** (保证不吃多)
        
        ### 👨‍🍳 核心烹饪法
        1. **水煮法 (Blanching)**：
            - 水开加点盐，丢西兰花煮2分钟，捞出淋生抽。
        2. **嫩煎法 (Pan-Sear)**：
            - 鸡胸肉切片，撒盐黑胡椒，锅热抹一层薄油，两面各2-3分钟。
        3. **蒸法 (Steaming)**：
            - 煮饭时，上层蒸架放南瓜/红薯/玉米，饭熟了主食也好了。
        """)
    
    with col_b:
        st.markdown("""
        ### 📦 存储技术
        - **冷却再盖盖**：防止水汽让蔬菜变黄。
        - **底部垫纸巾**：在餐盒底部垫一张厨房纸，吸收多余水分，保持3天新鲜。
        - **酱汁分离**：吃的时候再淋酱，防止肉变咸变老。
        
        ### 💡 减脂小贴士
        - 每天喝够 **3000ml** 水。
        - 馋的时候吃 **10 颗无盐杏仁**。
        - 尽量在晚上 8 点前吃完晚餐。
        """)

# 页脚
st.divider()
st.caption("Built with ❤️ for your 80kg to 70kg Journey. Keep going!")
