import streamlit as st
import pandas as pd
st.set_page_config(page_title="校园食堂菜品查询", layout="wide")
st.title("🍙 校园食堂菜品查询小程序")
st.subheader("快速查询食堂窗口、菜品、价格与口味评价")
st.info("💡 使用说明：可模糊搜索菜名、筛选窗口、价格区间、口味；还有随机干饭和收藏功能！")
@st.cache_data
def load_data():
     try:
         df = pd.read_csv("canteen.csv")
         # 强制清洗价格：不能转数字就变成空
         df["价格"] = pd.to_numeric(df["价格"], errors="coerce")
     except:
         df = pd.DataFrame(columns=["窗口", "菜名", "价格", "口味评价"])
     return df
df = load_data()
price_series = df["价格"].dropna()
if price_series.empty:
     min_p = 0.0
     max_p = 100.0
else:
     min_p = float(price_series.min())
     max_p = float(price_series.max())
 # 安全获取下拉选项，空的时候返回空列表
window_list = sorted(df["窗口"].dropna().unique().tolist())
taste_list = sorted(df["口味评价"].dropna().unique().tolist())
st.sidebar.header("🔍 筛选条件")
selected_window = st.sidebar.multiselect("选择窗口", window_list)
selected_taste = st.sidebar.multiselect("口味评价", taste_list)
price_range = st.sidebar.slider("价格区间", min_p, max_p, (min_p, max_p), step=1.0)
search_text = st.text_input("🔎 输入菜名关键词搜索")
filter_df = df.copy()
if selected_window:
     filter_df = filter_df[filter_df["窗口"].isin(selected_window)]
if selected_taste:
     filter_df = filter_df[filter_df["口味评价"].isin(selected_taste)]
 # 价格筛选：忽略空价格
filter_df = filter_df[
     (filter_df["价格"] >= price_range[0]) &
     (filter_df["价格"] <= price_range[1])
 ]
if search_text:
     filter_df = filter_df[filter_df["菜名"].str.contains(search_text, na=False, case=False)]
st.markdown(f"✅ 找到 {len(filter_df)} 道菜品")
st.dataframe(filter_df.reset_index(drop=True), use_container_width=True)
# 随机干饭
if st.button("🎲 随机选一道干饭！"):
     valid = filter_df.dropna(subset=["菜名"])
     if not valid.empty:
         rand = valid.sample(1)
         st.success(
             f"今天吃：**{rand.iloc[0]['菜名']}**｜窗口：{rand.iloc[0]['窗口']}｜¥{rand.iloc[0]['价格']}"
         )
     else:
         st.warning("没有可随机的菜品！")
 # 收藏（会话临时）
if "fav" not in st.session_state:
     st.session_state.fav = []
fav_name = st.text_input("⭐ 输入菜名加入收藏")
if st.button("加入收藏") and fav_name.strip():
     if fav_name not in st.session_state.fav:
         st.session_state.fav.append(fav_name)
         st.success(f"已收藏 {fav_name}")
     else:
         st.info("已经收藏过啦")
if st.session_state.fav:
     st.subheader("我的收藏")
     st.write(st.session_state.fav)
