import streamlit as st
import pandas as pd
import joblib

from ml_models.inference.execution_agent import build_execution_plan

FEATURE_STORE_FILE = "ml_models/feature_store/business_feature_store.csv"

NICHE_MODEL_PATH = "ml_models/artifacts/niche_model.pkl"
NICHE_LABEL_ENCODER_PATH = "ml_models/artifacts/niche_label_encoder.pkl"
NICHE_META_PATH = "ml_models/artifacts/niche_meta.pkl"

PLATFORM_MODEL_PATH = "ml_models/artifacts/platform_model.pkl"
PLATFORM_LABEL_ENCODER_PATH = "ml_models/artifacts/platform_label_encoder.pkl"
PLATFORM_META_PATH = "ml_models/artifacts/platform_meta.pkl"

DENSE_MODEL_PATH = "ml_models/artifacts/dense_slice_model.pkl"
DENSE_LABEL_ENCODER_PATH = "ml_models/artifacts/dense_slice_label_encoder.pkl"
DENSE_META_PATH = "ml_models/artifacts/dense_slice_meta.pkl"


@st.cache_data
def load_feature_store():
    df = pd.read_csv(FEATURE_STORE_FILE)
    df["vendor_id"] = df["vendor_id"].astype(str)
    return df


@st.cache_resource
def load_model_bundle(model_path, label_encoder_path, meta_path):
    model = joblib.load(model_path)
    label_encoder = joblib.load(label_encoder_path)
    meta = joblib.load(meta_path)
    return model, label_encoder, meta


def prepare_input(df: pd.DataFrame, meta: dict) -> pd.DataFrame:
    feature_cols = meta["feature_cols"]
    categorical_cols = meta["categorical_cols"]
    encoded_feature_columns = meta["encoded_feature_columns"]

    X = df[feature_cols].copy()
    X = pd.get_dummies(X, columns=categorical_cols)
    X = X.reindex(columns=encoded_feature_columns, fill_value=0)
    return X


def predict_top_1(model, label_encoder, X: pd.DataFrame):
    probs = model.predict_proba(X)[0]
    idx = probs.argmax()
    label = label_encoder.inverse_transform([idx])[0]
    prob = float(probs[idx])
    return {"label": label, "probability": round(prob, 4)}


def get_business_stage(row: pd.Series) -> str:
    conversion = row["conversion_readiness_score"]
    repeat = row["repeat_purchase_rate"]
    loyalty = row["brand_loyalty_score"]

    if conversion < 0.40 and repeat < 0.40:
        return "Early Stage"
    elif conversion < 0.65 and loyalty < 0.60:
        return "Growth Stage"
    return "Mature Stage"


def get_product_style(row: pd.Series) -> str:
    if row["is_visual_product"] >= 0.65:
        return "Visual Product"
    elif row["is_utility_product"] >= 0.65:
        return "Utility Product"
    return "Hybrid Product"


def build_strategy(niche: str, platform: str, dense_slice: str, row: pd.Series) -> dict:
    stage = get_business_stage(row)
    product_style = get_product_style(row)

    strategy_map = {
        "DIY_Crafters": "Lead with tutorials, creator demos, and community proof.",
        "Healthy_Eating": "Lead with trust, routines, and repeat purchase messaging.",
        "Pet_Lovers": "Use emotional storytelling, UGC, and repeat-purchase bundles.",
        "Home_Decor_Lovers": "Use visual inspiration, before-after content, and aesthetic positioning.",
        "Online_Learners": "Use educational value, long-form explanation, and proof of usefulness.",
        "Organic_Beauty": "Use trust, ingredients, brand story, and premium positioning.",
        "Skincare_Enthusiasts": "Use ingredient education, routine logic, and transformation proof.",
        "Streetwear_Fans": "Use trend-led visuals, drops, scarcity, and identity.",
        "Gadget_Geeks": "Use product depth, technical comparisons, and research-driven content.",
        "Gym_Beginners": "Use motivation, quick wins, and beginner-friendly positioning.",
    }

    platform_map = {
        "TikTok": "Use short-form hooks, fast demos, and trend-native creatives.",
        "Instagram": "Use strong visuals, creator content, and aesthetic storytelling.",
        "Reddit": "Use trust-building, honest explanations, and discussion-led positioning.",
        "Pinterest": "Use visual inspiration, save-worthy content, and intent-driven discovery.",
        "Website_First": "Optimize landing pages, intent capture, and conversion flow.",
        "Marketplace_First": "Compete on clarity, reviews, and conversion-ready positioning.",
        "Facebook_Groups": "Use community trust, referrals, and social proof.",
        "Discord": "Use niche community engagement and retention loops.",
        "YouTube_Shorts": "Use short educational or demonstration-led videos.",
        "Micro_Influencers": "Use creator partnerships and authentic product proof.",
    }

    dense_slice_map = {
        "College_Students": "Keep pricing accessible and content energetic.",
        "Young_Professionals": "Focus on convenience, identity, and practical value.",
        "Luxury_Buyers": "Use premium storytelling, exclusivity, and trust.",
        "Fitness_Enthusiasts": "Use performance, progress, and motivational framing.",
        "Pet_Owners": "Use emotional trust and routine-driven repeat value.",
        "Suburban_Families": "Emphasize practicality, reliability, and repeat utility.",
        "Tech_Early_Adopters": "Use innovation, detail, and differentiation.",
        "Urban_Female_20_30": "Use aesthetic identity, relevance, and social proof.",
        "Budget_Shoppers": "Lead with value, bundles, and affordability.",
        "DIY_Creators": "Lead with creator proof, tutorials, and hands-on value.",
    }

    return {
        "business_stage": stage,
        "product_style": product_style,
        "niche_strategy": strategy_map.get(niche, "Use niche-specific positioning."),
        "platform_strategy": platform_map.get(platform, "Use platform-native content."),
        "dense_slice_strategy": dense_slice_map.get(dense_slice, "Tailor the offer to the audience segment."),
    }


def run_decision_engine_by_vendor_id(vendor_id: str):
    df = load_feature_store()
    matched_rows = df[df["vendor_id"] == vendor_id]

    if matched_rows.empty:
        raise ValueError(f"Vendor ID {vendor_id} not found.")

    single_row = matched_rows.iloc[[0]].copy()
    row = single_row.iloc[0]

    niche_model, niche_encoder, niche_meta = load_model_bundle(
        NICHE_MODEL_PATH, NICHE_LABEL_ENCODER_PATH, NICHE_META_PATH
    )
    platform_model, platform_encoder, platform_meta = load_model_bundle(
        PLATFORM_MODEL_PATH, PLATFORM_LABEL_ENCODER_PATH, PLATFORM_META_PATH
    )
    dense_model, dense_encoder, dense_meta = load_model_bundle(
        DENSE_MODEL_PATH, DENSE_LABEL_ENCODER_PATH, DENSE_META_PATH
    )

    X_niche = prepare_input(single_row, niche_meta)
    X_platform = prepare_input(single_row, platform_meta)
    X_dense = prepare_input(single_row, dense_meta)

    niche_pred = predict_top_1(niche_model, niche_encoder, X_niche)
    platform_pred = predict_top_1(platform_model, platform_encoder, X_platform)
    dense_pred = predict_top_1(dense_model, dense_encoder, X_dense)

    best_niche = niche_pred["label"]
    best_platform = platform_pred["label"]
    best_dense = dense_pred["label"]

    strategy = build_strategy(best_niche, best_platform, best_dense, row)

    return {
        "vendor_id": row["vendor_id"],
        "business_name": row["business_name"],
        "actual_niche": row["target_micro_niche"],
        "actual_platform": row["target_platform"],
        "actual_dense_slice": row["target_dense_slice"],
        "niche_prediction": niche_pred,
        "platform_prediction": platform_pred,
        "dense_slice_prediction": dense_pred,
        "recommended_combination": {
            "niche": best_niche,
            "platform": best_platform,
            "dense_slice": best_dense,
        },
        "business_recommendation": strategy,
    }


def build_report_text(result: dict, execution_plan: dict) -> str:
    lines = []

    lines.append("AI COMMERCE INTELLIGENCE PLATFORM REPORT")
    lines.append("=" * 60)
    lines.append(f"Vendor ID: {result['vendor_id']}")
    lines.append(f"Business Name: {result['business_name']}")
    lines.append("")

    lines.append("PREDICTIONS")
    lines.append("-" * 60)
    lines.append(
        f"Niche: {result['niche_prediction']['label']} "
        f"({result['niche_prediction']['probability'] * 100:.2f}%)"
    )
    lines.append(
        f"Platform: {result['platform_prediction']['label']} "
        f"({result['platform_prediction']['probability'] * 100:.2f}%)"
    )
    lines.append(
        f"Dense Slice: {result['dense_slice_prediction']['label']} "
        f"({result['dense_slice_prediction']['probability'] * 100:.2f}%)"
    )
    lines.append("")

    lines.append("RECOMMENDED COMBINATION")
    lines.append("-" * 60)
    lines.append(f"Niche: {result['recommended_combination']['niche']}")
    lines.append(f"Platform: {result['recommended_combination']['platform']}")
    lines.append(f"Dense Slice: {result['recommended_combination']['dense_slice']}")
    lines.append("")

    lines.append("BUSINESS RECOMMENDATION")
    lines.append("-" * 60)
    lines.append(f"Stage: {result['business_recommendation']['business_stage']}")
    lines.append(f"Product Style: {result['business_recommendation']['product_style']}")
    lines.append(f"Niche Strategy: {result['business_recommendation']['niche_strategy']}")
    lines.append(f"Platform Strategy: {result['business_recommendation']['platform_strategy']}")
    lines.append(f"Dense Slice Strategy: {result['business_recommendation']['dense_slice_strategy']}")
    lines.append("")

    lines.append("AI EXECUTION PLAN")
    lines.append("-" * 60)
    
    summary_text = build_executive_summary(result)
    lines.append("EXECUTIVE SUMMARY")
    lines.append("-" * 60)
    lines.append(summary_text)
    lines.append("")
    
    section_titles = {
        "niche_strategy": "Niche Execution Tasks",
        "platform_strategy": "Platform Execution Tasks",
        "audience_strategy": "Audience Execution Tasks",
        "growth_strategy": "Growth Execution Tasks",
    }

    for section_key, section_label in section_titles.items():
        if section_key in execution_plan:
            lines.append(section_label + ":")
            for i, task in enumerate(execution_plan[section_key], start=1):
                lines.append(f"  {i}. {task}")
            lines.append("")

    return "\n".join(lines)

def build_reasoning_points(result: dict, row: pd.Series) -> list:
    reasons = []

    if row["repeat_purchase_rate"] >= 0.65:
        reasons.append("High repeat purchase behavior supports a retention-friendly niche recommendation.")

    if row["premium_affinity_score"] >= 0.65:
        reasons.append("Strong premium affinity suggests positioning toward premium or trust-driven segments.")

    if row["image_engagement_score"] >= 0.65:
        reasons.append("High visual engagement supports visually driven channel recommendations.")

    if row["short_form_video_affinity"] >= 0.65:
        reasons.append("Strong short-form content affinity supports video-first platform strategy.")

    if row["search_intent_score"] >= 0.65:
        reasons.append("Strong search intent indicates high-conversion, intent-driven discovery potential.")

    if row["community_engagement_score"] >= 0.65:
        reasons.append("High community engagement supports audience segments and platforms that depend on trust and interaction.")

    if row["female_ratio"] >= 0.60:
        reasons.append("Audience composition skews female, which influences the selected audience slice and creative direction.")

    if row["age_25_34_ratio"] >= 0.40:
        reasons.append("A strong 25–34 audience signal supports growth-oriented and digitally active customer segments.")

    if row["conversion_readiness_score"] >= 0.65:
        reasons.append("High conversion readiness suggests this business is prepared for immediate go-to-market execution.")

    if not reasons:
        reasons.append("The recommendation is based on the combined behavior, audience, and product signals across all three models.")

    return reasons

def build_executive_summary(result: dict) -> str:
    return (
        f"This business is best positioned for the niche "
        f"'{result['niche_prediction']['label']}', should prioritize "
        f"'{result['platform_prediction']['label']}' as its primary platform, "
        f"and target the audience slice '{result['dense_slice_prediction']['label']}'. "
        f"The recommended execution path is to align product positioning, platform strategy, "
        f"and audience targeting around this combination."
    )

def main():
    st.set_page_config(page_title="AI Commerce Intelligence Platform", layout="wide")

    st.title("AI Commerce Intelligence Platform")
    st.caption("From prediction to strategy to execution for Shopify businesses")

    st.markdown(
        """
        This dashboard predicts the best **niche**, **platform**, and **dense audience slice**
        for a business, then generates a practical **execution plan**.
        """
    )
    st.write("Enter a vendor_id to generate a final niche, platform, and dense-slice recommendation.")

    df = load_feature_store()
    df["vendor_id"] = df["vendor_id"].astype(str)

    vendor_ids = sorted(df["vendor_id"].unique(), key=lambda x: int(x))
    st.info(f"Available vendor_id range: {vendor_ids[0]} to {vendor_ids[-1]}")

    business_names = sorted(df["business_name"].dropna().unique().tolist())

    selected_business = st.selectbox("Select Business Name", business_names)

    vendor_id = df.loc[df["business_name"] == selected_business, "vendor_id"].iloc[0]

    st.write(f"**Selected Vendor ID:** {vendor_id}")
    
    st.caption("Business selected successfully. Click below to generate the full decision report.")

    if st.button("Generate Report"):
        if vendor_id not in set(vendor_ids):
            st.error("Invalid vendor_id mapped from selected business.")
            return

        result = run_decision_engine_by_vendor_id(vendor_id)
        execution_plan = build_execution_plan(result)
        
        report_text = build_report_text(result, execution_plan)
        
        summary_text = build_executive_summary(result)
        
        row = df[df["vendor_id"] == vendor_id].iloc[0]
        reasoning_points = build_reasoning_points(result, row)
        
        tab1, tab2, tab3 = st.tabs(["Overview", "Strategy", "Execution"])

        st.subheader("Business Info")
        col1, col2 = st.columns(2)
        col1.metric("Vendor ID", result["vendor_id"])
        col2.metric("Business Name", result["business_name"])

        st.subheader("Model Predictions")
        c1, c2, c3 = st.columns(3)
        c1.metric("Predicted Niche", result["niche_prediction"]["label"], result["niche_prediction"]["probability"])
        c2.metric("Predicted Platform", result["platform_prediction"]["label"], result["platform_prediction"]["probability"])
        c3.metric("Predicted Dense Slice", result["dense_slice_prediction"]["label"], result["dense_slice_prediction"]["probability"])

        st.subheader("Recommended Combination")
        st.write(result["recommended_combination"])

        st.subheader("Business Recommendation")
        st.write(f"**Stage:** {result['business_recommendation']['business_stage']}")
        st.write(f"**Product Style:** {result['business_recommendation']['product_style']}")
        st.write(f"**Niche Strategy:** {result['business_recommendation']['niche_strategy']}")
        st.write(f"**Platform Strategy:** {result['business_recommendation']['platform_strategy']}")
        st.write(f"**Dense Slice Strategy:** {result['business_recommendation']['dense_slice_strategy']}")
        
        st.subheader("AI Execution Plan")
        
        st.subheader("Executive Summary")
        st.info(summary_text)
        
        st.download_button(
            label="Download Report",
            data=report_text,
            file_name=f"business_report_{result['vendor_id']}.txt",
            mime="text/plain"
        )

        section_titles = {
            "niche_strategy": "Niche Execution Tasks",
            "platform_strategy": "Platform Execution Tasks",
            "audience_strategy": "Audience Execution Tasks",
            "growth_strategy": "Growth Execution Tasks",
        }

        for section_key, section_label in section_titles.items():
            if section_key in execution_plan:
                with st.container():
                    st.markdown(f"### {section_label}")
                    for i, task in enumerate(execution_plan[section_key], start=1):
                        st.write(f"{i}. {task}")
                    st.markdown("---")

        with st.expander("Actual Labels in Dataset"):
            st.write(f"Actual Niche: {result['actual_niche']}")
            st.write(f"Actual Platform: {result['actual_platform']}")
            st.write(f"Actual Dense Slice: {result['actual_dense_slice']}")
            
        with tab1:
            st.subheader("Business Info")
            col1, col2 = st.columns(2)
            col1.metric("Vendor ID", result["vendor_id"])
            col2.metric("Business Name", result["business_name"])

            st.subheader("Model Predictions")
            c1, c2, c3 = st.columns(3)
            c1.metric(
                "Predicted Niche",
                result["niche_prediction"]["label"],
                f"{result['niche_prediction']['probability'] * 100:.2f}%"
            )
            c2.metric(
                "Predicted Platform",
                result["platform_prediction"]["label"],
                f"{result['platform_prediction']['probability'] * 100:.2f}%"
            )
            c3.metric(
                "Predicted Dense Slice",
                result["dense_slice_prediction"]["label"],
                f"{result['dense_slice_prediction']['probability'] * 100:.2f}%"
            )

            with st.expander("Actual Labels in Dataset"):
                st.write(f"Actual Niche: {result['actual_niche']}")
                st.write(f"Actual Platform: {result['actual_platform']}")
                st.write(f"Actual Dense Slice: {result['actual_dense_slice']}")
        
        with tab2:
            st.subheader("Recommended Combination")
            st.write(result["recommended_combination"])

            st.markdown("### Why this recommendation?")
            st.caption("Key behavioral and audience signals that influenced the final recommendation.")

            for i, point in enumerate(reasoning_points, start=1):
                st.write(f"{i}. {point}")
            
            st.subheader("Business Recommendation")
            st.write(f"**Stage:** {result['business_recommendation']['business_stage']}")
            st.write(f"**Product Style:** {result['business_recommendation']['product_style']}")
            st.write(f"**Niche Strategy:** {result['business_recommendation']['niche_strategy']}")
            st.write(f"**Platform Strategy:** {result['business_recommendation']['platform_strategy']}")
            st.write(f"**Dense Slice Strategy:** {result['business_recommendation']['dense_slice_strategy']}")
            
        with tab3:
            st.success("Execution plan generated successfully.")

            st.markdown("## AI Execution Plan")
            st.caption("Actionable next steps generated from the final decision engine output.")

            section_titles = {
                "niche_strategy": "Niche Execution Tasks",
                "platform_strategy": "Platform Execution Tasks",
                "audience_strategy": "Audience Execution Tasks",
                "growth_strategy": "Growth Execution Tasks",
            }

            for section_key, section_label in section_titles.items():
                if section_key in execution_plan:
                    st.markdown(f"### {section_label}")
                    for i, task in enumerate(execution_plan[section_key], start=1):
                        st.write(f"{i}. {task}")
                    st.markdown("---")
                    
        
                    
        


if __name__ == "__main__":
    main()