#!/bin/bash
# AWS SAA-C03 Soru Çözüm Uygulaması - Sunucu Başlatma Scripti

echo "🚀 AWS SAA-C03 Soru Çözüm Uygulaması başlatılıyor..."
echo ""
echo "📋 Kontroller yapılıyor..."

# questions.json dosyasının varlığını kontrol et
if [ ! -f "questions.json" ]; then
    echo "❌ questions.json dosyası bulunamadı!"
    echo "📝 Parse scripti çalıştırılıyor..."
    python3 parse_questions.py
    if [ ! -f "questions.json" ]; then
        echo "❌ Hata: questions.json oluşturulamadı!"
        exit 1
    fi
fi

echo "✅ questions.json dosyası mevcut"
echo ""
echo "🌐 Web sunucusu başlatılıyor..."
echo "📍 Uygulama şu adreste çalışacak: http://localhost:8000"
echo ""
echo "💡 Tarayıcınızda http://localhost:8000 adresine gidin"
echo "🛑 Durdurmak için Ctrl+C tuşlarına basın"
echo ""

# Port kontrolü ve sunucu başlatma
PORT=8000

# Port kullanılıyorsa farklı bir port dene
if lsof -ti:$PORT > /dev/null 2>&1; then
    echo "⚠️  Port $PORT kullanımda, alternatif port deneniyor..."
    PORT=8080
    if lsof -ti:$PORT > /dev/null 2>&1; then
        PORT=3000
    fi
    echo "📍 Uygulama şu adreste çalışacak: http://localhost:$PORT"
fi

# Python 3 ile HTTP sunucusu başlat
python3 -m http.server $PORT

