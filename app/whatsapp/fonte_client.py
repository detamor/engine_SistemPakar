"""
WhatsApp Client menggunakan Fonte API
"""
import os
import requests
from typing import Optional, Dict, Any
from loguru import logger
from dotenv import load_dotenv

load_dotenv()


class FonteWhatsAppClient:
    """
    Client untuk berkomunikasi dengan WhatsApp melalui Fonte API
    """
    
    def __init__(self):
        self.api_key = os.getenv('FONTE_API_KEY')
        self.base_url = os.getenv('FONTE_BASE_URL', 'https://api.fonte.com')
        self.session = requests.Session()
        
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            })
        else:
            logger.warning("FONTE_API_KEY tidak ditemukan di environment variables")
    
    def send_message(self, phone_number: str, message: str) -> Dict[str, Any]:
        """
        Mengirim pesan WhatsApp
        
        Args:
            phone_number: Nomor telepon tujuan (format: 6281234567890)
            message: Pesan yang akan dikirim
            
        Returns:
            Dict berisi response dari API
        """
        try:
            url = f"{self.base_url}/messages"
            payload = {
                "to": phone_number,
                "message": message,
                "type": "text"
            }
            
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            
            logger.info(f"Pesan berhasil dikirim ke {phone_number}")
            return {
                "success": True,
                "data": response.json()
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error mengirim pesan: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def send_template_message(self, phone_number: str, template_name: str, 
                             parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mengirim pesan template WhatsApp
        
        Args:
            phone_number: Nomor telepon tujuan
            template_name: Nama template yang sudah terdaftar
            parameters: Parameter untuk template
            
        Returns:
            Dict berisi response dari API
        """
        try:
            url = f"{self.base_url}/messages/template"
            payload = {
                "to": phone_number,
                "template": template_name,
                "parameters": parameters
            }
            
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            
            logger.info(f"Template message berhasil dikirim ke {phone_number}")
            return {
                "success": True,
                "data": response.json()
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error mengirim template message: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_message_status(self, message_id: str) -> Dict[str, Any]:
        """
        Mengecek status pesan
        
        Args:
            message_id: ID pesan yang ingin dicek
            
        Returns:
            Dict berisi status pesan
        """
        try:
            url = f"{self.base_url}/messages/{message_id}"
            response = self.session.get(url)
            response.raise_for_status()
            
            return {
                "success": True,
                "data": response.json()
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error mengecek status pesan: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }



