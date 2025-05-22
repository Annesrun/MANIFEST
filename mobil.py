from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import tensorflow as tf
import numpy as np
from datetime import datetime

class PedKontrolApp(App):
    def build(self):
        # Ana layout
        self.layout = BoxLayout(orientation='vertical')
        
        # Kamera görüntüsü için
        self.img1 = Image()
        self.layout.add_widget(self.img1)
        
        # Sonuç etiketi
        self.label = Label(text="Bekleniyor...", size_hint=(1, .1))
        self.layout.add_widget(self.label)
        
        # Kontrol butonları
        btn_layout = BoxLayout(size_hint=(1, .1))
        self.start_button = Button(text="Başlat")
        self.start_button.bind(on_press=self.baslat)
        btn_layout.add_widget(self.start_button)
        
        self.stop_button = Button(text="Durdur")
        self.stop_button.bind(on_press=self.durdur)
        btn_layout.add_widget(self.stop_button)
        
        self.layout.add_widget(btn_layout)
        
        # Model yükle
        self.model = tf.keras.models.load_model('ped_model_resnet_improved.keras')
        
        # Kamera başlat
        self.capture = cv2.VideoCapture(0)
        self.is_running = False
        
        return self.layout
    
    def baslat(self, instance):
        """Kamera analizi başlat"""
        self.is_running = True
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # 30 FPS
        
    def durdur(self, instance):
        """Kamera analizi durdur"""
        self.is_running = False
        Clock.unschedule(self.update)
        
    def goruntu_isle(self, frame):
        """Görüntü analizi yap"""
        # Görüntüyü yeniden boyutlandır
        img = cv2.resize(frame, (224, 224))
        
        # BGR'den RGB'ye çevir
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Normalize et ve boyutları düzenle
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)
        
        # Tahmin yap
        prediction = self.model.predict(img_array, verbose=0)[0][0]
        
        # Sonucu yorumla
        result = "DÜZGÜN" if prediction < 0.5 else "HATALI"
        confidence = prediction if prediction >= 0.5 else 1 - prediction
        
        return result, confidence
    
    def update(self, dt):
        """Kamera görüntüsünü güncelle"""
        if not self.is_running:
            return
            
        # Kameradan görüntü al
        ret, frame = self.capture.read()
        if ret:
            # Görüntüyü analiz et
            result, confidence = self.goruntu_isle(frame)
            
            # Sonucu ekrana yaz
            cv2.putText(frame, f"{result} (%{confidence*100:.1f})", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                       (0, 255, 0) if result == "DÜZGÜN" else (0, 0, 255), 2)
            
            # Hatalı ürün ise kaydet
            if result == "HATALI":
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                cv2.imwrite(f"hatali_{timestamp}.jpg", frame)
            
            # Görüntüyü Kivy texture'una dönüştür
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            
            # Görüntüyü güncelle
            self.img1.texture = texture1
            
            # Label'ı güncelle
            self.label.text = f"Sonuç: {result} (Güven: %{confidence*100:.1f})"

if __name__ == '__main__':
    PedKontrolApp().run()
