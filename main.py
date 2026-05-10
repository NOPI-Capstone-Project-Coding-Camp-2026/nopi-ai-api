from fastapi import FastAPI, File, UploadFile
import shutil
import os

# Import fungsi OCR dari file ocr.py
from ocr import extract_text

# Import fungsi parser dari file parser.py yang baru dibuat
from parser import clean_ocr_text 

# Inisiasi aplikasi FastAPI
app = FastAPI(title="NOPI AI API", description="API Utama untuk OCR dan Validasi Struk NOPI")

@app.get("/")
def read_root():
    return {"message": "Selamat datang di NOPI AI API! Server berjalan lancar."}

@app.post("/scan-struk/")
async def scan_struk(file: UploadFile = File(...)):
    """
    Endpoint ini menerima upload foto struk dari Frontend, 
    lalu memprosesnya menggunakan OCR dan merapikannya menjadi tabel/JSON.
    """
    # 1. Simpan gambar yang diupload ke file sementara (temp file)
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # TODO: [SLOT UNTUK HANNA]
    # Nanti di sini gambar akan diprediksi dulu oleh model CNN Hanna (Valid/Tidak Valid)
    # is_valid = cnn_model.predict(temp_file_path)
    # if not is_valid: 
    #     return {"status": "error", "message": "Gambar tidak dikenali sebagai struk yang valid."}
    
    # 2. Eksekusi fungsi OCR (Gambar -> Teks Mentah)
    extracted_text = extract_text(temp_file_path)

    # 3. Eksekusi fungsi Parser (Teks Mentah -> Data Terstruktur)
    structured_data = clean_ocr_text(extracted_text)

    # 4. Hapus file sementara agar hardisk server tidak penuh
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)
    
    # 5. Kembalikan hasil ke Frontend (Format JSON)
    return {
        "status": "success",
        "filename": file.filename,
        "raw_ocr_text": extracted_text,  # Tetap dikirim untuk keperluan debugging/log
        "parsed_data": structured_data   # Ini akan dipakai web Frontend
    }