from src.data_quality.validator import validate_age
from src.data_quality.validator import validate_income,  analyze_column_types, detect_suspicious_numeric_values
import pandas as pd

def test_validate_age_flags_invalid_age():
    df = pd.DataFrame({
        "customer_id":[101,102,102,104],
        "age": [25,-1,32,150]
    })

    issues = validate_age(df)

    assert len(issues) == 2
    assert issues[0]['age'] == -1


def test_validate_income_flags_negative_income():
    df = pd.DataFrame({
        "customer_id":[101,102],
        "income": [25000,-100]
    })
    issues = validate_income(df)

    assert len(issues) == 1
    assert issues[0]['column'] == 'income'
    assert issues[0]['value'] == -100




def test_analyze_column_types():
    df = pd.DataFrame({
        "age": ["25", "30", "forty", "45"],
        "department": ["IT", "HR", "Finance", "IT"],
        "joining_year": [2020, 2021, 2019, 2022]
    })

    results = analyze_column_types(df)

    assert results["age"]["numeric_ratio"] == 0.75
    assert results["age"]["inferred_type"] == "likely_numeric"

    assert results["department"]["numeric_ratio"] == 0.0
    assert results["department"]["inferred_type"] == "likely_text"

    assert results["joining_year"]["inferred_type"] == "likely_numeric"


def test_detect_suspicious_numeric_values():
    df = pd.DataFrame({
        "age": ["25", "30", "forty", "45"],
        "department": ["IT", "HR", "Finance", "IT"]
    })

    original_df = df.copy(deep=True)

    issues = detect_suspicious_numeric_values(df)

    assert len(issues) == 1
    assert issues[0]["column"] == "age"
    assert issues[0]["value"] == "forty"
    assert issues[0]["row_index"] == 2

    pd.testing.assert_frame_equal(df, original_df)

    
