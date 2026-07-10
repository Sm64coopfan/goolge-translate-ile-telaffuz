# goolge-translate-ile-telaffuz
bu bir dil telaffuz uygulamasıdır


markdown# 🎯 Google Translate İle Telaffuz: Çok Dilli Konuşma ve Telaffuz Oyunu

Bu proje, Python programlama dili kullanılarak geliştirilmiş, oyuncuların **İngilizce** ve **Almanca** kelime telaffuzlarını dinamik olarak test eden ve değerlendiren eğlenceli bir konsol (terminal) oyunudur. Oyunlaştırma (Gamification) mekanikleriyle zenginleştirilmiş olup, dil öğrenimini interaktif hale getirmeyi amaçlar.

---

## 🚀 Özellikler

- **Çok Dilli Altyapı:** Oyuncular oyun başında İngilizce veya Almanca dillerinden birini seçebilir.
- **10 Farklı Zorluk Seviyesi:** CEFR standartlarına uygun (A1 seviyesinden Expert uzmanlık seviyesine kadar) tam 10 kademeli zorluk ayarı.
- **Geniş Kelime Havuzu:** Her seviye için özenle seçilmiş, oyun her başladığında rastgele değişen devasa kelime listeleri.
- **Dinamik Ses Kaydı ve Tanıma:** Mikrofon verisini anlık yakalama ve Google Speech Recognition altyapısı ile anında metne dönüştürme.
- **Canlı Çeviri Kontrolü:** `googletrans` kütüphanesi entegrasyonu ile kelimelerin doğruluğunu bulut üzerinden anlık doğrulama.
- **6 Kademeli Rütbe Sistemi:** Başarı yüzdesine göre oyuncuya verilen dinamik rütbeler (Tourist, Beginner, ... , Native Speaker).
- **11 Gizli Başarım (Achievements):** Oyuncuyu tekrar oynamaya teşvik eden özel unvanlar (Gece Kuşu, Son Saniye Golü, Devlerin Kelimesi vb.).
- **Kullanıcı Dostu ASCII Arayüz:** Emojiler ve temiz konsol çizimleriyle zenginleştirilmiş scannable görünüm.

---

## 📦 Gerekli Kütüphaneler ve Kurulum

Projenin çalışabilmesi için bilgisayarınızda bir **mikrofon** bulunmalı ve ses tanıma servisleri için **internet bağlantısı** aktif olmalıdır.

Aşağıdaki komutu terminalinizde çalıştırarak gerekli tüm kütüphaneleri tek seferde yükleyebilirsiniz:

```bash
pip install sounddevice scipy SpeechRecognition googletrans==4.0.0-rc1
```

> **Not:** `googletrans` kütüphanesinin Google API'leri ile kararlı çalışabilmesi için özellikle `4.0.0-rc1` sürümünün yüklenmesi önerilir.

---

## 🎮 Nasıl Oynanır?

1. Proje klasöründeyken terminale şu komutu yazarak oyunu başlatın:
   ```bash
   python main.py
   ```
2. Karşınıza gelen menüden pratik yapmak istediğiniz dili (**İngilizce** veya **Almanca**) seçin.
3. 10 farklı zorluk seviyesinden kendinize uygun olanın numarasını girin.
4. Ekranda beliren Türkçe kelimeyi görün.
5. Sistem **"🔴 >>> KAYIT BAŞLADI! Konuşun... <<<"** uyarısını verdiğinde, mikrofona doğru kelimenin seçtiğiniz dildeki karşılığını net bir şekilde telaffuz edin.
6. 3 sorunun ardından rütbenizi ve kazandığınız gizli başarımları inceleyin!

---

## 🛠️ Teknik Mimari ve Kod Yapısı

Proje, nesne yönelimli karmaşadan uzak, okunabilirliği ve sunum kolaylığını artırmak adına **tamamen modüler fonksiyonlar (prosedürel)** ile geliştirilmiştir:

- `dil_sec()` & `zorluk_sec()`: Kullanıcı tercihlerini alan ve ses motorunu dinamik olarak yapılandıran fonksiyonlar.
- `ses_kaydet()`: `sounddevice` ile mikrofonu dinleyip veriyi `scipy.io.wavfile` ile geçici bir `.wav` dosyasına yazan kısım.
- `sesi_metne_cevir()`: `speech_recognition` kütüphanesini kullanarak sesi ilgili dil kodunda (`en-US` / `de-DE`) işleyen motor.
- `kelime_ceviri_al()`: `googletrans.Translator` sınıfı ile Türkçe kelimenin hedef dildeki mutlak karşılığını bulan yapı.
- `rutbe_hesapla()` & `basarimlari_kontrol_et()`: Oyun sonu istatistiklerini ve başarı kriterlerini (tarih/saat, kelime uzunluğu, doğru serisi) denetleyen oyunlaştırma katmanı.

---

## 🏆 Değerlendirme Kriterleri Karşılanma Durumu

Ses kaydı, dönüştürme ve API doğrulaması entegre çalışıyor.
Seviye zorluğuna göre katlanarak artan puanlama mevcuttur.
Kullanıcıya tam 10 farklı seçenek sunulmaktadır.
Sorular bitince oyun durur ve detaylı performans özeti basılır.
Görsel ASCII şablonları ve fonksiyonel emojiler kullanılmıştır.
Çok dilli destek (Almanca/İngilizce), 13 adet gizli başarım ve zamana duyarlı dinamik ödüller eklenmiştir.

