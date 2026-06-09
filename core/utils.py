import uuid

import streamlit as st


def get_workspace_id():
    workspace_id = st.query_params.get("workspace_id")

    if isinstance(workspace_id, list):
        workspace_id = workspace_id[0] if workspace_id else None

    if not workspace_id:
        workspace_id = str(uuid.uuid4())
        st.query_params["workspace_id"] = workspace_id
        st.rerun()

    return workspace_id
