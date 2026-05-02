from flask import Flask, jsonify, request, render_template

from core.player import Player
from core.generator import generar_enemigo
from core.combat import combate, ACCION_ATACAR, ACCION_ESQUIVAR, ACCION_SALIR
from core.dungeon import Dungeon, ROOM_COMBAT, ROOM_REST, ROOM_BOSS


app = Flask(__name__,
            template_folder="web/templates",
            static_folder="web/static")

# -------------------------
# ESTADO GLOBAL (MVP)
# -------------------------

player = Player()
dungeon = Dungeon()
current_enemy = None


@app.route("/")
def index():
    return render_template("index.html")


# -------------------------
# SIGUIENTE SALA
# -------------------------

@app.route("/next_room", methods=["GET"])
def next_room():
    global current_enemy

    sala = dungeon.sala_actual()

    # -------------------------
    # COMBATE NORMAL
    # -------------------------
    if sala["type"] == ROOM_COMBAT:
        current_enemy = generar_enemigo(dungeon.piso, "normal")

        return jsonify({
            "mode": "combat",
            "room": sala,
            "enemy": current_enemy.get_estado(),
            "player": player.get_estado(),
            "dungeon": dungeon.get_estado(),
            "log": [{
                "type": "info",
                "text": "¡Un enemigo aparece!"
            }]
        })

    # -------------------------
    # DESCANSO
    # -------------------------
    elif sala["type"] == ROOM_REST:
        player.curar(20)

        dungeon.avanzar()

        return jsonify({
            "mode": "rest",
            "room": sala,
            "player": player.get_estado(),
            "dungeon": dungeon.get_estado(),
            "log": [{
                "type": "info",
                "text": "Descansas y recuperas vida"
            }]
        })

    # -------------------------
    # JEFE
    # -------------------------
    elif sala["type"] == ROOM_BOSS:
        current_enemy = generar_enemigo(dungeon.piso, "boss")

        return jsonify({
            "mode": "combat",
            "room": sala,
            "enemy": current_enemy.get_estado(),
            "player": player.get_estado(),
            "dungeon": dungeon.get_estado(),
            "log": [{
                "type": "info",
                "text": "👑 ¡Un jefe aparece!"
            }]
        })


# -------------------------
# ACCIONES DE COMBATE
# -------------------------

@app.route("/action", methods=["POST"])
def action():
    global current_enemy

    data = request.json
    accion = data.get("action")

    if not current_enemy:
        return jsonify({"error": "No hay combate activo"}), 400

    acciones_validas = {
        "attack": ACCION_ATACAR,
        "dodge": ACCION_ESQUIVAR,
        "exit": ACCION_SALIR
    }

    if accion not in acciones_validas:
        return jsonify({"error": "Acción inválida"}), 400

    accion_core = acciones_validas[accion]

    resultado = combate(player, current_enemy, [accion_core])

    # -------------------------
    # FIN DE COMBATE
    # -------------------------
    if resultado["victoria"] or resultado["salir"]:

        loot = []

        if resultado["victoria"]:
            loot = resultado["loot"]
            dungeon.avanzar()

        current_enemy = None

        return jsonify({
            "end": True,
            "victory": resultado["victoria"],
            "player": player.get_estado(),
            "loot": [
                {"nombre": i.nombre, "tipo": i.tipo}
                for i in loot
            ],
            "log": resultado.get("log", []),
            "dungeon": dungeon.get_estado()
        })

    # -------------------------
    # COMBATE CONTINÚA
    # -------------------------
    return jsonify({
        "end": False,
        "player": player.get_estado(),
        "enemy": current_enemy.get_estado(),
        "log": resultado.get("log", []),
        "dungeon": dungeon.get_estado()
    })


# -------------------------
# ESTADO
# -------------------------

@app.route("/state", methods=["GET"])
def state():
    return jsonify({
        "player": player.get_estado(),
        "enemy": current_enemy.get_estado() if current_enemy else None,
        "dungeon": dungeon.get_estado()
    })


if __name__ == "__main__":
    app.run(debug=True)