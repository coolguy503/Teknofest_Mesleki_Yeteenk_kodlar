from ultralytics import YOLO

def main():
    # yolo26l modelini yükle
    model = YOLO("yolo26l.pt")

    # Modeli Intel Arc (XPU) kullanarak eğit
    results = model.train(
        data="dataset.yaml",
        epochs=100,          # İhtiyacınıza göre artırabilirsiniz
        imgsz=640,          # Görsel boyutu
        batch=-1,           # Batch boyutu (VRAM durumunuza göre 8 veya 4 yapabilirsiniz)
        #device='xpu',       # Intel Arc ekran kartını kullanır
        workers=4
    )

    print("Eğitim başarıyla tamamlandı!")

if __name__ == '__main__':
    main()