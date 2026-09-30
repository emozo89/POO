"""Funciones de validación para los datos ingresados por el usuario."""

import re
from datetime import datetime


def validar_nombre(nombre: str) -> bool:
    """Valida que el nombre no esté vacío."""

    if not nombre:
        return False

    return bool(nombre.strip())


def validar_correo(correo: str) -> bool:
    """Valida el formato básico del correo electrónico."""

    if not correo:
        return False

    patron = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return bool(re.match(patron, correo.strip()))


def validar_fecha(fecha: str) -> bool:
    """Valida que la fecha exista y utilice el formato YYYY-MM-DD."""

    if not fecha:
        return False

    try:
        datetime.strptime(fecha.strip(), "%Y-%m-%d")
        return True

    except ValueError:
        return False


def validar_salario(salario: float) -> bool:
    """Valida que el salario sea mayor que cero."""

    return salario > 0


def validar_cargo(cargo: str) -> bool:
    """Valida que el cargo no esté vacío."""

    if not cargo:
        return False

    return bool(cargo.strip())
