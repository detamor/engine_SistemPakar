# Reinstall Python dengan PATH (Paling Mudah)

## 🎯 Cara Termudah: Reinstall dengan PATH

Jika menambahkan PATH manual terlalu rumit, cara termudah adalah **reinstall Python** dengan centang "Add Python to PATH".

## 📥 Langkah-langkah:

### 1. Uninstall Python yang Sekarang (Opsional)
- Buka Control Panel → Programs and Features
- Cari "Python 3.12"
- Uninstall (opsional, bisa langsung install ulang)

### 2. Download Python
- Buka: https://www.python.org/downloads/
- Klik "Download Python 3.12.x" (versi terbaru)
- Tunggu download selesai

### 3. Install dengan PATH
1. **Double-click** file installer yang didownload
2. **PENTING**: Di bagian bawah, **CENTANG checkbox "Add Python to PATH"**
   - Ini adalah langkah paling penting!
3. Klik **"Install Now"**
4. Tunggu sampai selesai
5. Klik **"Close"**

### 4. Verifikasi
1. **Tutup semua CMD/PowerShell**
2. Buka **CMD baru**
3. Test:
   ```cmd
   python --version
   pip --version
   ```

Jika berhasil, Python sudah siap digunakan!

## ✅ Setelah Python Berhasil

Lanjutkan setup engine:

```cmd
cd C:\laragon\www\SystemPakar\s_pakar_engine
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

Atau gunakan script:
```cmd
start_engine.bat
```

## 🎯 Kenapa Reinstall Lebih Mudah?

- Otomatis menambahkan ke PATH
- Tidak perlu edit environment variables manual
- Pasti berhasil jika centang "Add Python to PATH"
- Lebih cepat daripada edit PATH manual

## 📝 Catatan

- Tidak perlu uninstall Python lama (bisa langsung install ulang)
- Installer akan update Python yang sudah ada
- Pastikan **centang "Add Python to PATH"** saat install!


