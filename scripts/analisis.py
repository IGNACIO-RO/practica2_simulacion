import pandas as pd
import numpy as np

# 1. Cargar archivo Excel usando pd.read_excel
PATH_DATOS = '../datos/datos.xlsx'
df = pd.read_excel(PATH_DATOS)

# 2. Selección de la variable de estudio
variable_analisis = 'tiempo_atencion_min'
serie_tiempos = df[variable_analisis]

# 3. Cálculo de estadísticos descriptivos
resumen_estadistico = {
    "n": int(serie_tiempos.count()),
    "media": serie_tiempos.mean(),
    "mediana": serie_tiempos.median(),
    "moda": serie_tiempos.mode().iloc[0],
    "desv_std": serie_tiempos.std(ddof=1),
    "varianza": serie_tiempos.var(ddof=1),
    "min": serie_tiempos.min(),
    "max": serie_tiempos.max(),
    "q1": serie_tiempos.quantile(0.25),
    "q3": serie_tiempos.quantile(0.75),
}
resumen_estadistico["iqr"] = resumen_estadistico["q3"] - resumen_estadistico["q1"]

# 4. Identificación de outliers con Z-Score (|Z| > 3)
media_p = resumen_estadistico["media"]
std_p = resumen_estadistico["desv_std"]

df['z_score'] = (df[variable_analisis] - media_p) / std_p
filtro_outliers = df['z_score'].abs() > 3.0
outliers_df = df[filtro_outliers]

# 5. Salida de resultados en pantalla
print("┌" + "─" * 45 + "┐")
print("│     ESTADÍSTICAS DEL SISTEMA DE ATENCIÓN    │")
print("├" + "─" * 45 + "┤")
print(f"│ Muestra (n)          : {resumen_estadistico['n']:>20} │")
print(f"│ Media                : {resumen_estadistico['media']:>17.2f} min │")
print(f"│ Mediana              : {resumen_estadistico['mediana']:>17.2f} min │")
print(f"│ Moda                 : {resumen_estadistico['moda']:>17.2f} min │")
print(f"│ Desviación Estándar  : {resumen_estadistico['desv_std']:>17.2f} min │")
print(f"│ Varianza             : {resumen_estadistico['varianza']:>16.2f} min²│")
print(f"│ Mínimo               : {resumen_estadistico['min']:>17.2f} min │")
print(f"│ Máximo               : {resumen_estadistico['max']:>17.2f} min │")
print(f"│ Cuartil 1 (Q1)       : {resumen_estadistico['q1']:>17.2f} min │")
print(f"│ Cuartil 3 (Q3)       : {resumen_estadistico['q3']:>17.2f} min │")
print(f"│ Rango Intercuartil   : {resumen_estadistico['iqr']:>17.2f} min │")
print("└" + "─" * 45 + "┘\n")

print("=== DETECCIÓN DE VALORES ATÍPICOS (|Z| > 3.0) ===")
if not outliers_df.empty:
    print(outliers_df[['id_cliente', variable_analisis, 'z_score']].to_string(index=False))
else:
    print("No se encontraron registros atípicos bajo el criterio Z-Score > 3.")