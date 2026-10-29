
from src.data_quality.profiler import profile_csv


def test_profile_counts_rows(tmp_path):
    csv_file = tmp_path / "sample.csv"

    csv_file.write_text(
        "customer_id,age\n"
        "101,25\n"
        "102,32\n"
        "103,45\n",
        encoding="utf-8",
    )

    profile = profile_csv(csv_file)

    assert profile["row_count"] == 3
    assert profile["columns"]["age"]["missing_count"] == 0
    assert profile["columns"]["age"]["unique_count"] == 3
