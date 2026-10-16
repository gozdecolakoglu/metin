# metin
doğal dil işleme

## Projeyi Windows terminalinde çalıştırma

Bu adımları VS Code'da **Terminal > Yeni Terminal** menüsünden açtığınız
PowerShell terminalinde uygulayın. Komutlardaki `iphone_yorumlar.html`,
Amazon'dan kaydedip proje klasörüne koyduğunuz HTML dosyasıdır.

### 1. Proje klasörüne geçin

```powershell
Set-Location -LiteralPath 'C:\karışık\metin'
```

Terminalin proje klasöründe olduğunu kontrol edin:

```powershell
Get-Location
```

### 2. Python ve paketleri hazırlayın

Python komutunun çalıştığını kontrol edin:

```powershell
python --version
```

Gerekli paketleri kurun (ilk kullanımda veya paket hatası alırsanız):

```powershell
python -m pip install -r requirements.txt
```

`python` komutu tanınmazsa ve bu bilgisayardaki Python 3.13 kurulumunu
kullanıyorsanız, sonraki komutlarda `python` yerine şu yolu kullanabilirsiniz:

```powershell
$PY = 'C:\Users\LENOVO\AppData\Local\Programs\Python\Python313\python.exe'
& $PY --version
```

Bu durumda paket kurulumunu `& $PY -m pip install -r requirements.txt`
şeklinde yapın. Aşağıdaki örneklerdeki `python` komutunu da `& $PY` ile
değiştirin.

### Amazon projesinde kullanılan kütüphaneler

Kurulması gereken üçüncü taraf Python paketleri `requirements.txt` dosyasında
listelenmiştir:

| Paket | Python'daki import adı | Kullanım amacı |
|---|---|---|
| `beautifulsoup4` | `bs4` | Kaydedilmiş Amazon HTML sayfasını okuyup yorum, başlık ve yıldız alanlarını bulur. |
| `pandas` | `pandas` | Yorumları tablo olarak işler, CSV dosyalarını okur ve sonuçları CSV'ye yazar. |

İkisini birden proje klasöründe kurmak için:

```powershell
python -m pip install -r requirements.txt
```

İsterseniz ayrı ayrı da kurabilirsiniz:

```powershell
python -m pip install beautifulsoup4 pandas
```

`argparse`, `re`, `pathlib`, `typing` ve `urllib.parse` ise Python'ın standart
kütüphanesindendir; ayrıca kurulmaları gerekmez. Duygu analizi için ayrı bir
makine öğrenmesi paketi kullanılmıyor; sınıflandırma Python kodundaki Türkçe
kelime sözlüğü ve basit olumsuzluk kontrolüyle yapılıyor.

### 3. HTML dosyasından yorum CSV'si oluşturun

HTML dosyasının proje klasöründe bulunduğunu doğrulayın:

```powershell
Test-Path .\iphone_yorumlar.html
```

Sonuç `True` olmalı. Ardından yorumları çıkarın:

```powershell
python amazon_reviews_to_csv.py .\iphone_yorumlar.html `
  --product-url "https://www.amazon.com.tr/Apple-iPhone-15-128-GB/dp/B0CHXGB3NG"
```

Başarılı olursa `iphone_yorumlar.csv` dosyası oluşturulur. Bu CSV zaten
mevcutsa bu adımı tekrar etmeden doğrudan 4. adıma geçebilirsiniz.

### 4. Duygu analizini çalıştırın

```powershell
python analyze_turkish_sentiment.py .\iphone_yorumlar.csv
```

Terminalde her yorum için duygu etiketini ve puanını, ardından olumlu/olumsuz/
nötr sayılarının özetini görürsünüz. Ayrıntılı sonuçlar
`iphone_yorumlar_duygu_analizi.csv` dosyasına kaydedilir.

### 5. Yorumların tamamını terminalde veya Excel'de görüntüleyin

PowerShell'de yıldız, başlık, duygu ve yorum metnini satır satır görüntülemek
için:

```powershell
Import-Csv .\iphone_yorumlar_duygu_analizi.csv |
  Format-Table rating, title, sentiment, review -Wrap
```

CSV dosyasını Excel'de açarak tüm sütunları tablo halinde inceleyebilirsiniz.
Excel açılmıyorsa dosyanın proje klasöründe oluştuğunu kontrol edin:

```powershell
Get-Item .\iphone_yorumlar.csv, .\iphone_yorumlar_duygu_analizi.csv
```

## Amazon yorumlarını CSV'ye aktarma

Amazon'a otomatik istek gönderilmez. Amazon'un kullanım koşullarına ve ilgili
veri kullanım izinlerine uyduğunuzdan emin olun. İzin verilen bir yöntemle
tarayıcıda yorumların bulunduğu sayfayı açıp HTML olarak kaydedin; betik,
yalnızca bu yerel dosyada bulunan yorumları işler. Ürün sayfasındaki yıldız
ortalaması ile her yoruma verilen yıldız puanı farklıdır; bu betik her yorumun
puanını ve metnini alır.

Gerekli paketleri proje klasöründe kurun:

```powershell
python -m pip install -r requirements.txt
```

Yorumların listelendiği sayfayı tarayıcıdan HTML dosyası olarak kaydedin
(örneğin `iphone_yorumlar.html`), sonra çalıştırın:

```powershell
python amazon_reviews_to_csv.py .\iphone_yorumlar.html `
  --product-url "https://www.amazon.com.tr/Apple-iPhone-15-128-GB/dp/B0CHXGB3NG"
```

Varsayılan olarak `iphone_yorumlar.csv` oluşturulur. Başka bir dosya adı
vermek için `-o .\yorumlar.csv` ekleyin. CSV'de ASIN, yorum kimliği, sayısal
yıldız puanı, puanın ham metni, yorum başlığı, yorum, tarih ve onaylı satın
alma bilgisi yer alır. Yorumlar HTML içinde bulunamazsa betik hata verir;
Amazon'un sayfa yapısı değişirse HTML seçicilerinin güncellenmesi gerekebilir.

## Yorumlara duygu analizi uygulama

Yorumları olumlu/olumsuz olarak sınıflandırmak ve sonucu yeni bir CSV'ye
kaydetmek için:

```powershell
python analyze_turkish_sentiment.py .\iphone_yorumlar.csv
```

`iphone_yorumlar_duygu_analizi.csv` dosyasında özgün yorum alanlarına ek olarak
`sentiment` (Olumlu, Olumsuz veya Nötr), `sentiment_score` ve sınıflandırmada
eşleşen kelimeleri gösteren `sentiment_terms` sütunları bulunur. Analiz,
betik içindeki Türkçe kelime kökleri ve basit olumsuzluk kontrolüne dayanan
açıklanabilir bir başlangıç yöntemidir; bağlamı ve alaycı ifadeleri anlayan
eğitilmiş bir dil modeli değildir. Sözlükte duygu belirten sözcük bulunmayan
yorumlar yanlış bir olumlu/olumsuz karar vermemek için Nötr bırakılır.
