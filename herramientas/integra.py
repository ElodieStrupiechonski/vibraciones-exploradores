#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Registra los exploradores nuevos en temario.json y actualiza la barra de navegación y el índice sin regenerar
las páginas (equivale a build_index.py + add_navbar.py para las altas de noviembre de 2026). Idempotente.
Uso: python3 integra.py CARPETA"""
import json, os, re, sys, html
D = sys.argv[1]; esc = lambda s: html.escape(s, quote=True)
tp = os.path.join(D, "temario.json"); T = json.load(open(tp, encoding="utf-8")); P = T["paginas"]
NUEVAS = {
 "senales_interactivo.html": (7, {"corto": "Pilar 11 · Laboratorio de señales", "titulo": "Laboratorio de señales",
   "enfoque": "MEDIR · muestreo, ventanas y promedio de Welch",
   "descripcion": "Una señal sintética o un CSV de Phyphox se muestrea, se corta en segmentos y se promedia: aliasing, fuga, resolución y error aleatorio a la vista.",
   "puntos": ["Aliasing: f_a = |f − k·f_s|", "Δf = 1/T_seg y ε_r ≈ 1/√n_d", "G_rms como área de la PSD (Parseval)"], "tema": "temas 7.1–7.2", "swatch": ["#2E5496", "#2E7D46"]}),
 "dosgdl_interactivo.html": (8, {"corto": "Pilar 12 · Dos grados de libertad", "titulo": "Dos grados de libertad y absorbedor",
   "enfoque": "ACOPLAR · modos, antirresonancia y riesgo por acoplamiento",
   "descripcion": "Al montar un segundo sistema sobre la estructura, la resonancia se divide en dos modos; un absorbedor sintonizado anula la respuesta en su frecuencia.",
   "puntos": ["Valores propios: ω_1, ω_2 y formas modales", "Absorbedor dinámico y óptimo de Den Hartog", "Separación de frecuencias equipo–estructura"], "tema": "temas 8.1–8.3", "swatch": ["#1F3864", "#6B3FA0"]}),
}
for f, (n, d) in NUEVAS.items():
    P[f] = d
    u = next(x for x in T["unidades"] if x["n"] == n)
    if f not in u.setdefault("paginas", []): u["paginas"].append(f)
    u.pop("proximamente", None)
    if f not in T["recorrido"]: T["recorrido"].append(f)
T["actualizado"] = "2026-11-11"
json.dump(T, open(tp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def menu():
    g = []; fu = T["fundamentos"]
    it = lambda f, sub: f'<a href="{f}" data-nv="{f}">{esc(P[f]["titulo"])} <small>{esc(sub)}</small></a>'
    g.append(f'<div class="nv-grp">{esc(fu["titulo"] + " · conocimiento previo")}</div>')
    g += [it(f, P[f]["corto"].split(" · ")[0] + " · " + P[f].get("tema", "")) for f in fu["paginas"]]
    for u in T["unidades"]:
        g.append(f'<div class="nv-grp">{esc("Unidad %s · %s" % (u["n"], u["titulo"]) + (" · %s h" % u["horas"] if u.get("horas") else ""))}</div>')
        items = [it(f, P[f]["corto"].split(" · ")[0] + " · " + P[f].get("tema", "")) for f in u.get("paginas", [])] + [it(f, P[f].get("tema", "apoyo")) for f in u.get("apoyo", [])]
        g += items or ['<span class="nv-vacio">sin explorador todavía</span>']
    return "\n".join(g)

ref = open(os.path.join(D, "mediapotencia_interactivo.html"), encoding="utf-8").read()
NAV = re.search(r"<!-- navbar:inicio -->.*?<!-- navbar:fin -->\n?", ref, re.S).group(0)
def con_menu(b): return re.sub(r'(<div class="nv-menu">\n).*?(\s*<div class="nv-pie">)', lambda m: m.group(1) + menu() + "\n" + m.group(2), b, count=1, flags=re.S)
NAV = con_menu(NAV)
for f in sorted(x for x in os.listdir(D) if x.endswith(".html")):
    p = os.path.join(D, f); s = open(p, encoding="utf-8").read()
    s = re.sub(r"<!-- navbar:inicio -->.*?<!-- navbar:fin -->\n?", "", s, flags=re.S)
    assert s.count("</body>") == 1, f
    s = s.replace("</body>", NAV + "</body>", 1)
    open(p, "w", encoding="utf-8").write(s)

# ---- índice: tarjetas de las unidades que estrenan explorador
ip = os.path.join(D, "index.html"); s = open(ip, encoding="utf-8").read()
def card(f, eyebrow):
    p = P[f]; sw = p["swatch"]; pts = " · ".join(p.get("puntos", []))
    return f'''<div class="cw"><a class="card" href="{f}">
      <div class="swatch" style="background:linear-gradient(90deg,{sw[0]},{sw[1]})"></div>
      <div class="u">{esc(eyebrow)}</div>
      <div class="ct">{esc(p["titulo"])}</div>
      <div class="ce">{esc(p["enfoque"])}</div>
      <div class="cd">{esc(p["descripcion"])}</div>
      <div class="cp">{esc(pts)}</div>
      <div class="chip">Abrir explorador →</div>
    </a></div>'''
for f, (n, d) in NUEVAS.items():
    if f'href="{f}"' in s.split("<!-- navbar:inicio -->")[0]: continue
    pat = re.compile(r'(<div class="sk">Unidad %d<small>.*?)<div class="nota">.*?</div>' % n, re.S)
    assert pat.search(s), "no se encontró la sección de la unidad %d" % n
    s = pat.sub(lambda m: m.group(1) + '<div class="grid">\n' + card(f, "Unidad %d · %s · %s" % (n, d["tema"], d["corto"].split(" · ")[0])) + "\n</div>", s, count=1)
s = s.replace("abrir el temario desde cualquier página. Las hojas", "abrir el temario desde cualquier página. En cada explorador los valores se fijan con el deslizador o se escriben con el teclado en la casilla contigua (Enter los aplica). Las hojas") if "se escriben con el teclado" not in s else s
open(ip, "w", encoding="utf-8").write(s)
print("temario:", len(P), "páginas; barra e índice actualizados")
