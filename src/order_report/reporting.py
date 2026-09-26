import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def create_overview(orders: pd.DataFrame) -> pd.DataFrame:
    # Create the same overall metrics as in the original code
    total_sales = round(orders["discounted_value"].sum(), 2)
    order_count = orders["order_id"].nunique()
    return_count = int(orders["returned"].sum())

    overview = pd.DataFrame(
        {
            "metric": [
                "total_sales",
                "order_count",
                "return_count",
            ],
            "value": [
                total_sales,
                order_count,
                return_count,
            ],
        }
    )

    logger.info("Overview report created")

    return overview


def create_sales_report(orders: pd.DataFrame, group_by: str) -> pd.DataFrame:
    # Use the same report logic for both product category and region
    report = (
        orders.groupby(group_by, as_index=False)
        .agg(
            order_count=("order_id", "nunique"),
            total_sales=("discounted_value", "sum"),
            returns=("returned", "sum"),
        )
    )

    report["total_sales"] = report["total_sales"].round(2)

    report["return_rate"] = (
        report["returns"] / report["order_count"]
    ).round(3)

    report = (
        report.sort_values(
            "total_sales",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    logger.info("Sales report created for %s", group_by)

    return report


def create_returns_report(orders: pd.DataFrame) -> pd.DataFrame:
    # Create the return summary per product category
    report = (
        orders.groupby("product_category", as_index=False)
        .agg(
            order_count=("order_id", "nunique"),
            returns=("returned", "sum"),
        )
    )

    report["return_rate"] = (
        report["returns"] / report["order_count"]
    ).round(3)

    report = (
        report.sort_values(
            "return_rate",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    logger.info("Returns report created")

    return report


def save_report(report: pd.DataFrame, output_dir: Path, filename: str) -> None:
    # Create the output folder if it does not already exist
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / filename
    report.to_csv(output_path, index=False)

    logger.info("Saved report to %s", output_path)