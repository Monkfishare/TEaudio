import pandas as pd
import json

df = pd.read_csv('economist_data.csv')
data = df.to_dict(orient='records')

with open('data.json', 'w') as file:
    json.dump(data, file, indent=4)
