from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class ReportConfig:
    """
    Configuration for the order report generation.
    """
    input_path: Path
    output_dir: Path