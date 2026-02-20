import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)


class BaseConfig:
    """Base configuration shared by all environments."""

    SECRET_KEY = os.getenv('SECRET_KEY', '47ZMOcbXG0hr89tJR_VWma_82S_fHCRXXdLo7Ib0P6Kw6kk6AgYp7devbO6_A6PK')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '58EruUQ6jWZNzrlHISZ7W1BpsPJLJmUXBFfXC8FTDXW5n0sZtalW-ZloabLW1_Qv')

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    PROPAGATE_EXCEPTIONS = True

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:postgres@localhost:5432/merged_db'
    )

    # Multiple database bindings for CIS databases
    SQLALCHEMY_BINDS = {
        'cis_db_1': os.getenv(
            'CIS_DB_1_URL',
            'postgresql://postgres:postgres@localhost:5432/ganjamdj'
        ),
        'cis_db_2': os.getenv(
            'CIS_DB_2_URL',
            'postgresql://postgres:postgres@localhost:5432/ganjamcjm'
        ),
        'cis_db_3': os.getenv(
            'CIS_DB_3_URL',
            'postgresql://postgres:postgres@localhost:5432/ganjamsdjm'
        ),
        'cis_db_4': os.getenv(
            'CIS_DB_4_URL',
            'postgresql://postgres:postgres@localhost:5432/ganjamcjsd'
        ),
    }


class DevelopmentConfig(BaseConfig):
    DEBUG = True

class TestingConfig(BaseConfig):
    TESTING = True

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
