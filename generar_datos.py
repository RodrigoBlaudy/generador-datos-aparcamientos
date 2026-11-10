import pandas as pd
import random
from faker import Faker
import string
from datetime import datetime, timedelta

fake = Faker('es_ES')

# CONFIGURACIÓN DE CANTIDADES
NUM_CLIENTES = 100
NUM_VEHICULOS = 150
NUM_PLAZAS = 50
NUM_RESERVAS = 300
NUM_INCIDENCIAS = 30

# DATOS BASE
provincias = [
    "Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza", "Málaga", "Murcia", "Palma",
    "Las Palmas", "Bilbao", "Alicante", "Córdoba", "Valladolid", "Vigo", "Gijón", "Hospitalet"
]
colores = ["Negro", "Blanco", "Rojo", "Azul", "Gris", "Verde", "Amarillo", "Beige", "Marrón", "Naranja"]
metodos_pago = ["Efectivo", "Tarjeta de crédito", "Tarjeta de débito", "PayPal", "Bizum", "Transferencia"]
estados_incidencia = ["nueva", "abierta", "en proceso", "resuelta", "cerrada"]

# FUNCIONES DE GENERACIÓN
def generar_clientes(n):
    for i in range(1, n + 1):
        yield {
            'clienteid': i,
            'nombre': fake.first_name(),
            'apellido': fake.last_name(),
            'email': fake.email(),
            'telefono': fake.random_number(digits=9, fix_len=True),
            'provincia': random.choice(provincias)
        }

def generar_vehiculos(n, num_clientes):
    marcas = [f"Marca{i}" for i in range(1, 501)]
    modelos_por_marca = {marca: [f"{marca}_M{j}" for j in range(1, random.randint(5, 20))] for marca in marcas}
    for i in range(1, n + 1):
        marca = random.choice(marcas)
        yield {
            'vehiculoid': i,
            'matricula': ''.join(random.choices(string.ascii_uppercase, k=4)) + str(random.randint(1000, 9999)),
            'marca': marca,
            'modelo': random.choice(modelos_por_marca[marca]),
            'color': random.choice(colores),
            'clienteid': random.randint(1, num_clientes)
        }

def generar_plazas(n):
    for i in range(1, n + 1):
        yield {
            'plazaid': i,
            'numero': i,
            'nivel': random.randint(-10, 0),
            'seccion': random.choice(list("ABCDEF"))
        }

def generar_reservas(n, num_clientes, num_vehiculos, num_plazas):
    for i in range(1, n + 1):
        dias_estancia = random.randint(1, 10)
        fechaini = fake.date_time_between(start_date='-1y', end_date='now')
        fechafin = fechaini + timedelta(days=dias_estancia)
        yield {
            'reservaid': i,
            'fechainicio': fechaini,
            'fechafin': fechafin,
            'vehiculoid': random.randint(1, num_vehiculos),
            'plazaid': random.randint(1, num_plazas),
            'clienteid': random.randint(1, num_clientes)
        }

def generar_pagos(n, reservas):
    for r in reservas:
        horas = (r['fechafin'] - r['fechainicio']).total_seconds() // 3600
        yield {
            'pagoid': r['reservaid'],
            'cantidad': horas * 3,
            'fechapago': r['fechainicio'] - timedelta(days=random.randint(1, 3)),
            'metodopago': random.choice(metodos_pago),
            'reservaid': r['reservaid']
        }

def generar_incidencias(n, num_reservas):
    for i in range(1, n + 1):
        yield {
            'incidenciaid': i,
            'descripcion': fake.sentence(nb_words=6),
            'fechacread': fake.date_time_between(start_date='-1y', end_date='now'),
            'estado': random.choice(estados_incidencia),
            'reservaid': random.randint(1, num_reservas)
        }

# GENERACIÓN Y GUARDADO
def generar_datos(salida):
    print("Generando clientes...")
    clientes = pd.DataFrame(generar_clientes(NUM_CLIENTES))
    clientes.to_csv(salida / "clientes.csv", index=False)

    print("Generando vehículos...")
    vehiculos = pd.DataFrame(generar_vehiculos(NUM_VEHICULOS, NUM_CLIENTES))
    vehiculos.to_csv(salida / "vehiculos.csv", index=False)

    print("Generando plazas...")
    plazas = pd.DataFrame(generar_plazas(NUM_PLAZAS))
    plazas.to_csv(salida / "plazas.csv", index=False)

    print("Generando reservas...")
    reservas_list = list(generar_reservas(NUM_RESERVAS, NUM_CLIENTES, NUM_VEHICULOS, NUM_PLAZAS))
    reservas = pd.DataFrame(reservas_list)
    reservas.to_csv(salida / "reservas.csv", index=False)

    print("Generando pagos...")
    pagos = pd.DataFrame(generar_pagos(NUM_RESERVAS, reservas_list))
    pagos.to_csv(salida / "pagos.csv", index=False)

    print("Generando incidencias...")
    incidencias = pd.DataFrame(generar_incidencias(NUM_INCIDENCIAS, NUM_RESERVAS))
    incidencias.to_csv(salida / "incidencias.csv", index=False)

    print("¡Todos los datos han sido generados!")

if __name__ == "__main__":
    import argparse
    from pathlib import Path
    parser = argparse.ArgumentParser(description="Generador académico de datos sintéticos de aparcamientos")
    parser.add_argument("--salida", type=Path, default=Path("datos_demo"))
    args = parser.parse_args()
    args.salida.mkdir(parents=True, exist_ok=True)
    archivos = ["clientes", "vehiculos", "plazas", "reservas", "pagos", "incidencias"]
    if any((args.salida / (nombre + ".csv")).exists() for nombre in archivos):
        parser.error("La carpeta contiene CSV de una ejecución anterior; elige otra carpeta.")
    random.seed(42)
    Faker.seed(42)
    generar_datos(args.salida)
