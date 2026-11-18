#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera transmisibilidad_interactivo.html · Pilar 13 · Transmisibilidad y aislamiento (U6, tema 6.3; U1, tema 1.2).
Uso: python3 gen_trans.py CARPETA   (después: integra2.py y mejoras.py)"""
from base_pag import *

cuerpo = f"""
  <div class="intro full">
    <b>¿Qué muestra?</b> Un equipo de masa <i>m</i> descansa sobre un aislador de rigidez <i>k</i> y amortiguamiento <i>c</i>. La <b>transmisibilidad</b> <i>T</i><sub>r</sub> es el cociente entre lo que llega y lo que entra: el movimiento del equipo entre el de la base, o la fuerza que pasa al piso entre la fuerza aplicada. Ambas definiciones conducen a la misma curva. Solo hay <b>aislamiento</b> (<i>T</i><sub>r</sub> &lt; 1) cuando la frecuencia de excitación supera √2 veces la natural; por debajo, el aislador amplifica.
  </div>

  <div class="card">
    <canvas id="ct" width="760" height="400" aria-label="Transmisibilidad contra razón de frecuencias"></canvas>
    <div class="legend">
      <span><i class="sw" style="border-top-color:var(--steel)"></i> <i>T</i><sub>r</sub>(<i>r</i>) con el ζ elegido</span>
      <span><i class="sw" style="border-top-color:var(--grey);border-top-style:dotted"></i> familia ζ = 0.01, 0.1, 0.2, 0.5, 1</span>
      <span id="ldesb"><i class="sw" style="border-top-color:var(--orange)"></i> desbalance: <i>mX</i>/(<i>m</i><sub>0</sub><i>e</i>)</span>
      <span><i class="sw" style="border-top-color:var(--green);border-top-style:dashed"></i> <i>r</i> = √2 (inicio del aislamiento)</span>
      <span><i class="sw" style="border-top-color:var(--red)"></i> punto de operación</span>
    </div>
    <canvas id="cx" width="760" height="230" style="margin-top:10px" aria-label="Entrada y salida en el tiempo"></canvas>
  </div>

  <div class="card">
    <h2>Controles</h2>
    <div class="grp"><div class="t">Caso</div>
      <div class="btns">
        <button class="btn on" data-modo="base">Base móvil</button><button class="btn" data-modo="fuerza">Fuerza armónica</button><button class="btn" data-modo="desb">Desbalance rotatorio</button>
      </div>
      <div class="nota" id="nmodo"></div>
    </div>
    <div class="grp"><div class="t">Equipo y aislador</div>
      {fila("Masa <i>m</i>", "m", 0.05, 50, 0.01, 0.30, "kg")}
      {fila("Rigidez <i>k</i>", "k", 10, 50000, 1, 426, "N/m")}
      {fila("Factor de amortiguamiento ζ", "z", 0.005, 1, 0.005, 0.05)}
    </div>
    <div class="grp"><div class="t">Excitación</div>
      {fila("Frecuencia <i>f</i>", "f", 0.5, 100, 0.1, 15, "Hz")}
      <div id="gY">{fila("Amplitud de la base <i>Y</i>", "Y", 0.1, 20, 0.1, 1, "mm")}</div>
      <div id="gF" style="display:none">{fila("Fuerza <i>F</i><sub>0</sub>", "F0", 0.1, 100, 0.1, 1, "N")}</div>
      <div id="gD" style="display:none">{fila("Masa excéntrica <i>m</i><sub>0</sub>", "m0", 0.5, 100, 0.5, 5, "g")}{fila("Excentricidad <i>e</i>", "e", 1, 50, 0.5, 10, "mm")}</div>
    </div>
    <div class="grp"><div class="t">Diseño: aislamiento requerido</div>
      {fila("Aislamiento a la frecuencia <i>f</i>", "R", 10, 99, 1, 80, "%")}
    </div>
    <div class="btns">
      <button class="btn" data-pre="A">Equipo A: plataforma sobre ligas</button>
      <button class="btn" data-pre="R">En resonancia</button>
      <button class="btn" data-pre="C">Cruce <i>r</i> = √2</button>
      <button class="btn" data-pre="Z">¿Más amortiguamiento aísla mejor?</button>
      <button class="btn" id="pra">Ocultar lecturas (modo práctica)</button>
    </div>
    <div class="tiles t3" style="margin-top:10px">
      {tile("Frecuencia natural <i>f</i><sub>n</sub>", "ofn")}{tile("Deflexión estática δ<sub>st</sub>", "odst")}{tile("Razón <i>r</i> = <i>f</i>/<i>f</i><sub>n</sub>", "or")}
      {tile("Transmisibilidad <i>T</i><sub>r</sub>", "oT", "hl")}{tile("En decibeles", "odB")}{tile("Aislamiento 1 − <i>T</i><sub>r</sub>", "oais", "hl")}
      <div class="tile"><div class="k" id="kfase">Desfase</div><div class="v" id="ofase">…</div></div>{tile("Amplitud del equipo <i>X</i>", "oX")}{tile("Aceleración del equipo", "oacc")}
      {tile("Fuerza transmitida <i>F</i><sub>T</sub>", "oFT")}{tile("Pico: <i>T</i><sub>máx</sub> en <i>f</i>", "opk")}{tile("Para el aislamiento pedido: <i>f</i><sub>n</sub> ≤", "oreq", "hl")}
    </div>
    <div class="nota" id="oreq2"></div>
  </div>

  <div class="card full">
    <h2>Las fórmulas en pantalla</h2>
    <div class="two"><div>
    {eq("1 · Frecuencia natural y deflexión estática", M(r"\omega_n=\sqrt{\frac{k}{m}},\qquad f_n=\frac{\omega_n}{2\pi},\qquad \delta_{\text{st}}=\frac{mg}{k}=\frac{g}{\omega_n^2}") + nota("con un resorte lineal la deflexión estática por sí sola fija <i>f</i><sub>n</sub>: basta medirla con un calibrador. En elastómeros (ligas, hule) la rigidez dinámica supera a la estática y la <i>f</i><sub>n</sub> real resulta mayor"))}
    {eq("2 · Transmisibilidad (de desplazamiento o de fuerza)", M(r"T_r=\frac{X}{Y}=\frac{F_T}{F_0}=\sqrt{\frac{1+(2\zeta r)^2}{(1-r^2)^2+(2\zeta r)^2}},\qquad r=\frac{f}{f_n}"))}
    {eq("3 · Desfase del equipo respecto de la base", M(r"\phi=\arctan\frac{2\zeta r^3}{1-r^2+(2\zeta r)^2}") + nota("se evalúa con atan2, de modo que φ queda entre 0° y 180°; con amortiguamiento, φ pasa por un máximo y tiende a 90° cuando <i>r</i> → ∞"))}
    </div><div>
    {eq("4 · Desbalance rotatorio de masa <i>m</i><sub>0</sub> y excentricidad <i>e</i>", M(r"F_0=m_0\,e\,\omega^2,\qquad F_T=T_r\,m_0\,e\,\omega^2") + M(r"\frac{mX}{m_0 e}=\frac{r^2}{\sqrt{(1-r^2)^2+(2\zeta r)^2}}") + nota("<i>m</i> incluye la masa excéntrica; a alta velocidad <i>X</i> tiende a <i>m</i><sub>0</sub><i>e</i>/<i>m</i>"))}
    {eq("5 · Máximo de la curva", M(r"r_{p}=\frac{\sqrt{\sqrt{1+8\zeta^2}-1}}{2\zeta},\qquad T_{\text{máx}}\approx\frac{1}{2\zeta}\ \ (\zeta\ll1)"))}
    {eq("6 · Diseño sin amortiguamiento: aislamiento <i>R</i> = 1 − <i>T</i><sub>r</sub>", M(r"T_r=\frac{1}{r^2-1}\ \Rightarrow\ r=\sqrt{\frac{2-R}{1-R}},\qquad f_n\leq\frac{f}{r}") + nota("con amortiguamiento el explorador resuelve <i>T</i><sub>r</sub>(<i>r</i>) = 1 − <i>R</i> numéricamente en la rama <i>r</i> &gt; √2"))}
    </div></div>
    <div class="intro" style="margin-top:12px"><b>Lectura para el diseño.</b> Todas las curvas pasan por <i>T</i><sub>r</sub> = 1 en <i>r</i> = √2, cualquiera que sea ζ. A la izquierda de ese punto el amortiguamiento ayuda, porque limita el pico de resonancia; a la derecha estorba, porque el amortiguador transmite fuerza proporcional a la velocidad. Un aislador se diseña entonces con <i>f</i><sub>n</sub> baja (soporte blando, δ<sub>st</sub> grande) y con el amortiguamiento mínimo que permita cruzar la resonancia durante el arranque.</div>
    <div class="takeaway" style="margin-top:10px"><b>Cómo explorar:</b> (1) con el preajuste del equipo A (<i>m</i> = 0.30 kg, <i>k</i> = 426 N/m), <i>f</i><sub>n</sub> = 6.0 Hz y δ<sub>st</sub> = 6.9 mm; a 15 Hz la plataforma recibe 0.20 del movimiento de la base. (2) En resonancia con ζ = 0.05, <i>T</i><sub>r</sub> = 10.05: el aislador amplifica diez veces. (3) En el cruce, al variar ζ el punto no se mueve. (4) El último preajuste coloca el punto en <i>r</i> = 3 con ζ = 0.05, donde <i>T</i><sub>r</sub> = 0.13; al escribir ζ = 0.5 sube a 0.37: más amortiguamiento aísla peor. (5) En desbalance rotatorio la fuerza crece con ω<sup>2</sup>, de modo que la fuerza transmitida no tiende a cero a alta velocidad: para <i>r</i> ≫ 1 vale <i>m</i><sub>0</sub><i>e</i>ω<sub>n</sub><sup>2</sup>·√(1 + (2ζ<i>r</i>)<sup>2</sup>); sin amortiguamiento tiende al valor constante <i>k</i><i>m</i><sub>0</sub><i>e</i>/<i>m</i> y con amortiguamiento crece en proporción a la velocidad de giro. (6) Para practicar: «Ocultar lecturas», calcular <i>f</i><sub>n</sub>, <i>r</i> y <i>T</i><sub>r</sub> a mano y comprobar. En vehículos de lanzamiento la misma curva decide el montaje de los equipos: el aislador se elige para que las frecuencias dominantes del ambiente queden por encima de √2 <i>f</i><sub>n</sub>. Referencias: Rao, <i>Mechanical Vibrations</i>, 5.ª ed., secs. 3.6, 3.7 y 9.10; Inman, <i>Engineering Vibration</i>, 4.ª ed., secs. 2.4, 2.5 y 5.2; Den Hartog, <i>Mechanical Vibrations</i>, 4.ª ed., cap. 2.</div>
  </div>
"""
script = LIB + r"""
let S={m:0.30,k:426,z:0.05,f:15,Y:1,F0:1,m0:5,e:10,R:80,modo:'base'};
const UN={m:' kg',k:' N/m',z:'',f:' Hz',Y:' mm',F0:' N',m0:' g',e:' mm',R:' %'};
const Den=(r,z)=>Math.sqrt((1-r*r)*(1-r*r)+(2*z*r)*(2*z*r));
const Tr=(r,z)=>Math.sqrt(1+(2*z*r)*(2*z*r))/Den(r,z);
function rReq(Tq,z){ // raíz de Tr(r)=Tq en r>√2 (Tr decrece de 1 a 0); bisección
  let a=Math.SQRT2, b=1e4; if(Tr(b,z)>Tq) return NaN; for(let i=0;i<200;i++){ const c=0.5*(a+b); (Tr(c,z)>Tq)?a=c:b=c; } return 0.5*(a+b); }
function calc(){
  const wn=Math.sqrt(S.k/S.m), fn=wn/(2*Math.PI), r=S.f/fn, w=2*Math.PI*S.f, D=Den(r,S.z), T=Tr(r,S.z);
  const fase=Math.atan2(2*S.z*r*r*r, 1-r*r+(2*S.z*r)*(2*S.z*r));
  const rp=Math.sqrt(Math.sqrt(1+8*S.z*S.z)-1)/(2*S.z), Tmax=Tr(rp,S.z);
  let X, FT, F0;
  if(S.modo==='base'){ X=T*S.Y*1e-3; F0=null; FT=S.k*S.Y*1e-3*r*r*T; }   // fuerza sobre la base = m·ω²·X
  else if(S.modo==='fuerza'){ F0=S.F0; X=(F0/S.k)/D; FT=T*F0; }
  else { F0=S.m0*1e-3*S.e*1e-3*w*w; X=(F0/S.k)/D; FT=T*F0; }
  const Tq=1-S.R/100, rq=rReq(Tq,S.z), fnq=S.f/rq, dq=9.80665/Math.pow(2*Math.PI*fnq,2);
  return {wn,fn,r,w,D,T,fase,rp,Tmax,X,FT,F0,acc:w*w*X,dst:9.80665/(wn*wn),rq,fnq,dq,kq:S.m*Math.pow(2*Math.PI*fnq,2), rq0:Math.sqrt((2-S.R/100)/(1-S.R/100))};
}
function dibujar(){
  const q=calc();
  let g=lienzo($('ct'),400), e=ejes(g,{},{x0:0.1,x1:10,y0:0.01,y1:100,logx:true,logy:true,xl:'r = f / f_n',yl:S.modo==='desb'?'T_r  y  mX/(m_0 e)':'T_r',tit:'Transmisibilidad T_r(r)  ·  ζ = '+S.z});
  const c=g.c; c.fillStyle='rgba(46,125,70,.07)'; c.fillRect(e.X(Math.SQRT2),e.Y(1),e.px+e.w-e.X(Math.SQRT2),e.py+e.h-e.Y(1));
  c.fillStyle=GREEN; c.font='bold 11px Arial'; c.textAlign='right'; c.textBaseline='bottom'; c.fillText('zona de aislamiento: T_r < 1',e.px+e.w-6,e.py+e.h-6);
  [0.01,0.1,0.2,0.5,1].forEach(z=>funcion(e,r=>Tr(r,z),'#9AA7BF',1,[2,3]));
  hline(e,1,GREY,[2,3]); vline(e,Math.SQRT2,GREEN,[5,4],'r = √2'); vline(e,1,GREY,[2,3],'r = 1',16);
  if(S.modo==='desb') funcion(e,r=>r*r/Den(r,S.z),ORANGE,1.6);
  funcion(e,r=>Tr(r,S.z),STEEL,2.4);
  if(isFinite(q.rq)) { punto(e,q.rq,1-S.R/100,GREEN,4); }
  punto(e,Math.min(10,Math.max(0.1,q.r)),q.T,RED,5.5);
  c.fillStyle=RED; c.font='bold 11px Arial'; c.textAlign=q.r>4?'right':'left'; c.textBaseline='bottom'; c.fillText('T_r = '+q.T.toPrecision(3),e.X(Math.min(10,Math.max(0.1,q.r)))+(q.r>4?-8:8),e.Y(q.T)-6);
  // ----- tiempo: tres periodos, entrada y salida normalizadas con la amplitud de entrada
  g=lienzo($('cx'),230); const A=Math.max(1.05,q.T*1.1), ent=S.modo==='base'?'y(t)/Y':'F(t)/F_0', sal=S.modo==='base'?'x(t)/Y':'F_T(t)/F_0';
  e=ejes(g,{},{x0:0,x1:3,y0:-A,y1:A,yl:'salida / entrada',xl:'t / T  (periodos de la excitación)',tit:'Entrada '+ent+' (gris) y salida '+sal+' (azul)  ·  desfase '+(q.fase*180/Math.PI).toFixed(1)+'°',ny:4});
  funcion(e,t=>Math.sin(2*Math.PI*t),GREY,1.4,[4,3]); funcion(e,t=>q.T*Math.sin(2*Math.PI*t-q.fase),STEEL,2);
  // ----- lecturas
  const p3=v=>(+v).toPrecision(3);
  $('ofn').textContent=q.fn.toFixed(2)+' Hz'; $('odst').textContent=(q.dst*1e3).toPrecision(3)+' mm'; $('or').textContent=q.r.toFixed(3);
  $('oT').textContent=q.T<0.001?num(q.T):q.T.toFixed(3); const dB=20*Math.log10(q.T); $('odB').textContent=(Math.abs(dB)<0.05?'0.0':dB.toFixed(1).replace('-','−'))+' dB';
  $('oais').textContent=q.T<0.9995?(q.T<0.001?'> 99.9 %':(100*(1-q.T)).toFixed(1)+' %'):q.T<1.0005?'ninguno (T_r = 1)':'amplifica ×'+q.T.toFixed(2); $('oais').parentNode.classList.toggle('al',q.T>=1.0005);
  $('kfase').textContent=S.modo==='base'?'Desfase de x respecto de y':'Desfase de F_T respecto de F_0'; $('ldesb').style.setProperty('display',S.modo==='desb'?'inline-block':'none','important');
  $('ofase').textContent=(q.fase*180/Math.PI).toFixed(1)+'°'; $('oX').textContent=ing(q.X,'m'); $('oacc').textContent=p3(q.acc)+' m/s^2 = '+p3(q.acc/9.80665)+' g';
  $('oFT').textContent=p3(q.FT)+' N'+(q.F0!==null?' de '+p3(q.F0)+' N':'');
  $('opk').textContent=q.Tmax.toFixed(2)+' en '+(q.rp*q.fn).toFixed(2)+' Hz';
  $('oreq').textContent=isFinite(q.rq)?(+q.fnq.toPrecision(3))+' Hz':'…';
  $('oreq2').textContent=isFinite(q.rq)?'Para aislar '+S.R+' % a '+S.f+' Hz con ζ = '+S.z+': r ≥ '+q.rq.toFixed(3)+' (sin amortiguamiento bastaría r = '+q.rq0.toFixed(3)+'), es decir k ≤ '+ing(q.kq,'N/m')+' con la masa actual y δ_st ≥ '+ing(q.dq,'m')+'.':'';
  $('nmodo').textContent={base:'La base se mueve con y(t) = Y sen ωt (piso, estructura del vehículo); se lee el movimiento del equipo.',fuerza:'Sobre el equipo actúa F(t) = F_0 sen ωt; se lee la fuerza que el aislador pasa a la base fija.',desb:'Un rotor con masa excéntrica m_0 a una distancia e gira a ω: la fuerza de excitación crece con ω^2.'}[S.modo];
}
function modo(){ $('gY').style.display=S.modo==='base'?'':'none'; $('gF').style.display=S.modo==='fuerza'?'':'none'; $('gD').style.display=S.modo==='desb'?'':'none';
  document.querySelectorAll('[data-modo]').forEach(b=>b.classList.toggle('on',b.dataset.modo===S.modo)); dibujar(); }
document.querySelectorAll('[data-modo]').forEach(b=>b.addEventListener('click',()=>{ S.modo=b.dataset.modo; modo(); }));
liga(S,UN,dibujar); practica('pra');
const fnA=Math.sqrt(426/0.30)/(2*Math.PI);
const B0={m:0.30,k:426,z:0.05,Y:1,F0:1,m0:5,e:10,R:80,modo:'base'};
const PRE={A:{...B0,f:15}, R:{...B0,f:+fnA.toFixed(2)}, C:{...B0,f:+(fnA*Math.SQRT2).toFixed(2)}, Z:{...B0,f:+(3*fnA).toFixed(2)}};
document.querySelectorAll('[data-pre]').forEach(b=>b.addEventListener('click',()=>{ pon(S,UN,PRE[b.dataset.pre],modo); }));
window.addEventListener('resize',dibujar);
window.__tr={S,calc,Tr,rReq};
modo();
"""
pagina("transmisibilidad_interactivo.html", "Transmisibilidad y aislamiento de vibraciones", "Vibraciones · Pilar 13 · U6",
       "Al variar la masa, la rigidez del aislador, el amortiguamiento y la frecuencia de excitación se observa cuánto movimiento o cuánta fuerza se transmite, y desde qué frecuencia hay aislamiento",
       cuerpo, script, "Explorador didáctico de transmisibilidad, aislamiento y desbalance rotatorio · material de apoyo del curso de Vibraciones · funciona sin conexión (un solo archivo).")
