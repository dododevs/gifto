import pandas as pd
import os
import joblib
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# 1) Load the original training dataset
csv_path = "user_product_dataset.csv"
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV not found at: {csv_path}")

df_training = pd.read_csv(csv_path)
print("[INFO] Loaded training data:", df_training.shape)

# 2) Clean/prepare the columns the same way as in training
#    Ensure we have these columns. Fill missing values if needed.
if "gender" not in df_training.columns:
    raise KeyError("Column 'gender' is missing from df_training")
df_training["gender"] = df_training["gender"].fillna("Unknown")

if "category_name" not in df_training.columns:
    raise KeyError("Column 'category_name' is missing from df_training")
df_training["category_name"] = df_training["category_name"].fillna("Unknown")

if "hobbies" not in df_training.columns:
    raise KeyError("Column 'hobbies' is missing from df_training")
df_training["hobbies"] = df_training["hobbies"].fillna("none")

# 3) Create or fill the 'hobbies_category_interaction' column
#    If you already generated this column in your pipeline, just fillna.
#    Otherwise, let's create it by combining 'hobbies' and 'category_name'.
if "hobbies_category_interaction" not in df_training.columns:
    print("[INFO] Creating 'hobbies_category_interaction' on the fly...")
    df_training["hobbies_category_interaction"] = (
        df_training["hobbies"] + "_" + df_training["category_name"]
    )

df_training["hobbies_category_interaction"] = df_training["hobbies_category_interaction"].fillna("none")

# 4) Re-instantiate LabelEncoders for gender, category, hobbies, and h-c interaction
gender_encoder = LabelEncoder()
gender_encoder.fit(df_training["gender"].unique())

cat_encoder = LabelEncoder()
cat_encoder.fit(df_training["category_name"].unique())

hobby_encoder = LabelEncoder()
hobby_encoder.fit(df_training["hobbies"].unique())

hobbies_category_interaction_encoder = LabelEncoder()
hobbies_category_interaction_encoder.fit(df_training["hobbies_category_interaction"].unique())

# 5) Fit MinMaxScaler on 'price' and 'stars', verifying columns exist
if "price" not in df_training.columns:
    raise KeyError("Column 'price' is missing from df_training")
if "stars" not in df_training.columns:
    raise KeyError("Column 'stars' is missing from df_training")

price_scaler = MinMaxScaler()
price_scaler.fit(df_training[["price"]])   # or df_training['price'].values.reshape(-1,1)

stars_scaler = MinMaxScaler()
stars_scaler.fit(df_training[["stars"]])

# 6) Save encoders and scalers so you can load them in your recommend script
joblib.dump(gender_encoder, "gender_encoder.pkl")
joblib.dump(cat_encoder, "category_encoder.pkl")
joblib.dump(hobby_encoder, "hobby_encoder.pkl")
joblib.dump(hobbies_category_interaction_encoder, "hobbies_category_interaction_encoder.pkl")
joblib.dump(price_scaler, "price_scaler.pkl")
joblib.dump(stars_scaler, "stars_scaler.pkl")

print("\n=== Encoders and scalers re-instantiated and saved! ===")
print("Saved files:")
print("  - gender_encoder.pkl")
print("  - category_encoder.pkl")
print("  - hobby_encoder.pkl")
print("  - hobbies_category_interaction_encoder.pkl")
print("  - price_scaler.pkl")
print("  - stars_scaler.pkl")