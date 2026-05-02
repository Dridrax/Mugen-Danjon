#ui/input_handler

from core.combat import ACCION_ATACAR, ACCION_ESQUIVAR, ACCION_SALIR


# -------------------------
# MENÚ DE COMBATE
# -------------------------

def menu_combate():
    """
    Devuelve la acción del jugador en combate
    """

    print("\n--- TU TURNO ---")
    print("1. Atacar")
    print("2. Esquivar")
    print("3. Salir")

    opcion = input("Elige una acción: ")

    if opcion == "1":
        return ACCION_ATACAR

    elif opcion == "2":
        return ACCION_ESQUIVAR

    elif opcion == "3":
        return ACCION_SALIR

    else:
        print("Opción inválida, se asume atacar.")
        return ACCION_ATACAR


# -------------------------
# MENÚ FUTURO (INVENTARIO)
# -------------------------

def menu_inventario(jugador):
    """
    Muestra inventario y permite selección básica
    (preparado para futuro sistema UI)
    """

    print("\n--- INVENTARIO ---")

    if not jugador.inventario:
        print("Inventario vacío")
        return None

    for i, item in enumerate(jugador.inventario):
        print(f"{i + 1}. {item.nombre}")

    print("0. Salir")

    opcion = input("Selecciona un objeto: ")

    if opcion == "0":
        return None

    try:
        index = int(opcion) - 1
        return jugador.inventario[index]
    except:
        print("Selección inválida")
        return None


# -------------------------
# MENÚ DE EQUIPAMIENTO
# -------------------------

def menu_equipar(jugador, item):
    """
    Decide si equipar o no un arma
    """

    if item.tipo != "arma":
        return False

    print(f"\nHas encontrado: {item.nombre}")
    print("1. Equipar")
    print("2. Guardar en inventario")

    opcion = input("¿Qué deseas hacer?: ")

    if opcion == "1":
        return jugador.equipar_arma(item)

    else:
        jugador.agregar_item(item)
        return False


# -------------------------
# UTILIDAD GENERAL
# -------------------------

def pausa():
    input("\nPulsa ENTER para continuar...")