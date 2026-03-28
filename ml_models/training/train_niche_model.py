import os
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_sample_weight
from xgboost import XGBClassifier

INPUT_FILE = "ml_models/feature_store/business_feature_store.csv"
MODEL_OUTPUT = "ml_models/artifacts/niche_model.pkl"
LABEL_ENCODER_OUTPUT = "ml_models/artifacts/niche_label_encoder.pkl"
META_OUTPUT = "ml_models/artifacts/niche_meta.pkl"

FEATURE_COLS = [
    "business_category",
    "price_range",
    "content_format",
    "purchase_frequency",
    "geography_signal",
    "data_source_coverage",
    "top_micro_niche_2",
    "recommended_platform_2",
    "recommended_dense_slice_2",
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
    "niche_intent_strength",
    "youth_alignment",
    "premium_vs_budget_signal"
]

CATEGORICAL_COLS = [
    "business_category",
    "price_range",
    "content_format",
    "purchase_frequency",
    "geography_signal",
    "data_source_coverage",
    "top_micro_niche_2",
    "recommended_platform_2",
    "recommended_dense_slice_2",
]


def main():
    df = pd.read_csv(INPUT_FILE)

    print("\nTarget micro niche distribution:")
    print(df["target_micro_niche"].value_counts())

    X = df[FEATURE_COLS].copy()
    y = df["target_micro_niche"].astype(str)

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

    model = XGBClassifier(
        objective="multi:softprob",
        num_class=len(label_encoder.classes_),
        n_estimators=180,
        max_depth=4,
        learning_rate=0.06,
        subsample=0.75,
        colsample_bytree=0.75,
        reg_alpha=1.0,
        reg_lambda=2.0,
        min_child_weight=5,
        gamma=0.3,
        random_state=42,
        eval_metric="mlogloss"
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