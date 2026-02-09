# -*- coding: utf-8 -*-
"""
Veri yükleme modülü - CSV, Excel, JSON dosyalarını destekler.
"""

import pandas as pd
from pathlib import Path


def load_data(file_path: str, **kwargs) -> pd.DataFrame:
    """
    Dosya uzantısına göre veriyi yükler.
    
    Desteklenen formatlar: .csv, .xlsx, .xls, .json, .parquet
    
    Args:
        file_path: Dosya yolu
        **kwargs: Pandas read fonksiyonuna geçirilecek ek parametreler
        
    Returns:
        pandas DataFrame
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Dosya bulunamadı: {file_path}")
    
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
        # Varsayılan: CSV olarak dene
        try:
            return pd.read_csv(file_path, encoding="utf-8", **kwargs)
        except Exception:
            raise ValueError(
                f"Desteklenmeyen format: {suffix}. "
                "Desteklenen: .csv, .xlsx, .xls, .json, .parquet"
            )
