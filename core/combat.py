import random


# -------------------------
# ACCIONES DEL JUGADOR
# -------------------------

ACCION_ATACAR = "atacar"
ACCION_ESQUIVAR = "esquivar"
ACCION_SALIR = "salir"


# -------------------------
# RESULTADO DE COMBATE
# -------------------------

def crear_resultado(victoria, salir=False, loot=None, log=None):
    return {
        "victoria": victoria,
        "salir": salir,
        "loot": loot or [],
        "log": log or []
    }


# -------------------------
# UTILIDADES
# -------------------------

def calcular_ataque(ataque, defensa):
    base = ataque - defensa
    variacion = random.randint(-2, 2)
    return max(0, base + variacion)


def check_crit():
    return random.random() < 0.2  # 20%


def check_miss():
    return random.random() < 0.1  # 10%


# -------------------------
# TURNOS
# -------------------------

def turno_jugador(jugador, enemigo, accion, log):
    if accion == ACCION_SALIR:
        log.append({
            "type": "info",
            "text": "Huyes del combate..."
        })
        return "salir"

    if accion == ACCION_ESQUIVAR:
        exito = random.random() < 0.5

        if exito:
            log.append({
                "type": "dodge",
                "text": "¡Esquivas el próximo ataque!"
            })
            return "dodge_success"
        else:
            log.append({
                "type": "miss",
                "text": "Fallaste la esquiva..."
            })
            return "dodge_fail"

    # -------------------------
    # ATAQUE
    # -------------------------

    if check_miss():
        log.append({
            "type": "miss",
            "text": "¡Tu ataque falla!"
        })
        return "continue"

    dano = calcular_ataque(jugador.get_ataque(), enemigo.defensa)

    if check_crit():
        dano *= 2
        enemigo.hp_actual -= dano

        log.append({
            "type": "crit",
            "text": f"💥 ¡CRÍTICO! Haces {dano} de daño",
            "value": dano
        })
    else:
        enemigo.hp_actual -= dano

        log.append({
            "type": "damage",
            "text": f"Haces {dano} de daño",
            "value": dano
        })

    return "continue"


def turno_enemigo(jugador, enemigo, esquivado, log):
    if esquivado:
        log.append({
            "type": "dodge",
            "text": "Evitas el ataque del enemigo"
        })
        return

    if check_miss():
        log.append({
            "type": "miss",
            "text": "El enemigo falla su ataque"
        })
        return

    dano = calcular_ataque(enemigo.ataque, jugador.get_defensa())

    if check_crit():
        dano *= 2
        jugador.recibir_dano(dano)

        log.append({
            "type": "crit",
            "text": f"💀 ¡CRÍTICO enemigo! Recibes {dano} de daño",
            "value": dano
        })
    else:
        jugador.recibir_dano(dano)

        log.append({
            "type": "damage",
            "text": f"El enemigo hace {dano} de daño",
            "value": dano
        })


# -------------------------
# COMBATE (1 TURNO POR LLAMADA)
# -------------------------

def combate(jugador, enemigo, acciones_jugador):

    log = []
    loot = []

    accion = acciones_jugador[0] if acciones_jugador else ACCION_ATACAR

    # -------------------------
    # TURNO JUGADOR
    # -------------------------

    resultado = turno_jugador(jugador, enemigo, accion, log)

    if resultado == "salir":
        return crear_resultado(False, salir=True, log=log)

    # -------------------------
    # TURNO ENEMIGO
    # -------------------------

    if enemigo.esta_vivo():
        esquivado = (resultado == "dodge_success")
        turno_enemigo(jugador, enemigo, esquivado, log)

    # -------------------------
    # FINAL DEL COMBATE
    # -------------------------

    if not enemigo.esta_vivo():
        loot = enemigo.generar_drop()

        for item in loot:
            if item.tipo == "moneda":
                jugador.agregar_oro(item.valor)
            else:
                jugador.agregar_item(item)

        log.append({
            "type": "info",
            "text": "Has derrotado al enemigo"
        })

        return crear_resultado(True, loot=loot, log=log)

    if not jugador.esta_vivo():
        log.append({
            "type": "info",
            "text": "Has sido derrotado..."
        })

        return crear_resultado(False, log=log)

    return crear_resultado(False, log=log)