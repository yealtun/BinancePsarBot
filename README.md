# Binance API ile İşlem Botu

## Genel Bakış

Bu depo, Parabolik SAR (PSAR) göstergesi sinyallerine dayanarak işlemleri gerçekleştiren basit bir Python işlem botunu içerir. Bot, kripto para vadeli işlemleri için tasarlanmıştır.

## Gereksinimler

Botu kullanmadan önce şunlara sahip olduğunuzdan emin olun:

- Python 3 yüklü
- Gerekli Python paketleri yüklü (`ccxt`, `pandas`, `ta`, `winsound`)
- Binance API anahtarı ve sırrı (Binance hesabınızdan edinin)

## Yapılandırma

1. `config.py` dosyasını açın ve Binance API anahtarınızı (`apiKey`) ve sırrınızı (`secretKey`) doldurun.
2. Bildirim almak istiyorsanız, isteğe bağlı olarak `config.py` dosyasında e-posta ayrıntılarını sağlayın.
   - `mailAddress`: E-posta adresiniz
   - `mailAddress2`: Başka bir e-posta adresi (isteğe bağlı)
   - `password`: E-posta şifreniz (güvenlik için bir uygulama özel şifresi kullanın)

## Kullanım

1. `strategy.py` dosyasını çalıştırın.
2. Sembole (örneğin, BTC, ETH), kaldıraça ve zaman çerçevesine girin.
3. Bot, sürekli olarak PSAR sinyallerini izleyecek ve buna göre işlemler gerçekleştirecektir.

## PSAR Stratejisi

- **Uzun Giriş:** Kapanış fiyatı PSAR'ın üzerine çıktığında alış yapın.
- **Kısa Giriş:** Kapanış fiyatı PSAR'ın altına indiğinde satış yapın.
- **Stop-loss ve Take-profit:** Piyasa koşullarına bağlı olarak dinamik ayarlamalar.

## Bildirimler

- E-posta ayrıntıları sağlandıysa, bot işlem girişleri ve çıkışları için bildirimler gönderecektir.

## Önemli Notlar

- Bu botu kendi sorumluluğunuzda kullanın. Kodu ve işlem stratejilerini anlayın.
- Doğru risk yönetimi yapın ve kaldırağı dikkatlice yapılandırın.

## Sorunlar

Sorunlarla karşılaşırsanız veya önerileriniz varsa lütfen GitHub sorunu oluşturun.

## Feragatname

Bu işlem botu yalnızca eğitim amaçlıdır. Finansal tavsiye değildir. Sorumlu bir şekilde ve kendi riskinizle kullanın.
