from src.data_quality.validator import validate_age
from src.data_quality.validator import validate_income, detect_numeric_candidates
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


def test_detect_numeric_candidates():
    df = pd.DataFrame({
        "age": ["25", "30", "forty", "45"],
        "salary": ["40000", "50000", "unknown", "60000"],
        "department": ["IT", "HR", "Finance", "IT"]
    })

    issues = detect_numeric_candidates(df)

    # Check that suspicious values were detected
    assert len(issues) == 6

    # Check that the original suspicious values are present
    detected_values = [issue["value"] for issue in issues]

    assert "forty" in detected_values
    assert "unknown" in detected_values

    # Check that the original DataFrame was not modified
    assert df.loc[2, "age"] == "forty"
    assert df.loc[2, "salary"] == "unknown"

    
    
