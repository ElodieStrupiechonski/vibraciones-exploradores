#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera choque_interactivo.html · Pilar 16 · Ensayo de choque y espectro de respuesta (U7, tema 7.4).
Uso: python3 gen_choque.py CARPETA"""
from base_pag import *

cuerpo = f"""
  <div class="intro full">
    <b>¿Qué muestra?</b> En un ensayo de choque la mesa aplica al equipo un pulso de aceleración breve: un semiseno, un diente de sierra o un pulso rectangular de amplitud <i>A</i> y duración <i>D</i>. Cada componente del equipo responde como un oscilador de frecuencia natural <i>f</i><sub>n</sub>: unos apenas se enteran, otros reciben más aceleración que la aplicada. El <b>espectro de respuesta al choque</b> (SRS, por sus siglas en inglés) resume ese efecto: es la aceleración máxima de un oscilador de un grado de libertad en función de su frecuencia natural, para un amortiguamiento fijo (por convención, <i>Q</i> = 10). Arriba, el pulso y la respuesta en el tiempo de un componente; abajo, el espectro completo.
  </div>

  <div class="card">
    <canvas id="ct" width="760" height="300" aria-label="Pulso aplicado y respuesta del componente en el tiempo"></canvas>
    <canvas id="cs" width="760" height="360" style="margin-top:10px" aria-label="Espectro de respuesta al choque"></canvas>
    <div class="legend">
      <span><i class="sw" style="border-top-color:var(--grey)"></i> pulso de la base</span>
      <span><i class="sw" style="border-top-color:var(--steel)"></i> aceleración del componente y SRS</span>
      <span><i class="sw" style="border-top-color:var(--orange);border-top-style:dashed"></i> asíntota impulsiva 2π<i>f</i><sub>n</sub>Δ<i>v</i></span>
      <span><i class="sw" style="border-top-color:var(--green);border-top-style:dashed"></i> amplitud del pulso <i>A</i></span>
      <span><i class="sw" style="border-top-color:var(--red)"></i> componente elegido</span>
    </div>
  </div>

  <div class="card">
    <h2>Controles</h2>
    <div class="grp"><div class="t">Pulso de la mesa</div>
      <div class="btns"><button class="btn on" data-p="sen">Semiseno</button><button class="btn" data-p="sie">Diente de sierra</button><button class="btn" data-p="rec">Rectangular</button></div>
      {fila("Amplitud <i>A</i>", "A", 1, 200, 1, 20, "g")}
      {fila("Duración <i>D</i>", "D", 0.5, 50, 0.5, 11, "ms")}
    </div>
    <div class="grp"><div class="t">Componente (oscilador de 1 GDL)</div>
      {fila("Frecuencia natural <i>f</i><sub>n</sub>", "fn", 2, 2000, 1, 73, "Hz")}
      {fila("Factor de calidad <i>Q</i>", "Q", 2, 50, 0.5, 10)}
    </div>
    <div class="btns">
      <button class="btn" data-pre="C">Choque clásico: 20 g, 11 ms</button><button class="btn" data-pre="B">Componente blando</button><button class="btn" data-pre="R">Componente rígido</button><button class="btn" data-pre="P">El peor caso</button>
      <button class="btn" id="pra">Ocultar lecturas (modo práctica)</button>
    </div>
    <div class="tiles t3" style="margin-top:10px">
      {tile("Producto <i>f</i><sub>n</sub><i>D</i>", "ofd")}{tile("Aceleración máxima del componente", "opk", "hl")}{tile("Amplificación respecto de <i>A</i>", "oam", "hl")}
      {tile("El máximo ocurre", "odon")}{tile("Cambio de velocidad Δ<i>v</i>", "odv")}{tile("Desplazamiento relativo máximo", "oz")}
      {tile("Factor de amortiguamiento ζ", "oze")}{tile("Máximo del SRS", "osm")}{tile("En la frecuencia", "ofm")}
    </div>
    <div class="nota" id="olect"></div>
  </div>

  <div class="card full">
    <h2>Las fórmulas en pantalla</h2>
    <div class="two"><div>
    {eq("1 · Componente sobre una base que se acelera", M(r"\ddot z+2\zeta\omega_n\,\dot z+\omega_n^2\,z=-a_b(t),\qquad a(t)=-\left(2\zeta\omega_n\,\dot z+\omega_n^2\,z\right)") + nota("<i>z</i> es el desplazamiento del componente relativo a la base y <i>a</i> su aceleración absoluta; ζ = 1/(2<i>Q</i>)"))}
    {eq("2 · Pulsos clásicos (0 ≤ <i>t</i> ≤ <i>D</i>)", M(r"\text{semiseno:}\;\;A\,\mathrm{sen}\frac{\pi t}{D}\qquad \text{sierra:}\;\;A\,\frac{t}{D}\qquad \text{rectangular:}\;\;A"))}
    {eq("3 · Cambio de velocidad: el área del pulso", M(r"\Delta v=\int_0^D a_b\,dt") + M(r"\frac{2}{\pi}AD\ \ \text{(semiseno)},\qquad \frac{1}{2}AD\ \ \text{(sierra)},\qquad AD\ \ \text{(rectangular)}"))}
    </div><div>
    {eq("4 · Espectro de respuesta al choque", M(r"\mathrm{SRS}(f_n)=\max_t\,|a(t;\,f_n,\,Q)|") + nota("se calcula un oscilador por cada frecuencia; aquí se integra la ecuación 1 con un método de Runge-Kutta de cuarto orden"))}
    {eq("5 · Componente blando: el pulso actúa como impulso", M(r"f_nD\ll1:\qquad \mathrm{SRS}\approx\omega_n\,\Delta v=2\pi f_n\,\Delta v") + nota("solo importa el área del pulso, no su forma; el componente queda aislado del choque"))}
    {eq("6 · Componente rígido: sigue a la base", M(r"f_nD\gg1:\qquad \mathrm{SRS}\to A\ \ \text{(semiseno y sierra)},\qquad z_{\text{máx}}\approx\frac{\mathrm{SRS}}{\omega_n^2}") + nota("el pulso rectangular es la excepción: su frente súbito deja el espectro cerca de 2<i>A</i>"))}
    </div></div>
    <div class="intro" style="margin-top:12px"><b>Las tres pruebas del tema 7.4.</b> La <b>resistencia</b> de un equipo se demuestra con tres tipos de ensayo: (a) <b>senoidal</b>, por barrido o con permanencia en una resonancia, que busca las frecuencias naturales y somete a fatiga un modo a la vez (exploradores de respuesta forzada y de fatiga); (b) <b>aleatorio</b>, definido por una densidad espectral, que excita todos los modos a la vez (explorador del espectro a la carga de diseño); (c) <b>de choque</b>, definido por un pulso o directamente por su SRS, que representa separaciones pirotécnicas, aterrizajes y caídas (este explorador). El <b>diagnóstico</b> usa las mismas herramientas en sentido inverso: se repite un barrido de baja amplitud antes y después de cada ensayo, y un corrimiento de una frecuencia natural de más de unos puntos porcentuales indica que algo se aflojó o se agrietó, porque <i>f</i><sub>n</sub> es proporcional a √<i>k</i>.</div>
    <div class="takeaway" style="margin-top:10px"><b>Cómo explorar:</b> (1) con el preajuste del choque clásico (semiseno de 20 g y 11 ms) y un componente de 73 Hz, el producto <i>f</i><sub>n</sub><i>D</i> es 0.80 y el componente recibe 33 g: 1.65 veces lo aplicado. (2) «Componente blando» (5 Hz): recibe 4.1 g; el soporte lo aísla y la lectura queda cerca de la asíntota 2π<i>f</i><sub>n</sub>Δ<i>v</i> = 4.4 g (la diferencia se debe al amortiguamiento). (3) «Componente rígido» (1000 Hz): recibe 20 g, lo mismo que la mesa. (4) «El peor caso» coloca el componente en el máximo del espectro. (5) Al cambiar a diente de sierra con la misma amplitud, el máximo baja a 1.19 <i>A</i> y el espectro queda más plano, razón por la que ese pulso se prefiere para ensayar. (6) Con el pulso rectangular el espectro no regresa a <i>A</i>: se mantiene en 1.86 <i>A</i> con <i>Q</i> = 10. (7) Al bajar <i>Q</i> el máximo disminuye, pero poco: en un choque el amortiguamiento ayuda mucho menos que en una resonancia sostenida. Los valores de 20 g y 11 ms son del orden de los que piden las normas de ensayo para equipo de a bordo; el valor exigible debe leerse en la norma aplicable (véase «Dónde consultar las normas»). Referencias: Rao, <i>Mechanical Vibrations</i>, 5.ª ed., sec. 4.6 (espectro de respuesta); Lalanne, <i>Mechanical Vibration and Shock Analysis</i>, vol. 2: <i>Mechanical Shock</i>, 3.ª ed., Wiley-ISTE, 2014; Piersol y Paez (eds.), <i>Harris' Shock and Vibration Handbook</i>, 6.ª ed., McGraw-Hill, 2010.</div>
  </div>
"""
script = LIB + r"""
let S={A:20,D:11,fn:73,Q:10,p:'sen'};
const UN={A:' g',D:' ms',fn:' Hz',Q:''}, G0=9.80665, TP=2*Math.PI;
function pulso(u){ if(u<0||u>1) return 0; return S.p==='sen'?Math.sin(Math.PI*u):S.p==='sie'?u:1; }   // forma del pulso, u = t/D
function area(){ return S.p==='sen'?2/Math.PI:S.p==='sie'?0.5:1; }                                     // Δv/(A·D)
// respuesta de un oscilador (fn, Q) al pulso de amplitud 1 y duración D (s); devuelve el máximo y, si se pide, la traza
function resp(fn,Q,D,traza){
  const w=TP*fn, z=1/(2*Q), T=1/fn, tf=D+(traza?4*T:1.3*T), dt=Math.min(D/(traza?400:120),T/(traza?200:60)), n=Math.min(60000,Math.ceil(tf/dt)), h=tf/n;
  let x=0, v=0, mx=0, tm=0, zm=0; const pts=traza?[]:null, f=(t,x,v)=>-pulso(t/D)-2*z*w*v-w*w*x;
  for(let i=0;i<=n;i++){ const t=i*h, a=-(2*z*w*v+w*w*x); if(Math.abs(a)>mx){ mx=Math.abs(a); tm=t; } zm=Math.max(zm,Math.abs(x)); if(traza) pts.push([t,a]);
    const k1x=v, k1v=f(t,x,v), k2x=v+h/2*k1v, k2v=f(t+h/2,x+h/2*k1x,v+h/2*k1v), k3x=v+h/2*k2v, k3v=f(t+h/2,x+h/2*k2x,v+h/2*k2v), k4x=v+h*k3v, k4v=f(t+h,x+h*k3x,v+h*k3v);
    x+=h/6*(k1x+2*k2x+2*k3x+k4x); v+=h/6*(k1v+2*k2v+2*k3v+k4v); }
  return {mx,tm,zm,pts,tf};
}
const FR=[]; for(let i=0;i<=72;i++) FR.push(2*Math.pow(1500,i/72));       // 2 Hz a 3 kHz
let SR=null, clave='';
function espectro(){ const k=[S.D,S.Q,S.p].join('|'); if(k!==clave){ clave=k; SR=FR.map(f=>resp(f,S.Q,S.D*1e-3,false).mx); } return SR; }
function calc(){ const D=S.D*1e-3, r=resp(S.fn,S.Q,D,true), sr=espectro(); let im=0; sr.forEach((v,i)=>{ if(v>sr[im]) im=i; });
  return {r, sr, pk:r.mx*S.A, amp:r.mx, dv:area()*S.A*G0*D, zmax:r.zm*S.A*G0, fd:S.fn*D, smax:sr[im], fmax:FR[im], prim:r.tm<=D*1.0005, tm:r.tm}; }
function dibujar(){
  const q=calc(), D=S.D*1e-3;
  let g=lienzo($('ct'),300), ym=Math.max(1.1,q.amp*1.12)*S.A, e=ejes(g,{},{x0:0,x1:q.r.tf*1e3,y0:-ym,y1:ym,xl:'t (ms)',yl:'aceleración (g)',tit:'Pulso de la base y respuesta de un componente de '+S.fn+' Hz (Q = '+S.Q+')',ny:6});
  const c=g.c; c.fillStyle='rgba(91,91,91,.07)'; c.fillRect(e.X(0),e.py,e.X(S.D)-e.X(0),e.h);
  funcion(e,t=>S.A*pulso(t/S.D),GREY,2,null,600); curva(e,q.r.pts.map(p=>[p[0]*1e3,p[1]*S.A]),STEEL,2);
  hline(e,0,'#9AA7BF',[2,3]); const sg=q.r.pts.reduce((a,p)=>Math.abs(p[1])>Math.abs(a[1])?p:a,[0,0]); punto(e,sg[0]*1e3,sg[1]*S.A,RED,5);
  c.fillStyle=GREY; c.font='11px Arial'; c.textAlign='left'; c.textBaseline='bottom'; c.fillText('durante el pulso',e.X(0)+4,e.py+e.h-4); if(e.X(S.D)+90<e.px+e.w) c.fillText('después: vibración libre',e.X(S.D)+4,e.py+e.h-4);
  // espectro
  g=lienzo($('cs'),360); const y1=Math.pow(10,Math.ceil(Math.log10(Math.max(q.smax*S.A,S.A)*1.2))), y0=y1/1000;
  e=ejes(g,{},{x0:2,x1:3000,y0,y1,logx:true,logy:true,xl:'frecuencia natural del componente f_n (Hz)',yl:'aceleración máxima (g)',tit:'Espectro de respuesta al choque (máximo absoluto)  ·  Q = '+S.Q});
  const dvg=area()*S.A*D;                                         // Δv en g·s
  funcion(e,f=>TP*f*dvg,ORANGE,1.4,[6,4]); hline(e,S.A,GREEN,[6,4],'A = '+S.A+' g');
  curva(e,FR.map((f,i)=>[f,q.sr[i]*S.A]),STEEL,2.4); vline(e,1/D,GREY,[2,3],'f_n D = 1');
  punto(e,Math.min(3000,S.fn),q.pk,RED,5.5); const c2=g.c; c2.fillStyle=RED; c2.font='bold 11px Arial'; c2.textAlign=S.fn>600?'right':'left'; c2.textBaseline='top'; c2.fillText(q.pk.toPrecision(3)+' g',e.X(S.fn)+(S.fn>600?-8:8),e.Y(q.pk)+8);
  // lecturas
  const p3=v=>(+v).toPrecision(3);
  $('ofd').textContent=q.fd.toFixed(2); $('opk').textContent=p3(q.pk)+' g'; $('oam').textContent='× '+q.amp.toFixed(2); $('oam').parentNode.classList.toggle('al',q.amp>1.005);
  $('odon').textContent=q.prim?'durante el pulso':'después del pulso'; $('odv').textContent=p3(q.dv)+' m/s'; $('oz').textContent=ing(q.zmax,'m');
  $('oze').textContent=(1/(2*S.Q)).toFixed(3); $('osm').textContent=p3(q.smax*S.A)+' g  (× '+q.smax.toFixed(2)+')'; $('ofm').textContent=p3(q.fmax)+' Hz';
  $('olect').textContent=q.fd<0.2?'Componente blando frente al pulso (f_n D < 0.2): el choque actúa como un impulso y el soporte aísla.':q.fd>3?'Componente rígido frente al pulso (f_n D > 3): sigue a la base casi sin amplificar'+(S.p==='rec'?', salvo por el frente súbito del pulso rectangular.':'.'):'Zona de amplificación (f_n D entre 0.2 y 3): la duración del pulso es comparable con el periodo del componente.';
}
liga(S,UN,dibujar); practica('pra');
function forma(p){ S.p=p; document.querySelectorAll('[data-p]').forEach(b=>b.classList.toggle('on',b.dataset.p===p)); }
document.querySelectorAll('[data-p]').forEach(b=>b.addEventListener('click',()=>{ forma(b.dataset.p); dibujar(); }));
const PRE={C:{A:20,D:11,fn:73,Q:10}, B:{A:20,D:11,fn:5,Q:10}, R:{A:20,D:11,fn:1000,Q:10}};
document.querySelectorAll('[data-pre]').forEach(b=>b.addEventListener('click',()=>{ if(b.dataset.pre==='P'){ const q=calc(); pon(S,UN,{fn:Math.round(q.fmax)},dibujar); return; } forma('sen'); pon(S,UN,PRE[b.dataset.pre],dibujar); }));
window.addEventListener('resize',dibujar);
window.__ch={S,calc,resp,FR};
dibujar();
"""
pagina("choque_interactivo.html", "Ensayo de choque y espectro de respuesta", "Vibraciones · Pilar 16 · U7",
       "Al variar la forma, la amplitud y la duración del pulso se observa qué aceleración recibe cada componente según su frecuencia natural: el espectro de respuesta al choque",
       cuerpo, script, "Explorador didáctico del ensayo de choque (pulsos clásicos y espectro de respuesta al choque) · material de apoyo del curso de Vibraciones · funciona sin conexión (un solo archivo).")
