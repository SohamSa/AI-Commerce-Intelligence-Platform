import joblib
import pandas as pd
from catboost import CatBoostClassifier, Pool

FEATURE_STORE_FILE = "ml_models/feature_store/business_feature_store.csv"
MODEL_FILE = "ml_models/artifacts/dense_slice_model.cbm"
LABEL_ENCODER_FILE = "ml_models/artifacts/dense_slice_label_encoder.pkl"
META_FILE = "ml_models/artifacts/dense_slice_meta.pkl"


def load_artifacts():
    model = CatBoostClassifier()
    model.load_model(MODEL_FILE)
    label_encoder = joblib.load(LABEL_ENCODER_FILE)
    meta = joblib.load(META_FILE)
    return model, label_encoder, meta


def prepare_input_row(vendor_id, meta):
    df = pd.read_csv(FEATURE_STORE_FILE)

    row = df[df["vendor_id"] == vendor_id].copy()
    if row.empty:
        raise ValueError(f"Vendor ID {vendor_id} not found.")

    metadata = {
        "vendor_id": int(row.iloc[0]["vendor_id"]),
        "business_name": row.iloc[0]["business_name"],
        "business_category": row.iloc[0]["business_category"],
        "geography_signal": row.iloc[0]["geography_signal"],
    }

    X = row[meta["feature_cols"]].copy()

    for col in meta["categorical_cols"]:
        X[col] = X[col].astype(str)

    return X, metadata


def predict_dense_slice(vendor_id):
    model, label_encoder, meta = load_artifacts()
    X, metadata = prepare_input_row(vendor_id, meta)

    pool = Pool(X, cat_features=meta["categorical_cols"])
    probabilities = model.predict_proba(pool)[0]
    top_indices = probabilities.argsort()[::-1][:3]

    top_predictions = [
        {
            "predicted_dense_slice": label_encoder.inverse_transform([idx])[0],
            "probability": round(float(probabilities[idx]), 4),
        }
        for idx in top_indices
    ]

    predicted_index = top_indices[0]
    predicted_label = label_encoder.inverse_transform([predicted_index])[0]
    confidence = float(probabilities[predicted_index])
    gap = confidence - float(probabilities[top_indices[1]])

    if confidence > 0.85:
        confidence_level = "High"
    elif confidence > 0.60:
        confidence_level = "Medium"
    else:
        confidence_level = "Low"

    ambiguity = "Low" if gap >= 0.15 else "High"

    dense_slice_to_strategy = {
        "Budget_Shoppers": "Lead with value messaging, pricing clarity, and practical offer framing.",
        "Young_Professionals": "Use convenience, quality, and outcome-focused positioning.",
        "College_Students": "Prioritize affordability, experimentation, and fast visual hooks.",
        "Suburban_Families": "Use trust, family utility, and repeat-purchase logic.",
        "Tech_Early_Adopters": "Lead with novelty, performance, and feature-led proof.",
        "DIY_Creators": "Use inspiration, tutorials, and project-led engagement.",
        "Urban_Female_20_30": "Use modern lifestyle aesthetics, identity alignment, and discovery hooks.",
        "Fitness_Enthusiasts": "Use performance, routine-building, and progress-driven messaging.",
        "Pet_Owners": "Use emotional connection, care routines, and repeat utility.",
        "Luxury_Buyers": "Use premium framing, exclusivity, and refinement-led creative."
    }

    result = {
        "vendor_id": metadata["vendor_id"],
        "business_name": metadata["business_name"],
        "business_category": metadata["business_category"],
        "geography_signal": metadata["geography_signal"],
        "top_predicted_dense_slice": predicted_label,
        "confidence": round(confidence, 4),
        "top_3_predictions": top_predictions,
        "decision_intelligence": {
            "confidence_level": confidence_level,
            "ambiguity": ambiguity,
            "recommended_strategy": dense_slice_to_strategy.get(
                predicted_label,
                "Test localized segment campaigns and compare community response."
            )
        }
    }

    return result


if __name__ == "__main__":
    vendor_id = 1001
    print(predict_dense_slice(vendor_id))