import joblib

# Load trained model
model = joblib.load("food_toxicity_xgboost.pkl")  # Change if using a different model

# Print feature names used during training
print("✅ Features used in training:", model.get_booster().feature_names)
