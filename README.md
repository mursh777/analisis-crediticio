# Predicción de Riesgos Crediticios
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
| Etapa | Descripción | <br>
| 1. Diseño e instalación | Estructura de carpetas, setup del entorno, definición de
herramientas | <br>
| 2. Ingesta | Lectura desde CSV, carga a memoria | <br>
| 3. Limpieza | Eliminación de duplicados, tratamiento de nulos, revisión de tipos | <br>
| 4. Transformación | Creación de variables necesarias. | <br>
| 5. Validación | Revisión de rangos, tipos, coherencia; validación básica | <br>
| 6. Carga en PostgreSQL | Subida del dataset limpio y validado a la base de datos local | <br>
| 7. Entrenamiento IA | Clasificación binaria para Default o Pagado | <br>
| 8. Evaluación | Métricas como accuracy, recall; revisión de logs de ejecución | <br>
| 9. Visualización | Panel con predicciones | <br>
## Estructura del repositorio
analisis-crediticio/ <br>
├── README.md<br>
├── docs/<br>
│ └── diseño_tecnico.pdf<br>
├── scripts/<br>
│ ├── ingesta.py<br>
│ ├── limpieza.py<br>
│ ├── transformacion.py<br>
│ └── entrenamiento.py<br>
├── data/<br>
│ └── loan_data.csv<br>
├── dashboards/<br>
│ └── dashboard_metabase.png<br>
├── docker-compose.yml<br>
