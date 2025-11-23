# Menambahkan Python ke PATH Environment Variable

## 🔍 Masalah
Python sudah terinstall tapi tidak dikenali di CMD karena belum ditambahkan ke PATH.

## ✅ Solusi 1: Gunakan `py` Launcher (Paling Mudah)

Windows biasanya sudah punya Python launcher (`py`) yang otomatis di PATH. Coba dulu:

```cmd
py --version
```

Jika berhasil, gunakan `py` untuk semua command:

```cmd
py -m venv venv
py -m pip install -r requirements.txt
```

## ✅ Solusi 2: Tambah Python ke PATH Manual

### Langkah-langkah:

1. **Cari Lokasi Python**
   - Biasanya ada di: `C:\Users\ASUS\AppData\Local\Programs\Python\Python312\`
   - Atau: `C:\Python312\`
   - Atau cek di Start Menu → Python 3.12 → Right click → Open file location

2. **Buka Environment Variables**
   - Tekan `Windows + R`
   - Ketik: `sysdm.cpl` → Enter
   - Tab "Advanced" → Klik "Environment Variables"

   Atau:
   - Windows 10/11: Settings → System → About → Advanced system settings → Environment Variables

3. **Edit PATH**
   - Di bagian "System variables", cari variable `Path`
   - Klik "Edit"
   - Klik "New"
   - Tambahkan 2 path berikut (sesuaikan dengan lokasi Python Anda):
     ```
     C:\Users\ASUS\AppData\Local\Programs\Python\Python312
     C:\Users\ASUS\AppData\Local\Programs\Python\Python312\Scripts
     ```
   - Klik "OK" di semua dialog

4. **Restart CMD**
   - Tutup semua CMD/PowerShell
   - Buka CMD baru
   - Test: `python --version`

## ✅ Solusi 3: Reinstall Python dengan PATH (Paling Mudah)

1. Uninstall Python yang sekarang (jika perlu)
2. Download ulang dari https://www.python.org/downloads/
3. Saat install, **PASTIKAN centang "Add Python to PATH"**
4. Install
5. Restart CMD dan test: `python --version`

## 🧪 Test Setelah Setup

Buka CMD baru dan test:

```cmd
python --version
pip --version
```

Jika berhasil, lanjutkan setup engine.

## 📝 Catatan

- Setelah edit PATH, **WAJIB restart CMD/PowerShell**
- Jika masih error, restart komputer
- `py` launcher biasanya lebih reliable di Windows



