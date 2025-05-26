import pandas as pd

# Load the dataset
df = pd.read_csv('ECommerce_consumer behaviour.csv')  # Replace with your actual file name

# 1. Remove exact duplicate rows
df = df.drop_duplicates()

# 2. Replace NaNs in 'days_since_prior_order' with -1
df['days_since_prior_order'] = df['days_since_prior_order'].fillna(-1)

# 3. Convert to integers
df['days_since_prior_order'] = df['days_since_prior_order'].astype(int)

# 4. Split the cleaned dataset into two halves
midpoint = len(df) // 2
first_half = df.iloc[:midpoint]
second_half = df.iloc[midpoint:]

# 5. Save to separate CSVs (with headers included)
first_half.to_csv('cleaned_dataset_part1.csv', index=False, header=True)
second_half.to_csv('cleaned_dataset_part2.csv', index=False, header=True)

print("✅ Cleaned data saved into 'cleaned_dataset_part1.csv' and 'cleaned_dataset_part2.csv' with headers.")

