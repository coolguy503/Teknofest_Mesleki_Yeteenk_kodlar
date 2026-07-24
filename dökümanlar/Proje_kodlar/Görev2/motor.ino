#include <AccelStepper.h>

// Sürücü bağlantı ayarları (ZORUNLU: PUL=2, DIR=3)
// 1 = AccelStepper::DRIVER (Step ve Dir pinleri ile kontrol)
AccelStepper stepper(1, 2, 3);

String inputString = "";
bool stringComplete = false;

// Varsayılan hız ve ivme ayarları
const float DEFAULT_MAX_SPEED = 1500.0;
const float DEFAULT_ACCELERATION = 800.0;

void setup() {
    Serial.begin(115200);

    stepper.setMaxSpeed(DEFAULT_MAX_SPEED);
    stepper.setAcceleration(DEFAULT_ACCELERATION);

    // Rastgele dönüşler için analog pinden gürültü oku
    randomSeed(analogRead(0));

    inputString.reserve(50);
}

void loop() {
    // Motoru sürekli çalıştır (hedefe ulaşılana kadar adımları atar)
    stepper.run();

    // Seri porttan tam bir komut (newline ile biten) geldiyse işle
    if (stringComplete) {
        processCommand(inputString);
        inputString = "";
        stringComplete = false;
    }
}

// Kesme mantığıyla seri portu oku
void serialEvent() {
    while (Serial.available()) {
        char inChar = (char)Serial.read();
        if (inChar == '\n') {
            stringComplete = true;
        } else if (inChar != '\r') {
            inputString += inChar;
        }
    }
}

// PC'den gelen protokol komutlarını ayrıştır
void processCommand(String cmd) {
    char commandType = cmd.charAt(0);

    switch (commandType) {
        case 'R': // RASTGELE BAŞLA
        {
            // 1/8 mikro adımda (1600 adım/tur) motor hızı (300 ile 2000 arası rastgele)
            float randSpeed = random(300, 2000);

            // Yönü rastgele belirle ve çok uzak bir hedef vererek sürekli dönmesini sağla
            long randTarget = (random(0, 2) == 0) ? 1000000 : -1000000;

            stepper.setMaxSpeed(randSpeed);
            stepper.moveTo(stepper.currentPosition() + randTarget);
            break;
        }

        case 'S': // DUR (Yavaşlayarak anında durur)
        {
            stepper.stop(); // Hedefi anlık pozisyon + yavaşlama mesafesi olarak ezer
            break;
        }

        case 'G': // BELİRLİ BİR KONUMA GİT
        {
            // Komut formatı: "G<hedef_step>"
            long targetPosition = cmd.substring(1).toInt();

            // Hızı standart değere geri çek
            stepper.setMaxSpeed(DEFAULT_MAX_SPEED);
            stepper.moveTo(targetPosition);
            break;
        }

        case 'P': // POZİSYON VE DURUM İSTEĞİ
        {
            long currentPos = stepper.currentPosition();
            // distanceToGo() sıfırsa motor durmuştur (0), sıfır değilse dönüyordur (1)
            int isRunning = (stepper.distanceToGo() == 0) ? 0 : 1;

            // PC'ye gönderim formatı: POS:<step>,<durum>
            Serial.print("POS:");
            Serial.print(currentPos);
            Serial.print(",");
            Serial.println(isRunning);
            break;
        }
    }
}
