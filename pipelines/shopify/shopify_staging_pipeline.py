import json
from datetime import datetime

import pandas as pd


# Load raw data
def load_shopify_raw_data(file_path):
    df = pd.read_csv(file_path)
    return df.to_dict(orient="records")


# Normalize datetime
def parse_datetime(dt_str):
    if dt_str:
        return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    return None


# Normalize score (0-1)
def normalize_score(value):
    if value is None:
        return None
    return max(0.0, min(1.0, float(value)))


# Main transformation
def transform_shopify_to_staging(raw_data):
    staging_data = []

    for record in raw_data:
        transformed = {
            "vendor_id": record.get("vendor_id"),
            
            "business_name": record.get("shop_name"),

            "business_category": record.get("primary_category"),

            "event_timestamp": parse_datetime(record.get("created_at")),

            "repeat_customer_signal": normalize_score(record.get("customer_repeat_rate")),

            "product_category_affinity": normalize_score(record.get("product_niche_fit_score")),

            "top_micro_niche_1": record.get("predicted_micro_niche_1"),

            "top_micro_niche_2": record.get("predicted_micro_niche_2"),

            "niche_signal_score": normalize_score(record.get("niche_signal_raw")),

            "visual_content_signal": normalize_score(record.get("visual_score")),

            "transaction_conversion_signal": normalize_score(record.get("conversion_efficiency_raw")),

            "recommended_platform_1": record.get("primary_platform_prediction"),

            "recommended_platform_2": record.get("secondary_platform_prediction"),

            "platform_fit_score": normalize_score(record.get("platform_fit_raw")),

            "recommended_dense_slice_1": record.get("dense_slice_prediction_1"),

            "recommended_dense_slice_2": record.get("dense_slice_prediction_2"),

            "geography_signal": record.get("geo_cluster_type"),

            "dense_slice_confidence": normalize_score(record.get("dense_slice_confidence_raw")),

            "data_source_coverage": "shopify_only"
        }

        staging_data.append(transformed)

    return staging_data


# Run pipeline
if __name__ == "__main__":
    file_path = "synthetic_data/generated/shopify_raw_data_large.csv"

    raw_data = load_shopify_raw_data(file_path)

    staging_output = transform_shopify_to_staging(raw_data)

    for row in staging_output:
        print(row)