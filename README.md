# System Pakar Engine (Python)

Engine untuk menangani logika bisnis sistem pakar, perhitungan Certainty Factor, dan integrasi dengan Laravel API.

## Teknologi

- **Python 3.12**
- **FastAPI** - Web framework untuk API
- **Experta** - Rule-based expert system library untuk inference engine
- **NumPy** - Perhitungan Certainty Factor (opsional, untuk operasi numerik)
- **Uvicorn** - ASGI server

### Menggunakan Experta Library

Sistem ini menggunakan **Experta** library untuk implementasi expert system dengan rule-based reasoning. Experta menyediakan:

- **KnowledgeEngine**: Mesin inference untuk menjalankan rules
- **Facts**: Fakta yang dideklarasikan ke dalam knowledge base
- **Rules**: Aturan IF-THEN untuk reasoning
- **Certainty Factor**: Dukungan built-in untuk perhitungan CF

Implementasi menggunakan:
- `UserSymptom` Fact: Gejala yang dipilih user dengan CF value
- `DiseaseRule` Fact: Aturan penyakit dengan gejala dan CF dari pakar
- Rule untuk menghitung CF: `CF(H,E) = CF(E) * CF(Rule)`
- Formula combine CF: `CF_combine = CF_old + (CF_new * (1 - CF_old))`

## Versi Python yang Direkomendasikan

**Python 3.11** atau **Python 3.12**

Alasan:
- Kompatibel dengan library modern (pydantic 2.x, aiohttp 3.x)
- Performa lebih baik dibanding Python 3.10
- Support jangka panjang
- Kompatibel dengan Laravel 11 dan Vue 3

## Setup

1. Install Python 3.11 atau 3.12
2. Buat virtual environment:
```bash
python -m venv venv
```

3. Aktifkan virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Copy file `.env.example` ke `.env` dan isi konfigurasi:
```bash
cp .env.example .env
```

6. Jalankan server:
```bash
# Windows
START_ENGINE.bat

# Manual
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## Struktur Folder

```
s_pakar_engine/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── whatsapp/
│   │   ├── __init__.py
│   │   └── fonte_client.py  # WhatsApp client (Fonte API)
│   ├── services/
│   │   ├── __init__.py
│   │   └── expert_system.py # Expert system & CF calculation
│   └── api/
│       ├── __init__.py
│       └── client.py        # Laravel API client
├── config/
│   └── settings.py          # Configuration
├── requirements.txt
├── README.md
└── .env                     # Environment variables (not in git)
```

## API Endpoints

### POST /diagnose
Menghitung Certainty Factor untuk diagnosis penyakit tanaman.

**Request:**
```json
{
  "plant_id": 1,
  "symptoms": [
    {
      "symptom_id": 1,
      "certainty_factor": 0.8
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "diagnosis": [
      {
        "disease_id": 1,
        "disease_name": "Penyakit X",
        "certainty_value": 0.85,
        "recommendation": "..."
      }
    ]
  }
}
```

## Environment Variables

Buat file `.env` dengan konfigurasi berikut:

```env
# Laravel API
LARAVEL_API_URL=http://localhost:8000/api

# Fonte WhatsApp API (optional)
FONTE_API_KEY=your_api_key_here
FONTE_BASE_URL=https://api.fonnte.com
```

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run dengan auto-reload
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

# Run tests (jika ada)
pytest
```

## Dokumentasi API

Setelah server berjalan, akses dokumentasi API di:
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## License

MIT
