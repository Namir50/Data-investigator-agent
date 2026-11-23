from src.data_quality.validator import validate_age
from src.data_quality.validator import validate_income,  analyze_column_types, detect_suspicious_numeric_values, validate_dataset, validate_missing_values
import pandas as pd

def test_validate_age_flags_invalid_age():
    df = pd.DataFrame({
        "customer_id":[101,102,102,104],
        "age": [25,-1,32,150]
    })

    issues = validate_age(df)

    assert len(issues) == 2
    assert issues[0]['value'] == -1


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



def test_analyze_column_types_handles_empty_columns():
    df = pd.DataFrame({
        "age": [25, 30, 40],
        "salary": [None, None, None]
    })

    results = analyze_column_types(df)

    assert results["age"]["inferred_type"] == "likely_numeric"
    assert results["salary"]["inferred_type"] == "unknown"
    assert results["salary"]["numeric_ratio"] == 0.0

def test_analyze_column_types_handles_empty_columns_2():
    df = pd.DataFrame({
        "age": [],
        "salary": [],
        "department": []
    })

    results = analyze_column_types(df)

    assert results["age"]["inferred_type"] == "unknown"
    assert results["salary"]["inferred_type"] == "unknown"
    assert results["salary"]["numeric_ratio"] == 0.0


def test_validate_dataset():
    df1 = pd.DataFrame()
    results1 = validate_dataset(df1)
    assert results1['status'] == 'invalid dataset'
    assert results1["issues"][0]["issue"] == "dataset is empty"


    df2 = pd.DataFrame(columns=["name","age"])
    results2 = validate_dataset(df2)
    assert results2['status'] == 'invalid dataset'
    assert results2["issues"][0]["issue"] == "dataset has no rows"


    df3 = pd.DataFrame(index = [0,1,2])
    results3 = validate_dataset(df3)
    assert results3['status'] == 'invalid dataset'
    assert results3["issues"][0]["issue"] == "dataset has no columns"


    df4 = pd.DataFrame({
        "name": ["John", "Sam"],
        "age": [25, 30]
    })
    results4 = validate_dataset(df4)

    assert results4["status"] == "valid dataset"
    assert results4["message"] == "No structural errors detected."
    assert len(results4["issues"]) == 0


def test_validators_handle_mixed_data_types():
    df = pd.DataFrame({
        "age": [25, "150", "unknown", None, 100],
        "income": [45000, -2000, "unknown", None, 50000]
    })

    age_issues = validate_age(df)
    income_issues = validate_income(df)
    suspicious_issues = detect_suspicious_numeric_values(df)
    missing_issues = validate_missing_values(df)

    assert len(age_issues) == 1
    assert age_issues[0]["value"] == 150

    assert len(income_issues) == 1
    assert income_issues[0]["value"] == -2000.0

    assert len(suspicious_issues) == 2

    assert len(missing_issues) == 2


def test_validators_handle_mixed_data_types():
    df = pd.DataFrame({
        "age": [25, "150", "unknown", None, 100],
        "income": [45000, -2000, "unknown", None, 50000]
    })

    age_issues = validate_age(df)
    income_issues = validate_income(df)
    suspicious_issues = detect_suspicious_numeric_values(df)
    missing_issues = validate_missing_values(df)

    assert len(age_issues) == 1
    assert age_issues[0]["value"] == 150

    assert len(income_issues) == 1
    assert income_issues[0]["value"] == -2000.0

    assert len(suspicious_issues) == 2
    assert len(missing_issues) == 2