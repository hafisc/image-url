# Image Downloader - Bulk Download dari URL ke JPG

Program ini untuk download gambar dari URL dalam jumlah besar (3000+ URLs) dan menyimpannya dengan format penamaan khusus: `MNG{artikel_id}-{sequence_number}.jpg`

## Fitur Utama

✅ **Bulk Download**: Handle 3000+ URLs dengan efisien  
✅ **Smart Naming**: Format MNG{artikel_id}-{sequence_number}.jpg  
✅ **Resume Download**: Skip file yang sudah ada  
✅ **Progress Tracking**: Real-time progress dan statistik  
✅ **Error Handling**: Log error ke file JSON  
✅ **Multiple Input**: Support dictionary, JSON, dan CSV  
✅ **High Quality**: JPG quality 95% dengan optimasi  

## Cara Penggunaan

### 1. Pakai Data Dictionary (untuk testing kecil)
```python
python main.py
```

### 2. Pakai File JSON (untuk dataset besar)
```python
# Edit main.py, uncomment bagian ini:
data_from_json = downloader.load_from_json("urls_data.json")
downloader.download_batch(data_from_json)
```

### 3. Pakai File CSV (untuk dataset besar)
```python
# Edit main.py, uncomment bagian ini:
data_from_csv = downloader.load_from_csv("urls_data.csv")
downloader.download_batch(data_from_csv)
```

## Format File Input

### JSON Format (`urls_data.json`):
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

### CSV Format (`urls_data.csv`):
```csv
artikel_id,url
1703127252,https://shop.mango.com/assets/rcs/pics/static/T1/fotos/SE/17031272_52.jpg
1703127252,https://shop.mango.com/assets/rcs/pics/static/T1/fotos/SE/17031272_52_R.jpg
1703127999,https://shop.mango.com/assets/rcs/pics/static/T1/fotos/SE/17031279_99.jpg
```

## Output

- **Gambar**: `hasil_download/MNG{artikel_id}-{sequence_number}.jpg`
- **Error Log**: `hasil_download/failed_downloads.json` (jika ada yang gagal)

## Contoh Output Filename

Untuk artikel `1703127252` dengan 3 URL:
- `MNG1703127252-1.jpg`
- `MNG1703127252-2.jpg` 
- `MNG1703127252-3.jpg`

## Dependencies

```bash
pip install requests pillow
```

## Tips untuk 3000+ URLs

1. **Gunakan file JSON/CSV** - Lebih efisien daripada hardcode di script
2. **Jalankan bertahap** - Bisa pause/resume kapan saja
3. **Monitor progress** - Ada real-time progress tracking
4. **Cek error log** - File yang gagal akan tercatat di `failed_downloads.json`
5. **Bandwidth** - Program sudah optimasi untuk tidak overload server

## Troubleshooting

- **File sudah ada**: Program otomatis skip file yang sudah didownload
- **URL gagal**: Cek `failed_downloads.json` untuk detail error
- **Koneksi lambat**: Timeout sudah diset 30 detik per file
- **Memory**: Program stream download, tidak load semua ke memory
