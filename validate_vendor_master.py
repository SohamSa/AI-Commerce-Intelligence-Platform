import pandas as pd

df = pd.read_csv("synthetic_data/generated/vendor_master.csv")

print("Total rows:", len(df))

print("\nStrength distribution:")
print(df["strength_class"].value_counts())

print("\nTransaction tier distribution:")
print(df["transaction_tier"].value_counts())

print("\nSignal summary:")
print(df[[
    "niche_signal_score_base",
    "visual_content_signal_base",
    "transaction_conversion_signal_base",
    "platform_fit_score_base",
    "dense_slice_confidence_base"
]].describe())

print("\nCategory distribution:")
print(df["business_category"].value_counts())