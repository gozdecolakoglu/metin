"""Türkçe yorumları küçük ve açıklanabilir bir kelime sözlüğüyle sınıflandırır."""

# Terminalden girdi/çıktı dosyası gibi komut satırı argümanlarını almak için.
import argparse
# Metni kelimelere ayırmak ve kelime köklerini/olumsuzluk işaretlerini bulmak için.
import re
# CSV girdi ve çıktı dosyalarının yollarını yönetmek için.
from pathlib import Path

# CSV yorumlarını tablo olarak okumak, sınıflandırmak ve yeni CSV'ye yazmak için.
import pandas as pd


# Türkçe ekli kelimeleri kök başlangıcına göre tanımak için olumlu/olumsuz
# kelime başlangıçları tutulur (ör. "beğendim" -> "beg").
POSITIVE_STEMS = (
    "basar",
    "beg",
    "guzel",
    "harika",
    "hizli",
    "iyi",
    "kalite",
    "memnun",
    "mutlu",
    "orijinal",
    "orjinal",
    "ozel",
    "saglam",
    "sorunsuz",
    "super",
    "tesekkur",
    "uygun",
)
NEGATIVE_STEMS = (
    "berbat",
    "bozuk",
    "calismiyor",
    "eksik",
    "gecik",
    "iptal",
    "iade",
    "kotu",
    "memnuniyetsiz",
    "olmadi",
    "pahali",
    "rezalet",
    "sorun",
    "yapalmadi",
    "yapilmadi",
)
# Bu iki kelime kendilerinden önceki duygu kelimesinin anlamını tersine çevirir.
NEGATORS = ("degil", "yok")
# Türkçe karakterler ASCII karşılıklarına çevrilir; böylece sözlükte tek biçim
# kullanılır ve "güzel" gibi kelimeler "guzel" köküyle eşleşebilir.
TRANSLATION = str.maketrans(
    {
        "ç": "c",
        "ğ": "g",
        "ı": "i",
        "ö": "o",
        "ş": "s",
        "ü": "u",
    }
)


def normalize_text(text: str) -> str:
    # casefold büyük/küçük harf farkını kaldırır; translate Türkçe karakterleri
    # sözlüğün kullandığı ASCII biçimine dönüştürür.
    return text.casefold().translate(TRANSLATION)


def polarity_for(token: str) -> int | None:
    # Sözcüğün başına uyan kökleri bulur. Olumlu için +1, olumsuz için -1
    # döndürür; bir eşleşme yoksa bu sözcük puana katkı yapmaz.
    candidates = [
        (stem, 1) for stem in POSITIVE_STEMS if token.startswith(stem)
    ] + [
        (stem, -1) for stem in NEGATIVE_STEMS if token.startswith(stem)
    ]
    if not candidates:
        return None
    # Birden çok kök eşleşirse en uzun olan daha özgül kabul edilir.
    return max(candidates, key=lambda candidate: len(candidate[0]))[1]


def analyze_text(text: str) -> dict[str, object]:
    # Sözcükleri ve olumsuzluk denetiminde kullanmak üzere noktalama
    # işaretlerini ayırır.
    tokens = re.findall(r"[a-z0-9]+|[,;.!?]", normalize_text(text))
    score = 0
    matched_terms = []

    for index, token in enumerate(tokens):
        polarity = polarity_for(token)
        if polarity is None:
            continue

        # Duygu kelimesinden sonraki en fazla üç parçaya bakılır. Noktalama
        # veya yeni bir duygu kelimesi önceki kelimeye ait kapsamı bitirir.
        for following in tokens[index + 1 : index + 4]:
            if re.fullmatch(r"[,;.!?]", following) or polarity_for(following):
                break
            # "iyi değil" gibi ifadelerde kelimenin puanını tersine çevirir.
            if following.startswith(NEGATORS):
                polarity *= -1
                break
        # Her eşleşen kelime toplam puana bir birim ekler veya çıkarır.
        score += polarity
        matched_terms.append(token)

    # Pozitif toplam olumlu, negatif toplam olumsuz; sıfır toplam nötr sayılır.
    sentiment = "Olumlu" if score > 0 else "Olumsuz" if score < 0 else "Nötr"
    return {
        "sentiment_score": score,
        "sentiment": sentiment,
        "sentiment_terms": ", ".join(matched_terms),
    }


def analyze_reviews(input_file: Path, output_file: Path) -> pd.DataFrame:
    # Girdi CSV'sini yükler ve başlık/metin sütunlarının bulunduğunu doğrular.
    reviews = pd.read_csv(input_file)
    missing_columns = {"title", "review"} - set(reviews.columns)
    if missing_columns:
        raise ValueError(
            "Girdi CSV dosyasında gerekli sütunlar eksik: "
            + ", ".join(sorted(missing_columns))
        )

    def classify(row: pd.Series) -> pd.Series:
        # CSV'de boş alanlar NaN olarak okunabileceği için önce boş metne
        # çevrilir; başlık ve yorum birlikte analiz edilir.
        title = "" if pd.isna(row["title"]) else str(row["title"])
        review = "" if pd.isna(row["review"]) else str(row["review"])
        return pd.Series(analyze_text(f"{title} {review}"))

    # Her satıra analiz sonuçlarını ekler, özgün verilerle birlikte yeni CSV'ye
    # kaydeder ve sonucu ana programa döndürür.
    results = reviews.join(reviews.apply(classify, axis=1))
    results.to_csv(output_file, index=False, encoding="utf-8-sig")
    return results


def main() -> None:
    # Komut satırında girdi CSV'si ve isteğe bağlı çıktı adı alınır.
    parser = argparse.ArgumentParser(
        description="Türkçe yorumları sözlük tabanlı duygu analiziyle sınıflandırır."
    )
    parser.add_argument("input_csv", type=Path, help="Yorumların bulunduğu CSV")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Çıktı CSV dosyası (varsayılan: *_duygu_analizi.csv)",
    )
    args = parser.parse_args()

    # Yanlış dosya yolunu işlem başlamadan kullanıcıya bildirir.
    if not args.input_csv.is_file():
        parser.error(f"CSV dosyası bulunamadı: {args.input_csv}")

    # Çıktı adı belirtilmemişse giriş dosyasına "_duygu_analizi" ekler.
    output_file = args.output or args.input_csv.with_name(
        f"{args.input_csv.stem}_duygu_analizi.csv"
    )
    try:
        results = analyze_reviews(args.input_csv, output_file)
    # Dosya/CSV/sütun hatalarını kullanıcıya anlaşılır komut satırı hatası
    # olarak gösterir; hatayı sessizce yutmaz.
    except (OSError, UnicodeError, pd.errors.ParserError, ValueError) as error:
        parser.error(str(error))

    # Her yorumun etiketini/puanını ve bütün veri kümesinin duygu dağılımını
    # terminalde gösterir.
    print(f"{len(results)} yorum analiz edildi: {output_file}")
    print(
        results[["sentiment", "sentiment_score", "title"]]
        .fillna("")
        .to_string(index=False)
    )
    print("\nDuygu dağılımı:")
    print(results["sentiment"].value_counts().to_string())


# Dosya doğrudan çalıştırıldığında main'i başlatır; başka bir Python dosyası
# tarafından içe aktarıldığında komut satırı arayüzünü kendiliğinden açmaz.
if __name__ == "__main__":
    main()
