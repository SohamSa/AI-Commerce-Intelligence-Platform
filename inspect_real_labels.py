import pandas as pd

df = pd.read_csv("synthetic_data/generated/final_dataset.csv")

print("\nCOLUMNS:\n")
print(df.columns.tolist())

for col in df.columns:
    print(f"\n--- {col} ---")
    print(df[col].dropna().astype(str).value_counts().head(20))