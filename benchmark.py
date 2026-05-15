import time
import pandas as pd
# Import fungsi OCR di sini
from paddle_ocr import extract_text_paddle
from paddle_parser import parse_paddleocr_text
from tesseract_ocr import extract_text_tesseract
from tesseract_parser import parse_tesseract_text 

def run_benchmark(image_paths):
    hasil_komparasi = []

    for img in image_paths:
        print(f"\nMemproses: {img}")
        
        # 1. TES PADDLE OCR
        start_time = time.time()
        raw_paddle = extract_text_paddle(img)
        waktu_paddle = round(time.time() - start_time, 2)
        json_paddle = parse_paddleocr_text(raw_paddle)
        
        # 2. TES TESSERACT OCR
        start_time = time.time()
        raw_tesseract = extract_text_tesseract(img)
        waktu_tesseract = round(time.time() - start_time, 2)
        json_tesseract = parse_tesseract_text(raw_tesseract)

        # 3. TES EASY OCR (Nanti Punya Hanna Masuk Sini)
        # ...

        # Simpan hasil sementara
        hasil_komparasi.append({
            "File": img,
            "Waktu_Paddle (Detik)": waktu_paddle,
            "Hasil_Paddle": json_paddle,
            "Waktu_Tesseract": waktu_tesseract,
            "Hasil_Tesseract": json_tesseract
        })

    # Export ke CSV untuk bahan laporan di GDocs
    df = pd.DataFrame(hasil_komparasi)
    df.to_csv("hasil_komparasi_ocr.csv", index=False)
    print("\n✅ Selesai! Hasil uji coba tersimpan di 'hasil_komparasi_ocr.csv'")

if __name__ == "__main__":
    daftar_foto = [
        r"dataset_struk\primer_0067.jpg", 
        r"dataset_struk\primer_0071.jpg",  
        r"dataset_struk\primer_0081.jpg",  
        r"dataset_struk\primer_0082.jpg",  
        r"dataset_struk\primer_0096.jpg",  
        r"dataset_struk\primer_0099.jpg",  
        r"dataset_struk\primer_0108.jpg",  
        r"dataset_struk\primer_0109.jpg",  
        r"dataset_struk\primer_0111.jpg",  
        r"dataset_struk\primer_0117.jpg"  
    ]
    run_benchmark(daftar_foto)