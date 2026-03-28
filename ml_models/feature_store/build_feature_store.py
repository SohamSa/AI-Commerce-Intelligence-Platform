import os
import pandas as pd

INPUT_FILE = "synthetic_data/generated/strong_ml_dataset.csv"
OUTPUT_FILE = "ml_models/feature_store/business_feature_store.csv"


def main():
    df = pd.read_csv(INPUT_FILE).copy()

    numeric_cols = [
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
        "platform_anchor_tiktok",
        "platform_anchor_reddit",
        "platform_anchor_instagram",
        "platform_anchor_pinterest",
        "platform_anchor_website_first",
        "platform_anchor_discord",
        "platform_anchor_youtube_shorts",
        "platform_anchor_micro_influencers",
        "platform_anchor_marketplace_first",
        "platform_anchor_facebook_groups"
        
    ]

    categorical_cols = [
        "business_name",
        "business_category",
        "price_range",
        "content_format",
        "purchase_frequency",
        "geography_signal",
        "data_source_coverage",
        "top_micro_niche_1",
        "top_micro_niche_2",
        "recommended_platform_1",
        "recommended_platform_2",
        "recommended_dense_slice_1",
        "recommended_dense_slice_2",
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

    for col in categorical_cols:
        df[col] = df[col].fillna("Unknown").astype(str)

    df["success_score"] = (
        0.18 * df["niche_signal_score"]
        + 0.16 * df["platform_fit_score"]
        + 0.16 * df["transaction_conversion_signal"]
        + 0.14 * df["repeat_customer_signal"]
        + 0.10 * df["dense_slice_confidence"]
        + 0.08 * df["visual_content_signal"]
        + 0.08 * df["product_category_affinity"]
        + 0.10 * df["conversion_readiness_score"]
    )

    df["engagement_score"] = (
        0.20 * df["video_consumption_score"]
        + 0.20 * df["image_engagement_score"]
        + 0.15 * df["text_engagement_score"]
        + 0.15 * df["ugc_score"]
        + 0.15 * df["community_engagement_score"]
        + 0.15 * (df["avg_session_time_minutes"] / 12.0)
    )

    df["conversion_strength"] = (
        0.45 * df["transaction_conversion_signal"]
        + 0.35 * df["conversion_readiness_score"]
        + 0.20 * df["product_category_affinity"]
    )

    df["visual_strength"] = (
        0.40 * df["visual_content_signal"]
        + 0.35 * df["image_engagement_score"]
        + 0.25 * df["video_consumption_score"]
    )

    df["platform_readiness"] = (
        0.40 * df["platform_fit_score"]
        + 0.30 * df["engagement_score"]
        + 0.30 * df["conversion_strength"]
    )

    df["locality_strength"] = (
        0.30 * df["dense_slice_confidence"]
        + 0.25 * df["foot_traffic_score"]
        + 0.20 * df["population_density_score"]
        + 0.15 * df["local_discovery_score"]
        + 0.10 * df["college_presence_score"]
    )

    df["niche_platform_alignment"] = (
        df["niche_signal_score"] + df["platform_fit_score"]
    ) / 2.0

    df["behavioral_momentum"] = (
        df["repeat_customer_signal"]
        + df["transaction_conversion_signal"]
        + df["trend_score"]
        + df["demand_score"]
    ) / 4.0

    df["visual_conversion_balance"] = (
        df["visual_content_signal"] + df["transaction_conversion_signal"]
    ) / 2.0

    df["community_readiness"] = (
        df["community_engagement_score"]
        + df["repeat_purchase_rate"]
        + df["dense_slice_confidence"]
    ) / 3.0

    df["niche_dense_alignment"] = (
        df["niche_signal_score"] + df["dense_slice_confidence"]
    ) / 2.0

    df["product_visual_fit"] = (
        df["product_category_affinity"] + df["visual_content_signal"]
    ) / 2.0

    df["conversion_repeat_alignment"] = (
        df["transaction_conversion_signal"] + df["repeat_customer_signal"]
    ) / 2.0
    
    df["niche_intent_strength"] = (
        0.6 * df["niche_signal_score"]
        + 0.4 * df["product_category_affinity"]
    )

    df["youth_alignment"] = (
        0.5 * df["age_18_24_ratio"]
        + 0.5 * df["age_25_34_ratio"]
    )

    df["premium_vs_budget_signal"] = (
        df["premium_affinity_score"] - df["price_sensitivity_score"]
    )
    

    df["target_micro_niche"] = df["top_micro_niche_1"]
    df["target_platform"] = df["recommended_platform_1"]
    df["target_dense_slice"] = df["recommended_dense_slice_1"]

    final_columns = [
        "vendor_id",
        "business_name",
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
        "success_score",
        "engagement_score",
        "conversion_strength",
        "visual_strength",
        "platform_readiness",
        "locality_strength",
        "niche_platform_alignment",
        "behavioral_momentum",
        "visual_conversion_balance",
        "community_readiness",
        "niche_dense_alignment",
        "product_visual_fit",
        "conversion_repeat_alignment",
        "target_micro_niche",
        "target_platform",
        "target_dense_slice",
        "niche_intent_strength",
        "youth_alignment",
        "premium_vs_budget_signal",
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
        "niche_anchor_skincare",
        "niche_anchor_pet",
        "niche_anchor_streetwear",
        "niche_anchor_learning",
        "niche_anchor_home",
        "niche_anchor_organic",
        "niche_anchor_diy",
        "niche_anchor_gadget",
        "niche_anchor_gym",
        "niche_anchor_healthy"
        
    ]

    feature_store_df = df[final_columns].copy()

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    feature_store_df.to_csv(OUTPUT_FILE, index=False)

    print("Feature store created successfully")
    print("\nTarget micro niche distribution:")
    print(feature_store_df["target_micro_niche"].value_counts())
    print("\nTarget platform distribution:")
    print(feature_store_df["target_platform"].value_counts())
    print("\nTarget dense slice distribution:")
    print(feature_store_df["target_dense_slice"].value_counts())
    print(f"\nSaved to: {OUTPUT_FILE}")
    print(f"Rows: {len(feature_store_df)}")
    print(f"Columns: {len(feature_store_df.columns)}")


if __name__ == "__main__":
    main()