#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera tutorial_phyphox.html · Tutorial: del teléfono a la frecuencia natural y al amortiguamiento (U7, tema 7.1).
Incluye las ligas de descarga de Phyphox, del cuaderno de Jupyter y del registro de ejemplo, las instrucciones para
Colab y Visual Studio Code y un analizador en el navegador que reproduce los pasos del cuaderno.
Uso: python3 gen_tutorial.py CARPETA RUTA_segueta_10cm.csv"""
from base_pag import *
import csv, json
REPO = "elodiestrupiechonski/vibraciones-exploradores"
NB = "Tratamiento_decaimiento_Phyphox.ipynb"
COLAB = f"https://colab.research.google.com/github/{REPO}/blob/main/{NB}"
filas = list(csv.reader(open(sys.argv[2], encoding="utf-8")))[1:]
t = [float(r[0]) for r in filas]; z = [float(r[3]) for r in filas]
EJ = json.dumps({"t0": round(t[0], 5), "dt": round((t[-1] - t[0]) / (len(t) - 1), 8), "z": [round(v, 4) for v in z]}, separators=(",", ":"))

def paso(n, titulo, cuerpo):
    return f'''<section class="card full paso" id="paso{n}"><h2><span class="np">{n}</span>{titulo}<label class="hecho"><input type="checkbox" data-paso="{n}"> hecho</label></h2>
{cuerpo}
</section>'''
def boton(href, texto, extra=""): return f'<a class="btn dl" href="{href}" {extra}>{texto}</a>'
ext = 'target="_blank" rel="noopener"'

cuerpo = f"""
  <div class="intro full">
    <b>¿Para qué sirve este tutorial?</b> Con un teléfono y una regla, una hoja de segueta o cualquier estructura ligera se mide un <b>decaimiento libre</b>; de ese registro salen la frecuencia natural <i>f</i><sub>n</sub> y el factor de amortiguamiento ζ. El recorrido tiene siete pasos: instalar la aplicación, medir, exportar, descargar el cuaderno de análisis, abrirlo en Google Colab o en Visual Studio Code, comprobar el resultado con el analizador de esta página y revisar la lista de verificación. Cada paso se puede marcar como hecho; el avance se conserva en este navegador.
    <div class="prog"><div id="barra"></div></div>
    <nav class="indice" id="indice" aria-label="Pasos del tutorial"></nav>
  </div>

{paso(1, "Instalar Phyphox en el teléfono", f'''
  <p>Phyphox (<i>physical phone experiments</i>) es una aplicación gratuita y de código abierto de la Universidad RWTH de Aquisgrán que da acceso a los sensores del teléfono: acelerómetro, giroscopio, magnetómetro, micrófono. No requiere cuenta ni conexión para medir.</p>
  <div class="btns">
    {boton("https://phyphox.org/download/", "Página oficial de descarga (phyphox.org)", ext)}
    {boton("https://play.google.com/store/apps/details?id=de.rwth_aachen.phyphox", "Android: Google Play", ext)}
    {boton("https://apps.apple.com/app/phyphox/id1127716348", "iPhone: App Store", ext)}
  </div>
  <p class="nota">Comprobación: al abrir la aplicación aparece la lista de experimentos; en el grupo «Sensores» está «Aceleración (sin g)». Referencia: Staacks, Hütz, Heinke y Stampfer (2018), Phys. Educ. 53, 045009, <a href="https://doi.org/10.1088/1361-6552/aac05e" {ext}>doi:10.1088/1361-6552/aac05e</a>.</p>''')}

{paso(2, "Montar el experimento y medir", f'''
  <div class="two"><div>
  <ol>
    <li>Sujetar la viga (hoja de segueta, regla) con una prensa al borde de una mesa rígida y medir con el calibrador la <b>longitud libre</b> <i>L</i>, el ancho <i>b</i> y el espesor <i>h</i>.</li>
    <li>Colocar el teléfono y anotar dónde quedó. Hay dos montajes: (a) <b>teléfono junto al empotramiento</b>, sobre la prensa o la mesa, pegado con cinta: no añade masa a la viga y registra la vibración que esta transmite al soporte, con señal pequeña pero frecuencia sin alterar; (b) <b>teléfono sobre la viga</b>: la señal es grande, pero su masa baja mucho la frecuencia y hay que pesarlo e incluirlo en el cálculo (recuadro de la derecha).</li>
    <li>Identificar el eje: en Phyphox <i>x</i> va a lo ancho de la pantalla, <i>y</i> a lo largo y <i>z</i> es perpendicular a la pantalla. Se analiza el eje que queda en la dirección del movimiento de la viga.</li>
    <li>En Phyphox abrir «Aceleración (sin g)». En el menú ⋮ activar «Medición temporizada»: 3 s de retraso y de 10 a 12 s de duración.</li>
    <li>Iniciar con ▶, esperar el retraso, <b>desplazar la punta y soltarla</b> (o dar un golpe corto) y dejar que la vibración se extinga sin tocar la mesa.</li>
    <li>Repetir al menos tres veces con la misma longitud y guardar cada registro por separado.</li>
  </ol>
  </div><div>
  {eq("1 · Antes de medir: ¿alcanza la frecuencia de muestreo?", M(r"f_{\mathrm{Nyq}}=\frac{f_s}{2},\qquad f_n\lesssim 0.8\,f_{\mathrm{Nyq}}") + nota("un teléfono típico muestrea entre 100 y 500 Hz; con <i>f</i><sub>s</sub> = 200 Hz conviene que <i>f</i><sub>n</sub> quede por debajo de 80 Hz"))}
  {eq("2 · Estimación previa: viga en voladizo sin masa añadida", M(r"f_1=\frac{1.875^2}{2\pi L^2}\sqrt{\frac{E\,h^2}{12\,\rho}}") + nota("acero: <i>E</i> = 200 GPa, ρ = 7850 kg/m<sup>3</sup>. Para <i>L</i> = 10 cm: con el espesor nominal <i>h</i> = 0.64 mm resulta <i>f</i><sub>1</sub> ≈ 52 Hz; con <i>h</i> = 0.50 mm, 41 Hz. La frecuencia es proporcional a <i>h</i>/<i>L</i><sup>2</sup>: el espesor se mide con micrómetro. Si <i>f</i><sub>1</sub> queda cerca de Nyquist, alargar la viga."))}
  {eq("3 · Con una masa <i>M</i> en la punta (teléfono, imán)", M(r"f_1\approx\frac{1}{2\pi}\sqrt{\frac{3EI}{L^3\left(M+\frac{33}{140}\,m_v\right)}},\qquad I=\frac{b\,h^3}{12},\qquad m_v=\rho\,b\,h\,L") + nota("aproximación de Rayleigh. Una hoja de 10 cm pesa unos 6 g; con un teléfono de 180 g en la punta la frecuencia cae de unos 50 Hz a unos 5 Hz"))}
  </div></div>''')}

{paso(3, "Exportar los datos", f'''
  <ol>
    <li>Con la medición en pantalla, abrir el menú ⋮ y elegir «Exportar datos».</li>
    <li>Elegir el formato <b>CSV (Comma, decimal point)</b>. Phyphox entrega un archivo ZIP.</li>
    <li><b>Descomprimir el ZIP</b> y tomar el archivo <code>Raw Data.csv</code>, que contiene cinco columnas: tiempo (s), <i>a</i><sub>x</sub>, <i>a</i><sub>y</sub>, <i>a</i><sub>z</sub> y aceleración absoluta (m/s<sup>2</sup>). El formato Excel también sirve para el cuaderno, pero el analizador del paso 6 solo lee CSV.</li>
    <li>Enviar el archivo a la computadora (correo, Drive, cable) y renombrarlo sin espacios ni acentos, con la longitud y la repetición: <code>segueta_L10cm_rep1.csv</code>.</li>
  </ol>
  <p class="nota">Se analiza un solo eje, el de la dirección del movimiento, nunca la aceleración absoluta: el valor absoluto rectifica la señal y duplica la frecuencia aparente.</p>''')}

{paso(4, "Descargar el cuaderno de análisis y el registro de ejemplo", f'''
  <p>El cuaderno de Jupyter contiene el tratamiento completo en once pasos, cada uno con su fundamento matemático y su código en Python: lectura, frecuencia de muestreo real, recorte, espectro, filtro pasabanda, envolvente de Hilbert, decremento logarítmico, análisis por bloques y comparación con la teoría de vigas.</p>
  <div class="btns">
    {boton(NB, "Descargar el cuaderno (.ipynb)", "download")}
    {boton("segueta_10cm.csv", "Descargar el registro de ejemplo (.csv)", "download")}
    {boton(COLAB, "Abrir el cuaderno directamente en Colab", ext)}
  </div>
  <p class="nota">Registro de ejemplo: hoja de segueta de acero de 10 cm en voladizo, 2390 muestras a 198.9 Hz en 12 s. La frecuencia medida corresponde a la hoja sin masa añadida en la punta. Resultado esperado con el cuaderno: <i>f</i><sub>n</sub> entre 40.3 Hz (espectro) y 40.6 Hz (fase y máximos), ζ = 0.0034 por los dos métodos. El analizador del paso 6 da 40.3 Hz y ζ entre 0.0035 y 0.0036. La frecuencia de este registro sube cerca de 2 % mientras la amplitud decae (de 40.1 a 40.9 Hz), señal de una ligera no linealidad de la sujeción; por eso cada estimador, que pondera distinto el inicio y el final, da un valor algo diferente. Si al pulsar la liga el navegador muestra texto en lugar de descargar, usar el botón derecho y «Guardar enlace como».</p>''')}

{paso(5, "Abrir y ejecutar el cuaderno", f'''
  <div class="btns"><button class="btn on" id="tabC">Opción A · Google Colab (sin instalar nada)</button><button class="btn" id="tabV">Opción B · Visual Studio Code (Python instalado)</button></div>
  <div id="panC">
  <ol>
    <li>Abrir <a href="{COLAB}" {ext}>el cuaderno en Colab</a> con una cuenta de Google. Otra vía: en <a href="https://colab.research.google.com/" {ext}>colab.research.google.com</a>, menú Archivo → Subir cuaderno, y elegir el archivo <code>.ipynb</code> descargado.</li>
    <li>Guardar una copia propia: Archivo → Guardar una copia en Drive. Sin este paso los cambios se pierden al cerrar.</li>
    <li>Subir el registro: en la barra izquierda abrir el panel «Archivos» (icono de carpeta), pulsar «Subir al almacenamiento de la sesión» y elegir el CSV. Con el registro de ejemplo no hace falta: el cuaderno lo descarga solo.</li>
    <li>En la celda del paso 1 escribir el nombre del archivo y el eje: <code>ARCHIVO = "segueta_L10cm_rep1.csv"</code>, <code>EJE = 3</code> (1 = <i>x</i>, 2 = <i>y</i>, 3 = <i>z</i>).</li>
    <li>Ejecutar todo: Entorno de ejecución → Ejecutar todas (Ctrl + F9). Las gráficas aparecen debajo de cada celda y el resumen al final.</li>
  </ol>
  <p class="nota">Los archivos subidos a la sesión se borran cuando Colab se desconecta; el cuaderno guardado en Drive permanece. Las bibliotecas necesarias (NumPy, SciPy, pandas, Matplotlib) ya están instaladas en Colab.</p>
  </div>
  <div id="panV" style="display:none">
  <ol>
    <li>Requisitos: <a href="https://www.python.org/downloads/" {ext}>Python 3.10 o posterior</a> y <a href="https://code.visualstudio.com/" {ext}>Visual Studio Code</a> con las extensiones «Python» y «Jupyter» de Microsoft (panel Extensiones, Ctrl + Mayús + X).</li>
    <li>Crear una carpeta de trabajo y copiar en ella el cuaderno y el archivo CSV. En VS Code: Archivo → Abrir carpeta.</li>
    <li>Instalar las bibliotecas una sola vez. En el menú Terminal → Nuevo terminal:
      <pre class="cod">python -m pip install numpy scipy pandas matplotlib openpyxl xlrd ipykernel</pre>
      En Windows, si <code>python</code> no se reconoce, usar <code>py -m pip install …</code>.</li>
    <li>Abrir el archivo <code>.ipynb</code>; arriba a la derecha pulsar «Seleccionar kernel» → «Entornos de Python» y elegir la instalación donde se instalaron las bibliotecas.</li>
    <li>En la celda del paso 1 escribir <code>ARCHIVO</code> y <code>EJE</code>, y pulsar «Ejecutar todo».</li>
  </ol>
  <div style="overflow-x:auto"><table class="tb">
    <tr><th>Mensaje</th><th>Causa</th><th>Solución</th></tr>
    <tr><td><code>ModuleNotFoundError: No module named 'scipy'</code></td><td>el kernel elegido no es el Python donde se instaló</td><td>cambiar de kernel o repetir la instalación con ese intérprete</td></tr>
    <tr><td><code>FileNotFoundError</code></td><td>el CSV no está en la carpeta del cuaderno o el nombre no coincide</td><td>copiar el archivo junto al cuaderno; revisar mayúsculas y extensión</td></tr>
    <tr><td>Se pide instalar <code>ipykernel</code></td><td>falta el paquete que conecta Python con el cuaderno</td><td>aceptar la instalación que ofrece VS Code</td></tr>
    <tr><td>Columnas desplazadas o texto en lugar de números</td><td>se exportó con coma decimal</td><td>volver a exportar como «CSV (Comma, decimal point)»</td></tr>
  </table></div>
  </div>''')}

{paso(6, "Comprobar el resultado con el analizador", f'''
  <p>El analizador repite en el navegador los pasos centrales del cuaderno: quita la media, localiza el golpe, calcula el espectro, filtra alrededor del pico, obtiene la envolvente con la transformada de Hilbert y ajusta una recta a ln <i>A</i>(<i>t</i>). Sirve para verificar que el cuaderno y el registro propio dan valores coherentes. El archivo no sale del dispositivo.</p>
  <div class="two an"><div>
    <canvas id="c1" width="760" height="260" aria-label="Señal filtrada, envolvente y tramo ajustado"></canvas>
    <canvas id="c2" width="760" height="300" style="margin-top:10px" aria-label="Espectro y recta de la envolvente"></canvas>
    <div class="legend">
      <span><i class="sw" style="border-top-color:var(--grey)"></i> señal medida</span>
      <span><i class="sw" style="border-top-color:var(--steel)"></i> señal filtrada</span>
      <span><i class="sw" style="border-top-color:var(--orange)"></i> envolvente <i>A</i>(<i>t</i>)</span>
      <span><i class="sw" style="border-top-color:var(--red);border-top-style:dashed"></i> ajuste exponencial</span>
      <span><i class="sw" style="border-top-color:var(--green)"></i> máximos (decremento)</span>
    </div>
  </div><div>
    <div class="grp"><div class="t">Señal</div>
      <div class="row"><label>Origen</label><select id="origen"><option value="ej">Ejemplo: segueta de 10 cm (registro real)</option><option value="csv">Archivo CSV propio</option><option value="sint">Señal sintética</option></select></div>
      <div id="gcsv" style="display:none"><input class="archivo" type="file" id="csv" accept=".csv,.txt,text/csv">
        <div class="row" style="margin-top:8px"><label>Columna</label><select id="col"></select></div>
        <div class="nota" id="csvinfo">Archivo <code>Raw Data.csv</code> de Phyphox (formato CSV; el Excel no se lee aquí). La primera columna debe ser el tiempo en segundos.</div></div>
      <div id="gsint" style="display:none">
        {fila("Frecuencia natural <i>f</i><sub>n</sub>", "fn", 5, 300, 0.5, 40, "Hz")}
        {fila("Amortiguamiento ζ", "ze", 0.001, 0.05, 0.0005, 0.004)}
        {fila("Muestreo <i>f</i><sub>s</sub>", "fs", 50, 500, 1, 200, "Hz")}
        {fila("Ruido (% de la amplitud)", "ru", 0, 20, 0.5, 2, "%")}
      </div>
    </div>
    <div class="grp"><div class="t">Análisis</div>
      {fila("Semiancho del filtro (% de <i>f</i><sub>n</sub>)", "bw", 5, 50, 1, 20, "%")}
      {fila("Inicio del ajuste tras el golpe", "ti", 0, 1, 0.01, 0.05, "s")}
      {fila("Fin del ajuste: <i>A</i> cae a", "um", 5, 80, 1, 25, "%")}
    </div>
    <div class="tiles">
      {tile("Muestreo real <i>f</i><sub>s</sub>", "ofs")}{tile("Nyquist <i>f</i><sub>s</sub>/2", "ony")}
      {tile("<i>f</i><sub>d</sub> ≈ <i>f</i><sub>n</sub> (pico del espectro)", "ofp", "hl")}{tile("<i>f</i><sub>d</sub> (entre máximos)", "ofd")}
      {tile("ζ por envolvente", "oze", "hl")}{tile("ζ por decremento", "ozd", "hl")}
      {tile("Tasa de decaimiento σ", "osg")}{tile("Ajuste: <i>R</i><sup>2</sup> y ciclos", "or2")}
    </div>
    <div class="nota" id="aviso"></div>
  </div></div>
  <div class="two" style="margin-top:10px"><div>
  {eq("4 · Modelo del decaimiento", M(r"a(t)=A_0\,e^{-\sigma t}\cos(2\pi f_d t+\phi),\qquad \sigma=2\pi\zeta f_n"))}
  {eq("5 · Envolvente: recta en escala logarítmica", M(r"\ln A(t)=\ln A_0-\sigma\,t\qquad\Rightarrow\qquad \zeta=\frac{\sigma}{2\pi f_n}"))}
  </div><div>
  {eq("6 · Decremento logarítmico con <i>n</i> ciclos", M(r"\delta=\frac{1}{n}\ln\frac{x_0}{x_n},\qquad \zeta=\frac{\delta}{\sqrt{4\pi^2+\delta^2}}") + nota("aquí, y en el cuaderno, δ es el negativo de la pendiente de ln <i>x</i><sub>j</sub> contra el número de ciclo <i>j</i>, que usa todos los máximos"))}
  {eq("7 · Aliasing: frecuencia aparente", M(r"f_a=|f-k\,f_s|") + nota("<i>k</i> es el entero más cercano a <i>f</i>/<i>f</i><sub>s</sub>. Con la señal sintética, <i>f</i><sub>n</sub> = 150 Hz y <i>f</i><sub>s</sub> = 200 Hz producen un pico falso en 50 Hz, y el amortiguamiento calculado con esa frecuencia resulta tres veces mayor que el verdadero"))}
  </div></div>''')}

{paso(7, "Lista de verificación y qué reportar", f'''
  <div class="two"><div>
  <b>Antes de aceptar un resultado</b>
  <ul>
    <li>El pico del espectro queda por debajo de 0.8 <i>f</i><sub>s</sub>/2. Si está pegado a Nyquist puede ser un alias: alargar la viga y repetir.</li>
    <li>El tramo ajustado contiene al menos 20 ciclos y la recta de ln <i>A</i> tiene <i>R</i><sup>2</sup> ≥ 0.97.</li>
    <li>Los dos métodos (envolvente y decremento) difieren menos de 30 %. Esa diferencia indica la sensibilidad al tratamiento; la incertidumbre se estima con la desviación estándar de las repeticiones.</li>
    <li>Las tres repeticiones dan <i>f</i><sub>n</sub> dentro de 2 %.</li>
    <li>La frecuencia medida se compara con la fórmula que corresponde al montaje (viga sola o con masa en la punta); una diferencia de 10 a 25 % suele deberse al espesor real, a un empotramiento imperfecto o a una masa añadida que no se tomó en cuenta.</li>
    <li>Son los mismos criterios que imprime el cuaderno al final («cumple» o «NO cumple»).</li>
  </ul>
  </div><div>
  <b>Qué entregar</b>
  <ul>
    <li>Fotografía del montaje con la longitud libre visible, posición del teléfono y tabla con <i>L</i>, <i>b</i>, <i>h</i>, la masa del teléfono (si va sobre la viga) y su modelo.</li>
    <li><i>f</i><sub>s</sub> real, <i>f</i><sub>n</sub> y ζ por los dos métodos, con media y desviación de las repeticiones.</li>
    <li>Las gráficas del cuaderno: señal, espectro y recta de la envolvente.</li>
    <li>Comparación con la teoría y discusión de la diferencia.</li>
    <li>Los archivos CSV y el cuaderno ejecutado, en la carpeta del equipo.</li>
  </ul>
  <b>Errores frecuentes</b>
  <ul>
    <li>Analizar la aceleración absoluta en lugar de un eje.</li>
    <li>Incluir el golpe en el tramo de ajuste.</li>
    <li>Usar el método de media potencia con un registro corto: se requiere <i>T</i> ≥ 2/(ζ <i>f</i><sub>n</sub>), unos 15 s de decaimiento para este ejemplo.</li>
  </ul>
  </div></div>
  <p class="nota">Para profundizar: <a href="senales_interactivo.html">Laboratorio de señales</a> (muestreo, aliasing, ventanas) y <a href="modal_interactivo.html">Extracción de parámetros modales</a> (media potencia y círculo de Nyquist). Bibliografía: Inman, <i>Engineering Vibration</i>, 4.ª ed., secs. 1.3 y 1.6; Rao, <i>Mechanical Vibrations</i>, 5.ª ed., sec. 2.6 (decremento logarítmico) y cap. 8 (vigas); Bendat y Piersol, <i>Random Data</i>, 4.ª ed., cap. 13 (transformada de Hilbert).</p>''')}
"""
EXTRA_T = """<style>
  .paso h2{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
  .np{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;border-radius:50%;background:var(--navy);color:#fff;font-size:15px;flex:none}
  .hecho{margin-left:auto;font-size:12.5px;font-weight:400;color:var(--grey);display:flex;align-items:center;gap:7px;cursor:pointer;min-height:32px;padding:0 4px}
  .hecho input{width:20px;height:20px}
  .paso.ok .np{background:var(--green)}
  .paso ol,.paso ul{margin:8px 0 8px 0;padding-left:22px;line-height:1.55;font-size:14.5px} .paso li{margin-bottom:5px}
  .paso p{font-size:14.5px;line-height:1.55;margin:8px 0}
  a.btn.dl{display:inline-block;text-decoration:none}
  .prog{height:6px;background:var(--line);border-radius:3px;margin:12px 0 8px;overflow:hidden} #barra{height:100%;width:0;background:var(--green);transition:width .2s}
  .indice{display:flex;flex-wrap:wrap;gap:6px} .indice a{font-size:12.5px;text-decoration:none;color:var(--navy);border:1px solid var(--line);border-radius:14px;padding:3px 10px;background:#fff}
  .indice a.ok{border-color:var(--green);color:var(--green)}
  code,pre.cod{font-family:Consolas,"Courier New",monospace;font-size:13px;background:#F3F5FA;border:1px solid var(--line);border-radius:5px;padding:1px 5px}
  pre.cod{padding:8px 10px;overflow-x:auto;margin:6px 0;white-space:pre}
  @media(min-width:900px){.two.an{grid-template-columns:1.25fr 1fr}}
</style>"""
script = LIB + r"""
const EJ=__EJ__;
let S={origen:'ej',fn:40,ze:0.004,fs:200,ru:2,bw:20,ti:0.05,um:25}, CSV=null, R=null;
const UN={fn:' Hz',ze:'',fs:' Hz',ru:' %',bw:' %',ti:' s',um:' %'}, TP=2*Math.PI;
function rng(seed){ let a=seed>>>0; return function(){ a|=0; a=a+0x6D2B79F5|0; let t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }
function fft2(re,im){ const n=re.length; for(let i=1,j=0;i<n;i++){ let b=n>>1; for(;j&b;b>>=1) j^=b; j^=b; if(i<j){ let t=re[i];re[i]=re[j];re[j]=t; t=im[i];im[i]=im[j];im[j]=t; } }
  for(let len=2;len<=n;len<<=1){ const ang=-2*Math.PI/len, wr=Math.cos(ang), wi=Math.sin(ang); for(let i=0;i<n;i+=len){ let cr=1,ci=0; for(let k=0;k<len/2;k++){ const a=i+k,b=a+len/2, xr=re[b]*cr-im[b]*ci, xi=re[b]*ci+im[b]*cr; re[b]=re[a]-xr; im[b]=im[a]-xi; re[a]+=xr; im[a]+=xi; const t=cr*wr-ci*wi; ci=cr*wi+ci*wr; cr=t; } } } }
function recta(x,y){ const n=x.length; let sx=0,sy=0,sxx=0,sxy=0,syy=0; for(let i=0;i<n;i++){ sx+=x[i]; sy+=y[i]; sxx+=x[i]*x[i]; sxy+=x[i]*y[i]; syy+=y[i]*y[i]; } const d=n*sxx-sx*sx, m=(n*sxy-sx*sy)/d, b=(sy-m*sx)/n, r=(n*sxy-sx*sy)/Math.sqrt(d*(n*syy-sy*sy)); return {m,b,r2:r*r}; }
function leerCSV(txt){
  const filas=txt.split(/\r?\n/).filter(l=>l.trim()); if(filas.length<32) throw new Error('archivo demasiado corto');
  const sep=[';','\t',','].find(s=>filas[1].split(s).length>1)||','; const num=v=>parseFloat(String(v).replace(/"/g,'').replace(sep===';'?',':'\u0000','.'));
  const cab=filas[0].split(sep).map(h=>h.replace(/"/g,'').trim()), esCab=isNaN(num(filas[0].split(sep)[0])); const datos=(esCab?filas.slice(1):filas).map(l=>l.split(sep).map(num)).filter(f=>f.every(v=>isFinite(v)));
  if(!datos.length||datos[0].length<2||datos.length<32) throw new Error('se esperan al menos dos columnas numéricas');
  const nc=datos[0].length, t=datos.map(f=>f[0]), dur=t[t.length-1]-t[0]; if(!(dur>0)) throw new Error('la primera columna no es un tiempo creciente');
  const cols=[]; for(let j=1;j<nc;j++) cols.push(datos.map(f=>f[j]));
  return {t,cols,nombres:(esCab?cab.slice(1):cols.map((_,j)=>'columna '+(j+2))),sel:Math.min(2,cols.length-1)};
}
// remuestreo uniforme por interpolación lineal
function uniforme(t,x){ const N=t.length, fs=(N-1)/(t[N-1]-t[0]), o=new Float64Array(N); let j=0; for(let n=0;n<N;n++){ const tt=t[0]+n/fs; while(j<N-2&&t[j+1]<tt) j++; const u=(tt-t[j])/(t[j+1]-t[j]); o[n]=x[j]+(x[j+1]-x[j])*Math.min(1,Math.max(0,u)); } return {x:o,fs}; }
function senal(){
  if(S.origen==='csv'&&CSV) return uniforme(CSV.t,CSV.cols[CSV.sel]);
  if(S.origen==='sint'){ const fs=S.fs, N=Math.round(12*fs), x=new Float64Array(N), u=rng(20261117), wd=TP*S.fn*Math.sqrt(1-S.ze*S.ze), sg=TP*S.ze*S.fn, n0=Math.round(3*fs);
    for(let n=0;n<N;n++){ const g=Math.sqrt(-2*Math.log(1-u()))*Math.cos(TP*u()); x[n]=S.ru/100*g+(n>=n0?Math.exp(-sg*(n-n0)/fs)*Math.cos(wd*(n-n0)/fs):0); } return {x,fs}; }
  return {x:Float64Array.from(EJ.z),fs:1/EJ.dt};
}
function analizar(){
  const s=senal(), fs=s.fs, N=s.x.length, x=new Float64Array(N); let m=0; for(const v of s.x) m+=v; m/=N; for(let n=0;n<N;n++) x[n]=s.x[n]-m;
  let n0=0; for(let n=1;n<N;n++) if(Math.abs(x[n])>Math.abs(x[n0])) n0=n;                       // golpe
  // espectro del tramo posterior al golpe (relleno con ceros hasta potencia de 2)
  const L=N-n0; let M2=1; while(M2<4*L) M2<<=1; const re=new Float64Array(M2), im=new Float64Array(M2);
  for(let n=0;n<L;n++) re[n]=x[n0+n]*(0.5+0.5*Math.cos(Math.PI*n/L)); fft2(re,im);   // media ventana de Hann decreciente: no borra el inicio del transitorio
  const df=fs/M2, K=M2/2, mag=new Float64Array(K); let kp=Math.ceil(2/df); for(let k=0;k<K;k++){ mag[k]=Math.hypot(re[k],im[k]); if(k*df>=2&&mag[k]>mag[kp]) kp=k; }
  let fp=kp*df; if(kp>0&&kp<K-1){ const y0=Math.log(mag[kp-1]), y1=Math.log(mag[kp]), y2=Math.log(mag[kp+1]); fp=(kp+0.5*(y0-y2)/(y0-2*y1+y2))*df; }
  // señal analítica filtrada: pasabanda ideal fp(1 ± bw) sobre todo el registro
  let M=1; while(M<N) M<<=1; const ar=new Float64Array(M), ai=new Float64Array(M); for(let n=0;n<N;n++) ar[n]=x[n]; fft2(ar,ai);
  const fa=fp*(1-S.bw/100), fb=fp*(1+S.bw/100); for(let k=0;k<M;k++){ const f=k*fs/M; if(k<=M/2&&f>=fa&&f<=fb){ ar[k]*=2; ai[k]*=2; } else { ar[k]=0; ai[k]=0; } }
  for(let k=0;k<M;k++) ai[k]=-ai[k]; fft2(ar,ai); const xf=new Float64Array(N), A=new Float64Array(N); for(let n=0;n<N;n++){ xf[n]=ar[n]/M; const q=-ai[n]/M; A[n]=Math.hypot(xf[n],q); }
  // tramo de ajuste: desde el golpe + ti hasta que la envolvente cae a um % de su valor inicial
  const i0=Math.min(N-8,n0+Math.round(S.ti*fs)); let i1=i0; const lim=A[i0]*S.um/100; while(i1<N-1&&A[i1]>lim) i1++;
  const tt=[], la=[]; for(let n=i0;n<i1;n++){ tt.push((n-i0)/fs); la.push(Math.log(A[n])); }
  const aj=tt.length>=8?recta(tt,la):{m:NaN,b:NaN,r2:NaN}, sigma=-aj.m, zenv=sigma/(TP*fp);
  // decremento: máximos positivos de la señal filtrada con interpolación parabólica
  const pk=[]; for(let n=Math.max(1,i0);n<Math.min(N-1,i1);n++){ if(xf[n]>0&&xf[n]>=xf[n-1]&&xf[n]>xf[n+1]){ const d=0.5*(xf[n-1]-xf[n+1])/(xf[n-1]-2*xf[n]+xf[n+1]); pk.push([(n+d)/fs, xf[n]-0.25*(xf[n-1]-xf[n+1])*d]); } }
  let zdec=NaN, fd=NaN, delta=NaN; if(pk.length>=4){ const r=recta(pk.map((_,j)=>j),pk.map(p=>Math.log(p[1]))); delta=-r.m; zdec=delta/Math.sqrt(4*Math.PI*Math.PI+delta*delta); fd=(pk.length-1)/(pk[pk.length-1][0]-pk[0][0]); }
  R={x,xf,A,fs,N,n0,i0,i1,fp,df,mag,K,aj,sigma,zenv,zdec,fd,delta,pk,tt,la,fa,fb,ciclos:pk.length-1}; return R;
}
function dibujar(){
  const ejem=S.origen==='ej'||(S.origen==='csv'&&!CSV), r=analizar(), t0=r.n0/r.fs, tA=Math.max(0,t0-0.3), tB=Math.min(r.N/r.fs,(r.i1/r.fs)+0.8); let am=0; for(let n=0;n<r.N;n++) am=Math.max(am,Math.abs(r.x[n])); am*=1.08;
  let g=lienzo($('c1'),260), e=ejes(g,{},{x0:tA,x1:tB,y0:-am,y1:am,xl:'t (s)',yl:'a (m/s^2)',tit:(ejem?'Registro de ejemplo':S.origen==='csv'?'Archivo propio':'Señal sintética')+': señal, envolvente y tramo ajustado',ny:4}), c=g.c;
  c.fillStyle='rgba(197,90,17,.09)'; c.fillRect(e.X(r.i0/r.fs),e.py,e.X(r.i1/r.fs)-e.X(r.i0/r.fs),e.h);
  const a=Math.floor(tA*r.fs), b=Math.min(r.N-1,Math.ceil(tB*r.fs)), p0=[],p1=[],p2=[],p3=[]; for(let n=a;n<=b;n++){ const t=n/r.fs; p0.push([t,r.x[n]]); p1.push([t,r.xf[n]]); if(n>=r.n0){ p2.push([t,r.A[n]]); p3.push([t,-r.A[n]]); } }
  curva(e,p0,'#B9BEC8',1); curva(e,p1,STEEL,1.2); curva(e,p2,ORANGE,1.8); curva(e,p3,ORANGE,1.8);
  if(isFinite(r.sigma)){ const A0=Math.exp(r.aj.b); curva(e,[...Array(60)].map((_,i)=>{ const t=r.i0/r.fs+i/59*(r.i1-r.i0)/r.fs; return [t,A0*Math.exp(-r.sigma*(t-r.i0/r.fs))]; }),RED,1.6,[6,4]); }
  r.pk.forEach(p=>{ c.fillStyle=GREEN; c.beginPath(); c.arc(e.X(p[0]),e.Y(p[1]),2.4,0,7); c.fill(); });
  // espectro (izquierda) y ln A (derecha); en pantallas angostas, uno debajo del otro
  const ang=($('c2').clientWidth||760)<560, H2=ang?520:300; g=lienzo($('c2'),H2); c=g.c; const bx1=ang?{x:0,w:g.W,y:0,h:260}:{x:0,w:g.W/2,h:H2}, bx2=ang?{x:0,w:g.W,y:260,h:260}:{x:g.W/2,w:g.W/2,h:H2};
  let mx=0; for(let k=1;k<r.K;k++) mx=Math.max(mx,r.mag[k]);
  e=ejes(g,bx1,{x0:0,x1:r.fs/2,y0:mx*1e-4,y1:mx*2,logy:true,xl:'f (Hz)',yl:'|X| (relativa)',tit:'Espectro tras el golpe',nx:5});
  c.fillStyle='rgba(68,114,196,.10)'; c.fillRect(e.X(r.fa),e.py,e.X(Math.min(r.fs/2,r.fb))-e.X(r.fa),e.h);
  const ps=[], st=Math.max(1,Math.floor(r.K/1500)); for(let k=1;k<r.K;k+=st){ let v=0; for(let j=k;j<Math.min(r.K,k+st);j++) v=Math.max(v,r.mag[j]); ps.push([k*r.df,v]); } curva(e,ps,STEEL,1.3);
  vline(e,r.fp,RED,[5,4],'f_n = '+r.fp.toFixed(2)+' Hz'); vline(e,0.8*r.fs/2,GREY,[2,3],'0.8 f_s/2',16);
  if(r.tt.length>=8){ const y0=Math.min(...r.la), y1=Math.max(...r.la), pd=(y1-y0)*0.12+1e-6; e=ejes(g,bx2,{x0:0,x1:r.tt[r.tt.length-1],y0:y0-pd,y1:y1+pd,xl:'t desde el inicio del ajuste (s)',yl:'ln A  (A en m/s^2)',tit:'ln A(t) y recta ajustada',nx:5,ny:5});
    curva(e,r.tt.map((t,i)=>[t,r.la[i]]),ORANGE,1.8); funcion(e,t=>r.aj.b+r.aj.m*t,RED,1.5,[6,4]); }
  const f=(v,n)=>isFinite(v)?v.toFixed(n):'…';
  $('ofs').textContent=f(r.fs,1)+' Hz'; $('ony').textContent=f(r.fs/2,1)+' Hz'; $('ofp').textContent=f(r.fp,2)+' Hz'; $('ofd').textContent=f(r.fd,2)+' Hz';
  $('oze').textContent=f(r.zenv,4); $('ozd').textContent=f(r.zdec,4); $('osg').textContent=f(r.sigma,3)+' 1/s'; $('or2').textContent=f(r.aj.r2,3)+' · '+Math.max(0,r.ciclos)+' ciclos';
  const av=[];
  if(S.origen==='csv'&&!CSV) av.push('Todavía no hay un archivo cargado: se muestra el registro de ejemplo.');
  if(S.origen==='csv'&&CSV&&/abs/i.test(CSV.nombres[CSV.sel])) av.push('Se eligió la aceleración absoluta: el valor absoluto rectifica la señal y la frecuencia aparece duplicada. Elegir un eje (x, y o z).');
  if(isFinite(r.sigma)&&r.fp*S.bw/100<4*r.sigma/TP) av.push('El filtro es estrecho frente al ancho del pico (2ζ f_n ≈ '+(r.sigma/Math.PI).toFixed(2)+' Hz): ensanchar el semiancho del filtro, porque de lo contrario el amortiguamiento resulta sobrestimado.');
  if(r.fp>0.8*r.fs/2) av.push('El pico está por encima de 0.8 f_s/2: puede ser un alias de una frecuencia mayor. Conviene alargar la viga y repetir.');
  if(S.origen==='sint'&&S.fn>S.fs/2) av.push('La frecuencia verdadera ('+S.fn+' Hz) supera Nyquist: el pico en '+r.fp.toFixed(1)+' Hz es un alias, f_a = |f − k f_s|; el amortiguamiento calculado con esa frecuencia tampoco es válido.');
  if(r.ciclos<20) av.push('El tramo ajustado tiene menos de 20 ciclos: bajar el umbral de fin o revisar el registro.');
  if(r.aj.r2<0.97) av.push('R^2 menor que 0.97: la envolvente no es una exponencial limpia (ruido, golpe dentro del tramo o amortiguamiento que depende de la amplitud).');
  if(isFinite(r.zenv)&&isFinite(r.zdec)&&Math.abs(r.zenv-r.zdec)/r.zenv>0.3) av.push('Los dos métodos difieren más de 30 %.');
  $('aviso').textContent=av.join(' ')||((ejem?'Registro de ejemplo: ':'')+'cumple los criterios de la lista de verificación (pico bajo 0.8 f_s/2, al menos 20 ciclos, R^2 ≥ 0.97, métodos a menos de 30 %).');
}
liga(S,UN,dibujar);
function modo(){ $('gcsv').style.display=S.origen==='csv'?'':'none'; $('gsint').style.display=S.origen==='sint'?'':'none'; }
$('origen').addEventListener('change',ev=>{ S.origen=ev.target.value; modo(); dibujar(); });
$('csv').addEventListener('change',ev=>{ const fl=ev.target.files[0]; if(!fl) return; const rd=new FileReader();
  rd.onload=()=>{ try{ CSV=leerCSV(rd.result); $('col').innerHTML=''; CSV.nombres.forEach((n,i)=>{ const o=document.createElement('option'); o.value=i; o.textContent=n; o.selected=i===CSV.sel; $('col').appendChild(o); });
      $('csvinfo').textContent='Archivo leído: '+CSV.t.length.toLocaleString('es-MX')+' muestras en '+(CSV.t[CSV.t.length-1]-CSV.t[0]).toFixed(1)+' s. Elegir la columna del eje perpendicular a la viga.'; }
    catch(err){ CSV=null; $('col').innerHTML=''; $('csvinfo').textContent='No se pudo leer el archivo: '+err.message+'. Se muestra el registro de ejemplo.'; } dibujar(); }; rd.readAsText(fl); });
$('col').addEventListener('change',ev=>{ if(CSV){ CSV.sel=+ev.target.value; dibujar(); } });
// pestañas Colab / VS Code
function tab(c){ $('panC').style.display=c?'':'none'; $('panV').style.display=c?'none':''; $('tabC').classList.toggle('on',c); $('tabV').classList.toggle('on',!c); }
$('tabC').onclick=()=>tab(true); $('tabV').onclick=()=>tab(false);
// avance del tutorial (se conserva en este navegador si el almacenamiento está disponible)
const CL='vib-tutorial-phyphox'; let hechos={}; try{ hechos=JSON.parse(localStorage.getItem(CL)||'{}')||{}; }catch(err){ hechos={}; }
const secs=[...document.querySelectorAll('.paso')];
$('indice').innerHTML=secs.map((p,i)=>'<a href="#paso'+(i+1)+'" data-i="'+(i+1)+'"></a>').join(''); [...$('indice').children].forEach((a,i)=>a.textContent=(i+1)+' · '+secs[i].querySelector('h2').childNodes[1].textContent.trim());
function avance(){ let n=0; secs.forEach((p,i)=>{ const ok=!!hechos[i+1]; n+=ok; p.classList.toggle('ok',ok); p.querySelector('input[data-paso]').checked=ok; $('indice').children[i].classList.toggle('ok',ok); }); $('barra').style.width=(100*n/secs.length)+'%'; }
document.querySelectorAll('input[data-paso]').forEach(ch=>ch.addEventListener('change',()=>{ hechos[ch.dataset.paso]=ch.checked; try{ localStorage.setItem(CL,JSON.stringify(hechos)); }catch(err){} avance(); }));
window.addEventListener('resize',dibujar);
window.__tut={S,analizar,leerCSV,res:()=>R};
modo(); avance(); dibujar();
""".replace("__EJ__", EJ)
EXTRA = EXTRA + EXTRA_T
import base_pag; base_pag.EXTRA = EXTRA
pagina("tutorial_phyphox.html", "Tutorial: medir con Phyphox y analizar en Python", "Vibraciones · Tutorial · U7",
       "Del teléfono a la frecuencia natural y al amortiguamiento en siete pasos: instalar Phyphox, medir un decaimiento libre, exportar, abrir el cuaderno en Colab o en Visual Studio Code y comprobar el resultado",
       cuerpo, script, "Tutorial interactivo de medición con el teléfono y tratamiento de datos en Python · material de apoyo del curso de Vibraciones · el analizador funciona sin conexión.")
