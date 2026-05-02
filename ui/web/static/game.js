//ui/web/static/game.js

let combatActive = false;


// -------------------------
// INICIAR COMBATE
// -------------------------
function startGame() {
    fetch("/start")
        .then(res => res.json())
        .then(data => {
            combatActive = true;

            clearLog(); // 🔥 limpiar log anterior
            updateUI(data);

            addLog(data.log || [
                { type: "info", text: "¡Un enemigo aparece!" }
            ]);
        });
}


// -------------------------
// ENVIAR ACCIÓN
// -------------------------
function sendAction(action) {
    if (!combatActive) {
        addLog([{ type: "info", text: "No hay combate activo" }]);
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

        updateUI(data);

        // 🔥 añadir log del backend
        addLog(data.log || []);

        // -------------------------
        // ANIMACIÓN DE ATAQUE
        // -------------------------
        if (data.log) {
            data.log.forEach(line => {
                if (line.type === "damage" || line.type === "crit") {
                    animateEnemy();
                }
            });
        }

        // FIN DEL COMBATE
        if (data.end) {
            combatActive = false;

            if (data.victory) {
                addLog([{ type: "info", text: "🏆 ¡Has ganado!" }]);

                if (data.loot.length > 0) {
                    let lootText = data.loot.map(i => i.nombre).join(", ");
                    addLog([{ type: "info", text: "Loot: " + lootText }]);
                }

            } else {
                addLog([{ type: "info", text: "Has perdido o escapado..." }]);
            }

            return;
        }
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
// LOG SISTEMA NUEVO
// -------------------------

function clearLog() {
    document.getElementById("log-text").innerHTML = "";
}

function addLog(lines) {
    const log = document.getElementById("log-text");

    if (!Array.isArray(lines)) return;

    lines.forEach(line => {
        const p = document.createElement("p");

        if (typeof line === "object") {
            p.innerText = line.text;

            // 🎨 estilos por tipo
            switch (line.type) {
                case "damage":
                    p.classList.add("log-damage");
                    break;
                case "crit":
                    p.classList.add("log-crit");
                    break;
                case "miss":
                    p.classList.add("log-miss");
                    break;
                case "dodge":
                    p.classList.add("log-dodge");
                    break;
                default:
                    p.classList.add("log-info");
            }

        } else {
            p.innerText = line;
        }

        log.appendChild(p);
    });

    // 🔽 auto scroll
    log.scrollTop = log.scrollHeight;
}


// -------------------------
// ANIMACIÓN
// -------------------------

function animateEnemy() {
    const enemy = document.getElementById("enemy");

    enemy.classList.add("shake");

    setTimeout(() => {
        enemy.classList.remove("shake");
    }, 300);
}