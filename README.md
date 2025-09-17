# 🖼️ Image Downloader - Excel to JPG Bulk Downloader

📋 Program untuk download gambar dari file Excel yang berisi URL gambar dalam jumlah besar dan menyimpannya dengan format penamaan khusus: `MNG{artikel_id}-{sequence_number}.jpg`

## ⭐ Fitur Utama

📊 **Excel Processing**: Otomatis extract URL dari file Excel  
📁 **Dual Excel Support**: Handle 2 file Excel terpisah (`LINK IMAGE 1.xlsx` & `LINK IMAGE 2.xlsx`)  
🏷️ **Smart Naming**: Format MNG{artikel_id}-{sequence_number}.jpg  
⏭️ **Resume Download**: Skip file yang sudah ada  
📈 **Progress Tracking**: Real-time progress dan statistik  
🛡️ **Error Handling**: Log error ke file JSON  
🗂️ **Organized Output**: Folder terpisah untuk setiap Excel file  
🎨 **High Quality**: JPG quality 95% dengan optimasi  

## 🔄 Workflow

### 1️⃣ Persiapan Data Excel
Pastikan file Excel Anda memiliki:
- 🆔 **ID Column**: `ARTIKEL`, `Ref + Color`, `REF`, `ID`, atau `PRODUCT_ID`
- 🔗 **URL Columns**: Kolom yang mengandung kata `IMAGE` atau `LINK`

### 2️⃣ Extract URLs dari Excel
```bash
python excel_processor.py
```
Script ini akan:
- 📖 Membaca `LINK IMAGE 1.xlsx` → `data_url_link_image_1.json`
- 📖 Membaca `LINK IMAGE 2.xlsx` → `data_url_link_image_2.json`
- 🔗 Membuat `data_url_full.json` (gabungan kedua file)

### 3️⃣ Download Images
```bash
python main.py
```
Pilihan download:
1. 🎯 **Download from both Excel files** (recommended) - Folder terpisah
2. 📦 **Download from single combined file** - Satu folder
3. 🧪 **Test with small sample data** - Testing

## 📂 File Structure

```
Image url/
├── LINK IMAGE 1.xlsx              # Excel file pertama
├── LINK IMAGE 2.xlsx              # Excel file kedua
├── excel_processor.py             # Extract URLs dari Excel
├── main.py                        # Main downloader
├── check_excel_structure.py       # Debug Excel structure
├── data_url_link_image_1.json     # URLs dari Excel 1
├── data_url_link_image_2.json     # URLs dari Excel 2
├── data_url_full.json             # Combined URLs
└── hasil_download/                # Output folder
    ├── link_image_1/              # Images dari Excel 1
    ├── link_image_2/              # Images dari Excel 2
    └── failed_downloads.json      # Error log
```

## 📁 Output Structure

### 🎯 Dual Download (Recommended)
```
hasil_download/
├── link_image_1/
│   ├── MNG1703127252-1.jpg
│   ├── MNG1703127252-2.jpg
│   └── failed_downloads.json
└── link_image_2/
    ├── MNG1703127999-1.jpg
    ├── MNG1703127999-2.jpg
    └── failed_downloads.json
```

### 📦 Single Download
```
hasil_download/
├── MNG1703127252-1.jpg
├── MNG1703127252-2.jpg
├── MNG1703127999-1.jpg
└── failed_downloads.json
```

## 📦 Dependencies

```bash
pip install requests pillow pandas openpyxl
```

## 📋 Cara Penggunaan Detail

### 🔍 Step 1: Check Excel Structure (Optional)
```bash
python check_excel_structure.py
```
Untuk melihat struktur kolom Excel dan memastikan format yang benar.

### ⚙️ Step 2: Extract URLs
```bash
python excel_processor.py
```
Output:
- 📄 `data_url_link_image_1.json`
- 📄 `data_url_link_image_2.json` 
- 📄 `data_url_full.json`

### 🚀 Step 3: Download Images
```bash
python main.py
```
Pilih opsi sesuai kebutuhan:
- 🎯 **Opsi 1**: Download terpisah (recommended untuk organisasi yang lebih baik)
- 📦 **Opsi 2**: Download gabungan (untuk backward compatibility)
- 🧪 **Opsi 3**: Test dengan sample data

## 📄 Format JSON Output

```json
{
  "1703127252": [
    "https://shop.mango.com/assets/rcs/pics/static/T1/fotos/SE/17031272_52.jpg",
    "https://shop.mango.com/assets/rcs/pics/static/T1/fotos/SE/17031272_52_R.jpg"
  ],
  "1703127999": [
    "https://shop.mango.com/assets/rcs/pics/static/T1/fotos/SE/17031279_99.jpg"
  ]
}
```

## 💡 Tips untuk Dataset Besar

1. 🎯 **Gunakan Dual Download** - Lebih terorganisir dan mudah di-manage
2. 📊 **Monitor Progress** - Real-time progress tracking setiap 10 file
3. ⏭️ **Resume Capability** - Program otomatis skip file yang sudah ada
4. 📝 **Error Tracking** - Semua error tercatat di `failed_downloads.json`
5. 🌐 **Bandwidth Optimization** - Timeout 30 detik, stream download

## 🛠️ Troubleshooting

- 📊 **Excel tidak terbaca**: Pastikan format .xlsx dan ada kolom ID + URL
- ⏭️ **File sudah ada**: Program otomatis skip file yang sudah didownload
- ❌ **URL gagal**: Cek `failed_downloads.json` untuk detail error
- 💾 **Memory issue**: Program menggunakan stream download, tidak load semua ke memory
- ⏱️ **Koneksi timeout**: Timeout sudah diset 30 detik per file

## 🔧 Advanced Usage

### 📝 Manual JSON/CSV Input
Jika tidak menggunakan Excel, bisa langsung edit `main.py` untuk load dari:
- 📄 JSON file: `downloader.load_from_json("custom_data.json")`
- 📊 CSV file: `downloader.load_from_csv("custom_data.csv")`
