import streamlit as st
import pandas as pd
import random

# 1. 网页全局配置
st.set_page_config(page_title="MySukuSuku Master Ultra", page_icon="🇲🇾", layout="wide")

# 2. 核心数据库 (保持不变)
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

# --- 辅助计算函数 (保持不变) ---
def calc_meal(p_n, p_g, c_n, c_g, v_list, s_n):
    res_p = db["Protein"][p_n]
    res_c = db["Carbs"][c_n]
    res_s = db["Sauces"][s_n]
    total_p = (res_p['p'] * p_g / 100) + (res_c['p'] * c_g / 100) + res_s['p']
    total_cal = (res_p['cal'] * p_g / 100) + (res_c['cal'] * c_g / 100) + res_s['cal']
    total_cost = (res_p['price'] * p_g / 100) + (res_c['price'] * c_g / 100) + res_s['price']
    for v in v_list:
        v_s = db["Veggies"][v]
        total_p += v_s['p']
        total_cal += v_s['cal']
        total_cost += v_s['price']
    return total_p, total_cal, total_cost

# --- 主界面 ---
st.sidebar.title("🎯 目标与设置")
daily_p_goal = st.sidebar.number_input("每日蛋白质目标 (g)", 50, 250, 150)
show_price = st.sidebar.checkbox("开启 RM 成本估算", value=True)

st.title("🔥 MySukuSuku Master: 全天候备餐系统")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["🏗️ 每日自由组装", "📅 智能 5 天计划", "👨‍🍳 烹饪备忘录"])

with tab1:
    # (这部分代码保持你原本的逻辑完全不变)
    st.subheader("🍳 早餐 (Breakfast)")
    bf_choice = st.selectbox("选择快速早餐", list(db["Breakfast"].keys()))
    bf_data = db["Breakfast"][bf_choice]
    st.markdown("---")
    col_l, col_d = st.columns(2)
    with col_l:
        st.subheader("🍱 午餐 (Lunch)")
        lp = st.selectbox("蛋白质", list(db["Protein"].keys()), key="lp")
        lpg = st.slider("重量(g)", 50, 300, 150, 10, key="lpg")
        lc = st.selectbox("碳水", list(db["Carbs"].keys()), key="lc")
        lcg = st.slider("重量(g)", 50, 300, 100, 10, key="lcg")
        lv = st.multiselect("蔬菜模块", list(db["Veggies"].keys()), default=["Broccoli (西兰花)"], key="lv")
        ls = st.selectbox("酱料", list(db["Sauces"].keys()), key="ls")
        lp_p, lp_cal, lp_cost = calc_meal(lp, lpg, lc, lcg, lv, ls)
    with col_d:
        st.subheader("🍽️ 晚餐 (Dinner)")
        dp = st.selectbox("蛋白质", list(db["Protein"].keys()), key="dp")
        dpg = st.slider("重量(g)", 50, 300, 150, 10, key="dpg")
        dc = st.selectbox("碳水", list(db["Carbs"].keys()), key="dc")
        dcg = st.slider("重量(g)", 50, 300, 50, 10, key="dcg")
        dv = st.multiselect("蔬菜模块", list(db["Veggies"].keys()), default=["Okra (羊角豆)"], key="dv")
        ds = st.selectbox("酱料", list(db["Sauces"].keys()), key="ds")
        dp_p, dp_cal, dp_cost = calc_meal(dp, dpg, dc, dcg, dv, ds)
    st.divider()
    all_p = bf_data['p'] + lp_p + dp_p
    all_cal = bf_data['cal'] + lp_cal + dp_cal
    all_cost = bf_data['price'] + lp_cost + dp_cost
    c1, c2, c3 = st.columns(3)
    c1.metric("全天总热量", f"{int(all_cal)} kcal")
    c2.metric("全天蛋白质", f"{int(all_p)} g / {daily_p_goal}g")
    if show_price: c3.metric("全天预估成本", f"RM {all_cost:.2f}")
    st.progress(min(all_p / daily_p_goal, 1.0))
    st.caption(f"🔥 今日蛋白质目标已完成 {int(all_p/daily_p_goal*100)}%")

with tab2:
    st.subheader("📅 工作日 5 天全功能方案")
    
    # 设定生成逻辑
    if st.button("🪄 一键生成智能备餐清单"):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        shopping_list = {} # 存储需要购买的总生重
        
        # 布局：左侧显示排餐卡片，右侧显示购物清单
        col_plan, col_shop = st.columns([3, 1])
        
        with col_plan:
            for day in days:
                p_item = random.choice(list(db["Protein"].keys()))
                c_item = random.choice(list(db["Carbs"].keys()))
                v_selected = random.sample(list(db["Veggies"].keys()), 2)
                
                # 记录采购需求 (假设午餐晚餐各吃 150g 熟重)
                raw_weight_needed = (150 * 2) * db["Protein"][p_item].get("raw_ratio", 1.2)
                shopping_list[p_item] = shopping_list.get(p_item, 0) + raw_weight_needed
                
                with st.expander(f"📍 {day} 饮食安排", expanded=True):
                    c_a, c_b, c_c = st.columns(3)
                    c_a.markdown(f"**🍳 早餐**\n\n{random.choice(list(db['Breakfast'].keys()))}")
                    c_b.markdown(f"**🍱 午餐**\n\n150g {p_item}\n\n100g {c_item}\n\n🥗 {v_selected[0]}")
                    c_c.markdown(f"**🍽️ 晚餐**\n\n150g {p_item}\n\n🥗 {v_selected[1]}\n\n(建议低碳水)")
        
        with col_shop:
            st.info("🛒 周末采购清单 (生重)")
            for item, weight in shopping_list.items():
                st.write(f"- **{item}**: {weight/1000:.2f} kg")
            st.divider()
            st.write("🥦 **蔬菜建议**:")
            st.write("- 西兰花/包菜/羊角豆 各买 1-2 份")
            st.write("- 鸡蛋 1 盒 (10颗)")
            st.caption("注：分量基于每天两顿 150g 蛋白质熟重估算。")

with tab3:
    # (这部分代码保持不变)
    st.subheader("🍳 90 分钟模块化备餐流程")
    st.markdown("""
    1. **烤箱预热 220°C**：
        - 放置鸡胸、鱼柳、虾仁。**20 分钟**出炉。
        - 放置切块红薯、南瓜、土豆。**25 分钟**出炉。
    2. **大锅烧开水**：
        - 烫西兰花/羊角豆（**1 分钟**）。
        - 烫胡萝卜/包菜（**2 分钟**）。
    3. **储存秘籍**：
        - 蔬菜晾干后，在保鲜盒底部垫**厨房纸**吸收多余水分。
        - 酱料独立小盒装，吃之前再淋上去。
    """)
