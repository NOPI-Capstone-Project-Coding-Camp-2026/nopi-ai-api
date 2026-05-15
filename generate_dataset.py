import os
import pandas as pd
from tesseract_ocr import extract_text
from tesseract_parser import clean_ocr_text

folder_dataset = "dataset_struk" 
semua_data_terstruktur = []

print("🚀 Memulai proses Ekstraksi dan Parsing Khusus Dataset Sekunder...")

# Looping untuk membaca setiap gambar di dalam folder
for filename in os.listdir(folder_dataset):
    
    # PERBAIKAN FILTER: Wajib berawalan "train_" ATAU "test_"
    if filename.lower().startswith(("train_", "test_")) and filename.lower().endswith((".jpg", ".jpeg", ".png")):
        file_path = os.path.join(folder_dataset, filename)
        
        try:
            # 1. Tugas AI: Membaca Gambar jadi Teks
            raw_text = extract_text(file_path)
            
            # 2. Tugas AI: Mem-parsing Teks jadi Tabel Terstruktur
            parsed_items = clean_ocr_text(raw_text)
            
            # 3. Masukkan ke keranjang besar
            if parsed_items:
                for item in parsed_items:
                    item["Filename"] = filename
                    item["Raw_Text"] = raw_text 
                    semua_data_terstruktur.append(item)
            else:
                print(f"⚠️ {filename}: Format tidak dikenali, dilewati.")
                
        except Exception as e:
            print(f"❌ Error pada {filename}: {e}")

# 4. Ubah keranjang besar menjadi csv
if semua_data_terstruktur:
    df = pd.DataFrame(semua_data_terstruktur)
    
    # Rapikan urutan kolom
    kolom_urut = ["Filename", "Tanggal", "Nama Barang", "Jumlah Barang", "Harga Satuan", "Total Harga", "Raw_Text"]
    df = df[kolom_urut]
    
    # Menyimpan ke bentuk csv
    nama_file_output = "Dataset_Terstruktur_Sekunder_NOPI.csv"
    df.to_csv(nama_file_output, index=False, encoding='utf-8-sig')
    print(f"\n✅ BERHASIL! File '{nama_file_output}' sudah siap dikirim ke tim DS!")
else:
    print("\n❌ Gagal: Tidak ada data sekunder yang berhasil diparsing.")