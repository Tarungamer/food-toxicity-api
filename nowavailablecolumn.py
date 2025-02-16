import pandas as pd

# Load dataset (ensure UTF-8 encoding to avoid charmap issues)
df = pd.read_csv("processed_openfoodfacts.csv", encoding="utf-8", low_memory=False, dtype=str)

# Print available columns
print("\n✅ Available Columns in Dataset:")
print(df.columns.tolist())

# Show first few rows
print("\n✅ Sample Data:")
print(df.head())
