"""Autenticación segura de usuarios para EcoTech Solutions."""

import hashlib
import hmac


# Cantidad de iteraciones utilizadas para fortalecer el hash
ITERACIONES = 200_000


# Usuarios almacenados únicamente mediante salt + hash.
# Las contraseñas reales NO aparecen en el código.
USUARIOS_DB = {
    "admin": {
        "salt": "d22196c0a262c29d215ebb4e94307d6a",
        "hash": (
            "7a1cddc581ef163d7be71d8793bd39fd"
            "8fbaaa6b7cefc3a73564dcef87c2d899"
        ),
    },
    "gerente": {
        "salt": "89b0668026eab134d8c6fac227a0b233",
        "hash": (
            "bd64e589a4ac572abde9f61135d196cc"
            "cf70bf80ac8a3b42931b96b545d0e01c"
        ),
    },
}


def hashear_password(password: str, salt_hex: str) -> str:
    """Genera un hash seguro de la contraseña utilizando PBKDF2-HMAC-SHA256."""

    salt = bytes.fromhex(salt_hex)

    hash_generado = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERACIONES,
    )

    return hash_generado.hex()


def autenticar_usuario(usuario: str, password_ingresada: str) -> bool:
    """Valida las credenciales ingresadas de forma segura."""

    if not usuario or not password_ingresada:
        return False

    usuario = usuario.strip().lower()

    datos_usuario = USUARIOS_DB.get(usuario)

    if datos_usuario is None:
        return False

    hash_ingresado = hashear_password(
        password_ingresada,
        datos_usuario["salt"],
    )

    return hmac.compare_digest(
        datos_usuario["hash"],
        hash_ingresado,
    )
