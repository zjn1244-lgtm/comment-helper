from datetime import datetime

import pandas as pd
import streamlit as st

from core.database import get_comment_count, init_comments_table, insert_comments


COLUMN_ALIASES = {
    "comment_id": ["comment_id", "评论ID", "评论id"],
    "username": ["username", "用户名", "用户"],
    "content": ["content", "评论内容", "评论", "comment", "text"],
    "likes": ["likes", "点赞数", "点赞"],
    "replies": ["replies", "回复数", "回复"],
    "created_at": ["created_at", "发布时间", "时间"],
}


st.set_page_config(
    page_title="评论分析",
    page_icon="📊",
)

st.title("评论分析")
st.write("上传 CSV 或 Excel 评论数据文件，预览导入后的表格内容。")

uploaded_file = st.file_uploader(
    "上传评论数据文件",
    type=["csv", "xlsx"],
)


def get_column_value(row, aliases, default=None):
    for column_name in aliases:
        if column_name in row and pd.notna(row[column_name]):
            return normalize_value(row[column_name])
    return default


def normalize_value(value):
    if pd.isna(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    return value


def to_int(value):
    if pd.isna(value):
        return 0
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def build_comment_records(comments_df):
    imported_at = datetime.now().isoformat(timespec="seconds")
    records = []

    for _, row in comments_df.iterrows():
        records.append(
            {
                "comment_id": get_column_value(row, COLUMN_ALIASES["comment_id"]),
                "username": get_column_value(row, COLUMN_ALIASES["username"]),
                "content": get_column_value(row, COLUMN_ALIASES["content"]),
                "likes": to_int(get_column_value(row, COLUMN_ALIASES["likes"], 0)),
                "replies": to_int(get_column_value(row, COLUMN_ALIASES["replies"], 0)),
                "created_at": get_column_value(row, COLUMN_ALIASES["created_at"]),
                "system_tag": None,
                "note": None,
                "is_saved": 0,
                "is_processed": 0,
                "imported_at": imported_at,
            }
        )

    return records


init_comments_table()

if uploaded_file is not None:
    try:
        if uploaded_file.size == 0:
            st.error("文件为空，请上传包含评论数据的文件。")
        elif uploaded_file.name.lower().endswith(".csv"):
            comments_df = pd.read_csv(uploaded_file)
            if comments_df.empty:
                st.error("文件已读取，但没有可显示的数据。")
            else:
                inserted_count = insert_comments(build_comment_records(comments_df))
                total_count = get_comment_count()
                st.success(f"导入成功 {inserted_count} 条")
                st.info(f"数据库当前共有 {total_count} 条评论")
                st.dataframe(comments_df, use_container_width=True)
        elif uploaded_file.name.lower().endswith(".xlsx"):
            comments_df = pd.read_excel(uploaded_file)
            if comments_df.empty:
                st.error("文件已读取，但没有可显示的数据。")
            else:
                inserted_count = insert_comments(build_comment_records(comments_df))
                total_count = get_comment_count()
                st.success(f"导入成功 {inserted_count} 条")
                st.info(f"数据库当前共有 {total_count} 条评论")
                st.dataframe(comments_df, use_container_width=True)
        else:
            st.error("暂不支持该文件类型，请上传 CSV 或 XLSX 文件。")
    except Exception:
        st.error("文件读取失败，请检查文件格式或内容后重新上传。")
