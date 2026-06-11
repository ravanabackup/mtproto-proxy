import logging
import sys


def setup_logger(level: int = logging.INFO):
    log_format = "%(asctime)s [%(levelname)s][%(name)s]: %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    root = logging.getLogger()
    if root.handlers:
        for handler in root.handlers[:]:
            root.removeHandler(handler)


    logging.basicConfig(
        level=level,
        format=log_format,
        datefmt=date_format,
        handlers=[logging.StreamHandler(sys.stdout)]
    )