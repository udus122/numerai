"""
download numerai dataset through with numerai api
"""

import os

import numerapi
import numpy as np
import pandas as pd

napi = numerapi.NumerAPI(verbosity="info")


def download_current_data(directory: str):
    """
    Downloads the data for the current round
    :param directory: The path to the directory where the data needs to be saved
    """
    current_round = napi.get_current_round()
    if os.path.isdir(f"{directory}/numerai_dataset_{current_round}/"):
        print(f"You already have the newest data! Current round is: {current_round}")
    else:
        print(f"Downloading new data for round: {current_round}!")
        napi.download_current_dataset(dest_path=directory, unzip=True)


def load_data(directory: str, reduce_memory: bool = True) -> tuple:
    """
    Get data for current round
    :param directory: The path to the directory where the data needs to be saved
    :return: A tuple containing the datasets
    """
    print("Loading the data")
    full_path = f"{directory}/numerai_dataset_{napi.get_current_round()}/"
    train_path = full_path + "numerai_training_data.csv"
    test_path = full_path + "numerai_tournament_data.csv"
    train_data = pd.read_csv(train_path)
    tournament_data = pd.read_csv(test_path)

    # Reduce all features to 32-bit floats
    if reduce_memory:
        num_features = [f for f in train_data.columns if f.startswith("feature")]
        train_data[num_features] = train_data[num_features].astype(np.float32)
        tournament_data[num_features] = tournament_data[num_features].astype(np.float32)

    validation_data = tournament_data[tournament_data["data_type"] == "validation"]
    return train_data, validation_data, tournament_data


# TODO: add test code
# if __name__ == "__main__":
# Download, unzip and load data
# download_current_data(DIR)
# train, val, test = load_data(DIR, reduce_memory=True)
