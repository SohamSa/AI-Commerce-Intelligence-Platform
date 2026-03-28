import os
import joblib
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_sample_weight

INPUT_FILE = "ml_models/feature_store/business_feature_store.csv"
MODEL_OUTPUT = "ml_models/artifacts/dense_slice_model.pkl"
LABEL_ENCODER_OUTPUT = "ml_models/artifacts/dense_slice_label_encoder.pkl"
META_OUTPUT = "ml_models/artifacts/dense_slice_meta.pkl"

FEATURE_COLS = [
    "business_category",
    "price_range",
    "content_format",
    "purchase_frequency",
    "geography_signal",
    "data_source_coverage",

    "is_visual_product",
    "is_utility_product",
    "brand_loyalty_score",
    "impulse_buy_score",
    "research_time_score",
    "video_consumption_score",
    "image_engagement_score",
    "text_engagement_score",
    "ugc_score",
    "influencer_dependency_score",
    "repeat_purchase_rate",
    "price_sensitivity_score",
    "premium_affinity_score",
    "trend_sensitivity_score",
    "community_engagement_score",
    "local_discovery_score",
    "education_content_affinity",
    "short_form_video_affinity",
    "search_intent_score",
    "conversion_readiness_score",
    "ingredient_awareness_score",
    "routine_complexity_score",

    "age_18_24_ratio",
    "age_25_34_ratio",
    "age_35_50_ratio",
    "age_50_plus_ratio",
    "female_ratio",
    "male_ratio",
    "income_low_ratio",
    "income_mid_ratio",
    "income_high_ratio",

    "avg_session_time_minutes",
    "foot_traffic_score",
    "population_density_score",
    "college_presence_score",
    "competition_density_score",
    "market_saturation_score",
    "demand_score",
    "trend_score",

    "repeat_customer_signal",
    "product_category_affinity",
    "niche_signal_score",
    "visual_content_signal",
    "transaction_conversion_signal",
    "platform_fit_score",
    "dense_slice_confidence",

    "niche_anchor_skincare",
    "niche_anchor_pet",
    "niche_anchor_streetwear",
    "niche_anchor_learning",
    "niche_anchor_home",
    "niche_anchor_organic",
    "niche_anchor_diy",
    "niche_anchor_gadget",
    "niche_anchor_gym",
    "niche_anchor_healthy",

    "platform_anchor_tiktok",
    "platform_anchor_reddit",
    "platform_anchor_instagram",
    "platform_anchor_pinterest",
    "platform_anchor_website_first",
    "platform_anchor_discord",
    "platform_anchor_youtube_shorts",
    "platform_anchor_micro_influencers",
    "platform_anchor_marketplace_first",
    "platform_anchor_facebook_groups",
]

CATEGORICAL_COLS = [
    "business_category",
    "price_range",
    "content_format",
    "purchase_frequency",
    "geography_signal",
    "data_source_coverage",
]


def main():
    df = pd.read_csv(INPUT_FILE)

    print("\nTarget dense slice distribution:")
    print(df["target_dense_slice"].value_counts())

    X = df[FEATURE_COLS].copy()
    y = df["target_dense_slice"].astype(str)

    X = pd.get_dummies(X, columns=CATEGORICAL_COLS)
    encoded_feature_columns = X.columns.tolist()

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y_encoded,
        test_size=0.2,
        random_state=42,
        stratify=y_encoded
    )

    sample_weights = compute_sample_weight(class_weight="balanced", y=y_train)

    model = LGBMClassifier(
        objective="multiclass",
        n_estimators=240,
        max_depth=5,
        num_leaves=24,
        learning_rate=0.05,
        min_child_samples=18,
        subsample=0.82,
        colsample_bytree=0.82,
        reg_alpha=0.8,
        reg_lambda=1.2,
        class_weight="balanced",
        random_state=42
    )

    model.fit(X_train, y_train, sample_weight=sample_weights)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\nTest Accuracy: {accuracy:.4f}")

    labels_present = np.unique(y_test)
    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            y_pred,
            labels=labels_present,
            target_names=label_encoder.inverse_transform(labels_present)
        )
    )

    os.makedirs("ml_models/artifacts", exist_ok=True)
    joblib.dump(model, MODEL_OUTPUT)
    joblib.dump(label_encoder, LABEL_ENCODER_OUTPUT)
    joblib.dump(
        {
            "feature_cols": FEATURE_COLS,
            "categorical_cols": CATEGORICAL_COLS,
            "encoded_feature_columns": encoded_feature_columns,
        },
        META_OUTPUT
    )

    print(f"\nModel saved to: {MODEL_OUTPUT}")
    print(f"Label encoder saved to: {LABEL_ENCODER_OUTPUT}")
    print(f"Meta saved to: {META_OUTPUT}")


if __name__ == "__main__":
    main()