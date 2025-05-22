# MANIFEST

## 🎯 Ped Kalite Kontrol Sistemi

Ped üretim hattında kalite kontrol için yapay zeka destekli görüntü işleme sistemi. Sistem, web arayüzü ve mobil uygulama olmak üzere iki bileşenden oluşmaktadır.

### 🌟 Özellikler

#### Web Arayüzü
- 📸 Gerçek zamanlı kamera analizi
- 📊 Detaylı performans metrikleri
- 🚀 Hızlı işlem süresi (~203ms)
- 📈 Karmaşıklık analizi
- 🔄 REST API desteği

#### Mobil Uygulama
- 📱 Android platformu desteği
- 📸 Kamera entegrasyonu
- 🔄 Gerçek zamanlı analiz
- 💾 Yerel depolama
- 📊 Analiz geçmişi

### ⚡ Performans Analizi

#### Karmaşıklık Notasyonu
- Zaman Karmaşıklığı: O(n²)
  - CNN katmanları için matris işlemleri
  - 224x224 görüntü boyutu işleme
- Mekân Karmaşıklığı: O(n)
  - Model parametreleri
  - Görüntü tamponu
 
  ### 🔬 Model Karmaşıklığı Detayları

Görüntü işleme sürecinde kullanılan algoritmik modeller:
- Derin öğrenme tabanlı CNN mimarisi (ResNet50V2)
- Çok aşamalı görsel analiz yapıları
- Kenar tespiti sonrası sınıflandırma sistemleri

#### Algoritma Karmaşıklığı
- Görüntü ön işleme: O(n)
- CNN işlemleri: O(n²)
- Sınıflandırma: O(1)
- Toplam karmaşıklık: O(n²)

#### Bellek Kullanımı
- Model boyutu: ~98MB
- Çalışma zamanı belleği: ~256MB
- Görüntü tamponu: ~2MB/frame

#### FPS Ölçümü
- Test Süresi: 1 dakika
- İşlenen Görüntü Sayısı: 295 frame
- Ortalama FPS: 4.92
- Test Cihazı: Mobil kamera (1080p)

#### Model Performansı
- Doğruluk: %100
- Hassasiyet: %100
- F1-Score: %100
- İşlem Süresi: ~203ms/frame

#### API Performansı
- Ortalama yanıt süresi: 250ms
- Maksimum eşzamanlı istek: 100/dk
- Başarı oranı: %99.9

### 🛠️ Teknolojiler

#### Web Arayüzü
- Python 3.8+
- TensorFlow 2.15.0
- Streamlit 1.29.0
- FastAPI
- OpenCV

#### Mobil Uygulama
- Flutter
- Dart
- HTTP paketi
- Image Picker
- Shared Preferences

### 📋 Gereksinimler

#### Bağımlılıklar
python
requirements.txt
streamlit==1.29.0
tensorflow==2.15.0
opencv-python==4.8.1
numpy==1.24.3
Pillow==10.1.0
fastapi==0.109.0
uvicorn==0.27.0
python-multipart==0.0.6



#### Simülasyon Ortamı
1. Python 3.8+ kurulu olmalı
2. Kamera erişimi olan bir cihaz
3. En az 4GB RAM
4. CUDA destekli GPU (opsiyonel)

#### Mobil Uygulama Gereksinimleri
1. Flutter SDK
2. Android Studio / VS Code
3. Android 6.0+ cihaz
4. USB Debugging açık olmalı

#### Kamera Özellikleri
- Desteklenen Kamera Türleri:
  - Mobil cihaz kamerası
  - Bilgisayar web kamerası
- Minimum Çözünürlük: 720p
- Önerilen Çözünürlük: 1080p
- FPS Değeri: 4.92 FPS

### ⚙️ Kurulum Talimatları

#### Web Arayüzü & API
1. Repoyu klonlayın
2. Python bağımlılıklarını yükleyin:
   bash
pip install -r requirements.txt
3. API'yi başlatın:
   bash
python api.py
4. Web arayüzünü başlatın:
   bash
streamlit run app.py


#### Mobil Uygulama
1. Flutter SDK'yı yükleyin
2. Proje dizinine gidin
3. Bağımlılıkları yükleyin:
 bash
flutter pub get
4. API adresini `lib/config.dart` dosyasında güncelleyin
5. Uygulamayı başlatın:
   bash
flutter run

### 🔗 API Kullanımı

#### POST /analyze
Görüntü analizi için endpoint

**URL:** `http://[server-ip]:8000/analyze`

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (image)

**Response:**
json
{
"status": "DÜZGÜN/HATALI",
"confidence": 0.95,
"score": 0.05
}


### 📁 Proje Yapısı
manifest/
├── web/
│ ├── app.py # Web arayüzü
│ ├── api.py # REST API
│ ├── complexity_page.py # Karmaşıklık analizi
│ └── requirements.txt # Python bağımlılıkları
│
└── mobile/
├── lib/
│ ├── main.dart # Ana uygulama
│ ├── screens/ # Ekranlar
│ ├── services/ # API servisleri
│ └── widgets/ # UI bileşenleri
└── pubspec.yaml # Flutter bağımlılıkları


### 🎥 Demo Video
[<img src="demo_thumbnail.png" width="50%">](demo_video_link)

Bu 2 dakikalık demo video: https://youtu.be/sLGqP6V0fy8
- simülasyonun gösterimi
- Mobil uygulamanın kurulumu
- Gerçek zamanlı analiz örneği
- API entegrasyonu
- Performans metrikleri

### 🏷️ Proje Detayları
- Takım Adı: MANIFEST
- GitHub Etiketi: #ttg5hackathon2025
- Teslim Tarihi: 22 Mayıs 2025 saat 12:30
- Klasör: MANIFEST

