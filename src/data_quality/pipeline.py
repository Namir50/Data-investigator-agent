import pandas as pd

from src.data_quality.profiler import profile_dataframe
from src.data_quality.validator import(
     validate_age, 
     validate_income, 
     validate_duplicates, 
     validate_missing_values, 
     analyze_column_types, 
     detect_suspicious_numeric_values, 
     validate_dataset)

def analyze_dataframe(df: pd.DataFrame) -> dict:
    """validate and profile dataframe"""

    dataset_validation = validate_dataset(df)

    if dataset_validation["status"] == "invalid dataset":
        return {
            "dataset_validation": dataset_validation,
            "profile": None,
            "column_analysis": {},
            "issues": dataset_validation["issues"],
            "issue_count": len(dataset_validation["issues"]),
        }
    profile = profile_dataframe(df)
    column_analysis = analyze_column_types(df)

    issues = []

    if "age" in df.columns:
        issues.extend(validate_age(df))

    if "income" in df.columns:
        issues.extend(validate_income(df))

    issues.extend(validate_duplicates(df))
    issues.extend(validate_missing_values(df))
    issues.extend(detect_suspicious_numeric_values(df))

    report = {
        "dataset_validation": dataset_validation,
        "profile": profile,
        "column_analysis": column_analysis,
        "issues":issues,
        "issue_count": len(issues)
    }

    return report


