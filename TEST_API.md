# Test Python Engine API

## ✅ Server Sudah Running!

Python engine sudah berjalan di: **http://localhost:8001**

## 🧪 Test API

### 1. Test Health Check

Buka browser atau gunakan curl:

**Browser:**
```
http://localhost:8001
http://localhost:8001/health
```

**Curl (di CMD baru):**
```cmd
curl http://localhost:8001
curl http://localhost:8001/health
```

### 2. Test API Documentation

FastAPI otomatis menyediakan dokumentasi interaktif:

**Swagger UI:**
```
http://localhost:8001/docs
```

**ReDoc:**
```
http://localhost:8001/redoc
```

### 3. Test Diagnosis Endpoint

Endpoint diagnosis memerlukan data dari Laravel, jadi perlu Laravel backend running dulu.

## 📡 Endpoint yang Tersedia

### Public Endpoints

- `GET /` - Root endpoint (info API)
- `GET /health` - Health check
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation

### API Endpoints

- `POST /api/diagnose` - Proses diagnosis dengan Certainty Factor
- `GET /api/diseases/{plant_id}` - Daftar penyakit per tanaman

## 🔗 Integrasi dengan Laravel

Pastikan Laravel backend sudah dikonfigurasi dengan:

```env
PYTHON_API_URL=http://localhost:8001
```

Laravel akan mengirim request ke Python engine untuk proses diagnosis.

## ✅ Verifikasi

1. Buka browser: http://localhost:8001/docs
2. Anda akan melihat dokumentasi API interaktif
3. Test endpoint `/health` untuk memastikan server responsif

## 🎯 Next Steps

1. ✅ Python engine running (DONE)
2. ⏳ Setup Laravel backend
3. ⏳ Test integrasi Laravel ↔ Python
4. ⏳ Setup frontend Vue.js

## 🐛 Troubleshooting

### Port 8001 sudah digunakan?
Ganti port di command:
```cmd
uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
```

### Server tidak responsif?
- Cek apakah ada error di terminal
- Pastikan tidak ada firewall yang block port 8001
- Test dengan `curl http://localhost:8001/health`

