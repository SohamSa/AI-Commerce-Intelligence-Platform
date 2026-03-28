from pipelines.shopify.shopify_staging_pipeline import transform_shopify_to_staging, load_shopify_raw_data
from pipelines.square.square_staging_pipeline import transform_square_to_staging, load_square_raw_data

import pandas as pd


def merge_records(shopify_rec, square_rec):
    return {
        "vendor_id": shopify_rec.get("vendor_id") or square_rec.get("vendor_id"),
        "business_name": shopify_rec.get("business_name") or square_rec.get("business_name"),
        "business_category": shopify_rec.get("business_category") or square_rec.get("business_category"),
        "event_timestamp": shopify_rec.get("event_timestamp") or square_rec.get("event_timestamp"),

        "repeat_customer_signal": (
            (shopify_rec.get("repeat_customer_signal") + square_rec.get("repeat_customer_signal")) / 2
            if shopify_rec.get("repeat_customer_signal") is not None and square_rec.get("repeat_customer_signal") is not None
            else shopify_rec.get("repeat_customer_signal") or square_rec.get("repeat_customer_signal")
        ),

        "product_category_affinity": (
            (shopify_rec.get("product_category_affinity") + square_rec.get("product_category_affinity")) / 2
            if shopify_rec.get("product_category_affinity") is not None and square_rec.get("product_category_affinity") is not None
            else shopify_rec.get("product_category_affinity") or square_rec.get("product_category_affinity")
        ),

        "top_micro_niche_1": shopify_rec.get("top_micro_niche_1") or square_rec.get("top_micro_niche_1"),
        "top_micro_niche_2": shopify_rec.get("top_micro_niche_2") or square_rec.get("top_micro_niche_2"),
        "niche_signal_score": shopify_rec.get("niche_signal_score") or square_rec.get("niche_signal_score"),
        "visual_content_signal": shopify_rec.get("visual_content_signal") or square_rec.get("visual_content_signal"),

        "transaction_conversion_signal": (
            (shopify_rec.get("transaction_conversion_signal") + square_rec.get("transaction_conversion_signal")) / 2
            if shopify_rec.get("transaction_conversion_signal") is not None and square_rec.get("transaction_conversion_signal") is not None
            else shopify_rec.get("transaction_conversion_signal") or square_rec.get("transaction_conversion_signal")
        ),

        "recommended_platform_1": shopify_rec.get("recommended_platform_1") or square_rec.get("recommended_platform_1"),
        "recommended_platform_2": shopify_rec.get("recommended_platform_2") or square_rec.get("recommended_platform_2"),
        "platform_fit_score": shopify_rec.get("platform_fit_score") or square_rec.get("platform_fit_score"),
        "recommended_dense_slice_1": shopify_rec.get("recommended_dense_slice_1") or square_rec.get("recommended_dense_slice_1"),
        "recommended_dense_slice_2": shopify_rec.get("recommended_dense_slice_2") or square_rec.get("recommended_dense_slice_2"),
        "geography_signal": shopify_rec.get("geography_signal") or square_rec.get("geography_signal"),
        "dense_slice_confidence": shopify_rec.get("dense_slice_confidence") or square_rec.get("dense_slice_confidence"),

        "data_source_coverage": "shopify_and_square"
    }


def merge_datasets(shopify_data, square_data):
    shopify_map = {row["vendor_id"]: row for row in shopify_data if row.get("vendor_id") is not None}
    square_map = {row["vendor_id"]: row for row in square_data if row.get("vendor_id") is not None}

    all_vendor_ids = set(shopify_map.keys()) | set(square_map.keys())
    merged = []

    for vendor_id in all_vendor_ids:
        shopify_rec = shopify_map.get(vendor_id)
        square_rec = square_map.get(vendor_id)

        if shopify_rec and square_rec:
            merged.append(merge_records(shopify_rec, square_rec))
        elif shopify_rec:
            shopify_rec["data_source_coverage"] = "shopify_only"
            merged.append(shopify_rec)
        elif square_rec:
            square_rec["data_source_coverage"] = "square_only"
            merged.append(square_rec)

    return merged

def load_shopify_raw_data(file_path):
    df = pd.read_csv(file_path)
    return df.to_dict(orient="records")

def load_square_raw_data(file_path):
    df = pd.read_csv(file_path)
    return df.to_dict(orient="records")

if __name__ == "__main__":
    shopify_raw = load_shopify_raw_data("synthetic_data/generated/shopify_raw_data_large.csv")
    square_raw = load_square_raw_data("synthetic_data/generated/square_raw_data_large.csv")

    shopify_staging = transform_shopify_to_staging(shopify_raw)
    square_staging = transform_square_to_staging(square_raw)

    final_data = merge_datasets(shopify_staging, square_staging)

    import pandas as pd
    final_df = pd.DataFrame(final_data)

    output_path = "synthetic_data/generated/final_dataset.csv"
    final_df.to_csv(output_path, index=False)

    print(f"Final dataset saved to: {output_path}")
    print(f"Rows written: {len(final_df)}")
    print(f"Columns written: {len(final_df.columns)}")