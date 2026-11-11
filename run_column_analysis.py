
import pandas as pd

from src.data_quality.validator import (
    analyze_column_types,
    detect_suspicious_numeric_values
)

# Create a sample dataset
df = pd.DataFrame({
    "age": ["25", "30", "forty", "45"],
    "salary": ["40000", "50000", "unknown", "60000"],
    "department": ["IT", "HR", "Finance", "IT"],
    "joining_year": [2020, 2021, 2019, 2022]
})

# Step 1: Analyse column types
column_analysis = analyze_column_types(df)

print("\n----- COLUMN ANALYSIS -----")
for column, details in column_analysis.items():
    print(column, details)

# Step 2: Detect suspicious numeric values
suspicious_values = detect_suspicious_numeric_values(df)

print("\n----- SUSPICIOUS VALUES -----")
for issue in suspicious_values:
    print(issue)
