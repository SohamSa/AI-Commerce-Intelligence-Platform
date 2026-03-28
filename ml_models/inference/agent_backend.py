import pandas as pd

from ml_models.inference.decision_engine import run_decision_engine_by_vendor_id

from typing import Optional


FEATURE_STORE_FILE = "ml_models/feature_store/business_feature_store.csv"


def load_data():
    return pd.read_csv(FEATURE_STORE_FILE)


def answer_niche_question(question: str, df: pd.DataFrame) -> str:
    q = question.lower()

    if "repeat" in q:
        result = (
            df.groupby("target_micro_niche")["repeat_purchase_rate"]
            .mean()
            .sort_values(ascending=False)
            .round(3)
        )
        return f"Top niches for repeat purchases:\n{result.to_string()}"

    if "premium" in q:
        result = (
            df.groupby("target_micro_niche")["premium_affinity_score"]
            .mean()
            .sort_values(ascending=False)
            .round(3)
        )
        return f"Top niches for premium products:\n{result.to_string()}"

    if "vendor" in q:
        result = (
            df.groupby("target_micro_niche")["business_category"]
            .agg(lambda x: x.value_counts().index[0])
            .sort_index()
        )
        return f"Niche by vendor type:\n{result.to_string()}"

    return "I understood this as a niche question, but I do not yet have a rule for it."


def answer_platform_question(question: str, df: pd.DataFrame) -> str:
    q = question.lower()

    if "visual" in q:
        result = (
            df.groupby("target_platform")[["is_visual_product", "image_engagement_score", "video_consumption_score"]]
            .mean()
            .round(3)
        )
        return f"Platform patterns for visual products:\n{result.to_string()}"

    if "premium" in q:
        result = (
            df.groupby("target_platform")["premium_affinity_score"]
            .mean()
            .sort_values(ascending=False)
            .round(3)
        )
        return f"Top platforms for premium products:\n{result.to_string()}"

    if "community" in q:
        result = (
            df.groupby("target_platform")[["community_engagement_score", "ugc_score", "local_discovery_score"]]
            .mean()
            .round(3)
        )
        return f"Top community-led platforms:\n{result.to_string()}"

    return "I understood this as a platform question, but I do not yet have a rule for it."


def answer_dense_slice_question(question: str, df: pd.DataFrame) -> str:
    q = question.lower()

    if "repeat" in q:
        result = (
            df.groupby("target_dense_slice")["repeat_purchase_rate"]
            .mean()
            .sort_values(ascending=False)
            .round(3)
        )
        return f"Top dense slices for repeat buying:\n{result.to_string()}"

    if "premium" in q:
        result = (
            df.groupby("target_dense_slice")[["income_high_ratio", "premium_affinity_score", "price_sensitivity_score"]]
            .mean()
            .round(3)
        )
        return f"Premium-oriented dense slices:\n{result.to_string()}"

    if "young" in q or "age" in q:
        result = (
            df.groupby("target_dense_slice")[["age_18_24_ratio", "age_25_34_ratio", "age_35_50_ratio"]]
            .mean()
            .round(3)
        )
        return f"Age patterns by dense slice:\n{result.to_string()}"

    return "I understood this as a dense-slice question, but I do not yet have a rule for it."


def format_vendor_report(result: dict) -> str:
    return f"""
FINAL DECISION REPORT

Vendor ID: {result['vendor_id']}
Business Name: {result['business_name']}

Predicted Niche:
  {result['niche_prediction']['label']} -> {result['niche_prediction']['probability']}

Predicted Platform:
  {result['platform_prediction']['label']} -> {result['platform_prediction']['probability']}

Predicted Dense Slice:
  {result['dense_slice_prediction']['label']} -> {result['dense_slice_prediction']['probability']}

Recommended Combination:
  Niche: {result['recommended_combination']['niche']}
  Platform: {result['recommended_combination']['platform']}
  Dense Slice: {result['recommended_combination']['dense_slice']}

Business Recommendation:
  Stage: {result['business_recommendation']['business_stage']}
  Product Style: {result['business_recommendation']['product_style']}
  Niche Strategy: {result['business_recommendation']['niche_strategy']}
  Platform Strategy: {result['business_recommendation']['platform_strategy']}
  Dense Slice Strategy: {result['business_recommendation']['dense_slice_strategy']}
""".strip()


def route_question(question: str, vendor_id: Optional[str] = None) -> str:
    df = load_data()
    q = question.lower()

    if vendor_id is not None:
        result = run_decision_engine_by_vendor_id(vendor_id)
        if "decision" in q or "analyze" in q or "report" in q or "vendor" in q:
            return format_vendor_report(result)

        if "niche" in q:
            return (
                f"For vendor {vendor_id}, the predicted niche is "
                f"{result['niche_prediction']['label']} "
                f"with confidence {result['niche_prediction']['probability']}."
            )

        if "platform" in q:
            return (
                f"For vendor {vendor_id}, the predicted platform is "
                f"{result['platform_prediction']['label']} "
                f"with confidence {result['platform_prediction']['probability']}."
            )

        if "dense" in q or "audience" in q or "slice" in q:
            return (
                f"For vendor {vendor_id}, the predicted dense slice is "
                f"{result['dense_slice_prediction']['label']} "
                f"with confidence {result['dense_slice_prediction']['probability']}."
            )

    if "niche" in q:
        return answer_niche_question(question, df)

    if "platform" in q:
        return answer_platform_question(question, df)

    if "dense" in q or "slice" in q or "audience" in q:
        return answer_dense_slice_question(question, df)

    return (
        "I could not confidently route the question yet. "
        "Try asking about niche, platform, dense slice, or provide a vendor_id for a vendor-specific report."
    )


def main():
    print("AI Agent Backend")
    print("Type a question. You can also optionally enter a vendor_id first.")
    print()

    vendor_id = input("Enter vendor_id (or press Enter to skip): ").strip()
    if vendor_id == "":
        vendor_id = None

    question = input("Enter your question: ").strip()

    answer = route_question(question, vendor_id)
    print("\n" + "=" * 100)
    print(answer)
    print("=" * 100)


if __name__ == "__main__":
    main()