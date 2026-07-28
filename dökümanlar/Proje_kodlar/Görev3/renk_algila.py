import cv2
import numpy as np

# pip install opencv-python==4.5.4.60 numpy==1.26.4

# kamerayi ac
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

esik = 5000  # bunun altindaki alanlari tespit yok sayiyoruz
kernel = np.ones((5, 5), np.uint8)

son_renk = ""

print("baslatildi, cikmak icin q'ya bas")

while True:
    ret, frame = cap.read()
    if not ret:
        print("goruntu alinamadi")
        break

    frame = cv2.GaussianBlur(frame, (5, 5), 0)  # biraz gurultu azaltsin
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # kirmizi iki parcada (0-10 ve 170-180), ikisini birlestiriyoruz
    # not: evdeki olculere gore S ve V alt sinirlari dusuruldu (isik az/bulutlu ortam)
    kirmizi1 = cv2.inRange(hsv, np.array([0, 90, 60]), np.array([6, 255, 255]))
    kirmizi2 = cv2.inRange(hsv, np.array([168, 90, 60]), np.array([180, 255, 255]))
    maske_kirmizi = cv2.bitwise_or(kirmizi1, kirmizi2)

    maske_yesil = cv2.inRange(hsv, np.array([33, 45, 40]), np.array([65, 255, 255]))
    maske_mavi = cv2.inRange(hsv, np.array([100, 70, 45]), np.array([130, 255, 255]))

    # gurultu temizligi - kucuk beyaz noktaciklari sil, sonra delikleri kapat
    maske_kirmizi = cv2.morphologyEx(maske_kirmizi, cv2.MORPH_OPEN, kernel)
    maske_kirmizi = cv2.morphologyEx(maske_kirmizi, cv2.MORPH_CLOSE, kernel)
    maske_yesil = cv2.morphologyEx(maske_yesil, cv2.MORPH_OPEN, kernel)
    maske_yesil = cv2.morphologyEx(maske_yesil, cv2.MORPH_CLOSE, kernel)
    maske_mavi = cv2.morphologyEx(maske_mavi, cv2.MORPH_OPEN, kernel)
    maske_mavi = cv2.morphologyEx(maske_mavi, cv2.MORPH_CLOSE, kernel)

    alan_kirmizi = cv2.countNonZero(maske_kirmizi)
    alan_yesil = cv2.countNonZero(maske_yesil)
    alan_mavi = cv2.countNonZero(maske_mavi)

    renkler = {"RED": alan_kirmizi, "GREEN": alan_yesil, "BLUE": alan_mavi}
    maskeler = {"RED": maske_kirmizi, "GREEN": maske_yesil, "BLUE": maske_mavi}

    baskin = max(renkler, key=renkler.get)
    max_alan = renkler[baskin]

    yazi = "tespit yok"
    renk_bgr = (255, 255, 255)

    if max_alan > esik:
        yazi = baskin
        renk_bgr = {"RED": (0, 0, 255), "GREEN": (0, 255, 0), "BLUE": (255, 0, 0)}[baskin]

        # en buyuk lekenin etrafina kutu ciz, goze daha iyi gorunsun
        konturlar, _ = cv2.findContours(maskeler[baskin], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(konturlar) > 0:
            en_buyuk = max(konturlar, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(en_buyuk)
            cv2.rectangle(frame, (x, y), (x + w, y + h), renk_bgr, 2)

        if baskin != son_renk:
            print(baskin)
            son_renk = baskin
    else:
        son_renk = "tespit yok"

    cv2.putText(frame, "Renk: " + yazi, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, renk_bgr, 2)
    cv2.imshow("HSV Renk Tespiti", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
