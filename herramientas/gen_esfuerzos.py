#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera esfuerzos_interactivo.html · Pilar 17 · Esfuerzos directos en una unión con pernos (U5, temas 5.1 y 5.2).
Uso: python3 gen_esfuerzos.py CARPETA"""
from base_pag import *

cuerpo = f"""
  <div class="intro full">
    <b>¿Qué muestra?</b> Una unión a traslape transmite la carga <i>P</i> de una placa a otra a través de uno o varios pernos. En ese trayecto aparecen los dos esfuerzos directos del programa: el <b>esfuerzo normal</b> σ = <i>P</i>/<i>A</i>, con la fuerza perpendicular al área (tensión en la placa, aplastamiento contra el perno), y el <b>esfuerzo cortante directo</b> τ = <i>V</i>/<i>A</i>, con la fuerza contenida en el área (corte del perno, desgarre de la placa). La unión puede fallar de cuatro maneras; cada una tiene su propia área. El explorador calcula los cuatro esfuerzos, los compara con el admisible y señala el modo que gobierna.
  </div>

  <div class="card">
    <canvas id="cu" width="760" height="360" aria-label="Esquema de la unión: vista superior y vista lateral"></canvas>
    <canvas id="cb" width="760" height="230" style="margin-top:10px" aria-label="Aprovechamiento de cada modo de falla"></canvas>
    <div class="legend">
      <span><i class="sw" style="border-top-color:var(--red)"></i> modo que gobierna</span>
      <span><i class="sw" style="border-top-color:var(--steel)"></i> esfuerzo / admisible</span>
      <span><i class="sw" style="border-top-color:var(--grey);border-top-style:dashed"></i> límite (aprovechamiento = 1)</span>
    </div>
  </div>

  <div class="card">
    <h2>Controles</h2>
    <div class="grp"><div class="t">Carga y perno</div>
      {fila("Carga <i>P</i>", "P", 0.5, 60, 0.5, 5, "kN")}
      {fila("Diámetro del perno <i>d</i>", "d", 3, 20, 0.5, 6, "mm")}
      {fila("Pernos en la fila <i>n</i>", "n", 1, 5, 1, 1)}
      {fila("Fluencia del perno σ<sub>y,p</sub>", "sb", 200, 1100, 5, 640, "MPa")}
      <div class="btns"><button class="btn on" data-ns="1">Cortante simple</button><button class="btn" data-ns="2">Cortante doble</button></div>
    </div>
    <div class="grp"><div class="t">Placa</div>
      {fila("Espesor <i>t</i>", "t", 0.5, 12, 0.1, 3, "mm")}
      {fila("Ancho <i>w</i>", "w", 10, 150, 1, 30, "mm")}
      {fila("Distancia al borde <i>e</i>", "e", 4, 60, 0.5, 12, "mm")}
      {fila("Fluencia de la placa σ<sub>y</sub>", "sy", 100, 1000, 5, 345, "MPa")}
    </div>
    <div class="btns">
      <button class="btn" data-pre="A">Aluminio 2024-T3 con perno de acero</button><button class="btn" data-pre="C">Falla el perno</button><button class="btn" data-pre="N">Falla la sección neta</button><button class="btn" data-pre="D">Falla por desgarre</button>
      <button class="btn" id="pra">Ocultar lecturas (modo práctica)</button>
    </div>
    <div class="tiles t3" style="margin-top:10px">
      {tile("Cortante en el perno τ", "otau")}{tile("Aplastamiento σ<sub>b</sub>", "oap")}{tile("Tensión en la sección neta σ<sub>n</sub>", "onet")}
      {tile("Desgarre de la placa τ<sub>d</sub>", "odes")}{tile("Tensión en la sección bruta σ", "obr")}{tile("Área de corte de los pernos", "oab")}
      {tile("Factor de seguridad mínimo", "ofs", "hl")}{tile("Modo que gobierna", "omod", "hl")}{tile("Carga que inicia la fluencia", "opm")}
    </div>
    <div class="nota" id="olect"></div>
  </div>

  <div class="card full">
    <h2>Las fórmulas en pantalla</h2>
    <div class="two"><div>
    {eq("1 · Esfuerzo normal directo (tema 5.1)", M(r"\sigma=\frac{P}{A},\qquad \sigma_{\text{bruta}}=\frac{P}{w\,t},\qquad \sigma_n=\frac{P}{(w-n\,d)\,t}") + nota("la fuerza es perpendicular al área; la sección neta descuenta los barrenos de la fila, y en ella el valor calculado es el esfuerzo <i>medio</i>"))}
    {eq("2 · Esfuerzo cortante directo en el perno (tema 5.2)", M(r"\tau=\frac{V}{A}=\frac{P}{n\,n_s\,\frac{\pi d^2}{4}}") + nota("<i>n</i><sub>s</sub> = 1 en cortante simple y 2 en cortante doble: cada plano de corte lleva <i>P</i>/(<i>n</i>·<i>n</i><sub>s</sub>)"))}
    {eq("3 · Aplastamiento entre perno y placa", M(r"\sigma_b=\frac{P}{n\,d\,t}") + nota("esfuerzo normal de compresión sobre el área proyectada <i>d</i>·<i>t</i>; la presión real no es uniforme"))}
    </div><div>
    {eq("4 · Desgarre de la placa por cortante", M(r"\tau_d=\frac{P}{n\cdot 2\,t\left(e-\frac{d}{2}\right)}") + nota("dos planos de corte, del borde del barreno al borde de la placa; <i>e</i> se mide desde el centro del barreno"))}
    {eq("5 · Admisibles usados", M(r"\sigma_{\text{adm}}=\sigma_y,\qquad \tau_{\text{adm}}=\frac{\sigma_y}{\sqrt3}\approx0.577\,\sigma_y") + nota("fluencia en cortante según el criterio de von Mises (explorador del círculo de Mohr); para el aplastamiento se toma la menor de las fluencias de placa y perno, valor conservador"))}
    {eq("6 · Factor de seguridad y modo que gobierna", M(r"FS_i=\frac{\text{admisible}_i}{\text{esfuerzo}_i},\qquad FS=\min_i FS_i,\qquad P_{\text{máx}}=FS\cdot P"))}
    </div></div>
    <div class="intro" style="margin-top:12px"><b>Hipótesis.</b> (a) Todos los pernos de la fila toman la misma carga y la fila es perpendicular a <i>P</i>. (b) Los esfuerzos se reparten de manera uniforme en cada área: son esfuerzos medios. (c) No se cuenta la fricción entre placas ni la precarga del perno. (d) En cortante simple se ignora la flexión secundaria que produce la excentricidad de las placas. (e) En cortante doble la placa analizada es la central, de espesor <i>t</i>; cada placa exterior, de espesor no menor que <i>t</i>/2, no resulta más crítica. (f) Los admisibles son de fluencia; un diseño real usa los valores y los factores de la norma o del manual aplicable, y en aeronáutica los admisibles de aplastamiento dependen del cociente <i>e</i>/<i>d</i>.</div>
    <div class="takeaway" style="margin-top:10px"><b>Cómo explorar:</b> (1) con los valores iniciales (5 kN, perno de 6 mm, placa de 3 mm por 30 mm) gobierna el aplastamiento, con factor de seguridad 1.24. (2) Al pasar a <b>cortante doble</b> el esfuerzo en el perno baja a la mitad y los de la placa no cambian: el perno deja de importar. (3) «Falla el perno»: un perno delgado en una placa gruesa; el cortante crece con 1/<i>d</i>², mientras que el aplastamiento crece solo con 1/<i>d</i>. (4) «Falla la sección neta»: placa angosta con varios barrenos; cada perno añadido alivia el cortante y el aplastamiento, pero quita área a la placa. (5) «Falla por desgarre»: barreno demasiado cerca del borde; de ahí la regla habitual de diseño <i>e</i> ≥ 2<i>d</i>. (6) Una unión equilibrada tiene los cuatro aprovechamientos parecidos. <b>Relación con el resto del curso:</b> los esfuerzos de esta página son los datos de entrada del círculo de Mohr (tema 5.3), y bajo carga vibratoria el esfuerzo de la sección neta es el esfuerzo nominal del cálculo de fatiga; el barreno concentra el esfuerzo, por lo que el valor local es mayor que el medio. Referencias: Beer, Johnston, DeWolf y Mazurek, <i>Mecánica de materiales</i>, 7.ª ed., McGraw-Hill, cap. 1; Hibbeler, <i>Mecánica de materiales</i>, 9.ª ed., Pearson, cap. 1; Budynas y Nisbett, <i>Diseño en ingeniería mecánica de Shigley</i>, 10.ª ed., McGraw-Hill, cap. 8 (uniones cargadas en cortante); Niu, <i>Airframe Structural Design</i>, 2.ª ed., Conmilit Press, cap. 7.</div>
  </div>
"""
script = LIB + r"""
let S={P:5,d:6,n:1,sb:640,t:3,w:30,e:12,sy:345,ns:1};
const UN={P:' kN',d:' mm',n:'',sb:' MPa',t:' mm',w:' mm',e:' mm',sy:' MPa'}, K3=1/Math.sqrt(3);
function calc(){ const P=S.P*1e3, Ab=Math.PI*S.d*S.d/4, At=S.n*S.ns*Ab, an=(S.w-S.n*S.d)*S.t, ld=S.e-S.d/2;
  const tau=P/At, ap=P/(S.n*S.d*S.t), net=an>0?P/an:Infinity, des=ld>0?P/(S.n*2*S.t*ld):Infinity, br=P/(S.w*S.t);
  const M=[{k:'Cortante en el perno',c:'perno',s:tau,a:K3*S.sb},{k:'Aplastamiento',c:'aplastamiento',s:ap,a:Math.min(S.sy,S.sb)},{k:'Tensión en la sección neta',c:'sección neta',s:net,a:S.sy},{k:'Desgarre de la placa',c:'desgarre',s:des,a:K3*S.sy}];
  M.forEach(m=>{ m.u=m.s/m.a; m.fs=m.a/m.s; }); let ig=0; M.forEach((m,i)=>{ if(m.u>M[ig].u) ig=i; });
  return {M,ig,tau,ap,net,des,br,At,fs:M[ig].fs,pmax:M[ig].fs*S.P,an,ld}; }
function flecha(c,x0,y,x1,col){ c.strokeStyle=col; c.fillStyle=col; c.lineWidth=2.2; c.beginPath(); c.moveTo(x0,y); c.lineTo(x1,y); c.stroke(); const s=x1>x0?1:-1; c.beginPath(); c.moveTo(x1,y); c.lineTo(x1-9*s,y-5); c.lineTo(x1-9*s,y+5); c.closePath(); c.fill(); }
function dibujar(){
  const q=calc(), g=lienzo($('cu'),360), c=g.c, W=g.W, gob=q.M[q.ig].c;
  // ---------- vista superior
  const Lp=2*S.e+1.1*S.w, tot=2*Lp-2*S.e, sc=Math.min((W-112)/tot,150/S.w), x0=(W-tot*sc)/2, yc=100, hw=S.w*sc/2;
  const xa=x0+(Lp-2*S.e)*sc, xb=x0+Lp*sc, xcen=(xa+xb)/2;
  c.font='bold 12px Arial'; c.fillStyle=NAVY; c.textAlign='left'; c.textBaseline='top'; c.fillText('Vista superior',8,6);
  c.lineWidth=1.4; c.strokeStyle='#7A8AA8'; c.fillStyle='rgba(68,114,196,.16)'; c.fillRect(x0,yc-hw,Lp*sc,2*hw); c.strokeRect(x0,yc-hw,Lp*sc,2*hw);
  c.fillStyle='rgba(197,90,17,.13)'; c.fillRect(xa,yc-hw,Lp*sc,2*hw); c.strokeRect(xa,yc-hw,Lp*sc,2*hw);
  const r=S.d*sc/2, ys=[]; for(let i=0;i<S.n;i++) ys.push(yc-hw+(i+0.5)*2*hw/S.n);
  if(gob==='sección neta'){ c.strokeStyle=RED; c.lineWidth=3; c.setLineDash([7,4]); c.beginPath(); c.moveTo(xcen,yc-hw-6); c.lineTo(xcen,yc+hw+6); c.stroke(); c.setLineDash([]); }
  ys.forEach(y=>{ if(gob==='desgarre'){ c.strokeStyle=RED; c.lineWidth=3; [-1,1].forEach(s=>{ c.beginPath(); c.moveTo(xcen,y+s*r); c.lineTo(xb,y+s*r); c.stroke(); }); }
    c.beginPath(); c.arc(xcen,y,r,0,7); c.fillStyle=gob==='perno'?RED:'#5B6B86'; c.fill(); c.lineWidth=1.2; c.strokeStyle='#fff'; c.stroke();
    if(gob==='aplastamiento'){ c.strokeStyle=RED; c.lineWidth=4; c.beginPath(); c.arc(xcen,y,r+2,-Math.PI/2,Math.PI/2); c.stroke(); } });
  flecha(c,x0-6,yc,x0-46,NAVY); flecha(c,xa+Lp*sc+6,yc,xa+Lp*sc+46,NAVY); c.font='bold 12px Arial'; c.fillStyle=NAVY; c.textBaseline='bottom'; c.textAlign='center'; c.fillText('P',x0-28,yc-6); c.fillText('P',xa+Lp*sc+28,yc-6);
  // cotas
  c.strokeStyle=GREY; c.fillStyle=GREY; c.lineWidth=1; c.font='11px Arial'; const yq=yc+hw+14; c.beginPath(); c.moveTo(xcen,yq); c.lineTo(xb,yq); c.moveTo(xcen,yq-4); c.lineTo(xcen,yq+4); c.moveTo(xb,yq-4); c.lineTo(xb,yq+4); c.stroke(); c.textBaseline='top'; c.fillText('e = '+S.e+' mm',(xcen+xb)/2,yq+3);
  const xq=x0+10; c.beginPath(); c.moveTo(xq,yc-hw); c.lineTo(xq,yc+hw); c.stroke(); c.textAlign='left'; c.textBaseline='middle'; c.fillText('w = '+S.w+' mm',xq+5,yc);
  // ---------- vista lateral
  const y2=285, tp=Math.max(7,Math.min(22,S.t*sc)); c.font='bold 12px Arial'; c.fillStyle=NAVY; c.textAlign='left'; c.textBaseline='top'; c.fillText('Vista lateral · '+(S.ns===1?'cortante simple: un plano de corte':'cortante doble: dos planos de corte'),8,y2-62);
  c.lineWidth=1.4; c.strokeStyle='#7A8AA8';
  const placa=(xi,yi,l,h,col)=>{ c.fillStyle=col; c.fillRect(xi,yi,l,h); c.strokeRect(xi,yi,l,h); };
  let planos=[], ytop, ybot;
  if(S.ns===1){ placa(x0,y2-tp,Lp*sc,tp,'rgba(68,114,196,.16)'); placa(xa,y2,Lp*sc,tp,'rgba(197,90,17,.13)'); planos=[y2]; ytop=y2-tp; ybot=y2+tp; }
  else { placa(xa,y2-tp/2,Lp*sc,tp,'rgba(197,90,17,.13)'); placa(x0,y2-tp/2-Math.max(5,tp*0.6),Lp*sc,Math.max(5,tp*0.6),'rgba(68,114,196,.16)'); placa(x0,y2+tp/2,Lp*sc,Math.max(5,tp*0.6),'rgba(68,114,196,.16)'); planos=[y2-tp/2,y2+tp/2]; ytop=y2-tp/2-Math.max(5,tp*0.6); ybot=y2+tp/2+Math.max(5,tp*0.6); }
  c.fillStyle=gob==='perno'?RED:'#5B6B86'; c.fillRect(xcen-r,ytop-7,2*r,ybot-ytop+14); c.fillRect(xcen-1.6*r,ytop-11,3.2*r,5); c.fillRect(xcen-1.6*r,ybot+6,3.2*r,5);
  c.strokeStyle=RED; c.lineWidth=1.6; c.setLineDash([5,3]); planos.forEach(y=>{ c.beginPath(); c.moveTo(xcen-2.6*r-6,y); c.lineTo(xcen+2.6*r+6,y); c.stroke(); }); c.setLineDash([]);
  c.fillStyle=GREY; c.font='11px Arial'; c.textAlign='left'; c.textBaseline='middle'; c.fillText('t = '+S.t+' mm · d = '+S.d+' mm'+(S.n>1?' · '+S.n+' pernos':''),xa+Lp*sc*0.42,ybot+18);
  // ---------- barras de aprovechamiento
  const g2=lienzo($('cb'),230), c2=g2.c, mL=g2.W<520?128:190, mR=64, bw=g2.W-mL-mR, um=Math.max(1.25,Math.min(3,Math.max(...q.M.map(m=>isFinite(m.u)?m.u:3))*1.1));
  c2.font='bold 12px Arial'; c2.fillStyle=NAVY; c2.textAlign='left'; c2.textBaseline='top'; c2.fillText('Aprovechamiento = esfuerzo / admisible',8,6);
  q.M.forEach((m,i)=>{ const y=38+i*44, u=Math.min(isFinite(m.u)?m.u:um,um); c2.fillStyle='#EEF2F8'; c2.fillRect(mL,y,bw,24); c2.fillStyle=i===q.ig?RED:STEEL; c2.fillRect(mL,y,bw*u/um,24);
    c2.fillStyle=NAVY; c2.font=(i===q.ig?'bold ':'')+(g2.W<520?'11px':'12px')+' Arial'; c2.textAlign='right'; c2.textBaseline='middle'; c2.fillText(g2.W<520?m.c:m.k,mL-8,y+12);
    c2.textAlign='left'; c2.fillStyle=i===q.ig?RED:GREY; c2.fillText(isFinite(m.u)?m.u.toFixed(2):'∞',mL+bw*u/um+6,y+12); });
  const xl=mL+bw/um; c2.strokeStyle=GREY; c2.setLineDash([5,4]); c2.lineWidth=1.3; c2.beginPath(); c2.moveTo(xl,30); c2.lineTo(xl,212); c2.stroke(); c2.setLineDash([]); c2.fillStyle=GREY; c2.font='11px Arial'; c2.textAlign='center'; c2.textBaseline='top'; c2.fillText('1',xl,214);
  // ---------- lecturas
  const mp=v=>isFinite(v)?(+v.toPrecision(3))+' MPa':'∞';
  $('otau').textContent=mp(q.tau); $('oap').textContent=mp(q.ap); $('onet').textContent=mp(q.net); $('odes').textContent=mp(q.des); $('obr').textContent=mp(q.br); $('oab').textContent=(+q.At.toPrecision(3))+' mm²';
  $('ofs').textContent=isFinite(q.fs)?q.fs.toFixed(2):'0'; $('ofs').parentNode.classList.toggle('al',!(q.fs>=1)); $('omod').textContent=q.M[q.ig].c; $('omod').style.fontSize='15px'; $('opm').textContent=(+q.pmax.toPrecision(3))+' kN';
  let a=[]; if(q.an<=0) a.push('Los barrenos ocupan todo el ancho de la placa: no queda sección neta.'); else if(S.w/S.n<3*S.d) a.push('El paso entre pernos (w/n = '+(S.w/S.n).toFixed(1)+' mm) es menor que 3d: en la práctica los barrenos quedan demasiado juntos.');
  if(q.ld<=0) a.push('El barreno se sale de la placa (e ≤ d/2).'); else if(S.e<2*S.d) a.push('La distancia al borde es menor que 2d, el mínimo habitual.');
  a.push(q.fs>=1?'La unión resiste la carga sin fluencia; el modo más aprovechado es: '+q.M[q.ig].c+'.':'La unión fluye por '+q.M[q.ig].c+': el esfuerzo supera al admisible.'); $('olect').textContent=a.join(' ');
}
liga(S,UN,dibujar); practica('pra');
function planos(n){ S.ns=n; document.querySelectorAll('[data-ns]').forEach(b=>b.classList.toggle('on',+b.dataset.ns===n)); }
document.querySelectorAll('[data-ns]').forEach(b=>b.addEventListener('click',()=>{ planos(+b.dataset.ns); dibujar(); }));
const PRE={A:{P:5,d:6,n:1,sb:640,t:3,w:30,e:12,sy:345,ns:1}, C:{P:8,d:4,n:1,sb:640,t:6,w:40,e:12,sy:345,ns:1}, N:{P:20,d:8,n:2,sb:640,t:3,w:28,e:20,sy:345,ns:2}, D:{P:6,d:6,n:1,sb:640,t:3,w:40,e:5,sy:345,ns:2}};
document.querySelectorAll('[data-pre]').forEach(b=>b.addEventListener('click',()=>{ const o=Object.assign({},PRE[b.dataset.pre]); planos(o.ns); delete o.ns; pon(S,UN,o,dibujar); }));
window.addEventListener('resize',dibujar);
window.__es={S,calc};
dibujar();
"""
pagina("esfuerzos_interactivo.html", "Esfuerzos directos en una unión con pernos", "Vibraciones · Pilar 17 · U5",
       "Al variar la carga, el perno y la placa se calculan el esfuerzo normal y el cortante directo en cada área de la unión, y se identifica el modo de falla que gobierna",
       cuerpo, script, "Explorador didáctico de esfuerzos normales y cortantes directos (unión a traslape con pernos) · material de apoyo del curso de Vibraciones · funciona sin conexión (un solo archivo).")
