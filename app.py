import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ==========================================
# 1. SAYFA VE ARAYÜZ AYARLARI
# ==========================================
st.set_page_config(page_title="CargoMaster Pro 3D", layout="wide", page_icon="🚛")

st.markdown("""
    <div style='background-color:#1a1a1a; padding:15px; border-radius:10px; border-left: 5px solid #eb6109;'>
        <h2 style='color:white; margin:0;'>🚛 CARGOMASTER PRO - 3D Yükleme Optimizasyonu</h2>
        <p style='color:#cbd5e1; margin:0;'>BRN Sleep Products - Konteyner ve Tır Simülatörü</p>
    </div>
    <br>
""", unsafe_allow_html=True)

# ==========================================
# 2. YAN PANEL (KULLANICI GİRİŞLERİ)
# ==========================================
st.sidebar.header("📐 Lojistik Parametreleri")

konteyner_tipi = st.sidebar.selectbox("Konteyner / Tır Tipi", [
    "40HC Konteyner (1203 x 235 x 269 cm)", 
    "20DC Konteyner (589 x 235 x 239 cm)",
    "Standart Tır (1360 x 240 x 270 cm)"
])

st.sidebar.markdown("---")
st.sidebar.subheader("📦 Ürün / Koli Ölçüleri (cm)")
koli_en = st.sidebar.number_input("Koli Eni (W)", min_value=10, value=35, step=1)
koli_boy = st.sidebar.number_input("Koli Boyu (L)", min_value=10, value=170, step=1)
koli_yukseklik = st.sidebar.number_input("Koli Yüksekliği (H)", min_value=10, value=35, step=1)

siparis_adeti = st.sidebar.number_input("Sipariş Adeti", min_value=1, value=400, step=10)

# Konteyner Ebatlarını Ayrıştırma
if "40HC" in konteyner_tipi:
    C_L, C_W, C_H = 1203, 235, 269
elif "20DC" in konteyner_tipi:
    C_L, C_W, C_H = 589, 235, 239
else:
    C_L, C_W, C_H = 1360, 240, 270

# ==========================================
# 3. YÜKLEME ALGORİTMASI (GRID BPP)
# ==========================================
# X ekseni = Boy (L), Y ekseni = En (W), Z ekseni = Yükseklik (H)
adet_x = C_L // koli_boy
adet_y = C_W // koli_en
adet_z = C_H // koli_yukseklik

maksimum_kapasite = adet_x * adet_y * adet_z
yuklenecek_adet = min(siparis_adeti, maksimum_kapasite)
sigan_hacim_m3 = (yuklenecek_adet * (koli_en * koli_boy * koli_yukseklik)) / 1_000_000
konteyner_hacim_m3 = (C_L * C_W * C_H) / 1_000_000
doluluk_orani = (sigan_hacim_m3 / konteyner_hacim_m3) * 100

# ==========================================
# 4. KPI DASHBOARD (ÖZET KARTLARI)
# ==========================================
col1, col2, col3, col4 = st.columns(4)
col1.metric("📦 Yüklenen Koli", f"{yuklenecek_adet} / {siparis_adeti}")
col2.metric("🟢 Maksimum Kapasite", f"{maksimum_kapasite} Adet")
col3.metric("🧊 Yük Hacmi (m³)", f"{sigan_hacim_m3:.1f} m³")
col4.metric("📊 Doluluk Oranı", f"% {doluluk_orani:.1f}")

if siparis_adeti > maksimum_kapasite:
    st.warning(f"⚠️ Dikkat: Sipariş adeti konteyner kapasitesini aşıyor! {siparis_adeti - maksimum_kapasite} adet ürün dışarıda kaldı.")
else:
    st.success("✅ Tüm sipariş konteynere başarıyla sığdı.")

# ==========================================
# 5. 3D ÇİZİM MOTORU (PLOTLY)
# ==========================================
def draw_box(fig, x, y, z, dx, dy, dz, color):
    # Bir kolinin 8 köşesini tanımlayan noktalar (Wireframe/Line çizimi)
    xx = [x, x+dx, x+dx, x, x, x, x+dx, x+dx, x, x, x+dx, x+dx, x+dx, x+dx, x, x]
    yy = [y, y, y+dy, y+dy, y, y, y, y+dy, y+dy, y, y, y, y+dy, y+dy, y+dy, y+dy]
    zz = [z, z, z, z, z, z+dz, z+dz, z+dz, z+dz, z+dz, z+dz, z, z, z+dz, z+dz, z]
    
    fig.add_trace(go.Scatter3d(
        x=xx, y=yy, z=zz,
        mode='lines',
        line=dict(color=color, width=3),
        showlegend=False,
        hoverinfo='skip'
    ))

fig = go.Figure()

# 1. Konteynerin Dış İskeletini Çiz (Yarı Şeffaf Siyah)
draw_box(fig, 0, 0, 0, C_L, C_W, C_H, 'rgba(0,0,0,0.3)')

# 2. Yüklenen Kolileri 3D Olarak Çiz
sayac = 0
for z_idx in range(adet_z):
    for y_idx in range(adet_y):
        for x_idx in range(adet_x):
            if sayac < yuklenecek_adet:
                pos_x = x_idx * koli_boy
                pos_y = y_idx * koli_en
                pos_z = z_idx * koli_yukseklik
                # En üst sıradakileri farklı renk yapalım ki şık dursun
                renk = '#eb6109' if z_idx == (adet_z - 1) else '#1a1a1a'
                draw_box(fig, pos_x, pos_y, pos_z, koli_boy, koli_en, koli_yukseklik, renk)
                sayac += 1
            else:
                break

# 3D Grafik Kamera ve Sahne Ayarları
fig.update_layout(
    scene=dict(
        xaxis=dict(title='Boy (cm)', range=[-100, C_L+100], backgroundcolor="#f8fafc"),
        yaxis=dict(title='En (cm)', range=[-100, C_W+100], backgroundcolor="#f8fafc"),
        zaxis=dict(title='Yükseklik (cm)', range=[-10, C_H+50], backgroundcolor="#f8fafc"),
        aspectratio=dict(x=C_L/300, y=C_W/300, z=C_H/300),
        camera=dict(eye=dict(x=1.8, y=-1.8, z=0.8)) # Kamera açısı
    ),
    margin=dict(l=0, r=0, b=0, t=0),
    height=600
)

st.plotly_chart(fig, use_container_width=True)
