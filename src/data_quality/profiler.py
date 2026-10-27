from pathlib import Path
import pandas as pd 

def profile_csv(file_path: str | Path) -> dict:
    df = pd.read_csv(file_path)

    missing_values = df.isna().sum()
    duplicated_count = int(df.duplicated().sum())
    numeric_summary = df.describe(include="number")

    #converting results into a python dictionary
    profile = {
        "row_count": int(df.shape[0]),
        "column_count": int(df.shape[1]),
        "columns":{
            column:{
                "dtype":str(df[column].dtype),
                "missing_count":int(missing_values[column]),
                "missing_percentage": round(
                    float(missing_values[column]/ len(df)*100), 2
                ) if len(df) else 0.0,
                "unique_count" : int(df[column].nunique()),
            }
            for column in df.columns
        },
        "duplicated_count": duplicated_count,
        "numeric_summary": numeric_summary.to_dict(),

    }
    return profile