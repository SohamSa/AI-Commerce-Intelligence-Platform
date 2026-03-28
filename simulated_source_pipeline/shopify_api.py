from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI(title="Simulated Shopify API")

DATA_FILE = "synthetic_data/generated/strong_ml_dataset.csv"

SHOPIFY_COLUMNS = [
    "vendor_id",
    "business_name",
    "business_category",
    "price_range",
    "content_format",
    "is_visual_product",
    "image_engagement_score",
    "short_form_video_affinity",
    "premium_affinity_score",
    "trend_sensitivity_score",
    "search_intent_score",
    "conversion_readiness_score",
    "ingredient_awareness_score",
    "routine_complexity_score",
]

df = pd.read_csv(DATA_FILE)
df["vendor_id"] = df["vendor_id"].astype(str)


@app.get("/")
def home():
    return {"message": "Simulated Shopify API is running"}


@app.get("/vendors")
def get_vendors(limit: int = 20):
    return df[SHOPIFY_COLUMNS].head(limit).to_dict(orient="records")


@app.get("/vendors/{vendor_id}")
def get_vendor(vendor_id: str):
    row = df[df["vendor_id"] == vendor_id]
    if row.empty:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return row[SHOPIFY_COLUMNS].iloc[0].to_dict()