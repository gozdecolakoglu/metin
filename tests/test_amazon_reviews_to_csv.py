# Testleri tanımlamak ve beklenen sonuçları doğrulamak için Python'ın test çatısı.
import unittest

# Yıldız puanını dönüştürme ve HTML'den yorum çıkarma fonksiyonlarını sınar.
from amazon_reviews_to_csv import extract_reviews, parse_rating


class AmazonReviewsToCsvTests(unittest.TestCase):
    def test_rating_formats(self):
        # Türkçe, İngilizce ve kesir biçimindeki puanların sayıya çevrildiğini
        # ve tanınmayan bir puanın None döndürdüğünü doğrular.
        self.assertEqual(parse_rating("5 yıldız üzerinden 4,5"), 4.5)
        self.assertEqual(parse_rating("4.0 out of 5 stars"), 4.0)
        self.assertEqual(parse_rating("4,5 / 5 yıldız"), 4.5)
        self.assertIsNone(parse_rating("Yıldız bilgisi yok"))

    def test_extracts_reviews_and_product_asin(self):
        # Amazon yorum sayfasının yapısını taklit eden küçük bir HTML örneği.
        html = """
        <div data-hook="review" id="customer_review-R1">
          <i data-hook="review-star-rating"><span>5 yıldız üzerinden 4,5</span></i>
          <a data-hook="reviewTitle"><span>Güzel ürün</span></a>
          <span data-hook="reviewText">
            Brief content visible, double tap to read full content.
            Memnun kaldım. Daha fazla göster Daha az göster
          </span>
          <span data-hook="review-date">15 Ekim 2026</span>
          <span data-hook="avp-badge">Onaylı Alışveriş</span>
        </div>
        """

        rows = extract_reviews(
            html,
            "https://www.amazon.com.tr/Apple-iPhone/dp/B0CHXGB3NG",
        )

        # Yorum alanlarının ve ürün kodunun HTML'den doğru çıkarıldığını
        # kontrol eder.
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["asin"], "B0CHXGB3NG")
        self.assertEqual(rows[0]["rating"], 4.5)
        self.assertEqual(rows[0]["title"], "Güzel ürün")
        self.assertEqual(rows[0]["review"], "Memnun kaldım.")
        self.assertTrue(rows[0]["verified_purchase"])

    def test_missing_review_blocks_raise_error(self):
        # Yorum içermeyen HTML'nin boş sonuç yerine anlaşılır hata verdiğini
        # doğrular.
        with self.assertRaisesRegex(ValueError, "yorumları bulunamadı"):
            extract_reviews("<html><body>Yorum yok</body></html>")


# Test dosyası doğrudan çalıştırıldığında testleri başlatır.
if __name__ == "__main__":
    unittest.main()
