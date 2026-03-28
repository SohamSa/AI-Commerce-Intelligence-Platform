import joblib
import pandas as pd

MODEL_PATH = "ml_models/artifacts/niche_model.pkl"
LABEL_ENCODER_PATH = "ml_models/artifacts/niche_label_encoder.pkl"
META_PATH = "ml_models/artifacts/niche_meta.pkl"

INPUT_FILE = "ml_models/feature_store/business_feature_store.csv"


def load_artifacts():
    model = joblib.load(MODEL_PATH)
    label_encoder = joblib.load(LABEL_ENCODER_PATH)
    meta = joblib.load(META_PATH)
    return model, label_encoder, meta


def prepare_input(df: pd.DataFrame, meta: dict) -> pd.DataFrame:
    feature_cols = meta["feature_cols"]
    categorical_cols = meta["categorical_cols"]
    encoded_feature_columns = meta["encoded_feature_columns"]

    X = df[feature_cols].copy()
    X = pd.get_dummies(X, columns=categorical_cols)
    X = X.reindex(columns=encoded_feature_columns, fill_value=0)

    return X


def predict_top_k(model, label_encoder, X: pd.DataFrame, k: int = 3):
    probs = model.predict_proba(X)[0]
    top_idx = probs.argsort()[::-1][:k]

    results = []
    for idx in top_idx:
        label = label_encoder.inverse_transform([idx])[0]
        prob = float(probs[idx])
        results.append((label, prob))

    return results


def main():
    model, label_encoder, meta = load_artifacts()

    df = pd.read_csv(INPUT_FILE)

    # take first row for testing
    single_row = df.iloc[[0]].copy()

    X = prepare_input(single_row, meta)
    top_preds = predict_top_k(model, label_encoder, X, k=3)

    print("\nTop 3 niche predictions:")
    for rank, (label, prob) in enumerate(top_preds, start=1):
        print(f"{rank}. {label} -> {prob:.4f}")


if __name__ == "__main__":
    main()