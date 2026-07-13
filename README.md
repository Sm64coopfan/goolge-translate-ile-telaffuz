# goolge-translate-ile-telaffuz
bu bir dil telaffuz uygulamasıdır


markdown# 🎯 Google Translate ile Telaffuz: Çok Dilli Konuşma Oyunu

Bu proje, Python kullanarak eğlenceli bir şekilde yabancı dil telaffuz pratiği yapmanızı sağlayan interaktif bir terminal oyunudur. Ekrana gelen Türkçe kelimelerin seçtiğiniz hedef dildeki (İngilizce veya Almanca) karşılıklarını sesli olarak doğru telaffuz etmeye çalışırsınız.

---

## ✨ Özellikler

- 🌐 **Çok Dilli Pratik:** İngilizce (en-US) , Almanca (de-DE) , Fransızca (fr-FR) ve ispanyolca (es-ES) dil seçenekleri.
- 📊 **10 Seviyeli Kelime Sözlüğü:** A1 seviyesinden Expert (Efsanevi) seviyeye kadar geniş kelime havuzu.
- 💾 **Kalıcı Skor Sistemi:** Oyunu kapatsanız veya `CTRL+C` ile durdursanız bile toplam puanınız `skor_tablosu.json` dosyasında güvende kalır.
- 🏆 **15 Gizli Başarım ve Rütbe:** Her turun performansına göre hesaplanan eğlenceli rütbeler ve gizli başarımlar.
- 🛑 **Güvenli Çıkış Koruması:** Oyun aniden kesilirse mevcut turdaki puanlarınızı kalıcı hafızaya işler.

---

## 🛠️ Kurulum ve Gerekli Kütüphaneler

Projenin çalışabilmesi için bilgisayarınızda **Python 3.11** kurulu olmalıdır. `os` ve `json` kütüphaneleri Python ile yerleşik olarak gelir; harici olarak yüklemeniz gerekmez.

Gerekli olan diğer harici kütüphaneleri terminalinizde aşağıdaki komutu çalıştırarak yükleyebilirsiniz:

```bash
pip install sounddevice scipy SpeechRecognition googletrans==3.1.0a0
```

> **Önemli Not:** `googletrans` kütüphanesinin kararlı çalışması için yukarıdaki komutta belirtilen `3.1.0a0` sürümünü yüklemeniz önerilir. Ayrıca bilgisayarınızda çalışan bir **mikrofon** ve **internet bağlantısı** bulunmalıdır.

---

## 🎮 Nasıl Oynanır?

1. Proje klasöründe bir terminal açın ve oyunu başlatın:
   ```bash
   python main.py
   ```
2. **Hedef Dil Seçimi:** Pratik yapmak istediğiniz dili (İngilizce veya Almanca) seçin.
3. **Zorluk Seçimi:** 1 ile 10 arasında bir zorluk seviyesi belirleyin.
4. **Kayıt Aşaması:** Ekrandaki Türkçe kelimeyi gördükten sonra `>>> KAYIT BAŞLADI! <<<` uyarısıyla birlikte hedef dildeki karşılığını mikrofonunuza telaffuz edin. (Her soru için 4 saniye süreniz vardır).
5. **Sonuç:** Sistem sesinizi analiz eder, Google Translate üzerindeki doğru karşılıkla karşılaştırır ve puanınızı hesaplar.

---

## 🎖️ Rütbeler ve Başarımlar

- **Rütbeler:**
- *Başlangıç, Çaylak, Öğrenmeye istekli, Akıcı konuşur, Uzman mütercim, Dil üstadı ve Kelimelerin Efendisi.*
- **Başarımlar:** *Kusursuz Telaffuz, Dil Kralı, İlk Adım, Şanssız Gün, Devlerin Kelimesi, Son Saniye Golü, Gece Kuşu Telaffuzu, Çıraklıktan Ustalığa, Hızlı Yükseliş, Rekortmen, Kral, Hükümdar, Diplomat Sıfatı.*

> 💡 **Not:** Başarımlar ve rütbeler oyunun adil kalması için kalıcı puandan bağımsız olarak **sadece o an oynadığınız turun skoruna** göre hesaplanır.

---

## 🚨 Puanları Sıfırlama

Eğer tüm geçmişinizi silip puanınızı sıfırlamak isterseniz, proje klasöründe otomatik olarak oluşan **`skor_tablosu.json`** dosyasını silmeniz yeterlidir.
