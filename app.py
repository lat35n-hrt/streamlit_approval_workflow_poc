# app.py
# app.py
import streamlit as st
from api_mock import fetch_records, fetch_detail, approve_record, fetch_audit

st.set_page_config(page_title="Operational Review PoC", layout="centered")
st.title("Operational Review PoC")

# Mock actor selector (PoC: no real authentication)
actor = st.sidebar.selectbox("Actor (mock)", ["approver", "requester", "admin"], index=0)
show_all = st.sidebar.checkbox("Show all records", value=False)

status_filter = None if show_all else "pending"
records = fetch_records(status=status_filter)

if not records:
    st.info("No records to show.")
    st.stop()

selected = st.selectbox(
    "Records",
    records,
    format_func=lambda x: f"{x['id']} - {x['title']} ({x['status']})",
)

detail = fetch_detail(selected["id"])

st.subheader("Detail")
st.write(detail["content"])
st.caption(f"Status: {detail['status']}")

can_approve = (actor == "approver")
is_pending = (detail["status"] == "pending")
disabled = (not can_approve) or (not is_pending)

if st.button("Approve", disabled=disabled):
    ok = approve_record(detail["id"], actor=actor)
    if ok:
        st.success("Approved")
    else:
        st.warning("Not pending (already processed).")
    st.rerun()

if not can_approve:
    st.caption("Note: Only 'approver' can approve in this PoC.")
elif not is_pending:
    st.caption("Note: This record is already processed.")

st.divider()
st.subheader("Audit log (latest)")
audit = fetch_audit(limit=20)
if audit:
    st.dataframe(audit, use_container_width=True)
else:
    st.caption("No audit events yet.")
