from logging import DEBUG, INFO, FileHandler, Formatter, StreamHandler, getLogger

import config


def create_logger(run_name: str):
    log_file = config.LOG_DIR / f"{run_name}.log"

    # logger
    logger_ = getLogger(run_name)
    logger_.setLevel(DEBUG)

    # formatter
    fmr = Formatter(
        "[%(levelname)s] %(asctime)s >> %(filename)s, line %(lineno)d\n%(message)s "
    )

    # file handler
    fh = FileHandler(log_file)
    fh.setLevel(DEBUG)
    fh.setFormatter(fmr)

    # stream handler
    ch = StreamHandler()
    ch.setLevel(INFO)
    ch.setFormatter(fmr)

    logger_.addHandler(fh)
    logger_.addHandler(ch)


def get_logger(run_name):
    return getLogger(run_name)
