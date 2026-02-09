# -*- coding: utf-8 -*-
"""
Görselleştirme modülü - grafik ve rapor çıktıları.
"""

import pandas as pd
import numpy as np
from pathlib import Path

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import seaborn as sns
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False

# Türkçe karakter ve görsel ayarları
if HAS_PLOT:
    plt.rcParams["font.family"] = "DejaVu Sans"
    sns.set_style("whitegrid")


def _ensure_output_dir(output_dir: str) -> Path:
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def plot_correlation_heatmap(df: pd.DataFrame, output_path: str = "output") -> str | None:
    """Sayısal sütunlar için korelasyon ısı haritası."""
    if not HAS_PLOT:
        return None
    numeric = df.select_dtypes(include=[np.number])
    if len(numeric.columns) < 2:
        return None
    out = _ensure_output_dir(output_path)
    fig, ax = plt.subplots(figsize=(10, 8))
    corr = numeric.corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax, square=True)
    plt.title("Korelasyon Matrisi")
    plt.tight_layout()
    filepath = out / "korelasyon_haritasi.png"
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()
    return str(filepath)


def plot_distribution(df: pd.DataFrame, column: str, output_path: str = "output") -> str | None:
    """Tek sayısal sütunun dağılım grafiği (histogram)."""
    if not HAS_PLOT or column not in df.columns:
        return None
    if df[column].dtype not in (np.number, "int64", "float64"):
        return None
    out = _ensure_output_dir(output_path)
    fig, ax = plt.subplots(figsize=(8, 5))
    df[column].dropna().hist(ax=ax, bins=min(50, len(df[column].dropna().unique()) or 20), edgecolor="black", alpha=0.7)
    ax.set_title(f'Dağılım: {column}')
    ax.set_xlabel(column)
    ax.set_ylabel("Frekans")
    plt.tight_layout()
    safe_name = "".join(c if c.isalnum() or c in "._-" else "_" for c in column)
    filepath = out / f"dagilim_{safe_name}.png"
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()
    return str(filepath)


def plot_value_counts(df: pd.DataFrame, column: str, top_n: int = 15, output_path: str = "output") -> str | None:
    """Kategorik veya sayısal sütunun değer sayıları çubuk grafiği."""
    if not HAS_PLOT or column not in df.columns:
        return None
    out = _ensure_output_dir(output_path)
    counts = df[column].value_counts().head(top_n)
    if counts.empty:
        return None
    fig, ax = plt.subplots(figsize=(10, 6))
    counts.plot(kind="barh", ax=ax, color="steelblue", edgecolor="black", alpha=0.8)
    ax.set_title(f'En Sık Değerler: {column} (İlk {top_n})')
    ax.set_xlabel("Adet")
    ax.set_ylabel(column)
    plt.tight_layout()
    safe_name = "".join(c if c.isalnum() or c in "._-" else "_" for c in column)
    filepath = out / f"deger_sayilari_{safe_name}.png"
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()
    return str(filepath)


def plot_missing_values(df: pd.DataFrame, output_path: str = "output") -> str | None:
    """Eksik değerlerin sütun bazlı görselleştirmesi."""
    if not HAS_PLOT:
        return None
    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=True)
    if missing.empty:
        return None
    out = _ensure_output_dir(output_path)
    fig, ax = plt.subplots(figsize=(8, max(4, len(missing) * 0.3)))
    missing.plot(kind="barh", ax=ax, color="coral", alpha=0.8)
    ax.set_title("Eksik Değer Sayıları (Sütun Bazlı)")
    ax.set_xlabel("Eksik Adet")
    plt.tight_layout()
    filepath = out / "eksik_degerler.png"
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()
    return str(filepath)


def generate_all_plots(analyzer, output_path: str = "output") -> list[str]:
    """Mevcut veri seti için tüm uygun grafikleri üretir."""
    df = analyzer.get_dataframe()
    numeric_cols = analyzer.numeric_cols
    categorical_cols = analyzer.categorical_cols
    generated = []
    
    if len(numeric_cols) >= 2:
        p = plot_correlation_heatmap(df, output_path)
        if p:
            generated.append(p)
    
    for col in numeric_cols[:6]:  # En fazla 6 sayısal sütun
        p = plot_distribution(df, col, output_path)
        if p:
            generated.append(p)
    
    for col in (categorical_cols + numeric_cols)[:5]:
        p = plot_value_counts(df, col, top_n=15, output_path=output_path)
        if p:
            generated.append(p)
    
    p = plot_missing_values(df, output_path)
    if p:
        generated.append(p)
    
    return generated
