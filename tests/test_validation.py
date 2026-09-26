import pandas as pd
import pytest

from src.order_report.validation import validate_orders


def create_valid_orders() -> pd.DataFrame:
    # Small valid DataFrame used as a base for the validation tests
    return pd.DataFrame(
        {
            "order_id": ["O0001"],
            "order_date": ["2026-01-01"],
            "customer_id": ["C018"],
            "region": ["North"],
            "product_category": ["Electronics"],
            "quantity": [2],
            "unit_price": [100.0],
            "discount": [0.1],
            "returned": ["false"],
        }
    )


def test_valid_orders_pass_validation() -> None:
    # Normal case: valid data should pass without raising an error
    orders = create_valid_orders()

    validate_orders(orders)


def test_empty_orders_raise_value_error() -> None:
    # Empty input should be rejected
    orders = pd.DataFrame()

    with pytest.raises(ValueError, match="Order data is empty"):
        validate_orders(orders)


def test_missing_required_column_raises_value_error() -> None:
    # Remove one required column to test the column validation
    orders = create_valid_orders().drop(columns=["quantity"])

    with pytest.raises(ValueError, match="quantity"):
        validate_orders(orders)


def test_negative_quantity_raises_value_error() -> None:
    # Negative quantity is an unreasonable value and should be rejected
    orders = create_valid_orders()
    orders.loc[0, "quantity"] = -1

    with pytest.raises(ValueError, match="negative values"):
        validate_orders(orders)


def test_negative_unit_price_raises_value_error() -> None:
    # Negative unit price should be rejected
    orders = create_valid_orders()
    orders.loc[0, "unit_price"] = -50

    with pytest.raises(ValueError, match="negative values"):
        validate_orders(orders)


def test_discount_outside_valid_range_raises_value_error() -> None:
    # Discount should be between 0 and 1
    orders = create_valid_orders()
    orders.loc[0, "discount"] = 1.5

    with pytest.raises(ValueError, match="outside the range"):
        validate_orders(orders)