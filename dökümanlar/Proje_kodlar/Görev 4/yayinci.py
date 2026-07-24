import paho.mqtt.client as mqtt

# 1. Bilgisayarda mosquitto broker çalıştığı için adres localhost
BROKER_ADRESI = "localhost"
PORT = 1883
TOPIC = "arac/yuk"

# V2 API'sine uygun on_connect callback imzası (properties ve reason_code içerir)
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"[BAŞARILI] Mosquitto broker'a ({BROKER_ADRESI}:{PORT}) bağlanıldı!")
    else:
        print(f"[HATA] Bağlantı başarısız. Sebep Kodu: {reason_code}")

def main():
    # paho-mqtt 2.x zorunluluğu: CallbackAPIVersion.VERSION2 belirtilmek zorunda
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "RobotKolPublisher")
    client.on_connect = on_connect

    try:
        # Broker'a bağlan (Timeout 60 saniye)
        client.connect(BROKER_ADRESI, PORT, 60)
    except Exception as e:
        print(f"[HATA] Broker'a ulaşılamadı. Mosquitto servisinin çalıştığından emin olun: {e}")
        return

    # Arka planda ağı dinleyen thread'i başlat
    client.loop_start()

    print("\n--- Yayıncı (Publisher) Başlatıldı ---")
    print("Göndermek için RED, GREEN veya BLUE yazıp Enter'a basın.")
    print("Çıkmak için 'q' tuşuna basın.\n")

    while True:
        try:
            renk = input("Gönderilecek Renk: ").strip().upper()

            if renk == 'Q':
                print("[BİLGİ] Yayıncı kapatılıyor...")
                break

            if renk in ['RED', 'GREEN', 'BLUE']:
                # Mesajı yayınla (publish)
                client.publish(TOPIC, renk)
                print(f"[GONDERILDI] Renk: {renk}")
            else:
                print("[UYARI] Geçersiz giriş! Sadece RED, GREEN veya BLUE kullanın.")

        except KeyboardInterrupt:
            print("\n[BİLGİ] Yayıncı kapatılıyor...")
            break

    # Bağlantıyı temiz bir şekilde sonlandır
    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    main()
