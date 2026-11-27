// SexyLand - Lina Thorniel, bardo de Valdoria: toca música, cuenta historias e inspira a quien le deja propina.
var SL_SRV = Java.type("net.minecraftforge.server.ServerLifecycleHooks");
function __run(c) {
    var S = SL_SRV.getCurrentServer();
    try { return S.m_129892_().m_230957_(S.m_129893_().m_81324_(), c); } catch (x) { return 0; }
}

// [sonido, duración en ticks, título que anuncia Lina]
var CANCIONES = [
    ["minecraft:music_disc.cat", 3700, "La Gata del Molino"],
    ["minecraft:music_disc.blocks", 6900, "Piedra sobre Piedra"],
    ["minecraft:music_disc.chirp", 3700, "El Gorrión de la Plaza"],
    ["minecraft:music_disc.far", 3480, "Caminos de Eldoria"],
    ["minecraft:music_disc.mall", 3940, "Mercado de Valdoria"],
    ["minecraft:music_disc.mellohi", 1920, "Nana para un Centinela"],
    ["minecraft:music_disc.strad", 3760, "La Danza del Herrero"],
    ["minecraft:music_disc.wait", 4760, "Espera en la Taberna"],
    ["minecraft:music_disc.otherside", 3900, "El Otro Lado del Portal"],
    ["minecraft:music_disc.relic", 4360, "Reliquias del Siglo Vacío"],
    ["aether:item.music_disc.aether_tune", 2980, "Islas sobre las Nubes"],
    ["aether:item.music_disc.ascending_dawn", 7000, "Amanecer de las Valquirias"],
    ["aether:item.music_disc.high", 3720, "Más Alto que el Cielo"],
    ["biomeswevegone:music_disc.better_days", 2920, "Días Mejores"],
    ["alexsmobs:music_disc_thime", 6280, "El Reloj de Clock"],
    ["irons_spellbooks:music.dead_king_lullaby", 2740, "Canción de Cuna del Rey Muerto"],
    ["lost_aether_content:record.legacy", 5940, "El Legado de la Corona"]
];
var PLATA = "numismatic-overhaul:silver_coin";
var D_TOCAR = 9781, D_PARAR = 9783, D_HISTORIA = 9784, D_PROPINA = 9785;
var HISTORIAS = [9790, 9791, 9792, 9793];
var ESPERA_INSP = 20 * 60 * 1000;      // una inspiración cada 20 min por jugador
var AUTO = 8 * 60 * 1000;              // si hay público y está callada, toca sola cada 8 min

var __pend = [], __n = 0, __fin = 0, __ultima = -1, __auto = 0;

function ahora() { return java.lang.System.currentTimeMillis(); }
function pos(npc) { return npc.getX().toFixed(1) + " " + (npc.getY() + 1).toFixed(1) + " " + npc.getZ().toFixed(1); }
function cerca(npc, r) { return "@a[x=" + npc.getX().toFixed(1) + ",y=" + npc.getY().toFixed(1) + ",z=" + npc.getZ().toFixed(1) + ",distance=.." + r + "]"; }
function decir(npc, t) { __run('tellraw ' + cerca(npc, 32) + ' [{"text":"♪ Lina Thorniel: ","color":"light_purple","bold":true},{"text":' + JSON.stringify(t) + ',"color":"white","bold":false}]'); }
function sonando() { return ahora() < __fin; }

function tocar(npc, quien) {
    if (sonando()) { if (quien) quien.message("§d♪ Lina ya está tocando. §7Espera a que acabe la canción o pídele que pare."); return; }
    var i;
    do { i = Math.floor(Math.random() * CANCIONES.length); } while (i == __ultima && CANCIONES.length > 1);
    __ultima = i;
    var c = CANCIONES[i];
    __run("stopsound " + cerca(npc, 64) + " record");
    __run("execute positioned " + pos(npc) + " run playsound " + c[0] + " record " + cerca(npc, 64) + " " + pos(npc) + " 4 1");
    __fin = ahora() + c[1] * 50;
    __auto = ahora();
    decir(npc, "Esta se llama «" + c[2] + "». " + ["¡Que suene!", "Para quien quiera escuchar.", "Palmas, que esto se anima.", "Dedicada a los valientes de la Arena."][Math.floor(Math.random() * 4)]);
}

function parar(npc) {
    __run("stopsound " + cerca(npc, 64) + " record");
    __fin = 0;
    decir(npc, "Como quieras. Mi laúd también necesita descansar.");
}

function inspirar(npc, p) {
    var sd = p.getStoreddata(), t = sd.has("sl_bardo_insp") ? Number(sd.get("sl_bardo_insp")) : 0;
    if (ahora() - t < ESPERA_INSP) {
        p.message("§d♪ Lina:§r Todavía te dura la última inspiración. Vuelve en " + Math.ceil((t + ESPERA_INSP - ahora()) / 60000) + " minutos.");
        return;
    }
    var nm = "" + p.getName();
    if ((Number(__run("clear " + nm + " " + PLATA + " 0")) | 0) < 1 || (Number(__run("clear " + nm + " " + PLATA + " 1")) | 0) < 1) {
        p.message("§d♪ Lina:§r Una moneda de plata, nada más. El arte también come.");
        return;
    }
    sd.put("sl_bardo_insp", ahora());
    var g = cerca(npc, 8);
    __run("effect give " + g + " minecraft:speed 600 0 true");
    __run("effect give " + g + " minecraft:haste 600 0 true");
    __run("effect give " + g + " minecraft:luck 600 0 true");
    __run("effect give " + g + " minecraft:regeneration 20 0 true");
    __run("execute positioned " + pos(npc) + " run particle minecraft:note ~ ~1 ~ 2 1 2 1 40");
    __run("execute positioned " + pos(npc) + " run playsound minecraft:block.note_block.chime player " + g + " ~ ~ ~ 1 1.2");
    __run('title ' + g + ' actionbar {"text":"✦ Inspiración del Bardo: velocidad, prisa y suerte durante 10 minutos","color":"light_purple"}');
    decir(npc, "¡Por " + nm + ", que paga a los artistas! Que la canción os acompañe a todos los que estáis cerca.");
}

function dialog(e) {
    try {
        var id = e.dialog.getId();
        if (id != D_TOCAR && id != D_PARAR && id != D_HISTORIA && id != D_PROPINA) return;
        __pend.push(["" + e.player.getName(), id]);
        e.npc.getTimers().forceStart(81, 6, false);
    } catch (x) { print("[Bardo] dialog: " + x); }
}

function timer(e) {
    if (e.id != 81) return;
    var l = __pend; __pend = [];
    for (var i = 0; i < l.length; i++) {
        try {
            var p = e.npc.getWorld().getPlayer(l[i][0]);
            if (!p) continue;
            if (l[i][1] == D_TOCAR) tocar(e.npc, p);
            else if (l[i][1] == D_PARAR) parar(e.npc);
            else if (l[i][1] == D_PROPINA) inspirar(e.npc, p);
            else p.showDialog(HISTORIAS[Math.floor(Math.random() * HISTORIAS.length)], "Lina Thorniel");
        } catch (x) { print("[Bardo] " + l[i][0] + ": " + x); }
    }
}

function tick(e) {
    if ((++__n) % 4 != 0) return;                 // ~cada 2 segundos
    try {
        var npc = e.npc;
        if (sonando()) {
            __run("execute positioned " + pos(npc) + " run particle minecraft:note ~ ~1.2 ~ 0.6 0.3 0.6 1 2");
            return;
        }
        if (ahora() - __auto > AUTO && (Number(__run("execute if entity " + cerca(npc, 12))) | 0) > 0) tocar(npc, null);
    } catch (x) { print("[Bardo] tick: " + x); }
}
