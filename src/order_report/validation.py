import logging

import pandas as pd

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = {
    "order_id",
    "order_date",
    "customer_id",
    "region",
    "product_category",
    "quantity",
    "unit_price",
    "discount",
    "returned",
}


def validate_orders(orders: pd.DataFrame) -> None:
    # Stop validation early if there is no data to validate
    if orders.empty:
        logger.error("Order data is empty")
        raise ValueError("Order data is empty.")

    # Compare required columns with the columns that exist in the DataFrame
    missing_columns = REQUIRED_COLUMNS - set(orders.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        logger.error("Missing required columns: %s", missing)
        raise ValueError(f"Missing required columns: {missing}")

    # Convert numeric columns temporarily so unreasonable values can be checked
    quantity = pd.to_numeric(orders["quantity"], errors="coerce")
    unit_price = pd.to_numeric(orders["unit_price"], errors="coerce")
    discount = pd.to_numeric(orders["discount"], errors="coerce")

    if (quantity < 0).any():
        logger.error("Negative quantity values found")
        raise ValueError("quantity contains negative values.")

    if (unit_price < 0).any():
        logger.error("Negative unit_price values found")
        raise ValueError("unit_price contains negative values.")

    if ((discount < 0) | (discount > 1)).any():
        logger.error("Discount values outside the range 0 to 1 found")
        raise ValueError("discount contains values outside the range 0 to 1.")

    logger.info("Order data passed validation")