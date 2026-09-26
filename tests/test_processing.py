import pandas as pd

from src.order_report.processing import clean_orders, calculate_order_values


def test_clean_orders_normalizes_text_columns() -> None:
    # Text values should be cleaned in the same way as in the original program
    orders = pd.DataFrame(
        {
            "region": [" north "],
            "product_category": ["electronics "],
            "quantity": [2],
            "unit_price": [100.0],
            "discount": [0.1],
            "returned": ["Yes"],
        }
    )

    cleaned = clean_orders(orders)

    assert cleaned.loc[0, "region"] == "North"
    assert cleaned.loc[0, "product_category"] == "Electronics"
    assert bool(cleaned.loc[0, "returned"]) is True


def test_clean_orders_replaces_missing_numeric_values() -> None:
    # Missing or invalid numeric values should use the same fallback rules
    orders = pd.DataFrame(
        {
            "region": ["North", "South"],
            "product_category": ["Books", "Sports"],
            "quantity": [None, 2],
            "unit_price": [100.0, None],
            "discount": ["unknown", 0.2],
            "returned": ["false", "true"],
        }
    )

    cleaned = clean_orders(orders)

    assert cleaned.loc[0, "quantity"] == 1
    assert cleaned.loc[1, "unit_price"] == 100.0
    assert cleaned.loc[0, "discount"] == 0


def test_calculate_order_values() -> None:
    # Check the two main calculations used by the reports
    orders = pd.DataFrame(
        {
            "quantity": [2],
            "unit_price": [100.0],
            "discount": [0.25],
        }
    )

    result = calculate_order_values(orders)

    assert result.loc[0, "order_value"] == 200.0
    assert result.loc[0, "discounted_value"] == 150.0