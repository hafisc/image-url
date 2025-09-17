import pandas as pd
import json
import os
import re

def extract_urls_from_single_excel(excel_file, output_file):
    """Extract URLs from a single Excel file"""
    try:
        df = pd.read_excel(excel_file)
        print(f"✅ {excel_file}: {len(df)} rows")
        
        # Extract URLs and organize by artikel_id
        url_data = {}
        total_urls = 0
        
        for index, row in df.iterrows():
            # Get artikel ID - try different column names
            artikel_id = None
            
            # Try common ID column names
            id_columns = ['ARTIKEL', 'Ref + Color', 'REF', 'ID', 'PRODUCT_ID']
            for col in id_columns:
                if col in df.columns:
                    artikel_id = str(row.get(col, '')).strip()
                    if artikel_id and artikel_id != 'nan':
                        break
            
            if not artikel_id or artikel_id == 'nan':
                continue
            
            # Initialize artikel entry
            if artikel_id not in url_data:
                url_data[artikel_id] = []
            
            # Extract URLs from all image columns
            url_columns = [col for col in df.columns if 'IMAGE' in col.upper() or 'LINK' in col.upper()]
            
            for col in url_columns:
                url = str(row.get(col, '')).strip()
                if url and url != 'nan' and url.startswith('http'):
                    url_data[artikel_id].append(url)
                    total_urls += 1
        
        # Remove empty entries
        url_data = {k: v for k, v in url_data.items() if v}
        
        # Save to JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(url_data, f, indent=2, ensure_ascii=False)
        
        print(f"   📊 {len(url_data)} articles, {total_urls} URLs -> {output_file}")
        return url_data
        
    except Exception as e:
        print(f"❌ Error processing {excel_file}: {e}")
        return {}

def extract_urls_from_excel():
    """Extract all URLs from Excel files and create separate JSON files"""
    
    print("📖 Reading Excel files...")
    
    # Process each Excel file separately
    data1 = extract_urls_from_single_excel("LINK IMAGE 1.xlsx", "data_url_link_image_1.json")
    data2 = extract_urls_from_single_excel("LINK IMAGE 2.xlsx", "data_url_link_image_2.json")
    
    # Also create combined file for backward compatibility
    combined_data = {**data1, **data2}
    with open("data_url_full.json", 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, indent=2, ensure_ascii=False)
    
    total_articles = len(data1) + len(data2)
    total_urls = sum(len(urls) for urls in data1.values()) + sum(len(urls) for urls in data2.values())
    
    print(f"\n📊 Final Results:")
    print(f"   LINK IMAGE 1: {len(data1)} articles, {sum(len(urls) for urls in data1.values())} URLs")
    print(f"   LINK IMAGE 2: {len(data2)} articles, {sum(len(urls) for urls in data2.values())} URLs")
    print(f"   Combined: {total_articles} articles, {total_urls} URLs")
    
    print(f"\n✅ Files created:")
    print(f"   📁 data_url_link_image_1.json")
    print(f"   📁 data_url_link_image_2.json") 
    print(f"   📁 data_url_full.json (combined)")
    
    return combined_data

if __name__ == "__main__":
    url_data = extract_urls_from_excel()
    
    if url_data:
        print(f"\n🚀 Ready to download {sum(len(urls) for urls in url_data.values())} images!")
        print("   Run: python main.py (update to use data_url_full.json)")
