import logging

from libs.napi import napi


def submit(predictions, predict_output_path, model_id=None):
    logging.info("writing predictions to file")
    # numerai doesn't want the index, so don't write it to our file
    predictions.to_csv(predict_output_path, index=False)

    # Numerai API uses Environment variables to find your keys:
    # NUMERAI_PUBLIC_ID and NUMERAI_SECRET_KEY
    # these are set by docker via the numerai cli; see README for more info
    logging.info("submitting")
    napi.upload_predictions(predict_output_path, model_id=model_id)
