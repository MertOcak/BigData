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

Yapay zeka özetini kapatmak için (varsayılan: açık, API anahtarı varsa):

```bash
python main.py "veri.csv" --no-ai
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
3. **Yapay zeka özeti** (opsiyonel): `OPENAI_API_KEY` tanımlıysa veriye dair Türkçe yorum ve öneri üretir (OpenAI API kullanır).
4. **Sayısal istatistikler**: Min, max, ortalama, standart sapma, çeyrekler (describe).
5. **Kategorik özet**: Benzersiz değer sayıları, en sık değerler.
6. **Korelasyon matrisi**: Sayısal sütunlar arası korelasyon.
7. **Gelişmiş grafikler** (varsayılan: `output` klasörü):
   - Korelasyon ısı haritası ve özet dashboard
   - Dağılım (histogram), kutu grafiği (box plot), scatter (iki sayısal sütun)
   - Değer sayıları (renkli çubuk grafikler), eksik değer görselleştirmesi
8. **HTML rapor**: Tüm grafiklerin ve AI özetinin toplandığı `output/rapor.html` (tarayıcıda açılır).
9. **Örnek veri**: İlk 10.000 satır `output/veri_ornegi_ilk_10000.csv` olarak kaydedilir.

### Yapay zeka özeti için

Ortam değişkeni olarak OpenAI API anahtarınızı tanımlayın (isteğe bağlı):

```bash
# Windows (PowerShell)
$env:OPENAI_API_KEY = "sk-..."

# Linux / macOS
export OPENAI_API_KEY="sk-..."
```

Anahtar yoksa uygulama AI özetini atlar; grafikler ve diğer analizler normal çalışır.

## Proje yapısı

| Dosya | Açıklama |
|-------|----------|
| `main.py` | Ana uygulama ve CLI |
| `data_loader.py` | Dosyadan veri yükleme (CSV, Excel, JSON, Parquet) |
| `analyzer.py` | İstatistik ve özet hesaplama |
| `visualizer.py` | Gelişmiş grafikler ve HTML rapor |
| `ai_insights.py` | Yapay zeka özeti (OpenAI API, opsiyonel) |
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
