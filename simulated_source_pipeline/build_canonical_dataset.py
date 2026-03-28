import os
import pandas as pd

INPUT_FILE = "synthetic_data/generated/strong_ml_dataset.csv"
OUTPUT_FILE = "simulated_source_pipeline/canonical_merged_dataset.csv"

SHOPIFY_COLUMNS = [
    "vendor_id",
    "business_name",
    "business_category",
    "price_range",
    "content_format",
    "is_visual_product",
    "image_engagement_score",
    "short_form_video_affinity",
    "premium_affinity_score",
    "trend_sensitivity_score",
    "search_intent_score",
    "conversion_readiness_score",
    "ingredient_awareness_score",
    "routine_complexity_score",
]

SQUARE_COLUMNS = [
    "vendor_id",
    "purchase_frequency",
    "repeat_purchase_rate",
    "repeat_customer_signal",
    "transaction_conversion_signal",
    "community_engagement_score",
    "local_discovery_score",
    "demand_score",
    "avg_session_time_minutes",
    "price_sensitivity_score",
    "brand_loyalty_score",
    "income_low_ratio",
    "income_mid_ratio",
    "income_high_ratio",
]

CANONICAL_EXTRA_COLUMNS = [
    "age_18_24_ratio",
    "age_25_34_ratio",
    "age_35_50_ratio",
    "age_50_plus_ratio",
    "female_ratio",
    "male_ratio",
    "video_consumption_score",
    "text_engagement_score",
    "ugc_score",
    "influencer_dependency_score",
    "research_time_score",
    "education_content_affinity",
    "platform_fit_score",
    "dense_slice_confidence",
    "niche_signal_score",
    "visual_content_signal",
    "product_category_affinity"
]

def main():
    df = pd.read_csv(INPUT_FILE)
    print(df.columns.tolist())
    df["vendor_id"] = df["vendor_id"].astype(str)

    shopify_df = df[SHOPIFY_COLUMNS].copy()
    square_df = df[SQUARE_COLUMNS].copy()
    extra_df = df[["vendor_id"] + CANONICAL_EXTRA_COLUMNS].copy()

    canonical_df = (
        shopify_df
        .merge(square_df, on="vendor_id", how="inner")
        .merge(extra_df, on="vendor_id", how="inner")
    )

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    canonical_df.to_csv(OUTPUT_FILE, index=False)

    print(f"Canonical dataset saved to: {OUTPUT_FILE}")
    print(f"Rows: {len(canonical_df)}")
    print(f"Columns: {len(canonical_df.columns)}")

if __name__ == "__main__":
    main()