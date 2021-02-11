import predict
import os
import logging
import joblib
import pandas as pd

TRAINED_MODEL_PREFIX = "./trained_model"


def train(train_data_path, model_id, model, force_training=False):
    model_name = f'{TRAINED_MODEL_PREFIX}_{model_id or ""}'

    # load a model if we have a trained model already and we aren't forcing a training session
    if os.path.exists(model_name) and not force_training:
        logging.info("loading existing trained model")
        model = joblib.load(model_name)
        return model

    logging.info("reading training data")
    train_data = pd.read_csv(train_data_path)

    logging.info("extracting features and targets")
    train_features = train_data.iloc[
        :, 3:-1
    ]  # get all rows and all columns from 4th to last-1
    train_targets = train_data.iloc[:, -1]  # get all rows and only last column

    logging.info("training model")
    model.fit(X=train_features, y=train_targets)

    logging.info("saving features")
    joblib.dump(model, model_name)

    return model


train_data_path, predict_data_path, predict_output_path = predict.download_data()

for model_id, model_type in predict.MODEL_CONFIGS:
    predict.train(train_data_path, model_id, model_type, force_training=True)
