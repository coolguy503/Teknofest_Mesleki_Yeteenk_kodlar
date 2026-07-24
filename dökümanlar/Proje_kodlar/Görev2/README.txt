AKILLI FABRİKA - GÖREV 2: STEP MOTOR VE ARAYÜZ
==============================================

Donanım Bağlantıları (Zorunlu):
1. DM556 Sürücü PUL (Pulse/Step) pini -> Arduino D2'ye bağlanmalıdır.
2. DM556 Sürücü DIR (Direction) pini -> Arduino D3'e bağlanmalıdır.
3. DM556 üzerinden switch ayarları ile 1/8 mikro adım (1600 step/rev) seçilmelidir.
4. Arduino PC'ye USB ile bağlı olmalıdır.

Kurulum ve Çalıştırma:
1. "motor.ino" dosyasını Arduino IDE ile açın.
2. Sketch -> Include Library -> Manage Libraries üzerinden "AccelStepper" kütüphanesini indirin (Mike McCauley).
3. Kodu Arduino Uno'ya yükleyin.
4. PC tarafında Python kütüphanelerini kurun:
   > pip install pyserial
5. "arayuz.py" içindeki "SERIAL_PORT" değişkenini kendi bilgisayarınızın atadığı porta göre (Örn: 'COM3') güncelleyin.
6. Python scriptini çalıştırın:
   > python arayuz.py

Bilinmesi Gerekenler / Notlar:
------------------------------
- Arayüzdeki konum/durum göstergesi Arduino'yu 200ms aralıklarla sorgular;
  bu nedenle ekrandaki değer motorun o anki gerçek durumuna göre ~200ms
  gecikmeli olabilir. DUR'a bastıktan sonra KONUMU KAYDET'e basmadan önce
  motorun tamamen durduğundan (ekranda "Duruyor" yazdığından) emin olun,
  hemen art arda tıklamayın.
- DUR komutu motoru ani değil, ivmeye göre yavaşlayarak durdurur; bu yüzden
  DUR'a basıldığı andaki değil, motor tam durduktan sonraki step konumu
  kaydedilir.
- SERIAL_PORT değeri her bilgisayarda farklı olabilir (Windows: COM3, COM4...;
  Linux: /dev/ttyUSB0, /dev/ttyACM0...). Programı çalıştırmadan önce Aygıt
  Yöneticisi / `ls /dev/tty*` ile doğru portu kontrol edin, aksi halde program
  seri port hatası verip açılmaz.



Test Senaryosu Sıralaması:
Arayüz açıldığında Arduino ile otomatik bağlantı kuracak ve anlık konumu "0" olarak gösterecektir.
Test prosedürünü çalıştırmak için sırasıyla tıklayın:
1. BAŞLANGICI KAYDET (Şu anki konumu 'baslangic' olarak JSON'a yazar).
2. BAŞLA (Motor rastgele hız ve yönde sürekli dönmeye başlar. Arayüzde "Dönüyor" yazar, step sayacı artar/azalır).
3. DUR (Motor yavaşlayarak durur. Arayüzde "Duruyor" yazar).
4. KONUMU KAYDET (Durduğu bu rastgele yeni noktayı 'kayitli' olarak JSON'a yazar).
5. BAŞLANGICA GİT (Motor ilk sıfır noktasına, yani 'baslangic'a doğru geri döner).
6. KAYITLI KONUMA GİT (Motor az önce durdurduğunuz 'kayitli' noktasına tekrar gider).

Program kapatılıp açıldığında "konumlar.json" dosyası yerel olarak okunacak ve eski konum verileri kaybolmayacaktır.
