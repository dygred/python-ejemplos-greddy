import csv
import os

# Archivos de datos
CLIENTES_FILE = 'clientes.csv'
VIAJES_FILE = 'viajes.csv'
RESERVAS_FILE = 'reservas.csv'

def cargar_datos(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        return []
    with open(nombre_archivo, newline='', encoding='utf-8') as archivo:
        return list(csv.DictReader(archivo))

def guardar_datos(nombre_archivo, campo_nombres, datos):
    with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campo_nombres)
        escritor.writeheader()
        escritor.writerows(datos)

def registrar_cliente():
    clientes = cargar_datos(CLIENTES_FILE)
    nombre = input("Nombre del cliente: ")
    email = input("Correo electrónico: ")
    cliente = {"id": str(len(clientes)+1), "nombre": nombre, "email": email}
    clientes.append(cliente)
    guardar_datos(CLIENTES_FILE, ["id", "nombre", "email"], clientes)
    print("✅ Cliente registrado correctamente.\n")

def registrar_viaje():
    viajes = cargar_datos(VIAJES_FILE)
    origen = input("Origen del viaje: ")
    destino = input("Destino del viaje: ")
    fecha = input("Fecha del viaje (YYYY-MM-DD): ")
    precio = input("Precio por persona: ")
    asientos = input("Cantidad de asientos disponibles: ")
    viaje = {
        "id": str(len(viajes)+1),
        "origen": origen,
        "destino": destino,
        "fecha": fecha,
        "precio": precio,
        "asientos": asientos
    }
    viajes.append(viaje)
    guardar_datos(VIAJES_FILE, ["id", "origen", "destino", "fecha", "precio", "asientos"], viajes)
    print("✅ Viaje registrado correctamente.\n")

def mostrar_viajes():
    viajes = cargar_datos(VIAJES_FILE)
    if not viajes:
        print("❌ No hay viajes disponibles.\n")
        return []
    print("\n📅 Viajes disponibles:")
    for viaje in viajes:
        print(f"[{viaje['id']}] {viaje['origen']} → {viaje['destino']} | {viaje['fecha']} | ${viaje['precio']} | Asientos: {viaje['asientos']}")
    print()
    return viajes

def hacer_reserva():
    clientes = cargar_datos(CLIENTES_FILE)
    viajes = mostrar_viajes()
    reservas = cargar_datos(RESERVAS_FILE)

    cliente_id = input("ID del cliente: ")
    viaje_id = input("ID del viaje a reservar: ")

    cliente = next((c for c in clientes if c['id'] == cliente_id), None)
    viaje = next((v for v in viajes if v['id'] == viaje_id), None)

    if not cliente or not viaje:
        print("❌ Cliente o viaje no encontrado.\n")
        return

    if int(viaje['asientos']) < 1:
        print("🚫 No hay asientos disponibles en este viaje.\n")
        return

    viaje['asientos'] = str(int(viaje['asientos']) - 1)
    reserva = {
        "cliente_id": cliente['id'],
        "cliente_nombre": cliente['nombre'],
        "viaje_id": viaje['id'],
        "origen": viaje['origen'],
        "destino": viaje['destino'],
        "fecha": viaje['fecha']
    }
    reservas.append(reserva)

    guardar_datos(VIAJES_FILE, ["id", "origen", "destino", "fecha", "precio", "asientos"], viajes)
    guardar_datos(RESERVAS_FILE, ["cliente_id", "cliente_nombre", "viaje_id", "origen", "destino", "fecha"], reservas)
    print("✅ Reserva realizada con éxito.\n")

def menu():
    while True:
        print("=== SISTEMA DE RESERVAS DE VIAJES ===")
        print("1. Registrar cliente")
        print("2. Registrar viaje")
        print("3. Mostrar viajes disponibles")
        print("4. Hacer reserva")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            registrar_cliente()
        elif opcion == '2':
            registrar_viaje()
        elif opcion == '3':
            mostrar_viajes()
        elif opcion == '4':
            hacer_reserva()
        elif opcion == '5':
            print("¡Gracias por usar el sistema!")
            break
        else:
            print("⚠️ Opción no válida.\n")

if __name__ == "__main__":
    menu()
