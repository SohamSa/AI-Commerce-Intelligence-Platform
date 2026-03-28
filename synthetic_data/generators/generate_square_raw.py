import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

VENDOR_FILE = "synthetic_data/generated/vendor_master.csv"
TRANSACTION_FILE = "synthetic_data/generated/transactions.csv"
OUTPUT_FILE = "synthetic_data/generated/square_raw_data_large.csv"


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
            total_gmv = 0
            avg_ticket_size = 0
            txn_count = 0
            repeat_rate = 0
            refund_rate = 0
            payment_method_mix = "unknown"
        else:
            total_gmv = round(vendor_txns["order_value_usd"].sum(), 2)
            avg_ticket_size = round(vendor_txns["order_value_usd"].mean(), 2)
            txn_count = len(vendor_txns)
            repeat_rate = round(vendor_txns["is_repeat_customer"].mean(), 4)

            refund_rate = round(np.random.uniform(0.01, 0.08), 4)

            payment_method_mix = random.choice([
                "card_dominant",
                "mixed",
                "digital_wallet_heavy"
            ])

        revenue_volatility_score = round(np.random.uniform(0.2, 0.9), 4)
        weekend_sales_ratio = round(np.random.uniform(0.2, 0.7), 4)
        late_night_sales_ratio = round(np.random.uniform(0.05, 0.3), 4)

        location_type = random.choice([
            "mall",
            "standalone",
            "home_based",
            "pop_up"
        ])

        risk_score = round(
            0.5 * (1 - repeat_rate) +
            0.3 * refund_rate +
            0.2 * revenue_volatility_score,
            4
        )

        rows.append({
            "vendor_id": vendor_id,
            "business_name": vendor["business_name"],
            "category": vendor["business_category"],
            "location_type": location_type,

            "total_gmv": total_gmv,
            "avg_ticket_size": avg_ticket_size,
            "transaction_count": txn_count,
            "repeat_customer_rate": repeat_rate,
            "refund_rate_estimate": refund_rate,

            "payment_method_mix": payment_method_mix,

            "revenue_volatility_score": revenue_volatility_score,
            "weekend_sales_ratio": weekend_sales_ratio,
            "late_night_sales_ratio": late_night_sales_ratio,

            "risk_score": risk_score
        })

    square_df = pd.DataFrame(rows)
    square_df.to_csv(OUTPUT_FILE, index=False)

    print(f"Square raw generated: {OUTPUT_FILE}")
    print(f"Rows written: {len(square_df)}")
    print(f"Columns written: {len(square_df.columns)}")


if __name__ == "__main__":
    main()