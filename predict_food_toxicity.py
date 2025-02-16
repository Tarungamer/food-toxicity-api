import joblib
import numpy as np
import pandas as pd

# Load the trained model
model = joblib.load("food_toxicity_model.pkl")

# Define column names (must match training features)
feature_names = ["energy-kcal_100g", "additives_n", "nova_group"]

# Example: New food product data
new_food = pd.DataFrame(np.array([[300, 5, 3]]), columns=feature_names)

# Predict toxicity
prediction = model.predict(new_food)

# Output result
print(f"Predicted Toxicity: {'Toxic 🚨' if prediction[0] == 1 else 'Safe ✅'}")
