import pandas as pd

def analyze_dataset(file):
    df = pd.read_csv(file)

    analysis = {}

    analysis["rows"] = df.shape[0]
    analysis["columns"] = df.shape[1]
    analysis["missing_values"] = df.isnull().sum().to_dict()
    analysis["columns_list"] = list(df.columns)

    return analysis