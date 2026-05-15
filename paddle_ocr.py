import os
# Matikan fitur eksperimental Paddle 3.x di Windows
os.environ['FLAGS_enable_pir_api'] = '0'
os.environ['FLAGS_use_mkldnn'] = '0'

from paddleocr import PaddleOCR

# Inisiasi model
ocr_model = PaddleOCR(use_textline_orientation=True, lang='en') 

def extract_text_paddle(image_path):
    result = ocr_model.ocr(image_path)
    
    extracted_text = []
    
    for idx in range(len(result)):
        res = result[idx]
        if res is not None:
            for line in res:
                text = line[1][0]
                extracted_text.append(text)
                
    return "\n".join(extracted_text)

# --- BLOK TES ---
if __name__ == "__main__":
    path_gambar = r"dataset_struk\primer_0071.jpg" 
    
    print("Mulai membaca dengan PaddleOCR...")
    hasil_teks = extract_text_paddle(path_gambar)
    
    print("\n=== HASIL BACAAN PADDLEOCR ===")
    print(hasil_teks)