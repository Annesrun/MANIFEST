# test_model.py
from proje import PedTester
import os
import cv2
import time
from PIL import Image
import numpy as np

def ped_tespiti(roi):
    """Görüntüde ped olup olmadığını kontrol eder"""
    try:
        # Gri tonlama ve bulanıklaştırma
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        
        # Adaptif eşikleme
        thresh = cv2.adaptiveThreshold(blur, 255, 
                                     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, 11, 2)
        
        # Kontur bulma
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, 
                                     cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return False, None, "Kontur bulunamadı"
        
        # En büyük konturu bul
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        
        # Alan kontrolü
        if area < 1000:  # Eşik değeri düşürüldü
            return False, None, f"Alan çok küçük: {area}"
        
        # Renk kontrolü (beyaz bölge oranı)
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        lower_white = np.array([0, 0, 150])  # Değerler esnetildi
        upper_white = np.array([180, 60, 255])
        mask = cv2.inRange(hsv, lower_white, upper_white)
        white_ratio = np.sum(mask) / (mask.shape[0] * mask.shape[1])
        
        if white_ratio < 0.3:  # Eşik değeri düşürüldü
            return False, None, f"Beyaz oranı düşük: {white_ratio:.2f}"
        
        return True, largest_contour, "Ped tespit edildi"
        
    except Exception as e:
        return False, None, f"Hata: {str(e)}"

def kamera_analiz():
    try:
        cap = cv2.VideoCapture(0)
        tester = PedTester('ped_model_resnet.keras')
        
        analiz_sayisi = 0
        baslangic_zamani = time.time()
        TEST_SURESI = 30
        son_mesaj = ""
        
        print("\n=== Ped Analiz Testi ===")
        print("Yeşil çerçeveye pedi yerleştirin")
        print("SPACE: Analiz Et")
        print("Q: Çıkış")
        print(f"Test süresi: {TEST_SURESI} saniye")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            gecen_sure = time.time() - baslangic_zamani
            kalan_sure = max(0, TEST_SURESI - gecen_sure)
            
            if kalan_sure == 0:
                print("\n=== Test Tamamlandı! ===")
                print(f"Toplam analiz: {analiz_sayisi} ped")
                print(f"Hız: {analiz_sayisi / (TEST_SURESI/60):.1f} ped/dk")
                break
            
            # Hedef çerçeve
            h, w = frame.shape[:2]
            merkez_w, merkez_h = w // 2, h // 2
            hedef_genislik = w // 2  # Çerçeve büyütüldü
            hedef_yukseklik = h // 2
            
            x1 = merkez_w - hedef_genislik // 2
            y1 = merkez_h - hedef_yukseklik // 2
            x2 = merkez_w + hedef_genislik // 2
            y2 = merkez_h + hedef_yukseklik // 2
            
            # ROI
            roi = frame[y1:y2, x1:x2]
            
            # Ped tespiti
            ped_var, kontur, mesaj = ped_tespiti(roi)
            son_mesaj = mesaj  # Son mesajı sakla
            
            # Çerçeve rengini belirle
            cerceve_renk = (0,255,0) if ped_var else (0,0,255)
            cv2.rectangle(frame, (x1,y1), (x2,y2), cerceve_renk, 2)
            
            # Bilgileri göster
            cv2.putText(frame, f"Kalan: {int(kalan_sure)}s", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
            cv2.putText(frame, f"Analiz: {analiz_sayisi}", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
            cv2.putText(frame, son_mesaj, (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, cerceve_renk, 2)
            
            cv2.imshow('Ped Analizi', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord(' ') and ped_var:
                # Analiz
                analiz_sayisi += 1
                print(f"\n=== Ped #{analiz_sayisi} ===")
                
                # Simetri analizi
                height, width = roi.shape[:2]
                left_half = roi[:, :width//2]
                right_half = cv2.flip(roi[:, width//2:], 1)
                simetri_skoru = cv2.matchTemplate(
                    cv2.cvtColor(left_half, cv2.COLOR_BGR2GRAY),
                    cv2.cvtColor(right_half, cv2.COLOR_BGR2GRAY),
                    cv2.TM_CCOEFF_NORMED)[0][0]
                
                # Renk analizi
                hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv_roi, np.array([0, 0, 150]), np.array([180, 60, 255]))
                renk_skoru = np.sum(mask) / (mask.shape[0] * mask.shape[1] * 255)
                
                # Sonuçlar
                print(f"Simetri: %{simetri_skoru*100:.1f}")
                print(f"Renk: %{renk_skoru*100:.1f}")
                
                durum = "DÜZGÜN" if (simetri_skoru > 0.6 and renk_skoru > 0.8) else "HATALI"
                print(f"Durum: {durum}")
                print("\nSıradaki ped için hazır...")
                
                time.sleep(1)  # Sonucu görmek için bekle
        
        cap.release()
        cv2.destroyAllWindows()
        
    except Exception as e:
        print(f"Hata: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    kamera_analiz()