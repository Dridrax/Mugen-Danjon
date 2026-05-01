let combatActive = false;


// -------------------------
// INICIAR COMBATE
// -------------------------
function startGame() {
    fetch("/start")
        .then(res => res.json())
        .then(data => {
            combatActive = true;
            updateUI(data);
            setLog("¡Un enemigo aparece!");
        });
}


// -------------------------
// ENVIAR ACCIÓN
// -------------------------
function sendAction(action) {
    if (!combatActive) {
        setLog("No hay combate activo");
        return;
    }

    fetch("/action", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ action: action })
    })
    .then(res => res.json())
    .then(data => {

        // FIN DEL COMBATE
        if (data.end) {
            combatActive = false;

            if (data.victory) {
                setLog("¡Has ganado!");

                if (data.loot.length > 0) {
                    let lootText = data.loot.map(i => i.nombre).join(", ");
                    setLog("Loot: " + lootText);
                }

            } else {
                setLog("Has perdido o escapado...");
            }

            updateUI(data);
            return;
        }

        // COMBATE CONTINÚA
        updateUI(data);
        setLog("Acción realizada...");
    });
}


// -------------------------
// ACTUALIZAR UI
// -------------------------
function updateUI(data) {

    if (data.player) {
        document.getElementById("player-hp").innerText =
            data.player.hp + " / " + data.player.hp_max;

        document.getElementById("player-attack").innerText =
            data.player.ataque;

        document.getElementById("player-defense").innerText =
            data.player.defensa;

        document.getElementById("player-gold").innerText =
            data.player.oro;
    }

    if (data.enemy) {
        document.getElementById("enemy-name").innerText =
            data.enemy.nombre;

        document.getElementById("enemy-hp").innerText =
            data.enemy.hp + " / " + data.enemy.hp_max;
    } else {
        document.getElementById("enemy-name").innerText = "-";
        document.getElementById("enemy-hp").innerText = "-";
    }
}


// -------------------------
// LOG
// -------------------------
function setLog(text) {
    document.getElementById("log-text").innerText = text;
}