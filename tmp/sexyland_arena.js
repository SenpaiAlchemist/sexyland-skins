// SexyLand - Clock, Guardián de la Arena de Eldoria (Valdoria, capital de Eldoria)
// Desafío de bestias por niveles y oleadas (solo o en grupo), duelos 1 vs 1 y Juegos de Eldoria (todos contra todos).
// Se entra sin el equipo propio: cada luchador elige un set (que no cambia durante la partida) y lo mejora entre oleadas.
// Recompensas: solo monedas y XP. Las bestias no sueltan nada. Requiere sexyland_arena_inv.js en la ScriptList.
var SL_SRV = Java.type("net.minecraftforge.server.ServerLifecycleHooks");
function __run(c) {
    var S = SL_SRV.getCurrentServer();
    try { return S.m_129892_().m_230957_(S.m_129893_().m_81324_(), c); } catch (x) { return 0; }
}

// ---------- Geometría ----------
var CX = 568, CZ = -222;
var BX1 = 534, BX2 = 601, BY1 = 18, BY2 = 62, BZ1 = -258, BZ2 = -185;
var CAJA = "x=" + BX1 + ",y=" + BY1 + ",z=" + BZ1 + ",dx=" + (BX2 - BX1) + ",dy=" + (BY2 - BY1) + ",dz=" + (BZ2 - BZ1);

// ---------- Economía ----------
var PLATA = "numismatic-overhaul:silver_coin", ORO = "numismatic-overhaul:gold_coin";
var CUOTA_DUELO = 20, CUOTA_JDH = 20;
var JDH_MIN = 3, JDH_ESPERA = 60, DUELO_ESPERA = 120, ELEGIR = 25, TIENDA = 30, TIEMPO_OLEADA = 360;
var DIA = 24 * 3600 * 1000;
var COSTE = [0, 4, 9, 16];     // mejora a nivel 1, 2, 3 (arma o armadura)
var COSTE_SUM = 2;

// ---------- Niveles (3 oleadas cada uno) ----------
// [tipo, cantidad, jefe]
var NIVELES = [
    { n: "I", nombre: "Bestias del Páramo", plata: 12, xp: 150, hp: 1.5, dmg: 1.2, olas: [
        [["minecraft:husk", 4, 0]],
        [["minecraft:vindicator", 3, 0], ["minecraft:skeleton", 2, 0]],
        [["minecraft:vindicator", 4, 0], ["minecraft:husk", 3, 0], ["minecraft:skeleton", 2, 0]]] },
    { n: "II", nombre: "La Horda de Asalto", plata: 24, xp: 300, hp: 1.6, dmg: 1.25, olas: [
        [["minecraft:pillager", 3, 0], ["minecraft:vindicator", 2, 0]],
        [["minecraft:ravager", 1, 0], ["minecraft:pillager", 2, 0], ["minecraft:evoker", 1, 0]],
        [["minecraft:ravager", 2, 0], ["minecraft:pillager", 3, 0], ["minecraft:evoker", 1, 0]]] },
    { n: "III", nombre: "La Legión Infernal", plata: 40, xp: 600, hp: 1.7, dmg: 1.3, olas: [
        [["minecraft:wither_skeleton", 4, 0]],
        [["minecraft:blaze", 2, 0], ["realmrpg_demons:demon", 2, 0]],
        [["minecraft:wither_skeleton", 4, 0], ["minecraft:blaze", 2, 0], ["realmrpg_demons:demon", 2, 0]]] },
    { n: "IV", nombre: "El Wroughtnaut", plata: 70, xp: 1200, hp: 1.4, dmg: 1.2, olas: [
        [["minecraft:vindicator", 4, 0], ["minecraft:evoker", 1, 0]],
        [["minecraft:wither_skeleton", 3, 0], ["minecraft:ravager", 1, 0]],
        [["mowziesmobs:ferrous_wroughtnaut", 1, 1], ["minecraft:vindicator", 2, 0]]] },
    { n: "V", nombre: "El Rey Muerto", plata: 110, xp: 2500, hp: 1.4, dmg: 1.2, olas: [
        [["minecraft:wither_skeleton", 4, 0], ["minecraft:blaze", 2, 0]],
        [["realmrpg_demons:demon", 3, 0], ["minecraft:ravager", 1, 0]],
        [["irons_spellbooks:dead_king", 1, 1], ["minecraft:wither_skeleton", 2, 0]]] },
    { n: "VI", nombre: "Ignis, el Herrero del Fuego", plata: 200, xp: 5000, hp: 1.3, dmg: 1.15, olas: [
        [["realmrpg_demons:demon", 3, 0], ["minecraft:blaze", 2, 0]],
        [["minecraft:ravager", 2, 0], ["minecraft:wither_skeleton", 4, 0]],
        [["cataclysm:ignis", 1, 1]]] }
];
var REPARTO = [0.25, 0.25, 0.5];

// ---------- Sets ----------
var SETS = ["guerrero", "tanque", "apoyo", "francotirador", "magico", "picaro"];
var SET_NOMBRE = { guerrero: "Guerrero", tanque: "Tanque", apoyo: "Apoyo", francotirador: "Francotirador", magico: "Mágico", picaro: "Pícaro" };
var SET_DESC = { guerrero: "más ataque (Fuerza I)", tanque: "más defensa (Resistencia I + escudo)", apoyo: "+4 corazones y pociones para curar al grupo",
                 francotirador: "arco y flechas, pelea a distancia", magico: "bastón con hechizos", picaro: "más ágil (Velocidad II + salto)" };
var ARM_MAT = {
    guerrero: ["leather", "chainmail", "iron", "diamond"], tanque: ["chainmail", "iron", "diamond", "netherite"],
    apoyo: ["leather", "chainmail", "iron", "diamond"], francotirador: ["leather", "leather", "chainmail", "iron"],
    magico: ["mago", "mago", "mago", "mago"], picaro: ["leather", "leather", "chainmail", "chainmail"]
};
var ARM_PROT = {
    guerrero: [0, 0, 1, 2], tanque: [0, 1, 2, 3], apoyo: [0, 0, 1, 2], francotirador: [0, 1, 1, 2], magico: [0, 1, 2, 3], picaro: [0, 1, 1, 2]
};
var PASIVA = {
    guerrero: [["strength", 0]], tanque: [["resistance", 0]], apoyo: [["health_boost", 1]],
    francotirador: [], magico: [], picaro: [["speed", 1], ["jump_boost", 0]]
};

// ---------- Diálogos disparadores ----------
var D_SOLO0 = 9740, D_GRUPO0 = 9750, D_DUELO = 9730, D_JDH = 9731, D_ESTADO = 9732;

// ---------- Estado ----------
var ST = { modo: "libre" };   // libre | bestias | duelo_espera | duelo | jdh_espera | jdh
var __pend = [], __n = 0, __salida = [], __devolver = [];

function ahora() { return java.lang.System.currentTimeMillis(); }
function seg() { return Math.floor(ahora() / 1000); }
function nombre(p) { return "" + p.getName(); }
function decir(p, t) { if (p) p.message("§6§lClock:§r " + t); }
function todos(t) { __run('tellraw @a [{"text":"⚔ Arena de Eldoria » ","color":"gold","bold":true},{"text":' + JSON.stringify(t) + ',"color":"yellow","bold":false}]'); }
function titulo(nm, t, s) {
    __run('title ' + nm + ' times 5 40 10');
    __run('title ' + nm + ' subtitle ' + JSON.stringify({ text: s || "", color: "yellow" }));
    __run('title ' + nm + ' title ' + JSON.stringify({ text: t, color: "gold", bold: true }));
}
function monedas(nm, item) { return Number(__run("clear " + nm + " " + item + " 0")) | 0; }
function cobrar(nm, n) {
    if (monedas(nm, PLATA) < n) return false;
    return (Number(__run("clear " + nm + " " + PLATA + " " + n)) | 0) >= n;
}
function pagar(nm, plata) {
    plata = Math.floor(plata);
    var o = Math.floor(plata / 100), s = plata % 100;
    if (o > 0) __run("give " + nm + " " + ORO + " " + o);
    if (s > 0) __run("give " + nm + " " + PLATA + " " + s);
}
function textoPlata(plata) {
    plata = Math.floor(plata);
    var o = Math.floor(plata / 100), s = plata % 100, r = [];
    if (o > 0) r.push(o + " de oro");
    if (s > 0 || o == 0) r.push(s + " de plata");
    return r.join(" y ");
}
function sueloY(w, x, z) {
    for (var y = 45; y > BY1; y--) { try { if (!w.getBlock(x, y, z).isAir() && w.getBlock(x, y + 1, z).isAir() && w.getBlock(x, y + 2, z).isAir()) return y + 1; } catch (e) { } }
    return 27;
}
function enRuedo(p) {
    try {
        if (!p || !p.isAlive()) return false;
        if (("" + p.getWorld().getName()).indexOf("overworld") < 0) return false;
        var x = p.getX(), y = p.getY(), z = p.getZ();
        return x >= BX1 && x <= BX2 + 1 && z >= BZ1 && z <= BZ2 + 1 && y >= BY1 - 4 && y <= BY2 + 8;
    } catch (e) { return false; }
}
function tpRuedo(w, nm, ang, r) {
    var x = Math.round(CX + Math.cos(ang) * r), z = Math.round(CZ + Math.sin(ang) * r);
    var y = sueloY(w, x, z);
    __run("tp " + nm + " " + (x + 0.5) + " " + y + " " + (z + 0.5) + " facing " + CX + " " + y + " " + CZ);
}
function tpSalida(npc, nm) { __run("tp " + nm + " " + npc.getX() + " " + npc.getY() + " " + npc.getZ()); }
function limpiarSuelo() {
    __run("kill @e[type=minecraft:item," + CAJA + "]");
    __run("kill @e[type=minecraft:experience_orb," + CAJA + "]");
}
function limpiarCadaveres() { __run("kill @e[type=corpse:corpse," + CAJA + "]"); }
function vivosMobs() { return Number(__run("execute if entity @e[tag=sl_arena_mob]")) | 0; }
function quitarMobs() { __run("kill @e[tag=sl_arena_mob]"); }
function activos(w) {
    var r = [];
    for (var i = 0; i < ST.jug.length; i++) { var p = w.getPlayer(ST.jug[i]); if (enRuedo(p)) r.push(ST.jug[i]); }
    return r;
}
function marcarEnCurso(w, lista) {
    try { var sd = w.getStoreddata(); if (lista && lista.length) sd.put("sl_arena_en_curso", lista.join(",")); else sd.remove("sl_arena_en_curso"); } catch (x) { }
}

// ---------- Kits ----------
function encs(arr) {
    var l = ['{id:"minecraft:vanishing_curse",lvl:1s}'];
    for (var i = 0; i < arr.length; i++) if (arr[i][1] > 0) l.push('{id:"minecraft:' + arr[i][0] + '",lvl:' + arr[i][1] + 's}');
    return "Enchantments:[" + l.join(",") + "]";
}
function nbt(extra, enc) { return "{sl_arena:1b,Unbreakable:1b," + encs(enc || []) + (extra ? "," + extra : "") + "}"; }
var HECHIZOS = [
    [["firebolt", 2]],
    [["firebolt", 4], ["magic_missile", 3]],
    [["firebolt", 6], ["magic_missile", 5], ["icicle", 4]],
    [["firebolt", 8], ["magic_missile", 7], ["icicle", 6], ["lightning_bolt", 5]]
];
function baston(lv) {
    var h = HECHIZOS[lv], d = [];
    for (var i = 0; i < h.length; i++) d.push('{id:"irons_spellbooks:' + h[i][0] + '",index:' + i + ',level:' + h[i][1] + ',locked:1b}');
    return 'irons_spellbooks:graybeard_staff' + nbt('sl_arena_arma:1b,"irons_spellbooks:spell_container":{maxSpells:' + h.length + ',mustEquip:0b,spellWheel:1b,data:[' + d.join(",") + ']}');
}
function arma(set, lv) {
    var mat = ["stone", "iron", "diamond", "netherite"][lv];
    if (set == "guerrero") return "minecraft:" + mat + "_sword" + nbt("sl_arena_arma:1b", [["sharpness", lv]]);
    if (set == "tanque") return "minecraft:" + mat + "_axe" + nbt("sl_arena_arma:1b", [["sharpness", Math.max(0, lv - 1)]]);
    if (set == "apoyo") return "minecraft:" + ["wooden", "stone", "iron", "diamond"][lv] + "_sword" + nbt("sl_arena_arma:1b", [["sharpness", lv >= 2 ? 1 : 0]]);
    if (set == "francotirador") return "minecraft:bow" + nbt("sl_arena_arma:1b", [["power", lv + 1], ["punch", lv >= 3 ? 1 : 0], ["flame", lv >= 2 ? 1 : 0]]);
    if (set == "magico") return baston(lv);
    return "minecraft:" + ["stone", "iron", "iron", "diamond"][lv] + "_sword" + nbt("sl_arena_arma:1b", [["sharpness", lv], ["fire_aspect", lv >= 3 ? 1 : 0]]);
}
function pieza(set, lv, parte) {
    var mat = ARM_MAT[set][lv], prot = ARM_PROT[set][lv];
    var id = mat == "mago" ? "irons_spellbooks:wandering_magician_" + (parte == "helmet" ? "helmet" : parte) : "minecraft:" + mat + "_" + parte;
    var en = [["protection", prot]];
    if (set == "picaro" && parte == "boots") en.push(["feather_falling", 2]);
    return id + nbt("sl_arena_armadura:1b", en);
}
function equiparArmadura(nm, set, lv) {
    __run("item replace entity " + nm + " armor.head with " + pieza(set, lv, "helmet"));
    __run("item replace entity " + nm + " armor.chest with " + pieza(set, lv, "chestplate"));
    __run("item replace entity " + nm + " armor.legs with " + pieza(set, lv, "leggings"));
    __run("item replace entity " + nm + " armor.feet with " + pieza(set, lv, "boots"));
}
function darArma(nm, set, lv) {
    __run("clear " + nm + " *{sl_arena_arma:1b}");
    __run("give " + nm + " " + arma(set, lv));
    if (set == "francotirador") __run("give " + nm + " minecraft:wooden_sword" + nbt(""));
}
function suministros(nm, set, inicial) {
    __run("give " + nm + " minecraft:cooked_beef" + nbt("") + " " + (inicial ? 6 : 4));
    __run("give " + nm + " legendarysurvivaloverhaul:purified_water_bottle" + nbt("") + " " + (inicial ? 2 : 2));
    if (set == "francotirador") __run("give " + nm + " minecraft:arrow" + nbt("") + " " + (inicial ? 48 : 24));
    if (set == "apoyo") {
        __run("give " + nm + ' minecraft:splash_potion' + nbt('Potion:"minecraft:strong_healing"') + " 2");
        __run("give " + nm + ' minecraft:lingering_potion' + nbt('Potion:"minecraft:regeneration"') + " 1");
    }
    if (set == "picaro") __run("give " + nm + " minecraft:ender_pearl" + nbt("") + " " + (inicial ? 2 : 1));
    if (set == "tanque" && inicial) __run("item replace entity " + nm + " weapon.offhand with minecraft:shield" + nbt(""));
    if (set == "magico") __run("give " + nm + ' minecraft:potion' + nbt('Potion:"minecraft:regeneration"') + " 1");
}
function aplicarPasiva(nm, set) {
    var l = PASIVA[set];
    for (var i = 0; i < l.length; i++) __run("effect give " + nm + " minecraft:" + l[i][0] + " infinite " + l[i][1] + " true");
}
function equipar(w, nm, set, lvA, lvR) {
    var p = w.getPlayer(nm);
    if (!p) return false;
    if (!slaGuardar(p)) { decir(p, "§cNo he podido guardar tu inventario de forma segura, así que no entras. Avisa a un administrador."); return false; }
    __run("effect clear " + nm);
    darArma(nm, set, lvA);
    equiparArmadura(nm, set, lvR);
    suministros(nm, set, true);
    aplicarPasiva(nm, set);
    __run("effect give " + nm + " minecraft:saturation 2 4 true");
    __run("effect give " + nm + " minecraft:instant_health 1 4 true");
    return true;
}
function devolver(w, nm) {
    var p = w.getPlayer(nm);
    if (p && p.isAlive()) { try { if (slaDevolver(p)) decir(p, "Te devuelvo tu equipo. Vuelve cuando quieras."); } catch (x) { print("[Arena] devolver " + nm + ": " + x); } return true; }
    return false;       // muerto u offline: se intentará después (o al conectarse)
}

// ---------- Menús en el chat (botones /trigger arena) ----------
function boton(txt, n, color, hover) {
    return '{"text":' + JSON.stringify("[" + txt + "]") + ',"color":"' + color + '","bold":true,"clickEvent":{"action":"run_command","value":"/trigger arena set ' + n + '"},"hoverEvent":{"action":"show_text","contents":' + JSON.stringify(hover) + '}}';
}
function habilitar(nm) { __run("scoreboard players set " + nm + " arena 0"); __run("scoreboard players enable " + nm + " arena"); }
function leerTrigger(nm) {
    try {
        var S = SL_SRV.getCurrentServer(), sb = S.m_129896_(), obj = sb.m_83477_("arena");
        if (!obj) return 0;
        if (!sb.m_83461_(nm, obj)) return 0;
        var sc = sb.m_83471_(nm, obj), v = sc.m_83400_();
        if (v != 0) { sc.m_83402_(0); __run("scoreboard players enable " + nm + " arena"); }
        return v;
    } catch (x) { return 0; }
}
function menuSets(nm) {
    habilitar(nm);
    var b = [];
    for (var i = 0; i < SETS.length; i++) b.push(boton(SET_NOMBRE[SETS[i]], i + 1, "aqua", SET_NOMBRE[SETS[i]] + ": " + SET_DESC[SETS[i]]));
    __run('tellraw ' + nm + ' ["",{"text":"⚔ Elige tu set para esta partida (no se puede cambiar): ","color":"gold"},' + b.join(',{"text":" "},') + ']');
}
function menuTienda(nm) {
    habilitar(nm);
    var d = ST.dat[nm], bolsa = Math.floor(ST.bolsa[nm] || 0), b = [];
    if (d.a < 3) b.push(boton("Arma → nv " + (d.a + 1) + " (" + COSTE[d.a + 1] + " pl)", 11, "green", "Mejora tu arma del set " + SET_NOMBRE[d.set]));
    if (d.r < 3) b.push(boton("Armadura → nv " + (d.r + 1) + " (" + COSTE[d.r + 1] + " pl)", 12, "green", "Mejora tu armadura del set " + SET_NOMBRE[d.set]));
    b.push(boton("Suministros (" + COSTE_SUM + " pl)", 13, "yellow", "Comida, agua y objetos de tu set"));
    b.push(boton("¡Listo!", 19, "red", "Empezar ya la siguiente oleada (si todos están listos)"));
    __run('tellraw ' + nm + ' ["",{"text":"⚒ Tienda de la arena — bolsa: ' + bolsa + ' de plata » ","color":"gold"},' + b.join(',{"text":" "},') + ']');
}

// ---------- Eventos ----------
function init(e) {
    try { quitarMobs(); } catch (x) { }
    __run("scoreboard objectives add arena trigger");
    marcarEnCurso(e.npc.getWorld(), null);
    ST = { modo: "libre" };
}

function dialog(e) {
    try {
        var id = e.dialog.getId();
        if (!((id >= D_SOLO0 && id < D_SOLO0 + NIVELES.length) || (id >= D_GRUPO0 && id < D_GRUPO0 + NIVELES.length) || id == D_DUELO || id == D_JDH || id == D_ESTADO)) return;
        __pend.push([nombre(e.player), id]);
        e.npc.getTimers().forceStart(79, 8, false);
    } catch (x) { print("[Arena] dialog: " + x); }
}

function timer(e) {
    if (e.id == 80) {
        for (var s = 0; s < __salida.length; s++) { try { tpSalida(e.npc, __salida[s]); devolver(e.npc.getWorld(), __salida[s]) || __devolver.push(__salida[s]); } catch (x) { } }
        __salida = [];
        return;
    }
    if (e.id != 79) return;
    var l = __pend; __pend = [];
    for (var i = 0; i < l.length; i++) {
        try {
            var p = e.npc.getWorld().getPlayer(l[i][0]);
            if (!p) continue;
            var id = l[i][1];
            if (id >= D_SOLO0 && id < D_SOLO0 + NIVELES.length) bestias(e.npc, p, id - D_SOLO0, false);
            else if (id >= D_GRUPO0 && id < D_GRUPO0 + NIVELES.length) bestias(e.npc, p, id - D_GRUPO0, true);
            else if (id == D_DUELO) duelo(e.npc, p);
            else if (id == D_JDH) jdh(e.npc, p);
            else estado(p);
        } catch (x) { print("[Arena] " + l[i][0] + ": " + x); }
    }
}

function tick(e) {
    if ((++__n) % 2 != 0) return;      // ~1 vez por segundo
    try { vigilar(e.npc); } catch (x) { print("[Arena] tick: " + x); }
    // devoluciones pendientes (gente que murió o se desconectó)
    if (__devolver.length) {
        var w = e.npc.getWorld(), quedan = [];
        for (var i = 0; i < __devolver.length; i++) if (!devolver(w, __devolver[i])) quedan.push(__devolver[i]);
        __devolver = quedan;
    }
}

// ---------- Estado / historial ----------
function ocupada(p) {
    if (ST.modo == "libre") return false;
    var t = { bestias: "un desafío de bestias", duelo_espera: "un duelo esperando rival", duelo: "un duelo",
              jdh_espera: "la inscripción de los Juegos de Eldoria", jdh: "los Juegos de Eldoria" }[ST.modo];
    decir(p, "El ruedo está ocupado: hay " + t + ". Espera a que termine.");
    return true;
}
function estado(p) {
    var sd = p.getStoreddata(), max = sd.has("sl_arena_max") ? Number(sd.get("sl_arena_max")) : 0;
    var lin = ["§6§l⚔ Tu historial en la Arena de Eldoria"];
    lin.push("§7Nivel más alto superado: §e" + (max > 0 ? NIVELES[max - 1].n + " (" + NIVELES[max - 1].nombre + ")" : "ninguno"));
    for (var i = 0; i < NIVELES.length; i++) {
        var k = "sl_arena_t" + (i + 1), lib = i <= max;
        var t = sd.has(k) ? Number(sd.get(k)) : 0, falta = t + DIA - ahora();
        var est = !lib ? "§8bloqueado" : (falta > 0 ? "§cpremio cobrado (vuelve en " + Math.ceil(falta / 3600000) + " h)" : "§apremio disponible");
        lin.push("§7Nivel " + NIVELES[i].n + " §8- §f" + NIVELES[i].nombre + " §8(" + textoPlata(NIVELES[i].plata) + ")§7: " + est);
    }
    lin.push("§7El ruedo está ahora: §e" + (ST.modo == "libre" ? "libre" : "ocupado"));
    p.message(lin.join("\n"));
}

// ---------- Inicio de partidas ----------
function prepararEleccion(w, modo, jug, extra) {
    ST = { modo: modo, jug: jug, inicio: seg(), fase: "eleccion", dat: {}, bolsa: {} };
    for (var k in extra) ST[k] = extra[k];
    for (var i = 0; i < jug.length; i++) { ST.dat[jug[i]] = { set: null, a: 0, r: 0, listo: false }; menuSets(jug[i]); }
}

function bestias(npc, p, idx, grupo) {
    if (ocupada(p)) return;
    var w = npc.getWorld();
    var jug = [nombre(p)];
    if (grupo) {
        var cerca = w.getNearbyEntities(npc.getPos(), 6, 1);
        for (var i = 0; i < cerca.length && jug.length < 5; i++) { var nm = "" + cerca[i].getName(); if (jug.indexOf(nm) < 0) jug.push(nm); }
        if (jug.length < 2) { decir(p, "Para luchar en grupo, tus compañeros tienen que estar a mi lado (a menos de 6 pasos)."); return; }
    }
    for (var j = 0; j < jug.length; j++) {
        var q = w.getPlayer(jug[j]); if (!q) continue;
        var max = q.getStoreddata().has("sl_arena_max") ? Number(q.getStoreddata().get("sl_arena_max")) : 0;
        if (idx > max) { decir(p, (jug[j] == nombre(p) ? "Aún no has" : jug[j] + " aún no ha") + " superado el nivel " + NIVELES[idx - 1].n + ". En mi arena se sube peldaño a peldaño."); return; }
        if (slaTieneGuardado(q)) { decir(p, jug[j] + " tiene equipo pendiente de devolver de otra partida. Que hable conmigo antes."); return; }
    }
    prepararEleccion(w, "bestias", jug, { nivel: idx, ola: 0 });
    for (var k = 0; k < jug.length; k++) decir(w.getPlayer(jug[k]), "Nivel " + NIVELES[idx].n + ": §e" + NIVELES[idx].nombre + "§r. Tienes " + ELEGIR + " segundos para elegir set en el chat.");
}

function duelo(npc, p) {
    var nm = nombre(p), w = npc.getWorld();
    if (ST.modo == "duelo_espera") {
        if (ST.jug[0] == nm) { decir(p, "Ya estás inscrito. Esperamos a un rival."); return; }
        if (slaTieneGuardado(p)) { decir(p, "Tienes equipo pendiente de devolver; habla conmigo cuando reaparezcas."); return; }
        if (!cobrar(nm, CUOTA_DUELO)) { decir(p, "La inscripción del duelo cuesta §e" + CUOTA_DUELO + " de plata§r."); return; }
        var a = ST.jug[0], bote = ST.bote + CUOTA_DUELO;
        prepararEleccion(w, "duelo", [a, nm], { bote: bote });
        todos("¡Duelo! " + a + " contra " + nm + ". Bote: " + textoPlata(bote) + ".");
        return;
    }
    if (ocupada(p)) return;
    if (slaTieneGuardado(p)) { decir(p, "Tienes equipo pendiente de devolver; habla conmigo cuando reaparezcas."); return; }
    if (!cobrar(nm, CUOTA_DUELO)) { decir(p, "La inscripción del duelo cuesta §e" + CUOTA_DUELO + " de plata§r."); return; }
    ST = { modo: "duelo_espera", jug: [nm], bote: CUOTA_DUELO, inicio: seg() };
    decir(p, "Inscrito. Si en " + DUELO_ESPERA + " segundos nadie acepta, te devuelvo la cuota.");
    todos(nm + " busca rival para un duelo. Quien acepte, que hable con Clock (" + CUOTA_DUELO + " de plata).");
}

function jdh(npc, p) {
    var nm = nombre(p);
    if (ST.modo == "jdh_espera") {
        if (ST.jug.indexOf(nm) >= 0) { decir(p, "Ya estás inscrito. Empezamos en " + Math.max(0, JDH_ESPERA - (seg() - ST.inicio)) + " segundos."); return; }
        if (slaTieneGuardado(p)) { decir(p, "Tienes equipo pendiente de devolver; habla conmigo cuando reaparezcas."); return; }
        if (!cobrar(nm, CUOTA_JDH)) { decir(p, "Entrar en los Juegos cuesta §e" + CUOTA_JDH + " de plata§r."); return; }
        ST.jug.push(nm); ST.bote += CUOTA_JDH;
        todos(nm + " entra en los Juegos de Eldoria (" + ST.jug.length + " inscritos, bote: " + textoPlata(ST.bote) + ").");
        return;
    }
    if (ocupada(p)) return;
    if (slaTieneGuardado(p)) { decir(p, "Tienes equipo pendiente de devolver; habla conmigo cuando reaparezcas."); return; }
    if (!cobrar(nm, CUOTA_JDH)) { decir(p, "Entrar en los Juegos cuesta §e" + CUOTA_JDH + " de plata§r."); return; }
    ST = { modo: "jdh_espera", jug: [nm], bote: CUOTA_JDH, inicio: seg() };
    todos("¡Se abren los Juegos de Eldoria! Todos contra todos, el último en pie se lleva el bote. Inscripción con Clock durante " + JDH_ESPERA + " segundos (" + CUOTA_JDH + " de plata, mínimo " + JDH_MIN + " luchadores).");
}

// ---------- Oleadas ----------
function lanzarOleada(w) {
    var nv = NIVELES[ST.nivel], ola = nv.olas[ST.ola], n = ST.jug.length, total = 0;
    for (var m = 0; m < ola.length; m++) {
        var tipo = ola[m][0], cant = ola[m][1], jefe = ola[m][2] == 1;
        if (!jefe && n > 1) cant = Math.round(cant * (1 + 0.5 * (n - 1)));
        for (var c = 0; c < cant; c++) {
            var ang = (total * 0.6) - 1.0, r = jefe ? 12 : 18;
            var x = Math.round(CX + Math.cos(ang) * r), z = Math.round(CZ + Math.sin(ang) * r), y = sueloY(w, x, z);
            __run("summon " + tipo + " " + (x + 0.5) + " " + y + " " + (z + 0.5) + " {Tags:[\"sl_arena_mob\",\"sl_arena_new\"],PersistenceRequired:1b,DeathLootTable:\"minecraft:empty\"}");
            total++;
        }
    }
    var subida = 1 + 0.15 * ST.ola;                 // cada oleada pega más fuerte
    var hp = nv.hp * subida * (1 + 0.8 * (n - 1)), dm = nv.dmg * subida * (1 + 0.1 * (n - 1));
    __run("execute as @e[tag=sl_arena_new] run attribute @s minecraft:generic.max_health modifier add 6a1e0000-0000-4000-8000-000000000001 arena_hp " + (hp - 1).toFixed(3) + " multiply_base");
    __run("execute as @e[tag=sl_arena_new] run attribute @s minecraft:generic.attack_damage modifier add 6a1e0000-0000-4000-8000-000000000002 arena_dmg " + (dm - 1).toFixed(3) + " multiply_base");
    __run("execute as @e[tag=sl_arena_new] run data merge entity @s {Health:100000f}");
    __run("tag @e[tag=sl_arena_new] remove sl_arena_new");
    ST.inicioOla = seg();
    for (var k = 0; k < ST.jug.length; k++) titulo(ST.jug[k], "Oleada " + (ST.ola + 1) + "/3", ST.ola == 2 ? "¡La oleada final!" : nv.nombre);
    print("[Arena] Nivel " + nv.n + " oleada " + (ST.ola + 1) + ": " + total + " criaturas");
}

function empezarCombate(npc) {
    var w = npc.getWorld(), dentro = [];
    var lvl = ST.modo == "bestias" ? 0 : 1;           // en PvP todos empiezan con el set a nivel 1
    for (var i = 0; i < ST.jug.length; i++) {
        var nm = ST.jug[i], d = ST.dat[nm];
        if (!d.set) { d.set = "guerrero"; decir(w.getPlayer(nm), "No elegiste set: entras como §eGuerrero§r."); }
        d.a = lvl; d.r = lvl;
        if (equipar(w, nm, d.set, lvl, lvl)) dentro.push(nm);
        else if (ST.modo != "bestias") pagar(nm, ST.modo == "duelo" ? CUOTA_DUELO : CUOTA_JDH);
    }
    var minimo = ST.modo == "bestias" ? 1 : (ST.modo == "duelo" ? 2 : JDH_MIN);
    if (dentro.length < minimo) {
        for (var j = 0; j < dentro.length; j++) { devolver(w, dentro[j]); if (ST.modo != "bestias") pagar(dentro[j], ST.modo == "duelo" ? CUOTA_DUELO : CUOTA_JDH); }
        todos("La partida se cancela: no hay luchadores suficientes.");
        ST = { modo: "libre" }; marcarEnCurso(w, null);
        return;
    }
    ST.jug = dentro;
    marcarEnCurso(w, dentro);
    var n = dentro.length;
    for (var k = 0; k < n; k++) {
        var ang = ST.modo == "bestias" ? Math.PI + (k - (n - 1) / 2) * 0.35 : (2 * Math.PI * k) / n;
        tpRuedo(w, dentro[k], ang, ST.modo == "bestias" ? 6 : (n == 2 ? 12 : 18));
        __run("effect give " + dentro[k] + " minecraft:resistance 6 4 true");
        if (ST.modo == "bestias") ST.bolsa[dentro[k]] = 0;
    }
    limpiarSuelo();
    ST.fase = "cuenta"; ST.cuenta = 5; ST.inicio = seg();
}

// ---------- Vigilancia (cada segundo) ----------
function vigilar(npc) {
    if (ST.modo == "libre") return;
    var w = npc.getWorld(), t = seg() - ST.inicio;

    if (ST.modo == "duelo_espera") {
        if (t >= DUELO_ESPERA) { pagar(ST.jug[0], ST.bote); decir(w.getPlayer(ST.jug[0]), "Nadie ha aceptado tu reto. Te devuelvo la cuota."); ST = { modo: "libre" }; }
        return;
    }
    if (ST.modo == "jdh_espera") {
        if (t >= JDH_ESPERA) {
            if (ST.jug.length < JDH_MIN) {
                for (var i = 0; i < ST.jug.length; i++) pagar(ST.jug[i], CUOTA_JDH);
                todos("Los Juegos se cancelan: no hubo suficientes luchadores (mínimo " + JDH_MIN + "). Se devuelven las cuotas.");
                ST = { modo: "libre" };
                return;
            }
            var bote = ST.bote, jug = ST.jug;
            prepararEleccion(w, "jdh", jug, { bote: bote });
            todos("¡Inscripción cerrada! " + jug.length + " luchadores eligen su set. Bote: " + textoPlata(bote) + ".");
        } else if ((JDH_ESPERA - t) == 30 || (JDH_ESPERA - t) == 10) {
            todos("Quedan " + (JDH_ESPERA - t) + " segundos para inscribirse en los Juegos (" + ST.jug.length + " inscritos).");
        }
        return;
    }

    // botones del chat
    for (var b = 0; b < ST.jug.length; b++) {
        var nm = ST.jug[b], v = leerTrigger(nm), d = ST.dat[nm];
        if (!v || !d) continue;
        if (ST.fase == "eleccion" && v >= 1 && v <= 6) {
            d.set = SETS[v - 1];
            decir(w.getPlayer(nm), "Set elegido: §e" + SET_NOMBRE[d.set] + "§r (" + SET_DESC[d.set] + ").");
        } else if (ST.fase == "tienda") comprar(w, nm, v);
    }

    if (ST.fase == "eleccion") {
        var listos = true;
        for (var c = 0; c < ST.jug.length; c++) if (!ST.dat[ST.jug[c]].set) listos = false;
        if (listos || t >= ELEGIR) empezarCombate(npc);
        return;
    }

    if (ST.fase == "cuenta") {
        for (var a = 0; a < ST.jug.length; a++) titulo(ST.jug[a], ST.cuenta > 0 ? "" + ST.cuenta : "¡A LUCHAR!", "");
        if (ST.cuenta <= 0) { ST.fase = "lucha"; if (ST.modo == "bestias") lanzarOleada(w); }
        ST.cuenta--;
        return;
    }

    var vivos = activos(w);
    // los que caen o salen del ruedo pierden el equipo de la arena y recuperan el suyo
    for (var q = 0; q < ST.jug.length; q++) {
        if (vivos.indexOf(ST.jug[q]) < 0 && !ST.dat[ST.jug[q]].fuera) {
            ST.dat[ST.jug[q]].fuera = true;
            if (!devolver(w, ST.jug[q])) __devolver.push(ST.jug[q]);
            if (ST.modo == "bestias") ST.bolsa[ST.jug[q]] = 0;
        }
    }
    marcarEnCurso(w, vivos);

    if (ST.modo == "bestias") {
        limpiarSuelo();
        if (vivos.length == 0) {
            quitarMobs(); limpiarSuelo(); limpiarCadaveres();
            todos(ST.jug.join(", ") + (ST.jug.length > 1 ? " han caído" : " ha caído") + " en la oleada " + (ST.ola + 1) + " del nivel " + NIVELES[ST.nivel].n + ".");
            ST = { modo: "libre" }; marcarEnCurso(w, null);
            return;
        }
        if (ST.fase == "tienda") {
            var todosListos = true;
            for (var r = 0; r < vivos.length; r++) if (!ST.dat[vivos[r]].listo) todosListos = false;
            if (todosListos || t >= TIENDA) {
                ST.ola++; ST.fase = "cuenta"; ST.cuenta = 3; ST.inicio = seg();
                for (var s = 0; s < vivos.length; s++) ST.dat[vivos[s]].listo = false;
            } else if ((TIENDA - t) == 10) for (var s2 = 0; s2 < vivos.length; s2++) decir(w.getPlayer(vivos[s2]), "10 segundos para la siguiente oleada.");
            return;
        }
        if (vivosMobs() == 0) { oleadaSuperada(npc, vivos); return; }
        if (seg() - ST.inicioOla >= TIEMPO_OLEADA) {
            quitarMobs(); limpiarSuelo(); limpiarCadaveres();
            for (var v = 0; v < vivos.length; v++) { decir(w.getPlayer(vivos[v]), "Se acabó el tiempo. Las bestias se retiran: hoy no hay premio."); __salida.push(vivos[v]); }
            npc.getTimers().forceStart(80, 40, false);
            ST = { modo: "libre" }; marcarEnCurso(w, null);
        }
        return;
    }

    // duelo / juegos
    if (vivos.length == 1) {
        var gan = vivos[0];
        pagar(gan, ST.bote);
        titulo(gan, "¡VICTORIA!", "Ganas " + textoPlata(ST.bote));
        decir(w.getPlayer(gan), "El público de Valdoria grita tu nombre. Aquí tienes el bote: §e" + textoPlata(ST.bote) + "§r.");
        todos(gan + " gana " + (ST.modo == "duelo" ? "el duelo" : "los Juegos de Eldoria") + " y se lleva " + textoPlata(ST.bote) + ".");
        print("[Arena] " + ST.modo + " ganado por " + gan + " (" + ST.bote + " plata)");
        __salida = [gan]; npc.getTimers().forceStart(80, 100, false);
        limpiarCadaveres();
        ST = { modo: "libre" }; marcarEnCurso(w, null);
        return;
    }
    if (vivos.length == 0) {
        var rep = Math.floor(ST.bote / ST.jug.length);
        for (var r2 = 0; r2 < ST.jug.length; r2++) pagar(ST.jug[r2], rep);
        todos("Nadie queda en pie: empate y se reparte el bote.");
        limpiarCadaveres();
        ST = { modo: "libre" }; marcarEnCurso(w, null);
        return;
    }
    if (t >= TIEMPO_OLEADA * 2) {
        var rep2 = Math.floor(ST.bote / vivos.length);
        for (var s3 = 0; s3 < vivos.length; s3++) { pagar(vivos[s3], rep2); __salida.push(vivos[s3]); }
        npc.getTimers().forceStart(80, 40, false);
        todos("Se acabó el tiempo: empate entre " + vivos.join(", ") + ". El bote se reparte entre los supervivientes.");
        limpiarCadaveres();
        ST = { modo: "libre" }; marcarEnCurso(w, null);
    }
}

function comprar(w, nm, v) {
    var d = ST.dat[nm], p = w.getPlayer(nm), bolsa = ST.bolsa[nm] || 0;
    if (!d || d.fuera) return;
    if (v == 19) { d.listo = true; decir(p, "Preparado. Empezamos cuando todos lo estéis."); return; }
    var coste = v == 11 ? COSTE[d.a + 1] : (v == 12 ? COSTE[d.r + 1] : (v == 13 ? COSTE_SUM : -1));
    if (coste < 0 || (v == 11 && d.a >= 3) || (v == 12 && d.r >= 3)) return;
    if (bolsa < coste) { decir(p, "No te llega: tu bolsa tiene " + Math.floor(bolsa) + " de plata y cuesta " + coste + "."); return; }
    ST.bolsa[nm] = bolsa - coste;
    if (v == 11) { d.a++; darArma(nm, d.set, d.a); decir(p, "Arma mejorada a nivel §e" + d.a + "§r."); }
    else if (v == 12) { d.r++; equiparArmadura(nm, d.set, d.r); decir(p, "Armadura mejorada a nivel §e" + d.r + "§r."); }
    else { suministros(nm, d.set, false); decir(p, "Suministros entregados."); }
    menuTienda(nm);
}

function oleadaSuperada(npc, vivos) {
    var w = npc.getWorld(), nv = NIVELES[ST.nivel], ganado = nv.plata * REPARTO[ST.ola];
    limpiarSuelo();
    for (var i = 0; i < vivos.length; i++) ST.bolsa[vivos[i]] = (ST.bolsa[vivos[i]] || 0) + ganado;
    if (ST.ola < nv.olas.length - 1) {
        for (var j = 0; j < vivos.length; j++) {
            titulo(vivos[j], "Oleada superada", "+" + textoPlata(ganado) + " a tu bolsa");
            __run("effect give " + vivos[j] + " minecraft:regeneration 8 1 true");
            menuTienda(vivos[j]);
        }
        ST.fase = "tienda"; ST.inicio = seg();
        return;
    }
    victoriaBestias(npc, vivos);
}

function victoriaBestias(npc, vivos) {
    var w = npc.getWorld(), idx = ST.nivel, nv = NIVELES[idx];
    quitarMobs(); limpiarSuelo(); limpiarCadaveres();
    for (var i = 0; i < vivos.length; i++) {
        var p = w.getPlayer(vivos[i]); if (!p) continue;
        var sd = p.getStoreddata(), k = "sl_arena_t" + (idx + 1), bolsa = Math.floor(ST.bolsa[vivos[i]] || 0);
        var max = sd.has("sl_arena_max") ? Number(sd.get("sl_arena_max")) : 0;
        if (idx + 1 > max) { sd.put("sl_arena_max", idx + 1); if (idx + 1 < NIVELES.length) p.message("§a✔ Has desbloqueado el nivel " + NIVELES[idx + 1].n + ": " + NIVELES[idx + 1].nombre + "."); }
        var last = sd.has(k) ? Number(sd.get(k)) : 0;
        if (ahora() - last >= DIA) {
            sd.put(k, ahora());
            if (bolsa > 0) pagar(vivos[i], bolsa);
            __run("xp add " + vivos[i] + " " + nv.xp + " points");
            titulo(vivos[i], "¡VICTORIA!", textoPlata(bolsa) + " y " + nv.xp + " de experiencia");
            decir(p, "Has superado el nivel " + nv.n + ". Tu premio: §e" + textoPlata(bolsa) + "§r (lo que quedaba en tu bolsa) y §a" + nv.xp + " puntos de experiencia§r.");
        } else {
            titulo(vivos[i], "¡VICTORIA!", "Premio ya cobrado hoy");
            decir(p, "Has vencido, pero el premio de este nivel ya lo cobraste en las últimas 24 horas.");
        }
    }
    todos(vivos.join(", ") + (vivos.length > 1 ? " han superado" : " ha superado") + " el nivel " + nv.n + ": " + nv.nombre + ".");
    print("[Arena] Nivel " + nv.n + " superado por " + vivos.join(", "));
    __salida = vivos.slice();
    ST = { modo: "libre" }; marcarEnCurso(w, null);
    npc.getTimers().forceStart(80, 60, false);
}
