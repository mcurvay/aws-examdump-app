# 🚀 Uygulamayı Çalıştırma Kılavuzu

## Hızlı Başlangıç

### Yöntem 1: Otomatik Script (Önerilen) ⭐

Terminal'de şu komutu çalıştırın:

```bash
./start_server.sh
```

Bu script otomatik olarak:
- ✅ `questions.json` dosyasının varlığını kontrol eder
- ✅ Yoksa parse scriptini çalıştırır
- ✅ Web sunucusunu başlatır

### Yöntem 2: Manuel Komut

Terminal'de proje klasörüne gidin ve şu komutu çalıştırın:

```bash
python3 -m http.server 8000
```

### Yöntem 3: VS Code Live Server

1. VS Code'da projeyi açın
2. "Live Server" eklentisini yükleyin (yoksa)
3. `index.html` dosyasına sağ tıklayın
4. "Open with Live Server" seçeneğini tıklayın

---

## 📍 Tarayıcıda Açma

Sunucu başladıktan sonra, tarayıcınızda şu adrese gidin:

```
http://localhost:8000
```

---

## ⚠️ Önemli Notlar

1. **Web Sunucusu Gereklidir**: JSON dosyalarını yüklemek için bir web sunucusu kullanmanız gerekir. Dosyayı doğrudan açmak (file://) çalışmaz.

2. **Port 8000 Kullanılıyorsa**: Eğer 8000 portu kullanılıyorsa, farklı bir port kullanabilirsiniz:
   ```bash
   python3 -m http.server 8080
   ```
   Sonra tarayıcıda `http://localhost:8080` adresine gidin.

3. **Sorular Yüklenmiyorsa**: 
   - `questions.json` dosyasının mevcut olduğundan emin olun
   - Tarayıcı konsolunu açın (F12) ve hataları kontrol edin
   - Sunucunun çalıştığından emin olun

---

## 🛑 Sunucuyu Durdurma

Terminal'de `Ctrl+C` tuşlarına basın.

---

## 🔧 Sorun Giderme

### "questions.json bulunamadı" hatası

Parse scriptini çalıştırın:
```bash
python3 parse_questions.py
```

### Port hatası

Farklı bir port kullanın:
```bash
python3 -m http.server 8080
```

### Tarayıcıda "CORS" hatası

Mutlaka bir web sunucusu kullanmanız gerekiyor. Dosyayı doğrudan açmayın.

---

## 📱 Kullanım

1. ✅ Soruyu okuyun
2. ✅ Bir şık seçin
3. ✅ "Cevabı Kontrol Et" butonuna tıklayın
4. ✅ Sonucu görün (Doğru/Yanlış)
5. ✅ Çözümü inceleyin
6. ✅ "Sonraki Soru" ile devam edin

İyi çalışmalar! 🎯

