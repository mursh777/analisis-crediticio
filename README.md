# Predicción de Evaluaciones de Riesgos Crediticios
El proyecto tiene como objetivo predecir, mediante un modelo de IA, si se acepta el
préstamo solicitado por un cliente o se rechaza por riesgo de no pago, dependiendo de
su historial crediticio y de otras variables como su ingreso anual.
## Componentes del sistema
- **Ingesta de datos**: Para cargar los archivos CSV.
- **Preprocesamiento de datos**: Para limpieza y transformación de datos.
- **Entrenamiento de datos**: Modelo predictivo para análisis crediticios
- **Almacenamiento**: Donde se guardarán los datos limpios y estructurados.
- **Documentación**: Diseño técnico completo + planificación.
## Tecnologías utilizadas
- Python 3
- Pandas
- VS Code
- PostgreSQL
- Docker
- Git / GitHub
- GitHub Actions
- Render
## Pipeline implementado
| Etapa | Descripción | 
| 1. Diseño e instalación | Estructura de carpetas, setup del entorno, definición de
herramientas |
| 2. Ingesta | Lectura desde CSV, carga a memoria |
| 3. Limpieza | Eliminación de duplicados, tratamiento de nulos, revisión de tipos |
| 4. Transformación | Creación de variables necesarias. |
| 5. Validación | Revisión de rangos, tipos, coherencia; validación básica |
| 6. Carga en PostgreSQL | Subida del dataset limpio y validado a la base de datos local
| 7. Entrenamiento IA | Clasificación binaria para Default o Pagado |
8
| 8. Evaluación | Métricas como accuracy, recall; revisión de logs de ejecución |
| 9. Visualización | Panel con predicciones |
## Estructura del repositorio
analisis-crediticio/
├── README.md
├── docs/
│ └── diseño_tecnico.pdf
├── scripts/
│ ├── ingesta.py
│ ├── limpieza.py
│ ├── transformacion.py
│ └── entrenamiento.py
├── data/
│ └── loan_data.csv
├── dashboards/
│ └── dashboard_metabase.png
├── docker-compose.yml
