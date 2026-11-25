
import pandas as pd

from src.data_quality.validator import validate_with_rules


df = pd.read_csv(
    "data/sample_customers.csv",
    skipinitialspace=True,
    na_values=[" "]
)

validation_rules = {
    "age": {
        "rules": [
            {"type": "min", "value": 0},
            {"type": "max", "value": 120}
        ]
    },
    "income": {
        "rules": [
            {"type": "non_negative"}
        ]
    },
    "experience": {
        "rules": [
            {"type": "non_negative"}
        ]
    }
}

issues = validate_with_rules(df, validation_rules)

for issue in issues:
    print(issue)

print(f"\nTotal issues detected: {len(issues)}")
