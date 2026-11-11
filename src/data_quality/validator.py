import pandas as pd

def validate_age(df: pd.DataFrame) -> list[dict]:
    """flag rows where age is outside the allowed range"""
    issues = []

    invalid_rows = df[(df['age']<0) | (df['age']>120)]

    for index,row in invalid_rows.iterrows():
        issues.append({
            "row_index":int(index),
            "column":"age",
            "age": int(row['age']),
            "issue":"age is out of range"
        })
    return issues


def validate_income(df: pd.DataFrame) -> list[dict]:
    """flag rows where income is negative"""

    issues = []

    invalid_rows = df[df['income']<0]

    for index, row in invalid_rows.iterrows():
        issues.append({
            "row_index":int(index),
            "column": 'income',
            "value" : float(row["income"]),
            "issue":"income cannot be negative",
        })
    return issues


def validate_duplicates(df: pd.DataFrame) ->list[dict]:
    """flag duplicate rows"""
    issues = []
    duplicate_rows = df[df.duplicated(keep = 'first')]

    for index,row in duplicate_rows.iterrows():
        issues.append({
            "row_index": int(index),
            "row": row.to_dict(),
            "issue" : "duplicate row"
        })
    return issues

def validate_missing_values(df: pd.DataFrame) -> list[dict]:
    """flag missing values in the dataframe"""
    issues = []

    missing_values = df.isna()

    for column in df.columns:
        missing_rows = df[missing_values[column]]
        
        for index,row in missing_rows.iterrows():
            issues.append({
                "row_index": int(index),
                "column": column,
                "issues":"missing value detected"
            })
    return issues


def analyze_column_types(df: pd.DataFrame) -> dict:
    """Infer likely column types using numeric conversion ratios."""

    results = {}

    for column in df.columns:
        converted = pd.to_numeric(df[column], errors="coerce")

        total_values = df[column].notna().sum()
        numeric_values = converted.notna().sum()

        numeric_ratio = (
            numeric_values / total_values
            if total_values > 0
            else 0
        )

        if numeric_ratio > 0.50:
            inferred_type = "likely_numeric"
        else:
            inferred_type = "likely_text"

        results[column] = {
            "original_dtype": str(df[column].dtype),
            "numeric_ratio": round(float(numeric_ratio), 2),
            "inferred_type": inferred_type
        }

    return results


def detect_suspicious_numeric_values(df: pd.DataFrame) -> list[dict]:
    """Detect non-numeric values in columns classified as likely numeric."""

    suspicious_values = []

    column_analysis = analyze_column_types(df)

    for column, details in column_analysis.items():

        if details["inferred_type"] != "likely_numeric":
            continue

        converted = pd.to_numeric(df[column], errors="coerce")

        invalid_mask = df[column].notna() & converted.isna()

        invalid_values = df.loc[invalid_mask, column]

        for index, value in invalid_values.items():
            suspicious_values.append({
                "row_index": int(index),
                "column": column,
                "value": str(value),
                "issue": "non-numeric value in likely numeric column"
            })

    return suspicious_values
