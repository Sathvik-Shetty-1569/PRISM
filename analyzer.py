import pandas as pd
import matplotlib.pyplot as plt

def analyze_dataset(file):
    df = pd.read_csv(file)

    analysis = {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "summary": df.describe(include="all").to_dict()
    }
    return df, analysis

    
def plot_histograms(df):
    numeric_cols = df.select_dtypes(include=['int64','float64']).columns
    figs = []

    for col in numeric_cols:
        fig, ax = plt.subplots()
        df[col].hist(ax=ax)
        ax.set_title(f"Distribution of {col}")
        figs.append(fig)

    return figs


def correlation_matrix(df):
    numeric_df = df.select_dtypes(include=['int64','float64'])

    if numeric_df.shape[1] < 2:
        return None

    fig, ax = plt.subplots()
    corr = numeric_df.corr()

    cax = ax.matshow(corr)
    fig.colorbar(cax)

    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=90)

    ax.set_yticks(range(len(corr.columns)))
    ax.set_yticklabels(corr.columns)

    ax.set_title("Correlation Matrix")

    return fig
