import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

VENDOR_FILE = "synthetic_data/generated/vendor_master.csv"
TRANSACTION_FILE = "synthetic_data/generated/transactions.csv"
OUTPUT_FILE = "synthetic_data/generated/shopify_raw_data_large.csv"


def clamp(value, low=0.0, high=1.0):
    return max(low, min(high, value))


def add_noise(value, noise_level=0.05):
    noisy = value + np.random.uniform(-noise_level, noise_level)
    return round(clamp(noisy), 4)


def main():
    vendor_df = pd.read_csv(VENDOR_FILE)
    txn_df = pd.read_csv(TRANSACTION_FILE)

    txn_df["event_timestamp"] = pd.to_datetime(txn_df["event_timestamp"])

    grouped = txn_df.groupby("vendor_id")

    rows = []

    for _, vendor in vendor_df.iterrows():
        vendor_id = vendor["vendor_id"]
        vendor_txns = grouped.get_group(vendor_id) if vendor_id in grouped.groups else pd.DataFrame()

        if vendor_txns.empty:
            customer_repeat_rate = 0.0
            avg_order_value_estimate = 0.0
            monthly_revenue_estimate = 0.0
            returning_customer_revenue_ratio = 0.0
            geo_cluster_type = vendor["geography_signal"]
        else:
            customer_repeat_rate = round(vendor_txns["is_repeat_customer"].mean(), 4)
            avg_order_value_estimate = round(vendor_txns["order_value_usd"].mean(), 2)

            vendor_txns["month"] = vendor_txns["event_timestamp"].dt.to_period("M")
            monthly_totals = vendor_txns.groupby("month")["order_value_usd"].sum()
            monthly_revenue_estimate = round(monthly_totals.mean(), 2) if len(monthly_totals) > 0 else 0.0

            repeat_revenue = vendor_txns.loc[
                vendor_txns["is_repeat_customer"] == 1, "order_value_usd"
            ].sum()
            total_revenue = vendor_txns["order_value_usd"].sum()
            returning_customer_revenue_ratio = round(
                repeat_revenue / total_revenue, 4
            ) if total_revenue > 0 else 0.0

            geo_cluster_type = vendor_txns["geography"].mode().iloc[0]

        product_niche_fit_score = add_noise(vendor["niche_signal_score_base"], 0.04)
        niche_signal_raw = add_noise(vendor["niche_signal_score_base"], 0.04)
        visual_score = add_noise(vendor["visual_content_signal_base"], 0.05)
        conversion_efficiency_raw = add_noise(vendor["transaction_conversion_signal_base"], 0.04)
        platform_fit_raw = add_noise(vendor["platform_fit_score_base"], 0.04)
        dense_slice_confidence_raw = add_noise(vendor["dense_slice_confidence_base"], 0.04)

        engagement_to_conversion_ratio = round(
            visual_score / max(conversion_efficiency_raw, 0.05), 2
        )
        content_consistency_score = add_noise(vendor["visual_content_signal_base"], 0.06)
        platform_dependency_score = add_noise(vendor["platform_fit_score_base"], 0.08)
        product_category_depth_score = add_noise(vendor["niche_signal_score_base"], 0.07)

        rows.append({
            "vendor_id": vendor_id,
            "shop_name": vendor["business_name"],
            "primary_category": vendor["business_category"],
            "created_at": "2023-01-01 00:00:00",
            "customer_repeat_rate": customer_repeat_rate,
            "product_niche_fit_score": product_niche_fit_score,
            "predicted_micro_niche_1": vendor["top_micro_niche_1"],
            "predicted_micro_niche_2": vendor["top_micro_niche_2"],
            "niche_signal_raw": niche_signal_raw,
            "visual_score": visual_score,
            "conversion_efficiency_raw": conversion_efficiency_raw,
            "engagement_to_conversion_ratio": engagement_to_conversion_ratio,
            "content_consistency_score": content_consistency_score,
            "primary_platform_prediction": vendor["recommended_platform_1"],
            "secondary_platform_prediction": vendor["recommended_platform_2"],
            "platform_fit_raw": platform_fit_raw,
            "platform_dependency_score": platform_dependency_score,
            "dense_slice_prediction_1": vendor["recommended_dense_slice_1"],
            "dense_slice_prediction_2": vendor.get("recommended_dense_slice_2", None),
            "geo_cluster_type": geo_cluster_type,
            "dense_slice_confidence_raw": dense_slice_confidence_raw,
            "avg_order_value_estimate": avg_order_value_estimate,
            "monthly_revenue_estimate": monthly_revenue_estimate,
            "returning_customer_revenue_ratio": returning_customer_revenue_ratio,
            "product_category_depth_score": product_category_depth_score
        })

    shopify_df = pd.DataFrame(rows)
    shopify_df.to_csv(OUTPUT_FILE, index=False)

    print(f"Shopify raw generated: {OUTPUT_FILE}")
    print(f"Rows written: {len(shopify_df)}")
    print(f"Columns written: {len(shopify_df.columns)}")


if __name__ == "__main__":
    main()