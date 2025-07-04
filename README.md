Genel Bakış
ARCRover, Raspberry Pi tabanlı, otonom ve manuel kontrol yeteneklerine sahip bir keşif aracıdır. Üzerinde bulunan sensörler, motorlar, kamera ve GPS modülü sayesinde karmaşık görevleri yerine getirebilir. Proje, modüler bir yapıda geliştirilmiş olup her bir donanım bileşeni için özel kontrolcü sınıfları içerir. Bu sayede kodun bakımı ve geliştirilmesi kolaylaşır.

🤖 Temel Yetenekler
1. Hareket ve Sürüş
4 Tekerlekten Çekiş: Araç, gücünü 4 adet DC motordan alır ve bu sayede zorlu arazi koşullarında bile yüksek manevra kabiliyetine sahiptir.

Gamepad ile Manuel Kontrol: Tüm sürüş fonksiyonları, bir gamepad üzerinden anlık olarak kontrol edilebilir. İleri/geri hareket ve dönüşler analog çubuklarla yönetilir.

Yön Sabitleme (Stabilizasyon): Araç, IMU sensöründen (MPU9250) aldığı verileri kullanarak düz bir çizgide ilerlerken hedeflenen yönde kalmasını sağlayan bir stabilizasyon moduna sahiptir. Bu özellik, özellikle hassas görevlerde sürüşü kolaylaştırır.

2. Robotik Kol ve Servo Kontrolü
Çok Eklemli Kol: Rover, omuz, dirsek ve el (kıskaç) olmak üzere üç ana ekleme sahip bir robotik kol ile donatılmıştır. Bu kol, nesneleri tutma, taşıma ve bırakma gibi işlemler için kullanılır.

Gamepad ile Kol Kontrolü: Kolun tüm eklemleri ve tabanının dönüşü, gamepad üzerinden hassas bir şekilde kontrol edilebilir.

180 Derece Dönebilen Taban: Kol, bir servo motor üzerinde yer alır ve bu sayede 180 derecelik bir açıyla yatay düzlemde dönebilir.

3. Navigasyon ve Görev Planlama
Araç, üç farklı kontrol modunda çalışabilir: Sürüş, Kol ve Navigasyon.

GPS Destekli Otonom Sürüş: config.py dosyasında tanımlanan görev planı (MISSION_PLAN) sayesinde, araç belirlenmiş GPS koordinatlarına otonom olarak gidebilir. Araç, mevcut konumu ile hedef nokta arasındaki mesafeyi ve yönü hesaplayarak hedefe ulaşır.

Görsel Hedef Tespiti ve Yaklaşma (Visual Homing): Araç, bir hedefe yeterince yaklaştığında (NAV_ARRIVAL_DISTANCE), ArUco etiketlerini aramaya başlar. Hedef etiketi (ID ve renk bilgisiyle) bulduğunda, kamera görüntüsünü kullanarak hedefe hassas bir şekilde yaklaşır ve hizalanır.

ArUco Etiket ve Renk Tanıma: Rover, kamera aracılığıyla ArUco etiketlerini tespit eder ve bu etiketlerin etrafındaki renkli çerçeveleri (kırmızı, yeşil, mavi) tanıyabilir. Bu, görev planındaki hedeflerin doğru bir şekilde doğrulanmasını sağlar.

4. Sensörler ve Veri Toplama
Çevresel Sensörler: Araç üzerinde hava sıcaklığı ve nemi ölçen bir DHT11 sensörü ile toprağın nem seviyesini ölçen bir sensör bulunur.

IMU (Ataletsel Ölçüm Birimi): MPU9250 sensörü, aracın ivme, jiroskopik ve manyetik alan verilerini okuyarak yön ve konum takibine yardımcı olur.

Veri Kaydı (Logging): Gamepad üzerindeki özel bir tuşa basıldığında, araç tüm sensörlerden (GPS dahil) topladığı verileri zaman damgasıyla birlikte SD kart üzerindeki bir .csv dosyasına kaydeder.

5. Görüntüleme Sistemi
Yüksek Çözünürlüklü Kamera: Picamera2 kütüphanesi ile kontrol edilen kamera, yüksek kaliteli fotoğraflar çekebilir.

Fotoğraf Çekme: Gamepad üzerindeki atanmış bir tuş ile istenildiği an fotoğraf çekilip SD karta kaydedilebilir.

💻 Geliştiriciler İçin Teknik Detaylar
Proje Mimarisi
Proje, her biri belirli bir sorumluluğa sahip Python modüllerinden oluşur:

main.py: Ana döngünün bulunduğu, tüm modüllerin başlatıldığı ve kontrol modları arasındaki geçişin yönetildiği merkezi betik.

config.py: Tüm sabitlerin, GPIO pin numaralarının, kontrol parametrelerinin (kazanç değerleri, hızlar) ve görev planının tanımlandığı yapılandırma dosyası.

motor_controller.py: Sürüş motorlarını kontrol eden sınıf. Düz gidiş için stabilizasyon mantığını içerir.

arm_controller.py: Robotik kolun eklemlerini kontrol eden DC motorları yönetir.

servo_controller.py: Kolun tabanındaki servo motoru kontrol eder.

gamepad_controller.py: Gamepad girdilerini okur ve bunları aracın anlayacağı komutlara çevirir. Düğmelere "yeni basılma" durumunu takip eder.

camera_controller.py: Fotoğraf çekme işlevini yönetir.

vision_controller.py: Kamera görüntüsünü işleyerek ArUco etiketlerini ve renklerini tespit eder.

sensor_controller.py: DHT11, toprak nem sensörü ve IMU gibi sensörleri yönetir.

gps_reader.py: GPS modülünden gelen NMEA verilerini okur ve enlem/boylam bilgisi sağlar.

data_logger.py: Sensör verilerini CSV formatında dosyaya kaydeder.

navigation.py: GPS ve yön verilerini kullanarak hedefe yönelme komutları üretir.

Kurulum ve Bağımlılıklar
Projeyi çalıştırmak için aşağıdaki Python kütüphanelerinin yüklü olması gerekmektedir:
gpiozero, picamera2, pynmea2, inputs, adafruit-circuitpython-dht, adafruit-circuitpython-mcp3xxx, mpu9250-jmdev, opencv-python, numpy.

Yapılandırma (config.py)
Projenin en kritik dosyalarından biridir. Yeni bir donanım eklendiğinde veya mevcut donanımın pinleri değiştirildiğinde bu dosyanın güncellenmesi gerekir. Ayrıca, otonom görevler için MISSION_PLAN listesi bu dosyadan düzenlenir.

🛠️ Saha Kullanım Kılavuzu
1. Başlatma
Tüm donanım bağlantılarının (motorlar, sensörler, kamera vb.) doğru yapıldığından emin olun.

Raspberry Pi'ye güç verin ve terminalden main.py betiğini çalıştırın: python3 main.py

Sistem, "ARCRover başlatılıyor..." ve "Kurulum tamamlandı. ARCRover hazır." mesajlarını gösterecektir.

2. Gamepad Kontrolleri
Sol Analog Çubuk (Yukarı/Aşağı): İleri ve geri hareket.

Sağ Analog Çubuk (Sağ/Sol): Sağa ve sola dönüş.

'Y' Düğmesi: Sürüş Modu ile Kol Kontrol Modu arasında geçiş yapar.

'B' Düğmesi: Navigasyon Modunu başlatır veya iptal eder.

'A' Düğmesi: Mevcut tüm sensör verilerini SD karttaki log dosyasına kaydeder.

'X' Düğmesi: Fotoğraf çeker.

3. Kol Kontrolü (Kol Modu Aktifken)
D-Pad (Yukarı/Aşağı): Omuz eklemini hareket ettirir.

L1/L2 Düğmeleri: Dirsek eklemini hareket ettirir.

R1/R2 Düğmeleri: El (kıskaç) eklemini hareket ettirir.

Sağ Analog Çubuk (Sağ/Sol): Kolun tabanını döndürür.

4. Otonom Görev Yürütme
Görevi başlatmadan önce aracın GPS sinyali aldığından emin olun. main.py ekranında "[HATA] Navigasyon başlatılamadı: GPS sinyali yok." uyarısı alırsanız, aracın açık bir alanda olmasını sağlayın.

Gamepad üzerindeki 'B' düğmesine basarak navigasyonu başlatın.

Araç, config.py dosyasındaki MISSION_PLAN listesindeki ilk hedefe doğru hareket edecektir.

Hedef GPS konumuna ulaştığında, durup ilgili ArUco etiketini aramaya başlar.

Etiketi bulup yanına başarıyla yanaştıktan sonra bir sonraki hedefe geçer.

Tüm hedefler tamamlandığında "Tüm waypointler tamamlandı! Görev başarılı." mesajı görüntülenir ve araç tekrar manuel sürüş moduna döner.
