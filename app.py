import streamlit as st


st.set_page_config(page_title="PPKI Academic Formatter")
st.title("PPKI Academic Formatter")
st.write("Unggah dokumen dan pilih jenjang karya ilmiah.")

st.file_uploader("Dokumen DOCX", type=["docx"])
st.selectbox("Jenjang", ["S1", "S2", "S3"])

if st.button("Audit"):
    st.info("Audit belum tersedia pada tahap ini. Dokumen tidak diproses atau diubah.")
