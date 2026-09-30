"""models.py - Definición de Clases y Modelos de Datos."""

from datetime import datetime

class Persona:
    """Clase base (Superclase) que abstrae las características de una persona."""

    def __init__(self, nombre: str, rut: str, correo: str):
        self.nombre = nombre
        self._rut = rut
        self.correo = correo

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
    """Clase derivada que hereda de Persona e incorpora atributos laborales."""

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
        # Inicialización de los atributos heredados desde Persona
        super().__init__(
            nombre=nombre,
            rut=rut,
            correo=correo
        )

        # Atributos propios encapsulados de Empleado
        self._id_empleado = id_empleado
        self._fecha_ingreso = fecha_ingreso
        self._salario = salario
        self._cargo = cargo

    @property
    def id_empleado(self) -> int:
        """Devuelve el ID del empleado."""
        return self._id_empleado

    @property
    def fecha_ingreso(self) -> str:
        """Devuelve la fecha de ingreso del empleado."""
        return self._fecha_ingreso

    @fecha_ingreso.setter
    def fecha_ingreso(self, nueva_fecha: str):
        """Modifica la fecha de ingreso del empleado."""
        self._fecha_ingreso = nueva_fecha

    @property
    def salario(self) -> float:
        """Devuelve el salario del empleado."""
        return self._salario

    @salario.setter
    def salario(self, nuevo_salario: float):
        """Modifica el salario del empleado."""
        self._salario = nuevo_salario

    @property
    def cargo(self) -> str:
        """Devuelve el cargo del empleado."""
        return self._cargo

    @cargo.setter
    def cargo(self, nuevo_cargo: str):
        """Modifica el cargo del empleado."""
        self._cargo = nuevo_cargo

class Departamento:
    """Representa un departamento de EcoTech Solutions."""

    def __init__(self, id_departamento: int, nombre: str):
        self._id_departamento = id_departamento
        self._nombre = nombre

    @property
    def id_departamento(self):
        """Devuelve el ID del departamento."""
        return self._id_departamento

    @property
    def nombre(self):
        """Devuelve el nombre del departamento."""
        return self._nombre

class Proyecto:
    """Identifica un proyecto en curso con su fecha de inicio."""

    def __init__(
        self,
        id_proyecto: int,
        nombre_proyecto: str,
        fecha_inicio: str
    ):
        self.id_proyecto = id_proyecto
        self.nombre_proyecto = nombre_proyecto
        self.fecha_inicio = fecha_inicio
        self._empleados: list[Empleado] = []

    def asignar_empleado(self, empleado: Empleado) -> str:
        """Asigna un empleado al proyecto."""

        if empleado not in self._empleados:
            self._empleados.append(empleado)

            return (
                f"Empleado {empleado.nombre} asignado al proyecto "
                f"{self.nombre_proyecto}."
            )

        return (
            f"El empleado {empleado.nombre} ya está asignado al proyecto "
            f"{self.nombre_proyecto}."
        )

    def desasignar_empleado(self, empleado: Empleado) -> str:
        """Desasigna un empleado del proyecto."""

        if empleado in self._empleados:
            self._empleados.remove(empleado)

            return (
                f"Empleado {empleado.nombre} removido del proyecto "
                f"{self.nombre_proyecto}."
            )

        return (
            f"El empleado {empleado.nombre} no está asignado al proyecto "
            f"{self.nombre_proyecto}."
        )

    @property
    def empleados(self) -> list[Empleado]:
        """Devuelve una copia de los empleados asignados al proyecto."""
        return self._empleados.copy()


class RegistroHoras:
    """Trazabilidad de horas trabajadas por empleado y proyecto asignado."""

    def __init__(
        self,
        id_registro: int,
        id_empleado: int,
        id_proyecto: int,
        horas_trabajadas: int,
        fecha: str = None,
        hora_entrada: str = "09:00",
        hora_salida: str = "18:00"
    ):
        self._id_registro = id_registro
        self._id_empleado = id_empleado
        self._id_proyecto = id_proyecto
        self._horas_trabajadas = horas_trabajadas
        self._fecha = fecha or datetime.now().strftime("%Y-%m-%d")
        self._hora_entrada = hora_entrada
        self._hora_salida = hora_salida

    @property
    def id_registro(self) -> int:
        """Devuelve el ID del registro."""
        return self._id_registro

    @property
    def id_empleado(self) -> int:
        """Devuelve el ID del empleado asociado."""
        return self._id_empleado

    @property
    def id_proyecto(self) -> int:
        """Devuelve el ID del proyecto asociado."""
        return self._id_proyecto

    @property
    def horas_trabajadas(self) -> int:
        """Devuelve las horas trabajadas."""
        return self._horas_trabajadas

    @horas_trabajadas.setter
    def horas_trabajadas(self, nuevas_horas: int):
        """Modifica las horas trabajadas."""
        self._horas_trabajadas = nuevas_horas

    @property
    def fecha(self) -> str:
        """Devuelve la fecha del registro."""
        return self._fecha

    @property
    def hora_entrada(self) -> str:
        """Devuelve la hora de entrada."""
        return self._hora_entrada

    @property
    def hora_salida(self) -> str:
        """Devuelve la hora de salida."""
        return self._hora_salida

    def registrar_horas(self) -> str:
        """Registra las horas trabajadas y devuelve un mensaje de confirmación."""
        return (
            f"Registradas {self.horas_trabajadas} hrs "
            f"para empleado ID {self.id_empleado} "
            f"en proyecto ID {self.id_proyecto}."
        )

    def consultar_horas(self) -> int:
        """Devuelve la cantidad de horas trabajadas registradas."""
        return self.horas_trabajadas


class Informe:
    """Información consolidada generada a solicitud de las partes interesadas."""

    def __init__(
        self,
        id_informe: int,
        id_empleado: int,
        id_proyecto: int,
        id_departamento: int,
        reporte_horas: str = "",
        reporte_proyecto: str = "",
        reporte_empleado: str = ""
    ):
        self._id_informe = id_informe
        self._id_empleado = id_empleado
        self._id_proyecto = id_proyecto
        self._id_departamento = id_departamento
        self._reporte_horas = reporte_horas
        self._reporte_proyecto = reporte_proyecto
        self._reporte_empleado = reporte_empleado

    @property
    def id_informe(self) -> int:
        """Devuelve el ID del informe."""
        return self._id_informe

    @property
    def id_empleado(self) -> int:
        """Devuelve el ID del empleado asociado."""
        return self._id_empleado

    @property
    def id_proyecto(self) -> int:
        """Devuelve el ID del proyecto asociado."""
        return self._id_proyecto

    @property
    def id_departamento(self) -> int:
        """Devuelve el ID del departamento asociado."""
        return self._id_departamento

    @property
    def reporte_horas(self) -> str:
        """Devuelve el reporte de horas."""
        return self._reporte_horas

    @reporte_horas.setter
    def reporte_horas(self, nuevo_reporte: str):
        """Modifica el reporte de horas."""
        self._reporte_horas = nuevo_reporte

    @property
    def reporte_proyecto(self) -> str:
        """Devuelve el reporte del proyecto."""
        return self._reporte_proyecto

    @reporte_proyecto.setter
    def reporte_proyecto(self, nuevo_reporte: str):
        """Modifica el reporte del proyecto."""
        self._reporte_proyecto = nuevo_reporte

    @property
    def reporte_empleado(self) -> str:
        """Devuelve el reporte del empleado."""
        return self._reporte_empleado

    @reporte_empleado.setter
    def reporte_empleado(self, nuevo_reporte: str):
        """Modifica el reporte del empleado."""
        self._reporte_empleado = nuevo_reporte

    def generar_reporte(self) -> str:
        """Genera un resumen del informe."""
        return (
            f"Informe #{self.id_informe} "
            f"[Empleado: {self.id_empleado}, "
            f"Proyecto: {self.id_proyecto}, "
            f"Depto: {self.id_departamento}]"
        )
