import pandas as pd

df = pd.read_csv('../results/results_2020-07-22_13-25-37.csv')

detected = df['detected']
detected_count = detected.value_counts().rename_axis('detected').reset_index(name = 'frequency')

print(detected_count)
