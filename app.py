import streamlit as st

from core.utils import get_workspace_id


st.set_page_config(
    page_title="评论区运维助手",
    page_icon="💬",
)

get_workspace_id()

st.title("评论区运维助手")

st.write(
    "一个面向短视频评论区运营场景的评论筛选与处理辅助工具，"
    "用于帮助运营人员更快发现值得回复、需要关注和适合收藏的评论。"
)

st.info("请上传 CSV 或 Excel 评论数据文件，后续将在评论分析页中进行筛选、排序和处理。")
