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