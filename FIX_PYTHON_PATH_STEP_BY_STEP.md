# Fix Python PATH - Step by Step

## 🔍 Langkah 1: Cari Lokasi Python

### Cara 1: Via Start Menu
1. Klik Start Menu
2. Ketik "Python 3.12"
3. **Klik kanan** pada "Python 3.12 (64-bit)"
4. Pilih **"Open file location"** atau **"More" → "Open file location"**
5. Di jendela yang terbuka, **klik kanan** shortcut → **"Properties"**
6. Lihat di **"Target"** - contoh: `C:\Users\ASUS\AppData\Local\Programs\Python\Python312\python.exe`
7. **Copy path folder** (tanpa `python.exe`): `C:\Users\ASUS\AppData\Local\Programs\Python\Python312`

### Cara 2: Via File Explorer
1. Buka File Explorer
2. Masuk ke: `C:\Users\ASUS\AppData\Local\Programs\Python\`
3. Cari folder `Python312` atau `Python312-64`
4. **Copy path lengkap** folder tersebut

## 🔧 Langkah 2: Tambahkan ke PATH

### Step-by-Step:

1. **Buka Environment Variables**
   - Tekan `Windows + R`
   - Ketik: `sysdm.cpl`
   - Tekan Enter
   - Tab **"Advanced"**
   - Klik **"Environment Variables"**

2. **Edit PATH**
   - Di bagian bawah (System variables), cari variable bernama **`Path`**
   - Klik **"Edit"**
   - Klik **"New"**
   - Paste path Python (contoh: `C:\Users\ASUS\AppData\Local\Programs\Python\Python312`)
   - Klik **"New"** lagi
   - Tambahkan path Scripts (contoh: `C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Scripts`)
   - Klik **"OK"** di semua dialog

3. **Restart CMD**
   - **Tutup SEMUA CMD/PowerShell yang terbuka**
   - Buka CMD baru
   - Test: `python --version`

## ✅ Langkah 3: Verifikasi

Buka CMD baru dan test:

```cmd
python --version
pip --version
```

Jika berhasil, lanjutkan setup engine.

## 🔄 Alternatif: Reinstall Python dengan PATH

Jika masih tidak berhasil, reinstall Python:

1. Uninstall Python yang sekarang (Control Panel → Programs)
2. Download Python 3.12 dari: https://www.python.org/downloads/
3. **PENTING**: Saat install, **CENTANG "Add Python to PATH"** di bagian bawah
4. Install
5. Restart komputer (untuk memastikan PATH ter-update)
6. Test: `python --version`

## 🎯 Quick Fix Script

Saya juga sudah buat script `find_and_add_python.bat` yang akan membantu mencari dan menambahkan Python ke PATH secara otomatis.


