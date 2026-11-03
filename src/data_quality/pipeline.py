import pandas as pd

from src.data_quality.profiler import profile_dataframe
from src.data_quality.validator import validate_age, validate_income, validate_duplicates, validate_missing_values


def analyze_dataframe(df: pd.DataFrame) -> dict:
    """Profile and validate a DataFrame."""

    profile = profile_dataframe(df)

    issues = []

    if "age" in df.columns:
        issues.extend(validate_age(df))

    if "income" in df.columns:
        issues.extend(validate_income(df))

    issues.extend(validate_duplicates(df))

    issues.extend(validate_missing_values(df))


    report = {
        "profile": profile,
        "issues": issues,
        "issue_count": len(issues),
    }

    return report