import pandas as pd

def validate_age(df: pd.DataFrame) -> list[dict]:
    """flag rows where age is outside the allowed range"""
    issues = []

    numeric_age = pd.to_numeric(df['age'], errors='coerce')

    invalid_rows = df[(numeric_age<0) | (numeric_age>120)]

    for index,row in invalid_rows.iterrows():
        issues.append({
            "row_index":int(index),
            "column":"age",
            "value": int(numeric_age.loc[index]),
            "issue":"age is out of range"
        })
    return issues


def validate_income(df: pd.DataFrame) -> list[dict]:
    """flag rows where income is negative"""

    issues = []

    numeric_income = pd.to_numeric(df['income'], errors = 'coerce')

    invalid_rows  = df[numeric_income < 0]

    for index, row in invalid_rows.iterrows():
        issues.append({
            "row_index":int(index),
            "column": 'income',
            "value" : int(numeric_income.loc[index]),
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
                "issue":"missing value detected"
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

        if total_values == 0:
            inferred_type = "unknown"
        elif numeric_ratio > 0.50:
            inferred_type = "likely_numeric"
        else:
            inferred_type = "likely_text"

        results[column] = {
            "original_dtype": str(df[column].dtype),
            "numeric_ratio": round(float(numeric_ratio), 2),
            "inferred_type": inferred_type
        }

    return results

def get_numeric_columns(df: pd.DataFrame) -> list[str]:
    """Return columns classified as likely numeric."""

    column_analysis = analyze_column_types(df)

    numeric_columns = [
        column
        for column, details in column_analysis.items()
        if details["inferred_type"] == "likely_numeric"
    ]

    return numeric_columns


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

def validate_dataset(df: pd.DataFrame) -> dict:
    """Validate the basic structure of a dataset."""

    issues = []

    if len(df.index) == 0 and len(df.columns) == 0:
        issues.append({
            "issue": "dataset is empty",
            "description": "The dataset contains no rows and no columns."
        })

    elif len(df.index) == 0:
        issues.append({
            "issue": "dataset has no rows",
            "description": "The dataset contains no rows."
        })

    elif len(df.columns) == 0:
        issues.append({
            "issue": "dataset has no columns",
            "description": "The dataset contains no columns."
        })

    return {
        "status": "valid dataset" if not issues else "invalid dataset",
        "message": "No structural errors detected." if not issues else "Structural errors detected.",
        "issues": issues
    }



def execute_rule(series: pd.Series, rule: dict) -> pd.Series:
    " ""Execute one validation rule against a Pandas Series."""

    rule_type = rule["type"]

    numeric_series = pd.to_numeric(series, errors="coerce")

    if rule_type == "min":
        return numeric_series < rule["value"]

    elif rule_type == "max":
        return numeric_series > rule["value"]

    elif rule_type == "non_negative":
        return numeric_series < 0

    elif rule_type == "positive":
        return numeric_series <= 0

    else:
        raise ValueError(f"Unsupported rule type: {rule_type}")


def validate_with_rules(df: pd.DataFrame, validation_rules: dict) -> list[dict]:
    """Apply AI-generated validation rules to a DataFrame."""

    issues = []

    for column, column_config in validation_rules.items():

        if column not in df.columns:
            continue

        for rule in column_config["rules"]:

            invalid_mask = execute_rule(df[column], rule)

            invalid_rows = df.loc[invalid_mask]

            for index, row in invalid_rows.iterrows():

                issues.append({
                    "row_index": int(index),
                    "column": column,
                    "value": row[column],
                    "rule": rule["type"],
                    "issue": f"Value violates {rule['type']} rule"
                })

    return issues
 



