# Install Python di Windows untuk System Pakar

## 🔍 Masalah
Error: `'python' is not recognized as an internal or external command`

Ini berarti Python belum terinstall atau belum ditambahkan ke PATH.

## 📥 Langkah Install Python

### Opsi 1: Install dari Python.org (Recommended)

1. **Download Python 3.11 atau 3.12**
   - Buka: https://www.python.org/downloads/
   - Pilih versi terbaru (3.11.x atau 3.12.x)
   - Download installer untuk Windows (64-bit)

2. **Jalankan Installer**
   - Double-click file `.exe` yang didownload
   - **PENTING**: Centang checkbox **"Add Python to PATH"** di bagian bawah
   - Klik "Install Now"

3. **Verifikasi Install**
   - Buka CMD baru (penting: tutup CMD yang lama dan buka yang baru)
   - Ketik:
     ```cmd
     python --version
     ```
   - Harus menampilkan: `Python 3.11.x` atau `Python 3.12.x`

4. **Cek pip**
   ```cmd
   pip --version
   ```
   - Harus menampilkan versi pip

### Opsi 2: Install via Microsoft Store (Alternatif)

1. Buka Microsoft Store
2. Cari "Python 3.11" atau "Python 3.12"
3. Klik Install
4. Python akan otomatis ditambahkan ke PATH

### Opsi 3: Install via Laragon (Jika menggunakan Laragon)

Laragon biasanya sudah include Python, tapi perlu diaktifkan:

1. Buka Laragon
2. Menu → Tools → Quick add → Python
3. Pilih versi Python yang diinginkan
4. Install

## ✅ Verifikasi Setelah Install

Buka **CMD baru** (penting: tutup yang lama) dan test:

```cmd
python --version
pip --version
```

Jika berhasil, lanjut ke langkah berikutnya.

## 🚀 Setup Python Engine Setelah Python Terinstall

### 1. Buka CMD di folder s_pakar_engine

```cmd
cd C:\laragon\www\SystemPakar\s_pakar_engine
```

### 2. Buat Virtual Environment

```cmd
python -m venv venv
```

Jika error, coba:
```cmd
py -m venv venv
```

### 3. Aktifkan Virtual Environment

```cmd
venv\Scripts\activate
```

Setelah aktif, prompt akan menampilkan `(venv)` di depan.

### 4. Install Dependencies

```cmd
pip install -r requirements.txt
```

### 5. Jalankan Engine

```cmd
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

Atau gunakan script:
```cmd
start_engine.bat
```

## 🐛 Troubleshooting

### Masalah: Python masih tidak dikenali setelah install

**Solusi 1: Restart CMD**
- Tutup semua CMD/PowerShell
- Buka CMD baru
- Test lagi: `python --version`

**Solusi 2: Tambah ke PATH Manual**
1. Cari lokasi Python (biasanya `C:\Users\YourName\AppData\Local\Programs\Python\Python311\`)
2. Buka System Properties → Environment Variables
3. Edit "Path" di System Variables
4. Tambahkan:
   - `C:\Users\YourName\AppData\Local\Programs\Python\Python311\`
   - `C:\Users\YourName\AppData\Local\Programs\Python\Python311\Scripts\`
5. Restart CMD

**Solusi 3: Gunakan `py` launcher**
Windows biasanya punya Python launcher:
```cmd
py --version
py -m venv venv
py -m pip install -r requirements.txt
```

### Masalah: pip tidak ditemukan

**Solusi:**
```cmd
python -m ensurepip --upgrade
```

Atau install ulang Python dengan centang "Add Python to PATH"

### Masalah: Permission denied saat install

**Solusi:**
- Jalankan CMD sebagai Administrator
- Atau install ke folder user (bukan Program Files)

## 📝 Quick Check Script

Buat file `check_python.bat` di folder `s_pakar_engine`:

```batch
@echo off
echo Checking Python installation...
echo.

echo [1] Python version:
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo [2] pip version:
pip --version
if errorlevel 1 (
    echo ERROR: pip not found!
    pause
    exit /b 1
)

echo.
echo [3] Virtual environment:
if exist "venv\Scripts\activate.bat" (
    echo Virtual environment exists
) else (
    echo Virtual environment not found
    echo Creating virtual environment...
    python -m venv venv
)

echo.
echo [4] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [5] Checking uvicorn:
uvicorn --version
if errorlevel 1 (
    echo uvicorn not found, installing...
    pip install uvicorn[standard]
)

echo.
echo ========================================
echo All checks passed! Python is ready.
echo ========================================
pause
```

Jalankan:
```cmd
check_python.bat
```

## 🎯 Langkah Cepat (Setelah Python Terinstall)

```cmd
cd C:\laragon\www\SystemPakar\s_pakar_engine
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## 📞 Masih Error?

Jika masih ada masalah:
1. Pastikan Python sudah terinstall (cek di Control Panel → Programs)
2. Restart komputer (kadang perlu untuk update PATH)
3. Gunakan `py` launcher sebagai alternatif
4. Install Python via Microsoft Store (lebih mudah)



