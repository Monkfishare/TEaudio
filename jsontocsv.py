import pandas as pd
import json

with open('data.json', 'r') as file:
    data = json.load(file)

df = pd.DataFrame(data)

csv_file_path = 'economist_data.csv'
df.to_csv(csv_file_path, index=False)
