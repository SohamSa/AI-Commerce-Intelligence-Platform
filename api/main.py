from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

from database.connection import engine
from database.models import Business

from database.models import AudienceSegment

from pipelines.shopify.shopify_staging_pipeline import load_shopify_raw_data, transform_shopify_to_staging
from pipelines.square.square_staging_pipeline import load_square_raw_data, transform_square_to_staging
from pipelines.canonical.merge_pipeline import merge_datasets

from fastapi.responses import JSONResponse
import pandas as pd

app = FastAPI()

SessionLocal = sessionmaker(bind=engine)


class BusinessCreate(BaseModel):
    name: str
    category: str
    stage: str


@app.get("/")
def home():
    return {"message": "API is working 🚀"}


@app.get("/businesses")
def get_businesses():
    session = SessionLocal()

    businesses = session.query(Business).all()

    result = []
    for business in businesses:
        result.append({
            "id": business.id,
            "name": business.name,
            "category": business.category,
            "stage": business.stage
        })

    session.close()
    return result


@app.post("/businesses")
def create_business(business: BusinessCreate):
    session = SessionLocal()

    new_business = Business(
        name=business.name,
        category=business.category,
        stage=business.stage
    )

    session.add(new_business)
    session.commit()
    session.refresh(new_business)
    session.close()

    return {
        "id": new_business.id,
        "name": new_business.name,
        "category": new_business.category,
        "stage": new_business.stage
    }


@app.put("/businesses/{business_id}")
def update_business(business_id: int, business: BusinessCreate):
    session = SessionLocal()

    existing_business = session.query(Business).filter(Business.id == business_id).first()

    if not existing_business:
        session.close()
        raise HTTPException(status_code=404, detail="Business not found")

    existing_business.name = business.name
    existing_business.category = business.category
    existing_business.stage = business.stage

    session.commit()
    session.close()

    return {"message": "Business updated successfully"}


@app.delete("/businesses/{business_id}")
def delete_business(business_id: int):
    session = SessionLocal()

    existing_business = session.query(Business).filter(Business.id == business_id).first()

    if not existing_business:
        session.close()
        raise HTTPException(status_code=404, detail="Business not found")

    session.delete(existing_business)
    session.commit()
    session.close()

    return {"message": "Business deleted successfully"}

from database.models import Platform
from database.connection import engine
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(bind=engine)


@app.get("/business-insights")
def get_business_insights(
    category: str = None,
    platform: str = None,
    geo: str = None,
    top_n: int = 10
):
    df = pd.read_csv("synthetic_data/generated/final_dataset.csv")

    final_data = df.to_dict(orient="records")

    for row in final_data:
        repeat_customer_signal = row.get("repeat_customer_signal") or 0
        niche_signal_score = row.get("niche_signal_score") or 0
        visual_content_signal = row.get("visual_content_signal") or 0
        transaction_conversion_signal = row.get("transaction_conversion_signal") or 0
        platform_fit_score = row.get("platform_fit_score") or 0
        dense_slice_confidence = row.get("dense_slice_confidence") or 0
        product_category_affinity = row.get("product_category_affinity") or 0

        row["success_score"] = round(
            0.22 * niche_signal_score
            + 0.18 * platform_fit_score
            + 0.18 * transaction_conversion_signal
            + 0.16 * repeat_customer_signal
            + 0.10 * dense_slice_confidence
            + 0.08 * visual_content_signal
            + 0.08 * product_category_affinity,
            3
        )
        

        if row["success_score"] >= 0.70:
            strength = "strong"
        elif row["success_score"] >= 0.50:
            strength = "moderate"
        else:
            strength = "emerging"

        row["insight"] = (
            f"{row['business_name']} shows a {strength} success profile driven by "
            f"{row.get('top_micro_niche_1', 'unknown niche')}, strong fit on "
            f"{row.get('recommended_platform_1', 'unknown platform')}, and traction in "
            f"{row.get('recommended_dense_slice_1', 'unknown segment')}."
        )

        row["action"] = (
            f"Prioritize {row.get('recommended_platform_1', 'unknown platform')} for "
            f"{row.get('recommended_dense_slice_1', 'unknown segment')}, and position the offer around "
            f"{row.get('top_micro_niche_1', 'unknown niche')}."
        )

    final_data = sorted(
        final_data,
        key=lambda x: x["success_score"],
        reverse=True
    )

    if category:
        final_data = [
            x for x in final_data
            if x.get("business_category") == category
        ]

    if platform:
        final_data = [
            x for x in final_data
            if x.get("recommended_platform_1") == platform
            or x.get("recommended_platform_2") == platform
        ]

    if geo:
        final_data = [
            x for x in final_data
            if x.get("geography_signal") == geo
        ]

    final_data = final_data[:top_n]

    return JSONResponse(content=final_data, headers={"Content-Type": "application/json"})

@app.get("/top-opportunities")
def get_top_opportunities(
    category: str = None,
    platform: str = None,
    geo: str = None,
    top_n: int = 10
):
    df = pd.read_csv("synthetic_data/generated/final_dataset.csv")
    final_data = df.to_dict(orient="records")

    for row in final_data:
        repeat_customer_signal = row.get("repeat_customer_signal") or 0
        niche_signal_score = row.get("niche_signal_score") or 0
        visual_content_signal = row.get("visual_content_signal") or 0
        transaction_conversion_signal = row.get("transaction_conversion_signal") or 0
        platform_fit_score = row.get("platform_fit_score") or 0
        dense_slice_confidence = row.get("dense_slice_confidence") or 0
        product_category_affinity = row.get("product_category_affinity") or 0

        row["success_score"] = round(
            0.22 * niche_signal_score +
            0.18 * platform_fit_score +
            0.18 * transaction_conversion_signal +
            0.16 * repeat_customer_signal +
            0.10 * dense_slice_confidence +
            0.08 * visual_content_signal +
            0.08 * product_category_affinity,
            3
        )

        score_breakdown = {
            "niche_signal": round(0.22 * niche_signal_score, 3),
            "platform_fit": round(0.18 * platform_fit_score, 3),
            "conversion": round(0.18 * transaction_conversion_signal, 3),
            "repeat_customer": round(0.16 * repeat_customer_signal, 3),
            "dense_slice": round(0.10 * dense_slice_confidence, 3),
            "visual_content": round(0.08 * visual_content_signal, 3),
            "product_affinity": round(0.08 * product_category_affinity, 3)
        }

        row["score_breakdown"] = score_breakdown
        
        if row["success_score"] >= 0.70:
            strength = "strong"
        elif row["success_score"] >= 0.50:
            strength = "moderate"
        else:
            strength = "emerging"

        row["insight"] = (
            f"{row['business_name']} shows a {strength} success profile driven by "
            f"{row.get('top_micro_niche_1', 'unknown niche')}, strong fit on "
            f"{row.get('recommended_platform_1', 'unknown platform')}, and traction in "
            f"{row.get('recommended_dense_slice_1', 'unknown segment')}."
        )

        row["action"] = (
            f"Prioritize {row.get('recommended_platform_1', 'unknown platform')} for "
            f"{row.get('recommended_dense_slice_1', 'unknown segment')}, and position the offer around "
            f"{row.get('top_micro_niche_1', 'unknown niche')}."
        )

    if category:
        final_data = [x for x in final_data if x.get("business_category") == category]

    if platform:
        final_data = [
            x for x in final_data
            if x.get("recommended_platform_1") == platform or x.get("recommended_platform_2") == platform
        ]

    if geo:
        final_data = [x for x in final_data if x.get("geography_signal") == geo]

    final_data = sorted(final_data, key=lambda x: x["success_score"], reverse=True)
    final_data = final_data[:top_n]

    cleaned_output = []
    for row in final_data:
        cleaned_output.append({
            "vendor_id": row.get("vendor_id"),
            "business_name": row.get("business_name"),
            "business_category": row.get("business_category"),
            "success_score": row.get("success_score"),
            "score_breakdown": row.get("score_breakdown"),   # 👈 ADD THIS
            "recommended_platform_1": row.get("recommended_platform_1"),
            "recommended_dense_slice_1": row.get("recommended_dense_slice_1"),
            "insight": row.get("insight"),
            "action": row.get("action")
        })

    return JSONResponse(content=cleaned_output, headers={"Content-Type": "application/json"})