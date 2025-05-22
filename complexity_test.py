import time
import numpy as np
import tensorflow as tf
import cv2

def test_complexity():
    # Model yükleme
    print("Model yükleniyor...")
    model = tf.keras.models.load_model('C:/Users/Excalibur/Desktop/veripedi/ped_model_resnet.keras')
    print("Model yüklendi!")
    
    print("\n=== Karmaşıklık Analizi Başlıyor ===\n")
    
    # 1. Zaman Karmaşıklığı Testi
    print("Zaman Karmaşıklığı Testi:")
    image_sizes = [112, 224, 448]  # Farklı boyutlar için test
    times = []
    
    for size in image_sizes:
        # Test görüntüsü oluştur
        test_image = np.random.random((1, size, size, 3))
        
        # Zaman ölçümü
        start_time = time.time()
        model.predict(test_image, verbose=0)
        end_time = time.time()
        
        process_time = end_time - start_time
        times.append(process_time)
        print(f"{size}x{size} görüntü işleme süresi: {process_time*1000:.2f}ms")
    
    # 2. FPS Testi
    print("\nFPS Testi (30 saniye):")
    cap = cv2.VideoCapture(0)
    frame_count = 0
    start_time = time.time()
    
    try:
        while (time.time() - start_time) < 30:  # 30 saniye test
            ret, frame = cap.read()
            if ret:
                # Görüntüyü işle
                frame = cv2.resize(frame, (224, 224))
                frame = np.expand_dims(frame, axis=0)
                model.predict(frame, verbose=0)
                frame_count += 1
                
                # FPS göster
                if frame_count % 10 == 0:
                    current_fps = frame_count / (time.time() - start_time)
                    print(f"Anlık FPS: {current_fps:.2f}", end='\r')
    
    except KeyboardInterrupt:
        print("\nTest manuel olarak durduruldu.")
    finally:
        test_duration = time.time() - start_time
        fps = frame_count / test_duration
        print(f"\nOrtalama FPS: {fps:.2f}")
        print(f"Test süresi: {test_duration:.1f} saniye")
        print(f"İşlenen toplam görüntü: {frame_count}")
        print(f"Tahmini 1 dakikada işlenebilecek görüntü: {int(fps * 60)}")
    
    cap.release()
    
    # Sonuçları yazdır
    print("\n=== Karmaşıklık Analizi Sonuçları ===")
    print(f"Zaman Karmaşıklığı: O(n²)")  # CNN işlemleri nedeniyle
    print(f"Mekân Karmaşıklığı: O(n)")   # Doğrusal bellek kullanımı
    print(f"Ortalama FPS: {fps:.2f}")
    print(f"1 dakikada işlenebilecek görüntü sayısı: {int(fps * 60)}")
    print(f"Ortalama işlem süresi: {1000/fps:.1f}ms/frame")

if __name__ == "__main__":
    test_complexity()