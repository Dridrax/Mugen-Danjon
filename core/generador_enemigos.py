import random
from core.enemy import Enemigo
from core.data.enemies import ENEMIES

def generar_encuentro(piso_actual, cantidad_enemigos=2):
    """
    Selecciona enemigos del diccionario basándose en su peso 
    y devuelve una lista de objetos Enemigo instanciados.
    """
    ids_disponibles = list(ENEMIES.keys())
    pesos = [ENEMIES[eid].get("peso",10) for eid in ids_disponibles]

    #Elegimos los IDs al azar según el peso
    seleccionados = random.choices(ids_disponibles, weights=pesos, k=cantidad_enemigos)

    lista_enemigos = []
    for i, eid in enumerate(seleccionados):
        #Creamos un ID único para cada instancia (ej: goblin_1, goblim_2)
        unique_id = f"{eid}_{i+1}"
        nuevo_enemigo = Enemigo(unique_id, ENEMIES[eid], piso=piso_actual)
        lista_enemigos.append(nuevo_enemigo)

    return lista_enemigos




def generar_boss(piso_actual):
    bosses_disponibles = []

    for enemy_id, data in ENEMIES.items():

        if data.get("tipo") == "boss":
            bosses_disponibles.append(enemy_id)

    boss_id = random.choice(bosses_disponibles)

    boss_data = ENEMIES[boss_id]

    boss = Enemigo(
        enemy_id=f"{boss_id}_boss",
        data=boss_data,
        piso=piso_actual
    )

    return boss