import pandas as pd
from agents.quality_agent import DataQualityAgent


data = pd.read_csv("test_sales.csv")


agent = DataQualityAgent()


result = agent.analyze(data)


print(result)