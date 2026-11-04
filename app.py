import streamlit as st
from load_docs import load_documents
from agent import run_audit

st.title("Vendor Compliance Audit Assistant")
st.caption("Demo with sample data only. Do not upload real vendor documents.")

docs = load_documents("data")
sop = docs["sop.txt"]
vendor_files = sorted(n for n in docs if n.startswith("vendor_"))

choice = st.selectbox("Choose a sample vendor file", vendor_files)
uploaded = st.file_uploader("Or upload a vendor .txt file", type="txt")

vendor_text = uploaded.read().decode("utf-8") if uploaded else docs[choice]
with st.expander("Vendor submission"):
    st.text(vendor_text)

if st.button("Run audit"):
    with st.spinner("Auditing against the SOP..."):
        findings, score, email = run_audit(sop, vendor_text)
    st.metric("Compliance score", f"{score}/100")
    st.subheader("Findings")
    st.table(findings)
    st.subheader("Draft CAP email (review before sending)")
    st.markdown(email)