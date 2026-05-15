import re
import json

def parse_tesseract_text(raw_text): 
    # Struktur utama yang SAMA PERSIS dengan PaddleOCR
    parsed_data = {
        "nama_toko": "",
        "tanggal": "",
        "items": []
    }

    if not raw_text or not isinstance(raw_text, str):
        return json.dumps(parsed_data, indent=4)

    # --- 1. CARI TANGGAL ---
    date_match = re.search(r"\b(\d{2})\s*[-\./]\s*(\d{2})\s*[-\./]\s*((?:19|20)\d{2})\b|\b((?:19|20)\d{2})\s*[-\./]\s*(\d{2})\s*[-\./]\s*(\d{2})\b", raw_text)
    if date_match:
        if date_match.group(1):
            parsed_data["tanggal"] = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
        else:
            parsed_data["tanggal"] = f"{date_match.group(4)}-{date_match.group(5)}-{date_match.group(6)}"

    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
    
    # --- 2. CARI NAMA TOKO (Asumsi di 3 baris pertama) ---
    for i, line in enumerate(lines):
        if i < 3 and not parsed_data["nama_toko"]:
            if "toko" in line.lower() or "pt " in line.lower() or "cv " in line.lower() or "raya" in line.lower() or "mart" in line.lower():
                parsed_data["nama_toko"] = line
            elif i == 0:
                parsed_data["nama_toko"] = line

    # --- 3. CARI ITEM BARANG ---
    skip_next_line = False 
    for i, line in enumerate(lines):
        if skip_next_line:
            skip_next_line = False
            continue

        # POLA 1: Toko Sukatani
        match1 = re.match(r"^([a-zA-Z0-9\?é]+)\s*[xX]\s*[a-zA-Z]*\s*([\d\,\.\sOo]+)\s*[a-zA-Z]*\s*([\d\,\.\sOo]+)", line)
        if match1 and i > 0:
            nama = lines[i-1]
            qty_clean = re.sub(r'[^0-9]', '', match1.group(1))
            harga_clean = re.sub(r'[^0-9]', '', re.sub(r'[oO]', '0', match1.group(2)))
            total_clean = re.sub(r'[^0-9]', '', re.sub(r'[oO]', '0', match1.group(3)))
            
            parsed_data["items"].append({
                "nama_barang": nama,
                "jumlah_barang": int(qty_clean) if qty_clean else 1,
                "harga_satuan": int(harga_clean) if harga_clean else 0,
                "total_harga_item": int(total_clean) if total_clean else 0
            })
            continue

        # POLA 2: PT Balina Agung Perkasa (Satu Baris)
        match2_single = re.search(r"(AQ\.[^\s]+\s*\d*[xXX]\d+)\s+(\d+).*?([\d\.\,Oo]{4,}).*?([\d\.\,Oo]{4,})", line)
        if match2_single:
            nama = match2_single.group(1)
            qty_clean = match2_single.group(2)
            harga_clean = re.sub(r'[^0-9]', '', re.sub(r'[oO]', '0', match2_single.group(3)))
            total_clean = re.sub(r'[^0-9]', '', re.sub(r'[oO]', '0', match2_single.group(4)))
            
            parsed_data["items"].append({
                "nama_barang": nama,
                "jumlah_barang": int(qty_clean) if qty_clean else 1,
                "harga_satuan": int(harga_clean) if harga_clean else 0,
                "total_harga_item": int(total_clean) if total_clean else 0
            })
            continue

        # POLA 2: PT Balina Agung Perkasa (Pisah Baris)
        match2_split_name = re.search(r"(AQ\.[^\s]+\s*\d*[xXX]\d+)\s+(\d+)\s*$", line)
        if match2_split_name and i+1 < len(lines):
            next_line = lines[i+1]
            match2_split_price = re.search(r"([\d\.\,Oo]{4,}).*?([\d\.\,Oo]{4,})", next_line)
            if match2_split_price:
                nama = match2_split_name.group(1)
                qty_clean = match2_split_name.group(2)
                harga_clean = re.sub(r'[^0-9]', '', re.sub(r'[oO]', '0', match2_split_price.group(1)))
                total_clean = re.sub(r'[^0-9]', '', re.sub(r'[oO]', '0', match2_split_price.group(2)))
                
                parsed_data["items"].append({
                    "nama_barang": nama,
                    "jumlah_barang": int(qty_clean) if qty_clean else 1,
                    "harga_satuan": int(harga_clean) if harga_clean else 0,
                    "total_harga_item": int(total_clean) if total_clean else 0
                })
                skip_next_line = True 
                continue

        # POLA 3 & 4: Indomaret / Alfamart
        match3 = re.search(r"^(.*?)\s+([^\s]+)\s+([\d\.\,Oo]{3,})\s+([\d\.\,Oo]{3,})$", line)
        if match3:
            nama = match3.group(1).strip()
            if any(kata in nama.lower() for kata in ['total', 'tunai', 'kembali', 'ppn', 'bayar', 'item']):
                continue
                
            qty_raw = match3.group(2)
            qty_raw = re.sub(r'[\|Il\:\-\_!]', '1', qty_raw)
            qty_clean = re.sub(r'[^0-9]', '', qty_raw)
            
            harga_clean = re.sub(r'[^0-9]', '', re.sub(r'[oO]', '0', match3.group(3)))
            total_clean = re.sub(r'[^0-9]', '', re.sub(r'[oO]', '0', match3.group(4)))
            
            parsed_data["items"].append({
                "nama_barang": re.sub(r'[^a-zA-Z0-9\s]', '', nama).strip(), 
                "jumlah_barang": int(qty_clean) if qty_clean else 1, 
                "harga_satuan": int(harga_clean) if harga_clean else 0, 
                "total_harga_item": int(total_clean) if total_clean else 0
            })
            continue

        # POLA 5: PT. Depok Distribusindo
        match5 = re.search(r"(?:P[cC][sS])?\s*\d+\s+(.*?)\s+(\d+)\s*P[cC][sS]\s+([\d\.\,Oo]+)\s+([\d\.\,Oo]+)", line)
        if match5:
            nama = match5.group(1)
            qty_clean = match5.group(2)
            harga_clean = re.sub(r'[^0-9]', '', re.sub(r'[oO]', '0', match5.group(3)))
            total_clean = re.sub(r'[^0-9]', '', re.sub(r'[oO]', '0', match5.group(4)))
            
            parsed_data["items"].append({
                "nama_barang": re.sub(r'[^a-zA-Z0-9\s]', '', nama).strip(),
                "jumlah_barang": int(qty_clean) if qty_clean else 1,
                "harga_satuan": int(harga_clean) if harga_clean else 0,
                "total_harga_item": int(total_clean) if total_clean else 0
            })
            continue

    return json.dumps(parsed_data, indent=4)