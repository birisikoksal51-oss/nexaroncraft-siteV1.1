import os
import hashlib
from flask import Flask, render_template_string, request, session, redirect, url_for

current_dir = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(current_dir, 'templates', 'index.html')

app = Flask(__name__)
# Güvenlik Duvarı: Oturum güvenliği ve Session Hijacking koruması için zırhlı key
app.secret_key = "nexaron_secure_crypto_shield_2026_key"

def hash_sifre(sifre):
    return hashlib.sha256(sifre.encode('utf-8')).hexdigest()

# --- GELİŞMİŞ OYUNCU, BAKİYE VE ÖN KAYIT VERİ TABANI ---
# Test etmeniz için bakiye (TL) alanı ve e-postalar sisteme entegre edildi.
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
    if not os.path.exists(html_path):
        return "Hata: templates klasöründe index.html bulunamadı!", 404
        
    with open(html_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
    # 1. En İyi 10 Kişilik Liderlik Tablosu
    lider_html = ""
    sirali = sorted(oyuncular.items(), key=lambda x: x[1]['oldurme'], reverse=True)[:10]
    for sira, (isim, veri) in enumerate(sirali, 1):
        lider_html += f"<tr><td><span class='rank-badge'>#{sira}</span></td><td><strong>{isim}</strong></td><td style='color:var(--primary);'>{veri['rutbe']}</td><td style='color:var(--green); font-weight:bold;'>{veri['oldurme']}</td></tr>"
    content = content.replace("<!-- LIDERLIK_TABLOSU -->", lider_html)

    # 2. Üst Menü Profil ve Canlı Bakiye Alanı
    if 'kullanici_adi' in session:
        kullanici = session['kullanici_adi']
        v = oyuncular[kullanici]
        content = content.replace("<!-- PROFILE_ALANI -->", f'<div class="user-profile-nav">💰 Bakiye: <strong style="color:var(--amber);">{v.get("bakiye", 0)} TL</strong> | 🛠️ test sürümü, <strong>{kullanici}</strong>! <a href="/cikis">Oturumu Kapat</a></div>')
    else:
        content = content.replace("<!-- PROFILE_ALANI -->", "")

    # 3. Giriş / Gelişmiş Ön Kayıt Paneli (Ödül Açıklamalı)
    if 'kullanici_adi' in session:
        kullanici = session['kullanici_adi']
        v = oyuncular[kullanici]
        form_html = f"""
        <h2>👤 Ön Kayıt Bilgilerin</h2>
        <div style="line-height: 2; margin-top: 15px;">
            <p><strong>Kullanıcı Adı:</strong> <span style="color: var(--primary);">{kullanici}</span></p>
            <p><strong>Kayıtlı E-Posta:</strong> <span style="color: var(--amber);">{v.get('eposta', 'Belirtilmedi')}</span></p>
            <p><strong>Cüzdan Bakiyesi:</strong> <span style="color: var(--amber);">{v.get('bakiye', 0)} TL</span></p>
            <p><strong>Güvenlik Durumu:</strong> <span style="color: var(--green);">SHA-256 Kriptolu ✓</span></p>
            <p><strong>Mevcut Durum:</strong> <span style="color: var(--green);">Ön Kayıt Başarılı ✓</span></p>
            <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.1); margin: 15px 0;">
            <div style="background: rgba(254, 202, 87, 0.1); padding: 15px; border-radius: 8px; border: 1px solid var(--amber); margin-bottom: 15px;">
                <h4 style="color: var(--amber); text-transform: uppercase;">🎁 Ön Kayıt Ödülü!</h4>
                <p style="font-size: 0.95rem; color: #fff; margin-top: 5px;">Hesabınıza <strong>1 Adet NexaronKazma</strong> Eklenmiştir! Oyuna ilk giriş yaptığınızda otomatik olarak envanterinize verilecektir.</p>
            </div>
            <button class="btn" style="background:var(--secondary); color:white; border:1px solid var(--primary);" onclick="alert('Ödülünüz sunucu açılışında otomatik teslim edilmek üzere kilitlendi!')">Ödülü Kilitle ✓</button>
        </div>
        """
    else:
        form_html = """
        <div id="login-form-block">
            <h2>🔐 E-Postalı Oyuncu Girişi</h2>
            <form action="/giris" method="POST" style="margin-top:15px;">
                <div class="form-group"><label>E-Posta Adresi veya Kullanıcı Adı</label><input type="text" name="giris_kimlik" required placeholder="kral@nexaron.com veya RamboKutu"></div>
                <div class="form-group"><label>Şifre</label><input type="password" name="sifre" required placeholder="••••••••"></div>
                <button type="submit" class="btn">Giriş Yap</button>
            </form>
            <p class="switch-form-text" onclick="toggleForms()">Hesabın yok mu? <span>Buradan Güvenli Ön Kayıt Ol</span></p>
        </div>
        <div id="register-form-block" style="display: none;">
            <h2>📝 Güvenli Ön Kayıt Sistemi</h2>
            <form action="/kayit" method="POST" style="margin-top:15px;">
                <div class="form-group"><label>Minecraft Kullanıcı Adı</label><input type="text" name="kullanici_adi" required placeholder="Örn: RamboKutu"></div>
                <div class="form-group"><label>E-Posta Adresi</label><input type="email" name="eposta" required placeholder="kral@nexaron.com"></div>
                <div class="form-group"><label>Güvenli Şifre Belirle</label><input type="password" name="sifre" required placeholder="••••••••"></div>
                <button type="submit" class="btn" style="background-color: var(--amber); color: #000;">Kriptolu Ön Kaydı Tamamla</button>
            </form>
            <p class="switch-form-text" onclick="toggleForms()">Zaten üye misin? <span>Buradan Giriş Yap</span></p>
        </div>
        """
    content = content.replace("<!-- GIRIS_VE_KAYIT_ALANI -->", form_html)
    
    return render_template_string(content)

@app.route('/kayit', methods=['POST'])
def oyuncu_kayit():
    kullanici_adi = request.form.get('kullanici_adi', '').strip()
    eposta = request.form.get('eposta', '').strip()
    sifre = request.form.get('sifre', '').strip()
    
    if kullanici_adi and eposta and sifre and kullanici_adi not in oyuncular:
        kriptolu_sifre = hash_sifre(sifre)
        # Yeni ön kayıt olan oyuncuya başlangıçta 0 TL bakiye tanımlanır
        oyuncular[kullanici_adi] = {"sifre": kriptolu_sifre, "eposta": eposta, "oldurme": 0, "olme": 0, "rutbe": "Ön Kayıtlı", "bakiye": 0}
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
        session['kullanici_adi'] = ./hedef_isim if hasattr(session, 'kullanici_adi') else hedef_isim
        session['kullanici_adi'] = hedef_isim
        
    return redirect(url_for('home'))

@app.route('/cikis')
def oyuncu_cikis():
    session.pop('kullanici_adi', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
