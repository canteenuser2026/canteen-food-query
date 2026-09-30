# canteen_app.py
import streamlit as st
import pandas as pd
# 网页基础配置
import streamlit as st
import pandas as pd # ---------------------- 初始化会话状态（收藏） ----------------------
if "favorites" not in st.session_state:
     st.session_state.favorites = []
 # ---------------------- 缓存读取CSV（兼容gbk/utf‑8，容错加强） ----------------------
@st.cache_data
def load_data():
     try:
         # 优先gbk（适配腾讯文档导出csv），不行自动试utf‑8‑sig
         try:
             df = pd.read_csv("canteen.csv", encoding="gbk")
         except UnicodeDecodeError:
             df = pd.read_csv("canteen.csv", encoding="utf-8-sig")
         df = df.dropna(how="all")
         return df
     except FileNotFoundError:
         st.error("❌ 找不到 canteen.csv，请确认它和本py文件放在同一个文件夹！")
         return pd.DataFrame()
     except Exception as e:
         st.error(f"❌ 读取文件出错：{e}")
         return pd.DataFrame()
df = load_data()
# ---------------------- 页面基础配置&美化 ----------------------
st.set_page_config(
     page_title="食堂菜品查询",
     page_icon="🍚",
     layout="wide"
 )
st.title("🍚 校园食堂菜品查询小程序")
st.subheader("快速查询食堂窗口、菜品、价格与口味评价")
st.info("💡 使用说明：可模糊搜索菜名、筛选窗口、价格区间、口味；还有随机干饭和收藏功能！")
if df.empty:
     st.stop()
 # ---------------------- 侧边栏筛选区 ----------------------
with st.sidebar:
     st.header("🔍 筛选面板")
     keyword = st.text_input("菜名搜索（模糊匹配）", value="")
     window_list = ["全部窗口"] + sorted(df["窗口名称"].unique().tolist())
     select_window = st.selectbox("选择窗口", window_list)
     min_p = float(df["价格"].dropna().min())
     max_p = float(df["价格"].dropna().max())
     price_range = st.slider("价格区间(元)", min_p, max_p, (min_p, max_p))
     taste_list = ["全部"] + sorted(df["口味评价"].unique().tolist())
     select_taste = st.selectbox("口味评价", taste_list)
     sort_opt = st.radio("排序方式", ["默认顺序", "价格↑由低到高", "价格↓由高到低"])
     st.divider()
     col1, col2 = st.columns(2)
     with col1:
         rand_btn = st.button("🎲 随机干饭！")
     with col2:
         clear_btn = st.button("🗑️ 清空筛选")
     st.divider()
     st.subheader("⭐ 我的收藏")
     if st.session_state.favorites:
         fav_df = df[df["菜品"].isin(st.session_state.favorites)]
         st.dataframe(fav_df, hide_index=True)
     else:
         st.caption("还没有收藏菜品")
 # ---------------------- 筛选逻辑 ----------------------
filtered = df.copy()
if clear_btn:
     keyword = ""
     select_window = "全部窗口"
     select_taste = "全部"
if keyword:
     filtered = filtered[filtered["菜品"].str.contains(keyword, na=False, case=False)]
if select_window != "全部窗口":
     filtered = filtered[filtered["窗口名称"] == select_window]
if select_taste != "全部":
     filtered = filtered[filtered["口味评价"] == select_taste]
filtered = filtered[(filtered["价格"] >= price_range[0]) & (filtered["价格"] <= price_range[1])]
if sort_opt == "价格↑由低到高":
     filtered = filtered.sort_values("价格", ascending=True)
elif sort_opt == "价格↓由高到低":
     filtered = filtered.sort_values("价格", ascending=False)
 # ---------------------- 随机干饭逻辑 ----------------------
if rand_btn:
 if len(filtered) > 0:
         one = filtered.sample(1)
         st.success(
             f"🎲 今天吃：**{one.iloc[0]['菜品']}**｜{one.iloc[0]['窗口名称']}｜{one.iloc[0]['价格']}元｜{one.iloc[0]['口味评价']}"
         )
else:
         st.warning("⚠️ 当前筛选条件下没有菜品，没法随机！")
 # ---------------------- 展示结果 + 收藏 ----------------------
st.subheader(f"📋 查询结果（共 {len(filtered)} 道）")
if len(filtered) == 0:
     st.warning("😥 没有找到符合条件的菜品，请调整筛选条件！")
else:
     st.dataframe(filtered, hide_index=True, use_container_width=True)
     st.divider()
     st.subheader("➕ 添加收藏")
     select_fav = st.selectbox("选择要收藏的菜品", filtered["菜品"].tolist())
     add_btn = st.button("⭐ 加入收藏")
if add_btn:
 if select_fav not in st.session_state.favorites:
             st.session_state.favorites.append(select_fav)
             st.success(f"✅ {select_fav} 已收藏！")
else:
             st.info("已经收藏过啦！")
st.caption("📌 提示：收藏仅临时保存在本次会话，刷新页面会清空；可在报告中将此作为未来改进方向")


