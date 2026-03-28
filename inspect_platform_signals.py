import pandas as pd

INPUT_FILE = "ml_models/feature_store/business_feature_store.csv"

df = pd.read_csv(INPUT_FILE)

print("\nPlatform distribution:")
print(df["target_platform"].value_counts())

signal_cols = [
    "short_form_video_affinity",
    "image_engagement_score",
    "text_engagement_score",
    "video_consumption_score",
    "education_content_affinity",
    "trend_sensitivity_score",
    "community_engagement_score",
    "local_discovery_score",
    "search_intent_score",
    "platform_fit_score",
]

print("\nMean feature values by platform:")
print(df.groupby("target_platform")[signal_cols].mean().round(3))