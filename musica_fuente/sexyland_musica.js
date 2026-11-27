// SexyLand - musica ambiental por zonas (requiere el paquete de recursos "SexyLand_Musica").
// Suena solo para los jugadores que estan DENTRO de la zona; al salir se corta.
var SLM_SRV = Java.type("net.minecraftforge.server.ServerLifecycleHooks");
var SLM_SYS = Java.type("java.lang.System");

var SLM_ZONAS = [
    {
        id: "castillo", dim: "minecraft:overworld",
        x1: 834, x2: 893, y1: 130, y2: 320, z1: 268, z2: 351,
        volumen: 0.7,
        pistas: [
            ["sexyland:castillo.danza_hungara_5", 84.1],
            ["sexyland:castillo.canon_pachelbel", 135.2],
            ["sexyland:castillo.serenata_mozart", 64.7],
            ["sexyland:castillo.minueto_bach", 157.4],
            ["sexyland:castillo.jesus_alegria_bach", 69.4],
            ["sexyland:castillo.greensleeves", 167.4],
            ["sexyland:castillo.primavera_vivaldi", 47.2],
            ["sexyland:castillo.ambiente_salon", 177.7]
        ]
    }
];

function slmCmd(c) {
    var S = SLM_SRV.getCurrentServer();
    try { return S.m_129892_().m_230957_(S.m_129893_().m_81324_(), c); } catch (x) { print("[SexyLand musica] " + x); return 0; }
}

function slmDim(p) {
    try { return "" + p.getMCEntity().m_9236_().m_46472_().m_135782_(); } catch (x) { return ""; }
}

function slmZona(p) {
    var d = slmDim(p), x = p.getX(), y = p.getY(), z = p.getZ();
    for (var i = 0; i < SLM_ZONAS.length; i++) {
        var Z = SLM_ZONAS[i];
        if (d == Z.dim && x >= Z.x1 && x <= Z.x2 + 1 && y >= Z.y1 && y <= Z.y2 && z >= Z.z1 && z <= Z.z2 + 1) return Z;
    }
    return null;
}

function slmParar(p, td) {
    if (td.has("slm_ev")) slmCmd("stopsound " + p.getName() + " record " + td.get("slm_ev"));
    td.remove("slm_ev"); td.remove("slm_zona"); td.remove("slm_fin");
}

function slmMusica(p) {
    var td = p.getTempdata();
    var Z = slmZona(p);
    var zonaAct = td.has("slm_zona") ? "" + td.get("slm_zona") : "";
    if (!Z) { if (zonaAct) slmParar(p, td); return; }
    if (zonaAct && zonaAct != Z.id) slmParar(p, td);
    var ahora = SLM_SYS.currentTimeMillis();
    var fin = td.has("slm_fin") ? Number(td.get("slm_fin")) : 0;
    if (td.has("slm_zona") && ahora < fin) return;
    // elegir pista distinta de la anterior
    var prev = td.has("slm_prev") ? "" + td.get("slm_prev") : "";
    var k, n = Z.pistas.length, tries = 0;
    do { k = Math.floor(Math.random() * n); tries++; } while (n > 1 && Z.pistas[k][0] == prev && tries < 10);
    var ev = Z.pistas[k][0], dur = Z.pistas[k][1];
    var nm = "" + p.getName();
    slmCmd("execute as " + nm + " at @s run playsound " + ev + " record @s ~ ~ ~ " + Z.volumen + " 1 1");
    td.put("slm_ev", ev); td.put("slm_prev", ev); td.put("slm_zona", Z.id);
    // pausa de 6 a 14 s entre piezas
    td.put("slm_fin", ahora + Math.round(dur * 1000) + 6000 + Math.floor(Math.random() * 8000));
}

function tick(e) {
    try {
        var p = e.player, td = p.getTempdata();
        var t = p.getWorld().getTotalTime();
        var ult = td.has("slm_t") ? Number(td.get("slm_t")) : 0;
        if (t - ult < 20 && t >= ult) return;
        td.put("slm_t", t);
        slmMusica(p);
    } catch (x) { print("[SexyLand musica] tick: " + x); }
}

function logout(e) {
    try { e.player.getTempdata().remove("slm_zona"); } catch (x) { }
}
