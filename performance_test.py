import cv2
import time
import tensorflow as tf
import numpy as np

def test_model_performance():
    # Model yükleme
    interpreter = tf.lite.Interpreter(model_path="C:/Users/Excalibur/Desktop/veripedi/ped_model.tflite")
    interpreter.allocate_tensors()
    
    # Kamera başlatma
    cap = cv2.VideoCapture(0)
    
    # FPS hesaplama için değişkenler
    fps_start_time = time.time()
    fps = 0
    frame_count = 0
    total_frames = 0
    processing_times = []
    
    print("Performance testi başlıyor...")
    print("Test süresi: 60 saniye")
    
    while True:
        # Frame yakala
        ret, frame = cap.read()
        if not ret:
            break
            
        # İşleme başlama zamanı
        start_time = time.time()
        
        # Görüntü ön işleme
        img = cv2.resize(frame, (224, 224))
        img = img.astype(np.float32)
        img = np.expand_dims(img, axis=0)
        
        # Model tahmini
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        
        interpreter.set_tensor(input_details[0]['index'], img)
        interpreter.invoke()
        prediction = interpreter.get_tensor(output_details[0]['index'])
        
        # İşleme süresi hesaplama
        process_time = time.time() - start_time
        processing_times.append(process_time)
        
        # FPS hesaplama
        frame_count += 1
        total_frames += 1
        
        if time.time() - fps_start_time >= 1:
            fps = frame_count
            frame_count = 0
            fps_start_time = time.time()
        
        # Ekrana bilgi yazdırma
        cv2.putText(frame, f'FPS: {fps}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f'Process Time: {process_time*1000:.1f}ms', (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Görüntüyü göster
        cv2.imshow('Performance Test', frame)
        
        # 60 saniye sonra veya q tuşuna basılınca çık
        if cv2.waitKey(1) & 0xFF == ord('q') or time.time() - fps_start_time > 60:
            break
    
    # Sonuçları hesapla
    avg_fps = total_frames / 60
    avg_process_time = sum(processing_times) / len(processing_times)
    max_process_time = max(processing_times)
    min_process_time = min(processing_times)
    
    # Sonuçları yazdır
    print("\nPerformans Test Sonuçları:")
    print(f"Ortalama FPS: {avg_fps:.2f}")
    print(f"Ortalama İşleme Süresi: {avg_process_time*1000:.2f}ms")
    print(f"Maksimum İşleme Süresi: {max_process_time*1000:.2f}ms")
    print(f"Minimum İşleme Süresi: {min_process_time*1000:.2f}ms")
    print(f"1 Dakikada İşlenen Toplam Frame: {total_frames}")
    
    # Temizlik
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_model_performance() 