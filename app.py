import streamlit as st

# --- 页面配置 ---
st.set_page_config(page_title="MySukuSuku Pro", page_icon="🍱", layout="centered")

# --- 核心数据库 (每 100g 营养成分) ---
# p:蛋白质, c:碳水, f:脂肪, cal:卡路里
data = {
    "蛋白质 (Proteins)": {
        "烤鸡胸肉 (Ayam Dada)": {"p": 31, "c": 0, "f": 3.6, "cal": 165},
        "甘榜鱼 (Ikan Kembung)": {"p": 19, "c": 0, "f": 5, "cal": 125},
        "三文鱼 (Salmon)": {"p": 20, "c": 0, "f": 13, "cal": 208},
        "蒜香虾仁 (Udang)": {"p": 24, "c": 0.2, "f": 0.3, "cal": 99},
        "水煮蛋 (2颗/100g)": {"p": 13, "c": 1.1, "f": 11, "cal": 155},
        "瘦牛肉 (Beef Lean)": {"p": 26, "c": 0, "f": 15, "cal": 250}
    },
    "碳水 (Carbs)": {
        "糙米饭 (Brown Rice)": {"p": 2.6, "c": 23, "f": 0.9, "cal": 111},
        "红薯 (Ubi Keledek)": {"p": 1.6, "c": 20, "f": 0.1, "cal": 86},
        "马铃薯 (Potato)": {"p": 2, "c": 17, "f": 0.1, "cal": 77},
        "烤南瓜 (Labu)": {"p": 1, "c": 6.5, "f": 0.1, "cal": 26},
        "全麦意粉 (Pasta)": {"p": 5, "c": 25, "f": 1.1, "cal": 124}
    },
    "蔬菜 (Veggies)": {
        "西兰花 (Broccoli)": {"p": 2.8, "c": 7, "f": 0.4, "cal": 34},
        "羊角豆 (Okra)": {"p": 1.9, "c": 7, "f": 0.2, "cal": 33},
        "胡萝卜 (Carrot)": {"p": 0.9, "c": 10, "f": 0.2, "cal": 41},
        "包菜 (Cabbage)": {"p": 1.3, "c": 6, "f": 0.1, "cal": 25}
    },
    "灵魂酱料 (Sauces)": {
        "无糖 Sambal (15g)": {"p": 0.5, "c": 2, "f": 1, "cal": 20},
        "日式照烧汁 (15g)": {"p": 0.5, "c": 5, "f": 0, "cal": 25},
        "黑胡椒汁 (15g)": {"p": 0.2, "c": 3, "f": 1, "cal": 22},
        "泰式酸辣酱 (15g)": {"p": 0.1, "c": 6, "f": 0, "cal": 25},
        "纯牛油果酱 (30g)": {"p": 0.6, "c": 2.6, "f": 4.5, "cal": 50},
        "不加酱 (Dry)": {"p": 0, "c": 0, "f": 0, "cal": 0}
    }
}

st.title("🍱 马来西亚模块化备餐计算器")
st.write("根据视频概念：手动组合模块，自动计算卡路里。")

# --- 交互区域 ---
# 1. 蛋白质
st.subheader("🥩 第一步：选择蛋白质")
p_name = st.selectbox("肉类选择", list(data["蛋白质 (Proteins)"].keys()))
p_gram = st.slider(f"{p_name} 的重量 (g)", 50, 300, 150, 10)

# 2. 碳水
st.subheader("🍚 第二步：选择碳水")
c_name = st.selectbox("主食选择", list(data["碳水 (Carbs)"].keys()))
c_gram = st.slider(f"{c_name} 的重量 (g)", 50, 300, 100, 10)

# 3. 蔬菜 (默认每份100g)
st.subheader("🥦 第三步：选择蔬菜")
v_names = st.multiselect("选择蔬菜 (每种固定100g计算)", list(data["蔬菜 (Veggies)"].keys()), default=["西兰花 (Broccoli)"])

# 4. 酱料
st.subheader("🌶️ 第四步：选择酱料")
s_name = st.radio("今日灵魂酱料", list(data["灵魂酱料 (Sauces)"].keys()), horizontal=True)

# --- 计算逻辑 ---
def calc(name, category, gram):
    item = data[category][name]
    ratio = gram / 100
    return {k: v * ratio for k, v in item.items()}

res_p = calc(p_name, "蛋白质 (Proteins)", p_gram)
res_c = calc(c_name, "碳水 (Carbs)", c_gram)
res_s = data["灵魂酱料 (Sauces)"][s_name]

total_cal = res_p['cal'] + res_c['cal'] + res_s['cal']
total_protein = res_p['p'] + res_c['p'] + res_s['p']
total_carbs = res_p['c'] + res_c['c'] + res_s['c']

for v in v_names:
    v_stats = data["蔬菜 (Veggies)"][v]
    total_cal += v_stats['cal']
    total_protein += v_stats['p']
    total_carbs += v_stats['c']

# --- 结果展示 ---
st.divider()
col1, col2, col3 = st.columns(3)
col1.metric("总热量", f"{int(total_cal)} kcal")
col2.metric("蛋白质", f"{int(total_protein)} g")
col3.metric("总碳水", f"{int(total_carbs)} g")

st.success(f"✅ **你的组合：** {p_gram}g {p_name} + {c_gram}g {c_name} + {" & ".join(v_names)} + {s_name}")
