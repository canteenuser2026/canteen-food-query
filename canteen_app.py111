# canteen_app.py
import streamlit as st
import pandas as pd
# 网页基础配置
st.set_page_config(
     page_title="食堂菜品查询",
     page_icon="🍚",
     layout="wide"
 )
# 页面标题
st.title("🍚 校园食堂菜品查询小程序")
st.subheader("快速查询食堂窗口、菜品、价格与口味评价")
# 缓存读取csv数据，encoding="gbk"适配腾讯文档导出的csv
@st.cache_data
def load_data():
     df = pd.read_csv("canteen.csv", encoding="utf-8")
     return df


df = load_data()
# 获取全部窗口名称
window_list = df["窗口名称"].unique().tolist()
window_list.insert(0, "全部窗口")
# 页面布局
col1, col2, col3 = st.columns(3)
with col1:
     selected_window = st.selectbox("选择食堂窗口", window_list)
with col2:
     search_keyword = st.text_input("搜索菜品名称", placeholder="输入菜名，例如：鸡公煲、拌面")
with col3:
     price_range = st.selectbox("价格筛选", ["全部价格","10元以内","10~20元","20元以上"])
# 筛选逻辑
filter_df = df.copy()
# 窗口筛选
if selected_window != "全部窗口":
     filter_df = filter_df[filter_df["窗口名称"] == selected_window]
# 菜品模糊搜索
if search_keyword:
     filter_df = filter_df[filter_df["菜品"].str.contains(search_keyword, case=False, na=False)]
# 价格筛选
def get_price_num(price_str):
     try:
         num = float(''.join([c for c in price_str if c.isdigit() or c == '.']))
         return num
     except:
         return 0
filter_df["价格数字"] = filter_df["价格"].apply(get_price_num)
if price_range == "10元以内":
     filter_df = filter_df[filter_df["价格数字"] <10]
elif price_range == "10~20元":
     filter_df = filter_df[(filter_df["价格数字"] >=10) & (filter_df["价格数字"] <=20)]
elif price_range == "20元以上":
     filter_df = filter_df[filter_df["价格数字"]>20]
# 展示结果
st.markdown(f"### 查询结果：共找到 {len(filter_df)} 道菜品")
st.dataframe(filter_df[["窗口名称","菜品","价格","味道评价"]], use_container_width=True)
# 侧边栏说明
with st.sidebar:
     st.header("📖 使用说明")
     st.write("1. 下拉框选择食堂窗口，筛选单个窗口菜品")
     st.write("2. 搜索框输入菜名，模糊检索菜品")
     st.write("3. 可按价格区间筛选")
     st.divider()
     st.header("📌项目信息")
     st.write("项目：校园食堂菜品查询网页小程序")
     st.write("数据源：实地调研食堂收集")
     st.write("开发技术：Python + Streamlit + Pandas")
