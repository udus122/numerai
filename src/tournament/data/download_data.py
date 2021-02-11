"""
download numerai dataset through with numerai api
"""

import numerapi
import logging

napi = numerapi.NumerAPI()


def download_data():
    logging.info("downloading tournament data files")
    # create an API client and download current data
    file_path = napi.download_current_dataset()
    file_path = file_path.split(".zip")[0]  # we only want the unzipped directory
    logging.info(f"output path: {file_path}")

    train_data_path = f"{file_path}/numerai_training_data.csv"
    predict_data_path = f"{file_path}/numerai_tournament_data.csv"
    predict_output_path = f"{file_path}/predictions.csv"

    return train_data_path, predict_data_path, predict_output_path


if __name__ == "__main__":
    download_data()
