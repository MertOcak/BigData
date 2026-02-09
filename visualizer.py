# -*- coding: utf-8 -*-
"""
Visualization module — charts and HTML report.
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

if HAS_PLOT:
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.facecolor"] = "#f8f9fa"
    plt.rcParams["figure.facecolor"] = "white"
    sns.set_style("whitegrid")
    sns.set_palette("husl")

PALET_CANLI = ["#667eea", "#764ba2", "#f093fb", "#4facfe", "#00f2fe", "#43e97b"]


def _ensure_output_dir(output_dir: str) -> Path:
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def _safe_filename(name: str) -> str:
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in name)


def plot_correlation_heatmap(df: pd.DataFrame, output_path: str = "output") -> str | None:
    """Correlation heatmap."""
    if not HAS_PLOT:
        return None
    numeric = df.select_dtypes(include=[np.number])
    if len(numeric.columns) < 2:
        return None
    out = _ensure_output_dir(output_path)
    fig, ax = plt.subplots(figsize=(10, 8))
    corr = numeric.corr()
    sns.heatmap(
        corr, annot=True, fmt=".2f", cmap="RdYlBu_r", center=0,
        ax=ax, square=True, linewidths=0.5, cbar_kws={"shrink": 0.8},
        vmin=-1, vmax=1, annot_kws={"size": 9}
    )
    ax.set_title("Correlation Matrix", fontsize=14, fontweight="bold")
    plt.tight_layout()
    filepath = out / "correlation_heatmap.png"
    plt.savefig(filepath, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    return str(filepath)


def plot_distribution(df: pd.DataFrame, column: str, output_path: str = "output") -> str | None:
    """Distribution histogram with gradient fill."""
    if not HAS_PLOT or column not in df.columns:
        return None
    if not pd.api.types.is_numeric_dtype(df[column]):
        return None
    out = _ensure_output_dir(output_path)
    data = df[column].dropna()
    if data.empty:
        return None
    fig, ax = plt.subplots(figsize=(9, 5))
    n, bins, patches = ax.hist(data, bins=min(40, len(data.unique()) or 20), edgecolor="white", linewidth=0.5)
    for i, p in enumerate(patches):
        p.set_facecolor(plt.cm.viridis(i / max(len(patches), 1)))
    ax.set_title(f"Distribution: {column}", fontsize=13, fontweight="bold")
    ax.set_xlabel(column)
    ax.set_ylabel("Frequency")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    filepath = out / f"distribution_{_safe_filename(column)}.png"
    plt.savefig(filepath, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    return str(filepath)


def plot_value_counts(df: pd.DataFrame, column: str, top_n: int = 15, output_path: str = "output") -> str | None:
    """Value counts — horizontal bar chart."""
    if not HAS_PLOT or column not in df.columns:
        return None
    out = _ensure_output_dir(output_path)
    counts = df[column].value_counts().head(top_n)
    if counts.empty:
        return None
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.Spectral(np.linspace(0.2, 0.9, len(counts)))
    ax.barh(range(len(counts)), counts.values, color=colors, edgecolor="white", linewidth=0.5)
    ax.set_yticks(range(len(counts)))
    ax.set_yticklabels(counts.index, fontsize=9)
    ax.invert_yaxis()
    ax.set_title(f"Top Values: {column} (Top {top_n})", fontsize=13, fontweight="bold")
    ax.set_xlabel("Count")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    filepath = out / f"value_counts_{_safe_filename(column)}.png"
    plt.savefig(filepath, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    return str(filepath)


def plot_scatter(df: pd.DataFrame, col_x: str, col_y: str, output_path: str = "output") -> str | None:
    """Scatter plot for two numeric columns."""
    if not HAS_PLOT or col_x not in df.columns or col_y not in df.columns:
        return None
    if not pd.api.types.is_numeric_dtype(df[col_x]) or not pd.api.types.is_numeric_dtype(df[col_y]):
        return None
    out = _ensure_output_dir(output_path)
    data = df[[col_x, col_y]].dropna()
    if len(data) < 2:
        return None
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(data[col_x], data[col_y], alpha=0.4, c=data[col_y], cmap="plasma", s=20, edgecolors="none")
    ax.set_title(f"{col_x} vs {col_y}", fontsize=13, fontweight="bold")
    ax.set_xlabel(col_x)
    ax.set_ylabel(col_y)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    filepath = out / f"scatter_{_safe_filename(col_x)}_vs_{_safe_filename(col_y)}.png"
    plt.savefig(filepath, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    return str(filepath)


def plot_box(df: pd.DataFrame, column: str, output_path: str = "output") -> str | None:
    """Box plot for a numeric column."""
    if not HAS_PLOT or column not in df.columns:
        return None
    if not pd.api.types.is_numeric_dtype(df[column]):
        return None
    out = _ensure_output_dir(output_path)
    data = df[column].dropna()
    if data.empty:
        return None
    fig, ax = plt.subplots(figsize=(8, 5))
    bp = ax.boxplot([data], patch_artist=True, vert=True)
    bp["boxes"][0].set_facecolor("#4facfe")
    bp["boxes"][0].set_alpha(0.7)
    ax.set_ylabel(column)
    ax.set_title(f"Box Plot: {column}", fontsize=13, fontweight="bold")
    ax.set_xticklabels([column])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    filepath = out / f"box_{_safe_filename(column)}.png"
    plt.savefig(filepath, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    return str(filepath)


def plot_missing_values(df: pd.DataFrame, output_path: str = "output") -> str | None:
    """Missing values per column."""
    if not HAS_PLOT:
        return None
    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=True)
    if missing.empty:
        return None
    out = _ensure_output_dir(output_path)
    fig, ax = plt.subplots(figsize=(8, max(4, len(missing) * 0.35)))
    colors = plt.cm.Reds(np.linspace(0.4, 0.9, len(missing)))
    missing.plot(kind="barh", ax=ax, color=colors, edgecolor="white")
    ax.set_title("Missing Values by Column", fontsize=13, fontweight="bold")
    ax.set_xlabel("Missing Count")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    filepath = out / "missing_values.png"
    plt.savefig(filepath, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    return str(filepath)


def plot_dashboard(df: pd.DataFrame, numeric_cols: list, output_path: str = "output") -> str | None:
    """Single-page dashboard: correlation + 2 distributions + 1 value counts."""
    if not HAS_PLOT:
        return None
    out = _ensure_output_dir(output_path)
    n_num = len(numeric_cols)
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    fig = plt.figure(figsize=(14, 10))
    fig.suptitle("Big Data Analysis — Summary Dashboard", fontsize=16, fontweight="bold", y=1.02)

    if n_num >= 2:
        ax1 = fig.add_subplot(2, 2, 1)
        corr = df[numeric_cols].corr()
        sns.heatmap(corr, annot=True, fmt=".1f", cmap="coolwarm", center=0, ax=ax1, square=True, cbar_kws={"shrink": 0.7})
        ax1.set_title("Correlation")
    for i, col in enumerate(numeric_cols[:2]):
        ax = fig.add_subplot(2, 2, 2 + i)
        df[col].dropna().hist(ax=ax, bins=25, color=PALET_CANLI[i % len(PALET_CANLI)], edgecolor="white")
        ax.set_title(f"Distribution: {col}")
        ax.set_xlabel(col)
    if cat_cols:
        ax4 = fig.add_subplot(2, 2, 4)
        counts = df[cat_cols[0]].value_counts().head(10)
        counts.plot(kind="barh", ax=ax4, color=plt.cm.Paired(np.linspace(0, 1, len(counts))))
        ax4.set_title(f"Top: {cat_cols[0]}")
        ax4.invert_yaxis()
    else:
        ax4 = fig.add_subplot(2, 2, 4)
        ax4.text(0.5, 0.5, "No categorical columns", ha="center", va="center", transform=ax4.transAxes)
        ax4.set_axis_off()

    plt.tight_layout()
    filepath = out / "dashboard_summary.png"
    plt.savefig(filepath, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    return str(filepath)


def generate_all_plots(analyzer, output_path: str = "output") -> list[str]:
    """Generate all charts."""
    df = analyzer.get_dataframe()
    numeric_cols = analyzer.numeric_cols
    categorical_cols = analyzer.categorical_cols
    generated = []

    if len(numeric_cols) >= 2:
        p = plot_correlation_heatmap(df, output_path)
        if p:
            generated.append(p)
        p = plot_dashboard(df, numeric_cols, output_path)
        if p:
            generated.append(p)
        p = plot_scatter(df, numeric_cols[0], numeric_cols[1], output_path)
        if p:
            generated.append(p)

    for col in numeric_cols[:6]:
        p = plot_distribution(df, col, output_path)
        if p:
            generated.append(p)
        p = plot_box(df, col, output_path)
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


def generate_html_report(
    output_path: str,
    plot_files: list[str],
    ai_insight: str | None = None,
    title: str = "Big Data Analysis Report",
) -> str | None:
    """Build HTML report with all charts and optional AI summary."""
    out = Path(output_path)
    out.mkdir(parents=True, exist_ok=True)
    plot_files = [Path(p) for p in plot_files if Path(p).exists()]
    rel_paths = [p.name for p in plot_files if p.parent == out]

    ai_block = ""
    if ai_insight:
        ai_block = f"""
        <section class="ai-section">
            <h2>AI Summary</h2>
            <div class="ai-content">{ai_insight.replace(chr(10), "<br>")}</div>
        </section>
        """

    images_html = "\n".join(
        f'<div class="chart"><img src="{name}" alt="{name}"/><p>{name}</p></div>' for name in rel_paths
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', system-ui, sans-serif; margin: 0; padding: 24px; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); color: #e4e4e7; min-height: 100vh; }}
        h1 {{ text-align: center; font-size: 2rem; margin-bottom: 8px; background: linear-gradient(90deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
        .subtitle {{ text-align: center; color: #a1a1aa; margin-bottom: 32px; }}
        .ai-section {{ background: rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; margin-bottom: 32px; border: 1px solid rgba(255,255,255,0.1); }}
        .ai-section h2 {{ margin-top: 0; color: #a78bfa; }}
        .ai-content {{ line-height: 1.7; color: #d4d4d8; }}
        .charts {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(420px, 1fr)); gap: 24px; }}
        .chart {{ background: rgba(255,255,255,0.06); border-radius: 12px; overflow: hidden; border: 1px solid rgba(255,255,255,0.08); }}
        .chart img {{ width: 100%; height: auto; display: block; }}
        .chart p {{ margin: 0; padding: 12px; font-size: 0.85rem; color: #a1a1aa; }}
        footer {{ text-align: center; margin-top: 48px; color: #71717a; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p class="subtitle">Charts and visual summary</p>
    {ai_block}
    <section class="charts">{images_html}</section>
    <footer>Big Data Analysis — Generated automatically</footer>
</body>
</html>
"""
    report_path = out / "report.html"
    report_path.write_text(html, encoding="utf-8")
    return str(report_path)
