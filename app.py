import os
import hashlib
from flask import Flask, render_template_string, request, session, redirect, url_for

current_dir = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(current_dir, 'templates', 'index.html')

app = Flask(__name__)
app.secret_key = "nexaron_secure_crypto_key_2026"

def hash_sifre(sifre):
    return hashlib.sha256(sifre.encode('utf-8')).hexdigest()

oyuncular = {
    "RamboKutu": {"sifre": hash_sifre("12345"), "eposta": "rambo@nexaron.com", "oldurme": 150, "olme": 32, "rutbe": "Kurucu"},
    "KralPvP": {"sifre": hash_sifre("67890"), "eposta": "kral@nexaron.com", "oldurme": 135, "olme": 12, "rutbe": "Yönetici"},
    "NexaronAdmin": {"sifre": hash_sifre("admin321"), "eposta": "admin@nexaron.com", "oldurme": 110, "olme": 5, "rutbe": "Admin"}
}

@app.route('/')
def home():
    with open(html_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
    lider_html = ""
    sirali = sorted(oyuncular.items(), key=lambda x: x[1]['oldurme'], reverse=True)[:10]
    for sira, (isim, veri) in enumerate(sirali, 1):
        lider_html += f"<tr><td><span class='rank-badge'>#{sira}</span></td><td><strong>{isim}</strong></td><td style='color:var(--primary);'>{veri['rutbe']}</td><td style='color:var(--green); font-weight:bold;'>{veri['oldurme']}</td></tr>"
    content = content.replace("<!-- LIDERLIK_TABLOSU -->", lider_html)

    if 'kullanici_adi' in session:
        content = content.replace("<!-- PROFILE_ALANI -->", f'<div class="user-profile-nav">🛠️ test sürümü, <strong>{session["kullanici_adi"]}</strong>! <a href="/cikis">Oturumu Kapat</a></div>')
    else:
        content = content.replace("<!-- PROFILE_ALANI -->", "")

    if 'kullanici_adi' in session:
        kullanici = session['kullanici_adi']
        v = oyuncular[kullanici]
        form_html = f"""
        <h2>👤 Ön Kayıt Bilgilerin</h2>
        <div style="line-height: 2; margin-top: 15px;">
            <p><strong>Kullanıcı Adı:</strong> <span style="color: var(--primary);">{kullanici}</span></p>
            <p><strong>Kayıtlı E-Posta:</strong> <span style="color: var(--amber);">{v.get('eposta', 'Belirtilmedi')}</span></p>
            <p><strong>Güvenlik Durumu:</strong> <span style="color: var(--green);">SHA-256 Kriptolu ✓</span></p>
            <p><strong>Mevcut Durum:</strong> <span style="color: var(--green);">Ön Kayıt Başarılı ✓</span></p>
            <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.1); margin: 15px 0;">
            <button class="btn" style="background:var(--secondary); color:white; border:1px solid var(--primary);">Ödülleri Kontrol Et</button>
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
        oyuncular[kullanici_adi] = {"sifre": hash_sifre(sifre), "eposta": eposta, "oldurme": 0, "olme": 0, "rutbe": "Ön Kayıtlı"}
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
    # Render ve internet sunucuları için port ayarını otomatik alan kritik satır
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
