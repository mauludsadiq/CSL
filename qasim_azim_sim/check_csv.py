import pandas as pd

# Open the CSV file
data = pd.read_csv('output/trajectory_data.csv')

# Print the first 5 rows
print("First 5 rows of the data:")
print(data.head())

# Print a summary of the data (types, non-empty rows)
print("\nSummary info about the data:")
print(data.info())

# Print some simple statistics to see the ranges
print("\nBasic statistics about the data:")
print(data.describe())
