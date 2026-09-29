"""models.py - Definición de Clases y Modelos de Datos."""

from datetime import datetime

class Persona:
    """Clase base (Superclase) que abstrae las características de una persona."""
    
    def __init__(self, nombre: str, rut: str, correo: str):
        self._nombre = nombre
        self._rut = rut
        self._correo = correo

    # --- Getters y Setters con Encapsulamiento ---
    @property
    def nombre(self) -> str:
        """Devuelve el nombre de la persona."""
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre: str):
        if not nuevo_nombre or not nuevo_nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = nuevo_nombre.strip()

    @property
    def rut(self) -> str:
        """Devuelve el RUT de la persona."""
        return self._rut

    @property
    def correo(self) -> str:
        """Devuelve el correo de la persona."""
        return self._correo

    @correo.setter
    def correo(self, nuevo_correo: str):
        self._correo = nuevo_correo


class Empleado(Persona):
    """Clase derivada (Subclase) que hereda de Persona e incorpora atributos laborales."""
    
    def __init__(
        self, 
        id_empleado: int, 
        nombre: str, 
        rut: str, 
        correo: str, 
        fecha_ingreso: str = None, 
        salario: float = 0.0, 
        cargo: str = None
    ):
        # Delegate a la superclase Persona la inicialización de atributos personales
        super().__init__(nombre=nombre, rut=rut, correo=correo)
        
        # Atributos propios de Empleado
        self._id_empleado = id_empleado
        self.fecha_ingreso = fecha_ingreso
        self.salario = salario
        self.cargo = cargo

    @property
    def id_empleado(self) -> int:
        """Devuelve el ID del empleado."""
        return self._id_empleado

class Proyecto:
    """Identifica un proyecto en curso con su fecha de inicio."""
    def __init__(self, id_proyecto: int, nombre_proyecto: str, fecha_inicio: str):
        self.id_proyecto = id_proyecto
        self.nombre_proyecto = nombre_proyecto
        self.fecha_inicio = fecha_inicio

    def asignar_empleado(self, empleado: Empleado) -> str:
        """Asigna un empleado al proyecto y devuelve un mensaje de confirmación."""
        return f"Empleado {empleado.nombre} asignado al proyecto {self.nombre_proyecto}."

    def desasignar_empleado(self, empleado: Empleado) -> str:
        """Desasigna un empleado del proyecto y devuelve un mensaje de confirmación."""
        return f"Empleado {empleado.nombre} removido del proyecto {self.nombre_proyecto}."


class RegistroHoras:
    """Trazabilidad de horas trabajadas por empleado y proyecto asignado."""
    def __init__(self, id_registro: int, id_empleado: int, id_proyecto: int, horas_trabajadas: int, fecha: str = None, hora_entrada: str = "09:00", hora_salida: str = "18:00"):
        self.id_registro = id_registro
        self.id_empleado = id_empleado
        self.id_proyecto = id_proyecto
        self.horas_trabajadas = horas_trabajadas
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d")
        self.hora_entrada = hora_entrada
        self.hora_salida = hora_salida

    def registrar_horas(self) -> str:
        """Registra las horas trabajadas y devuelve un mensaje de confirmación."""
        return f"Registradas {self.horas_trabajadas} hrs para empleado ID {self.id_empleado} en proyecto ID {self.id_proyecto}."

    def consultar_horas(self) -> int:
        """Devuelve la cantidad de horas trabajadas registradas."""
        return self.horas_trabajadas


class Informe:
    """Información consolidada generada a solicitud de las partes interesadas."""
    def __init__(self, id_informe: int, id_empleado: int, id_proyecto: int, id_departamento: int, reporte_horas: str = "", reporte_proyecto: str = "", reporte_empleado: str = ""):
        self.id_informe = id_informe
        self.id_empleado = id_empleado
        self.id_proyecto = id_proyecto
        self.id_departamento = id_departamento
        self.reporte_horas = reporte_horas
        self.reporte_proyecto = reporte_proyecto
        self.reporte_empleado = reporte_empleado

    def generar_reporte(self) -> str:
        """Genera un resumen del informe y devuelve un mensaje de confirmación."""
        return f"Informe #{self.id_informe} [Empleado: {self.id_empleado}, Proyecto: {self.id_proyecto}, Depto: {self.id_departamento}]"
    