"""
recommend.py

A script to recommend top-5 products based on user input (age, gender, hobbies).
Run in terminal:
    python recommend.py

If first time running, make sure to have the files in the same directory as in the repo.
Ensure you have modified the script for running in your environment.
chmod +x recommend.py # make it executable
./recommend.py



"""

import joblib
import pandas as pd

def main():
    # 1) Collect user input from the terminal
    print("=== Welcome to the Recommendation Script ===")
    age_input = input("Enter age (e.g. 30): ")
    gender_input = input("Enter gender (e.g. male/female): ")
    hobbies_input = input("Enter hobbies (comma-separated, e.g. cars,gaming): ")

    try:
        user_age = int(age_input)
    except ValueError:
        print(f"Invalid age '{age_input}'. Defaulting to 30.")
        user_age = 30

    user_gender = gender_input.strip().lower() or "unknown"
    user_hobbies = hobbies_input.strip().lower() or "none"
    
    # 2) Load the trained model
    model = joblib.load("final_model.pkl")
    print("\n[INFO] Model loaded successfully.")

    # 3) Load the product catalog (same columns as training, minus user-specific)
    products_df = pd.read_csv("final_dataset.csv")
    print("[INFO] Products data loaded. Rows:", len(products_df))

    # 4) Load encoders/scalers used during training
    gender_encoder = joblib.load("gender_encoder.pkl")
    cat_encoder = joblib.load("category_encoder.pkl")
    hobby_encoder = joblib.load("hobby_encoder.pkl")
    price_scaler = joblib.load("price_scaler.pkl")
    stars_scaler = joblib.load("stars_scaler.pkl")
    hci_encoder = joblib.load("hobbies_category_interaction_encoder.pkl")

    # 5) Prepare candidate products for prediction
    candidates = products_df.copy()

    # Fill missing where appropriate
    candidates["category_name"] = candidates["category_name"].fillna("Unknown")
    # Encode category_name -> category_encoded
    candidates["category_encoded"] = cat_encoder.transform(candidates["category_name"])

    if user_hobbies not in hobby_encoder.classes_:
        user_hobbies = "none"

    candidates["hobbies_encoded"] = hobby_encoder.transform([user_hobbies])[0]

    # 3) Create the interaction
    candidates["hobbies_category_interaction"] = (
    candidates["hobbies_encoded"] * candidates["category_encoded"]
)

    # Scale numeric columns
    # candidates["price_scaled"] = price_scaler.transform(candidates[["price"]])
    # candidates["stars_scaled"] = stars_scaler.transform(candidates[["stars"]])

    # already scaled numeric columns price and stars


    # 6) Add user columns to each product row
    candidates["age"] = user_age

    # Handle unknown gender
    if user_gender not in gender_encoder.classes_:
        user_gender = "unknown"
    candidates["gender_encoded"] = gender_encoder.transform([user_gender])[0]

    # Convert isBestSeller to int if needed
    if "isBestSeller" in candidates.columns:
        candidates["isBestSeller"] = candidates["isBestSeller"].astype(int)


    
    # Convert isBestSeller to int if needed
    if "isBestSeller" in candidates.columns:
        candidates["isBestSeller"] = candidates["isBestSeller"].astype(int)

    print("\n[INFO] Candidate data prepared. Rows:", len(candidates), "\n",
          candidates[["age", "gender_encoded", "hobbies_encoded"]].head(10))

    
    # # Quick debug
    # print("\n[INFO] Candidate data prepared. Rows:", len(candidates))
    # print(candidates[["age", "gender_encoded", "hobbies_encoded", "hobbies_category_interaction", "hci_encoded"]].head(10))

    # 8) Build your final feature matrix (replace the string column with hci_encoded)
    feature_cols = [
        "age",
        "gender_encoded",
        "hobbies_encoded",
        "price_scaled",
        "stars_scaled",
        "category_encoded",
        "isBestSeller",
        "hobbies_category_interaction"  # now numeric
    ]

    X_candidates = candidates[feature_cols]


    print("\n[INFO] Actual X_candidates passed to model for prediction:\n", X_candidates.head(10))

    # 9) Predict probabilities
    proba = model.predict_proba(X_candidates)[:, 1]
    candidates["score"] = proba

    # Drop duplicates on product_id before sorting
    candidates_unique = candidates.drop_duplicates(subset="product_id")

    # 10) Sort by top scores and print top 5
    top_5 = candidates_unique.nlargest(5, "score")

    print("\n===== TOP 5 RECOMMENDATIONS =====\n")
    total_score = 0.0
    for idx, row in top_5.iterrows():
        p_id = row["product_id"]
        title = str(row["title"])[:40] if "title" in row else "No Title"
        score_pct = row["score"] * 100
        total_score += row["score"]
        print(f"{p_id}\t{title}...\tlike probability: {score_pct:.2f}%")

    avg_score = (total_score / 5.0) * 100
    print(f"\nAverage predicted probability among top-5: {avg_score:.2f}%\n")

    top_candidates = candidates.nlargest(10, "score")
    print(top_candidates[["product_id", "score"]])

    # Debug prints
    print("\n(DEBUG):\n", candidates[["hobbies_encoded", "category_encoded", "hobbies_category_interaction"]].head(10))

if __name__ == "__main__":
    main()