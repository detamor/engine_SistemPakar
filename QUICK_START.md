# Quick Start - Setup Python Engine

## 🚀 Cara Cepat (Setelah Python Terinstall)

### Opsi 1: Gunakan `py` Launcher (Recommended untuk Windows)

```cmd
cd C:\laragon\www\SystemPakar\s_pakar_engine
py --version
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

Atau gunakan script:
```cmd
start_engine_py.bat
```

### Opsi 2: Gunakan `python` (Jika sudah di PATH)

```cmd
cd C:\laragon\www\SystemPakar\s_pakar_engine
python --version
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

Atau gunakan script:
```cmd
start_engine.bat
```

## 🔍 Cek Python Terlebih Dahulu

Sebelum setup, test dulu apakah Python bisa digunakan:

### Test 1: Cek `py` launcher
```cmd
py --version
```
Jika berhasil → gunakan `py` untuk semua command

### Test 2: Cek `python` command
```cmd
python --version
```
Jika berhasil → gunakan `python` untuk semua command

### Jika keduanya tidak berhasil:
1. Baca: `ADD_PYTHON_TO_PATH.md`
2. Atau reinstall Python dengan centang "Add Python to PATH"

## 📋 Langkah Lengkap

### 1. Buka CMD di folder s_pakar_engine
```cmd
cd C:\laragon\www\SystemPakar\s_pakar_engine
```

### 2. Test Python
```cmd
py --version
```
atau
```cmd
python --version
```

### 3. Buat Virtual Environment
```cmd
py -m venv venv
```
atau
```cmd
python -m venv venv
```

### 4. Aktifkan Virtual Environment
```cmd
venv\Scripts\activate
```

Setelah aktif, prompt akan menampilkan `(venv)` di depan.

### 5. Install Dependencies
```cmd
pip install -r requirements.txt
```

### 6. Jalankan Engine
```cmd
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## ✅ Verifikasi

Setelah engine running, buka browser:
- API: http://localhost:8001
- Docs: http://localhost:8001/docs

## 🎯 One-Line Setup (Jika Python sudah di PATH)

```cmd
cd C:\laragon\www\SystemPakar\s_pakar_engine && py -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## 🐛 Masalah?

- Python tidak dikenali → Baca `ADD_PYTHON_TO_PATH.md`
- Virtual environment error → Pastikan Python sudah terinstall dengan benar
- Port 8001 sudah digunakan → Ganti port atau matikan aplikasi lain



