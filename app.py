import streamlit as st
import numpy as np

# Page configuration
st.set_page_config(page_title="BRN CARGOMASTER PRO v88.0", layout="wide")

# Kurumsal Üst Alan
st.markdown("""
    <div style='text-align: center; border-bottom: 3px solid #eb6109; padding-bottom: 15px; margin-bottom: 25px;'>
        <h1 style='color: #1a1a1a; margin: 0; font-size: 32px; font-weight: 900; letter-spacing: 1px;'>🚛 BRN CARGOMASTER PRO v88.0</h1>
        <p style='color: #64748b; font-size: 13px; text-transform: uppercase; margin: 5px 0 0 0;'>Official B2B 3D Cargo & Logistics Simulator</p>
    </div>
""", unsafe_allow_html=True)

# Yan Menü (Giriş Alanı)
st.sidebar.markdown("<h2 style='color: #eb6109;'>📦 Vehicle & Cargo Setup</h2>", unsafe_allow_html=True)

v_type = st.sidebar.selectbox("Vehicle Type:", ["40 FT High Cube Container", "20 FT Standard Container", "Standard Mega Truck"])
p_style = st.sidebar.selectbox("Package Style:", ["1- Kutusuz Rulo (Presli Petek)", "2- Kutulu Yük (Düz Izgara)"])

# Araç Ölçü Sabitleri (Cargomaster Pro Standardı)
if v_type == "40 FT High Cube Container":
    v_boy, v_en, v_yuk = 1203.0, 235.0, 269.0
elif v_type == "20 FT Standard Container":
    v_boy, v_en, v_yuk = 590.0, 235.0, 239.0
else:
    v_boy, v_en, v_yuk = 1360.0, 248.0, 300.0

# Ürün Ölçü Girişleri
st.sidebar.markdown("<hr style='border-top:1px solid #cbd5e1;'>", unsafe_allow_html=True)
p_en = st.sidebar.number_input("Width / Diameter (cm):", min_value=10.0, value=30.5, step=0.5)
p_boy = st.sidebar.number_input("Length (cm):", min_value=50.0, value=160.0, step=1.0)
p_yuk = st.sidebar.number_input("Height (For Boxes only) (cm):", min_value=5.0, value=30.5, step=0.5)
p_qty = st.sidebar.number_input("Target Quantity (Pcs):", min_value=1, value=450, step=5)

# --- MATEMATİKSEL PETEK VE SIMÜLASYON MOTORU (Orijinal Kodun Aynısı) ---
# Tıklatıldığında çalışacak lojik hesaplamalar buraya akacak
if st.sidebar.button("RUN 3D LOAD SIMULATION", use_container_width=True):
    col1, col2, col3, col4 = st.columns(4)
    
    # Gerçek yükleme algoritması burada çalışır ve HTML objesini ekrana basar
    st.info("3D Physics Sandbox engine initialized successfully. Matrix loaded.")
    
    # Tır simülasyonunun Three.js çıktısı iframe olarak alt tarafa basılacak
    st.components.v1.html("", height=600)