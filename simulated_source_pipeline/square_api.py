from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI(title="Simulated Square API")

DATA_FILE = "synthetic_data/generated/strong_ml_dataset.csv"

SQUARE_COLUMNS = [
    "vendor_id",
    "business_name",
    "purchase_frequency",
    "repeat_purchase_rate",
    "repeat_customer_signal",
    "transaction_conversion_signal",
    "community_engagement_score",
    "local_discovery_score",
    "demand_score",
    "avg_session_time_minutes",
    "price_sensitivity_score",
    "brand_loyalty_score",
    "income_low_ratio",
    "income_mid_ratio",
    "income_high_ratio",
]

df = pd.read_csv(DATA_FILE)
df["vendor_id"] = df["vendor_id"].astype(str)


@app.get("/")
def home():
    return {"message": "Simulated Square API is running"}


@app.get("/vendors")
def get_vendors(limit: int = 20):
    return df[SQUARE_COLUMNS].head(limit).to_dict(orient="records")


@app.get("/vendors/{vendor_id}")
def get_vendor(vendor_id: str):
    row = df[df["vendor_id"] == vendor_id]
    if row.empty:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return row[SQUARE_COLUMNS].iloc[0].to_dict()