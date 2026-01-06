# 🐳 Docker Kullanım Kılavuzu

## Docker Image Oluşturma

### 1. Image Build Etme

```bash
docker build -t mcurvay/aws-examdump-app:latest .
```

### 2. Image'i Test Etme

```bash
docker run -d -p 8080:80 --name aws-exam-app mcurvay/aws-examdump-app:latest
```

Tarayıcıda `http://localhost:8080` adresine gidin.

### 3. Container'ı Durdurma

```bash
docker stop aws-exam-app
docker rm aws-exam-app
```

## Docker Hub'a Push Etme

### 1. Docker Hub'a Login

```bash
docker login
```

### 2. Image'i Tag'leme (Opsiyonel)

```bash
docker tag mcurvay/aws-examdump-app:latest mcurvay/aws-examdump-app:v1.0.0
```

### 3. Push Etme

```bash
# Latest tag
docker push mcurvay/aws-examdump-app:latest

# Version tag (opsiyonel)
docker push mcurvay/aws-examdump-app:v1.0.0
```

## Docker Compose ile Çalıştırma

```bash
docker-compose up -d
```

Tarayıcıda `http://localhost:8080` adresine gidin.

Durdurmak için:
```bash
docker-compose down
```

## Image'i Docker Hub'dan Çekme ve Çalıştırma

```bash
docker pull mcurvay/aws-examdump-app:latest
docker run -d -p 8080:80 --name aws-exam-app mcurvay/aws-examdump-app:latest
```

## Production Kullanımı

### Environment Variables (Gelecekte eklenebilir)

```bash
docker run -d \
  -p 8080:80 \
  -e PORT=80 \
  --name aws-exam-app \
  mcurvay/aws-examdump-app:latest
```

### Volume Mount (Soruları güncellemek için)

```bash
docker run -d \
  -p 8080:80 \
  -v $(pwd)/questions.json:/usr/share/nginx/html/questions.json:ro \
  --name aws-exam-app \
  mcurvay/aws-examdump-app:latest
```

## Image Boyutu Optimizasyonu

Mevcut image nginx:alpine base image kullanıyor, bu da oldukça küçük bir image sağlıyor (~25MB).

## Health Check

Image otomatik health check içerir:
```bash
docker inspect --format='{{.State.Health.Status}}' aws-exam-app
```

## Logs

```bash
docker logs aws-exam-app
docker logs -f aws-exam-app  # Follow mode
```

