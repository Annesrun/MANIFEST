import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.applications import ResNet50V2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet_v2 import preprocess_input
import time
from sklearn.metrics import confusion_matrix, classification_report

def veri_seti_analiz(data_dir):
    """Veri setini analiz et ve görselleştir"""
    siniflar = ['duzgun', 'hatali']
    
    plt.figure(figsize=(10, 5))
    for i, sinif in enumerate(siniflar):
        # Sınıf klasörünü kontrol et
        sinif_path = os.path.join(data_dir, sinif)
        dosyalar = os.listdir(sinif_path)
        
        print(f"\n{sinif} sınıfı analizi:")
        print(f"Toplam görüntü sayısı: {len(dosyalar)}")
        
        # Örnek bir görüntüyü analiz et
        if dosyalar:
            ornek_dosya = os.path.join(sinif_path, dosyalar[0])
            img = Image.open(ornek_dosya)
            print(f"Örnek görüntü boyutu: {img.size}")
            print(f"Örnek görüntü modu: {img.mode}")
            
            # Görüntüyü göster
            plt.subplot(1, 2, i+1)
            plt.imshow(img)
            plt.title(f"{sinif} - Örnek Görüntü")
            plt.axis('off')
    
    plt.tight_layout()
    plt.show()

def goruntu_kirp(img):
    """Görüntüyü ortadan kırp"""
    # Görüntüyü numpy dizisine çevir
    img_array = np.array(img)
    
    # Ortadaki bölgeyi kırp (pedin olduğu kısım)
    h, w = img_array.shape[:2]
    crop_h = h // 3
    crop_w = w // 3
    
    start_h = h // 2 - crop_h // 2
    start_w = w // 2 - crop_w // 2
    
    cropped = img_array[start_h:start_h+crop_h, start_w:start_w+crop_w]
    return Image.fromarray(cropped)

def veri_kontrol(data_dir):
    """Veri setini kontrol et"""
    duzgun_path = os.path.join(data_dir, 'duzgun')
    hatali_path = os.path.join(data_dir, 'hatali')
    
    duzgun_files = os.listdir(duzgun_path)
    hatali_files = os.listdir(hatali_path)
    
    print(f"\nDüzgün örnek sayısı: {len(duzgun_files)}")
    print(f"Hatalı örnek sayısı: {len(hatali_files)}")
    
    # Örnek görüntüleri kontrol et
    if duzgun_files:
        img_path = os.path.join(duzgun_path, duzgun_files[0])
        img = Image.open(img_path)
        print(f"\nDüzgün örnek boyutu: {img.size}")
        print(f"Düzgün örnek modu: {img.mode}")
        
    if hatali_files:
        img_path = os.path.join(hatali_path, hatali_files[0])
        img = Image.open(img_path)
        print(f"Hatalı örnek boyutu: {img.size}")
        print(f"Hatalı örnek modu: {img.mode}")

class PedModel:
    def __init__(self):
        self.model = None
        self.image_size = (224, 224)
        self.history = None
    
    def model_olustur(self):
        # ResNet50V2 temel modelini yükle
        base_model = ResNet50V2(
            weights='imagenet',
            include_top=False,
            input_shape=(*self.image_size, 3)
        )
        
        # Son katmanları eğitilebilir yap
        for layer in base_model.layers[-30:]:
            layer.trainable = True
        
        # Gelişmiş model yapısı
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(1024, activation='relu')(x)
        x = Dropout(0.5)(x)
        x = Dense(512, activation='relu')(x)
        x = Dropout(0.3)(x)
        x = Dense(256, activation='relu')(x)
        predictions = Dense(1, activation='sigmoid')(x)
        
        model = Model(inputs=base_model.input, outputs=predictions)
        
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
            loss='binary_crossentropy',
            metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
        )
        
        model.summary()
        self.model = model
    
    def veri_yukle(self, data_dir):
        datagen = ImageDataGenerator(
            preprocessing_function=preprocess_input,
            validation_split=0.2,
            rotation_range=10,
            width_shift_range=0.1,
            height_shift_range=0.1,
            brightness_range=[0.8, 1.2],
            zoom_range=0.1,
            horizontal_flip=True,
            fill_mode='constant',
            cval=255
        )
        
        train_generator = datagen.flow_from_directory(
            data_dir,
            target_size=self.image_size,
            batch_size=32,
            class_mode='binary',
            subset='training',
            classes=['duzgun', 'hatali'],
            shuffle=True
        )
        
        validation_generator = datagen.flow_from_directory(
            data_dir,
            target_size=self.image_size,
            batch_size=32,
            class_mode='binary',
            subset='validation',
            classes=['duzgun', 'hatali'],
            shuffle=False
        )
        
        return train_generator, validation_generator
    
    def model_egit(self, data_dir, epochs=50):
        train_generator, validation_generator = self.veri_yukle(data_dir)
        
        # Sınıf ağırlıklarını hesapla
        total_duzgun = len(os.listdir(os.path.join(data_dir, 'duzgun')))
        total_hatali = len(os.listdir(os.path.join(data_dir, 'hatali')))
        weight_for_0 = (1 / total_duzgun) * (total_duzgun + total_hatali) / 2.0
        weight_for_1 = (1 / total_hatali) * (total_duzgun + total_hatali) / 2.0
        
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_accuracy',
                patience=10,
                restore_best_weights=True
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.2,
                patience=5,
                min_lr=0.00001
            ),
            tf.keras.callbacks.ModelCheckpoint(
                'best_model.keras',
                monitor='val_accuracy',
                save_best_only=True
            )
        ]
        
        history = self.model.fit(
            train_generator,
            epochs=epochs,
            validation_data=validation_generator,
            callbacks=callbacks,
            class_weight={0: weight_for_0, 1: weight_for_1},
            verbose=1
        )
        
        self.history = history
        return history

    def model_degerlendir(self, test_generator):
        predictions = self.model.predict(test_generator)
        y_pred = predictions > 0.5
        y_true = test_generator.classes
        
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_true, y_pred))
        
        print("\nSınıflandırma Raporu:")
        print(classification_report(y_true, y_pred, target_names=['Düzgün', 'Hatalı']))
        
        if self.history:
            plt.figure(figsize=(12, 4))
            
            plt.subplot(1, 2, 1)
            plt.plot(self.history.history['accuracy'])
            plt.plot(self.history.history['val_accuracy'])
            plt.title('Model Doğruluğu')
            plt.ylabel('Doğruluk')
            plt.xlabel('Epoch')
            plt.legend(['Eğitim', 'Validasyon'])
            
            plt.subplot(1, 2, 2)
            plt.plot(self.history.history['loss'])
            plt.plot(self.history.history['val_loss'])
            plt.title('Model Kaybı')
            plt.ylabel('Kayıp')
            plt.xlabel('Epoch')
            plt.legend(['Eğitim', 'Validasyon'])
            
            plt.tight_layout()
            plt.show()

class PedTester:
    def __init__(self, model_path='ped_model_resnet.keras'):
        try:
            print("Model yükleniyor...")
            self.model = load_model(model_path, compile=False)
            print("Model başarıyla yüklendi!")
            self.image_size = (224, 224)
        except Exception as e:
            print(f"Model yükleme hatası: {e}")
    
    def goruntu_isle(self, image):
        try:
            if isinstance(image, str):
                img = Image.open(image)
            else:
                img = image
            
            img = img.convert('RGB')
            img = img.resize(self.image_size)
            
            img_array = np.array(img)
            img_array = preprocess_input(img_array)  # ResNet preprocessing
            img_array = np.expand_dims(img_array, axis=0)
            
            prediction = self.model.predict(img_array, verbose=0)[0][0]
            
            threshold = 0.5  # Threshold değeri artırıldı
            result = "DÜZGÜN" if prediction < threshold else "HATALI"
            confidence = prediction if prediction >= threshold else 1 - prediction
            
            return result, confidence, f"Tahmin değeri: {prediction:.3f}"
            
        except Exception as e:
            return "HATA", 0.0, f"Görüntü işleme hatası: {str(e)}"

def kamera_analiz():
    try:
        # Kamera başlat
        cap = cv2.VideoCapture(0)
        tester = PedTester('ped_model_resnet.keras')
        
        print("\nKamera başlatıldı!")
        print("Fotoğraf çekmek için 'SPACE' tuşuna basın")
        print("Çıkmak için 'Q' tuşuna basın")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Kamera görüntüsü alınamadı!")
                break
            
            # Görüntüyü göster
            cv2.imshow('Kamera', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # Q tuşu - çıkış
                break
            elif key == ord(' '):  # Space tuşu - fotoğraf çek
                # Görüntüyü kaydet
                img_name = f"captured_{int(time.time())}.jpg"
                cv2.imwrite(img_name, frame)
                print(f"\nFotoğraf kaydedildi: {img_name}")
                
                # Görüntüyü analiz et
                img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                img_path = img_name
                
                result, confidence, message = tester.goruntu_isle(img_path)
                print("\nAnaliz Sonuçları:")
                print(f"Sonuç: {result}")
                print(f"Güven: %{confidence*100:.1f}")
                print(f"Mesaj: {message}")
                print("\nYeni fotoğraf için SPACE, çıkmak için Q tuşuna basın")
        
        # Temizlik
        cap.release()
        cv2.destroyAllWindows()
        
    except Exception as e:
        print(f"Hata: {e}")

def main():
    print("\nNe yapmak istersiniz?")
    print("1. Model eğit")
    print("2. Kamera ile analiz")
    print("3. Çıkış")
    
    choice = input("Seçiminiz (1/2/3): ")
    
    if choice == "1":
        # Mevcut eğitim kodu
        base_path = r"C:\Users\Excalibur\Desktop\veripedi\data"
        try:
            print("Veri seti kontrolü yapılıyor...")
            veri_kontrol(base_path)
            
            cevap = input("\nVeri seti kontrolü tamamlandı. Eğitime başlamak istiyor musunuz? (e/h): ")
            if cevap.lower() != 'e':
                print("İşlem iptal edildi.")
                return
            
            print("\nModel eğitimi başlatılıyor...")
            model = PedModel()
            model.model_olustur()
            history = model.model_egit(base_path)
            
            # Model değerlendirme
            _, validation_generator = model.veri_yukle(base_path)
            model.model_degerlendir(validation_generator)
            
            model.model.save('ped_model_resnet.keras')
            print("\nModel başarıyla kaydedildi!")
            
        except Exception as e:
            print(f"\nHata: {e}")
            
    elif choice == "2":
        kamera_analiz()
    
    else:
        print("Çıkış yapılıyor...")

if __name__ == "__main__":
    main()