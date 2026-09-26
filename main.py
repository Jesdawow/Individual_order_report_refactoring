import logging
from pathlib import Path

from src.order_report.config import ReportConfig
from src.order_report.loading import load_orders
from src.order_report.processing import clean_orders, calculate_order_values
from src.order_report.reporting import (
    create_overview,
    create_returns_report,
    create_sales_report,
    save_report,
)
from src.order_report.validation import validate_orders


def configure_logging() -> None:
    # Configure logging once at the main entry point of the program
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def main() -> None:
    configure_logging()
    logger = logging.getLogger(__name__)

    # Keep input and output paths together in one configuration object
    config = ReportConfig(
        input_path=Path("data/orders.csv"),
        output_dir=Path("output"),
    )

    logger.info("Starting order report")

    # Load and validate the order data
    orders = load_orders(config.input_path)
    validate_orders(orders)

    # Clean the data and calculate the values used in the reports
    orders = clean_orders(orders)
    orders = calculate_order_values(orders)

    # Create the same reports as the original program
    overview = create_overview(orders)
    sales_by_category = create_sales_report(
        orders,
        "product_category",
    )
    sales_by_region = create_sales_report(
        orders,
        "region"
    )
    returns_by_category = create_returns_report(orders)

    # Save all reports to the configured output folder
    save_report(
        overview,
        config.output_dir,
        "overview.csv",
    )
    save_report(
        sales_by_category,
        config.output_dir,
        "sales_by_category.csv",
    )
    save_report(
        sales_by_region,
        config.output_dir,
        "sales_by_region.csv",
    )
    save_report(
        returns_by_category,
        config.output_dir,
        "returns_by_category.csv",
    )

    logger.info("Order report completed successfully")


if __name__ == "__main__":
    main()