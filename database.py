 # Conexión SQLite y Operaciones CRUD (U2 - Paso 3 y 4)

import sqlite3

DB_NAME = "ecotech.db"

def obtener_conexion():
    """Establece conexión con SQLite activando llaves foráneas para integridad referencial."""
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    except sqlite3.Error as e:
        print(f"[ERROR CRÍTICO] Fallo al conectar a la BD: {e}")
        return None


def inicializar_bd():
    """Crea las tablas según el modelo relacional y la semántica de la empresa."""
    script = """
    CREATE TABLE IF NOT EXISTS departamentos (
        id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_depto TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS empleados (
        id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        rut TEXT UNIQUE NOT NULL,
        correo TEXT NOT NULL,
        fecha_ingreso TEXT NOT NULL,
        salario REAL NOT NULL,
        cargo TEXT NOT NULL,
        id_departamento INTEGER,
        FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento) ON DELETE SET NULL
    );

    CREATE TABLE IF NOT EXISTS proyectos (
        id_proyecto INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_proyecto TEXT NOT NULL UNIQUE,
        fecha_inicio TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS registro_horas (
        id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        hora_entrada TEXT NOT NULL,
        hora_salida TEXT NOT NULL,
        horas_trabajadas INTEGER NOT NULL,
        id_proyecto INTEGER NOT NULL,
        id_empleado INTEGER NOT NULL,
        FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto) ON DELETE CASCADE,
        FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS informes (
        id_informe INTEGER PRIMARY KEY AUTOINCREMENT,
        id_empleado INTEGER NOT NULL,
        id_proyecto INTEGER NOT NULL,
        id_departamento INTEGER NOT NULL,
        FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado),
        FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto),
        FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento)
    );
    """
    conn = obtener_conexion()
    if conn:
        try:
            with conn:
                conn.executescript(script)

            # Poblar datos iniciales si la BD está vacía
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM departamentos;")
            if cursor.fetchone()[0] == 0:
                conn.execute("INSERT INTO departamentos (id_departamento, nombre_depto) VALUES (13, 'Desarrollo Sostenible'), (1, 'RRHH'), (2, 'Ventas'), (3, 'Investigación y Desarrollo');")
                conn.execute("INSERT INTO empleados (id_empleado, nombre, rut, correo, fecha_ingreso, salario, cargo, id_departamento) VALUES (1, 'Carmen Lopez', '11.111.111-1', 'carmen@ecotech.cl', '2022-01-15', 1200000, 'Analista', 13), (2, 'Juan Gomez', '22.222.222-2', 'juan@ecotech.cl', '2023-03-10', 1400000, 'Desarrollador', 13);")
                conn.execute("INSERT INTO proyectos (id_proyecto, nombre_proyecto, fecha_inicio) VALUES (25, 'Campaña verde', '2023-12-13'), (14, 'Evolución sostenible', '2025-08-14');")
        except sqlite3.Error as e:
            print(f"[ERROR BD] Fallo en inicialización: {e}")
        finally:
            conn.close()

# --- OPERACIONES CRUD DE EMPLEADOS ---

def crear_empleado(nombre: str, rut: str, correo: str, fecha_ingreso: str, salario: float, cargo: str, id_depto: int) -> bool:
    """Crea un nuevo empleado guardando primero en Persona y luego en Empleado."""
    conn = obtener_conexion()
    if not conn:
        return False
    try:
        cursor = conn.cursor()

        # 1. Insertar en tabla base Persona
        cursor.execute(
            "INSERT INTO Persona (rut, nombre, correo) VALUES (?, ?, ?);",
            (rut, nombre, correo)
        )

        # 2. Insertar en tabla derivada Empleado
        cursor.execute(
            """INSERT INTO Empleado (rut, fecha_ingreso, salario, cargo, idDepartamento)
               VALUES (?, ?, ?, ?, ?);""",
            (rut, fecha_ingreso, salario, cargo, id_depto)
        )

        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        msg = str(e).lower()
        if "foreign key" in msg:
            print(f"\n[ERROR] El ID de Departamento ({id_depto}) no existe en la base de datos.")
        elif "unique" in msg or "primary key" in msg:
            print(f"\n[ERROR] El RUT '{rut}' ya se encuentra registrado.")
        else:
            print(f"\n[ERROR DE INTEGRIDAD]: {e}")
        conn.rollback()
        return False
    except sqlite3.Error as e:
        print(f"\n[ERROR BD]: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def obtener_empleados() -> list:
    """Obtiene todos los empleados de la base de datos."""
    conn = obtener_conexion()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_empleado, nombre, rut, correo, fecha_ingreso, salario, cargo FROM empleados;")
        return cursor.fetchall()
    finally:
        conn.close()

def actualizar_empleado(id_emp: int, nombre: str, correo: str, salario: float, cargo: str) -> bool:
    """Actualiza la información de un empleado en la base de datos."""
    conn = obtener_conexion()
    if not conn:
        return False
    try:
        with conn:
            cursor = conn.execute(
                "UPDATE empleados SET nombre = ?, correo = ?, salario = ?, cargo = ? WHERE id_empleado = ?;",
                (nombre, correo, salario, cargo, id_emp)
            )
            return cursor.rowcount > 0
    finally:
        conn.close()

def eliminar_empleado(id_emp: int) -> bool:
    """Elimina un empleado de la base de datos."""
    conn = obtener_conexion()
    if not conn:
        return False
    try:
        with conn:
            cursor = conn.execute("DELETE FROM empleados WHERE id_empleado = ?;", (id_emp,))
            return cursor.rowcount > 0
    finally:
        conn.close()
