// SexyLand - Arena de Eldoria: guardado y devolución del inventario real (compartido por Clock y el script de jugadores)
var SLA_SRV = Java.type("net.minecraftforge.server.ServerLifecycleHooks");
var SLA_CA = Java.type("top.theillusivec4.curios.api.CuriosApi");
var SLA_NBT = Java.type("net.minecraft.nbt.NbtIo");
var SLA_CT = Java.type("net.minecraft.nbt.CompoundTag");
var SLA_LT = Java.type("net.minecraft.nbt.ListTag");
var SLA_FILE = Java.type("java.io.File");
var SLA_DIR = "world/sexyland_arena";

function slaRun(c) {
    var S = SLA_SRV.getCurrentServer();
    try { return S.m_129892_().m_230957_(S.m_129893_().m_81324_(), c); } catch (x) { return 0; }
}
function slaArchivo(uuid) { return new SLA_FILE(SLA_DIR + "/" + uuid + ".dat"); }
function slaTieneGuardado(p) { try { return slaArchivo("" + p.getUUID()).exists(); } catch (x) { return false; } }
function slaCurios(mp) { var o = SLA_CA.getCuriosInventory(mp); return o.isPresent() ? o.resolve().get() : null; }

// Guarda inventario + Curios en disco y deja al jugador vacío. Devuelve true si todo fue bien.
function slaGuardar(p) {
    var uuid = "" + p.getUUID(), f = slaArchivo(uuid);
    if (f.exists()) return true;                       // ya estaba guardado (no pisar el original)
    var mp = p.getMCEntity(), inv = mp.m_150109_();
    var tag = new SLA_CT();
    var lista = inv.m_36026_(new SLA_LT());
    tag.m_128365_("inv", lista);
    var cur = slaCurios(mp), curL = null;
    if (cur) { curL = cur.saveInventory(false); tag.m_128365_("curios", curL); }
    tag.m_128359_("nombre", "" + p.getName());
    tag.m_128405_("xpNivel", Number(slaRun("xp query " + p.getName() + " levels")) | 0);
    tag.m_128405_("xpPuntos", Number(slaRun("xp query " + p.getName() + " points")) | 0);
    new SLA_FILE(SLA_DIR).mkdirs();
    SLA_NBT.m_128944_(tag, f);
    // comprobar que se puede leer antes de vaciar nada
    var chk = SLA_NBT.m_128937_(f);
    if (!chk || chk.m_128437_("inv", 10).size() != lista.size()) { try { f["delete"](); } catch (x) { } return false; }
    inv.m_6211_();
    if (cur) cur.saveInventory(true);
    print("[Arena] Inventario de " + p.getName() + " guardado (" + lista.size() + " pilas)");
    return true;
}

// Devuelve el inventario guardado (borra antes lo que lleve de la arena). Devuelve true si había algo que devolver.
function slaDevolver(p) {
    var uuid = "" + p.getUUID(), f = slaArchivo(uuid);
    if (!f.exists()) return false;
    var tag = SLA_NBT.m_128937_(f);
    var mp = p.getMCEntity(), inv = mp.m_150109_();
    inv.m_6211_();
    var cur = slaCurios(mp);
    if (cur) cur.saveInventory(true);
    inv.m_36035_(tag.m_128437_("inv", 10));
    if (cur && tag.m_128441_("curios")) cur.loadInventory(tag.m_128437_("curios", 10));
    mp.f_36095_.m_38946_();
    // si murió en la arena perdió su experiencia real: se la devolvemos (los premios ganados se respetan)
    if (tag.m_128441_("xpNivel")) {
        var lv = tag.m_128451_("xpNivel"), pt = tag.m_128451_("xpPuntos");
        var clv = Number(slaRun("xp query " + p.getName() + " levels")) | 0, cpt = Number(slaRun("xp query " + p.getName() + " points")) | 0;
        if (clv < lv || (clv == lv && cpt < pt)) {
            slaRun("xp set " + p.getName() + " " + lv + " levels");
            slaRun("xp set " + p.getName() + " " + pt + " points");
        }
    }
    // guardar copia del último devuelto por si hubiera que revisar algo
    var bak = new SLA_FILE(SLA_DIR + "/" + uuid + ".devuelto.dat");
    try { if (bak.exists()) bak["delete"](); } catch (x) { }
    f.renameTo(bak);
    var efs = ["strength", "resistance", "health_boost", "speed", "jump_boost", "regeneration", "absorption"];
    for (var i = 0; i < efs.length; i++) slaRun("effect clear " + p.getName() + " minecraft:" + efs[i]);
    print("[Arena] Inventario devuelto a " + p.getName());
    return true;
}

// ¿Está este jugador en una pelea en curso? (lo mantiene Clock en los datos del mundo)
function slaEnCombate(p) {
    try {
        var sd = p.getWorld().getStoreddata();
        if (!sd.has("sl_arena_en_curso")) return false;
        return ("," + sd.get("sl_arena_en_curso") + ",").indexOf("," + p.getName() + ",") >= 0;
    } catch (x) { return false; }
}
