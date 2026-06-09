from datetime import datetime
from io import BytesIO

import pandas as pd
import streamlit as st

from core.database import get_saved_comments, init_comments_table


st.set_page_config(
    page_title="收藏夹",
    page_icon="⭐",
)

st.title("收藏夹")


def build_saved_table(records):
    return pd.DataFrame(
        [
            {
                "发布用户": record.get("username"),
                "评论内容": record["content"],
                "点赞数": record["likes"],
                "回复数": record["replies"],
                "发布时间": record.get("created_at"),
                "视频链接": record.get("video_url"),
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
                "发布用户": record.get("username"),
                "评论内容": record["content"],
                "点赞数": record["likes"],
                "回复数": record["replies"],
                "发布时间": record.get("created_at"),
                "视频链接": record.get("video_url"),
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
        export_df.to_excel(writer, index=False, sheet_name="收藏评论")
    return output.getvalue()


def show_export_buttons(records):
    export_df = build_export_table(records)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_data = export_df.to_csv(index=False).encode("utf-8-sig")
    excel_data = build_excel_file(export_df)
    columns = st.columns(2)

    columns[0].download_button(
        "导出 CSV",
        data=csv_data,
        file_name=f"收藏夹评论_{timestamp}.csv",
        mime="text/csv",
    )
    columns[1].download_button(
        "导出 Excel",
        data=excel_data,
        file_name=f"收藏夹评论_{timestamp}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


init_comments_table()

saved_comments = get_saved_comments()

if not saved_comments:
    st.info("暂无收藏评论")
else:
    show_export_buttons(saved_comments)
    st.dataframe(build_saved_table(saved_comments), use_container_width=True)
