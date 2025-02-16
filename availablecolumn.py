import pandas as pd

# Define file path
file_path = "en.openfoodfacts.org.products.csv"  # Update with your correct path

# Read only the first 5 rows without filtering columns
df = pd.read_csv(file_path, sep="\t", encoding="utf-8", nrows=5)

# Print the column names to check for mismatches
print("Available columns in dataset:", df.columns.tolist())
