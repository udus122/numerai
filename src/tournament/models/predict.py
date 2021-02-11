import logging

import pandas as pd
from sklearn.linear_model import LinearRegression

from ..data.download_data import download_data
from .train import train
from ..libs.submit import submit

# Define models here as (ID, model instance),
# a model ID of None is submitted as your default model
MODEL_CONFIGS = [
    (None, LinearRegression()),
    # (YOUR MODEL ID, LinearRegression(n_jobs=10))
    #  etc...
]


def predict(model, predict_data_path):
    logging.info("reading prediction data")
    predict_data = pd.read_csv(predict_data_path)

    logging.info("extracting features")
    predict_ids = predict_data.iloc[:, 0]  # get all rows and only first column
    predict_features = predict_data.iloc[
        :, 3:-1
    ]  # get all rows and all columns from 4th to last-1

    logging.info("generating predictions")
    predictions = model.predict(predict_features)
    predictions = pd.DataFrame(predictions, columns=["prediction"])
    predictions.insert(0, "id", predict_ids)

    return predictions


if __name__ == "__main__":
    train_data_path, predict_data_path, predict_output_path = download_data()

    for model_id, model_type in MODEL_CONFIGS:
        trained_model = train(train_data_path, model_id, model_type)
        predictions = predict(trained_model, predict_data_path)
        submit(predictions, predict_output_path, model_id)
