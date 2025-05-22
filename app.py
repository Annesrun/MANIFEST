import streamlit as st
import cv2
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
import tensorflow as tf
from datetime import datetime
import json
import os

# Sayfa yapılandırması
st.set_page_config(page_title="Ped Analiz", layout="wide")

# Model yükleme
@st.cache_resource
def load_keras_model():
    try:
        model = load_model("C:/Users/Excalibur/Desktop/veripedi/ped_model_resnet.keras")
        return model
    except Exception as e:
        st.error(f"Model yüklenemedi: {e}")
        return None

def preprocess_image(img_array):
    """Görüntüyü model için hazırla"""
    img = cv2.resize(img_array, (224, 224))
    img = tf.keras.applications.resnet_v2.preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    return img

def analyze_image(img_array, model):
    """Model ile analiz yap"""
    try:
        processed_img = preprocess_image(img_array)
        prediction = model.predict(processed_img, verbose=0)
        score = prediction[0][0]
        
        # Threshold kontrolü (0.5 olarak güncellendi)
        threshold = 0.5
        sonuc = "DÜZGÜN" if score < threshold else "HATALI"
        confidence = 1 - score if score < threshold else score
        
        return sonuc, float(confidence)
    except Exception as e:
        st.error(f"Analiz hatası: {e}")
        return "HATALI", 0.0

# Sayaçları yükle
if 'counts' not in st.session_state:
    st.session_state.counts = {
        "toplam": 0,
        "duzgun": 0,
        "hatali": 0,
        "son_analizler": []
    }

# Model yükle
model = load_keras_model()

# Ana düzen
col1, col2 = st.columns([2, 1])

with col1:
    camera_input = st.camera_input("", key="camera")
    
    if camera_input and model:
        img = Image.open(camera_input)
        img_array = np.array(img)
        
        # Model ile analiz
        sonuc, guven = analyze_image(img_array, model)
        
        # Sayaçları güncelle
        st.session_state.counts["toplam"] += 1
        if sonuc == "DÜZGÜN":
            st.session_state.counts["duzgun"] += 1
            st.success(f"✅ DÜZGÜN (Güven: {guven:.2%})")
        else:
            st.session_state.counts["hatali"] += 1
            st.error(f"❌ HATALI (Güven: {guven:.2%})")
        
        # Son analizlere ekle
        now = datetime.now().strftime("%H:%M:%S")
        st.session_state.counts["son_analizler"].insert(0, f"{now} - {sonuc}")
        if len(st.session_state.counts["son_analizler"]) > 5:
            st.session_state.counts["son_analizler"].pop()

with col2:
    st.header("📊 Günlük Özet")
    
    # Metrikler
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Toplam", st.session_state.counts["toplam"])
        st.metric("Düzgün", st.session_state.counts["duzgun"])
    with col_b:
        st.metric("Hatalı", st.session_state.counts["hatali"])
        basari = (st.session_state.counts["duzgun"] / st.session_state.counts["toplam"] * 100) if st.session_state.counts["toplam"] > 0 else 0
        st.metric("Başarı", f"{basari:.1f}%")
    
    # Son analizler
    st.subheader("🕒 Son Analizler")
    for analiz in st.session_state.counts["son_analizler"]:
        icon = "✅" if "DÜZGÜN" in analiz else "❌"
        st.text(f"{icon} {analiz}")

# Analiz adımları
st.markdown("""
### 📋 Analiz Adımları
1. **Görüntü İşleme ile Tanıma**: Pedin bütün olarak tanınması
2. **Parça Bazlı Kontrol**: Kenar kesimlerinin düzgünlüğü ve simetri analizi
3. **Sağlamlık Tespiti**: Yırtık, eziklik kontrolü
4. **Renk ve Leke Tespiti**: Üretim hatası ve leke kontrolü
""")
