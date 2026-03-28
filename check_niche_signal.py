import pandas as pd
import os

# 🔥 THIS LINE FIXES EVERYTHING
BASE_DIR = os.getcwd()   # current project folder

OUTPUT_DIR = os.path.join(BASE_DIR, "analysis_outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

INPUT_FILE = os.path.join(BASE_DIR, "ml_models", "feature_store", "business_feature_store.csv")

df = pd.read_csv(INPUT_FILE)

# 1. Distribution
dist = df["target_micro_niche"].value_counts().reset_index()
dist.columns = ["micro_niche", "count"]
dist.to_csv(os.path.join(OUTPUT_DIR, "niche_distribution.csv"), index=False)

# 2. Crosstabs
pd.crosstab(df["target_micro_niche"], df["top_micro_niche_2"])\
    .to_csv(os.path.join(OUTPUT_DIR, "niche_vs_niche2.csv"))

pd.crosstab(df["target_micro_niche"], df["business_category"])\
    .to_csv(os.path.join(OUTPUT_DIR, "niche_vs_category.csv"))

pd.crosstab(df["target_micro_niche"], df["recommended_platform_1"])\
    .to_csv(os.path.join(OUTPUT_DIR, "niche_vs_platform.csv"))

pd.crosstab(df["target_micro_niche"], df["recommended_dense_slice_1"])\
    .to_csv(os.path.join(OUTPUT_DIR, "niche_vs_dense_slice.csv"))

print("\nFILES SAVED HERE:")
print(OUTPUT_DIR)