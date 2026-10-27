
from pprint import pprint

from src.data_quality.profiler import profile_csv

profile = profile_csv("data/sample_customers.csv")

pprint(profile)
