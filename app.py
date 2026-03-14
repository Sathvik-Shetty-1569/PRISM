import streamlit as st
from analyzer import analyze_dataset

st.title("AI Dataset Analyzer")

uploaded_file = st.file_uploader("Upload a CSV dataset", type=["csv"])

if uploaded_file:
    results = analyze_dataset(uploaded_file)

    st.write("### Dataset Overview")
    st.write(results)