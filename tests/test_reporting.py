import pandas as pd

from src.order_report.reporting import (
    create_overview,
    create_returns_report,
    create_sales_report,
)


def create_report_data() -> pd.DataFrame:
    # A small processed dataset used as a base for the reporting tests
    return pd.DataFrame(
        {
            "order_id": ["O0001", "O0002", "O0003"],
            "product_category": ["Books", "Books", "Electronics"],
            "region": ["North", "North", "South"],
            "discounted_value": [100.0, 200.0, 300.0],
            "returned": [False, True, True],
        }
    )


def test_create_overview_calculates_correct_values() -> None:
    # The overview should contain the main totals from the order data
    orders = create_report_data()

    overview = create_overview(orders)

    values = dict(zip(overview["metric"], overview["value"]))

    assert values["total_sales"] == 600.0
    assert values["order_count"] == 3
    assert values["return_count"] == 2


def test_create_sales_report_groups_by_category() -> None:
    # The sales report should summarize orders by product category
    orders = create_report_data()

    report = create_sales_report(
        orders,
        "product_category",
    )

    books = report[report["product_category"] == "Books"].iloc[0]

    assert books["order_count"] == 2
    assert books["total_sales"] == 300.0
    assert books["returns"] == 1
    assert books["return_rate"] == 0.5


def test_create_returns_report_calculates_return_rate() -> None:
    # Returns report should calculate return rates per category
    orders = create_report_data()

    report = create_returns_report(orders)

    electronics = report[
        report["product_category"] == "Electronics"
    ].iloc[0]

    assert electronics["order_count"] == 1
    assert electronics["returns"] == 1
    assert electronics["return_rate"] == 1.0