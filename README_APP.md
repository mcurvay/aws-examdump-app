# AWS SAA-C03 Soru Çözüm Uygulaması

Bu uygulama, AWS SAA-C03 sınavına hazırlık için interaktif bir soru çözüm platformudur.

## Özellikler

- ✅ **465+ Soru**: AWS SAA-C03 sınavına yönelik çoktan seçmeli sorular
- 🎯 **Doğru/Yanlış Takibi**: Her oturumda doğru ve yanlış cevaplarınızı takip eder
- 📊 **İstatistikler**: Toplam doğru, yanlış ve çözülen soru sayısını gösterir
- 🔄 **Spaced Repetition**: Yanlış yaptığınız soruları daha sık karşınıza çıkarır
- 🎲 **Karışık Sorular**: Sorular rastgele sırayla gösterilir
- 💡 **Detaylı Çözümler**: Her soru için açıklamalı çözümler
- 💾 **Oturum Hafızası**: Tarayıcınızın localStorage'ında ilerlemeniz kaydedilir

## Kurulum

1. Tüm dosyaların aynı klasörde olduğundan emin olun:
   - `index.html`
   - `style.css`
   - `app.js`
   - `questions.json`

2. Eğer `questions.json` dosyası yoksa, önce parse scriptini çalıştırın:
   ```bash
   python3 parse_questions.py
   ```

## Kullanım

### Yerel Sunucu ile Çalıştırma

JSON dosyalarını yüklemek için bir web sunucusu gereklidir. Aşağıdaki yöntemlerden birini kullanabilirsiniz:

#### Python ile:
```bash
python3 -m http.server 8000
```
Sonra tarayıcınızda `http://localhost:8000` adresine gidin.

#### Node.js ile:
```bash
npx http-server -p 8000
```

#### VS Code Live Server:
VS Code kullanıyorsanız, "Live Server" eklentisini yükleyip `index.html` dosyasına sağ tıklayıp "Open with Live Server" seçeneğini kullanabilirsiniz.

### Kullanım Adımları

1. Uygulamayı açın
2. Soruyu okuyun
3. Doğru olduğunu düşündüğünüz şıkkı seçin
4. "Cevabı Kontrol Et" butonuna tıklayın
5. Sonucu görün (Doğru/Yanlış)
6. Çözümü inceleyin
7. "Sonraki Soru" butonuna tıklayarak devam edin

## Spaced Repetition Algoritması

Uygulama, yanlış yaptığınız soruları daha sık karşınıza çıkarmak için bir öncelik sistemi kullanır:

- **Yanlış cevaplar**: Her yanlış cevap, sorunun önceliğini artırır
- **Doğru cevaplar**: Her doğru cevap, sorunun önceliğini azaltır
- **Zaman faktörü**: Uzun süredir görmediğiniz sorular daha yüksek öncelik alır

Bu sayede zorlandığınız konuları daha sık tekrar edersiniz.

## İstatistikler

Uygulama, tarayıcınızın localStorage'ında şu bilgileri saklar:

- **Session Stats**: Mevcut oturumdaki doğru/yanlış/toplam sayıları
- **Question Stats**: Her soru için doğru/yanlış sayıları ve son görülme zamanı

Bu veriler tarayıcınızı kapatıp açsanız bile korunur.

## Sorun Giderme

### Sorular yüklenmiyor
- `questions.json` dosyasının mevcut olduğundan emin olun
- Bir web sunucusu kullanarak çalıştırdığınızdan emin olun (doğrudan dosyayı açmak çalışmaz)

### Parse hatası
- `parse_questions.py` scriptini tekrar çalıştırın
- `AWS SAA-03 Solution.txt` dosyasının mevcut olduğundan emin olun

## Geliştirme

### Yeni Soru Ekleme

1. `AWS SAA-03 Solution.txt` dosyasına yeni soruyu ekleyin
2. Format:
   ```
   [Soru Numarası] Soru metni...
   
   A. Şık A
   B. Şık B
   C. Şık C
   D. Şık D
   
   ans- Doğru cevap açıklaması
   
   Çözüm açıklaması...
   -------------------------------------------------------
   ```
3. `parse_questions.py` scriptini çalıştırın

## Lisans

Bu proje eğitim amaçlıdır.

