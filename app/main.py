"""
FastAPI Application untuk System Pakar Diagnosis Penyakit Tanaman Hias
Menggunakan Experta Library untuk rule-based reasoning dan Certainty Factor

Experta adalah Python library untuk expert system yang menggunakan
rule-based approach dengan support untuk Certainty Factor.
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
from loguru import logger

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


class DiseaseSymptomInput(BaseModel):
    symptom_id: int
    certainty_factor: float


class DiseaseInput(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    cause: Optional[str] = None
    solution: Optional[str] = None
    prevention: Optional[str] = None
    symptoms: List[DiseaseSymptomInput] = []


class DiagnosisRequest(BaseModel):
    diagnosis_id: int
    plant_id: int
    symptoms: List[SymptomInput]
    diseases_data: Optional[List[DiseaseInput]] = None  # Data penyakit dari Laravel


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
def diagnose(request: DiagnosisRequest):
    """
    Endpoint untuk melakukan diagnosis penyakit tanaman hias
    menggunakan Certainty Factor
    """
    try:
        # Prioritas: Gunakan diseases_data dari request body (dikirim langsung dari Laravel)
        # Fallback: Ambil dari Laravel API jika tidak ada di request
        if request.diseases_data and len(request.diseases_data) > 0:
            # Convert Pydantic models ke dict
            data = []
            for disease in request.diseases_data:
                disease_dict = {
                    'id': disease.id,
                    'name': disease.name,
                    'description': disease.description or '',
                    'cause': disease.cause or '',
                    'solution': disease.solution or '',
                    'prevention': disease.prevention or '',
                    'symptoms': []
                }
                for symptom in disease.symptoms:
                    disease_dict['symptoms'].append({
                        'symptom_id': symptom.symptom_id,
                        'certainty_factor': symptom.certainty_factor
                    })
                data.append(disease_dict)
            
            logger.info(f"Menggunakan diseases_data dari request body: {len(data)} penyakit")
        else:
            # Fallback: Ambil data penyakit dan gejala dari Laravel API
            logger.info(f"diseases_data tidak ada di request, mengambil dari Laravel API untuk plant_id {request.plant_id}")
            try:
                diseases_data = laravel_client.get_diseases_by_plant(request.plant_id)
                
                if not diseases_data.get('success'):
                    logger.error(f"Gagal mengambil data penyakit dari Laravel API: {diseases_data.get('error', 'Unknown error')}")
                    raise HTTPException(
                        status_code=404,
                        detail=f"Data penyakit tidak ditemukan: {diseases_data.get('error', 'Unknown error')}"
                    )
                
                # Validasi format data
                data = diseases_data.get('data', [])
                if not isinstance(data, list):
                    logger.error(f"Data penyakit harus list, tapi mendapat: {type(data)}")
                    raise HTTPException(
                        status_code=500,
                        detail=f"Format data penyakit tidak valid: expected list, got {type(data)}"
                    )
            except Exception as e:
                logger.error(f"Error saat mengambil data penyakit dari Laravel API: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Error mengambil data penyakit: {str(e)}"
                )
        
        if len(data) == 0:
            raise HTTPException(
                status_code=404,
                detail="Tidak ada data penyakit untuk tanaman ini"
            )
        
        # Convert symptoms ke format dict
        symptoms_list = []
        for symptom in request.symptoms:
            symptoms_list.append({
                'symptom_id': symptom.symptom_id,
                'user_cf': float(symptom.user_cf)
            })
        
        # Proses diagnosis dengan Certainty Factor
        logger.info(f"Memproses diagnosis untuk diagnosis_id: {request.diagnosis_id}")
        result = expert_system.calculate_certainty_factor(
            plant_id=request.plant_id,
            symptoms=symptoms_list,
            diseases_data=data
        )
        
        logger.info(f"Diagnosis selesai, menyiapkan response untuk diagnosis_id: {request.diagnosis_id}")
        
        response_data = {
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
        
        logger.info(f"Response data siap untuk diagnosis_id: {request.diagnosis_id}, disease_id: {result.get('disease_id')}")
        logger.info(f"Response size: {len(str(response_data))} characters")
        
        # Pastikan response dikembalikan dengan benar
        import json
        try:
            # Test serialization
            json.dumps(response_data)
            logger.info("Response dapat di-serialize ke JSON")
        except Exception as json_error:
            logger.error(f"Error serializing response: {json_error}")
            raise HTTPException(
                status_code=500,
                detail=f"Error serializing response: {str(json_error)}"
            )
        
        return response_data
        
    except HTTPException:
        # Re-raise HTTPException as-is
        raise
    except Exception as e:
        logger.error(f"Error dalam proses diagnosis: {str(e)}", exc_info=True)
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



