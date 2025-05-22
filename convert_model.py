import tensorflow as tf
import os

# Model yolu
model_path = r"C:\Users\Excalibur\Desktop\veripedi\ped_model_resnet.keras"

# Modelin var olduğunu kontrol et
if not os.path.exists(model_path):
    print(f"HATA: Model bulunamadı: {model_path}")
    exit()

print("Model yükleniyor...")
try:
    # Keras modelini yükle
    model = tf.keras.models.load_model(model_path)
    print("Model başarıyla yüklendi!")

    print("TFLite'a dönüştürülüyor...")
    # TFLite dönüştürücüsü
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    
    # Optimizasyonlar
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_types = [tf.float16]

    # Dönüştürme
    tflite_model = converter.convert()
    print("Dönüştürme tamamlandı!")

    # Kaydetme yolu
    output_path = os.path.join(os.path.dirname(model_path), 'ped_model_resnet.tflite')
    
    # TFLite modelini kaydet
    with open(output_path, 'wb') as f:
        f.write(tflite_model)
    print(f"Model kaydedildi: {output_path}")

except Exception as e:
    print(f"HATA: {str(e)}") 