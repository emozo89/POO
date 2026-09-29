"""Servicios externos utilizados por EcoTech Solutions."""

import requests


# Monedas permitidas para consultas económicas
MONEDAS_PERMITIDAS = {"dolar", "euro", "uf"}


def validar_moneda(moneda: str) -> bool:
    """Valida que la moneda ingresada esté permitida."""

    if not moneda:
        return False

    moneda = moneda.strip().lower()

    return moneda in MONEDAS_PERMITIDAS


def obtener_indicador_economico(moneda: str = "dolar") -> dict:
    """Obtiene el valor actual de un indicador económico."""

    moneda = moneda.strip().lower()

    if not validar_moneda(moneda):
        return {
            "exito": False,
            "mensaje": (
                "Moneda no válida. "
                "Las opciones permitidas son: dolar, euro o uf."
            ),
        }

    url = f"https://mindicador.cl/api/{moneda}"

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()

            serie = data.get("serie")
            unidad = data.get("unidad_medida")

            if not serie or unidad is None:
                return {
                    "exito": False,
                    "mensaje": "La API entregó datos incompletos.",
                }

            valor = serie[0].get("valor")

            if valor is None:
                return {
                    "exito": False,
                    "mensaje": "No se encontró el valor del indicador.",
                }

            return {
                "exito": True,
                "moneda": moneda,
                "valor": valor,
                "unidad": unidad,
            }

        if response.status_code == 404:
            return {
                "exito": False,
                "mensaje": (
                    f"Indicador '{moneda}' no encontrado "
                    "(HTTP 404)."
                ),
            }

        return {
            "exito": False,
            "mensaje": (
                "Error del servidor externo "
                f"(HTTP {response.status_code})."
            ),
        }

    except requests.exceptions.Timeout:
        return {
            "exito": False,
            "mensaje": (
                "Tiempo de espera agotado al conectar "
                "con el servidor."
            ),
        }

    except requests.exceptions.RequestException:
        return {
            "exito": False,
            "mensaje": (
                "No fue posible conectarse al "
                "servicio económico."
            ),
        }

    except (ValueError, TypeError, KeyError, IndexError):
        return {
            "exito": False,
            "mensaje": (
                "La respuesta del servicio económico "
                "tiene un formato inesperado."
            ),
        }


def interpretar_codigo_clima(codigo: int) -> str:
    """Convierte un código meteorológico WMO en una descripción."""

    estados = {
        0: "Despejado",
        1: "Principalmente despejado",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Niebla",
        48: "Niebla con escarcha",
        51: "Llovizna ligera",
        53: "Llovizna moderada",
        55: "Llovizna intensa",
        56: "Llovizna helada ligera",
        57: "Llovizna helada intensa",
        61: "Lluvia ligera",
        63: "Lluvia moderada",
        65: "Lluvia intensa",
        66: "Lluvia helada ligera",
        67: "Lluvia helada intensa",
        71: "Nevada ligera",
        73: "Nevada moderada",
        75: "Nevada intensa",
        77: "Granos de nieve",
        80: "Chubascos ligeros",
        81: "Chubascos moderados",
        82: "Chubascos intensos",
        85: "Chubascos de nieve ligeros",
        86: "Chubascos de nieve intensos",
        95: "Tormenta",
        96: "Tormenta con granizo ligero",
        99: "Tormenta con granizo intenso",
    }

    return estados.get(codigo, "Estado meteorológico desconocido")


def obtener_clima_santiago() -> dict:
    """Obtiene las condiciones meteorológicas actuales de Santiago."""

    url = "https://api.open-meteo.com/v1/forecast"

    parametros = {
        "latitude": -33.45,
        "longitude": -70.66,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "weather_code,"
            "wind_speed_10m"
        ),
        "timezone": "America/Santiago",
    }

    try:
        response = requests.get(
            url,
            params=parametros,
            timeout=5,
        )

        if response.status_code != 200:
            return {
                "exito": False,
                "mensaje": (
                    "Error del servicio meteorológico "
                    f"(HTTP {response.status_code})."
                ),
            }

        data = response.json()

        datos_actuales = data.get("current")

        if not isinstance(datos_actuales, dict):
            return {
                "exito": False,
                "mensaje": (
                    "La API meteorológica entregó "
                    "datos incompletos."
                ),
            }

        temperatura = datos_actuales.get("temperature_2m")
        humedad = datos_actuales.get("relative_humidity_2m")
        codigo_clima = datos_actuales.get("weather_code")
        viento = datos_actuales.get("wind_speed_10m")

        if (
            temperatura is None
            or humedad is None
            or codigo_clima is None
        ):
            return {
                "exito": False,
                "mensaje": (
                    "No fue posible obtener todos los "
                    "datos meteorológicos requeridos."
                ),
            }

        estado = interpretar_codigo_clima(
            int(codigo_clima)
        )

        return {
            "exito": True,
            "temperatura": temperatura,
            "humedad": humedad,
            "estado": estado,
            "viento": viento,
        }

    except requests.exceptions.Timeout:
        return {
            "exito": False,
            "mensaje": (
                "El servicio meteorológico tardó "
                "demasiado en responder."
            ),
        }

    except requests.exceptions.RequestException:
        return {
            "exito": False,
            "mensaje": (
                "No fue posible conectarse al "
                "servicio meteorológico."
            ),
        }

    except (ValueError, TypeError, KeyError):
        return {
            "exito": False,
            "mensaje": (
                "La respuesta meteorológica tiene "
                "un formato inesperado."
            ),
        }
