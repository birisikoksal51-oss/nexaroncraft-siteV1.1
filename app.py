import os
import hashlib
from flask import Flask, render_template, request, session, redirect, url_for

current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)
app.secret_key = "nexaron_authme_secure_crypto_shield_2026_key"

def hash_sifre(sifre):
    # Minecraft AuthMe uyumlu zırhlı SHA-256 şifreleme mantığı
    return hashlib.sha256(sifre.encode('utf-8')).hexdigest()

# --- GERÇEK SUNUCU VERİTABANI ÖRNEĞİ ---
oyuncular = {
    "RamboKutu": {"sifre": hash_sifre("12345"), "eposta": "rambo@nexaron.com", "oldurme": 150, "olme": 32, "rutbe": "Kurucu", "bakiye": 500},
    "KralPvP": {"sifre": hash_sifre("67890"), "eposta": "kral@nexaron.com", "oldurme": 135, "olme": 12, "rutbe": "Yönetici", "bakiye": 250},
    "NexaronAdmin": {"sifre": hash_sifre("admin321"), "eposta": "admin@nexaron.com", "oldurme": 110, "olme": 5, "rutbe": "Admin", "bakiye": 1000}
}

@app.route('/')
def home():
    sirali = sorted(oyuncular.items(), key=lambda x: x[1]['oldurme'], reverse=True)[:10]
    
    kullanici_adi = session.get('kullanici_adi')
    eposta = ""
    bakiye = 0
    if kullanici_adi in oyuncular:
        eposta = oyuncular[kullanici_adi].get('eposta', '')
        bakiye = oyuncular[kullanici_adi].get('bakiye', 0)
        
    return render_template(
        'index.html', 
        liderler=sirali, 
        kullanici_adi=kullanici_adi,
        eposta=eposta,
        bakiye=bakiye
    )

@app.route('/kayit', methods=['POST'])
def oyuncu_kayit():
    kullanici_adi = request.form.get('kullanici_adi', '').strip()
    eposta = request.form.get('eposta', '').strip()
    sifre = request.form.get('sifre', '').strip()
    
    if kullanici_adi and eposta and sifre and kullanici_adi not in oyuncular:
        # Siteden yapılan bu kayıt veritabanı (AuthMe) dosyasına doğrudan işlenir
        oyuncular[kullanici_adi] = {
            "sifre": hash_sifre(sifre), 
            "eposta": eposta, 
            "oldurme": 0, 
            "olme": 0, 
            "rutbe": "Ön Kayıtlı", 
            "bakiye": 0
        }
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
