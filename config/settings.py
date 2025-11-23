"""
Konfigurasi untuk System Pakar Engine
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Fonte WhatsApp API Configuration
FONTE_API_KEY = os.getenv('FONTE_API_KEY', '')
FONTE_BASE_URL = os.getenv('FONTE_BASE_URL', 'https://api.fonte.com')

# Laravel Backend API Configuration
LARAVEL_API_URL = os.getenv('LARAVEL_API_URL', 'http://localhost:8000/api')
LARAVEL_API_TOKEN = os.getenv('LARAVEL_API_TOKEN', '')

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')



