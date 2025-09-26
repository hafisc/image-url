import pandas as pd

print("🔍 Checking Excel file structure...")

# Check IMAGE 26.09.2025.xlsx
try:
    df = pd.read_excel("IMAGE 26.09.2025.xlsx")
    print(f"\n📁 IMAGE 26.09.2025.xlsx ({len(df)} rows)")
    print("Columns:", df.columns.tolist())
    print("\nSample data:")
    print(df.head(3))
    
    # Check for ID/ARTIKEL column specifically
    id_cols = [col for col in df.columns if any(keyword in str(col).upper() for keyword in ['ARTIKEL', 'REF', 'ID', 'PRODUCT', 'SKU', 'CODE'])]
    print(f"\nID-related columns: {id_cols}")
    
    # Check for URL columns
    url_cols = [col for col in df.columns if any(keyword in str(col).upper() for keyword in ['IMAGE', 'LINK', 'URL', 'HTTP', 'PHOTO', 'PIC'])]
    print(f"URL-related columns: {url_cols}")
    
    # Show all column names for analysis
    print(f"\nAll columns ({len(df.columns)}):")
    for i, col in enumerate(df.columns):
        print(f"  {i+1:2d}. {col}")
    
    if id_cols:
        print(f"\nSample ID values from '{id_cols[0]}':")
        print(df[id_cols[0]].head(5).tolist())
    
    if url_cols:
        print(f"\nSample URL values from '{url_cols[0]}':")
        sample_urls = df[url_cols[0]].dropna().head(3).tolist()
        for url in sample_urls:
            print(f"  {url}")
        
except Exception as e:
    print(f"❌ Error reading IMAGE 26.09.2025.xlsx: {e}")
