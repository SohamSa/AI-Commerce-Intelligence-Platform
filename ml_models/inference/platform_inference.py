import joblib
import pandas as pd

FEATURE_STORE_FILE = "ml_models/feature_store/business_feature_store.csv"
MODEL_FILE = "ml_models/artifacts/platform_model.pkl"
LABEL_ENCODER_FILE = "ml_models/artifacts/platform_label_encoder.pkl"
META_FILE = "ml_models/artifacts/platform_meta.pkl"


def load_artifacts():
    model = joblib.load(MODEL_FILE)
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
    X = pd.get_dummies(X, columns=meta["categorical_cols"])

    for col in meta["encoded_feature_columns"]:
        if col not in X.columns:
            X[col] = 0

    X = X[meta["encoded_feature_columns"]]
    return X, metadata


def predict_platform(vendor_id):
    model, label_encoder, meta = load_artifacts()
    X, metadata = prepare_input_row(vendor_id, meta)

    probabilities = model.predict_proba(X)[0]
    top_indices = probabilities.argsort()[::-1][:3]

    top_predictions = [
        {
            "predicted_platform": label_encoder.inverse_transform([idx])[0],
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

    platform_to_strategy = {
        "TikTok": "Use short-form hooks, fast trend capture, and creator-native content loops.",
        "Website_First": "Invest in owned funnels, SEO, email capture, and landing-page conversion.",
        "Micro_Influencers": "Use niche creators, trust-based recommendations, and small audience precision.",
        "Pinterest": "Use discovery-led visuals, evergreen boards, and search-intent inspiration content.",
        "Discord": "Build retention through private communities, insider access, and repeated engagement.",
        "Facebook_Groups": "Use discussion-led community growth, trust loops, and local or interest-group activation.",
        "Reddit": "Win through specificity, authenticity, and problem-solution discussion in niche communities.",
        "Instagram": "Use visual storytelling, short-form content, and conversion-oriented creatives.",
        "YouTube_Shorts": "Use educational discovery, repeated short-form reach, and visual demonstration.",
        "Marketplace_First": "Prioritize high-conversion listings, ratings, and transaction-first distribution.",
    }

    result = {
        "vendor_id": metadata["vendor_id"],
        "business_name": metadata["business_name"],
        "business_category": metadata["business_category"],
        "geography_signal": metadata["geography_signal"],
        "top_predicted_platform": predicted_label,
        "confidence": round(confidence, 4),
        "top_3_predictions": top_predictions,
        "decision_intelligence": {
            "confidence_level": confidence_level,
            "ambiguity": ambiguity,
            "recommended_strategy": platform_to_strategy.get(
                predicted_label,
                "Run a controlled platform test and compare conversion efficiency."
            )
        }
    }

    return result


if __name__ == "__main__":
    vendor_id = 1001
    print(predict_platform(vendor_id))