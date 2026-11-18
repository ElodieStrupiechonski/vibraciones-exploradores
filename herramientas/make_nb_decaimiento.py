# -*- coding: utf-8 -*-
"""Genera el cuaderno «Tratamiento de un decaimiento libre medido con Phyphox» (Vibraciones, U7).
Escribe el .ipynb a mano (JSON) y un .py con las mismas celdas para probarlo sin Jupyter."""
import json
C = []
def md(t): C.append(("markdown", t.strip("\n")))
def code(t): C.append(("code", t.strip("\n")))

md(r"""
# Tratamiento de un decaimiento libre medido con Phyphox

**Vibraciones · Unidad 7 (temas 7.1 a 7.3) · ENES Juriquilla, UNAM**

Desplazamos y soltamos la punta de una viga en voladizo (la hoja de segueta), registramos la aceleración con Phyphox («Aceleración sin g») y de ese registro obtenemos la **frecuencia natural** $f_n$ y el **factor de amortiguamiento** $\zeta$ por dos caminos independientes. Al final comparamos con la teoría de vigas.

Modelo: un grado de libertad subamortiguado en vibración libre,

$$a(t)=A_0\,e^{-\sigma t}\cos(2\pi f_d\,t+\phi),\qquad \sigma=\zeta\,\omega_n=2\pi\zeta f_n,\qquad f_d=f_n\sqrt{1-\zeta^2}\approx f_n .$$

Todo el tratamiento consiste en estimar $f_d$ y $\sigma$; después $\zeta=\sigma/(2\pi f_n)$.

**Cómo usarlo.** Con el archivo de ejemplo (`segueta_10cm.csv`, una hoja de segueta de 10 cm en voladizo) el cuaderno corre sin cambios. Para un registro propio: subir a Colab, o copiar a la carpeta del cuaderno en Visual Studio Code, el archivo exportado de Phyphox (CSV o Excel) y escribir su nombre en la celda del paso 1. Cada paso tiene la matemática arriba y el código abajo. Instrucciones detalladas: https://elodiestrupiechonski.github.io/vibraciones-exploradores/tutorial_phyphox.html
""")
code(r"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
""")

md(r"""
## Paso 1 · Leer el archivo

Phyphox exporta cinco columnas: tiempo (s), $a_x$, $a_y$, $a_z$ y aceleración absoluta (m/s²). Trabajamos con **un solo eje**, el perpendicular a la hoja, y no con la aceleración absoluta: el valor absoluto rectifica la señal y duplica la frecuencia aparente.
""")
code(r"""
ARCHIVO = "segueta_10cm.csv"       # nombre del archivo exportado de Phyphox (.csv, .xls o .xlsx)
EJE = 3                            # 1 = x, 2 = y, 3 = z  (el eje perpendicular a la hoja; z es perpendicular a la pantalla)

# Datos de la viga para la comparación del paso 10 (poner los valores propios)
L_LIBRE = 0.100                    # longitud libre (m)
ESPESOR = 0.64e-3                  # espesor h (m); valor nominal de la hoja, medirlo con micrómetro
ANCHO = 12.7e-3                    # ancho b (m); solo interviene si hay masa en la punta
M_PUNTA = 0.0                      # masa sujeta a la punta (kg): teléfono, imán; 0 si la punta está libre

# Si el archivo de ejemplo no está en la carpeta de trabajo, se descarga del sitio del curso.
import os, urllib.request
EJEMPLO = "https://elodiestrupiechonski.github.io/vibraciones-exploradores/segueta_10cm.csv"
if not os.path.exists(ARCHIVO) and ARCHIVO == "segueta_10cm.csv":
    urllib.request.urlretrieve(EJEMPLO, ARCHIVO)

if not os.path.exists(ARCHIVO):
    raise SystemExit(f"No se encuentra «{ARCHIVO}». Debe estar en la misma carpeta que el cuaderno (en Colab: panel Archivos, subir). Archivos presentes: {sorted(os.listdir('.'))}")
if ARCHIVO.lower().endswith(".csv"):
    datos = pd.read_csv(ARCHIVO, sep=None, engine="python")
else:
    datos = pd.read_excel(ARCHIVO, sheet_name=0)
print(datos.columns.tolist())
t = datos.iloc[:, 0].to_numpy(float)
a = datos.iloc[:, EJE].to_numpy(float)
print(f"{len(t)} muestras, duración {t[-1]-t[0]:.2f} s")
""")

md(r"""
## Paso 2 · Frecuencia de muestreo real y límite de Nyquist

El teléfono no garantiza la frecuencia nominal. La medimos con los tiempos del registro:

$$f_s=\frac{N-1}{t_{N-1}-t_0},\qquad f_{\mathrm{Nyq}}=\frac{f_s}{2}.$$

Toda vibración por encima de $f_{\mathrm{Nyq}}$ se pliega y aparece en $f_a=|f-k\,f_s|$ (aliasing). También revisamos que el paso de tiempo sea uniforme, porque la FFT lo supone.
""")
code(r"""
dt = np.diff(t)
fs = (len(t) - 1) / (t[-1] - t[0])
print(f"f_s = {fs:.2f} Hz   Nyquist = {fs/2:.2f} Hz")
print(f"paso de tiempo: medio {dt.mean()*1e3:.3f} ms, mínimo {dt.min()*1e3:.3f} ms, máximo {dt.max()*1e3:.3f} ms")
print("muestreo uniforme" if (dt.max() - dt.min()) < 0.1 * dt.mean() else "ATENCIÓN: muestreo irregular; conviene remuestrear con np.interp")
""")

md(r"""
## Paso 3 · Quitar la media y recortar el decaimiento

Restamos la media (el sensor siempre deja un pequeño sesgo): $x_n=a_n-\bar a$.

Luego recortamos el tramo útil: empieza un poco **después** del golpe (el golpe mismo no es vibración libre) y termina cuando la señal se confunde con el ruido. Lo hacemos de forma automática con el máximo de $|x|$ y un umbral sobre el nivel de ruido medido antes del golpe.
""")
code(r"""
x = a - a.mean()
i_max = np.argmax(np.abs(x))
ruido = x[: max(10, i_max - int(0.3 * fs))].std()          # nivel de ruido antes del golpe
print(f"golpe en t = {t[i_max]:.2f} s, pico {np.abs(x[i_max]):.2f} m/s², ruido rms {ruido:.4f} m/s²")

fig, ax = plt.subplots(figsize=(9, 3))
ax.plot(t, x, lw=0.6); ax.axvline(t[i_max], color="r", ls="--")
ax.set_xlabel("t (s)"); ax.set_ylabel("a (m/s²)"); ax.set_title("Registro completo"); plt.show()
""")

md(r"""
## Paso 4 · Frecuencia natural con la FFT

Para $N$ muestras con ventana $w_n$, la transformada discreta es

$$X_k=\sum_{n=0}^{N-1}w_n\,x_n\,e^{-i2\pi kn/N},\qquad f_k=k\,\frac{f_s}{N},\qquad \Delta f=\frac{f_s}{N}=\frac1T .$$

La frecuencia natural es la del máximo de $|X_k|$. Dos cuidados:

- **Resolución.** $\Delta f=1/T$: con 3 s de decaimiento las líneas espectrales están cada 0.33 Hz. Rellenar con ceros (`nfft` grande) solo interpola entre líneas, no añade información.
- **Aliasing.** Si el pico queda por encima de $0.8\,f_s/2$, o las muestras alternan de signo una tras otra, la frecuencia real puede estar por encima de Nyquist.
- **Ventana.** Un decaimiento es un transitorio: su mayor amplitud está al inicio. Usamos media ventana de Hann decreciente, $w_n=\tfrac12\,[1+\cos(\pi n/N)]$, que vale 1 al inicio y 0 al final; la ventana de Hann completa borraría justo el tramo más intenso.

Refinamos el máximo con una parábola por los tres puntos vecinos del espectro en dB.
""")
code(r"""
T_ANALISIS = 4.0                                    # segundos de decaimiento que analizamos
i0 = i_max + int(0.05 * fs)                         # 50 ms después del golpe
i1 = min(len(x), i0 + int(T_ANALISIS * fs))
td, xd = t[i0:i1] - t[i0], x[i0:i1]

nfft = 2 ** 16
w = 0.5 * (1 + np.cos(np.pi * np.arange(len(xd)) / len(xd)))      # media ventana de Hann decreciente
X = np.abs(np.fft.rfft(xd * w, nfft))
f = np.fft.rfftfreq(nfft, 1 / fs)
k0 = int(2 / (f[1] - f[0]))                         # se ignora todo lo que esté por debajo de 2 Hz
k = np.argmax(X[k0:]) + k0
y0, y1, y2 = 20 * np.log10(X[k - 1 : k + 2])
fn_fft = f[k] + 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2) * (f[1] - f[0])
print(f"f_n (FFT) = {fn_fft:.2f} Hz    resolución real 1/T = {1/(td[-1]-td[0]):.2f} Hz")
if fn_fft > 0.8 * fs / 2:
    print("ATENCIÓN: pico por encima de 0.8·Nyquist, posible aliasing. Candidatos reales:", [round(v, 1) for v in (fs - fn_fft, fs + fn_fft)])

fig, ax = plt.subplots(figsize=(9, 3))
ax.semilogy(f, X / X.max()); ax.axvline(fn_fft, color="r", ls="--"); ax.axvline(fs / 2, color="gray", ls=":")
ax.set_xlim(0, fs / 2); ax.set_ylim(1e-4, 2); ax.set_xlabel("f (Hz)"); ax.set_ylabel("|X| normalizada"); plt.show()
""")

md(r"""
## Paso 5 · Aislar el modo con un filtro pasa banda

El registro trae otros componentes (soporte, mesa, armónicos). Dejamos pasar solo una banda alrededor de $f_n$ con un filtro Butterworth aplicado hacia adelante y hacia atrás (`filtfilt`), que **no desfasa** la señal.

La banda debe ser mucho más ancha que el pico ($2\zeta f_n$) para no alterar el decaimiento: usamos $\pm20\,\%$ de $f_n$.
""")
code(r"""
banda = [0.8 * fn_fft, min(1.2 * fn_fft, 0.98 * fs / 2)]
b, a_ = signal.butter(4, banda, btype="band", fs=fs)
xf_todo = signal.filtfilt(b, a_, x)                 # filtramos el registro completo y recortamos después
xf = xf_todo[i0:i1]
""")

md(r"""
## Paso 6 · Método 1: ajuste de la envolvente

La **señal analítica** $z(t)=x(t)+i\,\mathcal H\{x\}(t)$ (transformada de Hilbert) da la envolvente y la fase:

$$A(t)=|z(t)|=A_0\,e^{-\sigma t},\qquad f(t)=\frac{1}{2\pi}\frac{\mathrm d}{\mathrm dt}\arg z(t).$$

Tomando logaritmo, la envolvente es una recta:

$$\ln A(t)=\ln A_0-\sigma\,t .$$

Ajustamos por mínimos cuadrados; la pendiente es $-\sigma$ y entonces

$$\zeta=\frac{\sigma}{2\pi f_n}.$$

Usamos solo el tramo donde la envolvente está claramente por encima del ruido (aquí, más de 8 veces) y descartamos los bordes, donde la transformada de Hilbert se deforma.
""")
code(r"""
z = signal.hilbert(xf_todo)
A = np.abs(z)[i0:i1]
f_inst = (np.gradient(np.unwrap(np.angle(z)), t) / (2 * np.pi))[i0:i1]

ruido_f = xf_todo[: max(10, i_max - int(0.3 * fs))].std()
ok = (A > 8 * ruido_f) & (td > 0.05) & (td < td[-1] - 0.1)
ultimo = np.where(~ok & (td > 0.05))[0]
if len(ultimo): ok &= td < td[ultimo[0]]             # hasta la primera vez que cae bajo el umbral
pend, orden = np.polyfit(td[ok], np.log(A[ok]), 1)
sigma = -pend
fn_env = np.median(f_inst[ok])
zeta_env = sigma / (2 * np.pi * fn_env)
res = np.log(A[ok]) - (pend * td[ok] + orden)
r2 = 1 - res.var() / np.log(A[ok]).var()
print(f"tramo ajustado: {td[ok][0]:.2f} a {td[ok][-1]:.2f} s ({ok.sum()} muestras), R² = {r2:.4f}")
print(f"sigma = {sigma:.3f} 1/s    f_n = {fn_env:.2f} Hz    zeta (envolvente) = {zeta_env:.4f}")

fig, ax = plt.subplots(1, 2, figsize=(11, 3.2))
ax[0].plot(td, xf, lw=0.5); ax[0].plot(td, A, "C1"); ax[0].plot(td, -A, "C1")
ax[0].set_xlabel("t (s)"); ax[0].set_ylabel("a filtrada (m/s²)"); ax[0].set_title("Señal y envolvente")
ax[1].semilogy(td[ok], A[ok], ".", ms=3); ax[1].semilogy(td[ok], np.exp(pend * td[ok] + orden), "r")
ax[1].set_xlabel("t (s)"); ax[1].set_title("ln A es una recta de pendiente −σ"); plt.show()
""")

md(r"""
## Paso 7 · Método 2: decremento logarítmico

Si $x_0$ y $x_n$ son dos máximos separados por $n$ ciclos,

$$\delta=\frac1n\ln\frac{x_0}{x_n},\qquad \zeta=\frac{\delta}{\sqrt{4\pi^2+\delta^2}}\approx\frac{\delta}{2\pi}.$$

Con solo dos máximos, el ruido de cada uno pasa entero al resultado. Es mejor usar **todos**: como $\ln x_j=\ln x_0-\delta\,j$, el decremento es el negativo de la pendiente de la recta de $\ln x_j$ contra el número de ciclo $j$. La celda calcula las dos versiones para compararlas.

La frecuencia sale de los mismos máximos: $f_d=n/(t_n-t_0)$. Conviene tener 20 ciclos o más cuando $\zeta$ es pequeño.

Como el pico verdadero casi nunca coincide con una muestra, lo interpolamos con una parábola por tres puntos.
""")
code(r"""
pk, _ = signal.find_peaks(xf, height=8 * ruido_f, distance=int(0.6 * fs / fn_fft))
pk = pk[(pk > 0) & (pk < len(xf) - 1) & (td[pk] <= td[ok][-1])]      # solo el tramo ajustado: ahí ningún máximo se pierde bajo el umbral
ya, yb, yc = xf[pk - 1], xf[pk], xf[pk + 1]
corr = 0.5 * (ya - yc) / (ya - 2 * yb + yc)          # corrección parabólica, en muestras
tp = td[pk] + corr / fs
xp = yb - 0.25 * (ya - yc) * corr

n = len(xp) - 1
delta2 = np.log(xp[0] / xp[n]) / n                                  # con dos máximos (el primero y el último)
delta = -np.polyfit(np.arange(len(xp)), np.log(xp), 1)[0]           # con todos: pendiente de ln x_j contra j
zeta_dec = delta / np.sqrt(4 * np.pi ** 2 + delta ** 2)
fd_dec = n / (tp[n] - tp[0])
print(f"n = {n} ciclos: x0 = {xp[0]:.3f}, xn = {xp[n]:.3f} m/s²")
print(f"delta (dos máximos) = {delta2:.4f}    delta (regresión) = {delta:.4f}")
print(f"zeta (decremento) = {zeta_dec:.4f}    f_d = {fd_dec:.2f} Hz")
""")

md(r"""
## Paso 8 · ¿Es lineal el sistema? Amortiguamiento y frecuencia contra amplitud

Un sistema lineal tiene $\zeta$ y $f_n$ constantes. Repetimos el decremento en bloques de 10 ciclos: si $\zeta$ baja o $f_n$ sube al disminuir la amplitud, hay no linealidad (sujeción que desliza, fricción, aire). Esa dispersión indica cuánto depende el resultado del tramo elegido; la **incertidumbre** de la medición se estima con la desviación estándar de las repeticiones del ensayo.
""")
code(r"""
m = 10
filas = []
for j in range(0, len(xp) - m, m):
    if xp[j + m] < 20 * ruido_f: break               # los bloques cercanos al ruido no son fiables
    d = np.log(xp[j] / xp[j + m]) / m
    filas.append((xp[j], m / (tp[j + m] - tp[j]), d / np.sqrt(4 * np.pi ** 2 + d ** 2)))
tabla = pd.DataFrame(filas, columns=["amplitud inicial (m/s²)", "f_d (Hz)", "zeta"])
print(tabla.round(4).to_string(index=False))
print(f"\nzeta = {tabla.zeta.mean():.4f} ± {tabla.zeta.std():.4f}    f_d = {tabla['f_d (Hz)'].mean():.2f} ± {tabla['f_d (Hz)'].std():.2f} Hz")
""")

md(r"""
## Paso 9 · ¿Y la media potencia?

En el espectro, $\zeta\approx\Delta f/(2f_n)$ con $\Delta f=f_2-f_1$ medido donde $|X|$ cae a $1/\sqrt2$ del máximo. Solo funciona si la resolución alcanza: el ancho del pico es $2\zeta f_n$ y el registro debe durar

$$T\geq\frac{2}{\zeta f_n}$$

para tener al menos cuatro líneas espectrales dentro de ese ancho. La celda lo comprueba con los valores medidos.
""")
code(r"""
ancho = 2 * zeta_env * fn_env
T_min = 2 / (zeta_env * fn_env)
print(f"ancho de media potencia 2·zeta·f_n = {ancho:.3f} Hz;  resolución disponible 1/T = {1/td[-1]:.3f} Hz")
print(f"duración mínima para usar media potencia: {T_min:.1f} s;  duración analizada: {td[-1]:.1f} s")
print("media potencia utilizable" if td[-1] >= T_min else "media potencia NO utilizable con este registro: usar la envolvente o el decremento")
""")

md(r"""
## Paso 10 · Comparación con la teoría de vigas

Primer modo de una viga en voladizo de sección rectangular (ancho $b$, espesor $h$, longitud libre $L$):

$$f_1=\frac{\beta_1^2}{2\pi L^2}\sqrt{\frac{EI}{\mu}},\qquad \beta_1=1.875,\qquad I=\frac{b\,h^3}{12},\qquad \mu=\rho\,b\,h
\quad\Longrightarrow\quad f_1=\frac{\beta_1^2\,h}{2\pi L^2}\sqrt{\frac{E}{12\,\rho}} .$$

El ancho $b$ se cancela: la frecuencia depende de $h/L^2$. Por eso un error del 5 % en $L$ cambia $f_1$ un 10 %, y el espesor debe medirse con micrómetro.

Si la medición no coincide, despejamos qué longitud efectiva (o qué espesor) la explicaría: una sujeción que no empotra bien se comporta como una viga más larga.

**Masa en la punta.** La fórmula anterior vale para la viga sola. Si en la punta va una masa $M$ (el teléfono, un imán), la frecuencia baja mucho. Con la rigidez en la punta $k=3EI/L^3$ y la masa de la viga $m_v=\rho\,b\,h\,L$, la aproximación de Rayleigh da

$$f_1\approx\frac{1}{2\pi}\sqrt{\frac{3EI}{L^3\,(M+\tfrac{33}{140}\,m_v)}} .$$

Una hoja de segueta de 10 cm pesa unos 6 g y un teléfono unos 180 g: con el teléfono en la punta la frecuencia cae de decenas de hertz a unos 5 Hz. Con $M=0$ esta aproximación queda 1.5 % por encima del valor exacto.
""")
code(r"""
E, rho = 200e9, 7850          # acero: Pa, kg/m³
L, h, b = L_LIBRE, ESPESOR, ANCHO   # definidos en el paso 1

f_teo = 1.875 ** 2 * h / (2 * np.pi * L ** 2) * np.sqrt(E / (12 * rho))
L_ef = np.sqrt(1.875 ** 2 * h / (2 * np.pi * fn_env) * np.sqrt(E / (12 * rho)))
h_ef = fn_env * 2 * np.pi * L ** 2 / 1.875 ** 2 / np.sqrt(E / (12 * rho))
print(f"teoría: {f_teo:.1f} Hz    medido: {fn_env:.1f} Hz    diferencia: {100*(fn_env-f_teo)/f_teo:+.0f} %")
print(f"longitud efectiva que explica la medición (con h = {h*1e3:.2f} mm): {L_ef*100:.1f} cm")
print(f"espesor que explica la medición (con L = {L*100:.1f} cm): {h_ef*1e3:.2f} mm")
I, m_v = b * h ** 3 / 12, rho * b * h * L
f_masa = np.sqrt(3 * E * I / (L ** 3 * (M_PUNTA + 33 / 140 * m_v))) / (2 * np.pi)
print(f"masa de la viga: {m_v*1e3:.1f} g;  con M = {M_PUNTA*1e3:.0f} g en la punta (Rayleigh): {f_masa:.1f} Hz")
""")

md(r"""
## Paso 11 · Resumen para la bitácora
""")
code(r"""
print("RESULTADOS")
print(f"  f_s = {fs:.1f} Hz (Nyquist {fs/2:.1f} Hz)")
print(f"  f_n: FFT {fn_fft:.2f} Hz · fase {fn_env:.2f} Hz · picos {fd_dec:.2f} Hz")
print(f"  zeta: envolvente {zeta_env:.4f} · decremento {zeta_dec:.4f} · por bloques {tabla.zeta.mean():.4f} ± {tabla.zeta.std():.4f}")
dif = 100 * abs(zeta_env - zeta_dec) / zeta_env
print(f"  diferencia entre los dos métodos: {dif:.0f} %")
print("CRITERIOS")
for texto, cumple in [(f"pico por debajo de 0.8·Nyquist ({fn_fft:.1f} Hz frente a {0.8*fs/2:.1f} Hz)", fn_fft < 0.8 * fs / 2),
                      (f"al menos 20 ciclos en el tramo ({n})", n >= 20),
                      (f"R² de la envolvente ≥ 0.97 ({r2:.3f})", r2 >= 0.97),
                      (f"los dos métodos difieren menos de 30 % ({dif:.0f} %)", dif < 30)]:
    print(f"  {'cumple   ' if cumple else 'NO cumple'} · {texto}")
""")

md(r"""
## Lista de verificación antes de reportar

Son los mismos criterios del tutorial del sitio; la celda anterior imprime «cumple» o «NO cumple» para los cuatro primeros.

1. ¿El pico del espectro está por debajo de $0.8\,f_s/2$? Si no, alargar la viga o medir con otro sensor.
2. ¿El tramo ajustado tiene al menos 20 ciclos?
3. ¿La recta de $\ln A$ tiene $R^2\geq0.97$?
4. ¿Los dos métodos dan $\zeta$ con menos de 30 % de diferencia? Si no, revisar el tramo elegido y la banda del filtro.
5. ¿$\zeta$ o $f_n$ cambian con la amplitud? Reportarlo: es información sobre la sujeción.
6. Repetir el ensayo al menos tres veces: $f_n$ debe repetirse dentro de 2 %; reportar media y desviación estándar.

**Referencias.** Inman, *Engineering Vibration*, 4.ª ed., secs. 1.6 (decremento logarítmico) y 7.2 a 7.4 (medición); Rao, *Mechanical Vibrations*, 5.ª ed., cap. 8 (vigas) y sec. 2.5 (método de Rayleigh). Ewins, *Modal Testing*, 2.ª ed., cap. 3. Bendat y Piersol, *Random Data*, 4.ª ed., cap. 13 (transformada de Hilbert). Staacks et al. (2018), *Phys. Educ.* 53, 045009, doi:10.1088/1361-6552/aac05e.
""")

nb = {"cells": [], "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}
for i, (k, s) in enumerate(C):
    c = {"cell_type": k, "id": "c%02d" % i, "metadata": {}, "source": s.splitlines(keepends=True)}
    if k == "code": c.update(execution_count=None, outputs=[])
    nb["cells"].append(c)
json.dump(nb, open("Tratamiento_decaimiento_Phyphox.ipynb", "w", encoding="utf8"), ensure_ascii=False, indent=1)
open("prueba_nb.py", "w", encoding="utf8").write("import matplotlib; matplotlib.use('Agg')\n" + "\n\n".join(s for k, s in C if k == "code"))
print(len(C), "celdas")
