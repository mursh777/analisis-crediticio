import pandas as pd
import numpy as np
from src.common.database import get_engine

class QualityCheck:
    def __init__(self, data: pd.DataFrame, exclude_inconsistencies: list = None ):
        self.data = data
        self.exclude_inconsistencies = exclude_inconsistencies or []
    
    #Valores nulos
    def has_nulls(self):
        return self.data.isnull().sum().sum()
    
    #Valores duplicados
    def has_duplicates(self):
        return self.data.duplicated().sum()
    
    #Valores atipicos
    def has_outliers(self):
        numeric_cols = self.data.select_dtypes(include=["number"])
        outliers_total = 0
        for col in numeric_cols.columns:
            Q1 = numeric_cols[col].quantile(0.25)
            Q3 = numeric_cols[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            if ((numeric_cols[col] < lower) | (numeric_cols[col] > upper)).any():
                return True
        return False
    
    #Valores inconsistentes negativos
    def has_negative_values(self) -> bool:
        numeric_cols = self.data.select_dtypes(include=["number"])
        numeric_cols = numeric_cols.drop(columns=self.exclude_inconsistencies, errors='ignore' )
        for col in numeric_cols.columns:
            if (numeric_cols[col] < 0).any():
                return True
        return False
    
    #Valores inconsistentes categoricos
    def has_categorical_inconsistencies(self) -> bool:
        cat_cols = self.data.select_dtypes(include=["object"])
        for col in cat_cols.columns:
            values = cat_cols[col].dropna().astype(str)
            normalized = values.str.strip().str.lower()
            if len(values.unique()) != len(normalized.unique()):
                return True
        return False
    
    #Valores inconsistentes generales
    def has_inconsistencies(self) -> bool:
        return self.has_negative_values() or self.has_categorical_inconsistencies()

    #Reporte puntaje ponderado
    def quality_score_weighted(self) -> float:
        weights = {
            "nulos/faltantes": 0.3,
            "duplicados": 0.2,
            "outliers": 0.2,
            "inconsistencias": 0.3
        }
        checks = {
            "nulos/faltantes": self.has_nulls(),
            "duplicados": self.has_duplicates(),
            "outliers": self.has_outliers(),
            "inconsistencias": self.has_inconsistencies()
        }
        penalty = 0
        for key in checks:
            if checks[key]:
                penalty += weights[key]
        quality = (1 - penalty) * 100
        return round(quality, 2)
    
    def full_report(self):
        return {
            "Hay nulos": self.has_nulls(),
            "Hay duplicados": self.has_duplicates(),
            "Hay inconsistentes": self.has_outliers(),
            "Hay negativos": self.has_negative_values(),
            "Hay errores de texto": self.has_categorical_inconsistencies(),
            "Puntaje final": f"{self.quality_score_weighted()}%"
        }
    
def ejecutar_diagnostico():
        engine = get_engine()
        df = pd.read_sql("SELECT * FROM prestamos_crudos", con=engine)

        checker = QualityCheck(df, exclude_inconsistencies=['loan_status'])
        reporte = checker.full_report()

        print("\n=== chequeo de calidad de datos ===")
        for k, v in reporte.items():
            print(f" > {k}: {v}")

if __name__ == "__main__":
        ejecutar_diagnostico()