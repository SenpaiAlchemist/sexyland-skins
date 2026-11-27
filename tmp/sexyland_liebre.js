// SexyLand - Mala Liebre, juglar pícaro de la plaza de Valdoria: toca, cuenta chascarrillos y vende coplas de coraje.
var SL_SRV = Java.type("net.minecraftforge.server.ServerLifecycleHooks");
function __run(c) {
    var S = SL_SRV.getCurrentServer();
    try { return S.m_129892_().m_230957_(S.m_129893_().m_81324_(), c); } catch (x) { return 0; }
}

// [sonido, duración en ticks, título que anuncia Mala Liebre]
var CANCIONES = [
    ["minecraft:music_disc.strad", 3760, "La Jarra Sin Fondo"],
    ["minecraft:music_disc.chirp", 3700, "La Moza del Molino"],
    ["minecraft:music_disc.cat", 3700, "El Gato del Tabernero"],
    ["minecraft:music_disc.mall", 3940, "Regateando en Valdoria"],
    ["minecraft:music_disc.blocks", 6900, "La Danza de los Borrachos"],
    ["minecraft:music_disc.far", 3480, "Me Fui a la Frontera (y Volví sin Blanca)"],
    ["minecraft:music_disc.wait", 4760, "Espera, que Pago Mañana"],
    ["minecraft:music_disc.otherside", 3900, "La Liebre que Burló al Centinela"],
    ["biomeswevegone:music_disc.better_days", 2920, "Días de Vino y Coplas"],
    ["alexsmobs:music_disc_thime", 6280, "El Pícaro y el Reloj de Clock"],
    ["aether:item.music_disc.high", 3720, "Más Alto que una Valquiria"],
    ["minecraft:music_disc.mellohi", 1920, "Serenata Bajo el Balcón"]
];
var PLATA = "numismatic-overhaul:silver_coin";
var D_TOCAR = 9801, D_PARAR = 9803, D_HISTORIA = 9804, D_PROPINA = 9805;
var HISTORIAS = [9810, 9811, 9812, 9813];
var ESPERA_INSP = 20 * 60 * 1000;      // unas coplas cada 20 min por jugador
var PRECIO = 2;
var AUTO = 8 * 60 * 1000;              // si hay público y está callada, toca sola cada 8 min

var __pend = [], __n = 0, __fin = 0, __ultima = -1, __auto = 0, __sonido = "";
var RADIO = 8;          // solo se oye alrededor de su puesto en la plaza

function ahora() { return java.lang.System.currentTimeMillis(); }
function pos(npc) { return npc.getX().toFixed(1) + " " + (npc.getY() + 1).toFixed(1) + " " + npc.getZ().toFixed(1); }
function cerca(npc, r) { return "@a[x=" + npc.getX().toFixed(1) + ",y=" + npc.getY().toFixed(1) + ",z=" + npc.getZ().toFixed(1) + ",distance=.." + r + "]"; }
function decir(npc, t) { __run('tellraw ' + cerca(npc, 32) + ' [{"text":"♪ Mala Liebre: ","color":"green","bold":true},{"text":' + JSON.stringify(t) + ',"color":"white","bold":false}]'); }
function sonando() { return ahora() < __fin; }

function tocar(npc, quien) {
    if (sonando()) { if (quien) quien.message("§a♪ Mala Liebre ya está tocando. §7Espera a que acabe o pídele que se calle."); return; }
    var i;
    do { i = Math.floor(Math.random() * CANCIONES.length); } while (i == __ultima && CANCIONES.length > 1);
    __ultima = i;
    var c = CANCIONES[i];
    __run("stopsound " + cerca(npc, 64) + " record");
    __run("execute positioned " + pos(npc) + " run playsound " + c[0] + " record " + cerca(npc, RADIO) + " " + pos(npc) + " 0.35 1");
    __fin = ahora() + c[1] * 50;
    __sonido = c[0];
    __auto = ahora();
    decir(npc, "Esta se llama «" + c[2] + "». " + ["¡Que se arranquen las palmas!", "Esta la compuse borracho, se nota.", "Dedicada a las doncellas de Valdoria... y a sus madres, por si acaso.", "Si os gusta, la gorra está aquí abajo."][Math.floor(Math.random() * 4)]);
}

function parar(npc) {
    __run("stopsound " + cerca(npc, 64) + " record");
    __fin = 0;
    decir(npc, "Vale, vale, me callo. Pero que conste que el arte se paga.");
}

function inspirar(npc, p) {
    var sd = p.getStoreddata(), t = sd.has("sl_liebre_insp") ? Number(sd.get("sl_liebre_insp")) : 0;
    if (ahora() - t < ESPERA_INSP) {
        p.message("§a♪ Mala Liebre:§r Todavía te dura el coraje de la última copla. Vuelve en " + Math.ceil((t + ESPERA_INSP - ahora()) / 60000) + " minutos.");
        return;
    }
    var nm = "" + p.getName();
    if ((Number(__run("clear " + nm + " " + PLATA + " 0")) | 0) < PRECIO || (Number(__run("clear " + nm + " " + PLATA + " " + PRECIO)) | 0) < PRECIO) {
        p.message("§a♪ Mala Liebre:§r Dos de plata, ni una menos. El vino no se paga solo.");
        return;
    }
    sd.put("sl_liebre_insp", ahora());
    var g = cerca(npc, 8);
    __run("effect give " + g + " minecraft:strength 600 0 true");
    __run("effect give " + g + " minecraft:absorption 600 0 true");
    __run("execute positioned " + pos(npc) + " run particle minecraft:note ~ ~1 ~ 2 1 2 1 40");
    __run("execute positioned " + pos(npc) + " run playsound minecraft:block.note_block.banjo player " + g + " ~ ~ ~ 1 1");
    __run('title ' + g + ' actionbar {"text":"\u2726 Coplas de Coraje: fuerza y corazones extra durante 10 minutos","color":"green"}');
    decir(npc, "¡Va por " + nm + ", que paga como un noble! Escuchad esta copla y salid a partir caras... con elegancia.");
}

function dialog(e) {
    try {
        var id = e.dialog.getId();
        if (id != D_TOCAR && id != D_PARAR && id != D_HISTORIA && id != D_PROPINA) return;
        __pend.push(["" + e.player.getName(), id]);
        e.npc.getTimers().forceStart(82, 6, false);
    } catch (x) { print("[Liebre] dialog: " + x); }
}

function timer(e) {
    if (e.id != 82) return;
    var l = __pend; __pend = [];
    for (var i = 0; i < l.length; i++) {
        try {
            var p = e.npc.getWorld().getPlayer(l[i][0]);
            if (!p) continue;
            if (l[i][1] == D_TOCAR) tocar(e.npc, p);
            else if (l[i][1] == D_PARAR) parar(e.npc);
            else if (l[i][1] == D_PROPINA) inspirar(e.npc, p);
            else p.showDialog(HISTORIAS[Math.floor(Math.random() * HISTORIAS.length)], "Mala Liebre");
        } catch (x) { print("[Liebre] " + l[i][0] + ": " + x); }
    }
}

function tick(e) {
    if ((++__n) % 4 != 0) return;                 // ~cada 2 segundos
    try {
        var npc = e.npc;
        if (sonando()) {
            // quien sale del edificio deja de oírla
            __run("execute positioned " + pos(npc) + " run stopsound @a[distance=" + (RADIO + 1) + "..80] record " + __sonido);
            __run("execute positioned " + pos(npc) + " run particle minecraft:note ~ ~1.2 ~ 0.6 0.3 0.6 1 2");
            return;
        }
        if (ahora() - __auto > AUTO && (Number(__run("execute if entity " + cerca(npc, RADIO))) | 0) > 0) tocar(npc, null);
    } catch (x) { print("[Liebre] tick: " + x); }
}
