let combatActive = false;


// -------------------------
// SIGUIENTE SALA (CORE GAME)
// -------------------------
function nextRoom() {
    fetch("/next_room")
        .then(res => res.json())
        .then(data => {

            updateUI(data);
            clearLog();
            addLog(data.log || []);

            renderMap(data.dungeon);

            if (data.mode === "combat") {
                combatActive = true;
            } else {
                combatActive = false;
            }
        });
}


// -------------------------
// ACCIONES DE COMBATE
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
        addLog(data.log || []);
        renderMap(data.dungeon);

        // animación
        if (data.log) {
            data.log.forEach(line => {
                if (line.type === "damage" || line.type === "crit") {
                    animateEnemy();
                }
            });
        }

        // FIN COMBATE
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
        }
    });
}


// -------------------------
// ACTUALIZAR UI
// -------------------------
function updateUI(data) {

    // PLAYER
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

    // ENEMY
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
// MAPA VISUAL 🗺️
// -------------------------
function renderMap(dungeon) {
    const container = document.getElementById("map-container");

    if (!dungeon) return;

    container.innerHTML = "";

    dungeon.salas.forEach((room, index) => {
        const node = document.createElement("span");

        let icon = "❓";

        if (room.type === "combat") icon = "⚔️";
        if (room.type === "rest") icon = "🛏️";
        if (room.type === "boss") icon = "👑";

        node.innerText = icon;

        // estilos
        node.style.margin = "5px";
        node.style.fontSize = "24px";

        // visitada
        if (room.visited) {
            node.style.opacity = "0.4";
        }

        // actual
        if (index === dungeon.index) {
            node.style.border = "2px solid #38bdf8";
            node.style.borderRadius = "6px";
            node.style.padding = "2px";
        }

        container.appendChild(node);
    });
}


// -------------------------
// LOG
// -------------------------
function clearLog() {
    document.getElementById("log-text").innerHTML = "";
}

function addLog(lines) {
    const log = document.getElementById("log-text");

    if (!Array.isArray(lines)) return;

    lines.forEach(line => {
        const p = document.createElement("p");

        p.innerText = line.text;

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

        log.appendChild(p);
    });

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