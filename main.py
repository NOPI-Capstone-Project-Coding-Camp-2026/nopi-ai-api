from fastapi import FastAPI, File, UploadFile
import shutil
import os

# Import fungsi OCR dari file ocr.py
from ocr import extract_text

# Inisiasi aplikasi FastAPI
app = FastAPI(title="NOPI AI API", description="API Utama untuk OCR dan Validasi Struk NOPI")

@app.get("/")
def read_root():
    return {"message": "Selamat datang di NOPI AI API! Server berjalan lancar."}

@app.post("/scan-struk/")
async def scan_struk(file: UploadFile = File(...)):
    """
    Endpoint ini menerima upload foto struk dari Frontend, 
    lalu memprosesnya menggunakan OCR.
    """
    # 1. Simpan gambar yang diupload ke file sementara (temp file)
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # TODO: [SLOT UNTUK HANNA]
    # Nanti di sini gambar akan diprediksi dulu oleh model CNN Hanna (Valid/Tidak Valid)
    # is_valid = cnn_model.predict(temp_file_path)
    
    # 2. Eksekusi fungsi OCR 
    extracted_text = extract_text(temp_file_path)

    # 3. Hapus file sementara agar hardisk server tidak penuh
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)

    # TODO: [SLOT UNTUK TIM DATA SCIENCE]
    # Nanti teks mentah (extracted_text) akan diparsing oleh fungsi Regex buatan tim DS di sini
    
    # 4. Kembalikan hasil ke Frontend (Format JSON)
    return {
        "filename": file.filename,
        "raw_ocr_text": extracted_text,
        "status": "success"
    }