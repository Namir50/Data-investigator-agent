import pandas as pd

from src.data_quality.pipeline import analyze_dataframe


def test_analyze_dataframe():
    df = pd.DataFrame({
        "customer_id": [101, 102, 103],
        "age": [25, 150, 132],
        "income": [30000, -5000, 40000],
    })

    report = analyze_dataframe(df)

    assert report["profile"]["row_count"] == 3
    assert report["profile"]["column_count"] == 3

    assert report["issue_count"] == 3
    assert len(report["issues"]) == 3