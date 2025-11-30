# Panduan Menjalankan System Pakar Engine

## ✅ Verifikasi Kesesuaian dengan Proposal

Sistem engine Python **SUDAH SESUAI** dengan proposal Anda:

### 1. ✅ Metode Certainty Factor (CF)
- **Formula CF Gejala**: `CF(H,E) = CF(E) * CF(Rule)` ✅
  - CF(E) = user_cf (0.0 - 1.0)
  - CF(Rule) = rule_cf dari pakar (0.0 - 1.0)
  
- **Formula CF Combine**: `CF_combine = CF_old + (CF_new * (1 - CF_old))` ✅
  - Sesuai dengan contoh perhitungan di proposal:
    - CFGejala1 = 0.6 * 0.6 = 0.36
    - CFGejala2 = 0.8 * 0.8 = 0.64
    - CFcombine1 = 0.36 + 0.64 * (1 - 0.36) = 0.7696
    - CFcombine2 = 0.7696 + 0.48 * (1 - 0.7696) = 0.880192
    - CFcombine3 = 0.880192 + 0.36 * (1 - 0.880192) = 0.92332288

- **Persentase Keyakinan**: `CF_penyakit * 100` ✅
  - Contoh: 0.92332288 * 100 = 92.332288%

### 2. ✅ Forward Chaining
- Mulai dari fakta (gejala yang dipilih user) ✅
- Match dengan rules (aturan penyakit dengan gejala) ✅
- Infer kesimpulan (penyakit yang mungkin) ✅
- Hitung CF untuk setiap kesimpulan ✅

### 3. ✅ Experta Library
- Menggunakan `KnowledgeEngine` untuk inference ✅
- Menggunakan `Fact` untuk fakta (UserSymptom, DiseaseRule) ✅
- Menggunakan `Rule` dengan pattern matching ✅
- Forward Chaining otomatis oleh Experta ✅

### 4. ✅ Fitur F#13 - Sistem Pakar Diagnosis
- Menerima input gejala dan CF user ✅
- Mengakses rule base dari database ✅
- Menghitung CF untuk setiap penyakit ✅
- Menghasilkan kesimpulan diagnosis ✅
- Menyimpan hasil ke database ✅

## 🚀 Cara Menjalankan Sistem

### Opsi 1: Menggunakan start_engine.bat (RECOMMENDED)

1. **Buka Command Prompt atau File Explorer**
2. **Navigasi ke folder `s_pakar_engine`**
   ```bash
   cd C:\laragon\www\SystemPakar\s_pakar_engine
   ```
3. **Double-click file `start_engine.bat`** atau jalankan dari CMD:
   ```bash
   start_engine.bat
   ```

4. **Sistem akan:**
   - ✅ Mengecek Python (harus 3.11 atau 3.12)
   - ✅ Mengaktifkan virtual environment (atau membuat baru jika belum ada)
   - ✅ Menginstall dependencies jika diperlukan
   - ✅ Menjalankan FastAPI server di port 8001

5. **Server akan berjalan di:**
   - URL: `http://localhost:8001`
   - Health Check: `http://localhost:8001/health`
   - API Docs: `http://localhost:8001/docs`

### Opsi 2: Manual (Tanpa Batch File)

1. **Aktifkan virtual environment:**
   ```bash
   cd C:\laragon\www\SystemPakar\s_pakar_engine
   venv\Scripts\activate
   ```

2. **Jalankan server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
   ```

## 📁 File-File Penting

### File Utama:
- **`start_engine.bat`** - Script untuk menjalankan server (FILE YANG ANDA GUNAKAN)
- **`app/main.py`** - Entry point FastAPI application
- **`app/services/expert_system.py`** - Logika sistem pakar dengan Experta
- **`app/api/client.py`** - Client untuk komunikasi dengan Laravel API
- **`requirements.txt`** - Dependencies Python

### Struktur Folder:
```
s_pakar_engine/
├── start_engine.bat          ← FILE INI YANG ANDA JALANKAN
├── app/
│   ├── main.py               ← FastAPI application
│   ├── services/
│   │   └── expert_system.py  ← Logika CF & Forward Chaining
│   └── api/
│       └── client.py          ← Laravel API client
├── requirements.txt
└── venv/                      ← Virtual environment
```

## 🔄 Alur Kerja Sistem

### 1. **Startup (start_engine.bat)**
```
start_engine.bat
  ↓
Cek Python → Aktifkan venv → Install deps → Start FastAPI
  ↓
Server running di http://localhost:8001
```

### 2. **Proses Diagnosis (F#13)**
```
Laravel Backend
  ↓
POST /api/diagnose
  ↓
FastAPI (app/main.py)
  ↓
ExpertSystemService.calculate_certainty_factor()
  ↓
ExpertSystemEngine (Experta)
  ├── Declare DiseaseRule facts (dari database)
  ├── Declare UserSymptom facts (dari user input)
  ├── Run Forward Chaining
  │   ├── Match gejala dengan rules
  │   ├── Hitung CF gejala: CF_user * CF_pakar
  │   └── Combine CF: CF_old + (CF_new * (1 - CF_old))
  ↓
Return hasil diagnosis dengan CF tertinggi
```

### 3. **Contoh Request dari Laravel:**
```json
POST http://localhost:8001/api/diagnose
{
  "diagnosis_id": 1,
  "plant_id": 1,
  "symptoms": [
    {"symptom_id": 1, "user_cf": 0.6},
    {"symptom_id": 2, "user_cf": 0.8},
    {"symptom_id": 3, "user_cf": 0.6}
  ],
  "diseases_data": [
    {
      "id": 1,
      "name": "Kutu Daun",
      "solution": "...",
      "prevention": "...",
      "symptoms": [
        {"symptom_id": 1, "certainty_factor": 0.6},
        {"symptom_id": 2, "certainty_factor": 0.8}
      ]
    }
  ]
}
```

### 4. **Response:**
```json
{
  "success": true,
  "data": {
    "diagnosis_id": 1,
    "disease_id": 1,
    "disease_name": "Kutu Daun",
    "certainty_value": 0.7696,
    "recommendation": "Berdasarkan gejala...",
    "all_possibilities": [...]
  }
}
```

## ✅ Checklist Sebelum Menjalankan

- [ ] Python 3.11 atau 3.12 sudah terinstall
- [ ] File `start_engine.bat` ada di folder `s_pakar_engine`
- [ ] File `requirements.txt` ada
- [ ] Virtual environment sudah dibuat (atau akan dibuat otomatis)
- [ ] Port 8001 tidak digunakan aplikasi lain
- [ ] Laravel backend sudah running (untuk integrasi)

## 🐛 Troubleshooting

### Error: Python not found
- Install Python 3.11 atau 3.12
- Pastikan Python ada di PATH

### Error: ModuleNotFoundError: No module named 'experta'
- Jalankan: `pip install -r requirements.txt`
- Atau biarkan `start_engine.bat` install otomatis

### Error: Port 8001 already in use
- Tutup aplikasi yang menggunakan port 8001
- Atau ubah port di `start_engine.bat` (baris 41)

### Server tidak bisa connect ke Laravel
- Pastikan Laravel backend sudah running
- Cek konfigurasi di `.env` atau `config/settings.py`

## 📊 Monitoring

Setelah server running, Anda bisa:
- **Health Check**: `http://localhost:8001/health`
- **API Documentation**: `http://localhost:8001/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8001/redoc` (ReDoc)

## 🎯 Kesimpulan

✅ **Sistem engine Python SUDAH SESUAI dengan proposal Anda**
✅ **Cara menjalankan: Double-click `start_engine.bat`**
✅ **Server akan running di `http://localhost:8001`**
✅ **Semua formula CF sesuai dengan dokumen proposal**

Sistem siap digunakan untuk diagnosis penyakit tanaman hias dengan metode Certainty Factor dan Forward Chaining! 🌱

