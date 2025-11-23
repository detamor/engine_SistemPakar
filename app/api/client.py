"""
Client untuk berkomunikasi dengan Laravel Backend API
"""
import os
import requests
from typing import Optional, Dict, Any
from loguru import logger
from dotenv import load_dotenv

load_dotenv()


class LaravelAPIClient:
    """
    Client untuk berkomunikasi dengan Laravel Backend
    """
    
    def __init__(self):
        self.base_url = os.getenv('LARAVEL_API_URL', 'http://localhost:8000/api')
        self.api_token = os.getenv('LARAVEL_API_TOKEN')
        self.session = requests.Session()
        
        if self.api_token:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_token}',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            })
    
    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        POST request ke Laravel API
        
        Args:
            endpoint: Endpoint API (contoh: '/whatsapp/send')
            data: Data yang akan dikirim
            
        Returns:
            Dict berisi response
        """
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.post(url, json=data)
            response.raise_for_status()
            
            return {
                "success": True,
                "data": response.json()
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error POST ke {endpoint}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        GET request ke Laravel API
        
        Args:
            endpoint: Endpoint API
            params: Query parameters
            
        Returns:
            Dict berisi response
        """
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            return {
                "success": True,
                "data": response.json()
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error GET ke {endpoint}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_diseases_by_plant(self, plant_id: int) -> Dict[str, Any]:
        """
        Mendapatkan data penyakit beserta gejala dan CF berdasarkan plant_id
        
        Args:
            plant_id: ID tanaman
            
        Returns:
            Dict berisi data penyakit dengan gejala dan CF
        """
        try:
            # Gunakan endpoint public (tidak perlu auth)
            endpoint = f"/public/diseases/plant/{plant_id}"
            result = self.get(endpoint)
            
            if result.get('success'):
                return result
            
            # Fallback: coba endpoint admin jika public tidak ada
            logger.warning(f"Public endpoint tidak tersedia, mencoba admin endpoint")
            endpoint = f"/admin/diseases/plant/{plant_id}"
            result = self.get(endpoint)
            
            if result.get('success'):
                return result
            
            # Jika kedua endpoint tidak ada, coba alternatif
            # Ambil semua penyakit dan filter di Python
            endpoint = "/admin/diseases"
            result = self.get(endpoint)
            
            if result.get('success'):
                diseases = result.get('data', [])
                # Filter berdasarkan plant_id
                filtered = [d for d in diseases if d.get('plant_id') == plant_id]
                return {
                    "success": True,
                    "data": filtered
                }
            
            return result
            
        except Exception as e:
            logger.error(f"Error mendapatkan diseases: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "data": []
            }

