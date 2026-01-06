# 🔄 Spaced Repetition Algoritması - Yanlış Soruları Daha Sık Getirme

## Nasıl Çalışıyor?

Uygulama, yanlış yaptığınız soruları daha sık karşınıza çıkarmak için bir **öncelik sistemi** kullanır.

## Öncelik Hesaplama Formülü

Her soru için bir öncelik puanı hesaplanır:

```
Öncelik = (Yanlış × 20) + (Doğru × -3) + Zaman + Bonus
```

### 1. Yanlış Cevap Ağırlığı (En Önemli) ⚠️
- **Her yanlış cevap = +20 puan**
- Örnek:
  - 1 yanlış = 20 puan
  - 2 yanlış = 40 puan
  - 3 yanlış = 60 puan

### 2. Doğru Cevap Ağırlığı ✅
- **Her doğru cevap = -3 puan**
- Çok doğru yapılan sorular daha az öncelik alır
- Örnek:
  - 1 doğru = -3 puan
  - 5 doğru = -15 puan

### 3. Zaman Ağırlığı ⏰
- Uzun süredir görülmeyen sorular +5 puan alır
- Son görülme zamanından bu yana geçen saat başına 1 puan (maksimum 5)

### 4. Özel Bonus 🎯
- **Yanlış yapılan ama hiç doğru yapılmayan sorular = +30 ekstra puan**
- Bu sorular en yüksek önceliğe sahiptir

## Soru Seçimi

1. **Tüm sorular önceliğe göre sıralanır** (yüksek → düşük)
2. **En yüksek öncelikli %30 soru** seçilir (veya en az 15 soru)
3. **%70 ihtimalle** en yüksek öncelikli sorulardan biri seçilir
4. **%30 ihtimalle** diğer yüksek öncelikli sorulardan biri seçilir

## Örnek Senaryo

### Soru A:
- 3 yanlış, 0 doğru
- Öncelik = (3 × 20) + (0 × -3) + 0 + 30 = **90 puan** ⭐⭐⭐

### Soru B:
- 2 yanlış, 1 doğru
- Öncelik = (2 × 20) + (1 × -3) + 0 + 0 = **37 puan** ⭐⭐

### Soru C:
- 0 yanlış, 5 doğru
- Öncelik = (0 × 20) + (5 × -3) + 0 + 0 = **-15 puan** (düşük öncelik)

### Soru D:
- Hiç görülmemiş
- Öncelik = **0 puan** (orta öncelik)

## Sonuç

- ✅ **Yanlış yaptığınız sorular** çok daha sık karşınıza çıkar
- ✅ **Hiç doğru yapmadığınız yanlış sorular** en sık gelir
- ✅ **Çok doğru yaptığınız sorular** daha az gelir
- ✅ **Uzun süredir görmediğiniz sorular** da öncelik alır

## Kod Konumu

Algoritma `app.js` dosyasındaki `getNextQuestion()` fonksiyonunda bulunur (satır 89-145).

## İstatistikler

Her soru için şu bilgiler localStorage'da saklanır:
- `correct`: Doğru cevap sayısı
- `wrong`: Yanlış cevap sayısı
- `lastSeen`: Son görülme zamanı (timestamp)
- `priority`: Hesaplanan öncelik puanı

Bu veriler sayesinde uygulama kapatılıp açılsa bile algoritma çalışmaya devam eder.

