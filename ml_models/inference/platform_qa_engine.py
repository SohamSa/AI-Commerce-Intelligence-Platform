import pandas as pd

INPUT_FILE = "ml_models/feature_store/business_feature_store.csv"


def load_data() -> pd.DataFrame:
    return pd.read_csv(INPUT_FILE)


def answer_question(question_id: int, df: pd.DataFrame) -> None:
    print(f"\nQuestion {question_id}:")

    if question_id == 1:
        print("Which platform is best for what type of niche?")
        result = (
            df.groupby("target_platform")["target_micro_niche"]
            .agg(lambda x: x.value_counts().index[0])
            .sort_index()
        )
        print(result)

    elif question_id == 2:
        print("Which platform is best for visual products vs utility products?")
        cols = [
            "target_platform",
            "is_visual_product",
            "is_utility_product",
            "image_engagement_score",
            "video_consumption_score",
        ]
        result = df[cols].groupby("target_platform").mean().round(3)
        print(result)

    elif question_id == 3:
        print("Which platform is best for search intent vs content discovery?")
        cols = [
            "target_platform",
            "search_intent_score",
            "research_time_score",
            "image_engagement_score",
            "text_engagement_score",
            "short_form_video_affinity",
        ]
        result = df[cols].groupby("target_platform").mean().round(3)
        print(result)

    elif question_id == 4:
        print("Which platform is best for premium products?")
        result = (
            df.groupby("target_platform")["premium_affinity_score"]
            .mean()
            .sort_values(ascending=False)
            .round(3)
        )
        print(result)

    elif question_id == 5:
        print("Which platform is best for repeat-purchase businesses?")
        result = (
            df.groupby("target_platform")["repeat_purchase_rate"]
            .mean()
            .sort_values(ascending=False)
            .round(3)
        )
        print(result)

    elif question_id == 6:
        print("Which platform is most trend-driven?")
        cols = [
            "target_platform",
            "trend_sensitivity_score",
            "short_form_video_affinity",
            "impulse_buy_score",
        ]
        result = df[cols].groupby("target_platform").mean().round(3)
        print(result)

    elif question_id == 7:
        print("Which platform is strongest for community-led selling?")
        cols = [
            "target_platform",
            "community_engagement_score",
            "ugc_score",
            "local_discovery_score",
        ]
        result = df[cols].groupby("target_platform").mean().round(3)
        print(result)

    elif question_id == 8:
        print("Which platform is strongest for influencer-led selling?")
        cols = [
            "target_platform",
            "influencer_dependency_score",
            "image_engagement_score",
            "ugc_score",
        ]
        result = df[cols].groupby("target_platform").mean().round(3)
        print(result)

    elif question_id == 9:
        print("Which platform is strongest for conversion-ready buyers?")
        result = (
            df.groupby("target_platform")["conversion_readiness_score"]
            .mean()
            .sort_values(ascending=False)
            .round(3)
        )
        print(result)

    elif question_id == 10:
        print("Which platform is strongest for local discovery vs broad discovery?")
        cols = [
            "target_platform",
            "local_discovery_score",
            "community_engagement_score",
            "search_intent_score",
        ]
        result = df[cols].groupby("target_platform").mean().round(3)
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