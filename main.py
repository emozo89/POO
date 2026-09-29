"""main.py - Interfaz de Consola e Integración."""

from getpass import getpass

from models import Empleado
from database import (
    inicializar_bd, crear_empleado, obtener_empleados,
    actualizar_empleado, eliminar_empleado
)
from auth import autenticar_usuario
from services import obtener_indicador_economico, obtener_clima_santiago, validar_moneda

def login():
    """Solicita credenciales al usuario y verifica autenticación."""
    print("=== SISTEMA DE GESTIÓN DE EMPLEADOS - ECOTECH SOLUTIONS ===")
    intentos = 0
    while intentos < 3:
        user = input("Usuario: ").strip()
        pwd = getpass("Contraseña: ").strip()
        if autenticar_usuario(user, pwd):
            print(f"\n[OK] Autenticación exitosa. Bienvenido, {user.capitalize()}.\n")
            return True
        else:
            intentos += 1
            print(f"[ACCESO DENEGADO] Intentos restantes: {3 - intentos}\n")
    return False


def menu_principal():
    """Muestra el menu principal y gestiona las opciones del usuario."""
    while True:
        print("=== MENÚ PRINCIPAL ===")
        print("1. Registrar Empleado (CREATE)")
        print("2. Listar Empleados (READ)")
        print("3. Actualizar Empleado (UPDATE)")
        print("4. Eliminar Empleado (DELETE)")
        print("5. Consultar Clima para Proyectos (API)")
        print("6. Consultar Indicador Económico / Salarios (API)")
        print("7. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            print("\n--- REGISTRO DE EMPLEADO ---")
            nombre = input("Nombre completo (ej. Carmen Lopez): ").strip()
            rut = input("RUT: ").strip()
            correo = input("Correo electrónico: ").strip()
            fecha_ing = input("Fecha de ingreso (YYYY-MM-DD): ").strip()
            cargo = input("Cargo: ").strip()
            try:
                salario = float(input("Salario ($): "))
                id_depto = int(input("ID Departamento (ej. 13 - Dev. Sostenible): "))
                if crear_empleado(nombre, rut, correo, fecha_ing, salario, cargo, id_depto):
                    print("[ÉXITO] Empleado guardado en BD.\n")
            except ValueError:
                print("[ERROR] El salario y el ID de departamento deben ser numéricos.\n")

        elif opcion == "2":
            print("\n--- LISTA DE EMPLEADOS (INSTANCIAS POO) ---")
            registros = obtener_empleados()
            if not registros:
                print("No hay empleados registrados.")
            for r in registros:
                # Se instancia cada registro en un objeto Empleado respetando POO
                emp = Empleado(id_empleado=r[0], nombre=r[1], rut=r[2], correo=r[3], fecha_ingreso=r[4], salario=r[5], cargo=r[6])
                print(f"ID:{emp.id_empleado} | Nombre: {emp.nombre} | RUT: {emp.rut} | Cargo: {emp.cargo} | Salario: ${emp.salario}")
            print()

        elif opcion == "3":
            try:
                emp_id = int(input("ID de empleado a actualizar: "))
                nom = input("Nuevo nombre: ").strip()
                correo = input("Nuevo correo: ").strip()
                cargo = input("Nuevo cargo: ").strip()
                salario = float(input("Nuevo salario: "))
                if actualizar_empleado(emp_id, nom, correo, salario, cargo):
                    print("[ÉXITO] Empleado actualizado.\n")
                else:
                    print("[ERROR] ID no encontrado.\n")
            except ValueError:
                print("[ERROR] Entrada numérica inválida.\n")

        elif opcion == "4":
            try:
                emp_id = int(input("ID de empleado a eliminar: "))
                if eliminar_empleado(emp_id):
                    print("[ÉXITO] Registro eliminado de la BD.\n")
                else:
                    print("[ERROR] ID no existente.\n")
            except ValueError:
                print("[ERROR] Ingrese un ID de tipo entero.\n")

        elif opcion == "5":
            print("\n[API] Consultando servicio meteorológico...")

            clima = obtener_clima_santiago()

            if clima["exito"]:
                print("\n--- CLIMA ACTUAL EN SANTIAGO ---")

                print(
                    f"Temperatura: "
                    f"{clima['temperatura']} °C"
                )

                print(
                    f"Humedad: "
                    f"{clima['humedad']} %"
                )

                print(
                    f"Estado del tiempo: "
                    f"{clima['estado']}"
                )

                if clima["viento"] is not None:
                    print(
                        f"Viento: "
                        f"{clima['viento']} km/h"
                    )

                print()

            else:
                print(
                    f"[API ERROR] "
                    f"{clima['mensaje']}\n"
                )

        elif opcion == "6":
            print("\n--- CONSULTA DE INDICADOR ECONÓMICO ---")

            ind = input(
                "Moneda a consultar (dolar, euro, uf): "
            ).strip().lower()

            if not validar_moneda(ind):
                print(
                    "[ERROR] Moneda no válida. "
                    "Ingrese dolar, euro o uf.\n"
                )
                continue

            res = obtener_indicador_economico(ind)

            if res["exito"]:
                print(
                    f"[API] 1 {res['moneda'].upper()} "
                    f"= ${res['valor']} "
                    f"({res['unidad']})\n"
                )

            else:
                print(
                    f"[API ERROR] "
                    f"{res['mensaje']}\n"
                )


if __name__ == "__main__":
    inicializar_bd()

    if login():
        menu_principal()
    else:
        print("[ACCESO BLOQUEADO] Máximo de intentos alcanzado.")
