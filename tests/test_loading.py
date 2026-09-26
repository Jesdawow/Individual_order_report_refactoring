from pathlib import Path

import pandas as pd
import pytest

from src.order_report.loading import load_orders


def test_load_orders_reads_csv(tmp_path: Path) -> None:
    # Create a small temporary CSV file for the test
    file_path = tmp_path / "orders.csv"

    pd.DataFrame(
        {
            "order_id": [1, 2],
            "quantity": [1, 3],
        }
    ).to_csv(file_path, index=False)

    orders = load_orders(file_path)

    assert len(orders) == 2
    assert list(orders.columns) == ["order_id", "quantity"]


def test_load_orders_missing_file_raises_error(tmp_path: Path) -> None:
    # A missing input file should raise a clear FileNotFoundError
    file_path = tmp_path / "missing_orders.csv"

    with pytest.raises(FileNotFoundError, match="Order file not found"):
        load_orders(file_path)