# create_test_folders.py
import os

def create_test_folders():
    base_dir = r"C:\Users\Excalibur\Desktop\veripedi\test_data"
    
    # Ana klasör
    os.makedirs(base_dir, exist_ok=True)
    
    # Alt klasörler
    os.makedirs(os.path.join(base_dir, "duzgun"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "hatali"), exist_ok=True)
    
    print("Test klasörleri oluşturuldu:")
    print(f"1. {os.path.join(base_dir, 'duzgun')}")
    print(f"2. {os.path.join(base_dir, 'hatali')}")

if __name__ == "__main__":
    create_test_folders()