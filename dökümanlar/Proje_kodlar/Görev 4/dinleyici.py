import paho.mqtt.client as mqtt
import datetime

# KULLANICI NOTU: Buradaki IP adresini 1. bilgisayarın (Yayıncı/Broker) yerel ağdaki IP'si ile değiştirin
BROKER_IP = "192.168.1.100"
PORT = 1883
TOPIC = "arac/yuk"

# V2 API'sine uygun on_connect callback imzası
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"[BAŞARILI] Broker'a ({BROKER_IP}:{PORT}) bağlanıldı!")
        # Bağlantı kurulur kurulmaz konuya abone (subscribe) oluyoruz
        client.subscribe(TOPIC)
        print(f"[BİLGİ] '{TOPIC}' konusuna abone olundu. Mesajlar bekleniyor...\n")
    else:
        print(f"[HATA] Bağlantı başarısız. Sebep Kodu: {reason_code}")

# V2 API'sinde gelen mesajları karşılayan callback
def on_message(client, userdata, msg):
    # O anki zaman damgasını oluştur
    simdi = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Gelen mesajı (byte array) utf-8 formatında string'e çevir
    mesaj = msg.payload.decode('utf-8')

    # Terminale açıkça yazdır
    print(f"[{simdi}] [ALINDI] Renk: {mesaj}")

def main():
    # paho-mqtt 2.x API kuralı
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "OtonomAracSubscriber")

    # Callback fonksiyonlarını ata
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        # Broker'a bağlan
        print(f"[BİLGİ] {BROKER_IP} adresine bağlanılmaya çalışılıyor...")
        client.connect(BROKER_IP, PORT, 60)
    except Exception as e:
        print(f"[HATA] {BROKER_IP} adresindeki Broker'a ulaşılamadı.")
        print(f"Hata detayı: {e}")
        return

    # Sürekli olarak yeni mesajları beklemesini ve ağı dinlemesini sağlayan blocking loop
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n[BİLGİ] Dinleyici sonlandırılıyor, bağlantı kesiliyor...")
        client.disconnect()

if __name__ == "__main__":
    main()
