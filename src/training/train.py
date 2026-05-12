import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import job as os
import joblib
from src.common.database import get_engine

def entrenar_modelo():
    engine = get_engine()
    
    # 1. Cargar los datos limpios (Capa Plata)
    df = pd.read_sql("SELECT * FROM prestamos_limpios", con=engine)
    
    # 2. Separar características (X) y target (y)
    X = df.drop(columns=['loan_status'])
    y = df['loan_status']
    
    # 3. DIVISIÓN ESTRATIFICADA (75% training, 25% testing)
    # El parámetro 'stratify=y' asegura que el ~22% de rechazados 
    # de tu imagen se mantenga en ambos sets.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=0.25, 
        random_state=42, 
        stratify=y 
    )
    
    print(f"Set de Entrenamiento: {len(X_train)} filas")
    print(f"Set de Prueba: {len(X_test)} filas")

    # 4. Entrenamiento del Motor (Random Forest como ejemplo)
    print("Entrenando el motor de Machine Learning...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 5. Evaluación (Lo que pidió la profe: Analizar la data)
    y_pred = model.predict(X_test)
    
    print("\n=== REPORTE DE CLASIFICACIÓN ===")
    print(classification_report(y_test, y_pred))
    
    print("\n=== MATRIZ DE CONFUSIÓN ===")
    print(confusion_matrix(y_test, y_pred))

    # 6. Guardar el modelo (opcional para el comando de correr todo)
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/modelo_riesgo_v1.pkl')
    print("\nModelo guardado en 'models/modelo_riesgo_v1.pkl'")

if __name__ == "__main__":
    entrenar_modelo()