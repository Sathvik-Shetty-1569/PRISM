import pandas as pd

def analyze_dataset(file):
    df = pd.read_csv(file)

    analysis = {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "summary": df.describe(include="all").to_dict()
    }
    return df,analysis