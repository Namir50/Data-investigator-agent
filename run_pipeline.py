import pandas as pd 
from pprint import pprint

from src.data_quality.pipeline import analyze_dataframe

df = pd.read_csv("data/sample_customers.csv",
            na_values=[" "])

report = analyze_dataframe(df)

print("\n-----Data Quality Report-----\n")

pprint(report)

print("\n-------------------------------")