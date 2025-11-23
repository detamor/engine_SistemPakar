"""
FastAPI Application untuk System Pakar Diagnosis Penyakit Tanaman Hias
Menggunakan Experta untuk rule-based reasoning dan Certainty Factor
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Tambahkan path app ke sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.expert_system import ExpertSystemService
from app.api.client import LaravelAPIClient

app = FastAPI(title="System Pakar Engine", version="1.0.0")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dalam production, ganti dengan domain spesifik
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
expert_system = ExpertSystemService()
laravel_client = LaravelAPIClient()


class SymptomInput(BaseModel):
    symptom_id: int
    user_cf: float  # 0.0 - 1.0


class DiagnosisRequest(BaseModel):
    diagnosis_id: int
    plant_id: int
    symptoms: List[SymptomInput]


@app.get("/")
async def root():
    return {
        "message": "System Pakar Engine API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/diagnose")
async def diagnose(request: DiagnosisRequest):
    """
    Endpoint untuk melakukan diagnosis penyakit tanaman hias
    menggunakan Certainty Factor
    """
    try:
        # Ambil data penyakit dan gejala dari Laravel API
        diseases_data = laravel_client.get_diseases_by_plant(request.plant_id)
        
        if not diseases_data.get('success'):
            raise HTTPException(
                status_code=404,
                detail="Data penyakit tidak ditemukan"
            )
        
        # Proses diagnosis dengan Certainty Factor
        result = expert_system.calculate_certainty_factor(
            plant_id=request.plant_id,
            symptoms=request.symptoms,
            diseases_data=diseases_data['data']
        )
        
        return {
            "success": True,
            "data": {
                "diagnosis_id": request.diagnosis_id,
                "disease_id": result.get('disease_id'),
                "disease_name": result.get('disease_name'),
                "certainty_value": result.get('certainty_value'),
                "recommendation": result.get('recommendation'),
                "all_possibilities": result.get('all_possibilities', [])
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error dalam proses diagnosis: {str(e)}"
        )


@app.get("/api/diseases/{plant_id}")
async def get_diseases(plant_id: int):
    """
    Mendapatkan daftar penyakit berdasarkan plant_id
    """
    try:
        result = laravel_client.get_diseases_by_plant(plant_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)



