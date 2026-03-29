import streamlit as st
import random

# 设置网页标题
st.set_page_config(page_title="MySukuSuku", page_icon="🍱")

# 食材数据库
proteins = {
    "烤鸡胸肉 (Ayam Dada)": {"p": 31, "f": 4},
    "甘榜鱼 (Ikan Kembung)": {"p": 20, "f": 5},
    "水煮蛋 (Telur)": {"p": 12, "f": 10},
    "冷冻虾仁 (Udang)": {"p": 24, "f": 1}
}
veggies = ["西兰花", "羊角豆", "长豆", "胡萝卜", "包菜"]
carbs = {"糙米饭": {"c": 25}, "烤红薯": {"c": 20}, "烤南瓜": {"c": 7}, "马铃薯": {"c": 17}}
sauces = ["低卡 Sambal 酱", "日式照烧汁", "泰式酸辣汁", "黑胡椒酱"]

# 界面显示
st.title("🇲🇾 我的马来西亚备餐生成器")
if st.button("🔀 点击随机生成今日组合"):
    p = random.choice(list(proteins.keys()))
    c = random.choice(list(carbs.keys()))
    v = random.sample(veggies, 2)
    s = random.choice(sauces)
    
    st.success(f"今日推荐：{p} + {v[0]} + {v[1]} + {c} (配 {s})")
    st.info(f"📊 估算蛋白质：{proteins[p]['p']}g")
