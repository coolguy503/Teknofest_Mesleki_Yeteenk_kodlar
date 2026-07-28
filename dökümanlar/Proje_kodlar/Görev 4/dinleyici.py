import paho.mqtt.client as mqtt
import datetime

#yayıncı bilgisayarın ip'si
BROKER_IP = "192.168.1.100"
PORT = 1883
TOPIC = "arac/yuk"

# v2 api'sine uygun on_connect callback imzası
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"[BAŞARILI] Broker'a ({BROKER_IP}:{PORT}) bağlanıldı!")
        # bağlantı sonrası subscribe.
        client.subscribe(TOPIC)
        print(f"[BİLGİ] '{TOPIC}' konusuna abone olundu. Mesajlar bekleniyor...\n")
    else:
        print(f"[HATA] Bağlantı başarısız. Sebep Kodu: {reason_code}")

# v2 api'sinde gelen mesajları karşılayan callback
def on_message(client, userdata, msg):
    # zaman damgası
    simdi = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #mesajı utf-8 formatında string'e çevir
    mesaj = msg.payload.decode('utf-8')

    #terminal çıktı
    print(f"[{simdi}] [ALINDI] Renk: {mesaj}")

def main():
    # paho-mqtt 2.x API kuralı
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "OtonomAracSubscriber")

    # callback fonksiyonları
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        # broker bağlantı
        print(f"[BİLGİ] {BROKER_IP} adresine bağlanılmaya çalışılıyor...")
        client.connect(BROKER_IP, PORT, 60)
    except Exception as e:
        print(f"[HATA] {BROKER_IP} adresindeki Broker'a ulaşılamadı.")
        print(f"Hata detayı: {e}")
        return

    # yeni mesajları beklemesini ve ağı dinlemesini sağlayan blocking loop
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n[BİLGİ] Dinleyici sonlandırılıyor, bağlantı kesiliyor...")
        client.disconnect()

if __name__ == "__main__":
    main()
