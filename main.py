from fastapi import FastAPI, File, UploadFile
import shutil
import os

# 1. IMPORT Pipeline Gabungan cnn & ocr
from inference_notebook import inference_pipeline

# Inisiasi aplikasi FastAPI
app = FastAPI(title="NOPI AI API", description="API Utama untuk OCR dan Validasi Struk NOPI")

@app.get("/")
def read_root():
    return {"message": "Selamat datang di NOPI AI API! Server berjalan lancar."}

@app.post("/api/extract-nota")
async def scan_struk(file: UploadFile = File(...)):
    """
    Endpoint ini menerima upload foto struk dari Frontend, 
    lalu memprosesnya menggunakan Pipeline Terpadu (CNN -> OCR -> Parser).
    """
    # 1. Simpan gambar yang diupload ke file sementara (temp file)
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Otomatis jalanin CNN, lalu OCR, lalu Regex
    try:
        # Panggil fungsi dari inference_notebook.py
        hasil_akhir = inference_pipeline(temp_file_path)
    except Exception as e:
        # Try-Except (anti-crash)
        hasil_akhir = {
            "status": "error", 
            "message": f"Terjadi kesalahan internal pada sistem AI: {str(e)}"
        }

    # 3. Hapus file sementara agar hardisk server tidak penuh
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)
    
    # 4. Kembalikan hasil persis seperti yang dikeluarkan oleh pipeline
    # Hasilnya sudah berupa JSON rapi lengkap dengan status (success/rejected)
    return hasil_akhir