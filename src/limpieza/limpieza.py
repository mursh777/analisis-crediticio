import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.base import BaseEstimator, TransformerMixin
from src.common.database import get_engine

class Winsorizer(BaseEstimator, TransformerMixin):
    def __init__(self, limits=(0.05, 0.05)):
        self.limits = limits
    def fit(self, X, y = None):
        self.columns_ = X.columns if isinstance(X, pd.DataFrame) else np.arange(X.shape[1])
        return self
    def transform(self, X):
        X = pd.DataFrame(X, columns=self.columns_)
        for col in self.columns_:
            lower = X[col].quantile(self.limits[0])
            upper = X[col].quantile(1 - self.limits[1])
            X[col] = np.clip(X[col], lower, upper)
        return X
    
    def get_feature_names_out(self, input_features=None):
        return self.columns_

class CorrelationFilter(BaseEstimator, TransformerMixin):
    def __init__(self, threshold=0.9):
        self.threshold = threshold
    def fit(self, X, y=None):
        self.feature_names_in_ = X.columns if isinstance(X, pd.DataFrame) else [str(i) for i in range(X.shape[1])]
        df = pd.DataFrame(X)
        corr = df.corr().abs()
        upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
        self.to_drop_ = [col for col in upper.columns if any(upper[col] > self.threshold)]
        self.features_ = [i for i, col in enumerate(df.columns) if col not in self.to_drop_]
        return self
    def transform(self, X):
        df = pd.DataFrame(X)
        return df.iloc[:, self.features_].values
    
    def get_feature_names_out(self, input_features=None):
        return [self.feature_names_in_[i] for i in self.features_]

def build_pipeline(df):
    num_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    num_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('winsorizer', Winsorizer(limits=(0.01, 0.01))),
        ('scaler', StandardScaler())
    ])
    
    cat_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
        
    preprocessor = ColumnTransformer(transformers=[
        ('num', num_transformer, num_cols),
        ('cat', cat_transformer, cat_cols)
    ])
    
    full_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('colinealidad', CorrelationFilter(threshold=0.85))
    ])
    
    return full_pipeline

def ejecutar_limpieza():
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM prestamos_crudos", con=engine)
    
    df = df.drop_duplicates()
    
    X = df.drop(columns=['loan_status'])
    y = df['loan_status']
    
    pipeline = build_pipeline(X)
    X_limpio = pipeline.fit_transform(X)

    # Obtener nombres 
    nombres_finales = pipeline.get_feature_names_out()
    
    df_final = pd.DataFrame(X_limpio, columns=nombres_finales)
    
    # Limpieza estética
    df_final.columns = [c.split('__')[-1] for c in df_final.columns]
    
    df_final['loan_status'] = y.values
    
    # Guardar en base de datos
    df_final.to_sql("prestamos_limpios", con=engine, if_exists="replace", index=False)
    
    # Guardar en CSV
    df_final.to_csv("data/prestamos_limpios.csv", index=False)
    print("Limpieza completada.")

if __name__ == "__main__":
    ejecutar_limpieza()