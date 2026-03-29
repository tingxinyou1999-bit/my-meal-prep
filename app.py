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

# 将原来的 3 改成 4，并增加一个标题
tab1, tab2, tab3, tab4 = st.tabs(["🏗️ 自由组装", "📅 5天计划", "👨‍🍳 烹饪备忘录", "🚫 避雷图鉴"])

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
    st.markdown("### 🗓️ 5天高效备餐计划 (Precision Prep)")
    
    # --- 1. 配置中心 (使用容器美化) ---
    with st.container():
        st.markdown("""
            <style>
            .config-box {
                background-color: #f0f2f6;
                padding: 20px;
                border-radius: 15px;
                border: 1px solid #dfe3e6;
                margin-bottom: 25px;
            }
            </style>
            <div class="config-box">
                <p style="font-weight: bold; margin-bottom: 5px;">⚙️ 自动化配置中心</p>
                <span style="font-size: 0.85em; color: #666;">选择你本周在 Pasar 购买的主力食材，系统将自动分配。</span>
            </div>
        """, unsafe_allow_html=True)
        
        c_opt1, c_opt2 = st.columns(2)
        with c_opt1:
            main_protein = st.multiselect(
                "🥩 核心蛋白质 (建议选2种交替)", 
                list(db["Protein"].keys()), 
                default=["Chicken Breast (鸡胸)", "Ikan Kembung (甘榜鱼)"]
            )
        with c_opt2:
            main_carb = st.selectbox("🍚 核心碳水 (建议选1种)", list(db["Carbs"].keys()), index=0)

    # --- 2. 生成逻辑 ---
    if st.button("🪄 立即生成我的高效周计划"):
        if not main_protein:
            st.error("请至少选择一种蛋白质，保持肌肉代谢！")
        else:
            shopping = {}
            st.divider()
            
            # --- 3. 5天计划流布局 ---
            # 使用 CSS 打造纵向时间轴质感
            st.markdown("""
                <style>
                .day-card {
                    border-left: 5px solid #ff4b4b;
                    background-color: white;
                    padding: 15px;
                    border-radius: 0 10px 10px 0;
                    box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
                    margin-bottom: 15px;
                }
                .meal-tag {
                    font-size: 0.8em;
                    padding: 2px 8px;
                    border-radius: 5px;
                    font-weight: bold;
                    margin-right: 5px;
                }
                .breakfast { background-color: #e1f5fe; color: #01579b; }
                .lunch { background-color: #e8f5e9; color: #1b5e20; }
                .dinner { background-color: #fff3e0; color: #e65100; }
                </style>
            """, unsafe_allow_html=True)

            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            for i, day in enumerate(days):
                p_n = main_protein[i % len(main_protein)]
                # 随机分配蔬菜增加微量元素多样性
                v_s = random.sample(list(db["Veggies"].keys()), 2)
                
                # 计算生重
                raw_p = 300 * db["Protein"][p_n].get("raw_ratio", 1.2)
                shopping[p_n] = shopping.get(p_n, 0) + raw_p
                
                # 展示日计划
                with st.container():
                    st.markdown(f"#### 📍 {day}")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f'<div class="day-card"><span class="meal-tag breakfast">🌅 早餐</span><br><br>{list(db["Breakfast"].keys())[0]}</div>', unsafe_allow_html=True)
                    with col2:
                        st.markdown(f'<div class="day-card" style="border-left-color: #4caf50;"><span class="meal-tag lunch">🍱 午餐</span><br><br>150g {p_n}<br>150g {main_carb}<br>🥗 {v_s[0]}</div>', unsafe_allow_html=True)
                    with col3:
                        st.markdown(f'<div class="day-card" style="border-left-color: #ff9800;"><span class="meal-tag dinner">🍽️ 晚餐</span><br><br>150g {p_n}<br>🥗 {v_s[1]}<br><span style="font-size:0.8em; color:gray;">(低碳模式)</span></div>', unsafe_allow_html=True)

            # --- 4. 采购清单美化 ---
            st.divider()
            st.subheader("🛒 本周 Pasar 采购建议 (Johor Market)")
            
            wa_text = "🛒 我的高效减脂采购清单:\n\n"
            shop_cols = st.columns(len(shopping))
            for i, (item, weight_g) in enumerate(shopping.items()):
                rounded = math.ceil(weight_g / 500) * 0.5
                shop_cols[i].metric(item, f"{rounded:.2f} kg", help="已根据缩水率自动取整至 0.5kg")
                wa_text += f"- {item}: 约 {rounded:.2f} kg\n"
            
            # WhatsApp 按钮
            st.markdown(f'''
                <div style="text-align: center; margin-top: 20px;">
                    <a href="https://wa.me/?text={urllib.parse.quote(wa_text)}" target="_blank" class="whatsapp-button">
                        📲 将清单同步至 WhatsApp
                    </a>
                </div>
            ''', unsafe_allow_html=True)
with tab3:
    st.subheader("👨‍🍳 科学备餐与风味实验室")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        ### 🛠️ 核心工具
        - **不粘平底锅**: 减脂期的命根子，控油全靠它。
        - **电饭煲**: 煮糙米、蒸玉米/红薯的“全自动中心”。
        - **厨房秤**: 拒绝“凭感觉”，精准掌控 80kg 到 70kg 的每一克。
        
        ### 🧂 黄金调味公式 (让减脂餐变好吃)
        - **万能蘸料**: 生抽 + 陈醋 + 蒜末 + 指天椒 (大马风味，0脂肪)。
        - **干碟魔法**: 孜然粉 + 辣椒粉 + 少许盐 (煎鸡胸瞬间变烧烤味)。
        - **去腥神器**: 姜片 + 料酒/白胡椒粉 (处理甘榜鱼必选)。
        """)
    
    with col_b:
        st.markdown("""
        ### 👨‍🍳 核心烹饪法
        1. **水煮法 (Blanching)**: 西兰花/菜心烫 2 分钟，断生即捞，保持脆爽。
        2. **嫩煎法 (Pan-Sear)**: 鸡肉切片，小火抹薄油，利用肉本身水分焖熟更嫩。
        3. **蒸法 (Steaming)**: 煮饭时顺便蒸南瓜/红薯，粗粮口感更软糯。
        
        ### ⚠️ 减脂防雷提醒
        - **酱料陷阱**: 远离美乃滋、辣椒酱 (含糖量极高)。
        - **饮水指标**: 每天确保 3000ml 水，帮助代谢脂肪。
        - **大脑保护**: 如果感到脑雾，立刻补充 10 颗无盐坚果。
        """)

    st.success("💡 **专业建议**: 备餐时建议一次性处理 3 天的肉类生重，分袋装好，吃的时候现煎只需 5 分钟，口感远超微波炉加热。")

with tab4:
    # 注入更高级的 CSS 样式
    st.markdown("""
        <style>
        /* 避雷图鉴专属容器 */
        .avoid-container {
            background-color: #1e1e26; /* 深色背景增加专业感 */
            padding: 25px;
            border-radius: 20px;
            color: #ffffff;
        }
        
        /* 增强型避雷卡片 */
        .premium-avoid-card {
            background: rgba(255, 255, 255, 0.05); /* 毛玻璃效果 */
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .premium-avoid-card:hover {
            background: rgba(255, 75, 75, 0.1);
            border-color: #ff4b4b;
            transform: translateY(-5px);
        }

        /* 危险等级进度条 */
        .danger-bar {
            height: 6px;
            background-color: #444;
            border-radius: 3px;
            margin-top: 15px;
        }
        .danger-fill {
            height: 100%;
            background: linear-gradient(90deg, #ffa502, #ff4b4b);
            border-radius: 3px;
        }
        
        .food-emoji { font-size: 2em; margin-bottom: 10px; }
        .food-title { font-size: 1.1em; font-weight: bold; color: #ff6b6b; }
        .food-stats { font-size: 0.85em; color: #a1a1a1; margin-top: 5px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="avoid-container">', unsafe_allow_html=True)
    st.markdown("### 🚫 柔佛减脂防雷图鉴 (Avoid List)")
    st.write("金融交易员专属：血糖稳定 = 情绪稳定 = 交易盈利。")

    # 第一行：高糖陷阱
    st.markdown("#### 🥤 糖分与脑雾炸弹 (High Sugar)")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""
        <div class="premium-avoid-card">
            <div class="food-emoji">🥤</div>
            <div class="food-title">Gula Melaka Drinks</div>
            <div class="food-stats">含糖量：极高 | 脑雾风险：⭐⭐⭐⭐⭐</div>
            <div class="danger-bar"><div class="danger-fill" style="width: 95%;"></div></div>
            <div style="color:#ff4b4b; font-size:0.9em; margin-top:10px;">🔥 250 kcal/杯</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div class="premium-avoid-card">
            <div class="food-emoji">🥮</div>
            <div class="food-title">Traditional Kuih</div>
            <div class="food-stats">含糖量：高 | 饱腹感：极低</div>
            <div class="danger-bar"><div class="danger-fill" style="width: 85%;"></div></div>
            <div style="color:#ff4b4b; font-size:0.9em; margin-top:10px;">🔥 150 kcal/件</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown("""
        <div class="premium-avoid-card">
            <div class="food-emoji">🍧</div>
            <div class="food-title">Cendol / ABC</div>
            <div class="food-stats">椰浆+糖浆 | 胰岛素挑战者</div>
            <div class="danger-bar"><div class="danger-fill" style="width: 90%;"></div></div>
            <div style="color:#ff4b4b; font-size:0.9em; margin-top:10px;">🔥 400 kcal/份</div>
        </div>
        """, unsafe_allow_html=True)

    # 第二行：高油碳水
    st.markdown("#### 🍛 高油钠盐杀手 (High Fat & Sodium)")
    c4, c5, c6 = st.columns(3)
    
    with c4:
        st.markdown("""
        <div class="premium-avoid-card">
            <div class="food-emoji">🍛</div>
            <div class="food-title">Nasi Lemak</div>
            <div class="food-stats">椰浆饭 | 脂肪肝催化剂</div>
            <div class="danger-bar"><div class="danger-fill" style="width: 80%;"></div></div>
            <div style="color:#ff4b4b; font-size:0.9em; margin-top:10px;">🔥 800+ kcal/份</div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown("""
        <div class="premium-avoid-card">
            <div class="food-emoji">🍝</div>
            <div class="food-title">Char Kway Teow</div>
            <div class="food-stats">镬气 = 深度加工油脂</div>
            <div class="danger-bar"><div class="danger-fill" style="width: 98%;"></div></div>
            <div style="color:#ff4b4b; font-size:0.9em; margin-top:10px;">🔥 740 kcal/份</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c6:
        st.markdown("""
        <div class="premium-avoid-card">
            <div class="food-emoji">🍜</div>
            <div class="food-title">Instant Maggie</div>
            <div class="food-stats">钠含量爆炸 | 视觉水肿第一名</div>
            <div class="danger-bar"><div class="danger-fill" style="width: 75%;"></div></div>
            <div style="color:#ff4b4b; font-size:0.9em; margin-top:10px;">🔥 450 kcal/包</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    
    # 底部专业 Tips
    st.info("💡 **交易员避雷心得**：如果在交易时段摄入以上食物，你的大脑会因为消化压力而变得迟钝。为了 70kg 的目标和盈利曲线，请务必管住嘴！")
