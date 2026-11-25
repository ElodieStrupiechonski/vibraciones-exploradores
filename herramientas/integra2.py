#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Versión 1.3 (noviembre de 2026; durante su preparación se llamó «revisión 1.2»): integra los exploradores nuevos y homologa el sitio con el de Teoría
Electromagnética. Idempotente. Uso: python3 integra2.py CARPETA

  1. temario.json: altas (analogías, transmisibilidad, tutorial, extracción modal), orden por unidad del programa.
  2. Navegación: el menú superior («navbar») se sustituye por el panel lateral fijo («navegacion») del sitio de
     Teoría Electromagnética: anterior/siguiente con nombre, buscador (tecla /), lista por unidades, ☰ en móvil.
  3. Bloques «movil» y «seo» (descripción, canónica, Open Graph y JSON-LD) en todas las páginas; sitemap.xml.
  4. Índice: las secciones de cada unidad se regeneran desde temario.json.
  5. Versión 1.3 en pies de página, CITATION.cff, .zenodo.json y README.
"""
import json, os, re, sys, html
D = sys.argv[1]; esc = lambda s: html.escape(s, quote=True)
VERSION, FECHA = "1.6", "2026-11-25"
BASE = "https://elodiestrupiechonski.github.io/vibraciones-exploradores/"
DOI = "10.5281/zenodo.23422993"
tp = os.path.join(D, "temario.json"); T = json.load(open(tp, encoding="utf-8")); P = T["paginas"]

# ------------------------------------------------------------------------------------------------ 1. temario
NUEVAS = {
 "analogias_interactivo.html": (2, {"corto": "Pilar 14 · Analogías entre sistemas", "titulo": "Analogías entre sistemas",
   "enfoque": "MODELAR · una misma ecuación en cuatro dominios",
   "descripcion": "Al fijar masa, amortiguador y resorte se obtienen el circuito RLC análogo, el sistema de torsión y el hidráulico, con la misma frecuencia natural y el mismo amortiguamiento.",
   "puntos": ["Analogías fuerza-tensión y fuerza-corriente", "Escala de impedancia: ω_n y ζ no cambian", "Chapoteo, paneles y control de actitud"], "tema": "temas 2.1 y 2.4", "swatch": ["#2E5496", "#C55A11"],
   "claves": ["analogía electromecánica", "circuito RLC", "sistemas de segundo orden"]}),
 "transmisibilidad_interactivo.html": (6, {"corto": "Pilar 13 · Transmisibilidad y aislamiento", "titulo": "Transmisibilidad y aislamiento",
   "enfoque": "AISLAR · cuánto pasa del piso al equipo",
   "descripcion": "Al variar masa, rigidez, amortiguamiento y frecuencia se lee cuánto movimiento o cuánta fuerza se transmite, y desde qué frecuencia el soporte aísla.",
   "puntos": ["T_r = 1 en r = √2 para todo ζ", "Deflexión estática: δ_st = g/ω_n^2", "Desbalance rotatorio: F_0 = m_0 e ω^2"], "tema": "tema 6.3", "swatch": ["#2E7D46", "#2E5496"],
   "claves": ["transmisibilidad", "aislamiento de vibraciones", "desbalance rotatorio"]}),
 "tutorial_phyphox.html": (7, {"corto": "Tutorial · Phyphox y Python", "titulo": "Tutorial: medir con Phyphox y analizar en Python",
   "enfoque": "MEDIR · del teléfono a f_n y ζ en siete pasos",
   "descripcion": "Ligas para instalar Phyphox y descargar el cuaderno de Jupyter, instrucciones para Colab y Visual Studio Code, y un analizador que reproduce el tratamiento del decaimiento.",
   "puntos": ["Descarga de Phyphox, cuaderno y datos de ejemplo", "Colab o Visual Studio Code, paso a paso", "Envolvente de Hilbert y decremento logarítmico"], "tema": "tema 7.1", "swatch": ["#C55A11", "#2E7D46"],
   "claves": ["Phyphox", "acelerómetro del teléfono", "decremento logarítmico", "Jupyter"]}),
 "modal_interactivo.html": (7, {"corto": "Pilar 15 · Extracción modal", "titulo": "Extracción de parámetros modales",
   "enfoque": "IDENTIFICAR · f_n y ζ desde la FRF",
   "descripcion": "Sobre una función de respuesta en frecuencia con dos modos y ruido se comparan tres métodos: media potencia, círculo de Nyquist y recta de la FRF inversa.",
   "puntos": ["Media potencia: ζ = (f_b − f_a)/(2 f_n)", "Círculo de Nyquist por mínimos cuadrados", "Resolución necesaria: T ≥ 2/(ζ f_n)"], "tema": "tema 7.3", "swatch": ["#6B3FA0", "#2E5496"],
   "claves": ["análisis modal experimental", "función de respuesta en frecuencia", "diagrama de Nyquist"]}),
 "choque_interactivo.html": (7, {"corto": "Pilar 16 · Choque y SRS", "titulo": "Ensayo de choque y espectro de respuesta",
   "enfoque": "ENSAYAR · qué recibe cada componente en un choque",
   "descripcion": "Un pulso de semiseno, diente de sierra o rectangular sacude la base; el espectro de respuesta al choque muestra la aceleración máxima de cada componente según su frecuencia natural.",
   "puntos": ["SRS: máximo de |a(t)| para cada f_n, con Q = 10", "Blando: 2π f_n Δv; rígido: A", "Senoidal, aleatorio y choque; diagnóstico por corrimiento de f_n"], "tema": "tema 7.4", "swatch": ["#B23A3A", "#2E5496"],
   "claves": ["ensayo de choque", "espectro de respuesta al choque", "SRS", "semiseno", "prueba de vibración"]}),
 "esfuerzos_interactivo.html": (5, {"corto": "Pilar 17 · Esfuerzos directos", "titulo": "Esfuerzos directos en una unión con pernos",
   "enfoque": "DIMENSIONAR · cuatro maneras de fallar, cuatro áreas",
   "descripcion": "En una unión a traslape con pernos se calculan el cortante del perno, el aplastamiento, la tensión en la sección neta y el desgarre, y se identifica el modo que gobierna.",
   "puntos": ["σ = P/A y τ = V/A: cada modo tiene su área", "Cortante simple y cortante doble", "Factor de seguridad y carga que inicia la fluencia"], "tema": "temas 5.1 y 5.2", "swatch": ["#2E5496", "#B23A3A"],
   "claves": ["esfuerzo normal", "esfuerzo cortante directo", "aplastamiento", "unión atornillada", "sección neta", "remache"]}),
 "perdida_interactivo.html": (6, {"corto": "Pilar 18 · Pérdida por transmisión", "titulo": "Pérdida por transmisión de un panel",
   "enfoque": "AISLAR · cuánto sonido atraviesa un panel",
   "descripcion": "Al variar material, espesor y amortiguamiento de un panel se obtiene su pérdida por transmisión en cada frecuencia: ley de masa, caída por coincidencia y zona controlada por el amortiguamiento.",
   "puntos": ["Ley de masa: +6 dB por duplicar m″ o f", "Frecuencia crítica: f_c h es constante del material", "Sobre f_c solo ayuda el amortiguamiento"], "tema": "tema 6.3 (vía aérea)", "swatch": ["#6B3FA0", "#2E7D46"],
   "claves": ["pérdida por transmisión", "ley de masa", "frecuencia crítica", "coincidencia", "aislamiento acústico", "fuselaje"]}),
 "anecoica_interactivo.html": (6, {"corto": "Pilar 19 · Cámara anecoica", "titulo": "Campo libre y cámara anecoica",
   "enfoque": "MEDIR · dónde termina el campo libre",
   "descripcion": "Nivel sonoro en función de la distancia en un recinto: campo directo, campo reverberante, radio crítico y frecuencia de corte de las cuñas de una cámara anecoica.",
   "puntos": ["L_p = L_W + 10 log(Q/4πr² + 4/R)", "Radio crítico: r_c = √(QR/16π)", "Cuñas: profundidad de un cuarto de onda"], "tema": "tema 6.4", "swatch": ["#C55A11", "#4472C4"],
   "claves": ["cámara anecoica", "campo libre", "campo reverberante", "radio crítico", "tiempo de reverberación", "cámara reverberante"]}),
}
ORDEN = {2: ["analogias_interactivo.html", "coulomb_interactivo.html"],
         5: ["esfuerzos_interactivo.html", "mohr_interactivo.html", "fatiga_interactivo.html"],
         6: ["sonido_interactivo.html", "transmisibilidad_interactivo.html", "perdida_interactivo.html", "anecoica_interactivo.html"],
         7: ["tutorial_phyphox.html", "senales_interactivo.html", "modal_interactivo.html", "choque_interactivo.html"]}
CLAVES = {"complejos_interactivo.html": ["números complejos", "fasores"], "edo_interactivo.html": ["ecuaciones diferenciales de segundo orden", "amortiguamiento"],
          "edo3_interactivo.html": ["segunda ley de Newton", "frecuencia natural"], "coulomb_interactivo.html": ["fricción de Coulomb", "vibración libre"],
          "forzada_interactivo.html": ["respuesta forzada", "resonancia"], "mediapotencia_interactivo.html": ["método de media potencia", "factor de calidad"],
          "espectro_interactivo.html": ["vibración aleatoria", "densidad espectral de potencia", "ecuación de Miles"], "mohr_interactivo.html": ["círculo de Mohr", "criterios de falla"],
          "fatiga_interactivo.html": ["fatiga", "regla de Miner"], "sonido_interactivo.html": ["nivel de presión sonora", "bandas de octava", "exposición al ruido"],
          "senales_interactivo.html": ["muestreo", "aliasing", "método de Welch"], "dosgdl_interactivo.html": ["dos grados de libertad", "absorbedor dinámico"],
          "normas.html": ["normas de ensayo", "GEVS", "ECSS"]}
for f, (n, d) in NUEVAS.items(): P[f] = d
for f, c in CLAVES.items(): P[f]["claves"] = c
P["sonido_interactivo.html"]["tema"] = "temas 6.1, 6.2 y 6.4"
P["coulomb_interactivo.html"]["tema"] = "tema 2.3 (fricción seca)"
PEND = {1: "1.1 (conceptos generales de ruido y vibraciones)", 4: "4.4 (elementos de falla más comunes)"}
REMITE = {2: ("Los temas 2.2 y 2.3 (sistema masa-resorte-amortiguador y sus tres regímenes) se trabajan en los pilares de fundamentos; el 2.5 (acoplamiento), en el explorador de dos grados de libertad.",
              ["edo3_interactivo.html", "edo_interactivo.html", "dosgdl_interactivo.html"]),
          3: ("El análisis modal (3.2) continúa en la unidad 7 con la extracción de parámetros modales, y la transmisión de la vibración al soporte, en la unidad 6.",
              ["modal_interactivo.html", "transmisibilidad_interactivo.html"])}
for u in T["unidades"]:
    u.pop("pendientes", None)
    if u["n"] in PEND: u["pendientes"] = PEND[u["n"]]
    if u["n"] in REMITE: u["remite"], u["remite_a"] = REMITE[u["n"]]
for u in T["unidades"]:
    if u["n"] in ORDEN: u["paginas"] = ORDEN[u["n"]]
    u.pop("proximamente", None)
uni1 = next(u for u in T["unidades"] if u["n"] == 1)
uni1["remite"] = "Esta unidad se apoya en los pilares de fundamentos (vibración libre, frecuencia natural, amortiguamiento) y, para los sistemas rotatorios del tema 1.2, en el explorador de transmisibilidad y desbalance."
uni1["remite_a"] = ["edo3_interactivo.html", "edo_interactivo.html", "transmisibilidad_interactivo.html"]
P["autoevaluacion.html"] = {"corto": "Repaso · Autoevaluación", "titulo": "Autoevaluación para el examen final",
   "enfoque": "PRACTICAR · un problema de cada unidad, con datos nuevos cada vez",
   "descripcion": "Problemas de las unidades 1 a 8 con datos aleatorios, comprobación inmediata con 2 % de tolerancia y solución paso a paso con los números del problema.",
   "puntos": ["Trece problemas, de la señal armónica a los dos grados de libertad", "Comprobación con 2 % (0.2 dB en niveles)", "Solución completa al terminar"], "tema": "unidades 1 a 8", "swatch": ["#1F3864", "#C55A11"],
   "claves": ["examen final", "repaso", "autoevaluación", "problemas resueltos", "práctica"]}
PROY = {
 "proy_sensores.html": ("¿Mi teléfono puede medirlo?", "ELEGIR · acelerómetro, micrófono, magnetómetro o cámara",
   "Con la frecuencia, la amplitud y el amortiguamiento esperados se revisa qué sensor del teléfono sirve: muestreo y alias, señal frente a ruido, carga de masa y resolución.",
   ["Nyquist y alias de cada sensor", "Señal frente a ruido del acelerómetro", "Carga de masa del teléfono"], ["sensores del teléfono", "acelerómetro", "micrófono", "magnetómetro", "Phyphox", "aliasing", "carga de masa"], ["#4472C4", "#2E7D46"]),
 "proy_rigidez.html": ("Caracterizar la rigidez de un resorte o una placa", "MEDIR · tres caminos para obtener k",
   "Rigidez k por cargas y deflexión, por frecuencia con masa añadida y por la fórmula de la viga en voladizo, con ajuste por mínimos cuadrados e incertidumbre.",
   ["Estática: k = 1/pendiente de δ contra F", "Masa añadida: recta de 1/f² contra ΔM", "Voladizo: k = 3EI/L³"], ["rigidez", "constante del resorte", "masa añadida", "viga en voladizo", "ligas", "tapete"], ["#2E7D46", "#C55A11"]),
 "proy_bobina.html": ("Bobina e imán: fuerza y tensión inducida", "DISEÑAR · del calibre y las vueltas a la fuerza",
   "A partir de la geometría de la bobina y del imán se calculan la resistencia, la corriente, la fuerza sobre el imán (actuador) y la tensión inducida (sensor).",
   ["Resistencia y corriente según el calibre AWG", "F = K I y e = K v con la misma K", "Potencia disipada y calentamiento"], ["solenoide", "bobina", "imán de neodimio", "fuerza magnética", "fem inducida", "AWG"], ["#6B3FA0", "#C55A11"]),
 "proy_datos.html": ("Del dato al resultado: análisis por proyecto", "ANALIZAR · pegar las mediciones y obtener el resultado",
   "Cada equipo pega sus mediciones: transmisibilidad con ajuste de f_n y ζ (A), curva de vida de Basquin y Miner (B) y decremento logarítmico por configuración (C).",
   ["A: ajuste de f_n y ζ sobre T_r", "B: Basquin y Miner", "C: decremento por regresión"], ["transmisibilidad", "Basquin", "Miner", "decremento logarítmico", "análisis de datos", "proyecto final"], ["#B23A3A", "#1F3864"]),
}
for f, (tit, enf, desc, pts, cl, sw) in PROY.items():
    P[f] = {"corto": "Proyectos · " + tit, "titulo": tit, "enfoque": enf, "descripcion": desc, "puntos": pts, "tema": "apoyo a los proyectos", "swatch": sw, "claves": cl}
T["proyectos"] = {"titulo": "Apoyo a los proyectos", "paginas": list(PROY)}
T["repaso"] = {"titulo": "Repaso para el examen final", "paginas": ["autoevaluacion.html"]}
T["recorrido"] = T["fundamentos"]["paginas"] + [f for u in T["unidades"] for f in u.get("paginas", []) + u.get("apoyo", [])] + T["proyectos"]["paginas"] + T["repaso"]["paginas"]
T["actualizado"] = FECHA
T["nota"] = "Fuente única del panel de navegación, del índice, del mapa del sitio y de los metadatos. Para añadir un explorador: 1) registrarlo en 'paginas', 2) listarlo en la unidad (o en 'fundamentos') en el orden del programa, 3) ejecutar integra2.py."
json.dump(T, open(tp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
RECORRIDO = T["recorrido"]

# ------------------------------------------------------------------------------------------------ 2. navegación lateral
INI, FIN = "<!-- navegacion:inicio -->", "<!-- navegacion:fin -->"
def sub_de(f):
    p = P[f]; c = p["corto"].split(" · ")[0]; t = p.get("tema", "")
    t = re.sub(r"^temas? ", "", t)
    if f in T["fundamentos"]["paginas"]: return c + " · " + {"armar": "armar la ecuación", "resolver": "resolverla", "interpretar": "interpretar las raíces"}.get(t, t)
    if c in ("Proyectos", "Repaso"): return t
    return (t + " · " + c) if c.startswith(("Pilar", "Tutorial")) else t
def menu_html():
    g = [f'<div class="nv-grp">{esc(T["fundamentos"]["titulo"])} · conocimiento previo</div>']
    it = lambda f: f'<a href="{f}" data-nv="{f}" data-k="{esc(" ".join(P[f].get("claves", []) + P[f].get("puntos", [])))}">{esc(P[f]["titulo"])}<small>{esc(sub_de(f))}</small></a>'
    g += [it(f) for f in T["fundamentos"]["paginas"]]
    for u in T["unidades"]:
        fs = u.get("paginas", []) + u.get("apoyo", [])
        if not fs: continue
        g.append(f'<div class="nv-grp">Unidad {u["n"]} · {esc(u["titulo"])}</div>')
        g += [it(f) for f in fs]
    for kk in ("proyectos", "repaso"): g.append(f'<div class="nv-grp">{esc(T[kk]["titulo"])}</div>'); g += [it(f) for f in T[kk]["paginas"]]
    return "\n".join(g)

NAV = f"""{INI}
<style>
  :root{{--nv-w:272px}}
  body{{margin-top:0!important}}
  @media (min-width:1360px){{ body{{margin-left:var(--nv-w)!important}} }}
  .nvside{{position:fixed;top:0;left:0;bottom:0;width:var(--nv-w);z-index:9999;display:flex;flex-direction:column;
    background:var(--card,#fff);border-right:1px solid var(--line,#e2dcc9);
    font-family:Arial,"Helvetica Neue",Helvetica,sans-serif;font-size:14px;color:var(--ink,#1a1a1a);
    box-shadow:1px 0 8px rgba(0,0,0,.05);transition:transform .2s ease}}
  .nvside a{{text-decoration:none;color:inherit}}
  .nv-cab{{padding:14px 16px 10px;border-bottom:1px solid var(--line,#e2dcc9);position:relative}}
  .nv-marca{{display:block;font-family:"Century Gothic","Questrial",Arial,sans-serif;font-weight:700;font-size:15px;
    line-height:1.25;color:var(--navy,var(--ink,#1F3864))}}
  .nv-marca small{{display:block;font-weight:400;font-size:12px;color:var(--muted,var(--grey,#5a5a5a));margin-top:2px}}
  .nv-pasos{{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:10px}}
  .nv-paso{{display:flex;flex-direction:column;gap:1px;padding:6px 8px;border:1px solid var(--line,#e2dcc9);border-radius:8px;
    font-size:11px;color:var(--muted,var(--grey,#5a5a5a));min-width:0}}
  .nv-paso b{{font-size:12.5px;color:var(--ink,#1a1a1a);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
  .nv-paso.sig{{text-align:right}}
  .nv-paso:hover{{background:var(--bg,#f4f1ea)}}
  .nv-paso[aria-disabled="true"]{{opacity:.3;pointer-events:none}}
  .nv-busca{{margin-top:8px;width:100%;box-sizing:border-box;padding:7px 9px;border:1px solid var(--line,#e2dcc9);border-radius:8px;
    font:inherit;background:var(--bg,#f8f6f0);color:inherit}}
  .nv-lista{{flex:1;overflow-y:auto;padding:6px 8px 10px}}
  .nv-grp{{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted,var(--grey,#5a5a5a));padding:12px 8px 4px}}
  .nv-lista a{{display:block;padding:6px 8px 6px 10px;border-radius:6px;border-left:3px solid transparent;line-height:1.3}}
  .nv-lista a small{{display:block;font-size:11px;color:var(--muted,var(--grey,#5a5a5a))}}
  .nv-lista a:hover{{background:var(--bg,#f4f1ea)}}
  .nv-lista a.nv-aqui{{background:var(--bg,#f4f1ea);border-left-color:var(--accent,var(--orange,#C1571B));font-weight:700}}
  .nv-nada{{padding:10px;font-size:12.5px;color:var(--muted,var(--grey,#5a5a5a))}}
  .nv-pie{{padding:8px 14px;border-top:1px solid var(--line,#e2dcc9);font-size:11px;color:var(--muted,var(--grey,#5a5a5a))}}
  .nv-boton{{display:none;position:fixed;top:10px;left:10px;z-index:10000;gap:6px}}
  .nv-boton a,.nv-boton button{{display:flex;align-items:center;justify-content:center;height:38px;min-width:38px;padding:0 10px;
    border:1px solid var(--line,#e2dcc9);border-radius:9px;background:var(--card,#fff);color:var(--ink,#1a1a1a);
    font:600 14px Arial,sans-serif;text-decoration:none;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.12)}}
  .nv-boton [aria-disabled="true"]{{opacity:.3;pointer-events:none}}
  .nv-velo{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.35);z-index:10001}}
  .nv-cierra{{display:none;position:absolute;top:10px;right:10px;width:32px;height:32px;border:1px solid var(--line,#e2dcc9);border-radius:8px;background:var(--card,#fff);color:inherit;font-size:16px;cursor:pointer}}
  @media (max-width:1359px){{
    body{{margin-top:56px!important}}
    .nvside{{transform:translateX(-102%);width:min(320px,88vw)}}
    .nvside.abierto{{transform:none;z-index:10002}}
    .nv-cierra{{display:block}}
    .nv-pie{{display:none}}
    .nv-boton{{display:flex}}
    .nvside.abierto ~ .nv-velo{{display:block}}
  }}
  @media print{{.nvside,.nv-boton,.nv-velo{{display:none}} body{{margin:0!important}}}}
</style>
<nav class="nvside" id="nvside" aria-label="Exploradores del curso">
  <div class="nv-cab">
    <button class="nv-cierra" id="nv-cierra" aria-label="Cerrar el temario">✕</button>
    <a class="nv-marca" href="index.html">Exploradores de Vibraciones<small>ENES Juriquilla, UNAM · inicio</small></a>
    <div class="nv-pasos">
      <a class="nv-paso" id="nv-ant" href="#" aria-label="Explorador anterior">‹ anterior<b id="nv-ant-t">…</b></a>
      <a class="nv-paso sig" id="nv-sig" href="#" aria-label="Explorador siguiente">siguiente ›<b id="nv-sig-t">…</b></a>
    </div>
    <input class="nv-busca" id="nv-busca" type="search" placeholder="Buscar (tecla /)" aria-label="Buscar explorador">
  </div>
  <div class="nv-lista" id="nv-lista">
{menu_html()}
<div class="nv-nada" id="nv-nada" style="display:none">Sin coincidencias. Se busca en títulos, temas y palabras clave.</div>
  </div>
  <div class="nv-pie">Teclas (fuera de los controles): ← anterior · → siguiente · / buscar · Esc cerrar</div>
</nav>
<div class="nv-boton"><button id="nv-abre" aria-controls="nvside" aria-expanded="false">☰ Temario</button>
  <a id="nv-ant2" href="#" aria-label="Anterior">‹</a><a id="nv-sig2" href="#" aria-label="Siguiente">›</a></div>
<div class="nv-velo" id="nv-velo"></div>
<script>
(function(){{
  var lista=document.getElementById('nv-lista'), side=document.getElementById('nvside');
  var l=lista.querySelectorAll('a[data-nv]'), orden=[], dat={{}};
  for(var i=0;i<l.length;i++){{var f=l[i].getAttribute('data-nv');orden.push(f);
    dat[f]={{el:l[i],t:l[i].childNodes[0].textContent.trim()}};}}
  var aqui=(location.pathname.split('/').pop()||'index.html'), k=orden.indexOf(aqui);
  function paso(idA,idT,j){{var a=document.getElementById(idA);
    if(j<0||j>=orden.length){{a.setAttribute('aria-disabled','true');a.setAttribute('tabindex','-1');if(idT)document.getElementById(idT).textContent='';return;}}
    a.href=orden[j];a.title=dat[orden[j]].t+(j<k?' (tecla ←)':' (tecla →)');if(idT)document.getElementById(idT).textContent=dat[orden[j]].t;}}
  if(k>=0){{dat[aqui].el.className='nv-aqui';dat[aqui].el.setAttribute('aria-current','page');
    paso('nv-ant','nv-ant-t',k-1);paso('nv-sig','nv-sig-t',k+1);paso('nv-ant2',null,k-1);paso('nv-sig2',null,k+1);
    setTimeout(function(){{var r=dat[aqui].el;lista.scrollTop=r.offsetTop-lista.clientHeight/3;}},0);}}
  else{{paso('nv-ant','nv-ant-t',-1);paso('nv-sig','nv-sig-t',0);paso('nv-ant2',null,-1);paso('nv-sig2',null,0);}}
  var bus=document.getElementById('nv-busca');
  function llano(t){{return t.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');}}
  bus.addEventListener('input',function(){{var q=llano(bus.value), grp=null, vis=0, tot=0;
    Array.prototype.forEach.call(lista.children,function(c){{
      if(c.classList.contains('nv-grp')){{if(grp)grp.style.display=vis?'':'none';grp=c;vis=0;return;}}
      if(!c.getAttribute('data-nv')) return;
      var ok=!q||llano(c.textContent+' '+(c.getAttribute('data-k')||'')).indexOf(q)>=0;c.style.display=ok?'':'none';if(ok){{vis++;tot++;}}}});
    if(grp)grp.style.display=vis?'':'none';
    document.getElementById('nv-nada').style.display=tot?'none':'block';}});
  bus.addEventListener('keydown',function(e){{e.stopPropagation();if(e.key==='Enter'){{var v=lista.querySelector('a[data-nv]:not([style*="none"])');if(v)location.href=v.href;}}
    if(e.key==='Escape'){{bus.value='';bus.dispatchEvent(new Event('input'));bus.blur();cambia(false);}}}});
  var abre=document.getElementById('nv-abre'), velo=document.getElementById('nv-velo');
  function cambia(on){{side.classList.toggle('abierto',on);abre.setAttribute('aria-expanded',on?'true':'false');}}
  abre.addEventListener('click',function(){{cambia(!side.classList.contains('abierto'));}});
  velo.addEventListener('click',function(){{cambia(false);}});
  document.getElementById('nv-cierra').addEventListener('click',function(){{cambia(false);}});
  document.addEventListener('keydown',function(e){{
    var t=(e.target.tagName||'').toUpperCase();
    if(e.key==='Escape'){{cambia(false);return;}}
    if(t==='INPUT'||t==='TEXTAREA'||t==='SELECT'||t==='BUTTON'||t==='A'||t==='SUMMARY'||e.target.isContentEditable||e.altKey||e.ctrlKey||e.metaKey||e.shiftKey) return;
    if(e.key==='/'){{e.preventDefault();if(innerWidth<1360)cambia(true);bus.focus();return;}}
    if(k<0) return;
    if(e.key==='ArrowLeft'&&k>0) location.href=orden[k-1];
    if(e.key==='ArrowRight'&&k<orden.length-1) location.href=orden[k+1];
  }});
}})();
</script>
{FIN}
"""

MOVIL = """<!-- movil:inicio -->
<style>
  .card{min-width:0}
  pre{overflow-x:auto;max-width:100%}
  .row,.tile,.grp,.two>div{min-width:0}
  input[type=number],select{max-width:100%;min-width:0}
  canvas{max-width:100%}
  @media (max-width:480px){
    .eqbox{font-size:14px}
    .row,.row.kbrow{flex-wrap:wrap!important}
    .row>label{min-width:100%!important;flex:1 1 100%}
    .row>input[type=range]{flex:1 1 120px;min-height:28px}
    .tiles.t3{grid-template-columns:1fr 1fr}
    header h1{font-size:22px}
  }
</style>
<!-- movil:fin -->
"""

def seo(f):
    if f == "index.html":
        tit = "Vibraciones: exploradores interactivos"; desc = T["lede"]; claves = ["vibraciones mecánicas", "ingeniería aeroespacial", "simulaciones interactivas"]; url = BASE
    else:
        p = P[f]; tit = p["titulo"]; desc = p["descripcion"]; claves = p.get("claves", []); url = BASE + f
    ld = {"@context": "https://schema.org", "@type": "Collection" if f == "index.html" else "LearningResource", "name": tit, "description": desc, "url": url,
          "inLanguage": "es", "isAccessibleForFree": True, "learningResourceType": "simulación interactiva" if f != "normas.html" else "guía de consulta",
          "educationalLevel": "Licenciatura", "about": claves, "license": "https://creativecommons.org/licenses/by/4.0/", "identifier": "https://doi.org/" + DOI,
          "author": [{"@type": "Person", "name": "Elodie Strupiechonski", "sameAs": "https://orcid.org/0000-0001-8991-8499"},
                     {"@type": "Person", "name": "Andrés de Luna Bugallo", "sameAs": "https://orcid.org/0000-0002-7591-5235"}],
          "provider": {"@type": "CollegeOrUniversity", "name": "Universidad Nacional Autónoma de México, ENES Juriquilla"}}
    if f != "index.html": ld["isPartOf"] = {"@type": "Collection", "name": "Vibraciones: exploradores interactivos", "url": BASE}
    return f"""<!-- seo:inicio -->
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Exploradores de Vibraciones (UNAM)">
<meta property="og:title" content="{esc(tit)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="es_MX">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
<!-- seo:fin -->
"""
def sin(s, a): return re.sub(r"<!-- %s:inicio -->.*?<!-- %s:fin -->\n?" % (a, a), "", s, flags=re.S)

htmls = sorted(x for x in os.listdir(D) if x.endswith(".html"))
for f in htmls:
    p = os.path.join(D, f); s = open(p, encoding="utf-8").read()
    for a in ("navbar", "navegacion", "movil", "seo"): s = sin(s, a)
    s = re.sub(r'\s*<meta name="description"[^>]*>', "", s)
    assert s.count("</body>") == 1 and s.count("</head>") == 1, f
    s = s.replace("</head>", seo(f) + MOVIL + "</head>", 1)
    s = s.replace("</body>", NAV + "</body>", 1)
    s = re.sub(r"\(Versión 1\.[0-2]\)", "(Versión %s)" % VERSION, s)
    open(p, "w", encoding="utf-8").write(s)

# ------------------------------------------------------------------------------------------------ 4. índice
ip = os.path.join(D, "index.html"); s = open(ip, encoding="utf-8").read()
viejas = {m.group(1): m.group(0) for m in re.finditer(r'<div class="cw"><a class="card" href="([^"]+)">.*?</a>(?:<a class="hoja".*?</a>)?</div>', s, flags=re.S)}
def card(f, n):
    p = P[f]; sw = p["swatch"]; pts = " · ".join(p.get("puntos", [])); c = p["corto"].split(" · ")[0]
    return f'''<div class="cw"><a class="card" href="{f}">
      <div class="swatch" style="background:linear-gradient(90deg,{sw[0]},{sw[1]})"></div>
      <div class="u">{esc("Unidad %d · %s · %s" % (n, p["tema"], c))}</div>
      <div class="ct">{esc(p["titulo"])}</div>
      <div class="ce">{esc(p["enfoque"])}</div>
      <div class="cd">{esc(p["descripcion"])}</div>
      <div class="cp">{esc(pts)}</div>
      <div class="chip">Abrir {"el tutorial" if c == "Tutorial" else "explorador"} →</div>
    </a></div>'''
for u in T["unidades"]:
    n = u["n"]; fs = u.get("paginas", []) + u.get("apoyo", [])
    pat = re.compile(r'(<div class="sk">Unidad %d<small>.*?</ul>\s*</div>\n)(.*?)(</section>)' % n, re.S)
    assert pat.search(s), "sección de la unidad %d" % n
    if fs: cuerpo = '<div class="grid">\n' + "\n".join(viejas[f] if f in viejas and f not in NUEVAS else card(f, n) for f in fs) + "\n</div>\n"
    else: cuerpo = ""
    if u.get("remite"):
        ligas = ", ".join('<a href="%s">%s</a>' % (f, esc(P[f]["titulo"])) for f in u.get("remite_a", []))
        cuerpo += '<div class="nota"><b>Dónde se trabaja.</b> %s Exploradores: %s.</div>\n' % (esc(u["remite"]), ligas)
    if u.get("pendientes"):
        cuerpo += '<div class="nota"><b>Sin explorador todavía:</b> %s.</div>\n' % esc(u["pendientes"])
    s = pat.sub(lambda m: m.group(1) + cuerpo + m.group(3), s, count=1)
s = s.replace("la barra superior permite saltar entre exploradores (teclas ← y →) y abrir el temario desde cualquier página.",
              "el panel lateral permite saltar entre exploradores (teclas ← y →), buscar por nombre (tecla /) y ver el temario completo desde cualquier página; en pantallas de menos de 1360 px se abre con «☰ Temario», para que las gráficas conserven su tamaño.")
s = s.replace("Unidad 6 · temas 6.3–6.4 · Pilar 10", "Unidad 6 · temas 6.1, 6.2 y 6.4 · Pilar 10").replace("Unidad 2 · tema 2.3 · Pilar 4", "Unidad 2 · tema 2.3 (fricción seca) · Pilar 4")
def _card_extra(f, eti, chip):
    p = P[f]; sw = p["swatch"]
    return f'''<div class="cw"><a class="card" href="{f}">
      <div class="swatch" style="background:linear-gradient(90deg,{sw[0]},{sw[1]})"></div>
      <div class="u">{esc(eti)}</div>
      <div class="ct">{esc(p["titulo"])}</div>
      <div class="ce">{esc(p["enfoque"])}</div>
      <div class="cd">{esc(p["descripcion"])}</div>
      <div class="cp">{esc(" · ".join(p["puntos"]))}</div>
      <div class="chip">{chip} →</div>
    </a></div>'''
REP = """<!-- repaso:inicio -->
<section><div class="sect"><div class="sk">Proyectos<small>apoyo a los equipos</small></div><h2>Apoyo a los proyectos finales</h2><p>Herramientas para planear la medición, caracterizar el montaje y analizar los datos de cada equipo.</p></div>
<div class="grid">
""" + "\n".join(_card_extra(f, "Proyectos · apoyo", "Abrir la herramienta") for f in T["proyectos"]["paginas"]) + """
</div>
</section>
<section><div class="sect"><div class="sk">Repaso<small>unidades 1 a 8</small></div><h2>Preparación para el examen final</h2><p>Problemas de todas las unidades con datos nuevos cada vez y comprobación inmediata.</p></div>
<div class="grid">
""" + _card_extra("autoevaluacion.html", "Repaso · unidades 1 a 8", "Abrir la autoevaluación") + """
</div>
</section>
<!-- repaso:fin -->
"""
s = re.sub(r"<!-- repaso:inicio -->.*?<!-- repaso:fin -->\n?", "", s, flags=re.S)
i8 = s.index('<div class="sk">Unidad 8<'); j8 = s.index("</section>", i8) + len("</section>\n")
s = s[:j8] + REP + s[j8:]
open(ip, "w", encoding="utf-8").write(s)

# ------------------------------------------------------------------------------------------------ 3b. mapa del sitio
urls = [BASE] + [BASE + f for f in RECORRIDO]
open(os.path.join(D, "sitemap.xml"), "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join("  <url><loc>%s</loc><lastmod>%s</lastmod></url>\n" % (u, FECHA) for u in urls) + "</urlset>\n")

# ------------------------------------------------------------------------------------------------ 5. versión
n_exp = len([f for f in RECORRIDO if f != "normas.html"])
def cambia(nombre, fn):
    p = os.path.join(D, nombre)
    if os.path.exists(p):
        a = open(p, encoding="utf-8").read(); b = fn(a)
        if a != b: open(p, "w", encoding="utf-8").write(b)
cambia("CITATION.cff", lambda a: re.sub(r'(?m)^version: .*$', 'version: "%s"' % VERSION, re.sub(r'(?m)^date-released: .*$', 'date-released: "%s"' % FECHA, a)))
cambia(".zenodo.json", lambda a: re.sub(r'"version":\s*"[^"]*"', '"version": "%s"' % VERSION, a))
print("temario: %d páginas (%d exploradores y tutoriales); navegación lateral, seo, móvil e índice actualizados; versión %s" % (len(P), n_exp, VERSION))
print("orden:", " → ".join(f.split("_")[0].replace(".html", "") for f in RECORRIDO))

# ------------------------------------------------------------------------------------------------ 6. README y descripción de Zenodo
def fila_md(f, donde):
    p = P[f]; return "| `%s` | %s | %s |" % (f, p["titulo"] + ": " + p["descripcion"].rstrip("."), donde)
tabla = ["| Archivo | Contenido | Unidad · tema |", "|---|---|---|", "| `index.html` | Portada de la colección | |"]
tabla += [fila_md(f, "Fundamentos · " + P[f]["corto"].split(" · ")[0]) for f in T["fundamentos"]["paginas"]]
for u in T["unidades"]:
    tabla += [fila_md(f, "U%d · %s" % (u["n"], re.sub(r"^temas? ", "", P[f].get("tema", "")))) for f in u.get("paginas", []) + u.get("apoyo", [])]
tabla += [fila_md(f, "Apoyo a los proyectos") for f in T["proyectos"]["paginas"]]
tabla += [fila_md(f, "Repaso · U1 a U8") for f in T["repaso"]["paginas"]]
README = f"""# Vibraciones: exploradores interactivos

[![DOI](https://zenodo.org/badge/DOI/{DOI}.svg)](https://doi.org/{DOI})

Colección de recursos educativos abiertos (REA) para el curso de **Vibraciones** de la licenciatura en **Ingeniería Aeroespacial**, ENES Juriquilla, UNAM. Cada explorador es una página HTML autónoma e interactiva: se mueve un control, o se escribe un valor, y se observa cómo responde el sistema.

**Versión {VERSION} (2026)** · Portal en línea: {BASE}

## Cómo usar

Abrir **`index.html`** en cualquier navegador actual. No se necesita conexión ni instalación: todo el código va incluido en cada archivo. El panel lateral permite recorrer los exploradores en el orden del programa (teclas ← y →) y buscar por nombre (tecla /). Para que las ligas funcionen, todos los archivos deben estar en la misma carpeta.

## Contenido

{chr(10).join(tabla)}

Otros archivos: `Tratamiento_decaimiento_Phyphox.ipynb` (cuaderno de Jupyter del tutorial), `segueta_10cm.csv` (registro de ejemplo), `Hoja_alumno_Pilar1_Complejos.docx`, `Hoja_alumno_Pilar2_EDO.docx` y `Hoja_alumno_Pilar3_Dinamica.docx` (hojas de trabajo), `normas.json` (referencias normativas), `temario.json` (fuente única del panel de navegación, del índice y de los metadatos), `sitemap.xml`, `CHANGELOG.md`.

## Reglas de estilo

Las mismas que en el sitio de Teoría Electromagnética: tipografía institucional (Century Gothic o equivalente en títulos, Arial en texto, Cambria en fórmulas); fórmulas en notación matemática con subíndices y superíndices reales, también en las gráficas; redacción impersonal, sin rayas ni emojis decorativos; todo valor se puede fijar con el deslizador o escribirse con el teclado; cada resultado numérico se verifica con un cálculo independiente; las referencias son libros de texto reconocidos o publicaciones con DOI comprobado.

## Mantenimiento

La carpeta `herramientas/` contiene los scripts de Python que generan y homologan las páginas (todos idempotentes salvo `mejoras.py`, que se aplicó una sola vez en la revisión del 11 de noviembre de 2026). Para añadir un explorador: registrarlo en `temario.json` dentro de su unidad, en el orden del programa, y ejecutar `integra2.py`. `construir.sh` reconstruye la versión actual a partir de la anterior; `rev12.py`, `teclado.py`, `nuevos.py` y `audit.py` son las pruebas automáticas (Playwright) que comparan las lecturas con cálculos independientes.

## Licencia

Creative Commons Attribution 4.0 International (**CC BY 4.0**).

## Cómo citar

Strupiechonski, E., & de Luna Bugallo, A. (2026). *Vibraciones: exploradores interactivos* (Versión {VERSION}) [Recurso educativo abierto]. UNAM, ENES Juriquilla. DOI: {DOI}

## Autoría

- Elodie Strupiechonski: ENES Juriquilla, UNAM · ORCID [0000-0001-8991-8499](https://orcid.org/0000-0001-8991-8499)
- Andrés de Luna Bugallo: CFATA, UNAM · ORCID [0000-0002-7591-5235](https://orcid.org/0000-0002-7591-5235)

El historial de cambios está en [`CHANGELOG.md`](CHANGELOG.md).
"""
open(os.path.join(D, "README.md"), "w", encoding="utf-8").write(README)
def zen(a):
    a = a.replace("Colección de doce exploradores interactivos", "Colección de diecinueve exploradores interactivos y un tutorial de medición").replace("Colección de dieciséis exploradores", "Colección de diecinueve exploradores")
    if "analogías electromecánicas" not in a:
        a = a.replace(" Recurso educativo abierto.", " La versión 1.6 añade cuatro herramientas de apoyo a los proyectos (sensores del teléfono, rigidez, bobina e imán, análisis de datos). La versión 1.5 añade una autoevaluación con problemas de las unidades 1 a 8 para preparar el examen final. La versión 1.4 añade esfuerzos normales y cortantes directos en una unión con pernos (U5), pérdida por transmisión sonora de un panel (U6) y campo libre, campo reverberante y cámaras anecoicas (U6). Recurso educativo abierto.", 1)
        a = a.replace(" La versión 1.4 añade", " La versión 1.3 añade analogías electromecánicas (U2), transmisibilidad, aislamiento y desbalance rotatorio (U6), extracción de parámetros modales de una función de respuesta en frecuencia (U7), ensayo de choque y espectro de respuesta (U7) y un tutorial para medir un decaimiento libre con Phyphox y analizarlo en Python (U7). Recurso educativo abierto.", 1)
    return a
cambia(".zenodo.json", zen)
