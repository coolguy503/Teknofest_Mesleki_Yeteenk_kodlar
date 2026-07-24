import tkinter as tk
from tkinter import messagebox
import serial
import json
import os

# --- AYARLAR ---
# İşletim sistemine göre COM portunu ayarla (Örn: Windows için 'COM3', Linux için '/dev/ttyUSB0')
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200
JSON_FILE = 'konumlar.json'

class MotorKontrolArayuzu:
    def __init__(self, root):
        self.root = root
        self.root.title("Akıllı Fabrika - Motor Kontrol")
        self.root.geometry("400x350")
        self.root.configure(padx=20, pady=20)

        self.current_position = 0
        self.is_running = False
        self.data = {"baslangic": 0, "kayitli": 0}

        # Seri port bağlantısını başlat
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
        except Exception as e:
            messagebox.showerror("Bağlantı Hatası", f"Seri port açılamadı ({SERIAL_PORT}).\nHata: {e}")
            self.ser = None

        self.json_yukle()
        self.arayuz_olustur()
        self.durum_sorgula()

    def json_yukle(self):
        """Uygulama açıldığında JSON dosyasını okur veya yoksa oluşturur."""
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, 'r') as f:
                try:
                    loaded_data = json.load(f)
                    self.data.update(loaded_data)
                except json.JSONDecodeError:
                    pass
        else:
            self.json_kaydet()

    def json_kaydet(self):
        """Mevcut konum verilerini JSON'a kaydeder."""
        with open(JSON_FILE, 'w') as f:
            json.dump(self.data, f, indent=2)

    def arayuz_olustur(self):
        # Durum Göstergeleri
        self.lbl_pos = tk.Label(self.root, text="Konum: 0", font=("Helvetica", 14, "bold"))
        self.lbl_pos.pack(pady=5)

        self.lbl_status = tk.Label(self.root, text="Durum: Bekliyor", font=("Helvetica", 12), fg="red")
        self.lbl_status.pack(pady=5)

        # Butonlar
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        tk.Button(btn_frame, text="BAŞLANGICI KAYDET", command=self.baslangici_kaydet, bg="#d9edf7").pack(fill=tk.X, pady=3)
        tk.Button(btn_frame, text="BAŞLA", command=self.basla, bg="#dff0d8").pack(fill=tk.X, pady=3)
        tk.Button(btn_frame, text="DUR", command=self.dur, bg="#f2dede").pack(fill=tk.X, pady=3)
        tk.Button(btn_frame, text="KONUMU KAYDET", command=self.konumu_kaydet, bg="#d9edf7").pack(fill=tk.X, pady=3)
        tk.Button(btn_frame, text="BAŞLANGICA GİT", command=self.baslangica_git, bg="#fcf8e3").pack(fill=tk.X, pady=3)
        tk.Button(btn_frame, text="KAYITLI KONUMA GİT", command=self.kayitli_konuma_git, bg="#fcf8e3").pack(fill=tk.X, pady=3)

    def seri_yaz(self, komut):
        if self.ser and self.ser.is_open:
            self.ser.write((komut + '\n').encode('utf-8'))

    def durum_sorgula(self):
        """200ms'de bir Arduino'dan anlık durum ve konum ister."""
        self.seri_yaz('P')

        if self.ser and self.ser.is_open:
            while self.ser.in_waiting > 0:
                try:
                    line = self.ser.readline().decode('utf-8').strip()
                    if line.startswith("POS:"):
                        # Format: POS:<step>,<durum>
                        parts = line[4:].split(',')
                        if len(parts) == 2:
                            self.current_position = int(parts[0])
                            self.is_running = (parts[1] == '1')

                            # Arayüzü güncelle
                            self.lbl_pos.config(text=f"Konum: {self.current_position}")
                            if self.is_running:
                                self.lbl_status.config(text="Durum: Dönüyor", fg="green")
                            else:
                                self.lbl_status.config(text="Durum: Duruyor", fg="red")
                except Exception:
                    pass

        # Döngüyü native Tkinter thread'inde devam ettir
        self.root.after(200, self.durum_sorgula)

    # --- BUTON DAVRANIŞLARI ---
    def baslangici_kaydet(self):
        self.data["baslangic"] = self.current_position
        self.json_kaydet()

    def basla(self):
        self.seri_yaz('R')

    def dur(self):
        self.seri_yaz('S')

    def konumu_kaydet(self):
        self.data["kayitli"] = self.current_position
        self.json_kaydet()

    def baslangica_git(self):
        hedef = self.data["baslangic"]
        self.seri_yaz(f'G{hedef}')

    def kayitli_konuma_git(self):
        hedef = self.data["kayitli"]
        self.seri_yaz(f'G{hedef}')

if __name__ == "__main__":
    root = tk.Tk()
    app = MotorKontrolArayuzu(root)
    root.mainloop()
