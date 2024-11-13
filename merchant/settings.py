import os
from dotenv import dotenv_values

ROOT_DIR = src_path = os.path.dirname(os.path.abspath(__file__))

environ = {}

if os.path.exists(os.path.join(ROOT_DIR, '.env')):
    environ = {**dotenv_values(os.path.join(ROOT_DIR, '.env'))}

environ.update(**os.environ)
POSTGRES_HOST = environ.get('POSTGRES_HOST', '127.0.0.1')
POSTGRES_PORT = environ.get("POSTGRES_PORT", '5432')
POSTGRES_USER = environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = environ.get('POSTGRES_PASSWORD', 'postgres')
POSTGRES_DATABASE = environ.get('POSTGRES_DATABASE', 'merchant_point')
