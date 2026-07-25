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
