# capture_test_images.py
import cv2
import os
from datetime import datetime

def capture_images():
    # Kamera başlat
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Hata: Kamera başlatılamadı!")
        return
        
    # Klasör yolları
    base_dir = r"C:\Users\Excalibur\Desktop\veripedi\test_data"
    duzgun_dir = os.path.join(base_dir, "duzgun")
    hatali_dir = os.path.join(base_dir, "hatali")
    
    # Klasörleri oluştur
    os.makedirs(duzgun_dir, exist_ok=True)
    os.makedirs(hatali_dir, exist_ok=True)
    
    # Sayaçlar
    duzgun_count = 0
    hatali_count = 0
    
    print("\n=== Göz Pedi Test Görüntüsü Çekme ===")
    print("\nKontroller:")
    print("SPACE: Düzgün ürün olarak kaydet")
    print("H: Hatalı ürün olarak kaydet")
    print("R: Son kaydı sil")
    print("Q: Çıkış")
    print("\nBeklenen: Her kategoriden en az 3'er görüntü")
    
    last_saved = None
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Hata: Görüntü alınamadı!")
            break
            
        # Durum bilgisini ekrana yaz
        status = f"Duzgun: {duzgun_count} | Hatali: {hatali_count}"
        cv2.putText(frame, status, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Görüntüyü göster
        cv2.imshow('Test Goruntu Cekimi', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):  # SPACE tuşu
            # Düzgün ürün olarak kaydet
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"duzgun_{timestamp}.jpg"
            filepath = os.path.join(duzgun_dir, filename)
            cv2.imwrite(filepath, frame)
            duzgun_count += 1
            last_saved = filepath
            print(f"\n✓ Düzgün ürün kaydedildi: {filename}")
            
        elif key == ord('h'):
            # Hatalı ürün olarak kaydet
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"hatali_{timestamp}.jpg"
            filepath = os.path.join(hatali_dir, filename)
            cv2.imwrite(filepath, frame)
            hatali_count += 1
            last_saved = filepath
            print(f"\n✓ Hatalı ürün kaydedildi: {filename}")
            
        elif key == ord('r'):
            # Son kaydı sil
            if last_saved and os.path.exists(last_saved):
                os.remove(last_saved)
                print(f"\n← Son kayıt silindi: {os.path.basename(last_saved)}")
                if 'duzgun' in last_saved:
                    duzgun_count -= 1
                else:
                    hatali_count -= 1
                last_saved = None
            
        elif key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    print("\n=== Çekim Tamamlandı ===")
    print(f"Düzgün ürün: {duzgun_count} adet")
    print(f"Hatalı ürün: {hatali_count} adet")
    print(f"\nGörüntüler şurada: {base_dir}")

if __name__ == "__main__":
    capture_images()
