#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera perdida_interactivo.html · Pilar 18 · Pérdida por transmisión de un panel (U6, tema 6.3, parte acústica).
Uso: python3 gen_perdida.py CARPETA"""
from base_pag import *

cuerpo = f"""
  <div class="intro full">
    <b>¿Qué muestra?</b> Un panel separa la fuente de ruido del recinto que se quiere proteger: el fuselaje frente a la capa límite turbulenta, la cofia frente al ruido del despegue, una pared frente a una máquina. La <b>pérdida por transmisión</b> <i>TL</i> indica cuántos decibeles pierde el sonido al atravesarlo. A baja frecuencia manda la masa del panel (<b>ley de masa</b>: +6 dB por octava). Cerca de la <b>frecuencia crítica</b> <i>f</i><sub>c</sub> la onda de flexión del panel viaja a la misma velocidad que la traza de la onda sonora, el panel deja pasar el sonido y la curva se hunde (<b>coincidencia</b>); ahí solo ayuda el amortiguamiento. El explorador calcula la curva de un panel infinito, homogéneo y delgado, en incidencia normal, oblicua y de campo difuso.
  </div>

  <div class="card">
    <canvas id="ctl" width="760" height="430" aria-label="Pérdida por transmisión en función de la frecuencia"></canvas>
    <div class="legend">
      <span><i class="sw" style="border-top-color:var(--steel)"></i> campo difuso (0° a 78°)</span>
      <span><i class="sw" style="border-top-color:var(--orange);border-top-style:dashed"></i> ley de masa, incidencia normal</span>
      <span><i class="sw" style="border-top-color:var(--purple)"></i> incidencia oblicua θ</span>
      <span><i class="sw" style="border-top-color:var(--green);border-top-style:dashed"></i> frecuencia crítica <i>f</i><sub>c</sub></span>
      <span><i class="sw" style="border-top-color:var(--red)"></i> frecuencia de lectura</span>
    </div>
  </div>

  <div class="card">
    <h2>Controles</h2>
    <div class="grp"><div class="t">Panel</div>
      <div class="btns"><button class="btn on" data-mat="al">Aluminio</button><button class="btn" data-mat="ac">Acero</button><button class="btn" data-mat="vi">Vidrio</button><button class="btn" data-mat="ye">Panel de yeso</button><button class="btn" data-mat="co">Concreto</button></div>
      {fila("Módulo de Young <i>E</i>", "E", 1, 220, 0.5, 70, "GPa")}
      {fila("Densidad ρ", "rho", 300, 8000, 10, 2700, "kg/m³")}
      {fila("Espesor <i>h</i>", "h", 0.5, 200, 0.5, 2, "mm")}
      {fila("Factor de pérdida η", "eta", 0.005, 0.3, 0.005, 0.01)}
    </div>
    <div class="grp"><div class="t">Onda incidente</div>
      {fila("Frecuencia de lectura <i>f</i>", "f", 50, 10000, 10, 1000, "Hz")}
      {fila("Ángulo de incidencia θ", "th", 0, 85, 1, 60, "°")}
    </div>
    <div class="btns">
      <button class="btn" data-pre="F">Piel de fuselaje, 2 mm</button><button class="btn" data-pre="V">Ventana, 6 mm</button><button class="btn" data-pre="M">Muro de concreto, 100 mm</button><button class="btn" data-pre="A">Mismo panel con capa amortiguadora</button>
      <button class="btn" id="pra">Ocultar lecturas (modo práctica)</button>
    </div>
    <div class="tiles t3" style="margin-top:10px">
      {tile("Masa superficial <i>m</i>″", "om")}{tile("Frecuencia crítica <i>f</i><sub>c</sub>", "ofc", "hl")}{tile("Coincidencia para θ", "ofco")}
      {tile("<i>TL</i> en campo difuso", "otl", "hl")}{tile("Fracción de potencia transmitida τ", "otau")}{tile("Ley de masa (normal)", "otn")}
      {tile("<i>TL</i> para el ángulo θ", "oto")}{tile("Ganancia al duplicar el espesor", "odup")}{tile("Rigidez a flexión <i>B</i>", "oB")}
    </div>
    <div class="nota" id="olect"></div>
  </div>

  <div class="card full">
    <h2>Las fórmulas en pantalla</h2>
    <div class="two"><div>
    {eq("1 · Definición", M(r"TL=10\log_{10}\frac{1}{\tau},\qquad \tau=\frac{W_{\text{transmitida}}}{W_{\text{incidente}}}") + nota("<i>TL</i> = 30 dB significa que pasa una milésima de la potencia sonora"))}
    {eq("2 · Ley de masa en incidencia normal", M(r"TL_0=10\log_{10}\left[1+\left(\frac{\pi f\,m''}{\rho_0 c}\right)^2\right]\approx 20\log_{10}\left(f\,m''\right)-42.4\ \text{dB}") + nota("<i>m</i>″ = ρ<i>h</i> en kg/m², <i>f</i> en Hz; aire a 20 °C: ρ<sub>0</sub><i>c</i> = 413 Pa·s/m. Duplicar la masa o la frecuencia suma 6 dB"))}
    {eq("3 · Frecuencia crítica", M(r"f_c=\frac{c^2}{2\pi}\sqrt{\frac{m''}{B}},\qquad B=\frac{E\,h^3}{12\,(1-\nu^2)}") + nota("en ella la longitud de onda de flexión del panel iguala a la del sonido en el aire; como <i>f</i><sub>c</sub> es proporcional a 1/<i>h</i>, el producto <i>f</i><sub>c</sub><i>h</i> es una constante del material"))}
    </div><div>
    {eq("4 · Panel infinito en incidencia oblicua", M(r"\tau(\theta)=\left|1+\frac{Z\cos\theta}{2\rho_0 c}\right|^{-2},\qquad Z=j\omega m''\left[1-\left(\frac{f}{f_c}\right)^2\mathrm{sen}^4\theta\,(1+j\eta)\right]") + nota("la parte imaginaria de <i>Z</i> se anula en la frecuencia de coincidencia <i>f</i><sub>c</sub>/sen²θ; ahí solo queda el término de amortiguamiento"))}
    {eq("5 · Campo difuso", M(r"\tau_d=\frac{\int_0^{\theta_l}\tau(\theta)\,\mathrm{sen}\,2\theta\,d\theta}{\int_0^{\theta_l}\mathrm{sen}\,2\theta\,d\theta},\qquad \theta_l=78\degree") + nota("promedio sobre los ángulos de incidencia; el límite de 78° («incidencia de campo») es la convención que mejor reproduce las mediciones; la integral se evalúa numéricamente"))}
    {eq("6 · Por encima de la frecuencia crítica", M(r"f>f_c:\qquad TL\approx TL_0+10\log_{10}\left(\frac{2\eta}{\pi}\,\frac{f}{f_c}\right)") + nota("la pérdida depende del amortiguamiento y crece 9 dB por octava"))}
    </div></div>
    <div class="intro" style="margin-top:12px"><b>Hipótesis y límites del modelo.</b> Panel plano, infinito, homogéneo, isótropo y delgado (teoría de placas de Kirchhoff), con aire a 20 °C en ambas caras (ρ<sub>0</sub> = 1.204 kg/m³, <i>c</i> = 343 m/s). No se modelan: las resonancias del panel finito y la zona controlada por la rigidez, por debajo de su primera frecuencia natural; las fugas por juntas y rendijas, que en la práctica suelen limitar el aislamiento; las paredes dobles ni los paneles de emparedado, cuyo núcleo ligero y rígido baja la frecuencia crítica. Los valores de <i>E</i>, ρ, ν y η de los botones son representativos; el factor de pérdida de un panel instalado depende sobre todo de sus uniones.</div>
    <div class="takeaway" style="margin-top:10px"><b>Cómo explorar:</b> (1) «Piel de fuselaje»: aluminio de 2 mm, 5.4 kg/m²; la frecuencia crítica queda cerca de 6 kHz y en la banda de la voz (500 Hz a 2 kHz) la curva sigue la ley de masa. (2) Al duplicar el espesor la curva sube unos 6 dB a baja frecuencia, pero la frecuencia crítica baja a la mitad: la lectura «Ganancia al duplicar el espesor» resulta negativa entre la mitad de la frecuencia crítica original y esa frecuencia (por ejemplo, −6 dB a 3 kHz). (3) «Ventana»: vidrio de 6 mm con <i>f</i><sub>c</sub> cercana a 2 kHz, dentro de la banda donde el oído es más sensible. (4) «Muro de concreto»: <i>f</i><sub>c</sub> cae cerca de 180 Hz y casi toda la curva queda por encima de ella, controlada por el amortiguamiento. (5) «Capa amortiguadora»: al subir η de 0.01 a 0.1 la curva no cambia por debajo de <i>f</i><sub>c</sub>/2 y gana de 8 a 10 dB a partir de 1.3 <i>f</i><sub>c</sub>. (6) Al mover θ, el mínimo de la curva oblicua se desplaza a <i>f</i><sub>c</sub>/sen²θ: en incidencia normal no hay coincidencia. <b>Relación con el tema 6.3:</b> el explorador de transmisibilidad trata la vía estructural (el soporte que aísla); este trata la vía aérea. En ambos casos el aislamiento a baja frecuencia cuesta masa, y cerca de la resonancia o de la coincidencia solo lo aporta el amortiguamiento. Referencias: Fahy y Gardonio, <i>Sound and Structural Vibration</i>, 2.ª ed., Academic Press, 2007, cap. 5; Bies, Hansen y Howard, <i>Engineering Noise Control</i>, 5.ª ed., CRC Press, 2017 (capítulo de particiones y encapsulados); Cremer, Heckl y Petersson, <i>Structure-Borne Sound</i>, 3.ª ed., Springer, 2005; Kinsler, Frey, Coppens y Sanders, <i>Fundamentals of Acoustics</i>, 4.ª ed., Wiley, 2000 (transmisión a través de una capa y ley de masa).</div>
  </div>
"""
script = LIB + r"""
let S={E:70,rho:2700,h:2,eta:0.01,f:1000,th:60,nu:0.33};
const UN={E:' GPa',rho:' kg/m³',h:' mm',eta:'',f:' Hz',th:'°'}, RHO0=1.204, C0=343, Z0=RHO0*C0, UL=Math.pow(Math.sin(78*Math.PI/180),2), NI=6000;
function panel(h){ h=(h===undefined?S.h:h)*1e-3; const m=S.rho*h, B=S.E*1e9*h*h*h/(12*(1-S.nu*S.nu)); return {m,B,fc:C0*C0/(2*Math.PI)*Math.sqrt(m/B)}; }
// coeficiente de transmisión para u = sen²θ
function tauU(f,u,p){ const a=2*Math.PI*f*p.m*Math.sqrt(1-u)/(2*Z0), r=f/p.fc, q=r*r*u*u, ar=a*S.eta*q, ai=a*(1-q); return 1/((1+ar)*(1+ar)+ai*ai); }
function tauDif(f,p){ let s=0; const du=UL/NI; for(let i=0;i<NI;i++) s+=tauU(f,(i+0.5)*du,p); return s/NI; }
const TL=t=>-10*Math.log10(t), tl0=(f,p)=>10*Math.log10(1+Math.pow(Math.PI*f*p.m/Z0,2));
const FR=[]; for(let i=0;i<=150;i++) FR.push(50*Math.pow(200,i/150));       // 50 Hz a 10 kHz
let CU=null, clave='';
function curvas(){ const k=[S.E,S.rho,S.h,S.eta,S.nu].join('|'); if(k!==clave){ clave=k; const p=panel(); CU=FR.map(f=>TL(tauDif(f,p))); } return CU; }
function calc(){ const p=panel(), p2=panel(2*S.h), u=Math.pow(Math.sin(S.th*Math.PI/180),2), td=tauDif(S.f,p);
  return {p, u, tld:TL(td), taud:td, tln:tl0(S.f,p), tlo:TL(tauU(S.f,u,p)), fco:u>0?p.fc/u:Infinity, dup:TL(tauDif(S.f,p2))-TL(td), cu:curvas()}; }
function dibujar(){
  const q=calc(), p=q.p, g=lienzo($('ctl'),430), ymax=Math.max(40,Math.ceil((Math.max(...q.cu,tl0(1e4,p))+4)/10)*10);
  const e=ejes(g,{},{x0:50,x1:1e4,y0:0,y1:ymax,logx:true,xl:'frecuencia (Hz)',yl:'pérdida por transmisión TL (dB)',tit:'Panel de '+S.h+' mm  ·  m″ = '+(+p.m.toPrecision(3))+' kg/m²  ·  η = '+S.eta,ny:8});
  funcion(e,f=>tl0(f,p),ORANGE,1.5,[6,4],300); const u=q.u; funcion(e,f=>TL(tauU(f,u,p)),PURPLE,1.4,null,700);
  curva(e,FR.map((f,i)=>[f,q.cu[i]]),STEEL,2.6);
  vline(e,p.fc,GREEN,[6,4],'f_c = '+ing(p.fc,'Hz')); vline(e,S.f,RED,[2,3]); punto(e,S.f,q.tld,RED,5.5);
  const c=g.c; c.fillStyle=RED; c.font='bold 11px Arial'; c.textAlign=S.f>3000?'right':'left'; c.textBaseline='bottom'; c.fillText(q.tld.toFixed(1)+' dB',e.X(S.f)+(S.f>3000?-8:8),e.Y(Math.min(q.tld,ymax))-6);
  const d1=v=>v.toFixed(1)+' dB';
  $('om').textContent=(+p.m.toPrecision(3))+' kg/m²'; $('ofc').textContent=ing(p.fc,'Hz'); $('ofco').textContent=isFinite(q.fco)?ing(q.fco,'Hz'):'no hay (θ = 0)';
  $('otl').textContent=d1(q.tld); $('otau').textContent=num(q.taud); $('otn').textContent=d1(q.tln); $('oto').textContent=d1(q.tlo);
  $('odup').textContent=(q.dup>=0?'+':'−')+Math.abs(q.dup).toFixed(1)+' dB'; $('odup').parentNode.classList.toggle('al',q.dup<0); $('oB').textContent=ing(p.B,'N·m');
  const r=S.f/p.fc; $('olect').textContent=r<0.5?'Zona de la ley de masa (f < f_c/2): la pérdida depende solo de la masa superficial y de la frecuencia; el amortiguamiento no influye.':r<=1.5?'Zona de coincidencia (f cercana a f_c): el panel irradia con eficiencia y la pérdida cae por debajo de la ley de masa; solo el amortiguamiento la limita.':'Por encima de la frecuencia crítica: la pérdida crece 9 dB por octava y aumenta cerca de 10 dB por cada década de η.';
}
liga(S,UN,dibujar); practica('pra');
const MAT={al:{E:70,rho:2700,nu:0.33,eta:0.01}, ac:{E:200,rho:7850,nu:0.30,eta:0.01}, vi:{E:70,rho:2500,nu:0.22,eta:0.02}, ye:{E:2,rho:700,nu:0.30,eta:0.03}, co:{E:30,rho:2300,nu:0.20,eta:0.02}};
function mat(k,extra){ document.querySelectorAll('[data-mat]').forEach(b=>b.classList.toggle('on',b.dataset.mat===k)); const o=Object.assign({},MAT[k],extra||{}); S.nu=o.nu; delete o.nu; pon(S,UN,o,dibujar); }
document.querySelectorAll('[data-mat]').forEach(b=>b.addEventListener('click',()=>mat(b.dataset.mat)));
const PRE={F:['al',{h:2,f:1000}], V:['vi',{h:6,f:2000}], M:['co',{h:100,f:500}]};
document.querySelectorAll('[data-pre]').forEach(b=>b.addEventListener('click',()=>{ if(b.dataset.pre==='A'){ pon(S,UN,{eta:0.1},dibujar); return; } const o=PRE[b.dataset.pre]; mat(o[0],o[1]); }));
window.addEventListener('resize',dibujar);
window.__tl={S,calc,panel,tauDif,tauU,FR};
dibujar();
"""
pagina("perdida_interactivo.html", "Pérdida por transmisión de un panel", "Vibraciones · Pilar 18 · U6",
       "Al variar el material, el espesor y el amortiguamiento de un panel se observa cuánto sonido deja pasar en cada frecuencia: ley de masa, coincidencia y control por amortiguamiento",
       cuerpo, script, "Explorador didáctico de la pérdida por transmisión sonora de un panel (ley de masa y coincidencia) · material de apoyo del curso de Vibraciones · funciona sin conexión (un solo archivo).")
