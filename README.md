# MANIFEST
# Ped Kalite Kontrol Sistemi

Ped üretim hattında kalite kontrol için yapay zeka destekli görüntü işleme sistemi. Sistem, web arayüzü ve mobil uygulama olmak üzere iki bileşenden oluşmaktadır.

---

## 🌟 Özellikler

### Web Arayüzü
- 📸 Gerçek zamanlı kamera analizi
- 📊 Detaylı performans metrikleri
- 🚀 Hızlı işlem süresi (~203ms)
- 📈 Karmaşıklık analizi
- 🔄 REST API desteği

### Mobil Uygulama
- 📱 Android platformu desteği
- 📸 Kamera entegrasyonu
- 🔄 Gerçek zamanlı analiz
- 💾 Yerel depolama
- 📊 Analiz geçmişi

---

## 📋 Gereksinimler

### Bağımlılıklar

`requirements.txt` içeriği:
```plaintext
streamlit==1.29.0
tensorflow==2.15.0
opencv-python==4.8.1
numpy==1.24.3
Pillow==10.1.0
fastapi==0.109.0
uvicorn==0.27.0
python-multipart==0.0.6

🛠️ Teknolojiler
Web Arayüzü
Python 3.8+

TensorFlow 2.15.0

Streamlit 1.29.0

FastAPI

OpenCV

Mobil Uygulama
Flutter

Dart

HTTP paketi

Image Picker

Shared Preferences

📊 Performans Metrikleri
Model Performansı
Doğruluk: %99.89

F1-Score: %98.78

İşlem Süresi: ~203ms/frame

API Performansı
Ortalama yanıt süresi: 250ms

Maksimum eşzamanlı istek: 100/dk

Başarı oranı: %99.9

⚡ Performans Analizi
Zaman Karmaşıklığı: O(n²)
CNN katmanları için matris işlemleri, 224x224 görüntü boyutu işleme

Mekân Karmaşıklığı: O(n)
Model parametreleri, görüntü tamponu

FPS Ölçümü
Test Süresi: 1 dakika

İşlenen Görüntü Sayısı: 295 frame

Ortalama FPS: 4.92

Test Cihazı: Mobil kamera (1080p)

Kamera Özellikleri
Desteklenen Kamera Türleri:
Mobil cihaz kamerası, Bilgisayar web kamerası

Minimum Çözünürlük: 720p

Önerilen Çözünürlük: 1080p

FPS Değeri: 4.92 FPS

👥 Ekip
Takım lideri : Nursena Albayrak

Mobil Uygulama Geliştirici: Elif Ceren Kuru

Simülasyon : Aylin Şimşek

Model Eğitimi : Feyzanur İnan

🔗 API Kullanımı
POST /analyze
Görüntü analizi için endpoint

URL: http://[server-ip]:8000/analyze

Request:

Method: POST

Content-Type: multipart/form-data

Body: file (image)

Response:

json
Kopyala
{
  "status": "DÜZGÜN/HATALI",
  "confidence": 0.95,
  "score": 0.05
}
⚙️ Kurulum Talimatları
Web Arayüzü & API
bash
Kopyala
# Repoyu klonlayın
git clone <repo-url>
cd <repo-dizin>

# Python bağımlılıklarını yükleyin
pip install -r requirements.txt

# API'yi başlatın
python api.py

# Web arayüzünü başlatın
streamlit run app.py
Mobil Uygulama
bash
Kopyala
# Flutter SDK'yı yükleyin ve yapılandırın

# Proje dizinine gidin
cd mobile/

# Bağımlılıkları yükleyin
flutter pub get

# API adresini lib/config.dart dosyasında güncelleyin

# Uygulamayı başlatın
flutter run
📁 Proje Yapısı
bash
Kopyala
manifest/
├── web/
│   ├── app.py                # Web arayüzü
│   ├── api.py                # REST API
│   ├── complexity_page.py    # Karmaşıklık analizi
│   └── requirements.txt      # Python bağımlılıkları
└── mobile/
    ├── lib/
    │   ├── main.dart         # Ana uygulama
    │   ├── screens/          # Ekranlar
    │   ├── services/         # API servisleri
    │   └── widgets/          # UI bileşenleri
    └── pubspec.yaml          # Flutter bağımlılıkları
Simülasyon Ortamı
Python 3.8+ kurulu olmalı

Kamera erişimi olan bir cihaz

En az 4GB RAM

CUDA destekli GPU (opsiyonel)

Mobil Uygulama Gereksinimleri
Flutter SDK

Android Studio / VS Code

Android 6.0+ cihaz

USB Debugging açık olmalı

🎥 Demo Video
Bu 2 dakikalık demo video:

Web arayüzünün kullanımı

Mobil uygulamanın kurulumu

Gerçek zamanlı analiz örneği

API entegrasyonu

Performans metrikleri

Demo videoyu izlemek için tıklayın

🔍 Test Senaryoları
Normal ped görüntüsü analizi

Hatalı ped görüntüsü analizi

Farklı ışık koşullarında test

Farklı açılardan test

Stres testi (100 görüntü/dakika)

⚠️ Bilinen Sorunlar
Çok düşük ışıkta analiz hassasiyeti düşebilir

API'ye aynı anda 100'den fazla istek gelirse yavaşlama olabilir

📱 Desteklenen Platformlar
Web Arayüzü: Tüm modern tarayıcılar (Chrome, Firefox, Edge)

Mobil Uygulama: Android 6.0 ve üzeri

API: Platform bağımsız

🔜 Gelecek Güncellemeler
iOS desteği

Offline mod

Toplu analiz özelliği

Detaylı raporlama sistemi











