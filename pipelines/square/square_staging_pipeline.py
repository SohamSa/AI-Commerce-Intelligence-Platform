import json
from datetime import datetime

import pandas as pd


# Load raw data
def load_square_raw_data(file_path):
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


# Convert binary repeat flag → signal
def convert_repeat_flag(flag):
    if flag is None:
        return None
    return 1.0 if flag == 1 else 0.0


# Main transformation
def transform_square_to_staging(raw_data):
    staging_data = []

    for record in raw_data:
        transformed = {
            "vendor_id": record.get("vendor_id"),
            "business_name": record.get("business_name"),
            "business_category": record.get("category"),
            "event_timestamp": record.get("transaction_created_at"),

            "repeat_customer_signal": record.get("repeat_customer_rate"),
            "product_category_affinity": (
                round(record.get("avg_ticket_size") / 100, 4)
                if record.get("avg_ticket_size") is not None else None
            ),
            
            "top_micro_niche_1": None,
            "top_micro_niche_2": None,
            "niche_signal_score": None,
            "visual_content_signal": None,
            "transaction_conversion_signal": 1 - record.get("risk_score") if record.get("risk_score") is not None else None,

            "recommended_platform_1": None,
            "recommended_platform_2": None,
            "platform_fit_score": None,

            "recommended_dense_slice_1": None,
            "recommended_dense_slice_2": None,
            "geography_signal": record.get("location_type"),
            "dense_slice_confidence": None,

            "data_source_coverage": "square_only"
        }

        staging_data.append(transformed)

    return staging_data


# Run pipeline
if __name__ == "__main__":
    file_path = "synthetic_data/generated/square_raw_data_large.csv"

    raw_data = load_square_raw_data(file_path)

    staging_output = transform_square_to_staging(raw_data)

    for row in staging_output:
        print(row)