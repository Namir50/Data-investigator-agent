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



def detect_numeric_candidates(df: pd.DataFrame) -> list[dict]:
    """
    Identify non-missing values that cannot be converted into numbers.
    The original DataFrame is never modified.
    """

    # Create an empty list to store all detected issues
    issues = []

    # Loop through every column in the DataFrame
    for column in df.columns:

        # Attempt to convert the current column into numeric values.
        # If conversion fails, pandas replaces that value with NaN.
        # This creates a temporary Series; the original DataFrame is unchanged.
        converted = pd.to_numeric(df[column], errors="coerce")

        # Identify values that:
        # 1. Were NOT missing in the original DataFrame.
        # 2. Became NaN after numeric conversion.
        #
        # '&' means both conditions must be True.
        invalid_mask = df[column].notna() & converted.isna()

        # Use Boolean indexing to retrieve the ORIGINAL values
        # from rows where invalid_mask is True.
        invalid_values = df.loc[invalid_mask, column]

        # Loop through the suspicious values.
        # .items() gives us both the row index and the original value.
        for index, value in invalid_values.items():

            # Add each detected issue to our issues list
            issues.append({
                "row_index": int(index),  # Row containing the suspicious value
                "column": column,         # Name of the column
                "value": str(value),      # Original suspicious value
                "issue": "value cannot be converted to a number"
            })

    # Return all detected issues after inspecting every column
    return issues
