import streamlit as st

st.title("⚙️ Admin Dashboard")

new_doc = st.text_area("Add Academic Knowledge")

if st.button("Add Knowledge"):
    st.success("Knowledge added (we will connect vector DB next)")
