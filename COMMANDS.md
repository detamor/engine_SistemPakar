# Command yang Benar untuk Setup Python Engine

## ✅ Python Sudah Bisa Digunakan!

Anda sudah berhasil dengan `python --version`, jadi gunakan `python` untuk semua command.

## 🚀 Setup Cepat (Pilih Salah Satu)

### Opsi 1: Gunakan Script Otomatis (Paling Mudah)

```cmd
SETUP_NOW.bat
```

Setelah selesai, jalankan:
```cmd
start_server.bat
```

### Opsi 2: Manual Step-by-Step

```cmd
REM 1. Buat virtual environment
python -m venv venv

REM 2. Aktifkan virtual environment
venv\Scripts\activate

REM 3. Upgrade pip
python -m pip install --upgrade pip

REM 4. Install dependencies
python -m pip install -r requirements.txt

REM 5. Jalankan server
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## 📝 Catatan Penting

- Gunakan `python` bukan `py` (karena `py` tidak dikenali)
- Gunakan `python -m pip` bukan `pip` (karena pip belum di PATH)
- Setelah virtual environment aktif, `pip` dan `uvicorn` akan tersedia

## ✅ Verifikasi Setelah Setup

Setelah virtual environment aktif, test:

```cmd
pip --version
uvicorn --version
```

Jika berhasil, server siap dijalankan!

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Buat venv | `python -m venv venv` |
| Aktifkan venv | `venv\Scripts\activate` |
| Install deps | `python -m pip install -r requirements.txt` |
| Jalankan server | `uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload` |

