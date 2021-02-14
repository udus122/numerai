import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.metrics import mean_absolute_error


def sharpe_ratio(corrs: pd.Series) -> np.float32:
    """
    Calculate the Sharpe ratio for Numerai by using grouped per-era data

    :param corrs: A Pandas Series containing the Spearman correlations for each era
    :return: A float denoting the Sharpe ratio of your predictions.
    """
    return corrs.mean() / corrs.std()


def evaluate(df: pd.DataFrame) -> tuple:
    """
    Evaluate and display relevant metrics for Numerai

    :param df: A Pandas DataFrame containing the columns "era", "target" and "prediction"
    :return: A tuple of float containing the metrics
    """

    def _score(sub_df: pd.DataFrame) -> np.float32:
        """Calculates Spearman correlation"""
        return spearmanr(sub_df["target"], sub_df["prediction"])[0]

    # Calculate metrics
    corrs = df.groupby("era").apply(_score)
    payout_raw = (corrs / 0.2).clip(-1, 1)
    spearman = round(corrs.mean(), 4)
    payout = round(payout_raw.mean(), 4)
    numerai_sharpe = round(sharpe_ratio(corrs), 4)
    mae = mean_absolute_error(df["target"], df["prediction"]).round(4)

    # Display metrics
    print(f"Spearman Correlation: {spearman}")
    print(f"Average Payout: {payout}")
    print(f"Sharpe Ratio: {numerai_sharpe}")
    print(f"Mean Absolute Error (MAE): {mae}")
    return spearman, payout, numerai_sharpe, mae
