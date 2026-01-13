"""
Download winutils.exe for Windows Spark compatibility.
This downloads the Hadoop winutils binary needed for Spark on Windows.
"""
import os
import urllib.request
import sys

def download_winutils():
    # Hadoop version compatible with Spark
    hadoop_version = "3.3.6"
    
    # Create hadoop/bin directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    hadoop_home = os.path.join(script_dir, 'hadoop')
    bin_dir = os.path.join(hadoop_home, 'bin')
    os.makedirs(bin_dir, exist_ok=True)
    
    winutils_path = os.path.join(bin_dir, 'winutils.exe')
    hadoop_dll_path = os.path.join(bin_dir, 'hadoop.dll')
    
    # URLs for winutils.exe and hadoop.dll
    base_url = f"https://github.com/cdarlint/winutils/raw/master/hadoop-{hadoop_version}/bin/"
    winutils_url = base_url + "winutils.exe"
    hadoop_dll_url = base_url + "hadoop.dll"
    
    print(f"Downloading winutils.exe to {winutils_path}...")
    try:
        urllib.request.urlretrieve(winutils_url, winutils_path)
        print("✓ winutils.exe downloaded successfully")
    except Exception as e:
        print(f"✗ Failed to download winutils.exe: {e}")
        print("\nManual download instructions:")
        print(f"1. Download from: {winutils_url}")
        print(f"2. Save to: {winutils_path}")
        return False
    
    print(f"Downloading hadoop.dll to {hadoop_dll_path}...")
    try:
        urllib.request.urlretrieve(hadoop_dll_url, hadoop_dll_path)
        print("✓ hadoop.dll downloaded successfully")
    except Exception as e:
        print(f"✗ Failed to download hadoop.dll: {e}")
        print("\nManual download instructions:")
        print(f"1. Download from: {hadoop_dll_url}")
        print(f"2. Save to: {hadoop_dll_path}")
        return False
    
    print(f"\n✓ Setup complete! HADOOP_HOME will be set to: {hadoop_home}")
    return True

if __name__ == "__main__":
    if sys.platform != 'win32':
        print("This script is only needed on Windows.")
        sys.exit(0)
    
    success = download_winutils()
    sys.exit(0 if success else 1)
