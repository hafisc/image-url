import pandas as pd
import json
import os
import re

def extract_urls_from_excel():
    """Extract all URLs from Excel files and create JSON data structure"""
    
    print("📖 Reading Excel files...")
    
    # Read Excel files
    try:
        df1 = pd.read_excel("LINK IMAGE 1.xlsx")
        print(f"✅ LINK IMAGE 1.xlsx: {len(df1)} rows")
        
        df2 = pd.read_excel("LINK IMAGE 2.xlsx")
        print(f"✅ LINK IMAGE 2.xlsx: {len(df2)} rows")
        
    except Exception as e:
        print(f"❌ Error reading Excel files: {e}")
        return None
    
    # Combine dataframes
    combined_df = pd.concat([df1, df2], ignore_index=True)
    print(f"📊 Total rows: {len(combined_df)}")
    
    # Extract URLs and organize by artikel_id
    url_data = {}
    total_urls = 0
    
    for index, row in combined_df.iterrows():
        # Get artikel ID
        artikel_id = str(row.get('ARTIKEL', '')).strip()
        if not artikel_id or artikel_id == 'nan':
            continue
        
        # Initialize artikel entry
        if artikel_id not in url_data:
            url_data[artikel_id] = []
        
        # Extract URLs from all image columns
        url_columns = [col for col in combined_df.columns if 'IMAGE' in col.upper() or 'LINK' in col.upper()]
        
        for col in url_columns:
            url = str(row.get(col, '')).strip()
            if url and url != 'nan' and url.startswith('http'):
                url_data[artikel_id].append(url)
                total_urls += 1
    
    # Remove empty entries
    url_data = {k: v for k, v in url_data.items() if v}
    
    print(f"\n📊 Extraction Results:")
    print(f"   Total articles: {len(url_data)}")
    print(f"   Total URLs: {total_urls}")
    print(f"   Average URLs per article: {total_urls/len(url_data):.1f}")
    
    # Show sample data
    print(f"\n📋 Sample extracted data:")
    for i, (artikel_id, urls) in enumerate(list(url_data.items())[:3]):
        print(f"   {artikel_id}: {len(urls)} URLs")
        for j, url in enumerate(urls[:2]):
            print(f"      {j+1}. {url[:80]}...")
    
    # Save to JSON file
    output_file = "data_url_full.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(url_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Data saved to: {output_file}")
    print(f"📁 File size: {os.path.getsize(output_file)/1024:.1f} KB")
    
    return url_data

if __name__ == "__main__":
    url_data = extract_urls_from_excel()
    
    if url_data:
        print(f"\n🚀 Ready to download {sum(len(urls) for urls in url_data.values())} images!")
        print("   Run: python main.py (update to use data_url_full.json)")
