import random

from core.data.enemies import ENEMIES
from core.enemy import Enemy


# -------------------------
# UTILIDADES INTERNAS
# -------------------------

def _filtrar_enemigos_por_piso(piso):
    """
    Permite en el futuro limitar enemigos por piso.
    Si no existe restricción, devuelve todos.
    """
    enemigos_validos = {}

    for enemy_id, data in ENEMIES.items():
        piso_min = data.get("piso_min", 1)
        piso_max = data.get("piso_max", float("inf"))

        if piso_min <= piso <= piso_max:
            enemigos_validos[enemy_id] = data

    return enemigos_validos


def _seleccionar_enemigo_por_peso(enemigos_filtrados):
    """
    Selecciona un enemigo usando pesos.
    """
    ids = list(enemigos_filtrados.keys())
    pesos = [enemigos_filtrados[e]["peso"] for e in ids]

    seleccionado = random.choices(ids, weights=pesos, k=1)[0]
    return seleccionado


# -------------------------
# API PÚBLICA
# -------------------------

def generar_enemigo(piso):
    """
    Genera un enemigo basado en el piso actual.
    """
    enemigos_filtrados = _filtrar_enemigos_por_piso(piso)

    if not enemigos_filtrados:
        raise ValueError("No hay enemigos disponibles para este piso")

    enemy_id = _seleccionar_enemigo_por_peso(enemigos_filtrados)
    data = enemigos_filtrados[enemy_id]

    return Enemy(enemy_id, data, piso)


def generar_grupo_enemigos(piso, tamaño_min=1, tamaño_max=3):
    """
    Genera un grupo de enemigos para una habitación.
    """
    cantidad = random.randint(tamaño_min, tamaño_max)

    return [generar_enemigo(piso) for _ in range(cantidad)]


def generar_habitacion(piso):
    """
    Genera una habitación completa.
    Devuelve un diccionario para que UI lo interprete.
    """
    enemigos = generar_grupo_enemigos(piso)

    return {
        "tipo": "combate",
        "enemigos": enemigos
    }


def generar_piso(piso, habitaciones_por_piso=5):
    """
    Genera todas las habitaciones de un piso.
    """
    return [generar_habitacion(piso) for _ in range(habitaciones_por_piso)]


# -------------------------
# EXTENSIÓN FUTURA (PREPARADO)
# -------------------------

def generar_evento(piso):
    """
    Placeholder para eventos futuros:
    - cofres
    - tiendas
    - trampas
    """
    return {
        "tipo": "evento",
        "contenido": None
    }