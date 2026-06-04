import pandas as pd
import ipywidgets as widgets
from IPython.display import display, clear_output, HTML
from google.colab import auth
import gspread
from google.auth import default
import re
import plotly.graph_objects as go
import base64

app_html = """
<div id="master-app" style="font-family: 'Inter', sans-serif; background: #fdfdfd; color: #2d3436; padding: 25px; border-radius: 20px; max-width: 1250px; margin: auto; box-shadow: 0 4px 30px rgba(0,0,0,0.08); border: 1px solid #dfe6e9;">

    <div style="text-align: center; border-bottom: 1px solid #dfe6e9; padding-bottom: 20px; margin-bottom: 25px;">
        <h1 style="color: #0984e3; margin: 0; font-size: 32px; letter-spacing: 3px; font-weight: 900;">🚛 CARGOMASTER PRO v87.0</h1>
        <p style="color: #636e72; font-size: 14px; text-transform: uppercase;">Realistic Cargo Engine • Ultra-Realistic Rollpack Textures</p>
    </div>

    <div style="display:flex; gap:20px; margin-bottom:20px;">
        <div style="flex:1; background:#ffffff; padding:20px; border-radius:12px; border:1px solid #dfe6e9; box-shadow: 0 2px 10px rgba(0,0,0,0.03);">
            <h3 style="color:#0984e3; margin-top:0;">1. ARAÇ KONFİGÜRASYONU</h3>
            Vasıta Tipi:<br>
            <select id="v_type" onchange="updateModelDropdown()" style="width:100%; padding:10px; background:#fcfcfc; color:#2d3436; border:1px solid #dfe6e9; border-radius:5px; margin-bottom:10px;">
                <option value="Konteyner">Deniz Konteyneri</option>
                <option value="Tır">Karayolu Tırı</option>
            </select>
            Şasi Modeli:<br>
            <select id="v_model" onchange="syncDims()" style="width:100%; padding:10px; background:#fcfcfc; color:#2d3436; border:1px solid #dfe6e9; border-radius:5px; margin-bottom:10px;"></select>
            <div style="display:flex; gap:10px;">
                <div>Boy:<input type="number" id="v_boy" style="width:100%; padding:8px; background:#fcfcfc; color:#2d3436; border:1px solid #dfe6e9; border-radius:5px;"></div>
                <div>En:<input type="number" id="v_en" style="width:100%; padding:8px; background:#fcfcfc; color:#2d3436; border:1px solid #dfe6e9; border-radius:5px;"></div>
                <div>Yükseklik:<input type="number" id="v_yuk" style="width:100%; padding:8px; background:#fcfcfc; color:#2d3436; border:1px solid #dfe6e9; border-radius:5px;"></div>
            </div>
        </div>

        <div style="flex:2; background:#ffffff; padding:20px; border-radius:12px; border:1px solid #dfe6e9; box-shadow: 0 2px 10px rgba(0,0,0,0.03);">
            <h3 style="color:#00b894; margin-top:0;">2. KARMA YÜK ENVANTERİ</h3>
            <div style="display:flex; gap:10px; margin-bottom:10px;">
                <input type="text" id="p_name" placeholder="Ürün Tanımı" style="flex:1.5; padding:10px; background:#fcfcfc; border:1px solid #dfe6e9; color:#2d3436; border-radius:5px;">
                <select id="p_style" style="flex:2; padding:10px; background:#fcfcfc; border:1px solid #dfe6e9; color:#2d3436; border-radius:5px;">
                    <option value="1">1- Kutusuz Rulo (Presli 7-6 Petek)</option>
                    <option value="2">2- Kutulu Yük (Düz Izgara İstif)</option>
                </select>
            </div>
            <div style="display:flex; gap:10px; margin-bottom:10px;">
                <input type="number" id="p_en" placeholder="En/Çap (cm)" style="flex:1; padding:10px; background:#fcfcfc; border:1px solid #dfe6e9; color:#2d3436; border-radius:5px;">
                <input type="number" id="p_boy" placeholder="Boy (cm)" style="flex:1; padding:10px; background:#fcfcfc; border:1px solid #dfe6e9; color:#2d3436; border-radius:5px;">
                <input type="number" id="p_yuk" placeholder="Yükseklik" style="flex:1; padding:10px; background:#fcfcfc; border:1px solid #dfe6e9; color:#2d3436; border-radius:5px;">
                <input type="number" id="p_qty" placeholder="Adet" style="flex:1; padding:10px; background:#fcfcfc; border:1px solid #dfe6e9; color:#2d3436; border-radius:5px;">
                <button onclick="addItem()" style="flex:1.5; background:#0984e3; border:none; color:white; font-weight:bold; border-radius:5px; cursor:pointer;">➕ EKLE</button>
            </div>
            <div id="item_list" style="height: 120px; overflow-y: auto; background:#fdfdfd; border-radius:8px; padding:10px; border: 1px solid #dfe6e9; font-size:13px;"></div>
        </div>
    </div>

    <button onclick="runSim()" style="width:100%; padding:20px; background:linear-gradient(90deg, #00b894, #2ecc71); color:white; font-size:18px; font-weight:900; border:none; border-radius:12px; cursor:pointer; box-shadow: 0 5px 20px rgba(0,184,148,0.2);">🚀 YÜKLEME PLANINI OPTİMİZE ET</button>

    <div id="s4" style="display:none; margin-top:20px;">
        <div id="report_box" style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:15px; background:#ffffff; padding:20px; border-radius:12px; margin-bottom:20px; border:1px solid #dfe6e9; box-shadow: 0 2px 10px rgba(0,0,0,0.03);">
            <div style="text-align:center; border-right:1px solid #dfe6e9;"><b>Hacim</b><br><span id="r_vol" style="font-size:24px; color:#0984e3; font-weight:bold;">0 m³</span></div>
            <div style="text-align:center; border-right:1px solid #dfe6e9;"><b>Gerçek Doluluk</b><br><span id="r_fill" style="font-size:24px; color:#00b894; font-weight:bold;">%0</span></div>
            <div style="text-align:center; border-right:1px solid #dfe6e9;"><b>Yüklenen / Talep</b><br><span id="r_qty" style="font-size:24px; color:#e17055; font-weight:bold;">0 / 0</span></div>
            <div style="text-align:center;"><b>Sığmayan (Depoda)</b><br><span id="r_left" style="font-size:24px; color:#d63031; font-weight:bold;">0</span></div>
        </div>

        <div id="canvas-wrap" style="width:100%; height:800px; background: radial-gradient(circle at center, #ffffff 0%, #e0e4e8 100%); border-radius:12px; position:relative; border:1px solid #dfe6e9; overflow: hidden; box-shadow: inset 0 0 100px rgba(0,0,0,0.05);">
             <div id="canvas-stats" style="position:absolute; top:20px; left:20px; color:#2d3436; background:rgba(253,253,253,0.9); padding:10px; border-radius:8px; font-size:12px; pointer-events:none; display:none; border: 1px solid #dfe6e9; z-index:10; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                <b style="color:#0984e3;">ARAÇ SINIRI: <span id="r_type_text"></span> - <span id="r_model_text"></span></b><br>
                <span style="color:#636e72;">Boy: <span id="r_boy_text"></span> | En: <span id="r_en_text"></span> | Yük: <span id="r_yuk_text"></span></span>
             </div>
        </div>
    </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>

<script>
const DATA = {
    'Konteyner': { '40 FT High Cube': [1203, 235, 269], '20 FT Standart': [590, 235, 239], 'Özel Ölçü': [1200, 235, 269] },
    'Tır': { 'Standart Tente': [1360, 248, 270], 'Mega Tır': [1360, 248, 300] }
};

var cargoList = [];
const TOLERANCE_X = 1.2;

if(typeof window.cargoRenderer === 'undefined') window.cargoRenderer = null;
if(typeof window.cargoAnimId === 'undefined') window.cargoAnimId = null;

function updateModelDropdown() {
    let vT = document.getElementById('v_type').value;
    let select = document.getElementById('v_model');
    select.innerHTML = '';
    Object.keys(DATA[vT]).forEach(m => { select.innerHTML += `<option value="${m}">${m}</option>`; });
    syncDims();
}

function syncDims() {
    let vT = document.getElementById('v_type').value;
    let m = document.getElementById('v_model').value;
    document.getElementById('v_boy').value = DATA[vT][m][0];
    document.getElementById('v_en').value = DATA[vT][m][1];
    document.getElementById('v_yuk').value = DATA[vT][m][2];
}

function addItem() {
    let name = document.getElementById('p_name').value || 'Ürün';
    let style = document.getElementById('p_style').value;
    let en = parseFloat(document.getElementById('p_en').value);
    let boy = parseFloat(document.getElementById('p_boy').value);
    let yuk = parseFloat(document.getElementById('p_yuk').value) || en;
    let qty = parseInt(document.getElementById('p_qty').value);
    if(!en || !boy || !qty) return alert("Değerleri eksiksiz girin!");

    let parsedL, parsedD, parsedH;

    if (style === "2") {
        let dims = [en, boy, yuk].sort((a,b) => b-a);
        parsedL = dims[0];
        parsedD = dims[1];
        parsedH = dims[2];
    } else {
        parsedD = en;
        parsedL = boy;
        parsedH = yuk;
    }

    const colors = [0x74b9ff, 0x55efc4, 0xffeaa7, 0xa29bfe, 0xff7675, 0x81ecec, 0xffab40];
    cargoList.push({ name, style, d: parsedD, L: parsedL, h: parsedH, qty, color: colors[cargoList.length % colors.length] });
    updateListView();
}

function updateListView() {
    let listDiv = document.getElementById('item_list');
    listDiv.innerHTML = cargoList.map((it, i) => `
        <div style="padding:6px 10px; background:#f9f9f9; margin-bottom:4px; border-radius:4px; border-left:4px solid #${it.color.toString(16).padStart(6, '0')}; color:#2d3436; display:flex; justify-content:space-between; align-items:center; border: 1px solid #dfe6e9;">
            <span><b style="color:#2d3436;">${it.name}</b> (${it.style == "1" ? "Rulo" : "Kutu"} | ${it.d}x${it.L}x${it.h}) - <span style="color:#0984e3; font-weight:bold;">${it.qty} Adet</span></span>
            <button onclick="removeItem(${i})" style="background:#ff7675; border:none; color:white; padding:4px 8px; border-radius:4px; cursor:pointer; font-weight:bold;">Sil</button>
        </div>`).join('');
}

function removeItem(idx) { cargoList.splice(idx, 1); updateListView(); }
window.removeItem = removeItem;

// -------------------------------------------------------------
// 🔥 YENİ: ULTRA GERÇEKÇİ ROLLPACK DOKU MOTORU 🔥
// -------------------------------------------------------------

function createRollSideTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 1024; canvas.height = 1024;
    const ctx = canvas.getContext('2d');

    // Beyaz yatak kumaşı zemin
    ctx.fillStyle = '#f8f9fa';
    ctx.fillRect(0, 0, 1024, 1024);

    // Yatak kumaşı deseni (hafif çizgiler)
    for(let i=0; i<1024; i+=12) {
        ctx.fillStyle = 'rgba(0,0,0,0.03)';
        ctx.fillRect(i, 0, 2, 1024);
    }

    // Yeşil/Siyah Bağlama Şeritleri (Yatay yüzükler)
    const drawStrap = (y) => {
        ctx.fillStyle = '#1e272e'; // Siyah kenar
        ctx.fillRect(0, y, 1024, 40);
        ctx.fillStyle = '#218c53'; // Yeşil iç
        ctx.fillRect(0, y+5, 1024, 30);
        for(let i=0; i<1024; i+=8) { // Örgü dokusu
            ctx.fillStyle = 'rgba(0,0,0,0.3)';
            ctx.fillRect(i, y+5, 2, 30);
        }
    };
    drawStrap(200);
    drawStrap(784);

    // Etiketler (Farklı açılardan görünsün diye 3 tane atıyoruz)
    for (let lx of [100, 450, 800]) {
        ctx.fillStyle = 'rgba(255,255,255,0.9)';
        ctx.fillRect(lx, 460, 200, 100);
        ctx.strokeStyle = '#2d3436';
        ctx.lineWidth = 2;
        ctx.strokeRect(lx, 460, 200, 100);

        ctx.fillStyle = '#d63031';
        ctx.font = 'bold 20px Arial';
        ctx.fillText('↑ UP ↑', lx+70, 490);
        ctx.fillStyle = '#2d3436';
        ctx.font = 'bold 18px Arial';
        ctx.fillText('MEDLINE', lx+55, 520);
        ctx.font = '12px Arial';
        ctx.fillText('ULTRA-COMPRESSED', lx+35, 540);
    }

    // Plastik Naylon Kırışıklıkları (Parlak yansımalar)
    for(let i=0; i<150; i++) {
        ctx.beginPath();
        ctx.moveTo(Math.random()*1024, Math.random()*1024);
        ctx.bezierCurveTo(Math.random()*1024, Math.random()*1024, Math.random()*1024, Math.random()*1024, Math.random()*1024, Math.random()*1024);
        ctx.strokeStyle = `rgba(255, 255, 255, ${Math.random()*0.7})`;
        ctx.lineWidth = Math.random()*8;
        ctx.stroke();
    }

    const tex = new THREE.CanvasTexture(canvas);
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    return tex;
}

function createRollCapTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 512; canvas.height = 512;
    const ctx = canvas.getContext('2d');

    // Zemin
    ctx.fillStyle = '#f8f9fa';
    ctx.fillRect(0, 0, 512, 512);

    const cx = 256, cy = 256;

    // Sarmal (Spiral) Yatak Katmanları
    for(let r=15; r<240; r+=18) {
        ctx.beginPath();
        ctx.arc(cx, cy, r, 0, 2*Math.PI);
        ctx.strokeStyle = 'rgba(0,0,0,0.15)';
        ctx.lineWidth = 6 + Math.random()*4;
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(cx, cy, r-3, 0, 2*Math.PI);
        ctx.strokeStyle = 'rgba(0,0,0,0.05)';
        ctx.lineWidth = 2;
        ctx.stroke();
    }

    // Çapraz Şeritler (X şeklinde)
    ctx.save();
    ctx.translate(cx, cy);
    for(let angle=0; angle<2; angle++) {
        ctx.rotate(Math.PI/2 * angle + Math.PI/4);
        ctx.fillStyle = '#1e272e';
        ctx.fillRect(-256, -20, 512, 40);
        ctx.fillStyle = '#218c53';
        ctx.fillRect(-256, -15, 512, 30);
        for(let i=-256; i<256; i+=8) {
            ctx.fillStyle = 'rgba(0,0,0,0.3)';
            ctx.fillRect(i, -15, 2, 30);
        }
    }
    ctx.restore();

    // Uçlardaki Plastik Kırışıklıkları
    for(let i=0; i<100; i++) {
        ctx.beginPath();
        ctx.moveTo(Math.random()*512, Math.random()*512);
        ctx.bezierCurveTo(Math.random()*512, Math.random()*512, Math.random()*512, Math.random()*512, Math.random()*512, Math.random()*512);
        ctx.strokeStyle = `rgba(255, 255, 255, ${Math.random()*0.8})`;
        ctx.lineWidth = Math.random()*6;
        ctx.stroke();
    }

    const tex = new THREE.CanvasTexture(canvas);
    return tex;
}
// -------------------------------------------------------------

function createPlywoodTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 512; canvas.height = 512;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#6d4c41'; ctx.fillRect(0, 0, 512, 512);
    for(let i=0; i<400; i++) {
        ctx.strokeStyle = `rgba(0, 0, 0, ${Math.random() * 0.15})`;
        ctx.lineWidth = Math.random() * 4;
        ctx.beginPath();
        let x = Math.random() * 512;
        ctx.moveTo(x, 0); ctx.lineTo(x + (Math.random()-0.5)*15, 512);
        ctx.stroke();
    }
    const tex = new THREE.CanvasTexture(canvas);
    tex.wrapS = THREE.RepeatWrapping; tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(12, 4);
    return tex;
}

function createCorrugatedTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 256; canvas.height = 256;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#b2bec3';
    ctx.fillRect(0, 0, 256, 256);
    for(let i=0; i<256; i+=32) {
        ctx.fillStyle = 'rgba(0,0,0,0.15)';
        ctx.fillRect(i, 0, 12, 256);
        ctx.fillStyle = 'rgba(255,255,255,0.2)';
        ctx.fillRect(i-2, 0, 4, 256);
    }
    const tex = new THREE.CanvasTexture(canvas);
    tex.wrapS = THREE.RepeatWrapping; tex.wrapT = THREE.RepeatWrapping;
    return tex;
}

var materialsCache = {};
var geometriesCache = {};

function getMaterial(color, style) {
    let key = color + "_" + style;

    if (style === "1") {
        if (!materialsCache['roll_mat_side']) {
            let sideTex = createRollSideTexture();
            let capTex = createRollCapTexture();

            // Ultra Gerçekçi Plastik/Naylon Materyali
            let matConfig = {
                roughness: 0.6,
                metalness: 0.1,
                clearcoat: 1.0,         // Plastik naylonun o kusursuz yansıması
                clearcoatRoughness: 0.15
            };

            materialsCache['roll_mat_side'] = new THREE.MeshPhysicalMaterial({ map: sideTex, ...matConfig });
            materialsCache['roll_mat_cap'] = new THREE.MeshPhysicalMaterial({ map: capTex, ...matConfig });
        }
        // Silindir için materyal dizisi: [yan yüzey, üst kapak, alt kapak]
        return [materialsCache['roll_mat_side'], materialsCache['roll_mat_cap'], materialsCache['roll_mat_cap']];
    } else {
        if(!materialsCache[key]) {
            materialsCache[key] = new THREE.MeshPhysicalMaterial({ color: color, roughness: 0.2, clearcoat: 0.5 });
        }
        return materialsCache[key];
    }
}

function getGeometry(item) {
    let key = item.style + "_" + item.d + "_" + item.L + "_" + item.h;
    if(!geometriesCache[key]) {
        if (item.style === "2") {
            geometriesCache[key] = new THREE.BoxGeometry(item.L * 0.995, item.h * 0.98, item.d * 0.98);
        } else {
            geometriesCache[key] = new THREE.CylinderGeometry(item.d/2 * 0.98, item.d/2 * 0.98, item.L * 0.995, 48);
        }
    }
    return geometriesCache[key];
}

function runSim() {
    if(cargoList.length === 0) return alert("Listeye ürün ekleyin!");
    if (window.cargoAnimId !== null) cancelAnimationFrame(window.cargoAnimId);
    document.getElementById('s4').style.display = 'block';
    document.getElementById('canvas-stats').style.display = 'block';
    document.getElementById('r_type_text').innerText = document.getElementById('v_type').value;
    document.getElementById('r_model_text').innerText = document.getElementById('v_model').value;
    document.getElementById('r_boy_text').innerText = document.getElementById('v_boy').value;
    document.getElementById('r_en_text').innerText = document.getElementById('v_en').value;
    document.getElementById('r_yuk_text').innerText = document.getElementById('v_yuk').value;
    setTimeout(init3D, 50);
}

function init3D() {
    const wrap = document.getElementById('canvas-wrap');
    if (!window.cargoRenderer) {
        window.cargoRenderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, logarithmicDepthBuffer: true });
        window.cargoRenderer.setPixelRatio(window.devicePixelRatio);
        window.cargoRenderer.shadowMap.enabled = true;
    }
    let renderer = window.cargoRenderer;
    renderer.setSize(wrap.clientWidth, 800);
    let canvases = wrap.getElementsByTagName('canvas');
    while(canvases.length > 0) wrap.removeChild(canvases[0]);
    wrap.appendChild(renderer.domElement);

    let scene = new THREE.Scene();
    const VB = parseFloat(document.getElementById('v_boy').value);
    const VE = parseFloat(document.getElementById('v_en').value);
    const VY = parseFloat(document.getElementById('v_yuk').value);

    let camera = new THREE.PerspectiveCamera(40, wrap.clientWidth / 800, 1, 100000);
    camera.position.set(VB * 1.5, VY * 1.2, VE / 2);
    let controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.target.set(VB/2, VY/2, VE/2);

    scene.add(new THREE.AmbientLight(0xffffff, 0.6));
    const sunLight = new THREE.DirectionalLight(0xffffff, 0.7);
    sunLight.position.set(VB * 2, VY * 2, VE * 2);
    sunLight.castShadow = true;
    scene.add(sunLight);

    const doorLight = new THREE.PointLight(0xffffff, 0.6, VB * 1.5);
    doorLight.position.set(VB * 1.1, VY / 2, VE / 2);
    scene.add(doorLight);

    const floor = new THREE.Mesh(new THREE.BoxGeometry(VB, 2, VE), new THREE.MeshStandardMaterial({ map: createPlywoodTexture(), roughness: 0.9 }));
    floor.position.set(VB/2, -1, VE/2);
    floor.receiveShadow = true;
    scene.add(floor);

    const wallTex = createCorrugatedTexture();
    const texRepeatX = Math.ceil(VB / 100);
    const texRepeatY = Math.ceil(VY / 100);
    wallTex.repeat.set(texRepeatX, texRepeatY);

    const wallMat = new THREE.MeshStandardMaterial({ map: wallTex, roughness: 0.7, metalness: 0.4, side: THREE.FrontSide });

    let leftWall = new THREE.Mesh(new THREE.PlaneGeometry(VB, VY), wallMat);
    leftWall.position.set(VB/2, VY/2, 0);
    scene.add(leftWall);

    let rightWall = new THREE.Mesh(new THREE.PlaneGeometry(VB, VY), wallMat);
    rightWall.rotation.y = Math.PI;
    rightWall.position.set(VB/2, VY/2, VE);
    scene.add(rightWall);

    let backWallTex = createCorrugatedTexture();
    backWallTex.repeat.set(Math.ceil(VE / 100), texRepeatY);
    let backWallMat = new THREE.MeshStandardMaterial({ map: backWallTex, roughness: 0.7, metalness: 0.4, side: THREE.FrontSide });
    let backWall = new THREE.Mesh(new THREE.PlaneGeometry(VE, VY), backWallMat);
    backWall.rotation.y = Math.PI / 2;
    backWall.position.set(0, VY/2, VE/2);
    scene.add(backWall);

    let ceilTex = createCorrugatedTexture();
    ceilTex.repeat.set(texRepeatX, Math.ceil(VE / 100));
    let ceilMat = new THREE.MeshStandardMaterial({ map: ceilTex, roughness: 0.7, metalness: 0.4, side: THREE.FrontSide });
    let ceiling = new THREE.Mesh(new THREE.PlaneGeometry(VB, VE), ceilMat);
    ceiling.rotation.x = Math.PI / 2;
    ceiling.position.set(VB/2, VY, VE/2);
    scene.add(ceiling);

    let totalV = 0, placedQty = 0, requestedQty = 0;
    let queue = [];

    cargoList.forEach(sku => {
        requestedQty += sku.qty;
        for(let i=0; i<sku.qty; i++) queue.push({...sku});
    });

    queue.sort((a,b) => {
        if (a.style !== b.style) return parseInt(b.style) - parseInt(a.style);
        return b.L - a.L;
    });

    let firstItem = queue[0];
    let isBox = (firstItem.style === "2");
    let d = firstItem.d;
    let h = firstItem.h || d;
    let r = d/2;

    let N1, N2, effD, vSpace, startZ_even, startZ_odd;

    if (isBox) {
        N1 = Math.floor(VE / d); if (N1 < 1) N1 = 1;
        N2 = N1;
        effD = d; vSpace = h;
        startZ_even = (VE - (N1 * d)) / 2 + (d / 2);
        startZ_odd = startZ_even;
    } else {
        N1 = Math.floor(VE / d); if (N1 < 1) N1 = 1;
        N2 = Math.max(1, N1 - 1);
        effD = d;
        vSpace = d * 0.866;
        let centerShift = (VE - (N1 * d)) / 2;
        startZ_even = centerShift + r;
        startZ_odd = centerShift + d;
    }

    let maxL = Math.floor((VY - (isBox ? h : d)) / vSpace) + 1;
    if (maxL < 1) maxL = 1;

    let slots = [];
    for (let l = 0; l < maxL; l++) {
        let rowQty = (l % 2 === 0) ? N1 : N2;
        let startZ = (l % 2 === 0) ? startZ_even : startZ_odd;
        let yCenter = (isBox ? h/2 : r) + l * vSpace;
        slots[l] = [];
        for (let i = 0; i < rowQty; i++) {
            slots[l][i] = { x: 0, y: yCenter, z: startZ + i * effD };
        }
    }

    while(queue.length > 0) {
        let placedSomething = false;
        let hIdx = -1;
        let hBestSlot = null;

        for (let q = 0; q < queue.length; q++) {
            let item = queue[q];
            let bestSlot = null;
            let currentTol = (item.style === "2") ? 0 : TOLERANCE_X;

            for (let l = 0; l < maxL; l++) {
                let rowQty = (l % 2 === 0) ? N1 : N2;
                for (let i = 0; i < rowQty; i++) {
                    let startX = slots[l][i].x;
                    let reqX = startX + item.L + currentTol;

                    if (reqX > VB) continue;

                    let supported = true;
                    if (l > 0) {
                        let OVERHANG = (item.style === "2") ? 0 : item.L * 0.4;
                        let safeReqX = reqX - OVERHANG;

                        if (isBox) {
                            if (slots[l-1][i].x < safeReqX) supported = false;
                        } else {
                            if (l % 2 === 1) {
                                if (slots[l-1][i].x < safeReqX || slots[l-1][i+1].x < safeReqX) supported = false;
                            } else {
                                if (i > 0 && slots[l-1][i-1].x < safeReqX) supported = false;
                                if (i < N1 - 1 && slots[l-1][i].x < safeReqX) supported = false;
                            }
                        }
                    }

                    if (supported) {
                        if (!bestSlot) {
                            bestSlot = { l: l, i: i, x: startX };
                        } else {
                            if (startX < bestSlot.x - 0.1) {
                                bestSlot = { l: l, i: i, x: startX };
                            } else if (Math.abs(startX - bestSlot.x) <= 0.1) {
                                if (l < bestSlot.l) {
                                    bestSlot = { l: l, i: i, x: startX };
                                } else if (l === bestSlot.l && i < bestSlot.i) {
                                    bestSlot = { l: l, i: i, x: startX };
                                }
                            }
                        }
                    }
                }
            }
            if (bestSlot) { hIdx = q; hBestSlot = bestSlot; break; }
        }

        if (hIdx !== -1) {
            let item = queue.splice(hIdx, 1)[0];
            let currentTol = (item.style === "2") ? 0 : TOLERANCE_X;

            let mesh = new THREE.Mesh(getGeometry(item), getMaterial(item.color, item.style));
            if (item.style === "1") { mesh.rotation.x = Math.PI/2; mesh.rotation.z = Math.PI/2; }
            mesh.position.set(hBestSlot.x + item.L/2, slots[hBestSlot.l][hBestSlot.i].y, slots[hBestSlot.l][hBestSlot.i].z);
            scene.add(mesh);

            slots[hBestSlot.l][hBestSlot.i].x = hBestSlot.x + item.L + currentTol;
            totalV += (item.style === "2") ? ((item.d * item.h * item.L) / 1000000) : ((item.d * item.d * item.L) / 1000000);
            placedQty++;
            placedSomething = true;

        } else {
            let vIdx = -1;
            let vCapX = 0;
            let isSidewaysBox = false;

            for (let q = 0; q < queue.length; q++) {
                let item = queue[q];
                let currentTolForCap = (item.style === "2") ? 0 : TOLERANCE_X;

                let tempCapX = 0;
                for (let l = 0; l < maxL; l++) {
                    let blockHeight = (item.style === "2") ? VY : item.L;
                    if (slots[l][0].y - r < blockHeight) {
                        for (let i = 0; i < slots[l].length; i++) {
                            if (slots[l][i].x > tempCapX) tempCapX = slots[l][i].x;
                        }
                    }
                }

                if (item.style === "2") {
                    if (tempCapX + item.d + currentTolForCap <= VB && item.L <= VE) {
                        vIdx = q; vCapX = tempCapX; isSidewaysBox = true; break;
                    }
                } else {
                    if (tempCapX + item.d + currentTolForCap <= VB && item.L <= VY) {
                        vIdx = q; vCapX = tempCapX; isSidewaysBox = false; break;
                    }
                }
            }

            if (vIdx !== -1) {
                let item = queue[vIdx];
                let currentVX = vCapX;
                let currentTol = (item.style === "2") ? 0 : TOLERANCE_X;

                if (isSidewaysBox) {
                    let N_z = Math.floor(VE / item.L); if (N_z < 1) N_z = 1;
                    let N_y = Math.floor(VY / item.h);
                    let needed = N_z * N_y;

                    while (currentVX + item.d + currentTol <= VB && queue.length > 0) {
                        let vGroup = [];
                        for (let q = queue.length - 1; q >= 0; q--) {
                            if (queue[q].style === item.style && queue[q].d === item.d && queue[q].L === item.L && queue[q].h === item.h) {
                                vGroup.push(queue.splice(q, 1)[0]);
                                if (vGroup.length === needed) break;
                            }
                        }
                        if (vGroup.length === 0) break;

                        let currentY = item.h / 2;
                        let zIdx = 0;
                        let startZ = (VE - (N_z * item.L)) / 2 + item.L / 2;

                        for (let k = 0; k < vGroup.length; k++) {
                            let vItem = vGroup[k];
                            let mesh = new THREE.Mesh(getGeometry(vItem), getMaterial(vItem.color, vItem.style));
                            mesh.rotation.y = Math.PI / 2;
                            let posZ = startZ + zIdx * vItem.L;
                            mesh.position.set(currentVX + vItem.d / 2, currentY, posZ);
                            scene.add(mesh);
                            totalV += (vItem.d * vItem.h * vItem.L) / 1000000; placedQty++;
                            zIdx++;
                            if (zIdx >= N_z) { zIdx = 0; currentY += vItem.h; }
                        }
                        currentVX += item.d + currentTol;
                        if (vGroup.length < needed) break;
                    }
                    for (let l = 0; l < maxL; l++) {
                        for (let i = 0; i < slots[l].length; i++) slots[l][i].x = VB;
                    }
                    placedSomething = true;

                } else {
                    let N_vert = Math.floor(VE / item.d); if (N_vert < 1) N_vert = 1;
                    let effD_vert = item.d;
                    let centerShiftVert = (VE - (N_vert * item.d)) / 2;
                    let startZ_vert = centerShiftVert + (item.d / 2);
                    let placedVertRows = 0;

                    while (currentVX + item.d + currentTol <= VB && queue.length > 0) {
                        let vGroup = [];
                        for (let q = queue.length - 1; q >= 0; q--) {
                            if (queue[q].style === item.style && queue[q].d === item.d && queue[q].L === item.L) {
                                vGroup.push(queue.splice(q, 1)[0]);
                                if (vGroup.length === N_vert) break;
                            }
                        }
                        if (vGroup.length === 0) break;

                        for(let k=0; k < vGroup.length; k++) {
                            let vItem = vGroup[k];
                            let mesh = new THREE.Mesh(getGeometry(vItem), getMaterial(vItem.color, vItem.style));
                            mesh.position.set(currentVX + vItem.d/2, vItem.L/2, startZ_vert + k * effD_vert);
                            scene.add(mesh);
                            totalV += (vItem.d * vItem.d * vItem.L) / 1000000; placedQty++;
                        }
                        currentVX += item.d + currentTol;
                        placedVertRows++;
                        if (vGroup.length < N_vert) break;
                    }

                    let platformEndX = currentVX;
                    let remainingHeight = VY - item.L;

                    if (placedVertRows > 0 && remainingHeight >= item.d) {
                        let cap_d = item.d;
                        let cap_r = cap_d / 2;
                        let cap_L = item.L;

                        let N_z = Math.floor(VE / cap_L);

                        if (N_z >= 1) {
                            let startZ_cap = (VE - (N_z * cap_L)) / 2 + (cap_L / 2);

                            if (placedVertRows === 1) {
                                let capMaxY = Math.floor(remainingHeight / cap_d);
                                let xCenter = vCapX + cap_r;

                                for (let cY = 0; cY < capMaxY; cY++) {
                                    let yCenter = item.L + cap_r + (cY * cap_d);

                                    for (let zi = 0; zi < N_z; zi++) {
                                        let posZ = startZ_cap + (zi * cap_L);

                                        let capItemIdx = queue.findIndex(it => it.style === item.style && it.d === cap_d && it.L === cap_L);
                                        if (capItemIdx !== -1) {
                                            let cItem = queue.splice(capItemIdx, 1)[0];
                                            let mesh = new THREE.Mesh(getGeometry(cItem), getMaterial(cItem.color, cItem.style));

                                            mesh.rotation.x = Math.PI / 2;

                                            mesh.position.set(xCenter, yCenter, posZ);
                                            scene.add(mesh);
                                            totalV += (cItem.d * cItem.d * cItem.L) / 1000000;
                                            placedQty++;
                                        }
                                    }
                                }
                            } else {
                                let cap_vSpace = cap_d * 0.866;
                                let capMaxY = Math.floor((remainingHeight - cap_d) / cap_vSpace) + 1;
                                if(capMaxY < 1) capMaxY = 1;

                                let N_x1 = placedVertRows;
                                let N_x2 = N_x1 - 1;
                                let startX_even = vCapX + cap_r;
                                let startX_odd = vCapX + cap_d;

                                for (let cY = 0; cY < capMaxY; cY++) {
                                    let yCenter = item.L + cap_r + (cY * cap_vSpace);
                                    if (yCenter + cap_r > VY) break;

                                    let rowQtyX = (cY % 2 === 0) ? N_x1 : N_x2;
                                    let startX = (cY % 2 === 0) ? startX_even : startX_odd;

                                    for (let xi = 0; xi < rowQtyX; xi++) {
                                        let xCenter = startX + (xi * cap_d);

                                        for (let zi = 0; zi < N_z; zi++) {
                                            let posZ = startZ_cap + (zi * cap_L);

                                            let capItemIdx = queue.findIndex(it => it.style === item.style && it.d === cap_d && it.L === cap_L);
                                            if (capItemIdx !== -1) {
                                                let cItem = queue.splice(capItemIdx, 1)[0];
                                                let mesh = new THREE.Mesh(getGeometry(cItem), getMaterial(cItem.color, cItem.style));

                                                mesh.rotation.x = Math.PI / 2;

                                                mesh.position.set(xCenter, yCenter, posZ);
                                                scene.add(mesh);
                                                totalV += (cItem.d * cItem.d * cItem.L) / 1000000;
                                                placedQty++;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }

                    for (let l = 0; l < maxL; l++) {
                        for (let i = 0; i < slots[l].length; i++) slots[l][i].x = VB;
                    }
                    placedSomething = true;
                }
            }
        }
        if (!placedSomething) break;
    }

    document.getElementById('r_vol').innerText = totalV.toFixed(2) + ' m³';
    document.getElementById('r_fill').innerText = '%' + ((totalV / ((VB*VE*VY)/1000000)) * 100).toFixed(1);
    document.getElementById('r_qty').innerText = placedQty + ' / ' + requestedQty;
    document.getElementById('r_left').innerText = (requestedQty - placedQty);

    function animate() { window.cargoAnimId = requestAnimationFrame(animate); controls.update(); renderer.render(scene, camera); }
    animate();
}

updateModelDropdown();
</script>
"""
display(HTML(app_html))
