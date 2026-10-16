"""İzin verilen şekilde kaydedilmiş Amazon yorum HTML'sini CSV'ye aktarır."""

# Terminalden dosya adı ve seçenekleri almak için.
import argparse
# Yıldız puanları/ASIN gibi metin parçalarını desenle bulmak ve metni temizlemek için.
import re
# HTML ve CSV dosyalarının yollarını işletim sisteminden bağımsız yönetmek için.
from pathlib import Path
# Yorum kayıtlarının alan tipini belirtmek için kullanılan genel tip desteği.
from typing import Any
# Ürün URL'sini parçalayıp içindeki ASIN yolunu bulmak için.
from urllib.parse import urlparse

# Yorum kayıtlarını tabloya dönüştürmek ve CSV dosyası yazmak için.
import pandas as pd
# BeautifulSoup HTML'yi okumak, Tag ise HTML elemanlarının tipini belirtmek için.
from bs4 import BeautifulSoup, Tag


def text_for(review: Tag, selector: str) -> str:
    # CSS seçicisiyle aranan HTML alanını bulur; alan yoksa boş metin döndürür.
    element = review.select_one(selector)
    if not element:
        return ""
    # Etiketleri kaldırıp metni alır; HTML'deki "daha fazla göster" gibi arayüz
    # metinlerini yorum içeriğinden çıkarır.
    text = element.get_text(" ", strip=True)
    for control_text in (
        "Brief content visible, double tap to read full content.",
        "Full content visible, double tap to read brief content.",
        "Daha fazla göster",
        "Daha az göster",
    ):
        text = text.replace(control_text, "")
    # HTML boşluklarını tek boşluğa indirerek okunabilir bir metin döndürür.
    return re.sub(r"\s+", " ", text).strip()


def parse_rating(rating_text: str) -> float | None:
    # Amazon puanı Türkçe ("5 yıldız üzerinden 4,5") veya İngilizce
    # ("4.0 out of 5 stars") biçiminde gösterebilir.
    patterns = (
        r"(\d+(?:[.,]\d+)?)\s*out of\b",
        r"üzerinden\s*(\d+(?:[.,]\d+)?)",
    )
    for pattern in patterns:
        match = re.search(pattern, rating_text, flags=re.IGNORECASE)
        if match:
            # Sayısal puanı ondalıklı sayıya çevirir; virgüllü Türkçe puanlarda
            # Python'ın beklediği nokta biçimini kullanır.
            return float(match.group(1).replace(",", "."))

    # "4,5 / 5" gibi alternatif gösterim biçimini de kontrol eder.
    match = re.search(r"(\d+(?:[.,]\d+)?)\s*/\s*\d+", rating_text)
    if match:
        return float(match.group(1).replace(",", "."))
    return None


def extract_reviews(html: str, product_url: str = "") -> list[dict[str, Any]]:
    # Kaydedilmiş HTML metnini sorgulanabilir DOM ağacına dönüştürür.
    soup = BeautifulSoup(html, "html.parser")
    # Amazon ürün kimliğini (ASIN) ürün URL'sindeki /dp/ kısmından çıkarır.
    asin_match = re.search(r"/dp/([A-Z0-9]{10})", urlparse(product_url).path)
    asin = asin_match.group(1) if asin_match else ""

    rows = []
    # Amazon'un her yorum için kullandığı data-hook alanıyla yorum bloklarını
    # bulur ve her birinden CSV'ye yazılacak alanları toplar.
    for review in soup.select('[data-hook="review"]'):
        rating_text = text_for(
            review,
            '[data-hook="review-star-rating"], '
            '[data-hook="cmps-review-star-rating"]',
        )
        rows.append(
            {
                # Yorum kimliği ve ürün bilgisi yorumlarla ilişki kurmaya yarar.
                "asin": asin,
                "review_id": review.get("id", ""),
                # Sayısal yıldız değeri ve sayfadaki özgün puan yazısı saklanır.
                "rating": parse_rating(rating_text),
                "rating_text": rating_text,
                # Amazon'un farklı sayfa sürümlerinde kullandığı alternatif
                # başlık/gövde seçicileri birlikte kontrol edilir.
                "title": text_for(
                    review,
                    '[data-hook="review-title"], [data-hook="reviewTitle"]',
                ),
                "review": text_for(
                    review,
                    '[data-hook="review-body"], [data-hook="reviewText"]',
                ),
                "date": text_for(review, '[data-hook="review-date"]'),
                # Onaylı satın alma rozeti varsa True, yoksa False kaydedilir.
                "verified_purchase": bool(
                    review.select_one('[data-hook="avp-badge"]')
                ),
                "product_url": product_url,
            }
        )

    # Yorum bulunmaması çoğunlukla yanlış HTML sayfasının kaydedildiğini
    # gösterir; boş/sahte çıktı üretmek yerine nedeni açıkça bildirir.
    if not rows:
        raise ValueError(
            "HTML içinde Amazon yorumları bulunamadı. Yorumların listelendiği "
            "sayfayı kaydedin; yalnızca ürün detay sayfası yeterli olmayabilir."
        )
    return rows


def main() -> None:
    # Terminalden HTML dosya adı, isteğe bağlı CSV adı ve ürün URL'si alır.
    parser = argparse.ArgumentParser(
        description="Kaydedilmiş Amazon yorum HTML dosyasını CSV'ye dönüştürür."
    )
    parser.add_argument("html_file", type=Path, help="Kaydedilmiş yorum sayfası")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Çıktı CSV dosyası (varsayılan: HTML dosyasıyla aynı ad)",
    )
    parser.add_argument(
        "--product-url",
        default="",
        help="Ürün URL'si; ASIN ve kaynak URL CSV'ye eklenir",
    )
    args = parser.parse_args()

    # Yanlış veya mevcut olmayan dosya yolunu erken aşamada kullanıcıya bildirir.
    if not args.html_file.is_file():
        parser.error(f"HTML dosyası bulunamadı: {args.html_file}")

    # Çıktı adı verilmezse HTML dosyasının uzantısını .csv yapar.
    output_file = args.output or args.html_file.with_suffix(".csv")
    # Türkçe karakterleri koruyarak kaydedilmiş HTML'yi okur; hatalı karakter
    # baytları varsa dosyanın geri kalanını işlemeye devam eder.
    html = args.html_file.read_text(encoding="utf-8", errors="replace")
    rows = extract_reviews(html, args.product_url)
    # UTF-8 BOM, CSV'nin Excel'de Türkçe karakterlerle açılmasına yardımcı olur.
    pd.DataFrame(rows).to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"{len(rows)} yorum kaydedildi: {output_file}")


# Bu dosya terminalden çalıştırılırsa komut satırı arayüzünü başlatır.
if __name__ == "__main__":
    main()
