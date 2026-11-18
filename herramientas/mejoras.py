#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Revisión de noviembre de 2026 del sitio de exploradores de Vibraciones.
Aplica, sobre una copia del repositorio (carpeta de trabajo), de forma idempotente:
  1. fórmulas en MathML (fracciones, radicales, subíndices) en los recuadros y glosarios;
  2. correcciones de contenido (aproximaciones marcadas con ≈, formato de potencias, textos);
  3. estilo académico: sin raya (—), sin emojis decorativos, redacción impersonal, subíndices reales;
  4. bloques comunes: tipografía institucional y entrada por teclado en todos los deslizadores.
Uso: python3 mejoras.py CARPETA
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mml import M
from bloques import TIPOGRAFIA, TIPO_INI, TIPO_FIN, TECLADO, TEC_INI, TEC_FIN

D = sys.argv[1]
avisos = []
I = lambda t: M(t, inline=True)
def nota(t): return '<div class="eqnote">%s</div>' % t

# ------------------------------------------------------------------ 1. recuadros de ecuaciones (por orden de aparición)
EQ = {
"espectro_interactivo.html": [
 ("1 · Lo que impone la norma", nota("Densidad espectral de aceleración <i>W</i>(<i>f</i>) en g²/Hz; tramos rectos en escala log–log:") +
   M(r"W(f)\propto f^{\,n},\qquad n=\frac{N}{10\log_{10}2}\approx\frac{N}{3.01}") + nota("con <i>N</i> la pendiente en dB/octava: <i>n</i> ≈ ±2 para ±6 dB/octava y <i>n</i> ≈ ±1 para ±3 dB/octava")),
 ("2 · Valor eficaz del ensayo", M(r"G_{\mathrm{rms}}=\sqrt{\int_{f_1}^{f_2}W(f)\,\mathrm{d}f},\qquad\text{tramo plano: }G_{\mathrm{rms}}=\sqrt{W_0\,\Delta f}")),
 ("3 · Lo que aporta el equipo (ya conocido)", M(r"|H(f)|=M(r)=\frac{1}{\sqrt{(1-r^2)^2+(2\zeta r)^2}},\qquad r=\frac{f}{f_n},\qquad |H(f_n)|=\frac{1}{2\zeta}=Q")),
 ("4 · Respuesta: se multiplican potencias, no amplitudes", M(r"W_{\mathrm{resp}}(f)=|H(f)|^2\,W(f)")),
 ("5 · Ecuación de Miles (PSD plana en torno a <i>f</i><sub>n</sub>)", M(r"G_{\mathrm{rms,resp}}\approx\sqrt{\frac{\pi}{2}\,f_n\,Q\,W(f_n)}=\sqrt{\frac{\pi\,f_n\,W(f_n)}{4\zeta}}")),
 ("6 · Carga de diseño", M(r"3\sigma=3\,G_{\mathrm{rms,resp}},\qquad F=m\,(3\sigma)\,g_0,\qquad g_0=9.81\ \mathrm{m}/\mathrm{s}^2")),
 ("Lo de siempre: régimen permanente ante una armónica", M(r"m\,x''+c\,x'+k\,x=F_0\cos\omega t\quad\Rightarrow\quad x(t)=X\cos(\omega t-\varphi)") +
   M(r"X=\frac{F_0}{k}\,M(r),\qquad \varphi=\mathrm{atan2}(2\zeta r,\ 1-r^2)")),
],
"fatiga_interactivo.html": [
 ("1 · Curva S–N (Basquin), entre 10³ ciclos y el codo", M(r"S=a\,N^{\,b},\qquad S(10^3)=0.9\,S_{ut},\qquad S(N_e)=S_e") + nota("las dos condiciones fijan <i>a</i> y <i>b</i>")),
 ("2 · Esfuerzo medio: equivalente completamente invertido (Goodman)", M(r"\sigma_{ar}=\frac{K_f\,\sigma_a}{1-\sigma_m/S_{ut}},\qquad N=\left(\frac{\sigma_{ar}}{a}\right)^{1/b}")),
 ("3 · Factor de seguridad en el diagrama de Haigh", M(r"\text{Goodman: }\frac{1}{n}=\frac{K_f\,\sigma_a}{S_e}+\frac{\sigma_m}{S_{ut}}\qquad\text{Soderberg: }\frac{1}{n}=\frac{K_f\,\sigma_a}{S_e}+\frac{\sigma_m}{S_y}") +
   M(r"\text{Gerber: }\frac{n\,K_f\,\sigma_a}{S_e}+\left(\frac{n\,\sigma_m}{S_{ut}}\right)^2=1")),
 ("4 · Miner con tres bandas (Steinberg): la vibración aleatoria gaussiana", M(r"n_{1\sigma}=0.683\,N_t,\qquad n_{2\sigma}=0.271\,N_t,\qquad n_{3\sigma}=0.043\,N_t,\qquad N_t=f_n\,t") +
   M(r"D=\sum_i\frac{n_i}{N_i},\qquad\text{falla cuando }D=1")),
],
"forzada_interactivo.html": [
 (None, M(r"x_p(t)=X\cos(\omega t-\varphi),\qquad X=X_0\,M,\qquad X_0=\frac{F_0}{k}")),
 (None, M(r"M=\frac{1}{\sqrt{(1-r^2)^2+(2\zeta r)^2}},\qquad r=\frac{\omega}{\omega_n}")),
 (None, M(r"\varphi=\mathrm{atan2}(2\zeta r,\ 1-r^2)\in[0°,\,180°]")),
],
"mediapotencia_interactivo.html": [
 ("Factor de amplificación", M(r"M(r)=\frac{1}{\sqrt{(1-r^2)^2+(2\zeta r)^2}},\qquad r=\frac{f}{f_n}")),
 ("Resonancia y factor Q", M(r"M_{\text{máx}}=\frac{1}{2\zeta\sqrt{1-\zeta^2}}\approx\frac{1}{2\zeta}=Q,\qquad\text{media potencia: }M=\frac{M_{\text{máx}}}{\sqrt{2}}")),
 ("Medir el amortiguamiento desde la curva (válido para ζ pequeño)", M(r"\Delta f=f_2-f_1\approx 2\zeta f_n\quad\Rightarrow\quad \zeta\approx\frac{\Delta f}{2f_n},\qquad Q=\frac{1}{2\zeta}\approx\frac{f_n}{\Delta f}")),
],
"mohr_interactivo.html": [
 ("Cuña en deformaciones y Hooke en estado plano", M(r"\varepsilon_x=\varepsilon_a,\qquad \varepsilon_y=\varepsilon_c,\qquad \gamma_{xy}=2\varepsilon_b-\varepsilon_a-\varepsilon_c") +
   M(r"\sigma_x=\frac{E\,(\varepsilon_x+\nu\,\varepsilon_y)}{1-\nu^2},\qquad \sigma_y=\frac{E\,(\varepsilon_y+\nu\,\varepsilon_x)}{1-\nu^2},\qquad \tau_{xy}=G\,\gamma_{xy},\qquad G=\frac{E}{2(1+\nu)}")),
 ("von Mises: energía de distorsión", M(r"\sigma'=\sqrt{\sigma_1^2-\sigma_1\sigma_2+\sigma_2^2},\qquad\text{fluye si }\sigma'\geq S_y")),
 ("Tresca: cortante máximo", M(r"\text{fluye si }\max(|\sigma_1-\sigma_2|,\ |\sigma_1|,\ |\sigma_2|)\geq S_y")),
 ("1 · Transformación al girar el corte un ángulo θ", M(r"\sigma_{x'}=\frac{\sigma_x+\sigma_y}{2}+\frac{\sigma_x-\sigma_y}{2}\cos 2\theta+\tau_{xy}\,\mathrm{sen}\,2\theta") +
   M(r"\tau_{x'y'}=-\frac{\sigma_x-\sigma_y}{2}\,\mathrm{sen}\,2\theta+\tau_{xy}\cos 2\theta")),
 ("2 · Centro y radio", M(r"\sigma_{\mathrm{prom}}=\frac{\sigma_x+\sigma_y}{2},\qquad R=\sqrt{\left(\frac{\sigma_x-\sigma_y}{2}\right)^2+\tau_{xy}^2}")),
 ("3 · La ecuación del círculo", M(r"(\sigma-\sigma_{\mathrm{prom}})^2+\tau^2=R^2")),
 ("4 · Esfuerzos principales y su orientación", M(r"\sigma_{1,2}=\sigma_{\mathrm{prom}}\pm R,\qquad \tan 2\theta_p=\frac{2\,\tau_{xy}}{\sigma_x-\sigma_y}")),
],
"sonido_interactivo.html": [
 ("1 · Nivel de presión sonora", M(r"L_p=20\log_{10}\frac{p_{\mathrm{rms}}}{p_{\mathrm{ref}}},\qquad p_{\mathrm{ref}}=20\ \mu\mathrm{Pa}")),
 ("2 · Suma de niveles (energética)", M(r"L_{\mathrm{tot}}=10\log_{10}\sum_i 10^{L_i/10}") + nota("<i>n</i> fuentes iguales: +10 log<sub>10</sub> <i>n</i>; dos fuentes iguales: +3 dB")),
 ("3 · Distancia en campo libre (fuente puntual)", M(r"L(r)=L(r_0)-20\log_{10}\frac{r}{r_0}") + nota("−6 dB por cada duplicación de la distancia")),
 None,
 ("5 · Tiempo máximo de exposición, NOM-011-STPS-2001", M(r"T=8\cdot 2^{(90-L_A)/3}\ \mathrm{h},\qquad \text{dosis}=\sum_i\frac{t_i}{T_i}") + nota("cada +3 dB(A) reduce <i>T</i> a la mitad")),
],
}

def recuadros(f, s):
    if f not in EQ: return s
    lista = EQ[f]; k = [0]
    def rep(m):
        if m.group(0).count("<math"): return m.group(0)          # ya convertido
        if 'id="' in m.group(1): return m.group(0)                 # recuadro dinámico
        i = k[0]; k[0] += 1
        if i >= len(lista) or lista[i] is None: return m.group(0)
        lab, cuerpo = lista[i]
        return "<div%s>%s%s</div>" % (m.group(1), ('<span class="lab">%s</span>' % lab) if lab else "", cuerpo)
    cuerpo, n = re.subn(r'<div( class="eqbox"[^>]*)>(.*?)</div>', rep, s, flags=re.S)
    if k[0] and k[0] != len(lista): avisos.append("%s: %d recuadros convertidos de %d previstos" % (f, k[0], len(lista)))
    return cuerpo

# ------------------------------------------------------------------ 2. sustituciones literales por archivo (texto y fórmulas en línea)
WN = I(r"\omega_n=\sqrt{k/m}")
SUST = {
"complejos_interactivo.html": [
 ('z = r·e<sup>iθ</sup> &nbsp;(θ en radianes)', I(r"z=r\,e^{i\theta}") + ' &nbsp;(θ en radianes)'),
 ('wₖ = √r · e<sup>i(θ+2πk)/2</sup>, &nbsp;k = 0,1. &nbsp; Comprueba: (w₀)² = z.', I(r"w_k=\sqrt{r}\;e^{\,i(\theta+2\pi k)/2},\quad k=0,1") + '. &nbsp; Comprobación: ' + I(r"w_0^2=z") + '.'),
 ('x(t) = e<sup>Re·t</sup>·cos(Im·t)&nbsp; (interpretando z como raíz característica s = Re + i·Im):', I(r"x(t)=e^{\mathrm{Re}(s)\,t}\cos(\mathrm{Im}(s)\,t)") + '&nbsp; (interpretando <i>z</i> como raíz característica <i>s</i>):'),
 ('ω<sub>d</sub> = ω<sub>n</sub>·√(1−ζ²) = |Im(z)|, siempre ≤ ω<sub>n</sub>.', I(r"\omega_d=\omega_n\sqrt{1-\zeta^2}=|\mathrm{Im}(z)|") + ', siempre ≤ ω<sub>n</sub>.'),
 ('<b>T<sub>d</sub> = 2π/ω<sub>d</sub></b>', '<b>' + I(r"T_d=\frac{2\pi}{\omega_d}") + '</b>'),
 ('1 · Entra un número complejo', '1 · Introducción de un número complejo'),
 ('Aquí cierras el círculo: <b>interpretas</b>', 'Aquí se cierra el círculo: <b>se interpreta</b>'),
 ('Pulsa «fasor» para verlo.', 'El botón «fasor» lo muestra.'),
 ('Halla UNA raíz', 'Determinar una raíz'),
 ('z (arrástralo)', 'z (se puede arrastrar)'),
],
"edo_interactivo.html": [
 ('r = (−b ± √Δ)/(2a).', I(r"r=\frac{-b\pm\sqrt{\Delta}}{2a}") + '.'),
 ('<b>ω<sub>n</sub> = √(k/m) = √(c/a)</b>', '<b>' + I(r"\omega_n=\sqrt{k/m}=\sqrt{c/a}") + '</b>'),
 ('<b>ζ = c/(2√(k·m)) = b/(2√(a·c))</b>', '<b>' + I(r"\zeta=\frac{c}{2\sqrt{k\,m}}=\frac{b}{2\sqrt{a\,c}}") + '</b>'),
 ('<b>ω<sub>d</sub> = ω<sub>n</sub>·√(1−ζ²) = |Im(r)|</b>', '<b>' + I(r"\omega_d=\omega_n\sqrt{1-\zeta^2}=|\mathrm{Im}(r)|") + '</b>'),
 ('<b>c<sub>c</sub> = 2√(k·m)</b>', '<b>' + I(r"c_c=2\sqrt{k\,m}") + '</b>'),
 ('1 · Entra la ecuación', '1 · Introducción de la ecuación'),
 ('raíces r₁, r₂ (arrástralas)', 'raíces r₁, r₂ (se pueden arrastrar)'),
 ('Regresa al equilibrio', 'Vuelve al equilibrio'),
],
"edo3_interactivo.html": [
 ('<b>ω<sub>n</sub> = √(k/m)</b>', '<b>' + WN + '</b>'),
 ('<b>f<sub>n</sub> = ω<sub>n</sub>/2π</b>', '<b>' + I(r"f_n=\frac{\omega_n}{2\pi}") + '</b>'),
 ('<b>T = 1/f<sub>n</sub> = 2π/ω<sub>n</sub></b>', '<b>' + I(r"T=\frac{1}{f_n}=\frac{2\pi}{\omega_n}") + '</b>'),
 ('<b>ζ = c/(2√(km))</b>', '<b>' + I(r"\zeta=\frac{c}{2\sqrt{k\,m}}") + '</b>'),
 ('<b>c<sub>c</sub> = 2√(km)</b>', '<b>' + I(r"c_c=2\sqrt{k\,m}") + '</b>'),
 ('T = ½·m·v² (cinética), V = ½·k·x² (potencial elástica). Sin amortiguamiento, T + V = ½·k·A² = constante.',
  I(r"T=\tfrac{1}{2}m\,v^2") + ' (cinética), ' + I(r"V=\tfrac{1}{2}k\,x^2") + ' (potencial elástica). Sin amortiguamiento, ' + I(r"T+V=\tfrac{1}{2}k\,A^2") + ' = constante.'),
 ('θ″ + (g/L)·θ = 0 → ω<sub>n</sub> = √(g/L).', I(r"\theta''+\frac{g}{L}\,\theta=0\ \Rightarrow\ \omega_n=\sqrt{g/L}") + '.'),
 ('1 · Define el sistema', '1 · Definición del sistema'),
 ('Aquí <b>armaste</b> la ecuación', 'Aquí <b>se armó</b> la ecuación'),
 ('El primer paso —y el de este pilar— es', 'El primer paso, y el de este pilar, es'),
],
"coulomb_interactivo.html": [
 ('<b>ω<sub>n</sub> = √(k/m)</b>', '<b>' + WN + '</b>'),
 ('n = ⌈(x₀ − F<sub>f</sub>/k)/(2F<sub>f</sub>/k)⌉ (techo, porque completa el semiciclo en curso).', I(r"n=\left\lceil\frac{x_0-F_f/k}{2F_f/k}\right\rceil") + ' (función techo, porque se completa el semiciclo en curso).'),
 ('1 · Define el sistema', '1 · Definición del sistema'),
 ('Aquí viste un tipo de amortiguamiento', 'Aquí se estudió un tipo de amortiguamiento'),
 ('; regresa al <a href="edo3_interactivo.html">Pilar 3</a> para recordar cómo se arma ΣF = ma.', '; el <a href="edo3_interactivo.html">Pilar 3</a> recuerda cómo se arma ΣF = ma.'),
],
"forzada_interactivo.html": [
 ("<span style=\"font-family:'Cambria Math',serif\">r<sub>pico</sub> = √(1 − 2ζ²)</span>", I(r"r_{\mathrm{pico}}=\sqrt{1-2\zeta^2}")),
 ("<span style=\"font-family:'Cambria Math',serif\">ζ &lt; 1/√2 ≈ 0.707</span>", I(r"\zeta<1/\sqrt{2}\approx0.707")),
 ("<span style=\"font-family:'Cambria Math',serif\">M<sub>máx</sub> = 1/(2ζ√(1−ζ²)) ≈ 1/(2ζ)</span>", I(r"M_{\text{máx}}=\frac{1}{2\zeta\sqrt{1-\zeta^2}}\approx\frac{1}{2\zeta}")),
 ('M = X/X₀ = 1/√[(1−r²)²+(2ζr)²]. Adimensional.', I(r"M=\frac{X}{X_0}=\frac{1}{\sqrt{(1-r^2)^2+(2\zeta r)^2}}") + '. Adimensional.'),
 ('r<sub>pico</sub> = √(1−2ζ²) (existe si ζ &lt; 1/√2). Altura M<sub>máx</sub> = 1/(2ζ√(1−ζ²)); para ζ pequeño M<sub>máx</sub> ≈ 1/(2ζ).',
  I(r"r_{\mathrm{pico}}=\sqrt{1-2\zeta^2}") + ' (existe si ' + I(r"\zeta<1/\sqrt{2}") + '). Altura ' + I(r"M_{\text{máx}}=\frac{1}{2\zeta\sqrt{1-\zeta^2}}") + '; para ζ pequeño, ' + I(r"M_{\text{máx}}\approx\frac{1}{2\zeta}") + '.'),
 ('<b>Evita operar</b> un motor', '<b>Se evita operar</b> un motor'),
 ('Compara con los lectores de la derecha.', 'Se comparan con los lectores de la derecha.'),
 ('En el <a href="edo3_interactivo.html">Pilar 3</a> armaste', 'En el <a href="edo3_interactivo.html">Pilar 3</a> se armó'),
 ('y el pico de M crece sin cota — inestabilidad aeroelástica', 'y el pico de M crece sin cota: inestabilidad aeroelástica'),
],
"mediapotencia_interactivo.html": [
 ("<span style=\"font-family:'Cambria Math',serif\">r = √(1−2ζ²)</span>", I(r"r=\sqrt{1-2\zeta^2}")),
 ("<span style=\"font-family:'Cambria Math',serif\">M<sub>máx</sub>/√2</span> (potencia mitad)", I(r"M_{\text{máx}}/\sqrt{2}") + " (potencia mitad)"),
 ('El valor <b>«ζ medido»</b> se obtiene leyendo Δf de la gráfica y siempre coincide con el ζ real: así es como',
  'El valor <b>«ζ medido»</b> se obtiene leyendo Δf de la gráfica con ' + I(r"\zeta\approx\Delta f/(2f_n)") + '. Coincide con el ζ real cuando el amortiguamiento es pequeño (diferencia menor que 1 % hasta ζ = 0.10) y lo sobrestima al crecer ζ (con ζ = 0.30 se lee 0.341): así es como'),
 ('<div class="k">ζ medido = Δf/(2f<sub>n</sub>)</div>', '<div class="k">ζ medido ≈ Δf/(2f<sub>n</sub>)</div>'),
 ('<div class="k">Factor Q = 1/(2ζ)</div>', '<div class="k">Factor Q = 1/(2ζ)</div>'),
],
"mohr_interactivo.html": [
 ('<span class="mth">R = √(a² + τ<sub>xy</sub>²)</span>', I(r"R=\sqrt{a^2+\tau_{xy}^2}")),
],
"fatiga_interactivo.html": [
 ("el aluminio, no: lee N en el recuadro. Luego sube K<sub>f</sub> a 3 (un agujero) y observa cómo el punto cruza la curva.",
  "el aluminio, no: N se lee en el recuadro. Al subir después K<sub>f</sub> a 3 (un agujero) se observa cómo el punto cruza la curva."),
 ("Deja σ<sub>a</sub> fijo y sube σ<sub>m</sub>: el punto", "Con σ<sub>a</sub> fijo, al subir σ<sub>m</sub> el punto"),
 ("$('oD').textContent=E.D<1e-4?E.D.toExponential(2).replace('e-','×10⁻').replace('e+','×10'):fmt(E.D,3);",
  "$('oD').textContent=E.D<=0?'0':(E.D<1e-2?(function(p){return p[0]+'×10⁻'+sup(Math.abs(+p[1]));})(E.D.toExponential(2).split('e')):fmt(E.D,3));"),
 ("vida<60*48?fmt(vida/60,1)+' h':fmt(vida/60/24,1)+' días');",
  "vida<60*48?fmt(vida/60,1)+' h':vida<60*24*730?fmt(vida/60/24,1)+' días':vida<60*24*365.25*1000?fmt(vida/60/24/365.25,1)+' años':'más de 1000 años');"),
],
"sonido_interactivo.html": [
 ("Sube el espectro hasta que L<sub>A</sub> pase de 90 a 93 dB(A): el tiempo permitido baja de 8 a 4 h.", "Al subir el espectro hasta que L<sub>A</sub> pase de 90 a 93 dB(A), el tiempo permitido baja de 8 a 4 h."),
],
"espectro_interactivo.html": [],
}
TODOS = [
 ('¿por qué me importa?', '¿por qué importa?'),
 ('<b>Tu recorrido.</b>', '<b>Recorrido.</b>'),
 ('(elige una opción primero)', '(falta elegir una opción)'), ('(elige una opción)', '(falta elegir una opción)'),
 ('Vibraciones — Exploradores interactivos', 'Vibraciones: exploradores interactivos'),
 ('(Versión 1.0)', '(Versión 1.1)'),
 ('. Halla ', '. Determinar '), ('Halla el ', 'Determinar el '), ('Halla la ', 'Determinar la '),
]

CANVAS = {
 "mohr_interactivo.html": [("'σ1'", "'σ_1'"), ("'σ2'", "'σ_2'"), ("'σ3 = 0'", "'σ_3 = 0'"), ("'σprom'", "'σ_{prom}'"), ("'σx′ = '", "'σ_{x′} = '"), ("'σy′ = '", "'σ_{y′} = '"),
   ("τx′y′ = '", "τ_{x′y′} = '"), ("'τmáx,abs = '", "'τ_{máx,abs} = '"), ("'(σ1, σ2)'", "'(σ_1, σ_2)'")],
 "fatiga_interactivo.html": [("'Kf·σa alternante (MPa)'", "'K_f·σ_a alternante (MPa)'"), ("'Se'", "'S_e'"), ("'Sut'", "'S_{ut}'"), ("'Sy'", "'S_y'"), ("'límite Se = '", "'límite S_e = '"),
   ("'sin límite: Sf = '", "'sin límite: S_f = '"), ("'σar < 20", "'σ_{ar} < 20"), ("'σar = '", "'σ_{ar} = '"), ("'σm < 0: Goodman usa σm = 0", "'σ_m < 0: Goodman usa σ_m = 0"),
   ("'σm medio (MPa)'", "'σ_m medio (MPa)'"), ("'σm+σa = Sy'", "'σ_m+σ_a = S_y'")],
 "espectro_interactivo.html": [("'Grms = √σ² = '", "'G_{rms} = √σ² = '")],
}
def lienzos(f, s):
    if f not in CANVAS: return s
    out = []
    for l in s.split("\n"):
        if "txt(" in l or "fillText(" in l:
            for a, b in CANVAS[f]: l = l.replace(a, b)
        out.append(l)
    return "\n".join(out)

def sustituir(f, s):
    for a, b in SUST.get(f, []) + TODOS:
        if a == b: continue
        if a in s: s = s.replace(a, b)
        elif b not in s and (a, b) not in TODOS: avisos.append("%s: no se encontró «%s»" % (f, a[:60]))
    return s

# ------------------------------------------------------------------ 3. estilo académico
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-⛿✀-➿⬅-⬇⌨️]‍?")
def emojis(s):
    s = s.replace("⬅ Antes:", "Antes:").replace("➡ <b>Siguiente:</b>", "<b>Siguiente:</b>").replace("➡ Siguiente:", "Siguiente:")
    s = re.sub(r"⌨\s*", "", s)
    s = EMOJI.sub("", s)
    s = re.sub(r"(<(?:h[1-6]|summary|b|span|div|p)[^>]*>)[  ]+(?=\S)", r"\1", s)
    return s

def rayas(s):
    reglas = [(r" — Explorador interactivo", ": explorador interactivo"), (r"(['\"])—\1", r"\1…\1"), (r">—<", ">…<"), (r"\? '—' :", "? '…' :"),
              (r"</b> — <b>", "</b>: <b>"), (r"</b> — ", "</b>: ")]
    for a, b in reglas: s = re.sub(a, b, s)
    s = re.sub(r" — ([^—\n<]{1,160}?) — ", r", \1, ", s)
    s = re.sub(r" — (?=(y|o|porque|pero|si|aunque|sino)\b)", ", ", s)
    s = re.sub(r" — ", ": ", s)
    s = re.sub(r"(\w)—(\w)", r"\1, \2", s)
    s = re.sub(r"—", "…", s)
    return s

UNI = dict(zip("₀₁₂₃₄₅₆₇₈₉ₐₑₒₓₕₖₗₘₙₚₛₜᵢᵣᵤᵥⱼ", "0123456789aeoxhklmnpstiruvj"))
RE_UNI = re.compile("[" + "".join(UNI) + "]+")
SALTA = {"title", "script", "style", "textarea", "option", "math", "svg", "canvas"}
def subindices(s):
    """Subíndices Unicode (F₀, ωₙ) -> <sub> en el texto visible del HTML estático."""
    out, pila, pos = [], [], 0
    for m in re.finditer(r"<!--.*?-->|<(/?)([a-zA-Z][a-zA-Z0-9]*)\b[^>]*?(/?)>", s, flags=re.S):
        txt = s[pos:m.start()]
        out.append(txt if pila else RE_UNI.sub(lambda q: "<sub>" + "".join(UNI[c] for c in q.group(0)) + "</sub>", txt))
        out.append(m.group(0)); pos = m.end()
        if m.group(0).startswith("<!--"): continue
        cierre, nombre, auto = m.group(1), m.group(2).lower(), m.group(3)
        if nombre in SALTA:
            if cierre:
                if nombre in pila: pila.remove(nombre)
            elif not auto: pila.append(nombre)
    out.append(s[pos:])
    return "".join(out)

# ------------------------------------------------------------------ 4. bloques comunes
FUENTES_VIEJAS = re.compile(r'\s*<link[^>]+fonts\.googleapis\.com/css2\?family=(Spectral|IBM\+Plex)[^>]*>', re.I)
def bloques(s):
    s = re.sub(re.escape(TIPO_INI) + r".*?" + re.escape(TIPO_FIN) + r"\n?", "", s, flags=re.S)
    s = re.sub(re.escape(TEC_INI) + r".*?" + re.escape(TEC_FIN) + r"\n?", "", s, flags=re.S)
    s = FUENTES_VIEJAS.sub("", s)
    m = re.search(r"<meta[^>]+charset[^>]*>", s, re.I); k = m.end()
    s = s[:k] + "\n" + TIPOGRAFIA + s[k:]
    marca = "<!-- contador:inicio -->" if "<!-- contador:inicio -->" in s else ("<!-- navbar:inicio -->" if "<!-- navbar:inicio -->" in s else "</body>")
    if "type=\"range\"" in s or "type=range" in s or 'type="number"' in s:
        s = s.replace(marca, TECLADO + "\n" + marca, 1)
    return s

def main():
    for f in sorted(x for x in os.listdir(D) if x.endswith(".html")):
        p = os.path.join(D, f); s0 = open(p, encoding="utf-8").read(); s = s0
        s = recuadros(f, s); s = sustituir(f, s); s = lienzos(f, s); s = emojis(s); s = rayas(s); s = subindices(s); s = bloques(s)
        open(p, "w", encoding="utf-8").write(s)
        print("%-34s %6d -> %6d  math:%3d  rayas:%d" % (f, len(s0), len(s), s.count("<math"), s.count("—")))
    for f in ("README.md", "CITATION.cff", ".zenodo.json", "temario.json", "normas.json"):
        p = os.path.join(D, f)
        if os.path.exists(p):
            s = open(p, encoding="utf-8").read(); t = rayas(s.replace("Vibraciones — Exploradores interactivos", "Vibraciones: exploradores interactivos"))
            if t != s: open(p, "w", encoding="utf-8").write(t); print("rayas retiradas de", f)
    for a in avisos: print("AVISO", a)

if __name__ == "__main__":
    main()
