# TEKNOFEST 2026 — Akıllı Fabrika Sistemleri Programlama (Yarı Final)

Bu depo, TEKNOFEST 2026 Akıllı Fabrika Sistemleri Programlama kategorisi
yarı final teknik şartnamesi kapsamında hazırlanan Görev 1, Görev 2 ve
Görev 4 dosyalarını içerir.

## İçerik

- `gorev1/` — Sistem Algoritması Tasarımı (Robot Kol + Otonom Araç)
  - `algoritma.pdf` — akış şemaları ve sözde kod
- `gorev2/` — Arayüz Tasarımı ve Step Motor Kontrolü
  - `arayuz.py` — tkinter tabanlı kontrol arayüzü
  - `motor.ino` — Arduino (AccelStepper) firmware
  - `README.txt` — kurulum ve test adımları
- `gorev4/` — MQTT ile Haberleşme
  - `yayinci.py` — yayıncı (broker + robot kol tarafı)
  - `dinleyici.py` — dinleyici (araç tarafı)
- `requirements.txt` — Python bağımlılıkları

## Kurulum

pip install -r requirements.txt


Donanım bağlantıları ve kullanım detayları için ilgili görev klasöründeki
README/PDF dosyalarına bakınız.

## Standart Ayarlar (Şartname Gereği)

- Step Motor Sürücü: DM556, PUL=D2, DIR=D3, 1/8 mikro adım (1600 adım/tur)
- MQTT: paho-mqtt 2.1.0, mosquitto broker, topic: `arac/yuk`

## Nasıl Çalıştırılır (Genel Akış)

1. **Görev 1 (algoritma.pdf):** Sadece dokümantasyon, çalıştırma gerekmez.

2. **Görev 2 (Arayüz + Step Motor):**
   - `motor.ino`'yu Arduino IDE veya `arduino-cli` ile Arduino Uno'ya yükle
     (DM556 sürücü bağlantısı: PUL=D2, DIR=D3, 1/8 mikro adım).
   - `arayuz.py` içindeki `SERIAL_PORT` değerini kendi portunla değiştir.
   - Çalıştır: `python arayuz.py`

3. **Görev 4 (MQTT):**
   - Broker bilgisayarında mosquitto kur ve başlat
     (`listener 1883`, `allow_anonymous true` ayarlı).
   - Aynı bilgisayarda: `python yayinci.py`
   - Karşı bilgisayarda (`dinleyici.py` içindeki `BROKER_IP`'yi broker'ın
     IP'siyle güncelleyip): `python dinleyici.py`
   - İki bilgisayarın aynı ağda olduğundan ve 1883 portunun firewall'da
     açık olduğundan emin ol.
