import logging

import pandas as pd

logger = logging.getLogger(__name__)


def clean_orders(orders: pd.DataFrame) -> pd.DataFrame:
    # Work on a copy of the DataFrame to avoid modifying the original data
    cleaned_orders = orders.copy()

    cleaned_orders["region"] = (
        cleaned_orders["region"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .str.title()
    )

    cleaned_orders["product_category"] = (
        cleaned_orders["product_category"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .str.title()
    )

    # Convert quantity to numeric and report values that need a fallback
    quantity = pd.to_numeric(
        cleaned_orders["quantity"],
        errors="coerce",
    )

    missing_quantity = quantity.isna().sum()
    if missing_quantity:
        logger.warning(
            "%s quantity value(s) were missing or invalid and replaced with 1",
            missing_quantity,
        )

    cleaned_orders["quantity"] = quantity.fillna(1)


    unit_price = pd.to_numeric(
        cleaned_orders["unit_price"],
        errors="coerce"
    )

    missing_unit_price = unit_price.isna().sum()
    if missing_unit_price:
        logger.warning(
            "%s unit_price value(s) were missing or invalid and replaced with the median",
            missing_unit_price,
        )

    cleaned_orders["unit_price"] = unit_price.fillna(
        unit_price.median()
    )

    # Convert discount to numeric and report values that need a fallback
    discount = pd.to_numeric(
        cleaned_orders["discount"],
        errors="coerce",
    )

    missing_discount = discount.isna().sum()
    if missing_discount:
        logger.warning(
            "%s discount value(s) were missing or invalid and replaced with 0",
            missing_discount,
        )

    cleaned_orders["discount"] = discount.fillna(0)

    # Convert different return values to True or False
    cleaned_orders["returned"] = (
        cleaned_orders["returned"]
        .fillna("false")
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "1", "yes", "ja"])
    )

    logger.info("Order data cleaning completed")

    return cleaned_orders


def calculate_order_values(orders: pd.DataFrame) -> pd.DataFrame:
    # Work on a copy of the DataFrame to avoid modifying the original data
    calculated_orders = orders.copy()

    # Keep the original calculations for order value and discounted value
    calculated_orders["order_value"] = (
        calculated_orders["quantity"] * calculated_orders["unit_price"]
    )

    calculated_orders["discounted_value"] = (
        calculated_orders["order_value"] * (1 - calculated_orders["discount"])
    )

    logger.info("Order values calculated")

    return calculated_orders