#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Revisión 1.2: retoques a las páginas de la versión 1.1 derivados de la revisión con tres perfiles de lector
(estudiante, docente de la asignatura, autor de libro de texto). Sustituciones literales; idempotente (si el texto
nuevo ya está, no hace nada; si no encuentra el texto original, avisa). Uso: python3 retoques12.py CARPETA"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mml import M
import mejoras as mj
D = sys.argv[1]; avisos = []

R = {}
def r(f, a, b, todas=False): R.setdefault(f, []).append((a, b, todas))

# ------------------------------------------------------------------ respuesta forzada
f = "forzada_interactivo.html"
r(f, "' Sobreamortiguado (ζ ≥ 0.707): la curva M no tiene pico.'", "' Sin pico de resonancia (ζ ≥ 1/√2 ≈ 0.707): la curva M decrece desde 1.'")
r(f, "Aquí <b>añadimos la fuerza</b>", "Aquí <b>se añade la fuerza</b>")
r(f, "factor de amplificación dinámico", "factor de amplificación dinámica", True)
r(f, "<b>Problema 3.1</b> (m = 5, k = 2000, c = 40, F<sub>0</sub> = 50, ω = 25 rad/s).", "<b>Problema 3.1</b> (<i>m</i> = 5 kg, <i>k</i> = 2000 N/m, <i>c</i> = 40 N·s/m, <i>F</i><sub>0</sub> = 50 N, ω = 25 rad/s).")
r(f, "<li><b>«Desintonizar»</b> (detune): mover", "<li><b>Desintonizar</b>: mover")
r(f, "masa o el rpm de operación", "masa o la velocidad de giro de operación")
r(f, "<li><b>Flutter</b>: el caso límite en que el amortiguamiento neto tiende a cero y el pico de M crece sin cota", "<li><b>Flameo (<i>flutter</i>)</b>: inestabilidad autoexcitada en la que el amortiguamiento total (estructural más aerodinámico) se anula; no es una resonancia forzada, aunque también se manifiesta como una amplitud que crece sin cota")
# ------------------------------------------------------------------ fatiga, mohr, normas, mediapotencia, sonido
f = "fatiga_interactivo.html"
r(f, "Pero pon K<sub>f</sub> = 3 y 60 MPa rms (una barra más delgada o una entalla) y la vida se mide en minutos: el diseño a fatiga va de los detalles, no de la carga media.",
     "Con K<sub>f</sub> = 3 y 60 MPa rms (una barra más delgada o una entalla), en cambio, la vida se mide en minutos: el diseño a fatiga depende de los detalles, no de la carga media.")
r(f, "cuántos ciclos aguanta una pieza", "cuántos ciclos resiste una pieza")
r(f, "(ésa es la pendiente b ≈ −0.08: duplicar la amplitud divide la vida por unas 5 000)", "(esa es la pendiente b ≈ −0.08: duplicar la amplitud divide la vida entre 2<sup>12.5</sup> ≈ 5 800)")
f = "mohr_interactivo.html"
r(f, "pruébelo con el preajuste <b>Biaxial</b>", "se comprueba con el preajuste <b>Biaxial</b>")
r(f, "no son un capricho:", "tienen una razón:")
r(f, "El estado biaxial igual, y la trampa del plano", "El estado biaxial igual y el cortante fuera del plano")
r(f, "y el explorador hace el resto. Es lo que corre en el equipo de adquisición", "y el explorador completa el cálculo. Es el procedimiento que ejecuta el equipo de adquisición")
r(f, "y ése sí no produce fluencia", "y ese no produce fluencia")
r(f, "los recuadros azules …el centro y el radio… no se mueven", "los recuadros azules (el centro y el radio) no se mueven")
r(f, "txt(ctx,'Elemento diferencial, girado θ = '+fmt(TH,1)+'°', splitX/2, 22,", "txt(ctx,(W<700?'Elemento, θ = ':'Elemento diferencial, girado θ = ')+fmt(TH,1)+'°', splitX/2, 22,")
r(f, '<div class="row"><label>σ<sub>x</sub></label>', '<div class="row"><label>σ<sub>x</sub> (MPa)</label>')
r(f, '<div class="row"><label>σ<sub>y</sub></label>', '<div class="row"><label>σ<sub>y</sub> (MPa)</label>')
r(f, '<div class="row"><label>τ<sub>xy</sub></label>', '<div class="row"><label>τ<sub>xy</sub> (MPa)</label>')
r(f, '<div class="row"><label>Límite S<sub>y</sub></label>', '<div class="row"><label>Límite S<sub>y</sub> (MPa)</label>')
f = "fatiga_interactivo.html"
r(f, '<div class="row"><label>σ<sub>m</sub> medio</label>', '<div class="row"><label>σ<sub>m</sub> medio (MPa)</label>')
r(f, '<div class="row"><label>σ<sub>a</sub> alternante</label>', '<div class="row"><label>σ<sub>a</sub> alternante (MPa)</label>')
r(f, '<div class="row"><label>σ a 1σ (rms)</label>', '<div class="row"><label>σ a 1σ (rms, MPa)</label>')
f = "normas.html"
r(f, "y es lo que hacemos en el curso,", "y es lo que se hace en el curso,")
r(f, "<b>revendedores autorizados</b> …Accuris, antes IHS Markit, o Techstreet…, que", "<b>revendedores autorizados</b> (Accuris, antes IHS Markit, o Techstreet), que")
f = "mediapotencia_interactivo.html"
r(f, "(diferencia menor que 1 % hasta ζ = 0.10)", "(diferencia del orden de 1 % en ζ = 0.10)")
f = "sonido_interactivo.html"
r(f, "Nivel de acción internacional: 85 dB(A).", "Nivel de acción usual en otras normativas (NIOSH, Directiva 2003/10/CE): 85 dB(A).")
r(f, "Quien sume con 20 log obtiene unos 4 dB de más.", "Quien sume con 20 log sobrestima el resultado: con dos fuentes iguales obtiene +6 dB en lugar de +3 dB.")
# ------------------------------------------------------------------ coulomb
f = "coulomb_interactivo.html"
r(f, "<b>voltea de sentido</b>", "<b>cambia de sentido</b>")
r(f, "<b>ya no arranca</b>", "<b>ya no reanuda el movimiento</b>")
r(f, "Sinusoide a trozos (SHM a ω<sub>n</sub>", "Sinusoide a trozos (movimiento armónico simple a ω<sub>n</sub>")
r(f, "en cada semiciclo la EOM es m·x″ + k·x = ∓F<sub>f</sub>: es SHM a", "en cada semiciclo la ecuación de movimiento es m·x″ + k·x = ∓F<sub>f</sub>: es un movimiento armónico simple a")
r(f, "pero la EOM sigue siendo SHM a", "pero el movimiento sigue siendo armónico simple a")
r(f, "decaimiento LINEAL</h2>", "decaimiento lineal</h2>")
r(f, "'4F_f/k (decaimiento LINEAL)'", "'4F_f/k (decaimiento lineal)'")
r(f, "c.fillText('envolvente LINEAL'", "c.fillText('envolvente lineal'")
r(f, "<b>microdeslizamiento</b> (microslip)", "<b>microdeslizamiento</b> (<i>microslip</i>)")
r(f, "demasiado apriete reduce el microslip y el amortiguamiento", "demasiado apriete reduce el microdeslizamiento y el amortiguamiento")
r(f, "y en estudios de <i>joint damping / microslip</i>", "y en estudios de amortiguamiento en uniones (<i>joint damping</i>)")
r(f, "solo <b>cambia de signo</b> con la velocidad: igual que en este explorador.</li>", "solo <b>cambia de signo</b> con la velocidad: es el modelo ideal de este explorador (deslizamiento total, μ<sub>s</sub> = μ<sub>k</sub>).</li>")
r(f, "<li><b>Firma característica:</b> la amplitud cae de forma <b>lineal</b> (una recta), no exponencial;", "<li><b>Firma característica:</b> en el modelo ideal la amplitud cae de forma <b>lineal</b> (una recta), no exponencial; en uniones reales el microdeslizamiento produce un amortiguamiento que depende de la amplitud y el decaimiento se aparta de la recta;")
# ------------------------------------------------------------------ pilares
f = "edo_interactivo.html"
r(f, "decide si es seguro.</b>", "decide si es estable.</b>")
r(f, "el sistema físico cuya EOM es", "el sistema físico cuya ecuación de movimiento es")
f = "edo3_interactivo.html"
r(f, "es literalmente una <b>masa sísmica</b> sobre resortes; su desplazamiento mide la aceleración.", "es una <b>masa sísmica</b> sobre resortes; por debajo de su frecuencia natural (ω ≪ ω<sub>n</sub>) su desplazamiento relativo es proporcional a la aceleración.")
r(f, "<b>Slosh de combustible</b>", "<b>Chapoteo de propelente (<i>slosh</i>)</b>")
r(f, "se obtiene la EOM libre.", "se obtiene la ecuación de movimiento libre.")
r(f, "Al soltarla, la EOM decide", "Al soltarla, la ecuación de movimiento decide")
r(f, "(solución de la EOM con", "(solución de la ecuación de movimiento con")
r(f, "y desaparece de la EOM.", "y desaparece de la ecuación de movimiento.")
r(f, "(Conviene mantener los tres archivos en la misma carpeta para que los enlaces funcionen.)", "(Para que las ligas funcionen, todos los archivos del sitio deben estar en la misma carpeta.)")
f = "complejos_interactivo.html"
r(f, "z = r·(cos θ + i·sin θ) = r∠θ", "z = r·(cos θ + i·sen θ) = r∠θ")
r(f, "aparece el <b>flutter</b>.", "aparece el <b>flameo (<i>flutter</i>)</b>.")
r(f, "(Conviene mantener los tres archivos en la misma carpeta para que los enlaces funcionen.)", "(Para que las ligas funcionen, todos los archivos del sitio deben estar en la misma carpeta.)")
# ------------------------------------------------------------------ espectro: la excitación es por la base => transmisibilidad
f = "espectro_interactivo.html"
r(f, "function H2(f){ const r=f/fn; return 1/((1-r*r)*(1-r*r)+(2*z*r)*(2*z*r)); }", "function H2(f){ const r=f/fn; return (1+(2*z*r)*(2*z*r))/((1-r*r)*(1-r*r)+(2*z*r)*(2*z*r)); }   // transmisibilidad al cuadrado: aceleración de la base -> aceleración absoluta")
r(f, "es exactamente el factor de amplificación <span class=\"mth\">M(r)</span> elevado al cuadrado.", "es la transmisibilidad <span class=\"mth\">T<sub>r</sub>(r)</span> elevada al cuadrado, porque la excitación entra por la base; cerca de la resonancia y con ζ ≪ 1 coincide con el factor de amplificación <span class=\"mth\">M(r)</span> al cuadrado.")
r(f, "<b>En corto:</b>", "<b>En resumen:</b>")
r(f, "qué tan picuda es", "qué tan agudo es el pico")
r(f, "Lo de siempre: régimen permanente ante una armónica", "Punto de partida: régimen permanente ante una excitación armónica")
r(f, "tres piezas que ya estaban sobre la mesa:", "tres piezas ya conocidas:")
r(f, "se aplasta contra el eje y desaparece", "queda comprimido contra el eje y deja de verse")
r(f, "la carga baja de golpe,", "la carga baja de forma marcada,")
r(f, "(grupo 3, lo que sufre el componente)", "(grupo 3, lo que recibe el componente)")
r(f, "3 · Respuesta: lo que sufre el componente", "3 · Respuesta: lo que recibe el componente")
r(f, "Lo único que cambia es la contabilidad.", "Lo único que cambia es la forma de sumar.")
r(f, "<h3>El decibel no es una unidad, es una razón</h3>", "<h3>El decibel es una unidad logarítmica: expresa una razón</h3>")
r(f, "de tipo <b>potencia</b> …y una PSD lo es, porque está en g²/Hz… la razón", "de tipo <b>potencia</b> (y una PSD lo es, porque está en g²/Hz), la razón")
r(f, "de tipo <b>amplitud</b> …una aceleración en g, un desplazamiento… se usa", "de tipo <b>amplitud</b> (una aceleración en g, un desplazamiento), se usa")
# ------------------------------------------------------------------ dos grados de libertad
f = "dosgdl_interactivo.html"
r(f, "$('bDH').onclick=()=>pon({be:1/(1+S.mu), z2:Math.sqrt(3*S.mu/(8*Math.pow(1+S.mu,3))), z1:0});", "$('bDH').onclick=()=>pon({be:+(1/(1+S.mu)).toFixed(4), z2:+Math.sqrt(3*S.mu/(8*(1+S.mu))).toFixed(4), z1:0});   // ζ_2 referido a ω_a: (1+μ)·ζ_opt")
r(f, "const g=v=>v>=100?f(v,0):(v>=10?f(v,1):(v>=0.1?f(v,2):f(v,4)));", "const g=v=>(!isFinite(v)||v>1e6)?'∞ (sin amortiguamiento)':v>=100?f(v,0):(v>=10?f(v,1):(v>=0.1?f(v,2):f(v,4)));")
r(f, '<div class="eqnote">válido para la estructura principal sin amortiguamiento</div>', '<div class="eqnote">válido para la estructura principal sin amortiguamiento. En la fórmula, ζ<sub>2,opt</sub> = <i>c</i><sub>2</sub>/(2<i>m</i><sub>2</sub>ω<sub>n1</sub>), referido a la frecuencia de la estructura; el deslizador ζ<sub>2</sub> de esta página está referido a la del absorbedor, ω<sub>a</sub> = βω<sub>n1</sub>, por lo que el botón fija ζ<sub>2</sub> = (1 + μ) ζ<sub>2,opt</sub></div>')
# ------------------------------------------------------------------ señales: unidades con archivo CSV
f = "senales_interactivo.html"
r(f, "function sync(){ R=null; calcular(); dibujar(); }", "function sync(){ R=null; calcular(); dibujar(); }\nfunction UA(){ return (S.origen==='csv'&&CSV)?'m/s^2':'g'; }   // Phyphox exporta en m/s²; la señal sintética está en g")
r(f, "$('oPk').textContent=f3(r.Apk)+' g en '", "$('oPk').textContent=f3(r.Apk)+' '+UA()+' en '")
r(f, "$('oRt').textContent=f3(r.rt)+' g'; $('oRp').textContent=f3(r.rp)+' g';", "$('oRt').textContent=f3(r.rt)+' '+UA(); $('oRp').textContent=f3(r.rp)+' '+UA();")
r(f, "s  ·  a(t) en g'", "s  ·  a(t) en '+UA()")
r(f, "'PSD estimada G(f) en g^2/Hz  ·  '", "'PSD estimada G(f) en '+(UA()==='g'?'g^2/Hz':'(m/s^2)^2/Hz')+'  ·  '")
# ------------------------------------------------------------------ índice
f = "index.html"
r(f, "para tocar la física del curso:", "para explorar la física del curso:")
r(f, "T = 8·2^((90−LA)/3) h", "T = 8·2[sup](90 − L[sub]A[/sub])/3[/sup] h")

# Referencias que faltaban (se añaden al pie descriptivo de cada página). Libros de texto reconocidos y artículos con DOI comprobado.
REFS = {
 "fatiga_interactivo.html": "Referencias: Budynas y Nisbett, <i>Shigley's Mechanical Engineering Design</i>, cap. 6; Dowling, <i>Mechanical Behavior of Materials</i>, caps. 9 y 10; Steinberg, <i>Vibration Analysis for Electronic Equipment</i>, 3.ª ed. (método de las tres bandas); Miner (1945), «Cumulative damage in fatigue», J. Appl. Mech. 12, A159, <a href=\"https://doi.org/10.1115/1.4009458\">doi:10.1115/1.4009458</a>.",
 "mohr_interactivo.html": "Referencias: Beer, Johnston, DeWolf y Mazurek, <i>Mechanics of Materials</i>, cap. 7; Budynas y Nisbett, <i>Shigley's Mechanical Engineering Design</i>, cap. 5.",
 "sonido_interactivo.html": "Referencias: Kinsler, Frey, Coppens y Sanders, <i>Fundamentals of Acoustics</i>, 4.ª ed.; Bies y Hansen, <i>Engineering Noise Control</i>; NOM-011-STPS-2001; IEC 61672-1.",
 "mediapotencia_interactivo.html": "Referencias: Inman, <i>Engineering Vibration</i>, 4.ª ed., cap. 7; Ewins, <i>Modal Testing: Theory, Practice and Application</i>, 2.ª ed., cap. 4; Rao, <i>Mechanical Vibrations</i>, 5.ª ed., sec. 3.4.",
 "espectro_interactivo.html": "Referencias: Miles (1954), «On structural fatigue under random loading», J. Aeronaut. Sci. 21, 753, <a href=\"https://doi.org/10.2514/8.3199\">doi:10.2514/8.3199</a>; Bendat y Piersol, <i>Random Data</i>, 4.ª ed., cap. 6; NASA GSFC-STD-7000 (GEVS).",
}

def aplicar(f, s):
    for a, b, todas in R.get(f, []):
        if a in s: s = s.replace(a, b) if todas else s.replace(a, b, 1)
        elif b not in s: avisos.append("%s: no se encontró «%s»" % (f, a[:70]))
    if f in REFS and REFS[f][:40] not in s:
        m = re.search(r'(<footer>\s*<div style="margin-bottom:8px">)(.*?)(</div>)', s, flags=re.S)
        if m: s = s[:m.start()] + m.group(1) + m.group(2) + "<br>" + REFS[f] + m.group(3) + s[m.end():]
        else: avisos.append("%s: no se encontró el pie para las referencias" % f)
    return s

# espectro: fórmula 3 con la transmisibilidad
F3 = M(r"|H(f)|=T_r(r)=\sqrt{\frac{1+(2\zeta r)^2}{(1-r^2)^2+(2\zeta r)^2}}\approx M(r),\qquad r=\frac{f}{f_n},\qquad |H(f_n)|\approx\frac{1}{2\zeta}=Q")
def espectro(s):
    if "T_r" in s and "<mi>T</mi><mi>r</mi></msub><mo" in s: return s
    m = re.search(r'(<span class="lab">3 · Lo que aporta el equipo \(ya conocido\)</span>)<math.*?</math>', s, flags=re.S)
    if not m: avisos.append("espectro: no se encontró la fórmula 3"); return s
    return s[:m.start()] + m.group(1) + F3 + '<div class="eqnote">excitación por la base: transmisibilidad (véase el explorador de transmisibilidad); la aproximación por <i>M</i>(<i>r</i>) vale cerca de la resonancia con ζ ≪ 1</div>' + s[m.end():]

for f in sorted(x for x in os.listdir(D) if x.endswith(".html")):
    p = os.path.join(D, f); s0 = open(p, encoding="utf-8").read(); s = aplicar(f, s0)
    if f == "espectro_interactivo.html": s = espectro(s)
    if f == "index.html": s = s.replace("[sup]", "<sup>").replace("[/sup]", "</sup>").replace("[sub]", "<sub>").replace("[/sub]", "</sub>")
    s = mj.bloques(s)                                   # bloques de tipografía y de teclado actualizados (idempotente)
    if s != s0: open(p, "w", encoding="utf-8").write(s)
for a in avisos: print("AVISO", a)
print("retoques de la revisión 1.2 aplicados;", len(avisos), "avisos")
