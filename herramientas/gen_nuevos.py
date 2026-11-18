#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera los exploradores nuevos de noviembre de 2026:
  senales_interactivo.html  · Pilar 11 · Laboratorio de señales (U7, temas 7.1 y 7.2)
  dosgdl_interactivo.html   · Pilar 12 · Dos grados de libertad y absorbedor (U8)
Toman la hoja de estilo, el tema, el pie y el contador de un explorador existente (mediapotencia), de modo que
el aspecto es idéntico. Uso: python3 gen_nuevos.py CARPETA   (después: mejoras.py e integra.py)"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mml import M
D = sys.argv[1]
I = lambda t: M(t, inline=True)
base = open(os.path.join(D, "mediapotencia_interactivo.html"), encoding="utf-8").read()
CSS = re.search(r"<style>.*?</style>", base, re.S).group(0)
TEMA = re.search(r"<!-- tema:inicio -->.*?<!-- tema:fin -->", base, re.S).group(0)
CONT = re.search(r"<!-- contador:inicio -->.*?<!-- contador:fin -->", base, re.S).group(0)
PIE = re.search(r"<footer>.*?</footer>", base, re.S).group(0)
EXTRA = """<style>
  .grp{border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin-bottom:10px}
  .grp .t{font-size:11.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--orange);margin-bottom:6px}
  .nota{font-size:12px;color:var(--grey);margin:6px 0 0}
  select,.archivo{font:inherit;font-size:13px;border:1px solid var(--line);border-radius:8px;padding:5px 8px;background:#fff}
  .tiles.t3{grid-template-columns:1fr 1fr 1fr} @media(max-width:520px){.tiles.t3{grid-template-columns:1fr 1fr}}
  .tile .v{font-size:18px} .tile.al .v{color:var(--red)}
  .two{display:grid;grid-template-columns:1fr;gap:12px} @media(min-width:900px){.two{grid-template-columns:1fr 1fr}}
  .eqbox{overflow-x:auto} .two>div{min-width:0}
  table.tb{border-collapse:collapse;font-size:13px;width:100%} table.tb td,table.tb th{border-bottom:1px solid var(--line);padding:5px 8px;text-align:left} table.tb th{color:var(--navy)}
</style>"""

def pagina(archivo, titulo, hk, lede, cuerpo, script, pie1):
    pie = re.sub(r'<div style="margin-bottom:8px">.*?</div>', '<div style="margin-bottom:8px">%s</div>' % pie1, PIE, count=1, flags=re.S)
    s = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="author" content="Elodie Strupiechonski; Andrés de Luna Bugallo">
<title>{titulo} · Explorador · Vibraciones · ENES Juriquilla</title>
{CSS}
{EXTRA}
{TEMA}
</head>
<body>
<header>
  <div class="in">
    <h1>{titulo}</h1>
    <p><span class="hk">{hk}</span>{lede}</p>
  </div>
</header>

<div class="wrap">
{cuerpo}
</div>

{pie}

<script>
"use strict";
{script}
</script>
{CONT}
</body>
</html>
"""
    open(os.path.join(D, archivo), "w", encoding="utf-8").write(s); print("generado", archivo, len(s))

def fila(lab, i, mn, mx, st, v, u=""):
    return f'<div class="row"><label>{lab}</label><input id="{i}" type="range" min="{mn}" max="{mx}" step="{st}" value="{v}"><span class="val" id="v{i}">{v}{(" " + u) if u else ""}</span></div>'
def tile(k, i, cls=""):
    return f'<div class="tile {cls}"><div class="k">{k}</div><div class="v" id="{i}">…</div></div>'
def eq(lab, cuerpo, st=""): return f'<div class="eqbox" style="margin-top:10px;{st}"><span class="lab">{lab}</span>{cuerpo}</div>'
def nota(t): return '<div class="eqnote">%s</div>' % t

# =====================================================================================================================
# PILAR 11 · LABORATORIO DE SEÑALES
# =====================================================================================================================
cuerpo = f"""
  <div class="intro full">
    <b>¿Qué muestra?</b> Una señal de aceleración (sintética o medida con el teléfono) se muestrea a <i>f</i><sub>s</sub>, se corta en segmentos de duración <i>T</i><sub>seg</sub>, se multiplica por una ventana y se promedia: es el <b>método de Welch</b> para estimar la densidad espectral de potencia (PSD). Arriba, la señal en el tiempo con sus muestras; abajo, la PSD estimada. Las líneas verticales marcan dónde está cada componente <b>real</b> y dónde <b>aparece</b> en el espectro: si no coinciden, hay <b>aliasing</b>.
  </div>

  <div class="card">
    <canvas id="ct" width="760" height="230" aria-label="Señal en el tiempo con las muestras"></canvas>
    <canvas id="cp" width="760" height="360" style="margin-top:10px" aria-label="Densidad espectral de potencia estimada"></canvas>
    <div class="legend">
      <span><i class="sw" style="border-top-color:var(--steel)"></i> PSD estimada <i>G</i>(<i>f</i>)</span>
      <span><i class="sw" style="border-top-color:var(--green);border-top-style:dashed"></i> componente real</span>
      <span><i class="sw" style="border-top-color:var(--red);border-top-style:dashed"></i> alias (componente plegada)</span>
      <span><i class="sw" style="border-top-color:var(--grey);border-top-style:dotted"></i> <i>f</i><sub>s</sub>/2 (Nyquist)</span>
      <span><i class="sw" style="border-top-color:var(--orange)"></i> piso de ruido teórico</span>
    </div>
  </div>

  <div class="card">
    <h2>Controles</h2>
    <div class="grp"><div class="t">Señal</div>
      <div class="row"><label>Origen</label><select id="origen"><option value="sint">Sintética: dos tonos y ruido</option><option value="csv">Archivo CSV de Phyphox</option></select></div>
      <div id="gsint">
      {fila("Tono 1: <i>f</i><sub>1</sub>", "f1", 1, 400, 1, 30, "Hz")}
      {fila("Tono 1: amplitud", "a1", 0, 5, 0.05, 1, "g")}
      {fila("Tono 2: <i>f</i><sub>2</sub>", "f2", 1, 400, 1, 170, "Hz")}
      {fila("Tono 2: amplitud", "a2", 0, 5, 0.05, 0.5, "g")}
      {fila("Ruido blanco (rms)", "sr", 0, 2, 0.01, 0.2, "g")}
      </div>
      <div id="gcsv" style="display:none">
        <input class="archivo" type="file" id="csv" accept=".csv,.txt,text/csv">
        <div class="row" style="margin-top:8px"><label>Columna</label><select id="col"></select></div>
        <div class="nota" id="csvinfo">Phyphox, «Aceleración (sin g)», exportar como CSV. La primera columna debe ser el tiempo en segundos; el archivo no sale del dispositivo.</div>
      </div>
    </div>
    <div class="grp"><div class="t">Adquisición y análisis</div>
      <div id="gadq">
      {fila("Muestreo <i>f</i><sub>s</sub>", "fs", 20, 1000, 10, 200, "Hz")}
      {fila("Duración total <i>T</i>", "T", 2, 600, 1, 20, "s")}
      </div>
      {fila("Segmento <i>T</i><sub>seg</sub>", "ts", 0.5, 20, 0.5, 4, "s")}
      <div class="btns">
        <button class="btn on" id="wH">Ventana de Hann</button><button class="btn" id="wR">Rectangular</button>
        <button class="btn on" id="yL">Eje logarítmico</button><button class="btn" id="yN">Eje lineal</button>
      </div>
      <div class="btns" style="margin-top:8px">
        <button class="btn" data-pre="A">Equipo A: alias sobre el motor</button>
        <button class="btn" data-pre="F">Fuga: 10.3 Hz con 2 s</button>
        <button class="btn" data-pre="W">Welch: 100 promedios</button>
      </div>
    </div>
    <div class="tiles t3">
      {tile("Muestras <i>N</i>", "oN")}{tile("Nyquist <i>f</i><sub>s</sub>/2", "oNy")}{tile("Resolución Δ<i>f</i> = 1/<i>T</i><sub>seg</sub>", "oDf")}
      {tile("Promedios <i>n</i><sub>d</sub>", "oNd", "hl")}{tile("Error aleatorio ε<sub>r</sub>", "oEr", "hl")}{tile("Ancho equivalente <i>B</i><sub>e</sub>", "oBe")}
      {tile("Tono 1 aparece en", "oA1")}{tile("Tono 2 aparece en", "oA2")}{tile("Amplitud leída del pico mayor", "oPk")}
      {tile("rms en el tiempo", "oRt")}{tile("<i>G</i><sub>rms</sub> = √(área de la PSD)", "oRp")}{tile("rms de la señal continua", "oR0")}
    </div>
  </div>

  <div class="card full">
    <h2>Las fórmulas en pantalla</h2>
    <div class="two"><div>
    {eq("1 · Muestreo y aliasing", M(r"f_{\mathrm{Nyq}}=\frac{f_s}{2},\qquad f_a=|f-k\,f_s|") + nota("con <i>k</i> el entero que deja <i>f</i><sub>a</sub> dentro de [0, <i>f</i><sub>s</sub>/2]"))}
    {eq("2 · Resolución y promedios (Welch, sin traslape)", M(r"\Delta f=\frac{1}{T_{\mathrm{seg}}},\qquad n_d=\left\lfloor\frac{T}{T_{\mathrm{seg}}}\right\rfloor,\qquad \varepsilon_r\approx\frac{1}{\sqrt{n_d}}"))}
    {eq("3 · PSD unilateral de un segmento con ventana <i>w</i>", M(r"G(f_k)=\frac{2\,|X_k|^2}{f_s\sum_n w_n^2},\qquad X_k=\sum_{n=0}^{N-1}w_n\,x_n\,e^{-i2\pi kn/N}") + nota("el factor 2 no se aplica en <i>f</i> = 0 ni en <i>f</i><sub>s</sub>/2"))}
    </div><div>
    {eq("4 · Valor eficaz: el área bajo la PSD (Parseval)", M(r"G_{\mathrm{rms}}=\sqrt{\sum_k G(f_k)\,\Delta f}\ \approx\ \sqrt{\frac{A_1^2}{2}+\frac{A_2^2}{2}+\sigma_r^2}"))}
    {eq("5 · Piso de ruido blanco de valor eficaz σ<sub>r</sub>", M(r"G_{\mathrm{ruido}}=\frac{\sigma_r^2}{f_s/2}=\frac{2\,\sigma_r^2}{f_s}"))}
    {eq("6 · Fuga: lectura de un tono a δ barras de la más cercana", M(r"\text{rectangular: }\left|\frac{\mathrm{sen}\,\pi\delta}{\pi\delta}\right|\qquad\text{Hann: }\left|\frac{\mathrm{sen}\,\pi\delta}{\pi\delta}\right|\frac{1}{1-\delta^2}") + nota("ancho equivalente de ruido: <i>B</i><sub>e</sub> = Δ<i>f</i> (rectangular), 1.5 Δ<i>f</i> (Hann)"))}
    </div></div>
    <div class="intro" style="margin-top:12px"><b>Lectura para los proyectos.</b> La resolución depende solo de la duración del segmento, no de <i>f</i><sub>s</sub>; y para una duración total fija, ganar resolución cuesta precisión, porque {I(r"\varepsilon_r\approx 1/\sqrt{B_e\,T}")}. Un pico de resonancia de ancho {I(r"2\zeta f_n")} necesita al menos cuatro barras dentro de ese ancho: {I(r"T_{\mathrm{seg}}\geq 2/(\zeta f_n)")}. El teléfono no tiene filtro antialias accesible: toda componente por encima de <i>f</i><sub>s</sub>/2 se pliega hacia la banda útil.</div>
    <div class="takeaway" style="margin-top:10px"><b>Cómo explorar:</b> (1) con el preajuste del equipo A, el tono de 170 Hz muestreado a 200 Hz cae exactamente sobre la línea del motor en 30 Hz; al subir <i>f</i><sub>s</sub> a 400 Hz se separan. (2) Con el preajuste de fuga, un tono de 10.3 Hz y segmentos de 2 s se lee con 0.757 de su amplitud con ventana rectangular y con 0.901 con Hann; con segmentos de 10 s cae justo en una barra. (3) Con el preajuste de Welch, la curva se suaviza: ε<sub>r</sub> = 10 %. En todos los casos <i>G</i><sub>rms</sub> coincide con el rms medido en el tiempo (Parseval). En cambio, cuando un alias cae sobre otro tono, los dos se suman como fasores y el rms de la señal muestreada deja de coincidir con el de la señal continua: en el preajuste del equipo A, 0.632 g frente a 0.815 g. Referencias: Bendat y Piersol, <i>Random Data</i>, 4.ª ed., caps. 8 y 11; Welch (1967), doi:10.1109/TAU.1967.1161901; Harris (1978), doi:10.1109/PROC.1978.10837.</div>
  </div>
"""
script = r"""
const NAVY='#1F3864',STEEL='#4472C4',ORANGE='#C55A11',GREEN='#2E7D46',GREY='#5B5B5B',RED='#B23A3A';
const $=id=>document.getElementById(id);
let S={f1:30,a1:1,f2:170,a2:0.5,sr:0.2,fs:200,T:20,ts:4,hann:true,logy:true,origen:'sint'}, CSV=null, R=null;
// --- generador reproducible (mulberry32) y normal estándar (Box–Muller)
function rng(seed){ let a=seed>>>0; return function(){ a|=0; a=a+0x6D2B79F5|0; let t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }
function normales(n,seed){ const u=rng(seed), o=new Float64Array(n); for(let i=0;i<n;i+=2){ const r=Math.sqrt(-2*Math.log(1-u())), th=2*Math.PI*u(); o[i]=r*Math.cos(th); if(i+1<n) o[i+1]=r*Math.sin(th); } return o; }
// --- FFT: base 2 y Bluestein para longitudes arbitrarias
function fft2(re,im){ const n=re.length; for(let i=1,j=0;i<n;i++){ let b=n>>1; for(;j&b;b>>=1) j^=b; j^=b; if(i<j){ let t=re[i];re[i]=re[j];re[j]=t; t=im[i];im[i]=im[j];im[j]=t; } }
  for(let len=2;len<=n;len<<=1){ const ang=-2*Math.PI/len, wr=Math.cos(ang), wi=Math.sin(ang); for(let i=0;i<n;i+=len){ let cr=1,ci=0; for(let k=0;k<len/2;k++){ const a=i+k,b=a+len/2, xr=re[b]*cr-im[b]*ci, xi=re[b]*ci+im[b]*cr; re[b]=re[a]-xr; im[b]=im[a]-xi; re[a]+=xr; im[a]+=xi; const t=cr*wr-ci*wi; ci=cr*wi+ci*wr; cr=t; } } } }
function fft(x){ const n=x.length; if((n&(n-1))===0){ const re=Float64Array.from(x), im=new Float64Array(n); fft2(re,im); return [re,im]; }
  let m=1; while(m<2*n-1) m<<=1; const ar=new Float64Array(m), ai=new Float64Array(m), br=new Float64Array(m), bi=new Float64Array(m), cr=new Float64Array(n), ci=new Float64Array(n);
  for(let k=0;k<n;k++){ const ph=Math.PI*((k*k)%(2*n))/n; cr[k]=Math.cos(ph); ci[k]=Math.sin(ph); ar[k]=x[k]*cr[k]; ai[k]=-x[k]*ci[k]; br[k]=cr[k]; bi[k]=ci[k]; if(k){ br[m-k]=cr[k]; bi[m-k]=ci[k]; } }
  fft2(ar,ai); fft2(br,bi); for(let k=0;k<m;k++){ const t=ar[k]*br[k]-ai[k]*bi[k]; ai[k]=-(ar[k]*bi[k]+ai[k]*br[k]); ar[k]=t; }
  fft2(ar,ai); const re=new Float64Array(n), im=new Float64Array(n); for(let k=0;k<n;k++){ const pr=ar[k]/m, pi=-ai[k]/m; re[k]=pr*cr[k]+pi*ci[k]; im[k]=pi*cr[k]-pr*ci[k]; } return [re,im]; }
function alias(f,fs){ const k=Math.round(f/fs); return Math.abs(f-k*fs); }
function senal(){
  if(S.origen==='csv'&&CSV){ const x=CSV.cols[CSV.sel]; let m=0; for(const v of x) m+=v; m/=x.length; return {x:Float64Array.from(x,v=>v-m), fs:CSV.fs, T:x.length/CSV.fs}; }
  const N=Math.max(8,Math.round(S.fs*S.T)), x=new Float64Array(N), z=normales(N,20261113);
  for(let n=0;n<N;n++){ const t=n/S.fs; x[n]=S.a1*Math.sin(2*Math.PI*S.f1*t)+S.a2*Math.sin(2*Math.PI*S.f2*t+1)+S.sr*z[n]; }
  return {x,fs:S.fs,T:N/S.fs};
}
function welch(x,fs,ts,hann){
  const N=x.length, L=Math.max(8,Math.min(N,Math.round(ts*fs))), nd=Math.max(1,Math.floor(N/L)), K=Math.floor(L/2)+1, G=new Float64Array(K), w=new Float64Array(L); let sw=0, s1=0;
  for(let n=0;n<L;n++){ w[n]=hann?0.5-0.5*Math.cos(2*Math.PI*n/L):1; sw+=w[n]*w[n]; s1+=w[n]; }
  const seg=new Float64Array(L);
  for(let d=0;d<nd;d++){ for(let n=0;n<L;n++) seg[n]=x[d*L+n]*w[n]; const [re,im]=fft(seg);
    for(let k=0;k<K;k++){ const p=(re[k]*re[k]+im[k]*im[k])/(fs*sw); G[k]+=((k===0||(L%2===0&&k===L/2))?1:2)*p/nd; } }
  return {G,df:fs/L,L,nd,sw,s1};
}
function calcular(){
  const s=senal(), W=welch(s.x,s.fs,S.ts,S.hann); let m2=0; for(const v of s.x) m2+=v*v; const rt=Math.sqrt(m2/s.x.length);
  let area=0, kp=1; for(let k=0;k<W.G.length;k++){ area+=W.G[k]*W.df; if(k>0&&W.G[k]>W.G[kp]) kp=k; }
  // amplitud leída del pico: A = sqrt(2·G·Δf·Be/Δf) con Be = fs·Σw²/(Σw)²
  const Be=s.fs*W.sw/(W.s1*W.s1), Apk=Math.sqrt(2*W.G[kp]*Be);
  R={s,W,rt,rp:Math.sqrt(area),kp,Apk,Be}; return R;
}
function ejes(c,cv,H){ const dpr=Math.min(window.devicePixelRatio||1,2), Wd=cv.clientWidth||760; cv.width=Wd*dpr; cv.height=H*dpr; cv.style.height=H+'px'; c.setTransform(dpr,0,0,dpr,0,0); c.clearRect(0,0,Wd,H); return Wd; }
function dibujar(){
  const r=R||calcular(), s=r.s, W=r.W, sint=S.origen==='sint'||!CSV;
  // ---------- tiempo
  let cv=$('ct'), c=cv.getContext('2d'), H=230, Wd=ejes(c,cv,H); const mL=52,mR=14,mT=22,mB=34, pw=Wd-mL-mR; let ph=H-mT-mB;
  const tv=Math.min(s.T, Math.max(0.25, Math.min(1, 6/Math.max(1,sint?Math.min(S.f1,S.f2):5)))), nv=Math.min(s.x.length,Math.round(tv*s.fs)); let am=1e-9; for(let n=0;n<nv;n++) am=Math.max(am,Math.abs(s.x[n]));
  if(sint) am=Math.max(am,S.a1+S.a2); am*=1.1;
  const X=t=>mL+t/tv*pw, Y=v=>mT+(1-(v+am)/(2*am))*ph;
  c.strokeStyle='#EDF1F8'; c.fillStyle=GREY; c.font='11px Arial'; c.textAlign='center'; c.textBaseline='top';
  for(let i=0;i<=5;i++){ const t=tv*i/5; c.beginPath(); c.moveTo(X(t),mT); c.lineTo(X(t),mT+ph); c.stroke(); c.fillText(t.toFixed(2),X(t),mT+ph+5); }
  c.textAlign='right'; c.textBaseline='middle'; [-am/1.1,0,am/1.1].forEach(v=>{ c.beginPath(); c.moveTo(mL,Y(v)); c.lineTo(mL+pw,Y(v)); c.stroke(); c.fillText(v.toFixed(2),mL-6,Y(v)); });
  c.fillStyle=NAVY; c.font='bold 12px Arial'; c.textAlign='left'; c.textBaseline='top'; c.fillText('Señal en el tiempo: primeros '+tv.toFixed(2)+' s  ·  a(t) en g', mL, 4);
  c.textAlign='center'; c.fillText('t (s)', mL+pw/2, H-15);
  if(sint){ c.strokeStyle='rgba(91,91,91,.45)'; c.lineWidth=1; c.beginPath(); for(let px=0;px<=pw;px++){ const t=px/pw*tv, v=S.a1*Math.sin(2*Math.PI*S.f1*t)+S.a2*Math.sin(2*Math.PI*S.f2*t+1); px?c.lineTo(mL+px,Y(v)):c.moveTo(mL+px,Y(v)); } c.stroke(); }
  c.strokeStyle=STEEL; c.lineWidth=1.3; c.beginPath(); for(let n=0;n<nv;n++){ const x=X(n/s.fs), y=Y(s.x[n]); n?c.lineTo(x,y):c.moveTo(x,y); } c.stroke();
  if(nv<=260){ c.fillStyle=STEEL; for(let n=0;n<nv;n++){ c.beginPath(); c.arc(X(n/s.fs),Y(s.x[n]),2.2,0,7); c.fill(); } }
  // ---------- PSD
  cv=$('cp'); c=cv.getContext('2d'); H=360; Wd=ejes(c,cv,H); ph=H-mT-mB; const fN=s.fs/2, G=W.G, K=G.length;
  let gmax=1e-12, gmin=Infinity; for(let k=1;k<K;k++){ gmax=Math.max(gmax,G[k]); if(G[k]>0) gmin=Math.min(gmin,G[k]); }
  const piso=sint&&S.sr>0?2*S.sr*S.sr/s.fs:null; let y1,y0,Yp;
  if(S.logy){ y1=Math.ceil(Math.log10(gmax)+0.2); y0=Math.max(y1-8,Math.floor(Math.log10(Math.max(gmin,gmax*1e-8)))); Yp=g=>mT+(1-(Math.log10(Math.max(g,1e-300))-y0)/(y1-y0))*ph; }
  else { y1=gmax*1.12; y0=0; Yp=g=>mT+(1-g/y1)*ph; }
  const Xf=f=>mL+f/fN*pw;
  c.strokeStyle='#EDF1F8'; c.fillStyle=GREY; c.font='11px Arial'; c.textAlign='center'; c.textBaseline='top';
  const pasoF=[1,2,5,10,20,25,50,100,200].find(p=>fN/p<=10)||500; for(let f=0;f<=fN+1e-9;f+=pasoF){ c.beginPath(); c.moveTo(Xf(f),mT); c.lineTo(Xf(f),mT+ph); c.stroke(); c.fillText(String(+f.toFixed(2)),Xf(f),mT+ph+5); }
  c.textAlign='right'; c.textBaseline='middle';
  if(S.logy){ for(let e=y0;e<=y1;e++){ const y=mT+(1-(e-y0)/(y1-y0))*ph; c.beginPath(); c.moveTo(mL,y); c.lineTo(mL+pw,y); c.stroke(); c.fillText('10^'+(e<0?'−'+(-e):e),mL-6,y); } }
  else { for(let i=0;i<=4;i++){ const g=y1*i/4, y=Yp(g); c.beginPath(); c.moveTo(mL,y); c.lineTo(mL+pw,y); c.stroke(); c.fillText(g.toPrecision(2),mL-6,y); } }
  c.fillStyle=NAVY; c.font='bold 12px Arial'; c.textAlign='left'; c.textBaseline='top'; c.fillText('PSD estimada G(f) en g^2/Hz  ·  '+W.nd+' segmento'+(W.nd>1?'s':'')+' de '+(W.L/s.fs).toFixed(2)+' s  ·  ventana '+(S.hann?'de Hann':'rectangular'), mL, 4);
  c.textAlign='center'; c.fillText('f (Hz)', mL+pw/2, H-15);
  if(piso){ c.strokeStyle=ORANGE; c.lineWidth=1.2; c.beginPath(); c.moveTo(mL,Yp(piso)); c.lineTo(mL+pw,Yp(piso)); c.stroke(); }
  c.save(); c.beginPath(); c.rect(mL,mT,pw,ph); c.clip();
  c.strokeStyle=STEEL; c.lineWidth=1.6; c.beginPath(); for(let k=0;k<K;k++){ const x=Xf(k*W.df), y=Yp(G[k]); k?c.lineTo(x,y):c.moveTo(x,y); } c.stroke(); c.restore();
  if(sint){ [[S.f1,S.a1,'f_1'],[S.f2,S.a2,'f_2']].forEach(([f,a,n],i)=>{ if(a<=0) return; const fa=alias(f,s.fs), pleg=Math.abs(fa-f)>1e-9;
      c.strokeStyle=pleg?RED:GREEN; c.setLineDash([5,4]); c.lineWidth=1.3; c.beginPath(); c.moveTo(Xf(fa),mT); c.lineTo(Xf(fa),mT+ph); c.stroke(); c.setLineDash([]);
      c.fillStyle=pleg?RED:GREEN; c.font='bold 11px Arial'; c.textAlign=Xf(fa)>mL+pw-90?'right':'left'; c.textBaseline='top';
      c.fillText(n+(pleg?' = '+f+' Hz se ve en '+(+fa.toFixed(2))+' Hz':' = '+f+' Hz'), Xf(fa)+(Xf(fa)>mL+pw-90?-4:4), mT+18+16*i); }); }
  c.strokeStyle=GREY; c.setLineDash([2,3]); c.beginPath(); c.moveTo(Xf(fN),mT); c.lineTo(Xf(fN),mT+ph); c.stroke(); c.setLineDash([]);
  // ---------- lecturas
  const f3=v=>(+v).toFixed(3), eps=1/Math.sqrt(W.nd);
  $('oN').textContent=s.x.length.toLocaleString('es-MX'); $('oNy').textContent=(+fN.toFixed(2))+' Hz'; $('oDf').textContent=(+W.df.toFixed(4))+' Hz';
  $('oNd').textContent=W.nd; $('oEr').textContent=(100*eps).toFixed(1)+' %'; $('oBe').textContent=(+r.Be.toFixed(4))+' Hz';
  const ali=(f,a)=>{ if(!sint) return '…'; if(a<=0) return 'sin tono'; const fa=alias(f,s.fs); return (+fa.toFixed(2))+' Hz'+(Math.abs(fa-f)>1e-9?' (alias)':''); };
  $('oA1').textContent=ali(S.f1,S.a1); $('oA2').textContent=ali(S.f2,S.a2);
  $('oA1').parentNode.classList.toggle('al',sint&&S.a1>0&&alias(S.f1,s.fs)!==S.f1); $('oA2').parentNode.classList.toggle('al',sint&&S.a2>0&&alias(S.f2,s.fs)!==S.f2);
  $('oPk').textContent=f3(r.Apk)+' g en '+(+(r.kp*W.df).toFixed(2))+' Hz'; $('oRt').textContent=f3(r.rt)+' g'; $('oRp').textContent=f3(r.rp)+' g';
  $('oR0').textContent=sint?f3(Math.sqrt(S.a1*S.a1/2+S.a2*S.a2/2+S.sr*S.sr))+' g':'…';
}
function sync(){ R=null; calcular(); dibujar(); }
const UN={f1:' Hz',f2:' Hz',a1:' g',a2:' g',sr:' g',fs:' Hz',T:' s',ts:' s'};
Object.keys(UN).forEach(id=>$(id).addEventListener('input',e=>{ S[id]=+e.target.value; $('v'+id).textContent=(+S[id].toFixed(4))+UN[id]; sync(); }));
function pon(o){ Object.keys(o).forEach(k=>{ S[k]=o[k]; if($(k)){ $(k).value=o[k]; $('v'+k).textContent=o[k]+UN[k]; } }); botones(); sync(); }
function botones(){ $('wH').classList.toggle('on',S.hann); $('wR').classList.toggle('on',!S.hann); $('yL').classList.toggle('on',S.logy); $('yN').classList.toggle('on',!S.logy); }
$('wH').onclick=()=>{S.hann=true;botones();sync();}; $('wR').onclick=()=>{S.hann=false;botones();sync();};
$('yL').onclick=()=>{S.logy=true;botones();dibujar();}; $('yN').onclick=()=>{S.logy=false;botones();dibujar();};
const PRE={A:{f1:30,a1:1,f2:170,a2:0.5,sr:0.2,fs:200,T:20,ts:4,hann:true}, F:{f1:10.3,a1:1,f2:60,a2:0,sr:0,fs:200,T:20,ts:2,hann:false}, W:{f1:30,a1:0.3,f2:70,a2:0.1,sr:0.5,fs:200,T:400,ts:4,hann:true}};
document.querySelectorAll('[data-pre]').forEach(b=>b.addEventListener('click',()=>{ $('origen').value='sint'; S.origen='sint'; modo(); pon(PRE[b.dataset.pre]); }));
function modo(){ const c=S.origen==='csv'; $('gsint').style.display=c?'none':''; $('gcsv').style.display=c?'':'none'; $('gadq').style.display=c?'none':''; }
$('origen').addEventListener('change',e=>{ S.origen=e.target.value; modo(); sync(); });
function leerCSV(txt){
  const filas=txt.split(/\r?\n/).filter(l=>l.trim()); if(filas.length<16) throw new Error('archivo demasiado corto');
  const sep=[';','\t',','].find(s=>filas[1].split(s).length>1)||','; const num=v=>parseFloat(String(v).replace(/"/g,'').replace(sep===';'?',':'\u0000','.'));
  const cab=filas[0].split(sep).map(h=>h.replace(/"/g,'').trim()), esCab=isNaN(num(filas[0].split(sep)[0])); const datos=(esCab?filas.slice(1):filas).map(l=>l.split(sep).map(num)).filter(f=>f.every(v=>isFinite(v)));
  const nc=datos[0].length; if(nc<2||datos.length<16) throw new Error('se esperan al menos dos columnas numéricas');
  const t=datos.map(f=>f[0]), fs=(datos.length-1)/(t[t.length-1]-t[0]); if(!(fs>0)) throw new Error('la primera columna no es un tiempo creciente');
  const cols=[]; for(let j=1;j<nc;j++) cols.push(datos.map(f=>f[j]));
  return {fs,cols,nombres:(esCab?cab.slice(1):cols.map((_,j)=>'columna '+(j+2))),sel:Math.min(2,cols.length-1)};
}
$('csv').addEventListener('change',e=>{ const f=e.target.files[0]; if(!f) return; const rd=new FileReader();
  rd.onload=()=>{ try{ CSV=leerCSV(rd.result); $('col').innerHTML=CSV.nombres.map((n,i)=>'<option value="'+i+'"'+(i===CSV.sel?' selected':'')+'></option>').join(''); [...$('col').options].forEach((o,i)=>o.textContent=CSV.nombres[i]);
      $('csvinfo').textContent='Archivo leído: '+CSV.cols[0].length.toLocaleString('es-MX')+' muestras, f_s media = '+CSV.fs.toFixed(2)+' Hz, duración '+(CSV.cols[0].length/CSV.fs).toFixed(1)+' s. Se resta la media antes de analizar.'; sync(); }
    catch(err){ CSV=null; $('csvinfo').textContent='No se pudo leer el archivo: '+err.message+'.'; sync(); } }; rd.readAsText(f); });
$('col').addEventListener('change',e=>{ if(CSV){ CSV.sel=+e.target.value; sync(); } });
window.addEventListener('resize',dibujar);
window.__lab={S,calc:()=>R,leerCSV,alias,welch,fft};
sync();
"""
pagina("senales_interactivo.html", "Laboratorio de señales", "Vibraciones · Pilar 11 · U7",
       "Al variar la frecuencia de muestreo, la duración del segmento y la ventana se observa cómo cambian la densidad espectral estimada, el aliasing, la fuga y el error aleatorio",
       cuerpo, script, "Explorador didáctico de análisis de señales (muestreo, aliasing, ventanas y método de Welch) · material de apoyo del curso de Vibraciones · funciona sin conexión (un solo archivo).")

# =====================================================================================================================
# PILAR 12 · DOS GRADOS DE LIBERTAD Y ABSORBEDOR
# =====================================================================================================================
cuerpo = f"""
  <div class="intro full">
    <b>¿Qué muestra?</b> Una estructura principal (<i>m</i><sub>1</sub>, <i>k</i><sub>1</sub>, <i>c</i><sub>1</sub>) excitada por una fuerza armónica lleva encima un segundo sistema (<i>m</i><sub>2</sub>, <i>k</i><sub>2</sub>, <i>c</i><sub>2</sub>): un equipo montado sobre un soporte, o un <b>absorbedor dinámico</b>. Al acoplarlos, la resonancia única de la estructura se <b>divide en dos</b> frecuencias naturales, una por debajo y otra por encima de las originales. La curva compara la respuesta de <i>m</i><sub>1</sub> con y sin el segundo sistema; el diagrama inferior muestra las dos <b>formas modales</b> y el movimiento en la frecuencia de excitación elegida.
  </div>

  <div class="card">
    <canvas id="cf" width="760" height="380" aria-label="Respuesta en frecuencia de la masa principal con y sin el segundo sistema"></canvas>
    <div class="legend">
      <span><i class="sw" style="border-top-color:var(--steel)"></i> |<i>X</i><sub>1</sub>|/<i>X</i><sub>0</sub> con el segundo sistema</span>
      <span><i class="sw" style="border-top-color:var(--orange)"></i> |<i>X</i><sub>2</sub>|/<i>X</i><sub>0</sub></span>
      <span><i class="sw" style="border-top-color:var(--grey);border-top-style:dashed"></i> estructura sola (1 GDL)</span>
      <span><i class="sw" style="border-top-color:var(--green);border-top-style:dashed"></i> ω<sub>1</sub>, ω<sub>2</sub> (modos)</span>
      <span><i class="sw" style="border-top-color:var(--red)"></i> excitación ω</span>
    </div>
    <canvas id="cm" width="760" height="250" style="margin-top:10px" aria-label="Formas modales y movimiento forzado de las dos masas"></canvas>
  </div>

  <div class="card">
    <h2>Controles</h2>
    <div class="grp"><div class="t">Estructura principal</div>
      {fila("Masa <i>m</i><sub>1</sub>", "m1", 1, 100, 0.5, 10, "kg")}
      {fila("Rigidez <i>k</i><sub>1</sub>", "k1", 100, 50000, 100, 4000, "N/m")}
      {fila("Amortiguamiento ζ<sub>1</sub>", "z1", 0, 0.2, 0.005, 0.01)}
    </div>
    <div class="grp"><div class="t">Segundo sistema (equipo o absorbedor)</div>
      {fila("Razón de masas μ = <i>m</i><sub>2</sub>/<i>m</i><sub>1</sub>", "mu", 0.01, 1, 0.01, 0.1)}
      {fila("Sintonía β = ω<sub>a</sub>/ω<sub>n1</sub>", "be", 0.3, 2, 0.01, 1)}
      {fila("Amortiguamiento ζ<sub>2</sub>", "z2", 0, 0.5, 0.005, 0.02)}
      <div class="btns">
        <button class="btn" id="bDH">Óptimo de Den Hartog</button>
        <button class="btn" id="bT">Sintonía exacta (β = 1, ζ<sub>2</sub> = 0)</button>
        <button class="btn" id="bE">Equipo ligero mal sintonizado</button>
      </div>
    </div>
    <div class="grp"><div class="t">Excitación</div>
      {fila("Frecuencia <i>r</i> = ω/ω<sub>n1</sub>", "r", 0.3, 2, 0.005, 1)}
      <div class="btns"><button class="btn on" id="bAn">Animar</button><button class="btn" id="bM1">Ir al modo 1</button><button class="btn" id="bM2">Ir al modo 2</button></div>
    </div>
    <div class="tiles">
      {tile("ω<sub>n1</sub> = √(<i>k</i><sub>1</sub>/<i>m</i><sub>1</sub>) · <i>f</i><sub>n1</sub>", "oW")}{tile("<i>m</i><sub>2</sub> · <i>k</i><sub>2</sub>", "oMK")}
      {tile("Modo 1: ω<sub>1</sub> (y ω<sub>1</sub>/ω<sub>n1</sub>)", "oW1", "hl")}{tile("Modo 2: ω<sub>2</sub> (y ω<sub>2</sub>/ω<sub>n1</sub>)", "oW2", "hl")}
      {tile("Forma modal 1: <i>X</i><sub>2</sub>/<i>X</i><sub>1</sub>", "oU1")}{tile("Forma modal 2: <i>X</i><sub>2</sub>/<i>X</i><sub>1</sub>", "oU2")}
      {tile("|<i>X</i><sub>1</sub>|/<i>X</i><sub>0</sub> en la excitación", "oX1")}{tile("|<i>X</i><sub>2</sub>|/<i>X</i><sub>0</sub> en la excitación", "oX2")}
      {tile("Estructura sola en esa ω", "oXs")}{tile("Pico máximo de |<i>X</i><sub>1</sub>|/<i>X</i><sub>0</sub>", "oPk")}
    </div>
  </div>

  <div class="card full">
    <h2>Las fórmulas en pantalla</h2>
    <div class="two"><div>
    {eq("1 · Ecuaciones de movimiento (sin amortiguamiento)", M(r"\begin{bmatrix}m_1&0\\0&m_2\end{bmatrix}\begin{bmatrix}x_1''\\x_2''\end{bmatrix}+\begin{bmatrix}k_1+k_2&-k_2\\-k_2&k_2\end{bmatrix}\begin{bmatrix}x_1\\x_2\end{bmatrix}=\begin{bmatrix}F_0\cos\omega t\\0\end{bmatrix}"))}
    {eq("2 · Problema de valores propios: frecuencias naturales", M(r"\det\left(\mathbf{K}-\omega^2\mathbf{M}\right)=0") + M(r"m_1m_2\,\omega^4-\left[m_1k_2+m_2(k_1+k_2)\right]\omega^2+k_1k_2=0") + M(r"\left(\frac{\omega_{1,2}}{\omega_{n1}}\right)^2=\frac{1+\beta^2(1+\mu)\mp\sqrt{\left[1+\beta^2(1+\mu)\right]^2-4\beta^2}}{2}"))}
    {eq("3 · Formas modales", M(r"\left(\frac{X_2}{X_1}\right)_j=\frac{k_2}{k_2-m_2\,\omega_j^2}=\frac{\beta^2}{\beta^2-(\omega_j/\omega_{n1})^2}") + nota("modo 1: las masas se mueven en fase; modo 2: en oposición"))}
    </div><div>
    {eq("4 · Respuesta forzada con amortiguamiento", M(r"\begin{bmatrix}k_1+k_2-m_1\omega^2+i\omega(c_1+c_2)&-(k_2+i\omega c_2)\\-(k_2+i\omega c_2)&k_2-m_2\omega^2+i\omega c_2\end{bmatrix}\begin{bmatrix}X_1\\X_2\end{bmatrix}=\begin{bmatrix}F_0\\0\end{bmatrix}") + nota("<i>X</i><sub>0</sub> = <i>F</i><sub>0</sub>/<i>k</i><sub>1</sub> es la deflexión estática de la estructura"), "font-size:12.5px")}
    {eq("5 · Absorbedor sin amortiguamiento: antirresonancia", M(r"\omega=\omega_a=\sqrt{\frac{k_2}{m_2}}\ \Rightarrow\ X_1=0,\qquad X_2=-\frac{F_0}{k_2}"))}
    {eq("6 · Absorbedor amortiguado óptimo (Den Hartog)", M(r"\beta_{\mathrm{opt}}=\frac{1}{1+\mu},\qquad \zeta_{2,\mathrm{opt}}=\sqrt{\frac{3\mu}{8(1+\mu)^3}},\qquad \left(\frac{|X_1|}{X_0}\right)_{\text{máx}}\approx\sqrt{1+\frac{2}{\mu}}") + nota("válido para la estructura principal sin amortiguamiento"))}
    </div></div>
    <div class="intro" style="margin-top:12px"><b>Riesgo por acoplamiento de frecuencias.</b> Un equipo cuya frecuencia propia coincide con la de su soporte (β ≈ 1) no deja la resonancia donde estaba: la separa en dos picos a {I(r"\omega_{1,2}/\omega_{n1}\approx 1\mp\sqrt{\mu}/2")} cuando μ es pequeño. Con μ = 0.10 quedan en 0.854 y 1.171; una excitación que antes estaba lejos de la resonancia puede caer ahora sobre uno de los dos modos, y el equipo ligero se mueve mucho más que la estructura. Por eso los requisitos de diseño piden separar las frecuencias de los equipos de las de la estructura que los soporta (regla de la octava: al menos un factor 2).</div>
    <div class="takeaway" style="margin-top:10px"><b>Cómo explorar:</b> (1) con «Sintonía exacta», llevar la excitación a <i>r</i> = 1: la estructura queda inmóvil y el absorbedor se mueve en oposición a la fuerza; a cambio aparecen dos resonancias nuevas a los lados. (2) Con «Óptimo de Den Hartog» los dos picos quedan a la misma altura y mucho más bajos. (3) Con «Ir al modo 1» y «Ir al modo 2» se compara el movimiento en fase y en oposición. (4) Al reducir μ, los dos picos se acercan: un absorbedor ligero protege una banda más angosta. Referencias: Den Hartog, <i>Mechanical Vibrations</i>, 4.ª ed., secc. 3.2 y 3.3; Bottega, <i>Engineering Vibrations</i>, 2.ª ed., caps. 6 a 8; Rao, <i>Mechanical Vibrations</i>, 5.ª ed., secc. 9.11.</div>
  </div>
"""
script = r"""
const NAVY='#1F3864',STEEL='#4472C4',ORANGE='#C55A11',GREEN='#2E7D46',GREY='#5B5B5B',RED='#B23A3A';
const $=id=>document.getElementById(id);
let S={m1:10,k1:4000,z1:0.01,mu:0.1,be:1,z2:0.02,r:1}, anim=true, t0=performance.now();
function modelo(){ const wn=Math.sqrt(S.k1/S.m1), m2=S.mu*S.m1, wa=S.be*wn, k2=m2*wa*wa, c1=2*S.z1*S.m1*wn, c2=2*S.z2*m2*wa;
  const b=1+S.be*S.be*(1+S.mu), d=Math.sqrt(Math.max(0,b*b-4*S.be*S.be)), q1=Math.sqrt((b-d)/2), q2=Math.sqrt((b+d)/2);
  const u=q=>{ const den=S.be*S.be-q*q; return Math.abs(den)<1e-12?Infinity:S.be*S.be/den; };
  return {wn,m2,wa,k2,c1,c2,q1,q2,u1:u(q1),u2:u(q2)}; }
// respuesta compleja adimensional X/X0 a la razón de frecuencias r (ecuación 4)
function resp(r,P){ const w=r*P.wn, a_r=S.k1+P.k2-S.m1*w*w, a_i=w*(P.c1+P.c2), b_r=-P.k2, b_i=-w*P.c2, d_r=P.k2-S.mu*S.m1*w*w, d_i=w*P.c2;
  const det_r=a_r*d_r-a_i*d_i-(b_r*b_r-b_i*b_i), det_i=a_r*d_i+a_i*d_r-2*b_r*b_i, den=det_r*det_r+det_i*det_i;
  const x1r=(d_r*det_r+d_i*det_i)/den, x1i=(d_i*det_r-d_r*det_i)/den, x2r=-(b_r*det_r+b_i*det_i)/den, x2i=-(b_i*det_r-b_r*det_i)/den;
  return {x1:[x1r*S.k1,x1i*S.k1], x2:[x2r*S.k1,x2i*S.k1]}; }
const mod=z=>Math.hypot(z[0],z[1]);
function sola(r){ return 1/Math.hypot(1-r*r,2*S.z1*r); }
function ejes(c,cv,H){ const dpr=Math.min(window.devicePixelRatio||1,2), Wd=cv.clientWidth||760; cv.width=Wd*dpr; cv.height=H*dpr; cv.style.height=H+'px'; c.setTransform(dpr,0,0,dpr,0,0); c.clearRect(0,0,Wd,H); return Wd; }
let PK=0;
function curva(){
  const P=modelo(), cv=$('cf'), c=cv.getContext('2d'), H=380, Wd=ejes(c,cv,H), mL=52,mR=14,mT=22,mB=36, pw=Wd-mL-mR, ph=H-mT-mB, r0=0.3, r1=2, y0=-2, y1=3;
  const X=r=>mL+(r-r0)/(r1-r0)*pw, Y=v=>mT+(1-(Math.log10(Math.min(Math.max(v,1e-3),2e3))-y0)/(y1-y0))*ph;
  c.strokeStyle='#EDF1F8'; c.fillStyle=GREY; c.font='11px Arial'; c.textAlign='center'; c.textBaseline='top';
  for(let r=0.4;r<=2.001;r+=0.2){ c.beginPath(); c.moveTo(X(r),mT); c.lineTo(X(r),mT+ph); c.stroke(); c.fillText(r.toFixed(1),X(r),mT+ph+5); }
  c.textAlign='right'; c.textBaseline='middle'; for(let e=y0;e<=y1;e++){ const y=mT+(1-(e-y0)/(y1-y0))*ph; c.beginPath(); c.moveTo(mL,y); c.lineTo(mL+pw,y); c.stroke(); c.fillText(e>=0?String(Math.pow(10,e)):String(+Math.pow(10,e).toFixed(2)),mL-6,y); }
  c.fillStyle=NAVY; c.font='bold 12px Arial'; c.textAlign='left'; c.textBaseline='top'; c.fillText('Amplitud adimensional |X|/X_0 (escala logarítmica)', mL, 4); c.textAlign='center'; c.fillText('r = ω/ω_{n1}', mL+pw/2, H-15);
  c.save(); c.beginPath(); c.rect(mL,mT,pw,ph); c.clip();
  c.strokeStyle=GREY; c.setLineDash([6,4]); c.lineWidth=1.4; c.beginPath(); for(let px=0;px<=pw;px++){ const r=r0+px/pw*(r1-r0), y=Y(sola(r)); px?c.lineTo(mL+px,y):c.moveTo(mL+px,y); } c.stroke(); c.setLineDash([]);
  PK=0; const n=4*Math.round(pw);
  c.strokeStyle=ORANGE; c.lineWidth=1.6; c.beginPath(); for(let i=0;i<=n;i++){ const r=r0+i/n*(r1-r0), y=Y(mod(resp(r,P).x2)); i?c.lineTo(X(r),y):c.moveTo(X(r),y); } c.stroke();
  c.strokeStyle=STEEL; c.lineWidth=2.4; c.beginPath(); for(let i=0;i<=n;i++){ const r=r0+i/n*(r1-r0), v=mod(resp(r,P).x1), y=Y(v); if(v>PK) PK=v; i?c.lineTo(X(r),y):c.moveTo(X(r),y); } c.stroke();
  // refinamiento del pico cerca de los dos modos
  [P.q1,P.q2].forEach(q=>{ for(let i=-400;i<=400;i++){ const r=q*(1+i*2.5e-4); if(r>r0&&r<r1){ const v=mod(resp(r,P).x1); if(v>PK) PK=v; } } });
  c.restore();
  c.strokeStyle=GREEN; c.setLineDash([4,4]); c.lineWidth=1.2; c.fillStyle=GREEN; c.font='bold 11px Arial'; c.textBaseline='top';
  [[P.q1,'ω_1'],[P.q2,'ω_2']].forEach(([q,n])=>{ if(q>r0&&q<r1){ c.beginPath(); c.moveTo(X(q),mT); c.lineTo(X(q),mT+ph); c.stroke(); c.textAlign='center'; c.fillText(n,X(q),mT+3); } }); c.setLineDash([]);
  c.strokeStyle=RED; c.lineWidth=1.6; c.beginPath(); c.moveTo(X(S.r),mT); c.lineTo(X(S.r),mT+ph); c.stroke();
  const R=resp(S.r,P); c.fillStyle=RED; c.beginPath(); c.arc(X(S.r),Y(mod(R.x1)),4.5,0,7); c.fill();
  const f=(v,d)=>(+v).toFixed(d);
  $('oW').textContent=f(P.wn,2)+' rad/s · '+f(P.wn/2/Math.PI,2)+' Hz'; $('oMK').textContent=f(P.m2,2)+' kg · '+f(P.k2,0)+' N/m';
  $('oW1').textContent=f(P.q1*P.wn,2)+' rad/s ('+f(P.q1,3)+')'; $('oW2').textContent=f(P.q2*P.wn,2)+' rad/s ('+f(P.q2,3)+')';
  $('oU1').textContent=isFinite(P.u1)?f(P.u1,3):'∞'; $('oU2').textContent=isFinite(P.u2)?f(P.u2,3).replace('-','−'):'∞';
  const g=v=>v>=100?f(v,0):(v>=10?f(v,1):(v>=0.1?f(v,2):f(v,4)));
  $('oX1').textContent=g(mod(R.x1)); $('oX2').textContent=g(mod(R.x2)); $('oXs').textContent=g(sola(S.r)); $('oPk').textContent=g(PK);
}
function masas(now){
  const P=modelo(), cv=$('cm'), c=cv.getContext('2d'), H=250, Wd=ejes(c,cv,H), col=Wd/3, R=resp(S.r,P), ph=anim?((now-t0)/1000)*2*Math.PI*0.6:0;
  const a1=mod(R.x1), a2=mod(R.x2), am=Math.max(a1,a2,1e-9), f1=Math.atan2(R.x1[1],R.x1[0]), f2=Math.atan2(R.x2[1],R.x2[0]);
  const casos=[['Modo 1 · en fase',1,isFinite(P.u1)?P.u1:1e3,0,0],['Modo 2 · en oposición',1,isFinite(P.u2)?P.u2:-1e3,0,0],['Movimiento forzado en r = '+S.r.toFixed(3),a1/am,a2/am,f1,f2]];
  casos.forEach((k,j)=>{ const x0=j*col+18, w=col-36, cx=x0+w/2, nrm=j<2?Math.max(Math.abs(k[1]),Math.abs(k[2])):1, A=Math.min(34,w*0.16);
    const d1=A*k[1]/nrm*Math.cos(ph+k[3]), d2=A*k[2]/nrm*Math.cos(ph+k[4]);
    c.fillStyle=NAVY; c.font='bold 12px Arial'; c.textAlign='center'; c.textBaseline='top'; c.fillText(k[0],cx,6);
    const yB=H-26, y1m=H-118+0, y2m=H-200;
    c.fillStyle='#D9D2BF'; c.fillRect(x0+10,yB,w-20,8);
    const res=(xa,ya,xb,yb)=>{ c.strokeStyle=GREY; c.lineWidth=1.4; c.beginPath(); c.moveTo(xa,ya); const n=7; for(let i=1;i<n;i++){ const t=i/n; c.lineTo(xa+(xb-xa)*t+(i%2?7:-7),ya+(yb-ya)*t); } c.lineTo(xb,yb); c.stroke(); };
    res(cx,yB,cx+d1,y1m+30); res(cx+d1,y1m,cx+d2,y2m+26);
    c.fillStyle=STEEL; c.fillRect(cx+d1-34,y1m,68,30); c.fillStyle=ORANGE; c.fillRect(cx+d2-22,y2m,44,26);
    c.fillStyle='#fff'; c.font='bold 11px Arial'; c.textBaseline='middle'; c.fillText('m_1',cx+d1,y1m+15); c.fillText('m_2',cx+d2,y2m+13);
    c.strokeStyle='rgba(0,0,0,.15)'; c.setLineDash([3,3]); c.beginPath(); c.moveTo(cx,y2m-8); c.lineTo(cx,yB); c.stroke(); c.setLineDash([]);
    c.fillStyle=GREY; c.font='11px Arial'; c.textBaseline='top';
    c.fillText(j<2?('X_2/X_1 = '+(Math.abs(k[2])>=999?'∞':(+k[2]).toFixed(2).replace('-','−'))):('desfase entre masas: '+(((f2-f1)*180/Math.PI%360+540)%360-180).toFixed(0).replace('-','−')+'°'),cx,yB+10);
  });
  if(anim) requestAnimationFrame(masas);
}
function sync(){ curva(); if(!anim) masas(performance.now()); }
const DEC={m1:1,k1:0,z1:3,mu:2,be:3,z2:3,r:3}, UN={m1:' kg',k1:' N/m'};
Object.keys(DEC).forEach(id=>$(id).addEventListener('input',e=>{ S[id]=+e.target.value; $('v'+id).textContent=(+S[id].toFixed(4))+(UN[id]||''); sync(); }));
function pon(o){ Object.keys(o).forEach(k=>{ S[k]=o[k]; $(k).value=o[k]; $('v'+k).textContent=(+(+o[k]).toFixed(4))+(UN[k]||''); }); sync(); }
$('bDH').onclick=()=>pon({be:1/(1+S.mu), z2:Math.sqrt(3*S.mu/(8*Math.pow(1+S.mu,3))), z1:0});
$('bT').onclick=()=>pon({be:1,z2:0,r:1}); $('bE').onclick=()=>pon({mu:0.02,be:1.05,z2:0.02,z1:0.02,r:1});
$('bM1').onclick=()=>pon({r:Math.min(2,Math.max(0.3,modelo().q1))}); $('bM2').onclick=()=>pon({r:Math.min(2,Math.max(0.3,modelo().q2))});
$('bAn').onclick=function(){ anim=!anim; this.classList.toggle('on',anim); this.textContent=anim?'Animar':'Animación en pausa'; if(anim){ t0=performance.now(); requestAnimationFrame(masas); } else masas(performance.now()); };
window.addEventListener('resize',sync);
window.__gdl={S,modelo,resp,pico:()=>PK};
curva(); requestAnimationFrame(masas);
"""
pagina("dosgdl_interactivo.html", "Dos grados de libertad y absorbedor", "Vibraciones · Pilar 12 · U8",
       "Al acoplar un segundo sistema a la estructura se observa cómo la resonancia se divide en dos modos, cómo se mueven las masas en cada uno y cómo un absorbedor sintonizado anula la respuesta",
       cuerpo, script, "Explorador didáctico de sistemas de dos grados de libertad, formas modales y absorbedor dinámico · material de apoyo del curso de Vibraciones · funciona sin conexión (un solo archivo).")
