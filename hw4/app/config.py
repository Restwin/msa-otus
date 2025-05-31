import os

class Config:
    DB_USER = os.environ.get('POSTGRES_USER')
    DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    DB_HOST = os.environ.get('POSTGRES_HOST')
    DB_NAME = os.environ.get('POSTGRES_DB')
    DB_PORT = os.environ.get('POSTGRES_PORT', '5432')
    APP_PORT = int(os.environ.get('APP_PORT', 5000))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Функция для построения URI
    def get_db_uri(self):
        if 'DATABASE_URL' in os.environ:
            return os.environ.get('DATABASE_URL')
        elif all([self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME]):
            return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        else:
            print("WARNING: Database connection details not fully configured via environment variables. Using fallback.")
            return 'postgresql://user:password@localhost:5432/mydatabase'
