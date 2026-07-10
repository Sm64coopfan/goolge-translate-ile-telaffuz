import time
import datetime
import random
import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator

# --- GÖRSEL VE ASCII ELEMENTLERİ ---
LOGO = """
===========================================================
 🎯  SPEAK & LEARN: ÇOK DİLLİ KONUŞMA OYUNU  🎯
===========================================================
"""
WIN_ART = """
   🏆 TEBRİKLER! DOĞRU CEVAP! 🏆
"""
LOSE_ART = """
   ❌ MAALESEF YANLIŞ CEVAP ❌
"""

# --- 10 SEVİYELİ DEV KELİME SÖZLÜĞÜ ---
KELİMELER = {
    "1": {
        "ad": "temel başlangıç (a1-)", 
        "puan": 10, 
        "liste": ["kedi", "köpek", "su", "ev", "süt", "kuş", "ağaç", "gül", "ay", "güneş", "baba", "anne", "top", "balık", "çay", "muz", "et", "gün", "el", "göz", "yol", "oda", "çorba", "tuz", "at"]
    },
    "2": {
        "ad": "başlangıç üstü (a1+)", 
        "puan": 15, 
        "liste": ["araba", "yeşil", "mavi", "çocuk", "ekmek", "deniz", "şehir", "kapı", "pencere", "masa", "sarı", "siyah", "beyaz", "uçak", "tren", "ördek", "aslan", "fare", "yatak", "kaşık", "çatal", "tabak", "bıçak", "ayna", "saat"]
    },
    "3": {
        "ad": "çok kolay (a2)", 
        "puan": 20, 
        "liste": ["elma", "kitap", "okul", "kalem", "çanta", "doktor", "öğrenci", "gazete", "hafta", "ayakkabı", "gömlek", "pantolon", "ceket", "şapka", "yağmur", "kar", "rüzgar", "çiçek", "bahçe", "mutfak", "banyo", "sinema", "tiyatro", "market", "bilet"]
    },
    "4": {
        "ad": "kolay (b1-)", 
        "puan": 25, 
        "liste": ["arkadaş", "gökyüzü", "portakal", "kelebek", "öğretmen", "lokanta", "elbise", "köprü", "otobüs", "bisiklet", "fabrika", "eczane", "hastane", "postane", "banka", "kamera", "telefon", "radyo", "ayna", "tarak", "sabun", "havlu", "yastık", "battaniye", "halı"]
    },
    "5": {
        "ad": "orta altı (b1+)", 
        "puan": 30, 
        "liste": ["bilgisayar", "kütüphane", "televizyon", "mühendis", "avukat", "gazeteci", "mevsim", "hava durumu", "tatil", "seyahat", "otel", "pasaport", "valiz", "harita", "pusula", "nehir", "dağ", "orman", "göl", "ada", "kale", "saray", "müze", "sergi", "konser"]
    },
    "6": {
        "ad": "orta üstü (b2)", 
        "puan": 40, 
        "liste": ["tehlike", "gelecek", "hediye", "eğlence", "kahvaltı", "yolculuk", "toplantı", "manzara", "kıyafet", "akıllı", "tembel", "çalışkan", "korku", "heyecan", "mutluluk", "üzüntü", "öfke", "cesaret", "gurur", "saygı", "sevgi", "nefret", "güven", "şüphe", "sabır"]
    },
    "7": {
        "ad": "ileri altı (c1-)", 
        "puan": 50, 
        "liste": ["özgürlük", "mükemmel", "fırsat", "tecrübe", "gelenek", "yetenek", "cesaret", "keşfetmek", "hoşgörü", "adalet", "eşitlik", "barış", "savaş", "hükümet", "kanun", "toplum", "kültür", "sanat", "bilim", "teknoloji", "ekonomi", "ticaret", "sanayi", "tarım", "sağlık"]
    },
    "8": {
        "ad": "ileri üstü (c1+)", 
        "puan": 60, 
        "liste": ["sorumluluk", "bağımsızlık", "hayal gücü", "medeniyet", "kütüphaneci", "karşılaştırma", "seçenek", "kaynak", "yöntem", "çözüm", "başarı", "başarısızlık", "deneyim", "yaratıcılık", "iletişim", "etkileşim", "gelişim", "değişim", "dönüşüm", "küreselleşme", "modernleşme", "çeşitlilik", "bütünlük", "denge", "istikrar"]
    },
    "9": {
        "ad": "çok zor (c2)", 
        "puan": 70, 
        "liste": ["yaratıcılık", "küreselleşme", "kişiselleştirme", "gerçekleştirmek", "bilinçaltı", "ödünç almak", "çelişki", "farkındalık", "sermaye", "enflasyon", "yatırım", "üretim", "tüketim", "istihdam", "rekabet", "strateji", "politika", "felsefe", "psikoloji", "sosyoloji", "antropoloji", "arkeoloji", "astronomi", "biyoloji", "kimya"]
    },
    "10": {
        "ad": "efsanevi uzman (expert)", 
        "puan": 80, 
        "liste": ["sürdürülebilirlik", "çentiklendirmek", "girişimcilik", "kamulaştırma", "çeşitlendirme", "kurumsallaştırmak", "detaylandırmak", "belgelendirmek", "özelleştirmek", "yapılandırmak", "ilişkilendirmek", "değerlendirmek", "karşılaştırılabilirlik", "sömürgeleştirmek", "demokratikleştirmek"]
    }
}

# --- GLOBAL AYARLAR ---
FS = 44100       
SURE = 4         
TOPLAM_SORU = 3  

# --- FONKSİYONLAR ---

def baslangic_ekrani():
    print(LOGO)
    print("🎮 OYUN KURALLARI:")
    print("1. Önce pratik yapmak istediğiniz hedef dili (İngilizce / Almanca) seçeceksiniz.")
    print("2. Ekranda Türkçe bir kelime göreceksiniz.")
    print("3. Sistem 'KAYIT BAŞLADI' dediğinde hedef dildeki karşılığını telaffuz edin.")
    print("🎖️  Oyun sonunda rütbeniz belirlenir ve GİZLİ BAŞARIMLARINIZ listelenir!")
    print("-----------------------------------------------------------\n")

def dil_sec():
    """Kullanıcıya pratik yapmak istediği dili seçtirir (Yeni Özellik)."""
    while True:
        print("🌐 HEDEF DİL SEÇİMİ:")
        print(" [1] İNGİLİZCE (English)")
        print(" [2] ALMANCA (Deutsch)")
        secim = input("\n👉 Lütfen bir dil numarası girin (1-2): ").strip()
        if secim == "1":
            return {"kod": "en", "tanima_kodu": "en-US", "ad": "İngilizce"}
        elif secim == "2":
            return {"kod": "de", "tanima_kodu": "de-DE", "ad": "Almanca"}
        print("\n⚠️ Geçersiz seçim! Lütfen 1 veya 2 yazın.\n")

def zorluk_sec():
    while True:
        print("\n📊 ZORLUK SEVİYELERİ:")
        for anahtar, veri in KELİMELER.items():
            print(f" [{anahtar.zfill(2)}] {veri['ad'].upper().ljust(30)} ({veri['puan']} Puan)")
            
        secim = input("\n👉 Lütfen oynamak istediğiniz seviyenin numarasını girin (1-10): ").strip()
        if secim in KELİMELER:
            return secim
        print("\n⚠️ Geçersiz seçim! Lütfen 1 ile 10 arasında bir rakam girin.\n")

def ses_kaydet():
    print("\n🎙️  Hazırlanın... 3 saniye içinde kayıt başlayacak.")
    for i in range(3, 0, -1):
        print(f"⏳ {i}...")
        time.sleep(1)
        
    print("🔴 >>> KAYIT BAŞLADI! Konuşun... <<<")
    kayit = sd.rec(int(SURE * FS), samplerate=FS, channels=1, dtype='int16')
    sd.wait()  
    print("⚪ Kayıt tamamlandı. Analiz ediliyor...\n")
    wav.write("gecici_ses.wav", FS, kayit)

def sesi_metne_cevir(dil_tanima_kodu):
    """Seçilen dile göre ses tanıma yapar."""
    recognizer = sr.Recognizer()
    with sr.AudioFile("gecici_ses.wav") as source:
        ses_verisi = recognizer.record(source)
        try:
            # Dil parametresi dinamik hale getirildi (en-US veya de-DE)
            metin = recognizer.recognize_google(ses_verisi, language=dil_tanima_kodu)
            return metin.lower().strip()
        except sr.UnknownValueError:
            print("🤷 Söylediğiniz kelime anlaşılamadı.")
            return ""
        except sr.RequestError:
            print("🌐 İnternet bağlantısı hatası!")
            return ""

def kelime_ceviri_al(turkce_kelime, hedef_dil_kodu):
    """Seçilen hedef dile göre googletrans ile çeviri yapar."""
    translator = Translator()
    try:
        ceviri = translator.translate(turkce_kelime, src='tr', dest=hedef_dil_kodu)
        return ceviri.text.lower().strip()
    except Exception:
        return "error"

def basarimlari_kontrol_et(puan, maks_puan, seviye_no, dogru_sayisi, en_uzun_dogru_kelime, son_soru_dogru_mu):
    print("\n🏅 KAZANILAN BAŞARIMLAR:")
    kazanilan_basarim_var_mi = False

    if puan == maks_puan and maks_puan > 0:
        print("🥇 [KUSURSUZ TELAFFUZ] -> Hiç hata yapmadan tüm soruları bildiniz!")
        kazanilan_basarim_var_mi = True
        
    if puan == maks_puan and seviye_no == "10" and maks_puan > 0:
        print("👑 [DİL KRALI] -> En üst seviye olan EFSANEVİ UZMAN modda kusursuz oynadınız!")
        kazanilan_basarim_var_mi = True

    if dogru_sayisi >= 1:
        print("🌱 [İLK ADIM] -> En az 1 kelimeyi başarıyla telaffuz ettiniz.")
        kazanilan_basarim_var_mi = True

    if dogru_sayisi == 0:
        print("🥶 [ŞANSSIZ GÜN] -> Bu sefer hiç puan alamadınız ama pes etmek yok!")
        kazanilan_basarim_var_mi = True

    if isinstance(en_uzun_dogru_kelime, int) and en_uzun_dogru_kelime >= 10:
        print("🦕 [DEVLERİN KELİMESİ] -> 10 harften daha uzun ve zor bir kelimeyi tekte bildiniz!")
        kazanilan_basarim_var_mi = True

    if dogru_sayisi == 1 and son_soru_dogru_mu is True:
        print("⚽ [SON SANİYE GOLÜ] -> Son soruyu doğru bilerek oyunu sıfır çekmekten kurtardınız!")
        kazanilan_basarim_var_mi = True

    try:
        su_an = datetime.datetime.now().hour
        if su_an >= 22 or su_an <= 6:
            print("🦉 [GECE KUŞU TELAFFUZU] -> Herkes uyurken dil pratiği yapmaya devam ediyorsunuz!")
            kazanilan_basarim_var_mi = True
    except Exception:
        pass 

    if puan == maks_puan and seviye_no in ["1", "2", "3"] and maks_puan > 0:
        print("🛠️  [ÇIRAKLIKTAN USTALIĞA] -> Temel seviyeleri başarıyla fethettiniz!")
        kazanilan_basarim_var_mi = True

    if puan >= 100:
        print("💎 [HIZLI YÜKSELİŞ] -> Tek bir oyunda 100 puan barajını aşmayı başardınız!")
        kazanilan_basarim_var_mi = True

    if puan >= 150:
        print("🔥 [REKORTMEN] -> 150 puandan fazla toplayarak harika bir skora imza attınız!")
        kazanilan_basarim_var_mi = True

    if puan == maks_puan and int(seviye_no) >= 7:
        print("📜 [DİPLOMAT SIFATI] -> Üst düzey zorluklarda en yüksek rütbeyi kaparak listenin zirvesine yerleştiniz!")
        kazanilan_basarim_var_mi = True

    if not kazanilan_basarim_var_mi:
        print("Belirli kriterleri sağlayarak yeni gizli başarımları keşfedin!")

def rutbe_hesapla(puan, maks_puan):
    print("\n🎖️  DİL YETERLİLİK RÜTBENİZ:")
    if puan == 0 or maks_puan == 0:
        print("🔹 RÜTBE: ACEMİ ÖĞRENCİ (Tourist)")
    else:
        yuzde = (puan / maks_puan) * 100
        if yuzde <= 33:
            print("🔹 RÜTBE: SOKAK REHBERİ (Beginner)")
        elif yuzde <= 50:
            print("🔹 RÜTBE: KÜLTÜR ELÇİSİ (Intermediate)")
        elif yuzde <= 75:
            print("🔹 RÜTBE: İLERİ SEVİYE HATİP (Advanced)")
        elif yuzde < 100:
            print("🔹 RÜTBE: AKICI AKADEMİSYEN (Fluent Professional)")
        else:
            print("🔹 RÜTBE: ANA DİL SEVİYESİ (Native Speaker)")

def oyunu_baslat():
    puan = 0
    dogru_sayisi = 0
    en_uzun_dogru_kelime = 0
    son_soru_dogru_mu = False  
    
    baslangic_ekrani()
    
    # 1. Adım: Kullanıcı Dil Seçer
    secilen_dil = dil_sec()
    
    # 2. Adım: Kullanıcı Zorluk Seçer
    seviye_no = zorluk_sec()
    
    secilen_seviye = KELİMELER[seviye_no]
    kelime_listesi = secilen_seviye["liste"]
    seviye_adi = secilen_seviye["ad"]
    soru_puani = secilen_seviye["puan"]
    
    sorulacak_kelimeler = random.sample(kelime_listesi, min(TOPLAM_SORU, len(kelime_listesi)))
    
    print(f"\n🚀 {secilen_dil['ad'].upper()} dilinde, {seviye_adi.upper()} seviyesinde oyun başlıyor! Toplam {TOPLAM_SORU} soru.")
    
    for sira, tr_kelime in enumerate(sorulacak_kelimeler, 1):
        print(f"\n------------------ Soru {sira} / {TOPLAM_SORU} ------------------")
        print(f"🇹🇷 Türkçe Kelime: ⭐ {tr_kelime.upper()} ⭐")
        
        # Seçilen dil koduna göre çeviri dinamik alınır
        dogru_cevap = kelime_ceviri_al(tr_kelime, secilen_dil["kod"])
        ses_kaydet()
        
        # Seçilen dil tanıma koduna göre ses analiz edilir
        oyuncu_tahmini = sesi_metne_cevir(secilen_dil["tanima_kodu"])
        
        print(f"🗣️ Sizin Telaffuzunuz: '{oyuncu_tahmini}'")
        print(f"🤖 Doğru Çeviri ({secilen_dil['ad']}): '{dogru_cevap}'")
        
        if oyuncu_tahmini == dogru_cevap and dogru_cevap != "" and dogru_cevap != "error":
            print(WIN_ART)
            puan += soru_puani
            dogru_sayisi += 1
            
            kelime_uzunlugu = len(str(dogru_cevap))
            if kelime_uzunlugu > en_uzun_dogru_kelime:
                en_uzun_dogru_kelime = kelime_uzunlugu
            
            if sira == TOPLAM_SORU:
                son_soru_dogru_mu = True
                
            print(f"🎉 +{soru_puani} Puan kazandınız!")
        else:
            print(LOSE_ART)
            if sira == TOPLAM_SORU:
                son_soru_dogru_mu = False
            
        print(f"💰 Güncel Puanınız: {puan}")
        time.sleep(1.5)

    # --- OYUN BİTTİ EKRANI ---
    print("\n===========================================================")
    print("🏁 OYUN BİTTİ! 🏁")
    print(f"📊 Seçilen Dil: {secilen_dil['ad']} | Toplam Puanınız: {puan} (Doğru Sayısı: {dogru_sayisi}/{TOPLAM_SORU})")
    
    maks_puan = TOPLAM_SORU * soru_puani
    
    rutbe_hesapla(puan, maks_puan)
    
    basarimlari_kontrol_et(
        puan=puan, 
        maks_puan=maks_puan, 
        seviye_no=seviye_no, 
        dogru_sayisi=dogru_sayisi, 
        en_uzun_dogru_kelime=en_uzun_dogru_kelime, 
        son_soru_dogru_mu=son_soru_dogru_mu
    )
    
    print("===========================================================")

# Programı doğrudan çalıştır
if __name__ == "__main__":
    oyunu_baslat()