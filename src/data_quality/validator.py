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
