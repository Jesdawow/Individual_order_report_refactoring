import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def load_orders(file_path: Path) -> pd.DataFrame:
    # Stop early with a clear error if the input file does not exist
    
    if not file_path.exists():
        logger.error("Order file not found: %s", file_path)
        raise FileNotFoundError(f"Order file not found: {file_path}")

    logger.info("Reading order data from %s", file_path)

    orders = pd.read_csv(file_path)

    logger.info("Loaded %s rows", len(orders))

    return orders

