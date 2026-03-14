import streamlit as st
from analyzer import analyze_dataset, plot_histograms, correlation_matrix

st.title("AI Dataset Analyzer")

uploaded_file = st.file_uploader("Upload a CSV dataset", type=["csv"])

if uploaded_file:
    df, results = analyze_dataset(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Shape")
    st.write(f"Rows: {results['shape'][0]}, Columns: {results['shape'][1]}")

    st.subheader("Missing Values")
    st.write(results["missing_values"])

    st.subheader("Correlation Matrix")
    corr_fig = correlation_matrix(df)

    if corr_fig:
        st.pyplot(corr_fig)

    st.subheader("Column Distributions")

    histograms = plot_histograms(df)

    for fig in histograms:
        st.pyplot(fig)