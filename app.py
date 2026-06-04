import streamlit as st
import streamlit.components.v1 as components

# Sayfa ayarları
st.set_page_config(page_title="CargoMaster Pro v89.0", layout="wide", page_icon="🚛")

app_html = """
<div id="master-app" style="font-family: 'Inter', sans-serif; background: #fdfdfd; color: #2d3436; padding: 25px; border-radius: 20px; max-width: 1250px; margin: auto; box-shadow: 0 4px 30px rgba(0,0,0,0.08); border: 1px solid #dfe6e9;">

    <div style="text-align: center; border-bottom: 1px solid #dfe6e9; padding-bottom: 20px; margin-bottom: 25px;">
        <h1 style="color: #0984e3; margin: 0; font-size: 32px; letter-spacing: 3px; font-weight: 900;">🚛 CARGOMASTER PRO v89.0</h1>
        <p style="color: #636e72; font-size: 14px; text-transform: uppercase;">Dinamik Boşluk Doldurma Motoru (Nesting & Heightmap Engine)</p>
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
// 🔥 DOKU MOTORU (TEXTURE ENGINE) 🔥
// -------------------------------------------------------------
function createRollSideTexture() {
    const canvas = document.createElement('canvas'); canvas.width = 1024; canvas.height = 1024; const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#f8f9fa'; ctx.fillRect(0, 0, 1024, 1024);
    for(let i=0; i<1024; i+=12) { ctx.fillStyle = 'rgba(0,0,0,0.03)'; ctx.fillRect(i, 0, 2, 1024); }
    const drawStrap = (y) => {
        ctx.fillStyle = '#1e272e'; ctx.fillRect(0, y, 1024, 40);
        ctx.fillStyle = '#218c53'; ctx.fillRect(0, y+5, 1024, 30);
        for(let i=0; i<1024; i+=8) { ctx.fillStyle = 'rgba(0,0,0,0.3)'; ctx.fillRect(i, y+5, 2, 30); }
    };
    drawStrap(200); drawStrap(784);
    for (let lx of [100, 450, 800]) {
        ctx.fillStyle = 'rgba(255,255,255,0.9)'; ctx.fillRect(lx, 460, 200, 100);
        ctx.strokeStyle = '#2d3436'; ctx.lineWidth = 2; ctx.strokeRect(lx, 460, 200, 100);
        ctx.fillStyle = '#d63031'; ctx.font = 'bold 20px Arial'; ctx.fillText('↑ UP ↑', lx+70, 490);
        ctx.fillStyle = '#2d3436'; ctx.font = 'bold 18px Arial'; ctx.fillText('MEDLINE', lx+55, 520);
        ctx.font = '12px Arial'; ctx.fillText('ULTRA-COMPRESSED', lx+35, 540);
    }
    for(let i=0; i<150; i++) {
        ctx.beginPath(); ctx.moveTo(Math.random()*1024, Math.random()*1024);
        ctx.bezierCurveTo(Math.random()*1024, Math.random()*1024, Math.random()*1024, Math.random()*1024, Math.random()*1024, Math.random()*1024);
        ctx.strokeStyle = `rgba(255, 255, 255, ${Math.random()*0.7})`; ctx.lineWidth = Math.random()*8; ctx.stroke();
    }
    const tex = new THREE.CanvasTexture(canvas); tex.wrapS = THREE.RepeatWrapping; tex.wrapT = THREE.RepeatWrapping; return tex;
}

function createRollCapTexture() {
    const canvas = document.createElement('canvas'); canvas.width = 512; canvas.height = 512; const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#f8f9fa'; ctx.fillRect(0, 0, 512, 512); const cx = 256, cy = 256;
    for(let r=15; r<240; r+=18) {
        ctx.beginPath(); ctx.arc(cx, cy, r, 0, 2*Math.PI); ctx.strokeStyle = 'rgba(0,0,0,0.15)'; ctx.lineWidth = 6 + Math.random()*4; ctx.stroke();
        ctx.beginPath(); ctx.arc(cx, cy, r-3, 0, 2*Math.PI); ctx.strokeStyle = 'rgba(0,0,0,0.05)'; ctx.lineWidth = 2; ctx.stroke();
    }
    ctx.save(); ctx.translate(cx, cy);
    for(let angle=0; angle<2; angle++) {
        ctx.rotate(Math.PI/2 * angle + Math.PI/4);
        ctx.fillStyle = '#1e272e'; ctx.fillRect(-256, -20, 512, 40);
        ctx.fillStyle = '#218c53'; ctx.fillRect(-256, -15, 512, 30);
        for(let i=-256; i<256; i+=8) { ctx.fillStyle = 'rgba(0,0,0,0.3)'; ctx.fillRect(i, -15, 2, 30); }
    }
    ctx.restore();
    for(let i=0; i<100; i++) {
        ctx.beginPath(); ctx.moveTo(Math.random()*512, Math.random()*512);
        ctx.bezierCurveTo(Math.random()*512, Math.random()*512, Math.random()*512, Math.random()*512, Math.random()*512, Math.random()*512);
        ctx.strokeStyle = `rgba(255, 255, 255, ${Math.random()*0.8})`; ctx.lineWidth = Math.random()*6; ctx.stroke();
    }
    return new THREE.CanvasTexture(canvas);
}

function createPlywoodTexture() {
    const canvas = document.createElement('canvas'); canvas.width = 512; canvas.height = 512; const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#6d4c41'; ctx.fillRect(0, 0, 512, 512);
    for(let i=0; i<400; i++) {
        ctx.strokeStyle = `rgba(0, 0, 0, ${Math.random() * 0.15})`; ctx.lineWidth = Math.random() * 4;
        ctx.beginPath(); let x = Math.random() * 512; ctx.moveTo(x, 0); ctx.lineTo(x + (Math.random()-0.5)*15, 512); ctx.stroke();
    }
    const tex = new THREE.CanvasTexture(canvas); tex.wrapS = THREE.RepeatWrapping; tex.wrapT = THREE.RepeatWrapping; tex.repeat.set(12, 4); return tex;
}

function createCorrugatedTexture() {
    const canvas = document.createElement('canvas'); canvas.width = 256; canvas.height = 256; const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#b2bec3'; ctx.fillRect(0, 0, 256, 256);
    for(let i=0; i<256; i+=32) {
        ctx.fillStyle = 'rgba(0,0,0,0.15)'; ctx.fillRect(i, 0, 12, 256);
        ctx.fillStyle = 'rgba(255,255,255,0.2)'; ctx.fillRect(i-2, 0, 4, 256);
    }
    const tex = new THREE.CanvasTexture(canvas); tex.wrapS = THREE.RepeatWrapping; tex.wrapT = THREE.RepeatWrapping; return tex;
}

var materialsCache = {};
var geometriesCache = {};

function getMaterial(color, style) {
    let key = color + "_" + style;
    if (style === "1") {
        if (!materialsCache['roll_mat_side']) {
            let sideTex = createRollSideTexture(); let capTex = createRollCapTexture();
            let matConfig = { roughness: 0.6, metalness: 0.1, clearcoat: 1.0, clearcoatRoughness: 0.15 };
            materialsCache['roll_mat_side'] = new THREE.MeshPhysicalMaterial({ map: sideTex, ...matConfig });
            materialsCache['roll_mat_cap'] = new THREE.MeshPhysicalMaterial({ map: capTex, ...matConfig });
        }
        return [materialsCache['roll_mat_side'], materialsCache['roll_mat_cap'], materialsCache['roll_mat_cap']];
    } else {
        if(!materialsCache[key]) materialsCache[key] = new THREE.MeshPhysicalMaterial({ color: color, roughness: 0.2, clearcoat: 0.5 });
        return materialsCache[key];
    }
}

function getGeometry(item) {
    let key = item.style + "_" + item.d + "_" + item.L + "_" + item.h;
    if(!geometriesCache[key]) {
        if (item.style === "2") geometriesCache[key] = new THREE.BoxGeometry(item.L * 0.995, item.h * 0.98, item.d * 0.98);
        else geometriesCache[key] = new THREE.CylinderGeometry(item.d/2 * 0.98, item.d/2 * 0.98, item.L * 0.995, 48);
    }
    return geometriesCache[key];
}

// -------------------------------------------------------------
// 🔥 YENİ: DİNAMİK BOŞLUK DOLDURMA (NESTING) MOTORU 🔥
// -------------------------------------------------------------
let N1, N2, effD, vSpace, startZ_even, startZ_odd, maxL;
let slots = [];

function buildDynamicGrid(style, d, h, startX, VE, VY) {
    let isBox = (style === "2");
    let r = d/2;
    if (isBox) {
        N1 = Math.floor(VE / d); if (N1 < 1) N1 = 1;
        N2 = N1; effD = d; vSpace = h;
        startZ_even = (VE - (N1 * d)) / 2 + (d / 2);
        startZ_odd = startZ_even;
    } else {
        N1 = Math.floor(VE / d); if (N1 < 1) N1 = 1;
        N2 = Math.max(1, N1 - 1); effD = d; vSpace = d * 0.866;
        let centerShift = (VE - (N1 * d)) / 2;
        startZ_even = centerShift + r;
        startZ_odd = centerShift + d;
    }
    maxL = Math.floor((VY - (isBox ? h : d)) / vSpace) + 1;
    if (maxL < 1) maxL = 1;
    
    slots = [];
    for (let l = 0; l < maxL; l++) {
        let rowQty = (l % 2 === 0) ? N1 : N2;
        let startZ = (l % 2 === 0) ? startZ_even : startZ_odd;
        let yCenter = (isBox ? h/2 : r) + l * vSpace;
        slots[l] = [];
        for (let i = 0; i < rowQty; i++) {
            slots[l][i] = { x: startX, y: yCenter, z: startZ + i * effD };
        }
    }
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
    sunLight.position.set(VB * 2, VY * 2, VE * 2); sunLight.castShadow = true; scene.add(sunLight);
    const doorLight = new THREE.PointLight(0xffffff, 0.6, VB * 1.5);
    doorLight.position.set(VB * 1.1, VY / 2, VE / 2); scene.add(doorLight);

    const floor = new THREE.Mesh(new THREE.BoxGeometry(VB, 2, VE), new THREE.MeshStandardMaterial({ map: createPlywoodTexture(), roughness: 0.9 }));
    floor.position.set(VB/2, -1, VE/2); floor.receiveShadow = true; scene.add(floor);

    const wallTex = createCorrugatedTexture();
    const texRepeatX = Math.ceil(VB / 100); const texRepeatY = Math.ceil(VY / 100);
    wallTex.repeat.set(texRepeatX, texRepeatY);
    const wallMat = new THREE.MeshStandardMaterial({ map: wallTex, roughness: 0.7, metalness: 0.4, side: THREE.FrontSide });

    let leftWall = new THREE.Mesh(new THREE.PlaneGeometry(VB, VY), wallMat); leftWall.position.set(VB/2, VY/2, 0); scene.add(leftWall);
    let rightWall = new THREE.Mesh(new THREE.PlaneGeometry(VB, VY), wallMat); rightWall.rotation.y = Math.PI; rightWall.position.set(VB/2, VY/2, VE); scene.add(rightWall);
    
    let backWallTex = createCorrugatedTexture(); backWallTex.repeat.set(Math.ceil(VE / 100), texRepeatY);
    let backWallMat = new THREE.MeshStandardMaterial({ map: backWallTex, roughness: 0.7, metalness: 0.4, side: THREE.FrontSide });
    let backWall = new THREE.Mesh(new PlaneGeometry(VE, VY), backWallMat); backWall.rotation.y = Math.PI / 2; backWall.position.set(0, VY/2, VE/2); scene.add(backWall);

    let ceilTex = createCorrugatedTexture(); ceilTex.repeat.set(texRepeatX, Math.ceil(VE / 100));
    let ceilMat = new THREE.MeshStandardMaterial({ map: ceilTex, roughness: 0.7, metalness: 0.4, side: THREE.FrontSide });
    let ceiling = new THREE.Mesh(new THREE.PlaneGeometry(VB, VE), ceilMat); ceiling.rotation.x = Math.PI / 2; ceiling.position.set(VB/2, VY, VE/2); scene.add(ceiling);

    let totalV = 0, placedQty = 0, requestedQty = 0;
    let queue = [];
    let placedItems = []; // 🔥 Dizilmiş ürünlerin haritası

    cargoList.forEach(sku => {
        requestedQty += sku.qty;
        for(let i=0; i<sku.qty; i++) queue.push({...sku});
    });

    // Önce Çapa ve Yüksekliğe göre büyükten küçüğe sırala ki devrilmesin
    queue.sort((a,b) => {
        if (a.style !== b.style) return parseInt(b.style) - parseInt(a.style);
        if (b.d !== a.d) return b.d - a.d;
        if (b.h !== a.h) return b.h - a.h;
        return b.L - a.L;
    });

    if (queue.length === 0) return;

    let currentStyle = queue[0].style;
    let currentD = queue[0].d;
    let currentH = queue[0].h || queue[0].d;
    
    buildDynamicGrid(currentStyle, currentD, currentH, 0, VE, VY);

    while(queue.length > 0) {
        let firstQ = queue[0];
        let firstH = firstQ.h || firstQ.d;

        // 🔥 YENİ ÇAP (Örn: 34 bitti 32 başladı). Fiziksel haritayı tarayıp boşlukları bul!
        if (firstQ.style !== currentStyle || firstQ.d !== currentD || firstH !== currentH) {
            currentStyle = firstQ.style;
            currentD = firstQ.d;
            currentH = firstH;
            
            buildDynamicGrid(currentStyle, currentD, currentH, 0, VE, VY);

            // Her bir yeni slot için, eski yerleştirilmiş ürünleri çarpışma (overlap) testine sok
            for (let l = 0; l < maxL; l++) {
                for (let i = 0; i < slots[l].length; i++) {
                    let ny = slots[l][i].y;
                    let nz = slots[l][i].z;
                    let max_x = 0; // Eğer altı boşsa sıfırdan başlar!
                    
                    for (let p = 0; p < placedItems.length; p++) {
                        let pi = placedItems[p];
                        
                        if (currentStyle === "2" || pi.style === "2") {
                            let overlapY = Math.abs(ny - pi.y) < ((currentH/2) + (pi.h/2)) * 0.95;
                            let overlapZ = Math.abs(nz - pi.z) < ((currentD/2) + (pi.d/2)) * 0.95;
                            if (overlapY && overlapZ) {
                                if (pi.x_end > max_x) max_x = pi.x_end;
                            }
                        } else {
                            // Silindirler için YZ düzleminde gerçek merkez mesafesi kontrolü
                            let dy = ny - pi.y;
                            let dz = nz - pi.z;
                            let dist = Math.sqrt(dy*dy + dz*dz);
                            let threshold = ((currentD/2) + (pi.d/2)) * 0.95; // %5 tolerans
                            if (dist < threshold) {
                                if (pi.x_end > max_x) max_x = pi.x_end; // Fiziksel olarak engelliyorsa ileri it!
                            }
                        }
                    }
                    slots[l][i].x = max_x;
                }
            }
        }

        let placedSomething = false;
        let hIdx = -1;
        let hBestSlot = null;

        for (let q = 0; q < queue.length; q++) {
            let item = queue[q];
            let itemH = item.h || item.d;
            if (item.style !== currentStyle || item.d !== currentD || itemH !== currentH) continue;

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

                        if (item.style === "2") {
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

            let finalX = hBestSlot.x + item.L + currentTol;
            slots[hBestSlot.l][hBestSlot.i].x = finalX;
            
            placedItems.push({
                x_end: finalX,
                y: slots[hBestSlot.l][hBestSlot.i].y,
                z: slots[hBestSlot.l][hBestSlot.i].z,
                d: item.d,
                h: item.h,
                style: item.style
            });

            totalV += (item.style === "2") ? ((item.d * item.h * item.L) / 1000000) : ((item.d * item.d * item.L) / 1000000);
            placedQty++;
            placedSomething = true;
        }

        if (!placedSomething) {
            queue.shift(); // O çapa ait sığan kalmadıysa döngüden çıkar
        }
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

# HTML Bileşenini 1200px yükseklikte render ediyoruz
components.html(app_html, height=1200, scrolling=True)
