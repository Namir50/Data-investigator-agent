import pandas as pd 
from src.data_quality.validator import validate_age, validate_income

def analyze_dataframe(df: pd.DataFrame) -> dict:
    """validating dataframe"""

    issues = []

    if "age" in df.columns:
        issues.extend(validate_age(df))

    if "income" in df.columns:
        issues.extend(validate_income(df))

    report = {
        "row_count" : int(df.shape[0]),
        "column_count": int(df.shape[1]),
        "issues": issues,
        "issue_count" : len(issues)
    } 

    return report


