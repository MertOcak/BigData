# -*- coding: utf-8 -*-
"""
Data loader module — supports CSV, Excel, JSON, and Parquet.
"""

import pandas as pd
from pathlib import Path


def load_data(file_path: str, **kwargs) -> pd.DataFrame:
    """
    Load data based on file extension.

    Supported formats: .csv, .xlsx, .xls, .json, .parquet

    Args:
        file_path: Path to the file
        **kwargs: Additional arguments passed to the pandas read function

    Returns:
        pandas DataFrame
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = path.suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(file_path, encoding="utf-8", **kwargs)
    elif suffix in (".xlsx", ".xls"):
        return pd.read_excel(file_path, **kwargs)
    elif suffix == ".json":
        return pd.read_json(file_path, **kwargs)
    elif suffix == ".parquet":
        return pd.read_parquet(file_path, **kwargs)
    else:
        try:
            return pd.read_csv(file_path, encoding="utf-8", **kwargs)
        except Exception:
            raise ValueError(
                f"Unsupported format: {suffix}. "
                "Supported: .csv, .xlsx, .xls, .json, .parquet"
            )
