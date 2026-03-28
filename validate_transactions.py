import pandas as pd

df = pd.read_csv("synthetic_data/generated/transactions.csv")

print("Total transactions:", len(df))

print("\nTransactions per vendor (sample):")
print(df.groupby("vendor_id").size().describe())

print("\nRepeat customer distribution:")
print(df["is_repeat_customer"].value_counts(normalize=True))

print("\nOrder value summary:")
print(df["order_value_usd"].describe())

print("\nPlatform distribution:")
print(df["platform"].value_counts().head())

print("\nGeography distribution:")
print(df["geography"].value_counts().head())