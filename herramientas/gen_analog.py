#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera analogias_interactivo.html · Pilar 14 · Analogías entre sistemas (U2, temas 2.1 y 2.4).
Uso: python3 gen_analog.py CARPETA"""
from base_pag import *

cuerpo = f"""
  <div class="intro full">
    <b>¿Qué muestra?</b> Un sistema masa-resorte-amortiguador, un eje con disco en torsión, un circuito <i>RLC</i> y un depósito con conducto obedecen la <b>misma ecuación diferencial</b> de segundo orden. Al fijar <i>m</i>, <i>c</i> y <i>k</i> se obtienen los elementos del sistema análogo y se comprueba que la frecuencia natural y el factor de amortiguamiento coinciden: lo que se aprende en un dominio se traslada a los demás. La analogía permite además ensayar un sistema mecánico con un circuito, que es más barato de construir y de medir.
  </div>

  <div class="card">
    <canvas id="cs" width="760" height="250" aria-label="Esquema del sistema mecánico y de su circuito análogo"></canvas>
    <canvas id="cr" width="760" height="320" style="margin-top:10px" aria-label="Respuesta al escalón de los dos sistemas"></canvas>
    <div class="legend">
      <span><i class="sw" style="border-top-color:var(--steel)"></i> mecánico: <i>x</i>(<i>t</i>)</span>
      <span><i class="sw" style="border-top-color:var(--orange);border-top-style:dashed"></i> eléctrico: <i>q</i>(<i>t</i>) o λ(<i>t</i>)</span>
      <span><i class="sw" style="border-top-color:var(--grey);border-top-style:dotted"></i> valor final y envolvente</span>
    </div>
  </div>

  <div class="card">
    <h2>Controles</h2>
    <div class="grp"><div class="t">Sistema mecánico de referencia</div>
      {fila("Masa <i>m</i>", "m", 0.05, 20, 0.05, 1, "kg")}
      {fila("Coeficiente de amortiguamiento <i>c</i>", "c", 0, 1000, 0.1, 2, "N·s/m")}
      {fila("Rigidez <i>k</i>", "k", 1, 5000, 1, 100, "N/m")}
      {fila("Escalón de fuerza <i>F</i><sub>0</sub>", "F0", 0.1, 50, 0.1, 1, "N")}
    </div>
    <div class="grp"><div class="t">Analogía eléctrica</div>
      <div class="btns"><button class="btn on" data-an="serie">Fuerza-tensión (<i>RLC</i> serie)</button><button class="btn" data-an="par">Fuerza-corriente (<i>RLC</i> paralelo)</button></div>
      {fila("Escala de impedancia: log<sub>10</sub> α", "la", -3, 6, 0.1, 0)}
      <div class="nota" id="nan"></div>
    </div>
    <div class="btns">
      <button class="btn" data-pre="S">Subamortiguado</button><button class="btn" data-pre="C">Crítico</button><button class="btn" data-pre="O">Sobreamortiguado</button><button class="btn" data-pre="E">Componentes de laboratorio</button><button class="btn" id="pra">Ocultar lecturas (modo práctica)</button>
    </div>
    <div class="tiles t3" style="margin-top:10px">
      {tile("ω<sub>n</sub> mecánica √(<i>k</i>/<i>m</i>)", "own")}{tile("ω<sub>n</sub> eléctrica 1/√(<i>LC</i>)", "owe")}{tile("Frecuencia <i>f</i><sub>n</sub>", "ofn")}
      {tile("ζ mecánico <i>c</i>/(2√(<i>km</i>))", "ozm", "hl")}{tile("ζ eléctrico", "oze", "hl")}{tile("Factor de calidad <i>Q</i> = 1/(2ζ)", "oQ")}
      {tile("Inductancia <i>L</i>", "oL")}{tile("Resistencia <i>R</i>", "oR")}{tile("Capacitancia <i>C</i>", "oC")}
      <div class="tile"><div class="k">Régimen</div><div class="v" id="oreg" style="font-size:12.5px;line-height:1.5">…</div></div>{tile("Valor final <i>x</i><sub>est</sub> = <i>F</i><sub>0</sub>/<i>k</i>", "oxe")}{tile("Sobrepaso máximo", "osp")}
    </div>
  </div>

  <div class="card full">
    <h2>Tabla de equivalencias con los valores actuales</h2>
    <div style="overflow-x:auto"><table class="tb" id="tabla"></table></div>
    <div class="nota">En cada sistema, el producto de la variable análoga de la fuerza por la análoga de la velocidad es una potencia. La analogía fuerza-tensión (o de impedancia) asocia fuerza con tensión y velocidad con corriente. La analogía fuerza-corriente (o de movilidad, propuesta por Firestone) asocia las variables que atraviesan el elemento (fuerza, corriente) y las que se miden entre sus terminales (velocidad, tensión), con lo que conserva la topología de la red: elementos mecánicos en paralelo corresponden a elementos eléctricos en paralelo. Las filas de torsión e hidráulica muestran valores numéricamente iguales a los mecánicos (escala unitaria).</div>
  </div>

  <div class="card full">
    <h2>Las fórmulas en pantalla</h2>
    <div class="two"><div>
    {eq("1 · Mecánico de traslación", M(r"m\,\ddot x+c\,\dot x+k\,x=F(t)"))}
    {eq("2 · Circuito <i>RLC</i> serie (analogía fuerza-tensión)", M(r"L\,\ddot q+R\,\dot q+\frac{1}{C}\,q=V(t)") + nota("<i>L</i> ↔ <i>m</i>, <i>R</i> ↔ <i>c</i>, 1/<i>C</i> ↔ <i>k</i>, carga <i>q</i> ↔ <i>x</i>, corriente <i>i</i> ↔ velocidad"))}
    {eq("3 · Circuito <i>RLC</i> paralelo (analogía fuerza-corriente)", M(r"C\,\ddot\lambda+\frac{1}{R}\,\dot\lambda+\frac{1}{L}\,\lambda=I(t)") + nota("<i>C</i> ↔ <i>m</i>, 1/<i>R</i> ↔ <i>c</i>, 1/<i>L</i> ↔ <i>k</i>, enlace de flujo λ ↔ <i>x</i>, tensión <i>v</i> = dλ/d<i>t</i> ↔ velocidad"))}
    {eq("4 · Torsión", M(r"J\,\ddot\theta+c_t\,\dot\theta+k_t\,\theta=M(t)"))}
    {eq("5 · Hidráulico: conducto con depósito", M(r"I_f\,\ddot V+R_f\,\dot V+\frac{1}{C_f}\,V=p(t)") + nota("inertancia <i>I</i><sub>f</sub> = ρℓ/<i>A</i>; capacitancia de un depósito abierto <i>C</i><sub>f</sub> = <i>A</i><sub>d</sub>/(ρ<i>g</i>); resistencia en régimen laminar <i>R</i><sub>f</sub> = 8μℓ/(π<i>a</i><sup>4</sup>). En régimen turbulento la resistencia no es lineal y la analogía solo vale linealizada"))}
    </div><div>
    {eq("6 · Forma normalizada común", M(r"\ddot u+2\zeta\omega_n\,\dot u+\omega_n^2\,u=\omega_n^2\,u_{\text{est}}"))}
    {eq("7 · Parámetros en cada dominio", M(r"\omega_n=\sqrt{\frac{k}{m}}=\frac{1}{\sqrt{LC}},\qquad \zeta=\frac{c}{2\sqrt{km}}") + M(r"\zeta_{\text{serie}}=\frac{R}{2}\sqrt{\frac{C}{L}},\qquad \zeta_{\text{paralelo}}=\frac{1}{2R}\sqrt{\frac{L}{C}}"))}
    {eq("8 · Escala de impedancia α", M(r"L=\alpha\,m,\qquad R=\alpha\,c,\qquad C=\frac{1}{\alpha\,k}") + nota("ω<sub>n</sub> y ζ no cambian con α; en paralelo: <i>C</i> = <i>m</i>/α, <i>R</i> = α/<i>c</i>, <i>L</i> = α/<i>k</i>"))}
    {eq("9 · Control de actitud proporcional-derivativo de un satélite", M(r"J\,\ddot\theta+K_d\,\dot\theta+K_p\,\theta=0") + M(r"\omega_n=\sqrt{\frac{K_p}{J}},\qquad \zeta=\frac{K_d}{2\sqrt{K_pJ}}") + nota("la ganancia proporcional actúa como resorte y la derivativa como amortiguador"))}
    </div></div>
    <div class="intro" style="margin-top:12px"><b>Analogías con sistemas espaciales (tema 2.4).</b> El mismo modelo de un grado de libertad describe: (a) el <b>chapoteo de propelente</b> en un tanque, que se sustituye por un péndulo o por una masa con resorte cuya frecuencia depende del nivel de llenado; (b) un <b>panel solar flexible</b>, representado por su primer modo con masa, rigidez y amortiguamiento modales; (c) el <b>lazo de control de actitud</b> de la fórmula 9; (d) un <b>aislador de carga útil</b> entre el lanzador y el satélite. En todos los casos el diseño consiste en separar las frecuencias naturales de las de excitación y de las del lazo de control.</div>
    <div class="takeaway" style="margin-top:10px"><b>Cómo explorar:</b> (1) con <i>m</i> = 1 kg, <i>c</i> = 2 N·s/m y <i>k</i> = 100 N/m se obtiene ω<sub>n</sub> = 10 rad/s y ζ = 0.10 en los dos dominios; las dos curvas se superponen. (2) Al mover solo la escala α cambian <i>L</i>, <i>R</i> y <i>C</i>, pero no la respuesta. (3) El preajuste «Componentes de laboratorio» usa α = 10<sup>3</sup>: resultan <i>L</i> = 1 kH, <i>R</i> = 2 kΩ y <i>C</i> = 10 µF; una inductancia tan grande no es práctica, por lo que en el laboratorio se escala también el tiempo (un circuito mil veces más rápido con <i>L</i> = 1 H y <i>C</i> = 10 nF conserva ζ si <i>R</i> = 2 kΩ). (4) Con el amortiguamiento crítico <i>c</i> = 2√(<i>km</i>) = 20 N·s/m desaparece el sobrepaso. (5) Para practicar: «Ocultar lecturas», calcular <i>L</i>, <i>R</i> y <i>C</i> para una escala dada y comprobar. Referencias: Ogata, <i>System Dynamics</i>, 4.ª ed., caps. 3, 6 y 7; Wie, <i>Space Vehicle Dynamics and Control</i>, 2.ª ed., AIAA, 2008, <a href="https://doi.org/10.2514/4.860119">doi:10.2514/4.860119</a> (control de actitud); Firestone (1933), «A new analogy between mechanical and electrical systems», J. Acoust. Soc. Am. 4, 249–267, <a href="https://doi.org/10.1121/1.1915605">doi:10.1121/1.1915605</a>; Ibrahim, <i>Liquid Sloshing Dynamics</i>, Cambridge University Press, 2005, <a href="https://doi.org/10.1017/CBO9780511536656">doi:10.1017/CBO9780511536656</a>.</div>
  </div>
"""
script = LIB + r"""
let S={m:1,c:2,k:100,F0:1,la:0,an:'serie'};
const UN={m:' kg',c:' N·s/m',k:' N/m',F0:' N',la:''};
function calc(){
  const a=Math.pow(10,S.la), wn=Math.sqrt(S.k/S.m), z=S.c/(2*Math.sqrt(S.k*S.m));
  let L,R,C,we,ze;
  if(S.an==='serie'){ L=a*S.m; R=a*S.c; C=1/(a*S.k); we=1/Math.sqrt(L*C); ze=(R/2)*Math.sqrt(C/L); }
  else { C=S.m/a; R=S.c>0?a/S.c:Infinity; L=a/S.k; we=1/Math.sqrt(L*C); ze=S.c>0?(1/(2*R))*Math.sqrt(L/C):0; }
  const xe=S.F0/S.k, sp=z<1?Math.exp(-Math.PI*z/Math.sqrt(1-z*z)):0;
  return {a,wn,z,L,R,C,we,ze,xe,sp,fn:wn/(2*Math.PI)};
}
// respuesta al escalón normalizada u(t)/u_est para (wn, z)
function escalon(t,wn,z){
  if(z<1-1e-9){ const wd=wn*Math.sqrt(1-z*z); return 1-Math.exp(-z*wn*t)*(Math.cos(wd*t)+z*wn/wd*Math.sin(wd*t)); }
  if(z<=1+1e-9) return 1-Math.exp(-wn*t)*(1+wn*t);
  const s=Math.sqrt(z*z-1), s1=-wn*(z-s), s2=-wn*(z+s); return 1-(s2*Math.exp(s1*t)-s1*Math.exp(s2*t))/(s2-s1);
}
function zig(c,x0,y0,x1,y1,n,amp){ const dx=x1-x0, dy=y1-y0, L=Math.hypot(dx,dy), ux=dx/L, uy=dy/L, px=-uy, py=ux; c.beginPath(); c.moveTo(x0,y0); const a=0.15*L, b=0.85*L; c.lineTo(x0+ux*a,y0+uy*a);
  for(let i=0;i<n;i++){ const s=a+(b-a)*(i+0.5)/n, sg=i%2?-1:1; c.lineTo(x0+ux*s+px*amp*sg,y0+uy*s+py*amp*sg); } c.lineTo(x0+ux*b,y0+uy*b); c.lineTo(x1,y1); c.stroke(); }
function bobina(c,x0,y,x1,n){ const a=x0+0.15*(x1-x0), b=x0+0.85*(x1-x0), r=(b-a)/(2*n); c.beginPath(); c.moveTo(x0,y); c.lineTo(a,y); for(let i=0;i<n;i++) c.arc(a+r*(2*i+1),y,r,Math.PI,0); c.lineTo(x1,y); c.stroke(); }
function esquema(q){
  const ang=($('cs').clientWidth||760)<560, g=lienzo($('cs'),ang?470:250), c=g.c, W=g.W, wM=ang?W:W/2, ex=ang?0:W/2, ey=ang?225:0; c.lineWidth=1.8; c.font='bold 12px Arial'; c.textBaseline='middle';
  // ---- mecánico (mitad izquierda; arriba en pantallas angostas)
  c.fillStyle=NAVY; c.textAlign='left'; c.fillText('Mecánico de traslación',14,16);
  const xw=24, yc=130, xm=Math.max(150,Math.min(wM-150,wM-130)), mw=74, mh=74; c.strokeStyle=GREY; c.beginPath(); c.moveTo(xw,60); c.lineTo(xw,200); c.stroke(); for(let y=64;y<200;y+=12){ c.beginPath(); c.moveTo(xw,y); c.lineTo(xw-8,y+8); c.stroke(); }
  c.strokeStyle=STEEL; zig(c,xw,yc-22,xm,yc-22,8,8); c.fillStyle=STEEL; c.textAlign='center'; c.fillText('k = '+S.k+' N/m',(xw+xm)/2,yc-44);
  c.strokeStyle=ORANGE; const xa=(xw+xm)/2; c.beginPath(); c.moveTo(xw,yc+22); c.lineTo(xa-10,yc+22); c.moveTo(xa-10,yc+10); c.lineTo(xa-10,yc+34); c.moveTo(xa-10,yc+10); c.lineTo(xa+14,yc+10); c.moveTo(xa-10,yc+34); c.lineTo(xa+14,yc+34); c.moveTo(xa+2,yc+14); c.lineTo(xa+2,yc+30); c.moveTo(xa+2,yc+22); c.lineTo(xm,yc+22); c.stroke();
  c.fillStyle=ORANGE; c.fillText('c = '+S.c+' N·s/m',(xw+xm)/2,yc+50);
  c.fillStyle='#E9EEF7'; c.strokeStyle=NAVY; c.fillRect(xm,yc-mh/2,mw,mh); c.strokeRect(xm,yc-mh/2,mw,mh); c.fillStyle=NAVY; c.fillText('m = '+S.m+' kg',xm+mw/2,yc);
  c.strokeStyle=RED; c.fillStyle=RED; c.beginPath(); c.moveTo(xm+mw,yc); c.lineTo(xm+mw+30,yc); c.stroke(); c.beginPath(); c.moveTo(xm+mw+30,yc); c.lineTo(xm+mw+22,yc-5); c.lineTo(xm+mw+22,yc+5); c.fill(); c.textAlign='left'; c.fillText('F_0',xm+mw+34,yc);
  c.strokeStyle=GREY; c.beginPath(); c.moveTo(xm,yc+mh/2+12); c.lineTo(xm+mw+20,yc+mh/2+12); c.stroke(); c.fillStyle=GREY; c.textAlign='center'; c.fillText('x(t)',xm+mw/2,yc+mh/2+26);
  // ---- eléctrico (mitad derecha; abajo en pantallas angostas)
  c.save(); c.translate(ex,ey);
  const x0=34, x1=wM-34, yt=70, yb=200; c.fillStyle=NAVY; c.textAlign='left'; c.fillText(S.an==='serie'?'Circuito RLC serie':'Circuito RLC paralelo',14,16);
  c.strokeStyle=NAVY; c.lineWidth=1.8;
  if(S.an==='serie'){ const w=x1-x0, xa1=x0+w*0.08, xa2=x0+w*0.40, xb2=x0+w*0.74;
    c.beginPath(); c.moveTo(x0,yb); c.lineTo(x0,yt); c.lineTo(xa1,yt); c.stroke();
    c.strokeStyle=ORANGE; zig(c,xa1,yt,xa2,yt,7,7); c.strokeStyle=NAVY; bobina(c,xa2,yt,xb2,4);
    c.beginPath(); c.moveTo(xb2,yt); c.lineTo(x1,yt); c.lineTo(x1,(yt+yb)/2-5); c.moveTo(x1-16,(yt+yb)/2-5); c.lineTo(x1+16,(yt+yb)/2-5); c.moveTo(x1-16,(yt+yb)/2+5); c.lineTo(x1+16,(yt+yb)/2+5); c.moveTo(x1,(yt+yb)/2+5); c.lineTo(x1,yb); c.lineTo(x0,yb); c.stroke();
    c.fillStyle='#fff'; c.beginPath(); c.arc(x0,(yt+yb)/2,15,0,7); c.fill(); c.stroke(); c.fillStyle=RED; c.textAlign='center'; c.fillText('V_0',x0,(yt+yb)/2);
    c.fillStyle=ORANGE; c.fillText('R = '+ing(q.R,'Ω'),(xa1+xa2)/2,yt-20); c.fillStyle=NAVY; c.fillText('L = '+ing(q.L,'H'),(xa2+xb2)/2,yt-20); c.fillStyle=STEEL; c.textAlign='right'; c.fillText('C = '+ing(q.C,'F'),x1-22,(yt+yb)/2+24); c.fillStyle=GREY; c.textAlign='center'; c.fillText('q(t) en el capacitor',(x0+x1)/2,yb+18);
  } else { const w=x1-x0, xs=[x0+w*0.34,x0+w*0.62,x0+w*0.9];
    c.beginPath(); c.moveTo(x0,yt); c.lineTo(xs[2],yt); c.moveTo(x0,yb); c.lineTo(xs[2],yb); c.moveTo(x0,yt); c.lineTo(x0,yb); c.stroke();
    c.fillStyle='#fff'; c.beginPath(); c.arc(x0,(yt+yb)/2,15,0,7); c.fill(); c.stroke(); c.fillStyle=RED; c.textAlign='center'; c.fillText('I_0',x0,(yt+yb)/2);
    c.strokeStyle=ORANGE; zig(c,xs[0],yt,xs[0],yb,7,7); c.strokeStyle=NAVY;
    c.save(); c.translate(xs[1],yt); c.rotate(Math.PI/2); bobina(c,0,0,yb-yt,4); c.restore();
    const ym=(yt+yb)/2; c.beginPath(); c.moveTo(xs[2],yt); c.lineTo(xs[2],ym-5); c.moveTo(xs[2]-16,ym-5); c.lineTo(xs[2]+16,ym-5); c.moveTo(xs[2]-16,ym+5); c.lineTo(xs[2]+16,ym+5); c.moveTo(xs[2],ym+5); c.lineTo(xs[2],yb); c.stroke();
    c.textAlign='center'; c.font='bold 11px Arial'; c.fillStyle=ORANGE; c.fillText('R = '+(isFinite(q.R)?ing(q.R,'Ω'):'∞'),xs[0],yt-14); c.fillStyle=NAVY; c.fillText('L = '+ing(q.L,'H'),xs[1],yb+16); c.fillStyle=STEEL; c.fillText('C = '+ing(q.C,'F'),xs[2]-6,yt-14); c.fillStyle=GREY; c.fillText('λ(t): enlace de flujo en L',(x0+x1)/2,yb+34);
  }
  c.restore();
  c.strokeStyle='#C9D3E6'; c.lineWidth=1; c.setLineDash([3,4]); c.beginPath(); if(ang){ c.moveTo(8,ey-2); c.lineTo(W-8,ey-2); } else { c.moveTo(W/2,8); c.lineTo(W/2,242); } c.stroke(); c.setLineDash([]);
}
function dibujar(){
  const q=calc(); esquema(q);
  const tau=q.z>0?1/(q.z*q.wn):Infinity, Tn=2*Math.PI/q.wn, tf=Math.min(Math.max(4*Tn, isFinite(tau)?5*tau:12*Tn, q.z>1?8*q.z/q.wn:0), 40*Tn);
  const g=lienzo($('cr'),320), ymx=q.xe*Math.max(1.15,(1+q.sp)*1.1)*1e3;
  const e=ejes(g,{},{x0:0,x1:tf,y0:0,y1:ymx,xl:'t (s)',yl:S.an==='serie'?'x (mm)  ·  q (mC)':'x (mm)  ·  λ (mWb)',tit:'Respuesta al escalón: F_0 = '+S.F0+' N  ·  '+(S.an==='serie'?'V_0 = α F_0':'I_0 = F_0/α'),ny:5});
  hline(e,q.xe*1e3,GREY,[2,3],'x_est = F_0/k');
  if(q.z<1&&q.z>0){ funcion(e,t=>q.xe*1e3*(1+Math.exp(-q.z*q.wn*t)/Math.sqrt(1-q.z*q.z)),'#9AA7BF',1,[2,3]); funcion(e,t=>q.xe*1e3*(1-Math.exp(-q.z*q.wn*t)/Math.sqrt(1-q.z*q.z)),'#9AA7BF',1,[2,3]); }
  funcion(e,t=>q.xe*1e3*escalon(t,q.wn,q.z),STEEL,2.6); funcion(e,t=>q.xe*1e3*escalon(t,q.we,q.ze),ORANGE,1.6,[7,5]);
  const p4=v=>(+v).toPrecision(4);
  $('own').textContent=p4(q.wn)+' rad/s'; $('owe').textContent=p4(q.we)+' rad/s'; $('ofn').textContent=p4(q.fn)+' Hz';
  $('ozm').textContent=p4(q.z); $('oze').textContent=p4(q.ze); $('oQ').textContent=q.z>0?p4(1/(2*q.z)):'∞';
  $('oL').textContent=ing(q.L,'H'); $('oR').textContent=isFinite(q.R)?ing(q.R,'Ω'):'∞ (circuito abierto)'; $('oC').textContent=ing(q.C,'F');
  $('oreg').textContent=q.z===0?'sin amortiguamiento':Math.abs(q.z-1)<5e-4?'crítico':q.z<1?'subamortiguado':'sobreamortiguado';
  $('oxe').textContent=(q.xe*1e3).toPrecision(4)+' mm'; $('osp').textContent=(100*q.sp).toFixed(1)+' %';
  $('nan').textContent=(S.an==='serie'?'Serie: L = α m, R = α c, C = 1/(α k). ':'Paralelo: C = m/α, R = α/c, L = α/k. ')+'α = '+(+q.a.toPrecision(3))+(S.an==='serie'?' Ω·s/kg':' Ω·N·s/m')+'. La escala cambia los componentes, no la dinámica.';
  const f=(v,u)=>(+(+v).toPrecision(4))+' '+u, filas=[
    ['Sistema','Inercia','Disipación','Rigidez (o su inversa)','Análoga de la fuerza','Análoga de la velocidad','Análoga del desplazamiento'],
    ['Mecánico de traslación','m = '+f(S.m,'kg'),'c = '+f(S.c,'N·s/m'),'k = '+f(S.k,'N/m'),'fuerza F (N)','velocidad (m/s)','x (m)'],
    ['Mecánico de torsión','J = '+f(S.m,'kg·m^2'),'c_t = '+f(S.c,'N·m·s/rad'),'k_t = '+f(S.k,'N·m/rad'),'par M (N·m)','velocidad angular (rad/s)','θ (rad)'],
    ['Eléctrico serie (fuerza-tensión)','L = '+ing(q.a*S.m,'H'),'R = '+ing(q.a*S.c,'Ω'),'1/C, con C = '+ing(1/(q.a*S.k),'F'),'tensión V (V)','corriente i (A)','carga q (C)'],
    ['Eléctrico paralelo (fuerza-corriente)','C = '+ing(S.m/q.a,'F'),'1/R, con R = '+(S.c>0?ing(q.a/S.c,'Ω'):'∞'),'1/L, con L = '+ing(q.a/S.k,'H'),'corriente I (A)','tensión v (V)','enlace de flujo λ (Wb)'],
    ['Hidráulico (conducto y depósito)','inertancia I_f = '+f(S.m,'Pa·s^2/m^3'),'resistencia R_f = '+f(S.c,'Pa·s/m^3'),'1/C_f, con C_f = '+f(1/S.k,'m^3/Pa'),'presión p (Pa)','caudal Q (m^3/s)','volumen V (m^3)']];
  $('tabla').innerHTML=filas.map((r,i)=>'<tr>'+r.map(x=>i?'<td></td>':'<th></th>').join('')+'</tr>').join('');
  [...$('tabla').rows].forEach((tr,i)=>[...tr.cells].forEach((td,j)=>td.textContent=filas[i][j]));
}
liga(S,UN,dibujar); practica('pra');
function analogia(a){ S.an=a; document.querySelectorAll('[data-an]').forEach(x=>x.classList.toggle('on',x.dataset.an===a)); }
document.querySelectorAll('[data-an]').forEach(b=>b.addEventListener('click',()=>{ S.an=b.dataset.an; document.querySelectorAll('[data-an]').forEach(x=>x.classList.toggle('on',x===b)); dibujar(); }));
const PRE={S:{m:1,c:2,k:100,F0:1,la:0}, C:{m:1,c:20,k:100,F0:1,la:0}, O:{m:1,c:50,k:100,F0:1,la:0}, E:{m:1,c:2,k:100,F0:1,la:3}};
document.querySelectorAll('[data-pre]').forEach(b=>b.addEventListener('click',()=>{ analogia('serie'); pon(S,UN,PRE[b.dataset.pre],dibujar); }));
window.addEventListener('resize',dibujar);
window.__an={S,calc,escalon};
dibujar();
"""
pagina("analogias_interactivo.html", "Analogías entre sistemas mecánicos, eléctricos e hidráulicos", "Vibraciones · Pilar 14 · U2",
       "Al fijar la masa, el amortiguador y el resorte se obtienen los elementos del circuito análogo y se comprueba que la frecuencia natural, el amortiguamiento y la respuesta coinciden",
       cuerpo, script, "Explorador didáctico de analogías electromecánicas (fuerza-tensión y fuerza-corriente) · material de apoyo del curso de Vibraciones · funciona sin conexión (un solo archivo).")
