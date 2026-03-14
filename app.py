import streamlit as st
from analyzer import analyze_dataset

st.title("AI Dataset Analyzer")

uploaded_file = st.file_uploader("Upload a CSV dataset", type=["csv"])

if uploaded_file:
    df, results = analyze_dataset(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Shape")
    st.write(f"Rows: {results['shape'][0]}, Columns: {results['shape'][1]}")

    st.subheader("Columns")
    st.write(results["columns"])

    st.subheader("Data Types")
    st.write(results["dtypes"])

    st.subheader("Missing Values")
    st.write(results["missing_values"])

    st.subheader("Statistical Summary")
    st.write(results["summary"])