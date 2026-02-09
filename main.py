# -*- coding: utf-8 -*-
"""
Big Data Analysis Application — main entry point.
Loads your data file, runs analysis, and produces summaries and charts.
"""

import argparse
import sys
from pathlib import Path

from data_loader import load_data
from analyzer import DataAnalyzer
from visualizer import generate_all_plots, generate_html_report, HAS_PLOT

try:
    from ai_insights import generate_insights
    HAS_AI = True
except ImportError:
    HAS_AI = False
    generate_insights = None


def print_section(title: str):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def run_analysis(file_path: str, output_dir: str = "output", no_plots: bool = False, use_ai: bool = True):
    """Load the file, run analysis, and print results."""
    print_section("BIG DATA ANALYSIS")
    print(f"File: {file_path}")
    print(f"Output folder: {output_dir}")

    # Load data
    print_section("DATA LOADING")
    try:
        df = load_data(file_path)
        print(f"Loaded: {len(df):,} rows, {len(df.columns)} columns")
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Load error: {e}", file=sys.stderr)
        sys.exit(1)

    analyzer = DataAnalyzer(df)

    # Overview
    print_section("OVERVIEW")
    summary = analyzer.summary()
    for key, value in summary.items():
        if key == "missing_values":
            missing = {k: v for k, v in value.items() if v > 0}
            if missing:
                print(f"  Missing values: {missing}")
            else:
                print("  Missing values: None")
        elif key != "columns":
            print(f"  {key}: {value}")

    # Numeric summary
    print_section("NUMERIC COLUMNS — STATISTICS")
    desc_num = analyzer.describe_numeric()
    if not desc_num.empty:
        print(desc_num.to_string())
    else:
        print("  No numeric columns.")

    # Categorical summary
    print_section("CATEGORICAL COLUMNS — SUMMARY")
    desc_cat = analyzer.describe_categorical()
    if not desc_cat.empty:
        print(desc_cat.to_string())
    else:
        print("  No categorical columns.")

    # Correlation
    if len(analyzer.numeric_cols) >= 2:
        print_section("CORRELATION MATRIX")
        print(analyzer.correlation_matrix().to_string())

    # AI summary (optional)
    ai_insight_text = None
    if use_ai and HAS_AI and generate_insights:
        print_section("AI SUMMARY")
        try:
            summary = analyzer.summary()
            desc_text = analyzer.describe_numeric().to_string() if not analyzer.describe_numeric().empty else ""
            corr_text = analyzer.correlation_matrix().to_string() if len(analyzer.numeric_cols) >= 2 else ""
            ai_insight_text = generate_insights(summary, desc_text, corr_text)
            if ai_insight_text:
                print(ai_insight_text)
            else:
                print("  (OPENAI_API_KEY not set or API did not respond)")
        except Exception as e:
            print(f"  AI summary skipped: {e}")

    # Charts
    generated = []
    if HAS_PLOT and not no_plots:
        print_section("CHARTS")
        try:
            generated = generate_all_plots(analyzer, output_path=output_dir)
            for path in generated:
                print(f"  {path}")
            report_path = generate_html_report(output_dir, generated, ai_insight=ai_insight_text)
            if report_path:
                print(f"  {report_path}")
        except Exception as e:
            print(f"  Chart error: {e}")
    elif no_plots:
        print_section("CHARTS")
        print("  Charts skipped (--no-plots).")

    # Sample CSV (first 10,000 rows)
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    sample_file = out_path / "sample_first_10000.csv"
    sample = df.head(10000)
    sample.to_csv(sample_file, index=False, encoding="utf-8-sig")
    print_section("OUTPUT FILES")
    print(f"  Sample data (first 10,000 rows): {sample_file}")

    print("\nAnalysis complete.\n")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    parser = argparse.ArgumentParser(
        description="Big Data Analysis: analyze data from your file."
    )
    parser.add_argument(
        "file",
        nargs="?",
        default=None,
        help="Data file to analyze (CSV, Excel, JSON, Parquet)",
    )
    parser.add_argument(
        "-o", "--output",
        default="output",
        help="Output folder for charts and report (default: output)",
    )
    parser.add_argument(
        "--no-plots",
        action="store_true",
        help="Skip generating charts",
    )
    parser.add_argument(
        "--no-ai",
        action="store_true",
        help="Disable AI summary (skipped anyway if OPENAI_API_KEY is not set)",
    )
    args = parser.parse_args()

    if args.file:
        run_analysis(args.file, output_dir=args.output, no_plots=args.no_plots, use_ai=not args.no_ai)
        return

    # Interactive: ask for file path
    print("\nBig Data Analysis Application")
    print("Enter the full path to your data file (or press Enter to exit):")
    file_path = input("File path: ").strip()
    if not file_path:
        print("Exiting.")
        sys.exit(0)
    run_analysis(file_path, output_dir=args.output, no_plots=args.no_plots, use_ai=not args.no_ai)


if __name__ == "__main__":
    main()
