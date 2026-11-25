#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera proy_bobina.html · Apoyo a los proyectos · Bobina e imán: fuerza (actuador) y fem (sensor) según la geometría.
Modelo: bobina y cilindro imantado coaxiales; el imán se representa por su corriente superficial equivalente
(B_r t / μ0) y el acoplamiento sale de la inductancia mutua entre espiras coaxiales (integrales elípticas).
Uso: python3 gen_proy_bobina.py CARPETA"""
from base_pag import *

cuerpo = f"""
  <div class="intro full">
    <b>¿Qué resuelve?</b> Una bobina frente a un imán sirve para dos cosas: como <b>actuador</b>, empuja o jala el imán cuando circula corriente; como <b>sensor</b>, produce una tensión cuando el imán se mueve. Las dos usan la misma constante de acoplamiento <i>K</i> = d<i>Φ</i>/d<i>z</i> (en N/A, que es lo mismo que V·s/m): la fuerza es <i>F</i> = <i>K I</i> y la tensión inducida es <i>e</i> = <i>K v</i>. La página calcula <i>K</i> a partir de la geometría de la bobina (diámetro, largo, calibre AWG y número de vueltas) y del imán (diámetro, espesor y remanencia), junto con la resistencia, la corriente, la potencia que se disipa y el campo en el centro de la bobina.
  </div>
  <div class="card">
    <canvas id="ck" width="760" height="330" aria-label="Constante de acoplamiento y fuerza contra la separación"></canvas>
    <canvas id="cg" width="760" height="210" style="margin-top:8px" aria-label="Esquema de la bobina y el imán a escala"></canvas>
    <div class="legend">
      <span><i class="sw" style="border-top-color:var(--steel)"></i> fuerza con la corriente actual</span>
      <span><i class="sw" style="border-top-color:var(--orange);border-top-style:dashed"></i> peso del imán</span>
      <span><i class="sw" style="border-top-color:var(--red)"></i> separación elegida</span>
    </div>
  </div>
  <div class="card">
    <h2>Controles</h2>
    <div class="btns"><button class="btn" data-pre="C">Equipo C: bobina de 200 vueltas como sensor</button><button class="btn" data-pre="E">Excitador: 500 vueltas, 1 A</button></div>
    <div class="grp"><div class="t">Bobina</div>
      {fila("Diámetro interior", "di", 3, 60, 0.5, 20, "mm")}
      {fila("Largo del devanado", "lb", 2, 60, 0.5, 10, "mm")}
      {fila("Calibre del alambre", "awg", 20, 38, 1, 30, "AWG")}
      {fila("Número de vueltas <i>N</i>", "N", 10, 3000, 1, 200)}
    </div>
    <div class="grp"><div class="t">Fuente (modo actuador)</div>
      {fila("Tensión de la fuente", "V", 0, 30, 0.1, 5, "V")}
      {fila("Límite de corriente", "Il", 0.01, 5, 0.01, 1, "A")}
    </div>
    <div class="grp"><div class="t">Imán (coaxial, frente a una cara de la bobina)</div>
      {fila("Diámetro del imán", "dm", 2, 50, 0.5, 28, "mm")}
      {fila("Espesor del imán", "tm", 0.5, 30, 0.5, 5, "mm")}
      {fila("Remanencia <i>B</i><sub>r</sub>", "Br", 0.2, 1.45, 0.01, 1.25, "T")}
      {fila("Separación cara a cara <i>s</i>", "s", 0.2, 40, 0.1, 5, "mm")}
      {fila("Velocidad del imán (modo sensor)", "v", 0, 3, 0.01, 0.44, "m/s")}
    </div>
    <div class="tiles t3" style="margin-top:10px">
      {tile("Vueltas por capa · capas", "ocap")}{tile("Diámetro exterior", "oext")}{tile("Longitud de alambre", "olong")}
      {tile("Resistencia <i>R</i>", "oR")}{tile("Corriente <i>I</i>", "oI")}{tile("Potencia disipada", "oP")}
      {tile("Campo en el centro de la bobina", "oB")}{tile("Acoplamiento <i>K</i> en <i>s</i>", "oK", "hl")}{tile("Fuerza sobre el imán", "oF", "hl")}
      {tile("Fuerza / peso del imán", "oFw")}{tile("Tensión inducida <i>e</i> = <i>Kv</i>", "oe", "hl")}{tile("<i>K</i> máximo y dónde", "oKm")}
    </div>
    <div class="nota" id="olect"></div>
  </div>
  <div class="card full">
    <h2>Las fórmulas en pantalla</h2>
    <div class="two"><div>
    {eq("1 · Alambre y resistencia", M(r"d_{\mathrm{Cu}}=0.127\ \mathrm{mm}\times92^{(36-n)/39},\qquad R=\rho_{\mathrm{Cu}}\,\frac{L_w}{\pi d_{\mathrm{Cu}}^2/4}") + M(r"\rho_{\mathrm{Cu}}=1.72\times10^{-8}\ \Omega\,\mathrm{m}") + nota("n es el calibre AWG; L<sub>w</sub> es la longitud total del alambre, suma del perímetro medio de cada capa; con esmalte, el diámetro se estima en 1.1 veces el del cobre (aproximado)"))}
    {eq("2 · Campo en el eje de la bobina", M(r"B(z)=\sum_{\text{espiras}}\frac{\mu_0 I\,a^2}{2\left(a^2+z^2\right)^{3/2}}") + nota("suma sobre cada espira de radio a; en el centro de una bobina larga y delgada tiende a μ<sub>0</sub>NI/ℓ<sub>b</sub>"))}
    {eq("3 · Fuerza y tensión inducida", M(r"K=\frac{\partial\Phi_{\text{imán}}}{\partial z},\qquad F=K\,I,\qquad e=K\,v") + nota("Φ es el flujo del imán a través de las N espiras; la misma K da la fuerza (actuador) y la tensión (sensor), por reciprocidad"))}
    </div><div>
    {eq("4 · El imán como corriente superficial", M(r"I_m=\frac{B_r\,t}{\mu_0},\qquad K=\frac{I_m}{n_m}\sum_{i,j}\frac{\partial M_{ij}}{\partial z}") + nota("un cilindro imantado uniformemente equivale a una bobina de su mismo tamaño con corriente total B<sub>r</sub>t/μ<sub>0</sub>; se reparte en n<sub>m</sub> espiras"))}
    {eq("5 · Inductancia mutua de dos espiras coaxiales", M(r"M=\mu_0\sqrt{ab}\left[\left(\frac{2}{k}-k\right)K(k)-\frac{2}{k}E(k)\right],\qquad k^2=\frac{4ab}{(a+b)^2+d^2}") + nota("a y b son los radios, d la separación axial; K y E son las integrales elípticas completas, calculadas con la media aritmético-geométrica"))}
    </div></div>
    <div class="intro" style="margin-top:12px"><b>Hipótesis y límites.</b> Bobina e imán coaxiales, sin núcleo de hierro y sin piezas ferromagnéticas cerca (una placa de acero cambia el campo); imán uniformemente imantado con la remanencia de su grado (N35 ≈ 1.2 T, N42 ≈ 1.3 T, N52 ≈ 1.45 T; valores típicos, el del fabricante puede variar); devanado ordenado por capas. Si el imán no está centrado en el eje, <i>K</i> baja. En modo sensor con el osciloscopio no circula corriente apreciable, así que la bobina no frena al imán; si se cierra en corto o con una resistencia baja, sí lo frena: es otra forma de amortiguamiento magnético. La potencia disipada calienta la bobina: el esmalte típico soporta del orden de 130 a 180 °C, pero el carrete de PLA se ablanda cerca de 60 °C, así que en régimen continuo conviene mantener la potencia baja y medir la temperatura. Referencias: Jackson, <i>Classical Electrodynamics</i>, 3.ª ed., Wiley, 1999, sec. 5.5 (espira circular) y sec. 5.8 (imantación y corriente equivalente); Griffiths, <i>Introduction to Electrodynamics</i>, 4.ª ed., Cambridge University Press, 2017, cap. 6 y 7.</div>
  </div>
"""
script = LIB + r"""
let S={di:20,lb:10,awg:30,N:200,V:5,Il:1,dm:28,tm:5,Br:1.25,s:5,v:0.44};
const UN={di:' mm',lb:' mm',awg:'',N:'',V:' V',Il:' A',dm:' mm',tm:' mm',Br:' T',s:' mm',v:' m/s'}, MU0=4e-7*Math.PI, RHO=1.72e-8, G0=9.80665;
function KE(k){ // integrales elípticas completas K(k), E(k) por la media aritmético-geométrica
  let a=1, b=Math.sqrt(1-k*k), c=k, sum=0.5*c*c, p=1; for(let i=0;i<40;i++){ const an=(a+b)/2, bn=Math.sqrt(a*b); c=(a-b)/2; a=an; b=bn; p*=2; sum+=p*c*c/2; if(Math.abs(c)<1e-16) break; }
  const K=Math.PI/(2*a); return [K, K*(1-sum)]; }
function mutua(a,b,d){ const k2=4*a*b/((a+b)**2+d*d), k=Math.sqrt(Math.min(k2,1-1e-15)); const [K,E]=KE(k); return MU0*Math.sqrt(a*b)*((2/k-k)*K-2/k*E); }
function bobina(){ const dcu=0.127e-3*Math.pow(92,(36-S.awg)/39), dex=1.1*dcu, lb=S.lb*1e-3, tpl=Math.max(1,Math.floor(lb/dex)), cap=Math.ceil(S.N/tpl), ri=S.di/2*1e-3;
  const esp=[]; let n=0, largo=0; for(let j=0;j<cap&&n<S.N;j++){ const r=ri+(j+0.5)*dex, enCapa=Math.min(tpl,S.N-n); for(let i=0;i<enCapa;i++){ esp.push([r,(i+0.5)*lb/enCapa]); } largo+=enCapa*2*Math.PI*r; n+=enCapa; }
  const R=RHO*largo/(Math.PI*dcu*dcu/4), I=Math.min(S.V/R,S.Il), P=I*I*R, rext=ri+cap*dex;
  let Bc=0; esp.forEach(e=>{ const z=e[1]-lb/2; Bc+=MU0*1*e[0]*e[0]/(2*Math.pow(e[0]*e[0]+z*z,1.5)); }); // por ampere
  return {dcu,dex,tpl,cap,esp,largo,R,I,P,rext,Bc:Bc*I,limitada:S.V/R>S.Il}; }
// K(s): s = separación entre la cara superior de la bobina (z = lb) y la cara inferior del imán
function acople(esp,s){ const nm=8, am=S.dm/2*1e-3, tm=S.tm*1e-3, lb=S.lb*1e-3, Im=S.Br*tm/MU0/nm, h=2e-6; let K=0;
  for(let j=0;j<nm;j++){ const zm=lb+s+(j+0.5)*tm/nm; for(const e of esp){ const d=zm-e[1]; K+=(mutua(e[0],am,d+h)-mutua(e[0],am,d-h))/(2*h); } } return Math.abs(K*Im); }
function calc(){ const b=bobina(), s=S.s*1e-3, K=acople(b.esp,s), mim=7500*Math.PI*(S.dm/2e3)**2*S.tm*1e-3;
  const xs=[]; for(let i=0;i<=40;i++){ const x=0.2e-3*Math.pow(200,i/40); xs.push([x,acople(b.esp,x)]); } let km=xs[0]; xs.forEach(p=>{ if(p[1]>km[1]) km=p; });
  return {b,K,F:K*b.I,e:K*S.v,mim,peso:mim*G0,xs,km}; }
let Q=null;
function dibujar(){
  const q=calc(); Q=q; const b=q.b; const g=lienzo($('ck'),330); const Fmax=Math.max(...q.xs.map(p=>p[1]*b.I),q.peso)*1.15||1;
  const e=ejes(g,{mL:62,mR:70},{x0:0,x1:40,y0:0,y1:Fmax,xl:'separación cara a cara s (mm)',yl:'fuerza (N)',tit:'Fuerza sobre el imán con I = '+(+b.I.toPrecision(3))+' A (eje derecho: K en N/A)',nx:8,ny:5});
  curva(e,q.xs.map(p=>[p[0]*1e3,p[1]*b.I]),STEEL,2.4); hline(e,q.peso,ORANGE,[6,4],'peso del imán '+(+q.peso.toPrecision(2))+' N'); vline(e,S.s,RED,[3,3]); punto(e,S.s,q.F,RED,5);
  const c=g.c; c.fillStyle=GREY; c.font='11px Arial'; c.textAlign='left'; c.textBaseline='middle'; [0.25,0.5,0.75,1].forEach(f=>{ const y=e.py+e.h*(1-f); c.fillText((+(f*Fmax/Math.max(b.I,1e-9)).toPrecision(2))+' N/A',e.px+e.w+6,y); });
  // esquema a escala
  const g2=lienzo($('cg'),210), c2=g2.c, W=g2.W, lb=S.lb, sc=Math.min(150/(lb+S.s+S.tm+4), (W-80)/(2*Math.max(b.rext*1e3,S.dm/2)+10)), cx=W/2, yb=190, mm=v=>v*sc;
  c2.fillStyle=NAVY; c2.font='bold 12px Arial'; c2.textAlign='left'; c2.textBaseline='top'; c2.fillText('Corte a escala (eje vertical: eje de la bobina)',8,4);
  c2.fillStyle='rgba(197,90,17,.35)'; [[-1],[1]].forEach(([sg])=>{ const x0=cx+sg*mm(S.di/2), x1=cx+sg*mm(b.rext*1e3); c2.fillRect(Math.min(x0,x1),yb-mm(lb),Math.abs(x1-x0),mm(lb)); });
  c2.strokeStyle=GREY; c2.setLineDash([4,3]); c2.beginPath(); c2.moveTo(cx,20); c2.lineTo(cx,yb+6); c2.stroke(); c2.setLineDash([]);
  const ym=yb-mm(lb+S.s); c2.fillStyle='#5B6B86'; c2.fillRect(cx-mm(S.dm/2),ym-mm(S.tm),mm(S.dm),mm(S.tm)); c2.fillStyle='#fff'; c2.font='bold 11px Arial'; c2.textAlign='center'; c2.textBaseline='middle'; if(mm(S.tm)>12) c2.fillText('imán',cx,ym-mm(S.tm)/2);
  c2.fillStyle=ORANGE; c2.font='11px Arial'; c2.textAlign='left'; c2.fillText('bobina: '+S.N+' vueltas, '+b.cap+' capa'+(b.cap>1?'s':''),cx+mm(b.rext*1e3)+8,yb-mm(lb)/2);
  c2.fillStyle=RED; c2.fillText('s = '+S.s+' mm',cx+mm(S.dm/2)+8,ym+mm(S.s)/2);
  // lecturas
  const f3=v=>(+v.toPrecision(3));
  $('ocap').textContent=b.tpl+' · '+b.cap; $('oext').textContent=f3(2*b.rext*1e3)+' mm'; $('olong').textContent=f3(b.largo)+' m'; $('oR').textContent=f3(b.R)+' Ω';
  $('oI').textContent=f3(b.I)+' A'+(b.limitada?' (límite)':''); $('oP').textContent=f3(b.P)+' W'; $('oP').parentNode.classList.toggle('al',b.P>2);
  $('oB').textContent=ing(b.Bc,'T'); $('oK').textContent=f3(q.K)+' N/A'; $('oF').textContent=ing(q.F,'N')+' ('+f3(q.F/G0*1e3)+' g)'; $('oFw').textContent=f3(q.F/q.peso);
  $('oe').textContent=ing(q.e,'V'); $('oKm').textContent=f3(q.km[1])+' N/A a '+f3(q.km[0]*1e3)+' mm';
  let t=[]; if(b.P>2) t.push('La bobina disipa '+f3(b.P)+' W: se calentará; usar pulsos cortos, bajar la tensión o limitar la corriente.');
  if(b.limitada) t.push('La fuente trabaja en límite de corriente: '+f3(b.I)+' A.');
  t.push('Como sensor, un imán que pasa a '+S.v+' m/s a '+S.s+' mm induce unos '+ing(q.e,'V')+' de pico: '+(q.e<1e-3?'señal pequeña; acercar el imán, añadir vueltas o usar la escala más sensible del osciloscopio.':'suficiente para el osciloscopio.'));
  t.push('El acoplamiento es máximo a '+f3(q.km[0]*1e3)+' mm de separación; más cerca baja porque el imán queda frente al centro hueco de la bobina.');
  $('olect').textContent=t.join(' ');
}
liga(S,UN,dibujar);
const PRE={C:{di:20,lb:10,awg:30,N:200,V:0,Il:1,dm:28,tm:5,Br:1.25,s:5,v:0.44}, E:{di:30,lb:15,awg:26,N:500,V:12,Il:1,dm:28,tm:5,Br:1.25,s:3,v:0.1}};
document.querySelectorAll('[data-pre]').forEach(bt=>bt.addEventListener('click',()=>pon(S,UN,PRE[bt.dataset.pre],dibujar)));
window.addEventListener('resize',dibujar);
window.__bo={S,calc,mutua,KE,bobina,acople};
dibujar();
"""
pagina("proy_bobina.html", "Bobina e imán: fuerza y tensión inducida", "Vibraciones · Apoyo a los proyectos",
       "A partir de la geometría de la bobina y del imán se calculan la resistencia, la corriente, la fuerza que la bobina ejerce sobre el imán y la tensión que induce el imán al moverse",
       cuerpo, script, "Apoyo a los proyectos del curso de Vibraciones: bobina como actuador y como sensor · funciona sin conexión (un solo archivo).")
