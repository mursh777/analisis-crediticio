import pandas as pd
from sqlalchemy import create_engine
import os
import time
from src.common.database import get_engine

def ejecutar_ingesta():
    db_url = "postgresql://admin:password123@db:5432/loan_db"
    
    print("--- Iniciando proceso de ingesta ---")
    
    try:
        # 1. Conexión a la base de datos
        engine = create_engine(db_url)
        
        # 2. Leer el CSV 
        ruta_csv = 'data/02_loan_data.csv'
        df = pd.read_csv(ruta_csv)
        print(f"Archivo leido exitosamente: {len(df)} filas encontradas.")

        # 3. Cargar a PostgreSQL
        # 'if_exists=replace' crea la tabla si no existe o la sobreescribe
        df.to_sql('prestamos_crudos', con=engine, if_exists='append', index=False)
        
        print("¡Éxito! Los datos están cargados en la tabla 'prestamos_crudos'.")
        
    except Exception as e:
        print(f"Error en la ingesta: {e}")

if __name__ == "__main__":
    time.sleep(5)
    ejecutar_ingesta()
