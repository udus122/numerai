"""
Example classifier on Numerai data using a xgboost regression.
To get started, install the required packages: pip install pandas numpy sklearn xgboost
"""

import logging
from pathlib import Path

import joblib
import lightgbm as lgb
import numerapi
from libs import config
from libs.data.download_data import download_current_data, load_data

TARGET_NAME = f"target"
PREDICTION_NAME = f"prediction"
MODEL_FILE = Path("trained_model")


def main():
    logging.info("Loading data...")
    # The training data is used to train your model how to predict the targets.
    download_current_data(str(config.DATA_DIR))

    train_data, validation_data, code_data = load_data(
        str(config.DATA_DIR), reduce_memory=True
    )

    feature_names = [f for f in train_data.columns if f.startswith("feature")]
    logging.info(f"Loaded {len(feature_names)} features")

    if MODEL_FILE.is_file():
        logging.info("Loading pre-trained model...")
        model = joblib.load(MODEL_FILE)
    else:
        model = lgb.LGBMRegressor(
            bagging_fraction=0.7,
            bagging_freq=7,
            feature_fraction=0.65,
            learning_rate=0.05,
            max_depth=4,
            num_leaves=30,
        )
        logging.info("Training model...")
        model.fit(train_data.loc[:, feature_names], train_data.loc[:, TARGET_NAME])
        logging.info("saving features")
        joblib.dump(model, MODEL_FILE.name)

    # Generate predictions on both training and code data
    logging.info("Generating predictions...")
    train_data[PREDICTION_NAME] = model.predict(train_data[feature_names])
    code_data[PREDICTION_NAME] = model.predict(code_data[feature_names])

    # Set API Keys for submitting to Numerai
    PUBLIC_ID = "2JH4X4MSLA74NG4JRDE7WJ46EOFMM7CS"
    SECRET_KEY = "HBNFWREBA3NNAIIVT4QK7UOFOH4IGOHKEDVVVAAEN7AP3ZPA4W2RG52KFNIFZSGY"

    # Initialize API with API Keys
    napi = numerapi.NumerAPI(
        public_id=PUBLIC_ID, secret_key=SECRET_KEY, verbosity="info"
    )
    code_data[["id", PREDICTION_NAME]].to_csv("submission.csv", index=False)
    # Upload predictions to Numerai
    napi.upload_predictions("submission.csv")


if __name__ == "__main__":
    main()
