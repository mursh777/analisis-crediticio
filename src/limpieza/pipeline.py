import os
import glob
import pandas as pd
from src.common.database import get_engine
from src.limpieza.limpieza import build_pipeline 

def ejecutar_pipeline():
    engine = get_engine()
    
    # === FASE DE INGESTA ===
    print("Iniciando Fase de Ingesta...")
    archivos_csv = glob.glob("data/*.csv")
    if not archivos_csv:
        print("Error: No hay archivos CSV en la carpeta data/")
        return
        
    archivo_origen = max(archivos_csv, key=os.path.getctime)
    print(f"Cargando archivo: {archivo_origen}")
    df_crudo = pd.read_csv(archivo_origen)
    

    df_crudo.to_sql("prestamos_crudos", con=engine, if_exists="replace", index=False)
    
    # === FASE DE TRANSFORMACIÓN Y LIMPIEZA ===
    print("Iniciando Limpieza...")
    df_crudo = df_crudo.drop_duplicates()
    
    X = df_crudo.drop(columns=['loan_status'])
    y = df_crudo['loan_status']
    
    pipeline = build_pipeline(X)
    X_limpio = pipeline.fit_transform(X) 
    
    nombres_finales = pipeline.get_feature_names_out()
    df_final = pd.DataFrame(X_limpio, columns=nombres_finales)
    df_final.columns = [c.split('__')[-1] for c in df_final.columns]
    df_final['loan_status'] = y.values
    
    # === FASE DE CARGA ===
    print("Cargando datos limpios...")
    df_final.to_sql("prestamos_limpios", con=engine, if_exists="replace", index=False)
    df_final.to_csv("data/prestamos_limpios.csv", index=False)
    
    print("¡Proceso de Ingesta y Transformación terminado con exito!")

if __name__ == "__main__":
    ejecutar_pipeline()