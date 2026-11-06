import os
import hashlib
from flask import Flask, render_template, request, session, redirect, url_for

# Klasör yollarını hatasız bulması için Flask mimarisini yapılandırıyoruz
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
app = Flask(__name__, template_folder=template_dir)
app.secret_key = "nexaron_secure_crypto_shield_2026_key"

def hash_sifre(sifre):
    return hashlib.sha256(sifre.encode('utf-8')).hexdigest()

# --- GEÇİCİ VERİ TABANI ---
oyuncular = {
    "RamboKutu": {"sifre": hash_sifre("12345"), "eposta": "rambo@nexaron.com", "oldurme": 150, "olme": 32, "rutbe": "Kurucu", "bakiye": 500},
    "KralPvP": {"sifre": hash_sifre("67890"), "eposta": "kral@nexaron.com", "oldurme": 135, "olme": 12, "rutbe": "Yönetici", "bakiye": 250},
    "NexaronAdmin": {"sifre": hash_sifre("admin321"), "eposta": "admin@nexaron.com", "oldurme": 110, "olme": 5, "rutbe": "Admin", "bakiye": 1000},
    "BoxMaster": {"sifre": hash_sifre("box123"), "eposta": "box@gmail.com", "oldurme": 95, "olme": 45, "rutbe": "Oyuncu", "bakiye": 0},
    "ProMiner": {"sifre": hash_sifre("mine456"), "eposta": "miner@hotmail.com", "oldurme": 88, "olme": 14, "rutbe": "VIP+", "bakiye": 50},
    "ZümrütReiz": {"sifre": hash_sifre("zmrt1"), "eposta": "zmrt@gmail.com", "oldurme": 74, "olme": 20, "rutbe": "VIP", "bakiye": 20},
    "KutuCanavari": {"sifre": hash_sifre("canavar"), "eposta": "canavar@outlook.com", "oldurme": 62, "olme": 40, "rutbe": "Oyuncu", "bakiye": 0},
    "SharpnessV": {"sifre": hash_sifre("sharp5"), "eposta": "sharp@gmail.com", "oldurme": 55, "olme": 18, "rutbe": "Uzman", "bakiye": 10},
    "DiamondMan": {"sifre": hash_sifre("dia123"), "eposta": "dia@gmail.com", "oldurme": 41, "olme": 30, "rutbe": "Oyuncu", "bakiye": 0},
    "Unstoppable": {"sifre": hash_sifre("stop1"), "eposta": "unst@gmail.com", "oldurme": 33, "olme": 25, "rutbe": "Yeni Başlayan", "bakiye": 0}
}

@app.route('/')
def home():
    sirali = sorted(oyuncular.items(), key=lambda x: x[1]['oldurme'], reverse=True)[:10]
    
    mevcut_oyuncu = None
    if 'kullanici_adi' in session:
        mevcut_oyuncu = oyuncular.get(session['kullanici_adi'])
        
    return render_template(
        'index.html', 
        liderler=sirali, 
        kullanici_adi=session.get('kullanici_adi'),
        oyuncu=mevcut_oyuncu
    )

@app.route('/kayit', methods=['POST'])
def oyuncu_kayit():
    kullanici_adi = request.form.get('kullanici_adi', '').strip()
    eposta = request.form.get('eposta', '').strip()
    sifre = request.form.get('sifre', '').strip()
    if kullanici_adi and eposta and sifre and kullanici_adi not in oyuncular:
        oyuncular[kullanici_adi] = {"sifre": hash_sifre(sifre), "eposta": eposta, "oldurme": 0, "olme": 0, "rutbe": "Ön Kayıtlı", "bakiye": 0}
        session['kullanici_adi'] = kullanici_adi
    return redirect(url_for('home'))

@app.route('/giris', methods=['POST'])
def oyuncu_giris():
    giris_kimlik = request.form.get('giris_kimlik', '').strip()
    sifre = request.form.get('sifre', '').strip()
    kriptolu_sifre = hash_sifre(sifre)
    hedef_oyuncu = None
    hedef_isim = None
    if giris_kimlik in oyuncular:
        hedef_oyuncu = oyuncular[giris_kimlik]
        hedef_isim = giris_kimlik
    else:
        for isim, veri in oyuncular.items():
            if veri.get('eposta') == giris_kimlik:
                hedef_oyuncu = veri
                hedef_isim = isim
                break
    if hedef_oyuncu and hedef_oyuncu['sifre'] == kriptolu_sifre:
        session['kullanici_adi'] = hedef_isim
    return redirect(url_for('home'))

@app.route('/cikis')
def oyuncu_cikis():
    session.pop('kullanici_adi', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
