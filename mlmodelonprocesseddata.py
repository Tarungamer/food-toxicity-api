import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from xgboost import XGBClassifier
import joblib

# Load the processed dataset
df = pd.read_csv("processed_openfoodfacts.csv", dtype=str, low_memory=False)

# Define features and targets
features = ["energy-kcal_100g", "additives_n", "sodium_100g", "sugars_100g", "fat_100g", "proteins_100g", "fiber_100g"]
targets = ["toxicity_label", "nutriscore_grade", "nova_group"]

# Convert to numeric
for col in features + targets:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Drop missing values
df = df.dropna(subset=features + targets)

# Split data
X = df[features]
y = df[targets]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a multi-output model
clf = MultiOutputClassifier(XGBClassifier(n_estimators=200, learning_rate=0.1))
clf.fit(X_train, y_train)

# Save the model
joblib.dump(clf, "food_multioutput_model.pkl")
print("✅ Model saved as food_multioutput_model.pkl")
