import random

from core.data.enemies import ENEMIES
from core.enemy import Enemy


# -------------------------
# FILTROS
# -------------------------

def _filtrar_por_piso(piso):
    enemigos_validos = {}

    for enemy_id, data in ENEMIES.items():
        piso_min = data.get("piso_min", 1)
        piso_max = data.get("piso_max", float("inf"))

        if piso_min <= piso <= piso_max:
            enemigos_validos[enemy_id] = data

    return enemigos_validos


def _filtrar_por_tipo(enemigos, tipo):
    return {
        eid: data for eid, data in enemigos.items()
        if data.get("tipo", "normal") == tipo
    }


def _seleccionar_por_peso(enemigos):
    ids = list(enemigos.keys())
    pesos = [enemigos[e]["peso"] for e in ids]

    return random.choices(ids, weights=pesos, k=1)[0]


# -------------------------
# GENERADOR PRINCIPAL
# -------------------------

def generar_enemigo(piso, tipo="normal"):
    """
    Genera un enemigo según:
    - piso
    - tipo (normal / boss)
    """

    enemigos = _filtrar_por_piso(piso)
    enemigos = _filtrar_por_tipo(enemigos, tipo)

    if not enemigos:
        raise ValueError(f"No hay enemigos tipo '{tipo}' para este piso")

    enemy_id = _seleccionar_por_peso(enemigos)
    data = enemigos[enemy_id]

    enemigo = Enemy(enemy_id, data, piso)

    # -------------------------
    # ESCALADO SIMPLE
    # -------------------------
    enemigo.hp_actual += piso * 5
    enemigo.ataque += piso * 2

    return enemigo


# -------------------------
# GRUPOS (FUTURO)
# -------------------------

def generar_grupo_enemigos(piso, cantidad=1, tipo="normal"):
    return [generar_enemigo(piso, tipo) for _ in range(cantidad)]