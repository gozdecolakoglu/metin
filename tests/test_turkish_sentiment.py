# Test sırasında geçici dosyaları güvenli biçimde oluşturup sonunda kaldırmak için.
import tempfile
# Test senaryolarını tanımlamak ve sonuçları doğrulamak için Python'ın test çatısı.
import unittest
# Geçici girdi ve çıktı CSV dosyalarının yollarını oluşturmak için.
from pathlib import Path

# Test CSV'sini üretmek ve analiz çıktısını yeniden okuyup kontrol etmek için.
import pandas as pd

# Yorum metnini sınıflandırma ve CSV dosyasını analiz etme fonksiyonlarını sınar.
from analyze_turkish_sentiment import analyze_reviews, analyze_text


class TurkishSentimentTests(unittest.TestCase):
    def test_positive_review(self):
        # Olumlu kelimelerin pozitif toplam puan ve Olumlu etiketi verdiğini
        # doğrular.
        result = analyze_text("Harika ürün, çok memnun kaldım ve hızlı geldi.")
        self.assertEqual(result["sentiment"], "Olumlu")
        self.assertGreater(result["sentiment_score"], 0)

    def test_negative_review(self):
        # Olumsuz kelimeler ve olumsuzluk ifadesi bulunan yorumun Olumsuz
        # sınıflandırıldığını doğrular.
        result = analyze_text("Karta taksit yapılmadı, memnun değilim.")
        self.assertEqual(result["sentiment"], "Olumsuz")
        self.assertLess(result["sentiment_score"], 0)

    def test_negated_positive_word_is_negative(self):
        # "İyi değil" ifadesinde "değil" kelimesinin olumlu anlamı çevirdiğini
        # kontrol eder.
        result = analyze_text("Ürün iyi değil.")
        self.assertEqual(result["sentiment"], "Olumsuz")

    def test_no_sentiment_words_is_neutral(self):
        # Duygu sözlüğünde eşleşme yoksa yorumun Nötr kaldığını doğrular.
        result = analyze_text("Normal")
        self.assertEqual(result["sentiment"], "Nötr")

    def test_analyzes_csv_and_saves_results(self):
        # Gerçek kullanıcı dosyalarını etkilemeden test için geçici klasör
        # içinde örnek girdi ve çıktı CSV'leri oluşturur.
        with tempfile.TemporaryDirectory() as directory:
            input_file = Path(directory) / "reviews.csv"
            output_file = Path(directory) / "sentiment.csv"
            pd.DataFrame(
                [
                    {"title": "Harika", "review": "Çok güzel."},
                    {"title": "Normal", "review": "Normal"},
                ]
            ).to_csv(input_file, index=False, encoding="utf-8-sig")

            results = analyze_reviews(input_file, output_file)
            saved = pd.read_csv(output_file)

            # Hem fonksiyonun döndürdüğü tabloda hem yazılan CSV'de etiketlerin
            # beklenen sırada bulunduğunu doğrular.
            self.assertEqual(
                results["sentiment"].tolist(), ["Olumlu", "Nötr"]
            )
            self.assertEqual(saved["sentiment"].tolist(), ["Olumlu", "Nötr"])


# Test dosyası doğrudan çalıştırıldığında bütün testleri başlatır.
if __name__ == "__main__":
    unittest.main()
