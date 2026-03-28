import pandas as pd

INPUT_FILE = "ml_models/feature_store/business_feature_store.csv"


def load_data() -> pd.DataFrame:
    return pd.read_csv(INPUT_FILE)


def answer_question(question_id: int, df: pd.DataFrame) -> None:
    print(f"\nQuestion {question_id}:")

    if question_id == 1:
        print("Which niche is better for what type of vendor?")
        result = (
            df.groupby("target_micro_niche")["business_category"]
            .agg(lambda x: x.value_counts().index[0])
            .sort_index()
        )
        print(result)

    elif question_id == 2:
        print("Which niche is better for what type of products they sell?")
        cols = [
            "target_micro_niche",
            "is_visual_product",
            "is_utility_product",
            "premium_affinity_score",
            "repeat_purchase_rate",
            "ugc_score",
        ]
        result = df[cols].groupby("target_micro_niche").mean().round(3)
        print(result)

    elif question_id == 3:
        print("Which niche is better for what stage of business?")
        cols = [
            "target_micro_niche",
            "conversion_readiness_score",
            "repeat_purchase_rate",
            "brand_loyalty_score",
        ]
        result = df[cols].groupby("target_micro_niche").mean().round(3)
        print(result)

    elif question_id == 4:
        print("Which niche has the highest conversion readiness?")
        result = (
            df.groupby("target_micro_niche")["conversion_readiness_score"]
            .mean()
            .sort_values(ascending=False)
            .round(3)
        )
        print(result)

    elif question_id == 5:
        print("Which niche is most price sensitive?")
        result = (
            df.groupby("target_micro_niche")["price_sensitivity_score"]
            .mean()
            .sort_values(ascending=False)
            .round(3)
        )
        print(result)

    elif question_id == 6:
        print("Which niche is best for repeat purchases?")
        result = (
            df.groupby("target_micro_niche")["repeat_purchase_rate"]
            .mean()
            .sort_values(ascending=False)
            .round(3)
        )
        print(result)

    elif question_id == 7:
        print("Which niche is more content-driven vs intent-driven?")
        cols = [
            "target_micro_niche",
            "image_engagement_score",
            "text_engagement_score",
            "video_consumption_score",
            "search_intent_score",
            "research_time_score",
        ]
        result = df[cols].groupby("target_micro_niche").mean().round(3)
        print(result)

    elif question_id == 8:
        print("Which niche is strongest for premium products?")
        result = (
            df.groupby("target_micro_niche")["premium_affinity_score"]
            .mean()
            .sort_values(ascending=False)
            .round(3)
        )
        print(result)

    elif question_id == 9:
        print("Which niche is strongest for community / UGC behavior?")
        cols = [
            "target_micro_niche",
            "community_engagement_score",
            "ugc_score",
        ]
        result = df[cols].groupby("target_micro_niche").mean().round(3)
        print(result)

    elif question_id == 10:
        print("Which niche is strongest for trend-driven behavior?")
        cols = [
            "target_micro_niche",
            "trend_sensitivity_score",
            "short_form_video_affinity",
            "image_engagement_score",
        ]
        result = df[cols].groupby("target_micro_niche").mean().round(3)
        print(result)

    else:
        print("Invalid question id.")


def main():
    df = load_data()

    for question_id in range(1, 11):
        answer_question(question_id, df)
        print("\n" + "=" * 100)


if __name__ == "__main__":
    main()