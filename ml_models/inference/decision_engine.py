import joblib
import pandas as pd

FEATURE_STORE_FILE = "ml_models/feature_store/business_feature_store.csv"

NICHE_MODEL_PATH = "ml_models/artifacts/niche_model.pkl"
NICHE_LABEL_ENCODER_PATH = "ml_models/artifacts/niche_label_encoder.pkl"
NICHE_META_PATH = "ml_models/artifacts/niche_meta.pkl"

PLATFORM_MODEL_PATH = "ml_models/artifacts/platform_model.pkl"
PLATFORM_LABEL_ENCODER_PATH = "ml_models/artifacts/platform_label_encoder.pkl"
PLATFORM_META_PATH = "ml_models/artifacts/platform_meta.pkl"

DENSE_MODEL_PATH = "ml_models/artifacts/dense_slice_model.pkl"
DENSE_LABEL_ENCODER_PATH = "ml_models/artifacts/dense_slice_label_encoder.pkl"
DENSE_META_PATH = "ml_models/artifacts/dense_slice_meta.pkl"


def load_model_bundle(model_path, label_encoder_path, meta_path):
    model = joblib.load(model_path)
    label_encoder = joblib.load(label_encoder_path)
    meta = joblib.load(meta_path)
    return model, label_encoder, meta


def prepare_input(df: pd.DataFrame, meta: dict) -> pd.DataFrame:
    feature_cols = meta["feature_cols"]
    categorical_cols = meta["categorical_cols"]
    encoded_feature_columns = meta["encoded_feature_columns"]

    X = df[feature_cols].copy()
    X = pd.get_dummies(X, columns=categorical_cols)
    X = X.reindex(columns=encoded_feature_columns, fill_value=0)
    return X


def predict_top_1(model, label_encoder, X: pd.DataFrame):
    probs = model.predict_proba(X)[0]
    idx = probs.argmax()

    label = label_encoder.inverse_transform([idx])[0]
    prob = float(probs[idx])

    return {"label": label, "probability": round(prob, 4)}


def get_business_stage(row: pd.Series) -> str:
    conversion = row["conversion_readiness_score"]
    repeat = row["repeat_purchase_rate"]
    loyalty = row["brand_loyalty_score"]

    if conversion < 0.40 and repeat < 0.40:
        return "Early Stage"
    elif conversion < 0.65 and loyalty < 0.60:
        return "Growth Stage"
    else:
        return "Mature Stage"


def get_product_style(row: pd.Series) -> str:
    if row["is_visual_product"] >= 0.65:
        return "Visual Product"
    elif row["is_utility_product"] >= 0.65:
        return "Utility Product"
    else:
        return "Hybrid Product"


def build_strategy(niche: str, platform: str, dense_slice: str, row: pd.Series) -> dict:
    stage = get_business_stage(row)
    product_style = get_product_style(row)

    strategy_map = {
        "DIY_Crafters": "Lead with tutorials, creator demos, and community proof.",
        "Healthy_Eating": "Lead with trust, routines, and repeat purchase messaging.",
        "Pet_Lovers": "Use emotional storytelling, UGC, and repeat-purchase bundles.",
        "Home_Decor_Lovers": "Use visual inspiration, before-after content, and aesthetic positioning.",
        "Online_Learners": "Use educational value, long-form explanation, and proof of usefulness.",
        "Organic_Beauty": "Use trust, ingredients, brand story, and premium positioning.",
        "Skincare_Enthusiasts": "Use ingredient education, routine logic, and transformation proof.",
        "Streetwear_Fans": "Use trend-led visuals, drops, scarcity, and identity.",
        "Gadget_Geeks": "Use product depth, technical comparisons, and research-driven content.",
        "Gym_Beginners": "Use motivation, quick wins, and beginner-friendly positioning.",
    }

    platform_map = {
        "TikTok": "Use short-form hooks, fast demos, and trend-native creatives.",
        "Instagram": "Use strong visuals, creator content, and aesthetic storytelling.",
        "Reddit": "Use trust-building, honest explanations, and discussion-led positioning.",
        "Pinterest": "Use visual inspiration, save-worthy content, and intent-driven discovery.",
        "Website_First": "Optimize landing pages, intent capture, and conversion flow.",
        "Marketplace_First": "Compete on clarity, reviews, and conversion-ready positioning.",
        "Facebook_Groups": "Use community trust, referrals, and social proof.",
        "Discord": "Use niche community engagement and retention loops.",
        "YouTube_Shorts": "Use short educational or demonstration-led videos.",
        "Micro_Influencers": "Use creator partnerships and authentic product proof.",
    }

    dense_slice_map = {
        "College_Students": "Keep pricing accessible and content energetic.",
        "Young_Professionals": "Focus on convenience, identity, and practical value.",
        "Luxury_Buyers": "Use premium storytelling, exclusivity, and trust.",
        "Fitness_Enthusiasts": "Use performance, progress, and motivational framing.",
        "Pet_Owners": "Use emotional trust and routine-driven repeat value.",
        "Suburban_Families": "Emphasize practicality, reliability, and repeat utility.",
        "Tech_Early_Adopters": "Use innovation, detail, and differentiation.",
        "Urban_Female_20_30": "Use aesthetic identity, relevance, and social proof.",
        "Budget_Shoppers": "Lead with value, bundles, and affordability.",
        "DIY_Creators": "Lead with creator proof, tutorials, and hands-on value.",
    }

    return {
        "business_stage": stage,
        "product_style": product_style,
        "niche_strategy": strategy_map.get(niche, "Use niche-specific positioning."),
        "platform_strategy": platform_map.get(platform, "Use platform-native content."),
        "dense_slice_strategy": dense_slice_map.get(dense_slice, "Tailor the offer to the audience segment."),
    }


def run_decision_engine_by_vendor_id(vendor_id: str):
    df = pd.read_csv(FEATURE_STORE_FILE)
    df["vendor_id"] = df["vendor_id"].astype(str)

    matched_rows = df[df["vendor_id"] == vendor_id]

    if matched_rows.empty:
        raise ValueError(f"Vendor ID {vendor_id} not found in feature store.")

    single_row = matched_rows.iloc[[0]].copy()
    row = single_row.iloc[0]

    niche_model, niche_encoder, niche_meta = load_model_bundle(
        NICHE_MODEL_PATH, NICHE_LABEL_ENCODER_PATH, NICHE_META_PATH
    )
    platform_model, platform_encoder, platform_meta = load_model_bundle(
        PLATFORM_MODEL_PATH, PLATFORM_LABEL_ENCODER_PATH, PLATFORM_META_PATH
    )
    dense_model, dense_encoder, dense_meta = load_model_bundle(
        DENSE_MODEL_PATH, DENSE_LABEL_ENCODER_PATH, DENSE_META_PATH
    )

    X_niche = prepare_input(single_row, niche_meta)
    X_platform = prepare_input(single_row, platform_meta)
    X_dense = prepare_input(single_row, dense_meta)

    niche_pred = predict_top_1(niche_model, niche_encoder, X_niche)
    platform_pred = predict_top_1(platform_model, platform_encoder, X_platform)
    dense_pred = predict_top_1(dense_model, dense_encoder, X_dense)

    best_niche = niche_pred["label"]
    best_platform = platform_pred["label"]
    best_dense = dense_pred["label"]

    strategy = build_strategy(best_niche, best_platform, best_dense, row)

    result = {
        "vendor_id": row["vendor_id"],
        "business_name": row["business_name"],
        "actual_niche": row["target_micro_niche"],
        "actual_platform": row["target_platform"],
        "actual_dense_slice": row["target_dense_slice"],
        "niche_prediction": niche_pred,
        "platform_prediction": platform_pred,
        "dense_slice_prediction": dense_pred,
        "recommended_combination": {
            "niche": best_niche,
            "platform": best_platform,
            "dense_slice": best_dense,
        },
        "business_recommendation": strategy,
    }

    return result


def print_decision_report(result: dict):
    print("\n" + "=" * 100)
    print("FINAL DECISION ENGINE REPORT")
    print("=" * 100)

    print(f"\nBusiness Name: {result['business_name']}")
    print(f"Actual Niche: {result['actual_niche']}")
    print(f"Actual Platform: {result['actual_platform']}")
    print(f"Actual Dense Slice: {result['actual_dense_slice']}")

    print("\nPredicted Niche:")
    print(f"  {result['niche_prediction']['label']} -> {result['niche_prediction']['probability']}")

    print("\nPredicted Platform:")
    print(f"  {result['platform_prediction']['label']} -> {result['platform_prediction']['probability']}")

    print("\nPredicted Dense Slice:")
    print(f"  {result['dense_slice_prediction']['label']} -> {result['dense_slice_prediction']['probability']}")

    print("\nRecommended Combination:")
    print(f"  Niche: {result['recommended_combination']['niche']}")
    print(f"  Platform: {result['recommended_combination']['platform']}")
    print(f"  Dense Slice: {result['recommended_combination']['dense_slice']}")

    print("\nBusiness Recommendation:")
    print(f"  Stage: {result['business_recommendation']['business_stage']}")
    print(f"  Product Style: {result['business_recommendation']['product_style']}")
    print(f"  Niche Strategy: {result['business_recommendation']['niche_strategy']}")
    print(f"  Platform Strategy: {result['business_recommendation']['platform_strategy']}")
    print(f"  Dense Slice Strategy: {result['business_recommendation']['dense_slice_strategy']}")
    print("\n" + "=" * 100)


def main():
    try:
        df = pd.read_csv(FEATURE_STORE_FILE)
        df["vendor_id"] = df["vendor_id"].astype(str)

        vendor_ids = sorted(df["vendor_id"].unique(), key=lambda x: int(x))
        min_vendor_id = vendor_ids[0]
        max_vendor_id = vendor_ids[-1]

        print(f"Available vendor_id range: {min_vendor_id} to {max_vendor_id}")

        vendor_id = input("Enter vendor_id: ").strip()

        if vendor_id not in set(vendor_ids):
            raise ValueError(
                f"Vendor ID {vendor_id} not found. Please enter a valid vendor ID from the dataset."
            )

        result = run_decision_engine_by_vendor_id(vendor_id)
        print_decision_report(result)

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()