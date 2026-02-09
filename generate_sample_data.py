# -*- coding: utf-8 -*-
"""ornek_veri.csv için 10.000 satır rastgele veri üretir."""

import random
from datetime import datetime, timedelta

# Orijinal verideki değerler
URUNLER = ["Ürün A", "Ürün B", "Ürün C"]
KATEGORILER = ["Elektronik", "Giyim", "Ev"]
BOLGELER = ["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya", "Adana", "Konya", "Gaziantep"]
# Ürün bazlı fiyat aralıkları (min, max)
URUN_FIYAT = {
    "Ürün A": (250.0, 350.0),
    "Ürün B": (70.0, 120.0),
    "Ürün C": (120.0, 200.0),
}

def random_date(start_year=2026, end_year=2026):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))

def main():
    rows = []
    for _ in range(10000):
        urun = random.choice(URUNLER)
        fiyat_min, fiyat_max = URUN_FIYAT[urun]
        birim_fiyat = round(random.uniform(fiyat_min, fiyat_max), 2)
        tarih = random_date()
        kategori = random.choice(KATEGORILER)
        satis_miktari = random.randint(10, 500)
        bolge = random.choice(BOLGELER)
        rows.append({
            "tarih": tarih.strftime("%Y-%m-%d"),
            "ürün": urun,
            "kategori": kategori,
            "satış_miktarı": satis_miktari,
            "birim_fiyat": birim_fiyat,
            "bölge": bolge,
        })

    with open("ornek_veri.csv", "w", encoding="utf-8-sig", newline="") as f:
        import csv
        w = csv.DictWriter(f, fieldnames=["tarih", "ürün", "kategori", "satış_miktarı", "birim_fiyat", "bölge"])
        w.writeheader()
        w.writerows(rows)

    print("ornek_veri.csv guncellendi: 10.000 satir rastgele veri yazildi.")

if __name__ == "__main__":
    main()
