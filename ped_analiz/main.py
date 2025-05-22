import cv2
import numpy as np
import time

def kamera_analiz():
    try:
        cap = cv2.VideoCapture(0)
        analiz_sayisi = 0
        baslangic_zamani = time.time()
        
        print("\n=== Ped Analiz Başladı ===")
        print("SPACE: Analiz Et")
        print("R: Sayacı Sıfırla")
        print("Q: Çıkış")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Hedef çerçeve
            h, w = frame.shape[:2]
            merkez_w = w // 2
            merkez_h = h // 2
            hedef_genislik = w // 3
            hedef_yukseklik = h // 3
            
            x1 = merkez_w - hedef_genislik // 2
            y1 = merkez_h - hedef_yukseklik // 2
            x2 = merkez_w + hedef_genislik // 2
            y2 = merkez_h + hedef_yukseklik // 2
            
            # Çerçeveyi çiz
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
            
            # Bilgileri göster
            cv2.putText(frame, f"Analiz: {analiz_sayisi}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
            
            cv2.imshow('Ped Analizi', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord(' '):  # SPACE tuşu
                # ROI (Region of Interest)
                roi = frame[y1:y2, x1:x2]
                
                if roi.size > 0:
                    # Simetri analizi
                    height, width = roi.shape[:2]
                    if width > 1:
                        left_half = roi[:, :width//2]
                        right_half = cv2.flip(roi[:, width//2:], 1)
                        if left_half.shape == right_half.shape:
                            simetri_skoru = cv2.matchTemplate(
                                cv2.cvtColor(left_half, cv2.COLOR_BGR2GRAY),
                                cv2.cvtColor(right_half, cv2.COLOR_BGR2GRAY),
                                cv2.TM_CCOEFF_NORMED)[0][0]
                            
                            # Renk analizi
                            hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                            mask = cv2.inRange(hsv_roi, 
                                            np.array([0, 0, 180]),
                                            np.array([180, 40, 255]))
                            renk_skoru = np.sum(mask) / (mask.shape[0] * mask.shape[1] * 255)
                            
                            # Sonuçları yazdır
                            analiz_sayisi += 1
                            print(f"\n=== Ped #{analiz_sayisi} ===")
                            print(f"Simetri: %{simetri_skoru*100:.1f}")
                            print(f"Renk: %{renk_skoru*100:.1f}")
                            
                            durum = "DÜZGÜN" if (simetri_skoru > 0.6 and 
                                                renk_skoru > 0.8) else "HATALI"
                            print(f"Durum: {durum}")
            
            elif key == ord('r'):  # R tuşu
                analiz_sayisi = 0
                print("\nSayaç sıfırlandı!")
        
        cap.release()
        cv2.destroyAllWindows()
        
    except Exception as e:
        print(f"Hata: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    kamera_analiz()