from paddle_ocr import extract_text_paddle
from paddle_parser import parse_paddleocr_text

def test_foto_struk(image_path):
    print(f"\n" + "="*50)
    print(f"📸 MEMPROSES FOTO: {image_path}")
    print("="*50)
    
    try:
        # Ekstrak Teks
        raw_text = extract_text_paddle(image_path)
        
        # Teks mentah paddle ocr
        print("\n🔍 [DEBUG] TEKS MENTAH DARI PADDLE OCR:")
        print(raw_text)
        print("-" * 50)
        
        # Parsing
        hasil_json = parse_paddleocr_text(raw_text)
        print("\n✅ HASIL EKSTRAKSI JSON:")
        print(hasil_json)
        
    except Exception as e:
        print(f"[ERROR] Gagal memproses: {e}")

if __name__ == "__main__":
    daftar_foto_tes = [
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
    
    for foto in daftar_foto_tes:
        test_foto_struk(foto)