# Generador de datos sintéticos de aparcamientos

Proyecto académico de Rodrigo Blaudy Mayoral para Bases de Datos Avanzadas.
Genera seis archivos CSV relacionados para practicar carga y consultas en una
base de datos: clientes, vehículos, plazas, reservas, pagos e incidencias.

## Tecnologías
Python, pandas y Faker con configuración regional española.

## Ejecutar la demostración
Requiere Python 3.10 o posterior.

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python generar_datos.py --salida datos_demo
```

La demostración crea 100 clientes, 150 vehículos, 50 plazas, 300 reservas,
300 pagos y 30 incidencias. Para cambiar el volumen, modifica las constantes
`NUM_*` al comienzo del script. El script no sobrescribe una carpeta con CSV anteriores.

## Relaciones
Los vehículos referencian clientes. Las reservas referencian clientes, vehículos y
plazas. Los pagos y las incidencias referencian reservas.

## Alcance
Los datos son sintéticos y no deben utilizarse para contactar con personas.
Es un generador académico: no comprueba solapamientos de reservas ni que el
cliente de una reserva sea propietario del vehículo. Las fechas son relativas al
momento de ejecución. Aunque se fija una semilla, no se garantiza igualdad entre
fechas de ejecución o versiones distintas de las dependencias.

La versión original estaba configurada para millones de registros y construía
tablas completas en memoria. Esta versión conserva las funciones del proyecto,
pero incluye volúmenes de demostración, carpeta de salida y protección frente
a sobrescritura, añadidos con asistencia de IA al preparar el portfolio.
No incluye datos originales de personas, registros de PostgreSQL ni documentos
con identificadores académicos.
