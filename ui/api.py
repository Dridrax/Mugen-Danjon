#ui/api.py

from flask import Flask, jsonify, request, render_template

from core.player import Player
from core.enemy import Enemy
from core.generator import generar_enemigo
from core.combat import combate, ACCION_ATACAR, ACCION_ESQUIVAR, ACCION_SALIR
from core.data.enemies import ENEMIES


app = Flask(__name__,
            template_folder="web/templates",
            static_folder="web/static")

# -------------------------
# ESTADO GLOBAL TEMPORAL (MVP)
# -------------------------
# (más adelante se cambia por sistema de sesiones)
player = Player()
current_enemy = None
combat_result = None


@app.route("/")
def index():
    return render_template("index.html")
    

# -------------------------
# INICIAR ENCUENTRO
# -------------------------
@app.route("/start", methods=["GET"])
def start():
    global current_enemy, combat_result

    current_enemy = generar_enemigo(player.piso)
    combat_result = None

    return jsonify({
        "player": player.get_estado(),
        "enemy": current_enemy.get_estado(),
        "log": [{
            "type": "info",
            "text": "¡Un enemigo aparece!"
        }]
    })


# -------------------------
# ACCIONES DE COMBATE
# -------------------------
@app.route("/action", methods=["POST"])
def action():
    global player, current_enemy, combat_result

    data = request.json
    accion = data.get("action")

    if not current_enemy:
        return jsonify({"error": "No hay combate activo"}), 400

    # -------------------------
    # MAPEO DE ACCIONES
    # -------------------------
    acciones_validas = {
        "attack": ACCION_ATACAR,
        "dodge": ACCION_ESQUIVAR,
        "exit": ACCION_SALIR
    }

    if accion not in acciones_validas:
        return jsonify({"error": "Acción inválida"}), 400

    accion_core = acciones_validas[accion]

    # -------------------------
    # EJECUTAR COMBATE (1 TURNO)
    # -------------------------
    resultado = combate(player, current_enemy, [accion_core])

    # -------------------------
    # SI TERMINA EL COMBATE
    # -------------------------
    if resultado["victoria"] or resultado["salir"]:

        loot = []

        if resultado["victoria"]:
            loot = resultado["loot"]

        current_enemy = None

        return jsonify({
            "end": True,
            "victory": resultado["victoria"],
            "player": player.get_estado(),
            "loot": [
                {
                    "nombre": item.nombre,
                    "tipo": item.tipo
                } for item in loot
            ],
            "log": resultado.get("log", [])  # 🔥 IMPORTANTE
        })

    # -------------------------
    # COMBATE CONTINÚA
    # -------------------------
    return jsonify({
        "end": False,
        "player": player.get_estado(),
        "enemy": current_enemy.get_estado(),
        "log": resultado.get("log", [])
    })


# -------------------------
# OBTENER ESTADO ACTUAL
# -------------------------
@app.route("/state", methods=["GET"])
def state():
    return jsonify({
        "player": player.get_estado(),
        "enemy": current_enemy.get_estado() if current_enemy else None
    })


# -------------------------
# ARRANQUE DEL SERVIDOR
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)