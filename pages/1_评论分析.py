from io import BytesIO
from datetime import datetime

import pandas as pd
import streamlit as st

from core.classifier import classify_comment
from core.database import (
    clear_comments,
    get_comment_count,
    get_comments,
    init_comments_table,
    insert_comments,
    update_comment_saved,
    update_comment_processed,
)


COLUMN_ALIASES = {
    "comment_id": ["comment_id", "评论ID", "评论id"],
    "username": ["username", "用户名", "用户"],
    "content": ["content", "评论内容", "评论", "comment", "text"],
    "likes": ["likes", "点赞数", "点赞"],
    "replies": ["replies", "回复数", "回复"],
    "created_at": ["created_at", "发布时间", "时间"],
}

FILTER_OPTIONS = [
    "全部评论",
    "普通评论",
    "值得回复评论",
    "风险评论",
    "高价值评论",
]

SORT_OPTIONS = [
    "默认排序",
    "点赞数从高到低",
    "回复数从高到低",
]

PROCESS_STATUS_OPTIONS = [
    "全部",
    "未处理",
    "已处理",
]


st.set_page_config(
    page_title="评论分析",
    page_icon="📊",
)

st.title("评论分析")
st.write("上传 CSV 或 Excel 评论数据文件，预览导入后的表格内容。")

clear_requested = st.button("清空数据库")

if clear_requested:
    clear_comments()
    st.session_state.pop("last_import_signature", None)
    st.session_state.pop("last_inserted_count", None)
    st.success("数据库已清空")

selected_tag = st.selectbox(
    "按系统标签筛选",
    FILTER_OPTIONS,
)

selected_process_status = st.selectbox(
    "按处理状态筛选",
    PROCESS_STATUS_OPTIONS,
)

search_keyword = st.text_input("搜索评论内容")

selected_sort = st.selectbox(
    "排序方式",
    SORT_OPTIONS,
)

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
        content = get_column_value(row, COLUMN_ALIASES["content"])
        records.append(
            {
                "comment_id": get_column_value(row, COLUMN_ALIASES["comment_id"]),
                "username": get_column_value(row, COLUMN_ALIASES["username"]),
                "content": content,
                "likes": to_int(get_column_value(row, COLUMN_ALIASES["likes"], 0)),
                "replies": to_int(get_column_value(row, COLUMN_ALIASES["replies"], 0)),
                "created_at": get_column_value(row, COLUMN_ALIASES["created_at"]),
                "system_tag": classify_comment(content),
                "note": None,
                "is_saved": 0,
                "is_processed": 0,
                "imported_at": imported_at,
            }
        )

    return records


def build_preview_table(records):
    return pd.DataFrame(
        [
            {
                "id": record.get("id"),
                "评论内容": record["content"],
                "点赞数": record["likes"],
                "回复数": record["replies"],
                "系统标签": record["system_tag"],
                "处理状态": "已处理" if record["is_processed"] else "未处理",
                "收藏状态": "已收藏" if record["is_saved"] else "未收藏",
            }
            for record in records
        ]
    )


def build_export_table(records):
    return pd.DataFrame(
        [
            {
                "评论内容": record["content"],
                "点赞数": record["likes"],
                "回复数": record["replies"],
                "系统标签": record["system_tag"],
                "是否已处理": "是" if record["is_processed"] else "否",
                "是否已收藏": "是" if record["is_saved"] else "否",
            }
            for record in records
        ]
    )


def build_excel_file(export_df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        export_df.to_excel(writer, index=False, sheet_name="评论")
    return output.getvalue()


def show_export_buttons(records, filename_prefix):
    if not records:
        return

    export_df = build_export_table(records)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_data = export_df.to_csv(index=False).encode("utf-8-sig")
    excel_data = build_excel_file(export_df)
    columns = st.columns(2)

    columns[0].download_button(
        "导出 CSV",
        data=csv_data,
        file_name=f"{filename_prefix}_{timestamp}.csv",
        mime="text/csv",
    )
    columns[1].download_button(
        "导出 Excel",
        data=excel_data,
        file_name=f"{filename_prefix}_{timestamp}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


def filter_records(records, selected_filter, selected_status, keyword, selected_sort):
    filtered_records = records

    if selected_filter == "全部评论":
        filtered_records = filtered_records
    else:
        filtered_records = [
            record
            for record in filtered_records
            if record["system_tag"] == selected_filter
        ]

    if selected_status == "未处理":
        filtered_records = [
            record for record in filtered_records if not record["is_processed"]
        ]
    elif selected_status == "已处理":
        filtered_records = [
            record for record in filtered_records if record["is_processed"]
        ]

    keyword = keyword.strip()
    if keyword:
        filtered_records = [
            record
            for record in filtered_records
            if keyword in str(record.get("content") or "")
        ]

    if selected_sort == "点赞数从高到低":
        return sorted(filtered_records, key=lambda record: record["likes"], reverse=True)
    if selected_sort == "回复数从高到低":
        return sorted(filtered_records, key=lambda record: record["replies"], reverse=True)

    return filtered_records


def import_and_show_comments(comments_df):
    records = build_comment_records(comments_df)
    inserted_count = insert_comments(records)
    st.session_state.last_inserted_count = inserted_count


def set_processed_status(record_id, is_processed):
    update_comment_processed(record_id, is_processed)


def set_saved_status(record_id, is_saved):
    update_comment_saved(record_id, is_saved)


def show_comment_list(records):
    if not records:
        st.warning("没有符合条件的评论")
        return

    st.dataframe(
        build_preview_table(records).drop(columns=["id"]),
        use_container_width=True,
    )

    st.write("评论操作")
    for index, record in enumerate(records):
        status_text = "已处理" if record["is_processed"] else "未处理"
        saved_text = "已收藏" if record["is_saved"] else "未收藏"
        process_button_text = "取消已处理" if record["is_processed"] else "标记已处理"
        save_button_text = "取消收藏" if record["is_saved"] else "收藏"
        columns = st.columns([5, 1, 1, 1, 1, 1, 1, 1])

        columns[0].write(record["content"])
        columns[1].write(record["likes"])
        columns[2].write(record["replies"])
        columns[3].write(record["system_tag"])
        columns[4].write(status_text)
        columns[5].write(saved_text)

        if columns[6].button(
            process_button_text,
            key=f"processed_{record.get('id', index)}_{record['is_processed']}",
        ):
            set_processed_status(record.get("id"), not record["is_processed"])
            st.rerun()

        if columns[7].button(
            save_button_text,
            key=f"saved_{record.get('id', index)}_{record['is_saved']}",
        ):
            set_saved_status(record.get("id"), not record["is_saved"])
            st.rerun()


def show_import_result(selected_filter, selected_status, keyword, selected_sort):
    records = get_comments()
    total_count = get_comment_count()
    filtered_records = filter_records(
        records,
        selected_filter,
        selected_status,
        keyword,
        selected_sort,
    )

    st.info(f"数据库当前共有 {total_count} 条评论")
    if not records:
        st.info("暂无评论，请上传 CSV 或 Excel 文件")
        return

    show_export_buttons(filtered_records, "评论筛选结果")
    show_comment_list(filtered_records)


def read_uploaded_file(uploaded_file):
    if uploaded_file.name.lower().endswith(".csv"):
        return pd.read_csv(uploaded_file)
    if uploaded_file.name.lower().endswith(".xlsx"):
        return pd.read_excel(uploaded_file)
    return None


init_comments_table()

if uploaded_file is not None and not clear_requested:
    try:
        if uploaded_file.size == 0:
            st.error("文件为空，请上传包含评论数据的文件。")
        else:
            comments_df = read_uploaded_file(uploaded_file)
            current_signature = (uploaded_file.name, uploaded_file.size)

            if comments_df is None:
                st.error("暂不支持该文件类型，请上传 CSV 或 XLSX 文件。")
            elif comments_df.empty:
                st.error("文件已读取，但没有可显示的数据。")
            elif st.session_state.get("last_import_signature") != current_signature:
                import_and_show_comments(comments_df)
                st.session_state.last_import_signature = current_signature
                st.success(f"导入成功 {st.session_state.last_inserted_count} 条")
            else:
                st.info("当前文件已导入")
    except Exception:
        st.error("文件读取失败，请检查文件格式或内容后重新上传。")

show_import_result(
    selected_tag,
    selected_process_status,
    search_keyword,
    selected_sort,
)
