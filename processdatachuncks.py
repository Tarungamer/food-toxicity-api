import pandas as pd

# -----------------------------
# Step 1: Define File Path & Columns to Extract
# -----------------------------
file_path = "en.openfoodfacts.org.products.csv"  # Replace with your actual file path

# Define only the necessary columns (to reduce memory usage)
columns_to_keep = [
    "code", "product_name", "categories", "ingredients_text",
    "energy-kcal_100g",  # Corrected column name
    "additives_n", "labels", "nova_group"
]



# -----------------------------
# Step 2: Process Dataset in Chunks
# -----------------------------
chunk_size = 100000  # Read 100,000 rows at a time
filtered_data = []

for chunk in pd.read_csv(file_path, usecols=columns_to_keep, sep="\t", encoding="utf-8", low_memory=False, chunksize=chunk_size):
    # Drop rows with missing important data
    chunk = chunk.dropna(subset=["product_name", "ingredients_text"])

    # Filter: Keep only relevant food categories
    valid_categories = ["Snacks", "Beverages", "Dairy products", "Bread", "Cereals", "Frozen foods"]
    chunk = chunk[chunk["categories"].str.contains('|'.join(valid_categories), na=False, case=False)]

    # Append filtered data to the list
    filtered_data.append(chunk)

# Merge all processed chunks
df_processed = pd.concat(filtered_data, ignore_index=True)

# -----------------------------
# Step 3: Save the Processed Dataset
# -----------------------------
output_file = "processed_openfoodfacts.csv"
df_processed.to_csv(output_file, index=False)
print(f"✅ Processed dataset saved as {output_file}. Total products: {len(df_processed)}")
