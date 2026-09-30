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
        # 显示当前CSV真实表头（方便你核对！）
        st.caption(f"📌 当前CSV表头：{list(df.columns)}")
        # 价格容错
        if "价格" in df.columns:
            df["价格"] = pd.to_numeric(df["价格"], errors="coerce")
    except Exception:
        df = pd.DataFrame()
    return df

df = load_data()

# 安全取列：没有这一列就返回空Series
def safe_col(df, name):
    if name in df.columns:
        return df[name]
    return pd.Series([], dtype="object")

window_series = safe_col(df, "窗口")
dish_series = safe_col(df, "菜名")
price_series = safe_col(df, "价格").dropna()
taste_series = safe_col(df, "口味评价")

# 价格区间
if price_series.empty:
    min_p = 0.0
    max_p = 100.0
else:
    min_p = float(price_series.min())
    max_p = float(price_series.max())

# 下拉列表安全生成
window_list = sorted(window_series.dropna().unique().tolist())
taste_list = sorted(taste_series.dropna().unique().tolist())

st.sidebar.header("🔍 筛选条件")
selected_window = st.sidebar.multiselect("选择窗口", window_list)
selected_taste = st.sidebar.multiselect("口味评价", taste_list)
price_range = st.sidebar.slider("价格区间", min_p, max_p, (min_p, max_p), step=1.0)

search_text = st.text_input("🔎 输入菜名关键词搜索")

filter_df = df.copy()

if selected_window and "窗口" in filter_df.columns:
    filter_df = filter_df[filter_df["窗口"].isin(selected_window)]

if selected_taste and "口味评价" in filter_df.columns:
    filter_df = filter_df[filter_df["口味评价"].isin(selected_taste)]

if "价格" in filter_df.columns:
    filter_df = filter_df[
        (filter_df["价格"] >= price_range[0]) &
        (filter_df["价格"] <= price_range[1])
    ]

if search_text and "菜名" in filter_df.columns:
    filter_df = filter_df[filter_df["菜名"].str.contains(search_text, na=False, case=False)]

st.markdown(f"✅ 找到 {len(filter_df)} 道菜品")
st.dataframe(filter_df.reset_index(drop=True), use_container_width=True)

# 随机干饭
if st.button("🎲 随机选一道干饭！"):
    if not df.empty and "菜名" in df.columns:
        valid = filter_df.dropna(subset=["菜名"])
        if not valid.empty:
            rand = valid.sample(1)
            win = rand.iloc[0]["窗口"] if "窗口" in rand.columns else "未知"
            pri = rand.iloc[0]["价格"] if "价格" in rand.columns else "未知"
            st.success(f"今天吃：**{rand.iloc[0]['菜名']}**｜窗口：{win}｜¥{pri}")
        else:
            st.warning("没有可随机的菜品！")
    else:
        st.warning("暂无菜品数据")

# 收藏
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
