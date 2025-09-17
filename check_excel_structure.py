import pandas as pd

print("🔍 Checking Excel file structures...")

# Check LINK IMAGE 1
try:
    df1 = pd.read_excel("LINK IMAGE 1.xlsx")
    print(f"\n📁 LINK IMAGE 1.xlsx ({len(df1)} rows)")
    print("Columns:", df1.columns.tolist())
    print("\nSample data:")
    print(df1.head(2))
except Exception as e:
    print(f"❌ Error reading LINK IMAGE 1: {e}")

print("\n" + "="*60)

# Check LINK IMAGE 2  
try:
    df2 = pd.read_excel("LINK IMAGE 2.xlsx")
    print(f"\n📁 LINK IMAGE 2.xlsx ({len(df2)} rows)")
    print("Columns:", df2.columns.tolist())
    print("\nSample data:")
    print(df2.head(2))
    
    # Check for ARTIKEL column specifically
    artikel_cols = [col for col in df2.columns if 'ARTIKEL' in str(col).upper()]
    print(f"\nARTIKEL-related columns: {artikel_cols}")
    
    # Check for URL columns
    url_cols = [col for col in df2.columns if 'IMAGE' in str(col).upper() or 'LINK' in str(col).upper() or 'URL' in str(col).upper()]
    print(f"URL-related columns: {url_cols}")
    
    if artikel_cols:
        print(f"\nSample ARTIKEL values:")
        print(df2[artikel_cols[0]].head(5).tolist())
        
except Exception as e:
    print(f"❌ Error reading LINK IMAGE 2: {e}")
