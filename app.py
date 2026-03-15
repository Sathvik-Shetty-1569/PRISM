import streamlit as st
from core.analyzer import analyze_dataset, plot_histograms, correlation_matrix
from agents.ai_agent import generate_code, generate_summary
from core.code_executor import run_code
from utils.clean_code import clean_ai_code
import markdown

st.set_page_config(
    page_title="PRISM",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, .stApp {
    background-color: #f8f9fa !important;
    font-family: 'DM Sans', sans-serif !important;
}

#MainMenu, footer, header { visibility: hidden; }

h1 {
    font-family: 'DM Mono', monospace !important;
    font-size: 28px !important;
    font-weight: 500 !important;
    letter-spacing: 0.12em !important;
    color: #0a0a0a !important;
}

h2, h3 {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    color: #999 !important;
    text-transform: uppercase !important;
    margin-top: 28px !important;
    border: none !important;
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] {
    background: #ffffff !important;
    border-radius: 10px !important;
    padding: 4px !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: #ffffff !important;
    border: 1.5px dashed #d4d4d4 !important;
    border-radius: 10px !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #4f46e5 !important;
    background: #fafafe !important;
}

[data-testid="stFileUploaderDropzone"] > div {
    background: transparent !important;
    color: #666 !important;
}

[data-testid="stFileUploaderDropzone"] button {
    background: #4f46e5 !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 12px !important;
    font-weight: 500 !important;
}

[data-testid="stFileUploaderDropzone"] small {
    color: #999 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
}

/* Hide stray file icon after upload */
[data-testid="stFileUploaderFile"] {
    display: none !important;
}

/* TEXT INPUT */
.stTextInput input {
    background: #ffffff !important;
    border: 1px solid #e8e8e8 !important;
    border-radius: 6px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    color: #0a0a0a !important;
}

.stTextInput input:focus {
    border-color: #4f46e5 !important;
    background: #ffffff !important;
    box-shadow: 0 0 0 3px rgba(79,70,229,0.08) !important;
}

.stTextInput input::placeholder {
    color: #bbb !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
}

/* CODE BLOCK */
.stCodeBlock {
    background: #fafafa !important;
    border: 1px solid #e8e8e8 !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
}

/* EXPANDER */
.stExpander {
    border: 1px solid #e8e8e8 !important;
    border-radius: 8px !important;
    background: #ffffff !important;
}

details summary {
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    color: #666 !important;
    letter-spacing: 0.05em !important;
}

/* MARKDOWN TEXT */
.stMarkdown p {
    font-size: 13px !important;
    line-height: 1.7 !important;
    color: #444 !important;
}

/* SPINNER */
.stSpinner > div {
    border-top-color: #4f46e5 !important;
}

/* DIVIDER */
hr {
    border-color: #e8e8e8 !important;
    margin: 28px 0 !important;
}

/* PYPLOT CHARTS */
.stImage, [data-testid="stImage"] {
    border-radius: 8px !important;
}

/* AI INSIGHT BOX */
.insight-box {
    background: #ffffff;
    border: 1px solid #e8e8e8;
    border-left: 3px solid #4f46e5;
    border-radius: 8px;
    padding: 20px 24px;
    margin: 16px 0 24px;
    font-size: 13px;
    line-height: 1.8;
    color: #444;
}

.insight-box p { margin: 6px 0; color: #444; font-size: 13px; }
.insight-box strong { color: #0a0a0a; font-weight: 600; }
.insight-box ul { padding-left: 18px; margin: 8px 0; }
.insight-box li { margin: 4px 0; color: #444; font-size: 13px; }

.insight-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.2em;
    color: #4f46e5;
    text-transform: uppercase;
    margin-bottom: 14px;
    font-weight: 500;
}

/* METRIC CARDS */
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin: 16px 0 24px;
}

.metric-card {
    background: #ffffff;
    border: 1px solid #e8e8e8;
    border-radius: 8px;
    padding: 18px 20px;
}

.metric-card.accent {
    border-color: #ddd6fe;
    background: #faf8ff;
}

.metric-value {
    font-family: 'DM Mono', monospace;
    font-size: 24px;
    font-weight: 500;
    color: #0a0a0a;
    margin-bottom: 4px;
    display: block;
}

.metric-card.accent .metric-value { color: #4f46e5; }

.metric-label {
    font-size: 10px;
    color: #aaa;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-family: 'DM Mono', monospace;
}

/* RESULT BOX */
.result-box {
    background: #ffffff;
    border: 1px solid #e8e8e8;
    border-top: 2px solid #4f46e5;
    border-radius: 8px;
    padding: 16px 20px;
    margin-top: 12px;
    font-size: 13px;
    line-height: 1.7;
    color: #444;
    font-family: 'DM Mono', monospace;
    white-space: pre-wrap;
}

/* SECTION WRAPPER */
.section {
    background: #ffffff;
    border: 1px solid #e8e8e8;
    border-radius: 10px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)

# ── HEADER ──────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align:center; padding: 48px 0 36px">
        <svg width="44" height="44" viewBox="0 0 28 28" fill="none"
             style="display:block; margin: 0 auto 16px">
            <polygon points="14,3 25,22 3,22" fill="none" stroke="#4f46e5"
                     stroke-width="1.5" stroke-linejoin="round"/>
            <line x1="14" y1="3" x2="14" y2="22"
                  stroke="#a5b4fc" stroke-width="0.8" opacity="0.6"/>
            <line x1="14" y1="3" x2="3" y2="22"
                  stroke="#818cf8" stroke-width="0.6" opacity="0.35"/>
            <line x1="14" y1="3" x2="25" y2="22"
                  stroke="#6366f1" stroke-width="0.6" opacity="0.35"/>
            <circle cx="14" cy="3" r="1.8" fill="#4f46e5"/>
        </svg>
        <div style="font-family:'DM Mono',monospace; font-size:32px;
                    font-weight:500; letter-spacing:0.2em; color:#0a0a0a;
                    line-height:1">
            PRISM
        </div>
        <div style="font-family:'DM Mono',monospace; font-size:11px;
                    color:#bbb; margin-top:10px; letter-spacing:0.12em">
            One dataset. Every angle.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── FILE UPLOAD ──────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    uploaded_file = st.file_uploader(
        "Drop your CSV here",
        type=["csv"],
        label_visibility="collapsed"
    )

# ── MAIN ANALYSIS ────────────────────────────────────────────────────────────
if uploaded_file:
    df, results = analyze_dataset(uploaded_file)

    # ── Metric cards
    total_cells = results["shape"][0] * results["shape"][1]
    missing_count = sum(results["missing_values"].values())
    missing_pct = round((missing_count / total_cells) * 100, 1) if total_cells > 0 else 0
    numeric_cols = len([v for v in results["dtypes"].values()
                        if "int" in v or "float" in v])
    accent = "accent" if missing_pct > 5 else ""

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <span class="metric-value">{results['shape'][0]:,}</span>
            <span class="metric-label">Rows</span>
        </div>
        <div class="metric-card">
            <span class="metric-value">{results['shape'][1]}</span>
            <span class="metric-label">Columns</span>
        </div>
        <div class="metric-card {accent}">
            <span class="metric-value">{missing_pct}%</span>
            <span class="metric-label">Missing Data</span>
        </div>
        <div class="metric-card">
            <span class="metric-value">{numeric_cols}</span>
            <span class="metric-label">Numeric Cols</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── AI Summary
    with st.spinner("Analyzing with Gemini..."):
        summary = generate_summary(df)
    summary_html = markdown.markdown(summary)

    st.markdown(f"""
    <div class="insight-box">
        <div class="insight-label">▸ AI Insights &nbsp;·&nbsp; Gemini 2.5 Flash</div>
        {summary_html}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Dataset Preview
    st.subheader("Dataset Preview")
    st.dataframe(
        df.head(10),
        use_container_width=True,
        hide_index=False
    )

    # ── Missing Values
    st.subheader("Missing Values")
    missing_data = {k: v for k, v in results["missing_values"].items() if v > 0}
    if missing_data:
        import pandas as pd
        missing_df = pd.DataFrame(
            list(missing_data.items()),
            columns=["Column", "Missing Count"]
        )
        missing_df["% Missing"] = (
            missing_df["Missing Count"] / results["shape"][0] * 100
        ).round(2).astype(str) + "%"
        st.dataframe(missing_df, use_container_width=True, hide_index=True)
    else:
        st.markdown("""
        <div style="font-family:'DM Mono',monospace; font-size:12px;
                    color:#16a34a; padding:8px 0; display:flex;
                    align-items:center; gap:6px">
            ✓ &nbsp;No missing values found
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Correlation Matrix
    st.subheader("Correlation Matrix")
    corr_fig = correlation_matrix(df)
    if corr_fig:
        st.pyplot(corr_fig, use_container_width=True)
    else:
        st.markdown("""
        <div style="font-family:'DM Mono',monospace; font-size:12px;
                    color:#aaa; padding:8px 0">
            Need at least 2 numeric columns for correlation matrix.
        </div>
        """, unsafe_allow_html=True)

    # ── Column Distributions
    st.subheader("Column Distributions")
    hist_figs = plot_histograms(df)
    if hist_figs:
        cols = st.columns(2)
        for i, fig in enumerate(hist_figs):
            with cols[i % 2]:
                st.pyplot(fig, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Ask Your Data
    st.subheader("Ask Your Data")
    st.markdown("""
    <div style="font-family:'DM Mono',monospace; font-size:11px;
                color:#bbb; margin-bottom:12px; letter-spacing:0.05em">
        Ask anything about your dataset in plain English.
        PRISM will write and run the code for you.
    </div>
    """, unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    question = st.text_input(
        "query",
        placeholder="e.g. Which column has the strongest correlation with the target?",
        label_visibility="collapsed",
        key="query_input"
    )

    if question:
        st.session_state.chat_history.append(question)

        with st.spinner("Writing code..."):
            code = generate_code(
                question,
                df.columns,
                st.session_state.chat_history
            )
            code = clean_ai_code(code)

        with st.expander("View generated code", expanded=False):
            st.code(code, language="python")

        with st.spinner("Running..."):
            result, fig = run_code(code, df)

        if fig:
            st.pyplot(fig, use_container_width=True)

        if result and result.strip():
            st.markdown(f"""
            <div class="result-box">{result}</div>
            """, unsafe_allow_html=True)

    # ── Past questions
    if len(st.session_state.get("chat_history", [])) > 1:
        with st.expander("Query history", expanded=False):
            for i, q in enumerate(st.session_state.chat_history[:-1], 1):
                st.markdown(f"""
                <div style="font-family:'DM Mono',monospace; font-size:11px;
                            color:#999; padding:4px 0; border-bottom:1px solid #f0f0f0">
                    {i}. {q}
                </div>
                """, unsafe_allow_html=True)