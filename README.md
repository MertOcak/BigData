# Big Data Analiz Uygulaması

Verdiğiniz veri dosyasını (CSV, Excel, JSON, Parquet) yükleyip istatistiksel analiz yapan ve grafikler üreten Python uygulaması.

## Kurulum

```bash
git clone https://github.com/KULLANICI_ADINIZ/BigData.git
cd BigData
pip install -r requirements.txt
```

> **Not:** `KULLANICI_ADINIZ` yerine kendi GitHub kullanıcı adınızı yazın.

## Kullanım

### Komut satırından (dosya yolu vererek)

```bash
python main.py "C:\veriler\satis.csv"
```

Çıktıları farklı bir klasöre yazmak için:

```bash
python main.py "veri.csv" -o raporlar
```

Grafik oluşturmadan sadece sayısal analiz:

```bash
python main.py "veri.csv" --no-plots
```

### Etkileşimli mod

Dosya yolu vermeden çalıştırırsanız uygulama dosya yolunu sizden ister:

```bash
python main.py
```

## Desteklenen dosya formatları

| Format   | Uzantı    |
|----------|-----------|
| CSV      | `.csv`    |
| Excel    | `.xlsx`, `.xls` |
| JSON     | `.json`   |
| Parquet  | `.parquet` |

## Ne yapar?

1. **Veri yükleme**: Dosyayı otomatik format algılayarak yükler.
2. **Genel özet**: Satır/sütun sayısı, sayısal/kategorik sütunlar, eksik değerler, bellek kullanımı.
3. **Sayısal istatistikler**: Min, max, ortalama, standart sapma, çeyrekler (describe).
4. **Kategorik özet**: Benzersiz değer sayıları, en sık değerler.
5. **Korelasyon matrisi**: Sayısal sütunlar arası korelasyon.
6. **Grafikler** (varsayılan olarak `output` klasörüne):
   - Korelasyon ısı haritası
   - Sayısal sütunların dağılım grafikleri
   - Sütun bazlı değer sayıları (çubuk grafik)
   - Eksik değer görselleştirmesi
7. **Örnek veri**: İlk 10.000 satır `output/veri_ornegi_ilk_10000.csv` olarak kaydedilir.

## Proje yapısı

| Dosya | Açıklama |
|-------|----------|
| `main.py` | Ana uygulama ve CLI |
| `data_loader.py` | Dosyadan veri yükleme (CSV, Excel, JSON, Parquet) |
| `analyzer.py` | İstatistik ve özet hesaplama |
| `visualizer.py` | Grafik üretimi (matplotlib, seaborn) |
| `generate_sample_data.py` | Örnek 10.000 satır rastgele veri üretir |
| `requirements.txt` | Python bağımlılıkları |
| `ornek_veri.csv` | Örnek veri (isteğe bağlı; script ile de üretilebilir) |

## Örnek veri ile test

10.000 satırlık örnek veri yoksa önce üretin:

```bash
python generate_sample_data.py
```

Ardından analizi çalıştırın:

```bash
python main.py ornek_veri.csv
```

Sonuçlar konsola yazılır, grafikler ve örnek export `output/` klasörüne kaydedilir.

## Lisans

MIT License — detaylar için [LICENSE](LICENSE) dosyasına bakın.
