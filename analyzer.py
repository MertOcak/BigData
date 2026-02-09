# -*- coding: utf-8 -*-
"""
Big Data analysis module — statistics, summary, and data inspection.
"""

import pandas as pd
import numpy as np


class DataAnalyzer:
    """Analyzes a dataset and provides summary statistics."""

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    def summary(self) -> dict:
        """Return basic summary statistics."""
        return {
            "row_count": len(self.df),
            "column_count": len(self.df.columns),
            "columns": self.df.columns.tolist(),
            "numeric_columns": self.numeric_cols,
            "categorical_columns": self.categorical_cols,
            "missing_values": self.df.isnull().sum().to_dict(),
            "memory_usage_mb": self.df.memory_usage(deep=True).sum() / 1024 / 1024,
        }

    def describe_numeric(self) -> pd.DataFrame:
        """Describe numeric columns (min, max, mean, std, quartiles)."""
        if not self.numeric_cols:
            return pd.DataFrame()
        return self.df[self.numeric_cols].describe()

    def describe_categorical(self) -> pd.DataFrame:
        """Unique counts and most frequent values for categorical columns."""
        if not self.categorical_cols:
            return pd.DataFrame()
        result = []
        for col in self.categorical_cols:
            result.append({
                "column": col,
                "unique_count": self.df[col].nunique(),
                "most_frequent": self.df[col].mode().iloc[0] if len(self.df[col].dropna()) > 0 else None,
                "missing_count": self.df[col].isnull().sum(),
            })
        return pd.DataFrame(result)

    def correlation_matrix(self) -> pd.DataFrame:
        """Correlation matrix for numeric columns."""
        if len(self.numeric_cols) < 2:
            return pd.DataFrame()
        return self.df[self.numeric_cols].corr()

    def value_counts_summary(self, column: str, top_n: int = 10) -> pd.Series:
        """Value distribution for a column (top N values)."""
        if column not in self.df.columns:
            raise ValueError(f"Column not found: {column}")
        return self.df[column].value_counts().head(top_n)

    def get_dataframe(self) -> pd.DataFrame:
        """Return the raw DataFrame."""
        return self.df
