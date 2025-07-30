import logging
import sys

def setup_logger(name: str) -> logging.Logger:
    # Only configure the root logger once
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    return logging.getLogger(name)