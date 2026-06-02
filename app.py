import streamlit as st
import numpy as np

# 1. SAYFA AYARLARI & GENEL STİL
st.set_page_config(page_title="BRN CARGOMASTER PRO v100.0", layout="wide")

st.markdown("""
    <style>
    .main-title { color: #eb6109; font-weight: 900; letter-spacing: 1px; }
    .stButton>button { background-color: #eb6109 !important; color: white !important; font-weight: bold !important; border: none !important; }
    .stButton>button:hover { background-color: #1a1a1a !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# Kurumsal Üst Başlık
st.markdown("""
    <div style='text-align: center; border-bottom: 3px solid #eb6109; padding-bottom: 15px; margin-bottom: 25px;'>
        <h1 style='color: #1a1a1a; margin: 0; font-size: 32px; font-weight: 900; letter-spacing: 1px;'>🚛 BRN CARGOMASTER PRO v100.0</h1>
        <p style='color: #64748b; font-size: 13px; text-transform: uppercase; margin: 5px 0 0 0;'>Official B2B 3D Cargo & Logistics Simulator</p>
    </div>
""", unsafe_allow_html=True)

# 2. SOL PANEL (GİRİŞ PARAMETRELERİ)
st.sidebar.markdown("<h3 style='color: #eb6109; margin:0;'>📦 Cargo & Vehicle Setup</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='margin:10px 0;'>", unsafe_allow_html=True)

v_type = st.sidebar.selectbox("Vehicle Type:", ["40 FT High Cube Container", "20 FT Standard Container", "Standard Mega Truck"])
p_style = st.sidebar.selectbox("Package Style:", ["1- Kutusuz Rulo (Presli Petek)", "2- Kutulu Yük (Düz Izgara)"])

# Araç Ölçü Sabitleri (cm cinsinden iç hacim ölçüleri)
if v_type == "40 FT High Cube Container":
    v_boy, v_en, v_yuk = 1203.0, 235.0, 269.0
elif v_type == "20 FT Standard Container":
    v_boy, v_en, v_yuk = 590.0, 235.0, 239.0
else: # Standard Mega Truck
    v_boy, v_en, v_yuk = 1360.0, 248.0, 300.0

st.sidebar.markdown("<b style='color:#64748b; font-size:12px;'>PRODUCT DIMENSIONS</b>", unsafe_allow_html=True)
p_en = st.sidebar.number_input("Width / Diameter (cm):", min_value=10.0, value=30.0, step=0.5)
p_boy = st.sidebar.number_input("Length (cm):", min_value=50.0, value=160.0, step=1.0)
p_yuk = st.sidebar.number_input("Height (For Boxes Only) (cm):", min_value=5.0, value=30.0, step=0.5)
p_qty = st.sidebar.number_input("Target Order Quantity (Pcs):", min_value=1, value=450, step=10)

# 3. LOJİSTİK HESAPLAMA MOTORU (ORİJİNAL KODUN AYNISI)
is_roll = "Rulo" in p_style

if is_roll:
    # Rulo için silindirik hacim korumalı petek matrisi (Sin60 verimliliği)
    d = p_en
    roll_len = min(p_en, p_boy) if p_en != p_boy else p_en
    if roll_len < 50: roll_len = p_boy 
    
    # En iyi rotasyonu bulmak için 3 yönü de simüle et
    # Rotasyon 1: Enlemesine Yatay
    N1 = int(v_en // d)
    N2 = max(1, N1 - 1)
    layers = int((v_yuk - d) // (d * 0.866)) + 1 if v_yuk >= d else 0
    rps = sum([(N1 if l % 2 == 0 else N2) for l in range(layers)]) if layers > 0 else 0
    slices = int(v_boy // roll_len)
    qty1 = slices * rps
    
    # Rotasyon 2: Boylamasına Yatay
    N1_s = int(v_boy // d)
    N2_s = max(1, N1_s - 1)
    layers_s = int((v_yuk - d) // (d * 0.866)) + 1 if v_yuk >= d else 0
    rps_s = sum([(N1_s if l % 2 == 0 else N2_s) for l in range(layers_s)]) if layers_s > 0 else 0
    slices_s = int(v_en // roll_len)
    qty2 = slices_s * rps_s
    
    # Rotasyon 3: Dikine Ayakta Durma
    N1_v = int(v_en // d)
    N2_v = max(1, N1_v - 1)
    depthLayers = int((v_boy - d) // (d * 0.866)) + 1 if v_boy >= d else 0
    rps_v = sum([(N1_v if l % 2 == 0 else N2_v) for l in range(depthLayers)]) if depthLayers > 0 else 0
    slices_v = int(v_yuk // roll_len)
    qty3 = slices_v * rps_v
    
    calc_max = max(qty1, qty2, qty3)
    best_orientation = "Enlemesine Yatay" if calc_max == qty1 else ("Boylamasına Yatay" if calc_max == qty2 else "Dikey Ayakta")
else:
    # Kutulu yük için 3D Grid Optimizasyonu (6 Farklı kombinasyon testi)
    dims = [p_en, p_boy, p_yuk]
    perms = [[0,1,2], [0,2,1], [1,0,2], [1,2,0], [2,0,1], [2,1,0]]
    calc_max = 0
    best_orientation = "Düz Izgara Standart"
    for p in perms:
        q = int(v_boy // dims[p[0]]) * int(v_en // dims[p[1]]) * int(v_yuk // dims[p[2]])
        if q > calc_max:
            calc_max = q

# Gerçek Hayat Emniyet Toleransı (%98 Emniyet Katsayısı)
calc_max = int(calc_max * 0.98)
fill_rate = min(100.0, (p_qty / max(1, calc_max)) * 100.0)
status_color = "#2e7d32" if fill_rate <= 100 else "#d32f2f"

# 4. ANA EKRAN ÇIKTILARI (KPI KARTLARI)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Vehicle Capacity", f"{calc_max} Pcs")
with col2:
    st.metric("Your Order Quantity", f"{p_qty} Pcs")
with col3:
    # Renkli Doluluk Oranı Göstergesi
    st.markdown(f"""
        <div style="background: #ffffff; padding: 10px; border-radius: 8px; border-left: 5px solid {status_color}; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <small style="color:#64748b; font-weight:bold; text-transform:uppercase;">Vehicle Utilization</small><br>
            <b style="font-size:22px; color:{status_color};">{fill_rate:.1f}%</b>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 5. 🔥 Gelişmiş 3D THREE.JS GRAFİK MOTORU İNTEGRASYONU 🔥
# Bu script, tır kasasını ve içine yüklenecek matrisi milimetrik 3 boyutlu çizer.
three_js_code = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <style>
        body {{ margin: 0; overflow: hidden; background-color: #f8fafc; font-family: sans-serif; }}
        #info {{ position: absolute; top: 10px; left: 10px; background: rgba(26,26,26,0.9); color: white; padding: 10px; border-radius: 6px; font-size: 12px; line-height: 1.5; }}
    </style>
</head>
<body>
    <div id="info">
        <b>📐 SIMULATION PASSPORT</b><br>
        Vehicle: {v_type} ({v_boy}x{v_en}x{v_yuk} cm)<br>
        Style: {p_style}<br>
        Max Fit: {calc_max} Pcs
    </div>
    <script>
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xf8fafc);
        
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 5000);
        camera.position.set({v_boy} * 0.8, {v_yuk} * 1.5, {v_en} * 2);
        
        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);
        
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.target.set({v_boy}/2, {v_yuk}/2, {v_en}/2);

        // Işıklandırma
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        scene.add(ambientLight);
        const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
        dirLight.position.set({v_boy}, {v_yuk}*2, {v_en}*2);
        scene.add(dirLight);

        // 🚛 TIR KASASI ÇİZİMİ (Tel Kafes / Wireframe)
        const containerGeo = new THREE.BoxGeometry({v_boy}, {v_yuk}, {v_en});
        // Merkezleme ayarı
        containerGeo.translate({v_boy}/2, {v_yuk}/2, {v_en}/2);
        const edges = new THREE.EdgesGeometry(containerGeo);
        const lineMat = new THREE.LineBasicMaterial({{ color: #eb6109, linewidth: 2 }});
        const containerWire = new THREE.LineSegments(edges, lineMat);
        scene.add(containerWire);

        // Zemin Izgarası
        const grid = new THREE.GridHelper(Math.max({v_boy}, {v_en}) * 2, 50, 0xcbd5e1, 0xf1f5f9);
        grid.position.set({v_boy}/2, 0, {v_en}/2);
        scene.add(grid);

        // 📦 ÜRÜNLERİ DİZME MOTORU (Görsel Matris Gösterimi)
        const maxToShow = Math.min({p_qty}, {calc_max});
        let placed = 0;

        if ("{is_roll}" === "True") {{
            // Rulo Görselleştirme (Silindirler)
            const radius = {p_en} / 2;
            const rLen = {p_boy};
            const cylGeo = new THREE.CylinderGeometry(radius, radius, rLen, 16);
            cylGeo.rotateZ(Math.PI / 2); // Yatay yatır
            const cylMat = new THREE.MeshStandardMaterial({{ color: 0x1a1a1a, roughness: 0.4 }});

            // Basit sıralı gösterim matrisi
            for (let x = radius; x < {v_boy} && placed < maxToShow; x += rLen) {{
                for (let y = radius; y < {v_yuk} && placed < maxToShow; y += {p_en}) {{
                    for (let z = radius; z < {v_en} && placed < maxToShow; z += {p_en}) {{
                        const mesh = new THREE.Mesh(cylGeo, cylMat);
                        mesh.position.set(x + rLen/2, y, z);
                        scene.add(mesh);
                        placed++;
                    }}
                }}
            }}
        }} else {{
            // Kutu Görselleştirme (Küp Bloklar)
            const boxGeo = new THREE.BoxGeometry({p_en}, {p_yuk}, {p_boy});
            boxGeo.translate({p_en}/2, {p_yuk}/2, {p_boy}/2);
            const boxMat = new THREE.MeshStandardMaterial({{ color: 0x334155, roughness: 0.5 }});

            for (let x = 0; x < {v_boy} && placed < maxToShow; x += {p_en}) {{
                for (let y = 0; y < {v_yuk} && placed < maxToShow; y += {p_yuk}) {{
                    for (let z = 0; z < {v_en} && placed < maxToShow; z += {p_boy}) {{
                        const mesh = new THREE.Mesh(boxGeo, boxMat);
                        mesh.position.set(x, y, z);
                        scene.add(mesh);
                        placed++;
                    }}
                }}
            }}
        }}

        function animate() {{
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }}
        animate();

        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});
    </script>
</body>
</html>
"""

# HTML Bileşenini Ekrana Basma
st.components.v1.html(three_js_code, height=650)
