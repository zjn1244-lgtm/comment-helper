import os
import uuid

import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager


COOKIE_PREFIX = "comment_ops_helper/"
COOKIE_PASSWORD = os.environ.get(
    "COOKIE_PASSWORD",
    "comment-ops-helper-workspace-cookie",
)
WORKSPACE_COOKIE_KEY = "workspace_id"


def get_cookie_manager():
    cookies = EncryptedCookieManager(
        prefix=COOKIE_PREFIX,
        password=COOKIE_PASSWORD,
    )

    if not cookies.ready():
        st.stop()

    return cookies


def get_workspace_id():
    cookies = get_cookie_manager()
    workspace_id = cookies.get(WORKSPACE_COOKIE_KEY)

    if not workspace_id:
        workspace_id = str(uuid.uuid4())
        cookies[WORKSPACE_COOKIE_KEY] = workspace_id
        cookies.save()

    if st.session_state.get("workspace_id") != workspace_id:
        st.session_state["workspace_id"] = workspace_id

    return workspace_id
