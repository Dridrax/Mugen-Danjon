def curva_lineal(valor):
    return valor


def curva_panico(valor):
    return valor ** 2


def curva_agresiva(valor):
    return valor ** 0.7


def score_atacar(contexto, stats_enemigo):
    """
    Calcula qué tan buena idea es atacar
    """

    # Consideración 1:
    # A menos HP del jugador, más ganas de atacar
    hp_jugador = contexto["hp"]
    max_hp_jugador = contexto["hp_max"]

    score = 1.0 - (hp_jugador / max_hp_jugador)

    # Consideración 2:
    # Enemigos fuertes son más agresivos
    score += min(stats_enemigo.ataque / 50, 0.4)

    return min(max(score, 0), 1)

def score_defenderse(contexto, stats_enemigo):

    # Consideración 1:
    # ¿Tengo poca vida?
    porcentaje_hp = (
        stats_enemigo.hp_actual /
        stats_enemigo.hp
    )

    utilidad_por_peligro = 1.0 - porcentaje_hp

    # Consideración 2:
    # ¿El jugador prepara algo fuerte?
    bonus_anticipacion = (
        0.5
        if contexto.get("jugador_preparando_especial")
        else 0.0
    )

    score = (
        utilidad_por_peligro * 0.7
    ) + bonus_anticipacion

    return min(max(score, 0), 1)

def score_curar(contexto, enemigo):

    if not contexto.get("puede_curarse", True):
        return 0

    hp_ratio = enemigo.hp_actual / enemigo.hp

    # Si ya está full vida, no curarse
    if hp_ratio >= 1.0:
        return 0

    cantidad_cura = 10

    # Cuánta vida REAL recuperaría
    cura_real = min(cantidad_cura, enemigo.hp - enemigo.hp_actual)

    # Normalizamos respecto a la vida máxima
    valor_cura = cura_real / enemigo.hp

    # Necesidad de curarse
    necesidad = 1.0 - hp_ratio

    score = necesidad * valor_cura

    return min(max(score, 0), 1)