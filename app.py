import json
import requests
import pandas as pd
from waitress import serve
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the dataset (Ensure UTF-8 encoding to avoid charmap errors)
try:
    df = pd.read_csv("processed_openfoodfacts.csv", encoding="utf-8", low_memory=False, dtype=str)
except Exception as e:
    print(f"❌ Error loading dataset: {e}")
    df = None

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "✅ Food Toxicity API is running!"})

# ================================
# ✅ 1. Barcode Scanning Endpoint
# ================================
@app.route('/scan_barcode', methods=['POST'])
def scan_barcode():
    try:
        data = request.json
        barcode = data.get("barcode")

        if not barcode:
            return jsonify({"error": "No barcode provided"})

        # Fetch product data from OpenFoodFacts API
        url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        response = requests.get(url)
        product_data = response.json()

        if "product" in product_data:
            product = product_data["product"]
            return jsonify({
                "product_name": product.get("product_name", "Unknown"),
                "energy-kcal_100g": product.get("nutriments", {}).get("energy-kcal_100g", 0),
                "additives_n": len(product.get("additives_tags", [])),
                "nova_group": product.get("nova_group", 0)
            })
        else:
            return jsonify({"error": "Product not found"})

    except Exception as e:
        return jsonify({"error": str(e)})

# =========================================
# ✅ 2. Food Toxicity Prediction Endpoint
# =========================================
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json  
        
        # Define the expected features based on the trained model
        model_features = ["energy-kcal_100g", "additives_n", "nova_group"]
        
        # Convert input to DataFrame with correct columns
        df_input = pd.DataFrame([data])
        df_input = df_input[model_features]  # Keep only required columns

        # Load ML model
        import joblib
        model = joblib.load("food_toxicity_model.pkl")
        predictions = model.predict(df_input)

        # JSON response
        response_data = {
            "toxicity": "Toxic 🚨" if int(predictions[0][0]) == 1 else "Safe ✅",
            "nova_group": int(predictions[0][2])
        }

        return app.response_class(
            response=json.dumps(response_data, ensure_ascii=False),
            status=200,
            mimetype="application/json"
        )

    except Exception as e:
        return jsonify({"error": str(e)})

# =========================================
# ✅ 3. Recommend Healthier Alternatives
# =========================================

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.json
        category = data.get("category", "").lower()

        if df is None:
            return jsonify({"error": "Dataset not loaded"})

        if "categories" not in df.columns:
            return jsonify({"error": "Category column missing from dataset"})

        # Define a "toxicity" threshold based on additives_n (assumption: more additives = more harmful)
        additives_threshold = 3  # Foods with >3 additives are considered "less healthy"

        # Filter dataset for same category & healthier options
        alternatives = df[
            (df["categories"].str.contains(category, case=False, na=False)) &
            (df["additives_n"].astype(float) <= additives_threshold)  # Keep only low-additive foods
        ].sort_values(by=["nova_group", "energy-kcal_100g"])

        # Return top 3 healthiest alternatives
        recommendations = alternatives[["product_name", "nova_group", "energy-kcal_100g"]].head(3).to_dict(orient="records")

        return jsonify({"best_alternatives": recommendations})

    except Exception as e:
        return jsonify({"error": str(e)})

# Run Flask server
if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=10000)

