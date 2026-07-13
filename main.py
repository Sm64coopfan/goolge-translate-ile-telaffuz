import time
import datetime
import random
import json  # Hafıza yönetimi için eklendi
import os    # Dosya kontrolü için eklendi
import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator

# --- GÖRSEL VE ASCII ELEMENTLERİ ---
LOGO = """
===========================================================
 🎯  Google Translate İle Telaffuz: ÇOK DİLLİ KONUŞMA OYUNU  🎯
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
        "liste": ["kedi", "köpek", "şu", "ev", "süt", "kuş", "ağaç", "gül", "ay", "güneş", "baba", "anne", "top", "balık", "çay", "muz", "et", "gün", "el", "göz", "yol", "oda", "çorba", "tuz", "at"]
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
        "ad": "efsanevi (expert)", 
        "puan": 80, 
        "liste": ["sürdürülebilirlik", "çentiklendirmek", "girişimcilik", "kamulaştırma", "çeşitlendirme", "kurumsallaştırmak", "detaylandırmak", "belgelendirmek", "özelleştirmek", "yapılandırmak", "ilişkilendirmek", "değerlendirmek", "karşılaştırılabilirlik", "sömürgeleştirmek", "demokratikleştirmek"]
    }
}

# --- GLOBAL AYARLAR ---
FS = 45000       
SURE = 4         
TOPLAM_SORU = 3  
SKOR_DOSYASI = "skor_tablosu.json" 

# --- YARDIMCI HAFIZA FONKSİYONLARI ---
def skoru_yukle():
    if os.path.exists(SKOR_DOSYASI):
        try:
            with open(SKOR_DOSYASI, "r", encoding="utf-8") as f:
                return json.load(f).get("kalici_toplam_puan", 0)
        except Exception:
            return 0
    return 0

def skoru_kaydet(puan):
    try:
        with open(SKOR_DOSYASI, "w", encoding="utf-8") as f:
            json.dump({"kalici_toplam_puan": puan}, f)
    except Exception:
        pass

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
    while True:
        print("🌐 HEDEF DİL SEÇİMİ:")
        print(" İNGİLİZCE (English)")
        print(" ALMANCA (Deutsch)")
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
    recognizer = sr.Recognizer()
    with sr.AudioFile("gecici_ses.wav") as source:
        ses_verisi = recognizer.record(source)
        try:
            metin = recognizer.recognize_google(ses_verisi, language=dil_tanima_kodu)
            return metin.lower().strip()
        except sr.UnknownValueError:
            print("🤷 Söylediğiniz kelime anlaşılamadı.")
            return ""
        except sr.RequestError:
            print("🌐 İnternet bağlantısı hatası!")
            return ""

def kelime_ceviri_al(turkce_kelime, hedef_dil_kodu):
    translator = Translator()
    try:
        ceviri = translator.translate(turkce_kelime, src='tr', dest=hedef_dil_kodu)
        return ceviri.text.lower().strip()
    except Exception:
        return "error"

def basarimlari_kontrol_et(puan, maks_puan, seviye_no, dogru_sayisi, en_uzun_dogru_kelime, son_soru_dogru_mu):
    print("\n🏅 KAZANILAN BAŞARIMLAR:")
    kazanilan_basarim_var_mi = False

    # 1. Kusursuz Telaffuz
    if puan == maks_puan and maks_puan > 0:
        print("🥇 [KUSURSUZ TELAFFUZ] -> Hiç hata yapmadan tüm soruları bildiniz!")
        kazanilan_basarim_var_mi = True
        
    # 2. Dil Kralı
    if puan == maks_puan and seviye_no == "10" and maks_puan > 0:
        print("👑 [DİL KRALI] -> En üst seviye olan EFSANEVİ modda kusursuz oynadınız!")
        kazanilan_basarim_var_mi = True

    # 3. İlk Adım
    if dogru_sayisi >= 1:
        print("🌱 [İLK ADIM] -> En az 1 kelimeyi başarıyla telaffuz ettiniz.")
        kazanilan_basarim_var_mi = True

    # 4. Şanssız Gün
    if dogru_sayisi == 0:
        print("🥶 [ŞANSSIZ GÜN] -> Bu sefer hiç puan alamadınız ama pes etmek yok!")
        kazanilan_basarim_var_mi = True

    # 5. Devlerin Kelimesi
    if isinstance(en_uzun_dogru_kelime, int) and en_uzun_dogru_kelime >= 10:
        print("🦕 [DEVLERİN KELİMESİ] -> 10 harften daha uzun ve zor bir kelimeyi tekte bildiniz!")
        kazanilan_basarim_var_mi = True

    # 6. Son Saniye Golü
    if dogru_sayisi == 1 and son_soru_dogru_mu is True:
        print("⚽ [SON SANİYE GOLÜ] -> Son soruyu doğru bilerek oyunu sıfır çekmekten kurtardınız!")
        kazanilan_basarim_var_mi = True

    # 7. Gece Kuşu Telaffuzu
    try:
        su_an = datetime.datetime.now().hour
        if su_an >= 22 or su_an <= 6:
            print("🦉 [GECE KUŞU TELAFFUZU] -> Herkes uyurken dil pratiği yapmaya devam ediyorsunuz!")
            kazanilan_basarim_var_mi = True
    except Exception:
        pass 

    # 8. Çıraklıktan Ustalığa
    if puan == maks_puan and seviye_no in ["1", "2", "3"] and maks_puan > 90:
        print("🛠️  [ÇIRAKLIKTAN USTALIĞA] -> Temel seviyeleri başarıyla fethettiniz!")
        kazanilan_basarim_var_mi = True

    # 9. Hızlı Yükseliş
    if puan >= 1000:
        print("💎 [HIZLI YÜKSELİŞ] -> oyunda 1000 puan barajını aşmayı başardınız!")
        kazanilan_basarim_var_mi = True

    # 10. Rekortmen
    if puan >= 5000:
        print("🔥 [REKORTMEN] -> 5000 puandan fazla toplayarak harika bir skora imza attınız!")
        kazanilan_basarim_var_mi = True
     
    # 11. Kral
    if puan >= 10000:
        print("👑 [KRAL] -> 10000 puandan fazla toplayarak resmen bir kral ilan edildiniz!")
        kazanilan_basarim_var_mi = True

    # 12. Hükümdar

    if puan >= 50000:
        print("👑 [HÜKÜMDAR] -> TEBRİKLER ! 50000 puan topladınız ve kelimeler diyarı nın hühümdarı oldunuz!")
        kazanilan_basarim_var_mi = True

    # 13. Diplomat Sıfatı
    if puan == maks_puan and int(seviye_no) >= 7:
        print("📜 [DİPLOMAT SIFATI] -> Üst düzey zorluklarda en yüksek rütbeyi kaparak listenin zirvesine yerleştiniz!")
        kazanilan_basarim_var_mi = True
    # 14. Dil Avcısı
    if dogru_sayisi == TOPLAM_SORU and int(seviye_no) >= 5:
        print("🎯 [DİL AVCISI] -> Orta ve üzeri seviyelerde tüm kelimeleri eksiksiz avladınız!")
        kazanilan_basarim_var_mi = True

    # 15. İstikrarlı Kelime bükücü
    if isinstance(en_uzun_dogru_kelime, int) and en_uzun_dogru_kelime >= 15:
        print("🧠 [SON KELİME BÜKÜCÜ!] -> 15 harften uzun, telaffuzu aşırı zor devasa bir kelimeyi devirdiniz!")
        kazanilan_basarim_var_mi = True
     
    if not kazanilan_basarim_var_mi:
        print("🤷 Henüz özel bir başarım kilidi açılmadı.")
    print("-" * 59 + "\n")

def rutbe_belirle(toplam_puan):
    print("🎖️  OYUNCU RÜTBENİZ:")
    if toplam_puan >=50:
        print("⚡ Rütbe: ÇAYLAK (Pratik yapmaya devam edin!)")
    elif toplam_puan >= 100:
        print("📚 Rütbe: ÖĞRENMEYE İSTEKLİ (Temeliniz oluşuyor)")
    elif toplam_puan <= 500:
        print("🚀 Rütbe: AKICI KONUŞUR (Güzel telaffuz, tebrikler!)")
    elif toplam_puan >= 500:
        print("🌟 Rütbe: DİL ÜSTADI / NATIVE SPEAKER (Harika bir performans!)")
    print("=" * 59 + "\n")

# --- ANA OYUN DÖNGÜSÜ ---
def oyna():
    baslangic_ekrani()
    
    gecmis_toplam_puan = skoru_yukle()
    if gecmis_toplam_puan > 0:
        print(f"💾 Hoş geldiniz! Önceki oyunlardan biriken Toplam Puanınız: {gecmis_toplam_puan}\n")
    
    hedef_dil = dil_sec()
    print(f"\n✨ Harika! {hedef_dil['ad']} dilinde pratik yapacaksınız.\n")
    
    seviye_no = zorluk_sec()
    seviye = KELİMELER[seviye_no]
    
    toplam_puan = 0
    dogru_sayisi = 0
    en_uzun_dogru_kelime = 0
    maks_puan = TOPLAM_SORU * seviye["puan"]
    son_soru_dogru_mu = False
    
    sorulacak_kelimeler = random.sample(seviye["liste"], min(TOPLAM_SORU, len(seviye["liste"])))
    
    print(f"\n🚀 {seviye['ad'].upper()} seviyesi başladı! Toplam {TOPLAM_SORU} soru sorulacak.")
    print(f"Her doğru cevap için +{seviye['puan']} puan kazanacaksınız.\n")
    
    try:
        for sira, tr_kelime in enumerate(sorulacak_kelimeler, 1):
            print(f"================ SORU {sira} / {TOPLAM_SORU} ================")
            print(f"Anlamı Sorulan Türkçe Kelime: ➔  {tr_kelime.upper()}")
            
            hedef_cevap = kelime_ceviri_al(tr_kelime, hedef_dil["kod"])
            if hedef_cevap == "error":
                print("⚠️ Çeviri servisine şu an ulaşılamıyor, bu soru atlanıyor.")
                continue
                
            ses_kaydet()
            kullanici_ses_metni = sesi_metne_cevir(hedef_dil["tanima_kodu"])
            
            print(f"🗣️  Sizin Telaffuzunuz  : {kullanici_ses_metni if kullanici_ses_metni else '[Anlaşılamadı]'}")
            print(f"🎯 Doğru Hedef Kelime : {hedef_cevap}")
            
            if kullanici_ses_metni == hedef_cevap and kullanici_ses_metni != "":
                print(WIN_ART)
                toplam_puan += seviye["puan"]
                dogru_sayisi += 1
                if len(hedef_cevap) > en_uzun_dogru_kelime:
                    en_uzun_dogru_kelime = len(hedef_cevap)
                son_soru_dogru_mu = True
                
                skoru_kaydet(gecmis_toplam_puan + toplam_puan)
            else:
                print(LOSE_ART)
                son_soru_dogru_mu = False
                
            print(f"📊 Bu Tur Puanınız: {toplam_puan} | 💾 Genel Toplam Puanınız: {gecmis_toplam_puan + toplam_puan}\n")
            time.sleep(1.5)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Oyun aniden durduruldu! Skorlarınız başarıyla korundu.")
        print(f"💾 Güncel Genel Toplam Puanınız: {gecmis_toplam_puan + toplam_puan}")
        return
        
    print("=================== OYUN BİTTİ ===================")
    print(f"🏆 Bu Tur Skorunuz: {toplam_puan} / {maks_puan}")
    print(f"💾 Genel Toplam Skorunuz: {gecmis_toplam_puan + toplam_puan}")
    print(f"✅ Doğru Telaffuz Sayısı: {dogru_sayisi} / {TOPLAM_SORU}")
    
    basarimlari_kontrol_et(toplam_puan, maks_puan, seviye_no, dogru_sayisi, en_uzun_dogru_kelime, son_soru_dogru_mu)
    rutbe_belirle(toplam_puan) 

if __name__ == "__main__":
    oyna()
