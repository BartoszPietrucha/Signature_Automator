import os
import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import io
from PIL import Image


def dodaj_pieczatke_na_podstawie_lokalizacji_tekstu(plik_pdf, obraz_png, tekst_do_wykrycia, skalowanie=0.3, przesuniecia=None):
    if przesuniecia is None:
        przesuniecia = {}

    # Wczytaj oryginalne wymiary obrazu
    with Image.open(obraz_png) as img:
        szerokosc_obrazka = img.width * skalowanie
        wysokosc_obrazka = img.height * skalowanie

    dokument = fitz.open(plik_pdf)
    writer = PdfWriter()
    apk_writer = PdfWriter()

    znalezione_pieczatki = 0  # Licznik pieczątek
    strony_do_apk = []        # Lista stron do zapisania w folderze APK

    for numer_strony, strona in enumerate(dokument):
        prostokaty = strona.search_for(tekst_do_wykrycia)
        print(f"Strona {numer_strony + 1}: Znaleziono {len(prostokaty)} wystąpień tekstu '{tekst_do_wykrycia}'")

        # Inicjalizujemy bufor dla każdej strony
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(strona.rect.width, strona.rect.height))

        if prostokaty:
            for prostokat in prostokaty:
                print(f"Strona {numer_strony + 1}: Prostokąt przed analizą: {prostokat}")

                # Oblicz współrzędne pieczątki
                x = prostokat.x0 - 35
                y = strona.rect.height - prostokat.y1 + wysokosc_obrazka - 20

                print(f"Strona {numer_strony + 1}: Współrzędne pieczątki: x={x}, y={y}")
                can.drawImage(obraz_png, x, y, width=szerokosc_obrazka, height=wysokosc_obrazka, mask='auto')

                znalezione_pieczatki += 1

                # Dodaj stronę do listy stron do pliku APK, jeśli to pierwsza lub druga pieczątka
                if znalezione_pieczatki <= 2 and numer_strony + 1 not in strony_do_apk:
                    strony_do_apk.append(numer_strony + 1)

            can.save()
            packet.seek(0)

            # Dodaj zmodyfikowaną stronę do PDF
            nowa_strona = PdfReader(packet)
            strona_pdf = PdfReader(plik_pdf).pages[numer_strony]
            strona_pdf.merge_page(nowa_strona.pages[0])
            writer.add_page(strona_pdf)
        else:
            print(f"Strona {numer_strony + 1}: Brak dopasowania tekstu, dodano oryginalną stronę.")
            writer.add_page(PdfReader(plik_pdf).pages[numer_strony])

    # Przygotuj folder `podpisane` do zapisu
    folder_podpisane = "podpisane"
    os.makedirs(folder_podpisane, exist_ok=True)

    # Zapisz plik PDF do folderu `podpisane`
    nazwa_pliku = os.path.basename(plik_pdf).replace(".pdf", ".pdf")
    zapisany_pdf = os.path.join(folder_podpisane, nazwa_pliku)
    with open(zapisany_pdf, "wb") as output:
        writer.write(output)

    # Jeśli znaleziono pierwsze dwie pieczątki, zapisz odpowiednie strony do folderu APK
    if strony_do_apk:
        folder_apk = "SOP"
        os.makedirs(folder_apk, exist_ok=True)

        for numer_strony in strony_do_apk:
            apk_writer.add_page(PdfReader(zapisany_pdf).pages[numer_strony - 1])

        apk_pdf = os.path.join(folder_apk, nazwa_pliku.replace(".pdf", "_SOP.pdf"))
        with open(apk_pdf, "wb") as apk_output:
            apk_writer.write(apk_output)
        print(f"Plik z pierwszymi dwoma pieczątkami zapisano w: {apk_pdf}")

    print(f"Plik zapisano w: {zapisany_pdf}")
    return zapisany_pdf


# Główna pętla dla folderu source/
source_folder = "source"
obraz_png = "pieczatka_podpis_przezroczysty.png"
tekst_do_wykrycia = "podpis przedstawiciela TUW „TUW”"

for filename in os.listdir(source_folder):
    if filename.endswith(".pdf"):
        plik_pdf = os.path.join(source_folder, filename)
        print(f"Przetwarzanie pliku: {plik_pdf}")
        zapisany_pdf = dodaj_pieczatke_na_podstawie_lokalizacji_tekstu(
            plik_pdf, obraz_png, tekst_do_wykrycia, skalowanie=0.12
        )
        print(f"Zapisano plik: {zapisany_pdf}")
