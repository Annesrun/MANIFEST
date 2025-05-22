import tensorflow as tf

# Model yolu
MODEL_PATH = 'C:/Users/Excalibur/Desktop/veripedi/ped_model_resnet.keras'
SAVE_PATH = 'C:/Users/Excalibur/Desktop/veripedi/ped_model.tflite'

print("Model yükleniyor...")
model = tf.keras.models.load_model(MODEL_PATH)
print("Model başarıyla yüklendi!")

print("\nTFLite dönüştürücü hazırlanıyor...")
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# Optimizasyonları ayarla
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_types = [tf.float32]

print("\nModel dönüştürülüyor...")
tflite_model = converter.convert()

# Modeli kaydet
print("\nModel kaydediliyor...")
with open(SAVE_PATH, 'wb') as f:
    f.write(tflite_model)

# Boyut kontrolü
model_size = len(tflite_model) / 1024 / 1024  # MB cinsinden

print(f"\nDönüştürme tamamlandı!")
print(f"Model kaydedildi: {SAVE_PATH}")
print(f"TFLite model boyutu: {model_size:.2f} MB") 