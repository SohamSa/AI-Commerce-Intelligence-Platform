import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
np.random.seed(42)
random.seed(42)

# Load vendor master
vendor_df = pd.read_csv("synthetic_data/generated/vendor_master.csv")

transactions = []

# Transaction count per tier
tier_transaction_map = {
    "high": (180, 300),
    "medium_high": (120, 200),
    "medium": (80, 140),
    "low": (30, 80)
}

start_date = datetime(2023, 1, 1)

for _, row in vendor_df.iterrows():
    vendor_id = row["vendor_id"]
    tier = row["transaction_tier"]

    min_txn, max_txn = tier_transaction_map[tier]
    num_transactions = np.random.randint(min_txn, max_txn)

    # simulate customers per vendor
    customer_pool_size = int(num_transactions * 0.6)

    customers = [f"CUST_{vendor_id}_{i}" for i in range(customer_pool_size)]

    repeat_probability = row["niche_signal_score_base"]

    for _ in range(num_transactions):
        customer_id = random.choice(customers)

        is_repeat = np.random.rand() < repeat_probability

        # order value based on strength
        if row["strength_class"] == "A":
            order_value = np.random.uniform(40, 120)
        elif row["strength_class"] == "B":
            order_value = np.random.uniform(25, 90)
        elif row["strength_class"] == "C":
            order_value = np.random.uniform(15, 60)
        else:
            order_value = np.random.uniform(8, 40)

        timestamp = start_date + timedelta(days=random.randint(0, 365))

        transactions.append({
            "transaction_id": f"TXN_{vendor_id}_{random.randint(100000,999999)}",
            "vendor_id": vendor_id,
            "customer_id": customer_id,
            "order_value_usd": round(order_value, 2),
            "event_timestamp": timestamp,
            "platform": row["recommended_platform_1"],
            "dense_slice": row["recommended_dense_slice_1"],
            "geography": row["geography_signal"],
            "is_repeat_customer": int(is_repeat)
        })

df_txn = pd.DataFrame(transactions)

output_path = "synthetic_data/generated/transactions.csv"
df_txn.to_csv(output_path, index=False)

print(f"Transactions generated: {len(df_txn)} rows")