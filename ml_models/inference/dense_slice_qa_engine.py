import pandas as pd

INPUT_FILE = "ml_models/feature_store/business_feature_store.csv"


def load_data() -> pd.DataFrame:
    return pd.read_csv(INPUT_FILE)


def answer_question(question_id: int, df: pd.DataFrame) -> None:
    print(f"\nQuestion {question_id}:")

    if question_id == 1:
        print("Which dense slice is best for what type of niche?")
        result = (
            df.groupby("target_dense_slice")["target_micro_niche"]
            .agg(lambda x: x.value_counts().index[0])
            .sort_index()
        )
        print(result)

    elif question_id == 2:
        print("Which dense slice is best for what type of platform?")
        result = (
            df.groupby("target_dense_slice")["target_platform"]
            .agg(lambda x: x.value_counts().index[0])
            .sort_index()
        )
        print(result)

    elif question_id == 3:
        print("Which dense slice has the youngest audience?")
        cols = [
            "target_dense_slice",
            "age_18_24_ratio",
            "age_25_34_ratio",
            "age_35_50_ratio",
            "age_50_plus_ratio",
        ]
        result = df[cols].groupby("target_dense_slice").mean().round(3)
        print(result)

    elif question_id == 4:
        print("Which dense slice is strongest for female-driven demand?")
        result = (
            df.groupby("target_dense_slice")["female_ratio"]
            .mean()
            .sort_values(ascending=False)
            .round(3)
        )
        print(result)

    elif question_id == 5:
        print("Which dense slice is strongest for premium buyers?")
        cols = [
            "target_dense_slice",
            "income_high_ratio",
            "premium_affinity_score",
            "price_sensitivity_score",
        ]
        result = df[cols].groupby("target_dense_slice").mean().round(3)
        print(result)

    elif question_id == 6:
        print("Which dense slice is strongest for budget-sensitive buyers?")
        cols = [
            "target_dense_slice",
            "income_low_ratio",
            "price_sensitivity_score",
        ]
        result = df[cols].groupby("target_dense_slice").mean().round(3)
        print(result)

    elif question_id == 7:
        print("Which dense slice is strongest for trend and content behavior?")
        cols = [
            "target_dense_slice",
            "trend_sensitivity_score",
            "short_form_video_affinity",
            "image_engagement_score",
            "video_consumption_score",
        ]
        result = df[cols].groupby("target_dense_slice").mean().round(3)
        print(result)

    elif question_id == 8:
        print("Which dense slice is strongest for repeat buying?")
        result = (
            df.groupby("target_dense_slice")["repeat_purchase_rate"]
            .mean()
            .sort_values(ascending=False)
            .round(3)
        )
        print(result)

    elif question_id == 9:
        print("Which dense slice is strongest for search/research intent?")
        cols = [
            "target_dense_slice",
            "search_intent_score",
            "research_time_score",
            "conversion_readiness_score",
        ]
        result = df[cols].groupby("target_dense_slice").mean().round(3)
        print(result)

    elif question_id == 10:
        print("Which dense slice is strongest for community-led commerce?")
        cols = [
            "target_dense_slice",
            "community_engagement_score",
            "ugc_score",
            "local_discovery_score",
        ]
        result = df[cols].groupby("target_dense_slice").mean().round(3)
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