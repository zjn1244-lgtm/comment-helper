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
                "评论内容": record["content"],
                "点赞数": record["likes"],
                "回复数": record["replies"],
                "系统标签": record["system_tag"],
                "处理状态": "已处理" if record["is_processed"] else "未处理",
            }
            for record in records
        ]
    )


init_comments_table()

saved_comments = get_saved_comments()

if not saved_comments:
    st.info("暂无收藏评论")
else:
    st.dataframe(build_saved_table(saved_comments), use_container_width=True)
