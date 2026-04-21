import cv2
import pytesseract
import numpy as np
import os

# Pastikan path tesseract disesuaikan dengan laptop kamu!
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text(image_path: str) -> str:
    """
    Fungsi untuk mengekstrak teks dari gambar struk menggunakan OpenCV dan Tesseract.
    """
    if not os.path.exists(image_path):
        return "Error: File gambar tidak ditemukan."

    # 1. Baca gambar
    img = cv2.imread(image_path)
    if img is None:
        return "Error: Format gambar tidak didukung."

    # 2. PRE-PROCESSING LEVEL UP!
    # Trik 1: Perbesar gambar 2x lipat agar hurufnya lebih jelas dibaca Tesseract
    img_resized = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # Trik 2: Ubah ke hitam putih (Grayscale)
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    
    # Trik 3: Otsu's Thresholding (Lebih pintar memisahkan tinta hitam dan kertas putih)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 3. Ekstraksi OCR 
    # PSM 4 biasanya lebih cocok untuk struk yang bentuknya seperti kolom memanjang ke bawah
    custom_config = r'--psm 4'
    text = pytesseract.image_to_string(thresh, config=custom_config)

    return text.strip()