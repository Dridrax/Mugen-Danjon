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

def crear_resultado(victoria, salir=False, loot=None):
    return {
        "victoria": victoria,
        "salir": salir,
        "loot": loot or []
    }


# -------------------------
# LÓGICA DE COMBATE
# -------------------------

def procesar_turno_jugador(jugador, enemigo, accion):
    """
    Procesa acción del jugador y devuelve:
    - daño hecho
    - si esquiva o no
    - si quiere salir
    """

    if accion == ACCION_ATACAR:
        dano = max(
            0,
            jugador.get_ataque() - enemigo.defensa + random.randint(-2, 2)
        )

        enemigo.hp_actual -= dano
        return {"tipo": "ataque", "dano": dano}

    elif accion == ACCION_ESQUIVAR:
        exito = random.random() < 0.5
        return {"tipo": "esquivar", "exito": exito}

    elif accion == ACCION_SALIR:
        return {"tipo": "salir"}

    return {"tipo": "invalido"}


def procesar_turno_enemigo(jugador, enemigo):
    """
    El enemigo ataca al jugador
    """

    dano = max(
        0,
        enemigo.ataque - jugador.get_defensa() + random.randint(-2, 2)
    )

    jugador.recibir_dano(dano)

    return {
        "dano": dano
    }


# -------------------------
# LOOP PRINCIPAL DE COMBATE
# -------------------------

def combate(jugador, enemigo, acciones_jugador):
    """
    acciones_jugador = lista de acciones predefinidas desde UI
    (la UI decide input, aquí solo se procesa)
    """

    historial = []
    loot = []

    i = 0

    while jugador.esta_vivo() and enemigo.esta_vivo():

        # -------------------------
        # TURNO JUGADOR
        # -------------------------

        if i < len(acciones_jugador):
            accion = acciones_jugador[i]
        else:
            accion = ACCION_ATACAR  # fallback seguro

        resultado_jugador = procesar_turno_jugador(jugador, enemigo, accion)
        historial.append(resultado_jugador)

        # SALIR DEL JUEGO
        if resultado_jugador["tipo"] == "salir":
            return crear_resultado(False, salir=True)

        # ESQUIVAR
        if resultado_jugador["tipo"] == "esquivar":
            if not resultado_jugador["exito"]:
                # si falla esquiva, enemigo ataca igual
                resultado_enemigo = procesar_turno_enemigo(jugador, enemigo)
                historial.append({"enemigo": resultado_enemigo})

        # ATAQUE NORMAL → enemigo responde si sigue vivo
        if enemigo.esta_vivo():
            resultado_enemigo = procesar_turno_enemigo(jugador, enemigo)
            historial.append({"enemigo": resultado_enemigo})

        i += 1

    # -------------------------
    # FINAL DEL COMBATE
    # -------------------------

    if jugador.esta_vivo():
        loot = enemigo.generar_drop()

        # aplicar loot automáticamente al jugador
        for item in loot:
            if item.tipo == "moneda":
                jugador.agregar_oro(item.valor)
            else:
                jugador.agregar_item(item)

        return crear_resultado(True, loot=loot)

    return crear_resultado(False)