# -*- coding: utf-8 -*-
"""
Big Data Analiz Uygulaması - Ana giriş noktası.
Verdiğiniz dosyadaki verileri yükleyip analiz eder, özet ve grafikler üretir.
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
    """
    Dosyayı yükler, analiz eder ve sonuçları yazar.
    """
    print_section("BIG DATA ANALIZ UYGULAMASI")
    print(f"Dosya: {file_path}")
    print(f"Çıktı klasörü: {output_dir}")

    # Veri yükleme
    print_section("VERİ YÜKLEME")
    try:
        df = load_data(file_path)
        print(f"✓ Yüklendi: {len(df):,} satır, {len(df.columns)} sütun")
    except FileNotFoundError as e:
        print(f"HATA: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Yükleme hatası: {e}", file=sys.stderr)
        sys.exit(1)

    analyzer = DataAnalyzer(df)

    # Genel özet
    print_section("GENEL ÖZET")
    summary = analyzer.summary()
    for key, value in summary.items():
        if key == "eksik_değerler":
            eksik = {k: v for k, v in value.items() if v > 0}
            if eksik:
                print(f"  Eksik değerler: {eksik}")
            else:
                print("  Eksik değer: Yok")
        elif key != "sütunlar":
            print(f"  {key}: {value}")

    # Sayısal özet
    print_section("SAYISAL SÜTUNLAR - İSTATİSTİKLER")
    desc_num = analyzer.describe_numeric()
    if not desc_num.empty:
        print(desc_num.to_string())
    else:
        print("  Sayısal sütun yok.")

    # Kategorik özet
    print_section("KATEGORİK SÜTUNLAR - ÖZET")
    desc_cat = analyzer.describe_categorical()
    if not desc_cat.empty:
        print(desc_cat.to_string())
    else:
        print("  Kategorik sütun yok.")

    # Korelasyon (en az 2 sayısal sütun varsa)
    if len(analyzer.numeric_cols) >= 2:
        print_section("KORELASYON MATRİSİ")
        print(analyzer.correlation_matrix().to_string())

    # Yapay zeka özeti (opsiyonel)
    ai_insight_text = None
    if use_ai and HAS_AI and generate_insights:
        print_section("YAPAY ZEKA ÖZETİ")
        try:
            summary = analyzer.summary()
            desc_text = analyzer.describe_numeric().to_string() if not analyzer.describe_numeric().empty else ""
            corr_text = analyzer.correlation_matrix().to_string() if len(analyzer.numeric_cols) >= 2 else ""
            ai_insight_text = generate_insights(summary, desc_text, corr_text)
            if ai_insight_text:
                print(ai_insight_text)
            else:
                print("  (OPENAI_API_KEY tanımlı değil veya API yanıt vermedi)")
        except Exception as e:
            print(f"  AI özet atlandı: {e}")

    # Grafikler
    generated = []
    if HAS_PLOT and not no_plots:
        print_section("GRAFİKLER")
        try:
            generated = generate_all_plots(analyzer, output_path=output_dir)
            for path in generated:
                print(f"  ✓ {path}")
            # HTML rapor (grafikler + AI özet)
            report_path = generate_html_report(output_dir, generated, ai_insight=ai_insight_text)
            if report_path:
                print(f"  ✓ {report_path}")
        except Exception as e:
            print(f"  Grafik oluşturma hatası: {e}")
    elif no_plots:
        print_section("GRAFİKLER")
        print("  Grafikler atlandı (--no-plots).")

    # Özet CSV (ilk 10.000 satır örnek)
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    sample_file = out_path / "veri_ornegi_ilk_10000.csv"
    sample = df.head(10000)
    sample.to_csv(sample_file, index=False, encoding="utf-8-sig")
    print_section("ÇIKTI DOSYALARI")
    print(f"  Örnek veri (ilk 10.000 satır): {sample_file}")

    print("\nAnaliz tamamlandı.\n")


def main():
    # Windows konsolunda Türkçe çıktı için UTF-8 dene
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    parser = argparse.ArgumentParser(
        description="Big Data Analiz: Verdiğiniz dosyadaki verileri analiz eder."
    )
    parser.add_argument(
        "dosya",
        nargs="?",
        default=None,
        help="Analiz edilecek veri dosyası (CSV, Excel, JSON, Parquet)",
    )
    parser.add_argument(
        "-o", "--output",
        default="output",
        help="Grafik ve rapor çıktılarının klasörü (varsayılan: output)",
    )
    parser.add_argument(
        "--no-plots",
        action="store_true",
        help="Grafik oluşturma",
    )
    parser.add_argument(
        "--no-ai",
        action="store_true",
        help="Yapay zeka özetini kapatır (OPENAI_API_KEY yoksa zaten atlanır)",
    )
    args = parser.parse_args()

    if args.dosya:
        run_analysis(args.dosya, output_dir=args.output, no_plots=args.no_plots, use_ai=not args.no_ai)
        return

    # Etkileşimli: dosya yolu sor
    print("\nBig Data Analiz Uygulaması")
    print("Analiz etmek istediğiniz dosyanın tam yolunu girin (veya çıkmak için Enter):")
    file_path = input("Dosya yolu: ").strip()
    if not file_path:
        print("Çıkılıyor.")
        sys.exit(0)
    run_analysis(file_path, output_dir=args.output, no_plots=args.no_plots, use_ai=not args.no_ai)


if __name__ == "__main__":
    main()
