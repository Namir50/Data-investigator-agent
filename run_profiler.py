
from pprint import pprint

from src.data_quality.profiler import profile_dataframe

profile = profile_dataframe("data/sample_customers.csv")

pprint(profile)
