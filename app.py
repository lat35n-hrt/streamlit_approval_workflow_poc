# app.py
import streamlit as st
from api_mock import fetch_records, fetch_detail, approve_record

st.title("Operational Review PoC")

records = fetch_records()

selected = st.selectbox(
    "Pending records",
    records,
    format_func=lambda x: f"{x['id']} - {x['title']}"
)

detail = fetch_detail(selected["id"])
st.write(detail["content"])

if st.button("Approve"):
    approve_record(selected["id"])
    st.success("Approved")
