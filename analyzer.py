# -*- coding: utf-8 -*-
"""
Big Data analiz modülü - istatistik, özet ve görselleştirme.
"""

import pandas as pd
import numpy as np
from pathlib import Path


class DataAnalyzer:
    """Veri seti üzerinde analiz işlemleri yapan sınıf."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    
    def summary(self) -> dict:
        """Temel özet istatistikleri döndürür."""
        return {
            "satır_sayısı": len(self.df),
            "sütun_sayısı": len(self.df.columns),
            "sütunlar": self.df.columns.tolist(),
            "sayısal_sütunlar": self.numeric_cols,
            "kategorik_sütunlar": self.categorical_cols,
            "eksik_değerler": self.df.isnull().sum().to_dict(),
            "bellek_kullanımı_mb": self.df.memory_usage(deep=True).sum() / 1024 / 1024,
        }
    
    def describe_numeric(self) -> pd.DataFrame:
        """Sayısal sütunlar için describe (min, max, ortalama, std, çeyrekler)."""
        if not self.numeric_cols:
            return pd.DataFrame()
        return self.df[self.numeric_cols].describe()
    
    def describe_categorical(self) -> pd.DataFrame:
        """Kategorik sütunlar için benzersiz değer sayıları ve en sık değerler."""
        if not self.categorical_cols:
            return pd.DataFrame()
        result = []
        for col in self.categorical_cols:
            result.append({
                "sütun": col,
                "benzersiz_sayı": self.df[col].nunique(),
                "en_sık": self.df[col].mode().iloc[0] if len(self.df[col].dropna()) > 0 else None,
                "eksik_sayı": self.df[col].isnull().sum(),
            })
        return pd.DataFrame(result)
    
    def correlation_matrix(self) -> pd.DataFrame:
        """Sayısal sütunlar arası korelasyon matrisi."""
        if len(self.numeric_cols) < 2:
            return pd.DataFrame()
        return self.df[self.numeric_cols].corr()
    
    def value_counts_summary(self, column: str, top_n: int = 10) -> pd.Series:
        """Belirtilen sütunun değer dağılımı (en sık N değer)."""
        if column not in self.df.columns:
            raise ValueError(f"Sütun bulunamadı: {column}")
        return self.df[column].value_counts().head(top_n)
    
    def get_dataframe(self) -> pd.DataFrame:
        """Ham DataFrame'i döndürür."""
        return self.df
