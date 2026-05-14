"""
Model loading and prediction logic.

The model must be loaded ONCE at module level, NOT inside the predict function.
"""

import pickle
from pathlib import Path
import pandas as pd
import joblib

# TODO 1: Load your serialized churn model from data/model.joblib
MODEL_PATH = Path(__file__).resolve().parent.parent / "data" / "model.pkl"

with MODEL_PATH.open("rb") as model_file:
    model = pickle.load(model_file)

PREPROC_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "column_transformer.joblib"
)
preproc = joblib.load(PREPROC_PATH)


def predict_churn(features: list[float]) -> int:
    """
    Takes a list of feature values and returns a churn prediction (0 or 1).
    """
    # TODO 2: Use model.predict() to get a prediction and return it as an int
    #         Hint: model.predict() expects a 2D array
    columns = [
        "CreditScore",
        "Geography",
        "Gender",
        "Age",
        "Tenure",
        "Balance",
        "NumOfProducts",
        "HasCrCard",
        "IsActiveMember",
        "EstimatedSalary",
    ]

    df = pd.DataFrame([features], columns=columns)

    # 3. Transform the raw strings/cats into numerical arrays
    transformed_features = preproc.transform(df)

    # 4. Predict
    return int(model.predict(transformed_features)[0])


if __name__ == "__main__":
    # TODO 3: Replace with sample features that match your model
    # load preprocessed model and test the predict_churn function with a sample input

    sample = [619, "France", "Female", 42, 2, 0, 1, 1, 1, 101348.88]

    print(f"Input:      {sample}")
    print(f"Prediction: {predict_churn(sample)}")
