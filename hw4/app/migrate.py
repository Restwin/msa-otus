import os
import time
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, ProgrammingError
from .models import db
from .config import Config

def run_migrations():
    # Загрузка конфигурации из переменных окружения
    config = Config()
    DATABASE_URL = config.get_db_uri()

    print(f"Attempting to connect to database: {DATABASE_URL.split('@')[-1]}") # Не печатаем пароль

    # Ждем доступности БД
    max_retries = 10
    retry_delay = 5
    engine = None

    for attempt in range(max_retries):
        try:
            engine = create_engine(DATABASE_URL)
            with engine.connect() as connection:
                print("Successfully connected to the database.")
            break 
        except OperationalError as e:
            print(f"Database connection failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Exiting.")
                exit(1)
    
    if not engine:
        print("Could not establish database engine.")
        exit(1)

    # Создаем таблицы на основе моделей SQLAlchemy
    try:
        print("Applying migrations (creating tables if not exist)...")
        db.metadata.create_all(bind=engine)
        print("Migrations applied successfully.")
    except ProgrammingError as e:
        print(f"Warning during migration (table might already exist or schema mismatch): {e}")
    except Exception as e:
        print(f"Error applying migrations: {e}")
        exit(1)

if __name__ == '__main__':
    run_migrations()
