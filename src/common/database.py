from sqlalchemy import create_engine
import os

def get_engine():
    user = "admin"
    password = "password123"
    host = "db"  
    port = "5432"
    db_name = "loan_db"
    
    url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    
    #Motor de conexion
    engine = create_engine(url)
    return engine