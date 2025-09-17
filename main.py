import requests
from PIL import Image
from io import BytesIO
import os
import json
import csv
import time
from datetime import datetime
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

class ImageDownloader:
    def __init__(self, output_dir="hasil_download", max_workers=5):
        self.output_dir = output_dir
        self.max_workers = max_workers
        self.downloaded_count = 0
        self.failed_count = 0
        self.total_count = 0
        self.failed_urls = []
        
        # Buat folder output
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Setup session untuk reuse connection
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def download_single_image(self, artikel_id, url, sequence_num):
        """Download single image dengan error handling yang lebih baik"""
        # Pastikan folder output ada
        os.makedirs(self.output_dir, exist_ok=True)
        filename = f"{self.output_dir}/MNG{artikel_id}-{sequence_num}.jpg"
        
        # Skip jika file sudah ada
        if os.path.exists(filename):
            print(f"⏭️  Skip (sudah ada): {filename}")
            return True, filename
        
        try:
            response = self.session.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            # Cek apakah response adalah gambar
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                raise Exception(f"Bukan file gambar: {content_type}")
            
            # Download dan convert ke JPG
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img = img.convert("RGB")
            
            # Simpan dengan kualitas bagus
            img.save(filename, "JPEG", quality=95, optimize=True)
            
            return True, filename
            
        except Exception as e:
            error_msg = f"❌ Gagal download {url}: {str(e)}"
            self.failed_urls.append({"artikel_id": artikel_id, "url": url, "error": str(e)})
            return False, error_msg
    
    def download_artikel(self, artikel_id, urls):
        """Download semua gambar untuk satu artikel"""
        print(f"\n📂 Memproses artikel {artikel_id} ({len(urls)} gambar)")
        
        success_count = 0
        for i, url in enumerate(urls, start=1):
            success, result = self.download_single_image(artikel_id, url, i)
            
            if success:
                success_count += 1
                self.downloaded_count += 1
                print(f"✅ [{self.downloaded_count}/{self.total_count}] {result}")
            else:
                self.failed_count += 1
                print(f"❌ [{self.failed_count} gagal] {result}")
            
            # Progress update setiap 10 file
            if (self.downloaded_count + self.failed_count) % 10 == 0:
                self.print_progress()
        
        print(f"📊 Artikel {artikel_id}: {success_count}/{len(urls)} berhasil")
        return success_count
    
    def download_batch(self, data_dict):
        """Download semua gambar dari dictionary data"""
        # Hitung total gambar
        self.total_count = sum(len(urls) for urls in data_dict.values())
        
        print(f"🚀 Mulai download {self.total_count} gambar dari {len(data_dict)} artikel")
        print(f"📁 Output folder: {self.output_dir}")
        print("=" * 60)
        
        start_time = time.time()
        
        for artikel_id, urls in data_dict.items():
            self.download_artikel(artikel_id, urls)
        
        # Summary
        end_time = time.time()
        duration = end_time - start_time
        
        print("\n" + "=" * 60)
        print(f"🏁 SELESAI!")
        print(f"✅ Berhasil: {self.downloaded_count}")
        print(f"❌ Gagal: {self.failed_count}")
        print(f"⏱️  Waktu: {duration:.1f} detik")
        print(f"📊 Success rate: {(self.downloaded_count/self.total_count*100):.1f}%")
        
        # Simpan log error jika ada
        if self.failed_urls:
            self.save_failed_log()
    
    def print_progress(self):
        """Print progress saat ini"""
        processed = self.downloaded_count + self.failed_count
        percentage = (processed / self.total_count) * 100
        print(f"📈 Progress: {processed}/{self.total_count} ({percentage:.1f}%)")
    
    def save_failed_log(self):
        """Simpan log URL yang gagal ke file"""
        log_file = f"{self.output_dir}/failed_downloads.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(self.failed_urls, f, indent=2, ensure_ascii=False)
        print(f"📝 Log error disimpan: {log_file}")
    
    def load_from_json(self, json_file):
        """Load data dari file JSON"""
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_from_csv(self, csv_file):
        """Load data dari file CSV (format: artikel_id,url)"""
        data = {}
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header jika ada
            
            for row in reader:
                if len(row) >= 2:
                    artikel_id, url = row[0], row[1]
                    if artikel_id not in data:
                        data[artikel_id] = []
                    data[artikel_id].append(url)
        return data

# Contoh data: id artikel + daftar url
data = {
    "1703127252": [
        "https://shop.mango.com/assets/rcs/pics/static/T1/fotos/SE/17031272_52.jpg?ts=1747924512864",
        "https://shop.mango.com/assets/rcs/pics/static/T1/fotos/SE/17031272_52_R.jpg?ts=1747924512864",
        "https://shop.mango.com/assets/rcs/pics/static/T1/fotos/SE/17031272_52_D8.jpg?ts=1744016729173"
    ],
    # Untuk 3000+ URLs, lebih baik pakai file JSON atau CSV
    # Contoh: downloader.load_from_json("data_urls.json")
    # atau: downloader.load_from_csv("data_urls.csv")
}

def download_both_excel_files():
    """Download images from both Excel files to separate folders"""
    
    print("🚀 Starting dual download from both Excel files...")
    print("=" * 60)
    
    # Create main hasil_download folder
    os.makedirs("hasil_download", exist_ok=True)
    
    # Download LINK IMAGE 1
    print("\n📁 LINK IMAGE 1.xlsx -> hasil_download/link_image_1/")
    downloader1 = ImageDownloader(output_dir="hasil_download/link_image_1")
    
    try:
        data1 = downloader1.load_from_json("data_url_link_image_1.json")
        print(f"📊 LINK IMAGE 1: {len(data1)} articles, {sum(len(urls) for urls in data1.values())} URLs")
        downloader1.download_batch(data1)
    except FileNotFoundError:
        print("❌ File data_url_link_image_1.json not found. Please run excel_processor.py first.")
    except Exception as e:
        print(f"❌ Error downloading LINK IMAGE 1: {e}")
    
    print("\n" + "="*60)
    
    # Download LINK IMAGE 2
    print("\n📁 LINK IMAGE 2.xlsx -> hasil_download/link_image_2/")
    downloader2 = ImageDownloader(output_dir="hasil_download/link_image_2")
    
    try:
        data2 = downloader2.load_from_json("data_url_link_image_2.json")
        print(f"📊 LINK IMAGE 2: {len(data2)} articles, {sum(len(urls) for urls in data2.values())} URLs")
        downloader2.download_batch(data2)
    except FileNotFoundError:
        print("❌ File data_url_link_image_2.json not found. Please run excel_processor.py first.")
    except Exception as e:
        print(f"❌ Error downloading LINK IMAGE 2: {e}")
    
    print("\n" + "="*60)
    print("🏁 DUAL DOWNLOAD COMPLETE!")
    print("📁 Check folders:")
    print("   - hasil_download/link_image_1/ (from LINK IMAGE 1.xlsx)")
    print("   - hasil_download/link_image_2/ (from LINK IMAGE 2.xlsx)")
    
    # Show folder contents summary
    try:
        if os.path.exists("hasil_download/link_image_1"):
            count1 = len([f for f in os.listdir("hasil_download/link_image_1") if f.endswith('.jpg')])
            print(f"   📊 Link Image 1: {count1} images downloaded")
        
        if os.path.exists("hasil_download/link_image_2"):
            count2 = len([f for f in os.listdir("hasil_download/link_image_2") if f.endswith('.jpg')])
            print(f"   📊 Link Image 2: {count2} images downloaded")
    except Exception as e:
        print(f"   ⚠️  Could not count files: {e}")

if __name__ == "__main__":
    # Pilihan download
    print("🔄 Image Downloader - Dual Excel File Support")
    print("=" * 50)
    print("1. Download from both Excel files (recommended)")
    print("2. Download from single combined file")
    print("3. Test with small sample data")
    
    choice = input("\nPilih opsi (1/2/3): ").strip()
    
    if choice == "1":
        download_both_excel_files()
    
    elif choice == "2":
        # Original single download
        downloader = ImageDownloader(output_dir="hasil_download")
        data_from_json = downloader.load_from_json("data_url_full.json")
        print(f"📊 Dataset loaded: {len(data_from_json)} articles, {sum(len(urls) for urls in data_from_json.values())} total URLs")
        
        response = input("\n❓ Start downloading? (y/n): ")
        if response.lower() in ['y', 'yes', 'ya']:
            downloader.download_batch(data_from_json)
        else:
            print("❌ Download cancelled.")
    
    elif choice == "3":
        # Test with sample data
        downloader = ImageDownloader(output_dir="hasil_download/test")
        downloader.download_batch(data)
    
    else:
        print("❌ Invalid choice. Exiting.")
