"""
Example classifier on Numerai data using a xgboost regression.
To get started, install the required packages: pip install pandas numpy sklearn xgboost
"""
from typing import Tuple

import joblib
import lightgbm as lgb
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

import config
from libs.features import get_group_stats
from libs.utils.data import download_current_data, load_data
from libs.utils.log import create_logger
from libs.utils.metrics import evaluate
from libs.utils.submit import submit

RUN_NAME = "base_lgbm"
MODEL_NAME = "udus"
MODEL_ID = "5f4056a7-60a9-4203-839a-2ab0a2cbec5f"
TARGET_NAME = "target"
PREDICTION_NAME = "prediction"
DATASET_DIR = config.RAW_DATA_DIR
MODEL_FILE = config.MODEL_DIR / f"{RUN_NAME}.model"


logger = create_logger(RUN_NAME)


def prepare_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    logger.info("Loading data...")
    # The training data is used to train your model how to predict the targets.
    download_current_data(DATASET_DIR)

    train_data, validataion_data, tournament_data = load_data(
        DATASET_DIR, reduce_memory=True
    )
    logger.info("Data loading has finished")
    return train_data, validataion_data, tournament_data


def main():
    train_data, validation_data, tournament_data = prepare_data()

    feature_names = [f for f in train_data.columns if f.startswith("feature")]
    logger.info(f"Loaded data have {len(feature_names)} features")

    # 特徴量エンジニアリング

    # feature creation
    # Add group statistics features
    train_data = get_group_stats(train_data)
    validation_data = get_group_stats(validation_data)
    tournament_data = get_group_stats(tournament_data)

    # feature selection
    # Calculate correlations with target
    full_corr = train_data.corr()
    corr_with_target = full_corr["target"].T.apply(abs).sort_values(ascending=False)

    # Select features with highest correlation to the target variable
    features = corr_with_target[:150]
    features.drop("target", inplace=True)

    # Create list of most correlated features
    feature_list = features.index.tolist()

    if MODEL_FILE.is_file():
        logger.info("Loading pre-trained model...")
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
        logger.info("Training model...")
        model.fit(train_data[feature_list], train_data[TARGET_NAME])
        logger.info("saving features")
        joblib.dump(model, MODEL_FILE)

    # Generate predictions on both training and code data
    logger.info("Generating predictions...")
    train_data[PREDICTION_NAME] = model.predict(train_data[feature_list])
    validation_data[PREDICTION_NAME] = model.predict(validation_data[feature_list])
    tournament_data[PREDICTION_NAME] = model.predict(tournament_data[feature_list])

    # Evaluation
    # Evaluate Model
    spearman, payout, numerai_sharpe, mae = evaluate(train_data)
    logger.info("--- Final Training Scores ---")
    logger.info(f"Spearman Correlation: {spearman}")
    logger.info(f"Average Payout: {payout}")
    logger.info(f"Sharpe Ratio: {numerai_sharpe}")
    logger.info(f"Mean Absolute Error (MAE): {mae}")
    spearman, payout, numerai_sharpe, mae = evaluate(validation_data)
    logger.info("--- Final Validation Scores ---")
    logger.info(f"Spearman Correlation: {spearman}")
    logger.info(f"Average Payout: {payout}")
    logger.info(f"Sharpe Ratio: {numerai_sharpe}")
    logger.info(f"Mean Absolute Error (MAE): {mae}")
    # Calculate feature exposure
    all_features = [col for col in train_data.columns if "feature" in col]
    feature_spearman_val = [
        spearmanr(validation_data[PREDICTION_NAME], validation_data[f])[0]
        for f in all_features
    ]
    feature_exposure_val = np.std(feature_spearman_val).round(4)
    logger.info(f"Feature Exposure: {feature_exposure_val}")

    # Submission
    logger.info("writing predictions to file and submitting.")
    submit(
        tournament_data[["id", PREDICTION_NAME]],
        config.OUTPUT_DIR / "submission.csv",
        model_id=MODEL_ID,
    )


if __name__ == "__main__":
    main()
