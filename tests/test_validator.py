from src.data_quality.validator import validate_age
from src.data_quality.validator import validate_income
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
    
    
