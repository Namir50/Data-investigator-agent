import pandas as pd

from src.data_quality.profiler import profile_dataframe


def test_profile_dataframe():
    df = pd.DataFrame({
        "customer_id": [101, 102, 102],
        "age": [25, None, None],
    })

    profile = profile_dataframe(df)

    assert profile["row_count"] == 3
    assert profile["column_count"] == 2

    assert profile["columns"]["age"]["missing_count"] == 2
    assert profile["columns"]["age"]["missing_percentage"] == 66.67

    assert profile["duplicate_count"] == 1