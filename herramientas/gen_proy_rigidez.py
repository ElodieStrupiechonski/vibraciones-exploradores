#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera proy_rigidez.html · Apoyo a los proyectos · Caracterizar la rigidez k (estática, masa añadida y fórmula de viga).
Uso: python3 gen_proy_rigidez.py CARPETA"""
from base_pag import *

cuerpo = f"""
<style>
  .dat{{width:100%;min-height:150px;font:13px/1.45 'IBM Plex Mono',Consolas,monospace;border:1px solid var(--line);border-radius:8px;padding:8px;box-sizing:border-box}}
  .tabs{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px}} .pan{{display:none}} .pan.on{{display:block}}
  .err{{color:var(--red);font-size:12.5px;margin-top:4px}}
</style>
  <div class="intro full">
    <b>¿Qué resuelve?</b> La rigidez <i>k</i> de un resorte, de un conjunto de ligas, de una placa sobre un tapete o de una viga en voladizo se puede obtener de tres maneras: <b>estática</b> (cargas conocidas y deflexión medida), <b>dinámica con masa añadida</b> (frecuencia natural con varias masas extra) y <b>por fórmula</b> (viga en voladizo). La página ajusta una recta por mínimos cuadrados a los datos de cada equipo y da <i>k</i> con su incertidumbre. Se recomienda usar dos métodos y compararlos: si no coinciden, el modelo de un grado de libertad o la sujeción tienen un problema.
  </div>
  <div class="card full">
    <div class="tabs"><button class="btn on" data-t="est">1 · Estática: cargas y deflexión</button><button class="btn" data-t="din">2 · Dinámica: masa añadida</button><button class="btn" data-t="vig">3 · Fórmula: viga en voladizo</button></div>

    <div class="pan on" id="p-est"><div class="two"><div>
      <p>Un renglón por medición: <b>masa colgada o apoyada (g), deflexión (mm)</b>. La deflexión se mide desde la posición sin carga añadida; conviene esperar unos segundos antes de leer, porque el hule y el PLA se siguen deformando un poco.</p>
      <textarea class="dat" id="dest" spellcheck="false"></textarea><div class="err" id="eest"></div>
      <div class="btns"><button class="btn" data-ej="est-A">Ejemplo: una liga (A)</button><button class="btn" data-ej="est-T">Ejemplo: placa sobre tapete (A)</button><button class="btn" data-ej="est-C">Ejemplo: segueta (C)</button></div>
      <div class="tiles t3" style="margin-top:10px">{tile("Rigidez <i>k</i>", "kest", "hl")}{tile("Incertidumbre de <i>k</i>", "ukest")}{tile("Ajuste <i>R</i>²", "r2est")}</div>
      <div class="nota" id="nest"></div>
    </div><div><canvas id="cest" width="420" height="320" aria-label="Deflexión contra fuerza"></canvas></div></div></div>

    <div class="pan" id="p-din"><div class="two"><div>
      <p>Un renglón por medición: <b>masa añadida (g), frecuencia natural medida (Hz)</b>. La primera puede ser 0. Como <i>f</i> = (1/2π)√(<i>k</i>/(<i>m</i> + Δ<i>M</i>)), la gráfica de 1/<i>f</i>² contra Δ<i>M</i> es una recta: de su pendiente sale <i>k</i> y de su ordenada, la masa efectiva <i>m</i>, sin tener que estimarla.</p>
      <textarea class="dat" id="ddin" spellcheck="false"></textarea><div class="err" id="edin"></div>
      <div class="btns"><button class="btn" data-ej="din-T">Ejemplo: placa sobre tapete (A)</button><button class="btn" data-ej="din-C">Ejemplo: segueta con imán (C)</button></div>
      <div class="tiles t3" style="margin-top:10px">{tile("Rigidez <i>k</i>", "kdin", "hl")}{tile("Incertidumbre de <i>k</i>", "ukdin")}{tile("Masa efectiva <i>m</i>", "mdin")}</div>
      <div class="nota" id="ndin"></div>
    </div><div><canvas id="cdin" width="420" height="320" aria-label="Inverso del cuadrado de la frecuencia contra masa añadida"></canvas></div></div></div>

    <div class="pan" id="p-vig"><div class="two"><div>
      <div class="btns"><button class="btn on" data-mat="hss">Acero (segueta HSS)</button><button class="btn" data-mat="al">Aluminio</button><button class="btn" data-mat="pla">PLA impreso</button></div>
      {fila("Módulo de Young <i>E</i>", "E", 1, 220, 0.1, 200, "GPa")}
      {fila("Densidad ρ", "rho", 900, 8000, 10, 7850, "kg/m³")}
      {fila("Ancho <i>b</i>", "b", 1, 50, 0.1, 12.7, "mm")}
      {fila("Espesor <i>h</i>", "h", 0.1, 10, 0.01, 0.64, "mm")}
      {fila("Longitud libre <i>L</i>", "L", 10, 400, 1, 150, "mm")}
      {fila("Masa en la punta <i>M</i>", "Mp", 0, 200, 0.1, 23, "g")}
      <div class="tiles t3" style="margin-top:10px">{tile("Rigidez en la punta <i>k</i>", "kvig", "hl")}{tile("Masa efectiva", "mvig")}{tile("Frecuencia natural <i>f</i><sub>n</sub>", "fvig", "hl")}{tile("Flecha estática por <i>M</i>", "dvig")}{tile("Primer modo sin masa", "f0vig")}{tile("Masa de la viga", "mbvig")}</div>
      <div class="nota">Los valores de <i>E</i> son representativos. En el PLA impreso dependen del relleno, la orientación y la temperatura: si la precisión importa, conviene medir <i>k</i> con el método 1 y despejar <i>E</i>. Un error de 5 % en <i>h</i> produce 15 % en <i>k</i>, porque <i>k</i> ∝ <i>h</i>³: medir el espesor con micrómetro.</div>
    </div><div>
      {eq("Viga en voladizo, carga en la punta", M(r"k=\frac{3EI}{L^3},\qquad I=\frac{bh^3}{12},\qquad m_{\mathrm{ef}}=0.2357\,m_{\mathrm{viga}}+M,\qquad f_n=\frac{1}{2\pi}\sqrt{\frac{k}{m_{\mathrm{ef}}}}") + nota("la masa efectiva 33/140 de la viga viene del método de Rayleigh con la deformada estática; primer modo sin masa: f<sub>1</sub> = (1.875²/2π L²)√(EI/μ)"))}
      {eq("Resortes combinados", M(r"\text{paralelo: }k=k_1+k_2+\ldots\qquad \text{serie: }\frac1k=\frac1{k_1}+\frac1{k_2}+\ldots") + nota("cuatro ligas iguales bajo una plataforma trabajan en paralelo: k = 4k<sub>1</sub>; una liga doblada en dos, también en paralelo"))}
    </div></div></div>
  </div>
  <div class="card full">
    <h2>Las fórmulas del ajuste</h2>
    <div class="two"><div>
    {eq("1 · Estática", M(r"\delta=\frac{F}{k}+\delta_0,\qquad F=Mg\quad\Rightarrow\quad k=\frac{1}{s}") + nota("s es la pendiente de la recta de δ contra F; se ajusta δ contra F porque el error está en la deflexión; la ordenada δ<sub>0</sub> absorbe un cero mal puesto"))}
    </div><div>
    {eq("2 · Masa añadida", M(r"\frac{1}{f^2}=\frac{4\pi^2}{k}\,m+\frac{4\pi^2}{k}\,\Delta M\quad\Rightarrow\quad k=\frac{4\pi^2}{s},\qquad m=\frac{c}{s}") + nota("s es la pendiente y c la ordenada de la recta de 1/f² contra ΔM (en kg); la incertidumbre sale del error estándar de la pendiente"))}
    </div></div>
    <div class="takeaway" style="margin-top:10px"><b>Consejos.</b> (1) Al menos cuatro cargas, repartidas en todo el intervalo de trabajo; las ligas y el tapete no son lineales, así que conviene medir con cargas cercanas a las del ensayo. (2) La frecuencia de cada masa añadida, como promedio de tres golpes; en un decaimiento corto es más preciso contar ciclos en el tiempo que leer el pico de la FFT. (3) En los elastómeros la rigidez dinámica suele ser mayor que la estática: para el modelo de vibración vale la dinámica. (4) Si <i>R</i>² baja de 0.98, revisar un dato o la sujeción antes de usar el resultado. Referencias: Rao, <i>Mechanical Vibrations</i>, 5.ª ed., Pearson, cap. 2 (rigidez de elementos y método de Rayleigh); Beer, Johnston, DeWolf y Mazurek, <i>Mecánica de materiales</i>, 7.ª ed., McGraw-Hill (deflexión de vigas).</div>
  </div>
"""
script = LIB + r"""
const G0=9.80665, TP=2*Math.PI;
let S={E:200,rho:7850,b:12.7,h:0.64,L:150,Mp:23};
const UN={E:' GPa',rho:' kg/m³',b:' mm',h:' mm',L:' mm',Mp:' g'};
const EJ={'est-A':'0, 0\n100, 9.3\n200, 18.1\n300, 27.6\n400, 36.4','est-T':'0, 0\n500, 0.84\n1000, 1.62\n1500, 2.48\n2000, 3.25','est-C':'0, 0\n5, 1.02\n10, 1.97\n15, 3.01\n20, 3.96',
          'din-T':'0, 9.21\n250, 8.62\n500, 8.11\n1000, 7.36','din-C':'0, 7.02\n5, 6.41\n10, 5.96\n20, 5.24'};
function leer(t){ const P=[], mal=[]; t.split(/\n/).forEach((l,i)=>{ l=l.trim(); if(!l||l[0]==='#') return; const v=l.split(/[\s;,\t]+/).map(x=>Number(x.replace('−','-'))); if(v.length<2||!isFinite(v[0])||!isFinite(v[1])) mal.push(i+1); else P.push([v[0],v[1]]); }); return {P,mal}; }
// regresión lineal y = a + s x, con error estándar de la pendiente
function recta(P){ const n=P.length, mx=P.reduce((a,p)=>a+p[0],0)/n, my=P.reduce((a,p)=>a+p[1],0)/n; let sxx=0,sxy=0,syy=0; P.forEach(p=>{ sxx+=(p[0]-mx)**2; sxy+=(p[0]-mx)*(p[1]-my); syy+=(p[1]-my)**2; });
  const s=sxy/sxx, a=my-s*mx, ssr=P.reduce((q,p)=>q+(p[1]-a-s*p[0])**2,0), se=n>2?Math.sqrt(ssr/(n-2)/sxx):NaN, r2=syy>0?1-ssr/syy:1; return {s,a,se,r2,n}; }
function estatica(t){ const {P,mal}=leer(t); if(P.length<3) return {err:'Hacen falta al menos tres renglones válidos'+(mal.length?' (revisar renglón '+mal.join(', ')+')':'')+'.'};
  const Q=P.map(p=>[p[0]*1e-3*G0, p[1]*1e-3]); const r=recta(Q); if(!(r.s>0)) return {err:'La deflexión no crece con la carga: revisar los datos.'}; const k=1/r.s; return {k, uk:k*r.se/r.s, r2:r.r2, r, Q, mal}; }
function dinamica(t){ const {P,mal}=leer(t); if(P.length<3) return {err:'Hacen falta al menos tres renglones válidos'+(mal.length?' (revisar renglón '+mal.join(', ')+')':'')+'.'};
  const Q=P.map(p=>[p[0]*1e-3, 1/(p[1]*p[1])]); const r=recta(Q); if(!(r.s>0)) return {err:'La frecuencia debe bajar al añadir masa: revisar los datos.'}; const k=4*Math.PI*Math.PI/r.s; return {k, uk:k*r.se/r.s, m:r.a/r.s, r2:r.r2, r, Q, mal}; }
function viga(){ const b=S.b*1e-3, h=S.h*1e-3, L=S.L*1e-3, E=S.E*1e9, I=b*h**3/12, k=3*E*I/L**3, mb=S.rho*b*h*L, mef=0.2357*mb+S.Mp*1e-3, mu=S.rho*b*h;
  return {k, mb, mef, fn:Math.sqrt(k/mef)/TP, d:S.Mp*1e-3*G0/k, f0:1.875104**2/(TP*L*L)*Math.sqrt(E*I/mu)}; }
const fmt=(v,u)=>isFinite(v)?(+v.toPrecision(3))+' '+u:'…';
function graf(id,Q,r,xl,yl,tit,sx,sy){ const g=lienzo($(id),320); const xs=Q.map(p=>p[0]*sx), ys=Q.map(p=>p[1]*sy); const x1=Math.max(...xs)*1.08||1, y1=Math.max(...ys,(r.a+r.s*Math.max(...Q.map(p=>p[0])))*sy)*1.1||1;
  const e=ejes(g,{mL:58},{x0:0,x1,y0:Math.min(0,Math.min(...ys)),y1,xl,yl,tit,nx:5,ny:5}); funcion(e,x=>(r.a+r.s*x/sx)*sy,STEEL,2,null,100); Q.forEach(p=>punto(e,p[0]*sx,p[1]*sy,RED,4.5)); }
function pEst(){ const R=estatica($('dest').value); $('eest').textContent=R.err||''; if(R.err){ ['kest','ukest','r2est'].forEach(i=>$(i).textContent='…'); lienzo($('cest'),320); return; }
  $('kest').textContent=fmt(R.k,'N/m'); $('ukest').textContent='± '+fmt(R.uk,'N/m')+' ('+(100*R.uk/R.k).toFixed(1)+' %)'; $('r2est').textContent=R.r2.toFixed(4);
  $('nest').textContent=(R.r2<0.98?'R² bajo: revisar un dato, la no linealidad o la sujeción. ':'')+'Deflexión con 1 N: '+fmt(1e3/R.k,'mm')+'. Ordenada (cero de la medición): '+fmt(R.r.a*1e3,'mm')+'.';
  graf('cest',R.Q,R.r,'fuerza F (N)','deflexión δ (mm)','Deflexión contra fuerza',1,1e3); }
function pDin(){ const R=dinamica($('ddin').value); $('edin').textContent=R.err||''; if(R.err){ ['kdin','ukdin','mdin'].forEach(i=>$(i).textContent='…'); lienzo($('cdin'),320); return; }
  $('kdin').textContent=fmt(R.k,'N/m'); $('ukdin').textContent='± '+fmt(R.uk,'N/m')+' ('+(100*R.uk/R.k).toFixed(1)+' %)'; $('mdin').textContent=R.m>0?fmt(R.m*1e3,'g'):'negativa: revisar';
  $('ndin').textContent=(R.r2<0.98?'R² bajo: revisar un dato. ':'')+'Ajuste R² = '+R.r2.toFixed(4)+'. Frecuencia sin masa añadida según el ajuste: '+fmt(1/Math.sqrt(R.r.a),'Hz')+'.';
  graf('cdin',R.Q,R.r,'masa añadida ΔM (g)','1/f² (s² × 1000)','Recta de masa añadida',1e3,1e3); }
function pVig(){ const v=viga(); $('kvig').textContent=fmt(v.k,'N/m'); $('mvig').textContent=fmt(v.mef*1e3,'g'); $('fvig').textContent=fmt(v.fn,'Hz'); $('dvig').textContent=fmt(v.d*1e3,'mm'); $('f0vig').textContent=fmt(v.f0,'Hz'); $('mbvig').textContent=fmt(v.mb*1e3,'g'); }
liga(S,UN,pVig);
const MAT={hss:{E:200,rho:7850,b:12.7,h:0.64,L:150,Mp:23},al:{E:69,rho:2700,b:20,h:2,L:200,Mp:0},pla:{E:3.0,rho:1240,b:10,h:2,L:40,Mp:0}};
document.querySelectorAll('[data-mat]').forEach(bt=>bt.addEventListener('click',()=>{ document.querySelectorAll('[data-mat]').forEach(x=>x.classList.toggle('on',x===bt)); pon(S,UN,MAT[bt.dataset.mat],pVig); }));
document.querySelectorAll('[data-t]').forEach(bt=>bt.addEventListener('click',()=>{ document.querySelectorAll('[data-t]').forEach(x=>x.classList.toggle('on',x===bt)); document.querySelectorAll('.pan').forEach(p=>p.classList.toggle('on',p.id==='p-'+bt.dataset.t)); pEst(); pDin(); pVig(); }));
document.querySelectorAll('[data-ej]').forEach(bt=>bt.addEventListener('click',()=>{ const k=bt.dataset.ej; if(k.startsWith('est')){ $('dest').value=EJ[k]; pEst(); } else { $('ddin').value=EJ[k]; pDin(); } }));
$('dest').addEventListener('input',pEst); $('ddin').addEventListener('input',pDin);
let guard=null; try{ guard=JSON.parse(localStorage.getItem('rig-vib')||'null'); }catch(e){}
$('dest').value=(guard&&guard.e)||EJ['est-A']; $('ddin').value=(guard&&guard.d)||EJ['din-T'];
['dest','ddin'].forEach(i=>$(i).addEventListener('change',()=>{ try{ localStorage.setItem('rig-vib',JSON.stringify({e:$('dest').value,d:$('ddin').value})); }catch(e){} }));
window.addEventListener('resize',()=>{ pEst(); pDin(); });
window.__ri={S,estatica,dinamica,viga,recta};
pEst(); pDin(); pVig();
"""
pagina("proy_rigidez.html", "Caracterizar la rigidez de un resorte o una placa", "Vibraciones · Apoyo a los proyectos",
       "Rigidez k por tres caminos: cargas y deflexión, frecuencia con masa añadida y fórmula de la viga en voladizo, con ajuste por mínimos cuadrados e incertidumbre",
       cuerpo, script, "Apoyo a los proyectos del curso de Vibraciones: medición de la rigidez · funciona sin conexión (un solo archivo).")
