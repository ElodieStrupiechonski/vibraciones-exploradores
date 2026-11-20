#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera anecoica_interactivo.html · Pilar 19 · Campo libre, campo reverberante y cámara anecoica (U6, tema 6.4).
Uso: python3 gen_anecoica.py CARPETA"""
from base_pag import *

cuerpo = f"""
  <div class="intro full">
    <b>¿Qué muestra?</b> En un recinto, el micrófono recibe dos contribuciones: el <b>campo directo</b>, que llega de la fuente sin tocar las paredes y baja 6 dB cada vez que se duplica la distancia, y el <b>campo reverberante</b>, formado por las reflexiones, que es casi uniforme en toda la sala. Una <b>cámara anecoica</b> («sin eco») cubre todas sus superficies con cuñas absorbentes para eliminar el segundo y dejar solo el primero: reproduce el <b>campo libre</b>, la condición en la que se mide la potencia y la directividad de una fuente. El explorador calcula el nivel en función de la distancia, el radio hasta el que domina el campo directo y la frecuencia desde la que las cuñas funcionan.
  </div>

  <div class="card">
    <canvas id="cn" width="760" height="340" aria-label="Nivel de presión sonora en función de la distancia a la fuente"></canvas>
    <canvas id="cp" width="760" height="290" style="margin-top:10px" aria-label="Planta del recinto con el radio crítico"></canvas>
    <div class="legend">
      <span><i class="sw" style="border-top-color:var(--steel)"></i> nivel total</span>
      <span><i class="sw" style="border-top-color:var(--orange);border-top-style:dashed"></i> campo directo (campo libre)</span>
      <span><i class="sw" style="border-top-color:var(--green);border-top-style:dashed"></i> campo reverberante</span>
      <span><i class="sw" style="border-top-color:var(--purple);border-top-style:dashed"></i> radio crítico <i>r</i><sub>c</sub></span>
      <span><i class="sw" style="border-top-color:var(--red)"></i> micrófono</span>
    </div>
  </div>

  <div class="card">
    <h2>Controles</h2>
    <div class="grp"><div class="t">Fuente y micrófono</div>
      {fila("Nivel de potencia <i>L</i><sub>W</sub>", "LW", 60, 150, 1, 100, "dB")}
      {fila("Distancia <i>r</i>", "r", 0.1, 20, 0.1, 2, "m")}
      <div class="btns"><button class="btn on" data-q="1">Fuente suspendida (<i>Q</i> = 1)</button><button class="btn" data-q="2">Sobre piso reflejante (<i>Q</i> = 2)</button><button class="btn" data-q="4">En una arista (<i>Q</i> = 4)</button><button class="btn" data-q="8">En una esquina (<i>Q</i> = 8)</button></div>
    </div>
    <div class="grp"><div class="t">Recinto</div>
      {fila("Largo <i>L</i><sub>x</sub>", "Lx", 2, 30, 0.5, 8, "m")}
      {fila("Ancho <i>L</i><sub>y</sub>", "Ly", 2, 30, 0.5, 6, "m")}
      {fila("Alto <i>L</i><sub>z</sub>", "Lz", 2, 15, 0.5, 3, "m")}
      {fila("Absorción media ᾱ", "al", 0.01, 0.99, 0.01, 0.15)}
    </div>
    <div class="grp"><div class="t">Cuñas absorbentes</div>
      {fila("Profundidad de la cuña <i>d</i>", "dc", 0.05, 1.5, 0.05, 0.85, "m")}
      {fila("Frecuencia del ensayo <i>f</i>", "f", 20, 2000, 5, 250, "Hz")}
    </div>
    <div class="btns">
      <button class="btn" data-pre="A">Aula</button><button class="btn" data-pre="R">Cámara reverberante</button><button class="btn" data-pre="N">Cámara anecoica</button><button class="btn" data-pre="S">Cámara semianecoica</button>
      <button class="btn" id="pra">Ocultar lecturas (modo práctica)</button>
    </div>
    <div class="tiles t3" style="margin-top:10px">
      {tile("Nivel en el micrófono <i>L</i><sub>p</sub>", "olp", "hl")}{tile("Campo directo", "old")}{tile("Campo reverberante", "olr")}
      {tile("Desviación respecto del campo libre", "odev", "hl")}{tile("Radio crítico <i>r</i><sub>c</sub>", "orc")}{tile("Campo libre dentro de 1.5 dB hasta", "or15")}
      {tile("Constante del recinto <i>R</i>", "oR")}{tile("Tiempo de reverberación", "oT")}{tile("Frecuencia de corte de las cuñas", "ofc")}
    </div>
    <div class="nota" id="olect"></div>
  </div>

  <div class="card full">
    <h2>Las fórmulas en pantalla</h2>
    <div class="two"><div>
    {eq("1 · Campo libre: ley del inverso del cuadrado", M(r"L_p=L_W+10\log_{10}\frac{Q}{4\pi r^2}") + nota("<i>L</i><sub>W</sub> referido a 1 pW y <i>L</i><sub>p</sub> a 20 µPa, con <i>r</i> en metros y aire en condiciones normales; <i>Q</i> es el factor de directividad. Cada vez que <i>r</i> se duplica, el nivel baja 6 dB"))}
    {eq("2 · Recinto con campo directo y reverberante", M(r"L_p=L_W+10\log_{10}\left(\frac{Q}{4\pi r^2}+\frac{4}{R}\right),\qquad R=\frac{S\,\bar\alpha}{1-\bar\alpha}") + nota("<i>S</i> es el área total de las superficies y ᾱ su coeficiente de absorción medio; <i>R</i> es la constante del recinto, en m²"))}
    {eq("3 · Radio crítico", M(r"r_c=\sqrt{\frac{Q\,R}{16\pi}}") + nota("distancia a la que el campo directo y el reverberante tienen el mismo nivel; más lejos, acercar o alejar el micrófono casi no cambia la lectura"))}
    </div><div>
    {eq("4 · Desviación respecto del campo libre", M(r"\Delta=10\log_{10}\left(1+\frac{r^2}{r_c^2}\right)") + nota("la desviación no supera 1.5 dB mientras <i>r</i> ≤ 0.64 <i>r</i><sub>c</sub>; una tolerancia de ese orden es la que se exige para calificar una cámara"))}
    {eq("5 · Tiempo de reverberación (Eyring)", M(r"T_{60}=\frac{0.161\,V}{-S\,\ln(1-\bar\alpha)}") + nota("tiempo en el que el nivel cae 60 dB al apagar la fuente; con ᾱ pequeña se reduce a la fórmula de Sabine, 0.161 <i>V</i>/(<i>S</i>ᾱ)"))}
    {eq("6 · Frecuencia de corte de las cuñas", M(r"f_{\text{corte}}\approx\frac{c}{4\,d}") + nota("la cuña absorbe al menos 99 % de la energía incidente cuando su profundidad es del orden de un cuarto de la longitud de onda; por debajo, la cámara deja de ser anecoica"))}
    </div></div>
    <div class="intro" style="margin-top:12px"><b>Hipótesis y límites del modelo.</b> La ecuación 2 supone un campo reverberante difuso (energía uniforme y sin dirección preferente), lo que exige un recinto de proporciones regulares, absorción repartida y una frecuencia muy por encima de sus primeros modos; con ᾱ cercana a 1 ese campo deja de existir como tal y la fórmula solo indica el orden de magnitud del residuo. La fuente se toma como puntual, con directividad dada por su posición. La absorción ᾱ se fija con el deslizador y no depende de la frecuencia: la regla de un cuarto de onda indica desde qué frecuencia es válido suponer ᾱ ≈ 0.99 para unas cuñas dadas. No se incluye la absorción del aire.</div>
    <div class="takeaway" style="margin-top:10px"><b>Cómo explorar:</b> (1) «Aula»: con ᾱ = 0.15 el radio crítico queda en 0.79 m; el micrófono a 2 m lee 8.7 dB más que en campo libre, casi todo reflexiones. (2) «Cámara reverberante»: paredes duras (ᾱ = 0.02), radio crítico de 0.25 m y un nivel casi uniforme en toda la sala; así se mide la potencia total de una fuente y así se ensayan los satélites frente al ruido del lanzamiento. (3) «Cámara anecoica»: con ᾱ = 0.99 la curva total coincide con la recta de −6 dB por duplicación hasta las paredes. (4) En esa cámara, al bajar la frecuencia del ensayo por debajo de la frecuencia de corte de las cuñas (101 Hz con cuñas de 0.85 m) aparece el aviso: para ensayar a 50 Hz harían falta cuñas de 1.7 m. (5) «Cámara semianecoica»: el piso reflejante duplica la intensidad (<i>Q</i> = 2, +3 dB) y permite colocar vehículos y equipo pesado. (6) Al llevar la fuente a una esquina (<i>Q</i> = 8) el campo directo sube 9 dB. <b>Nota:</b> las cámaras anecoicas de radiofrecuencia, donde se miden antenas, aplican el mismo principio a las ondas electromagnéticas con absorbentes piramidales cargados de carbón; no son intercambiables con las acústicas. Referencias: Beranek y Sleeper, «The design and construction of anechoic sound chambers», <i>J. Acoust. Soc. Am.</i> 18, 140 (1946), <a href="https://doi.org/10.1121/1.1916351">doi:10.1121/1.1916351</a>; Kinsler, Frey, Coppens y Sanders, <i>Fundamentals of Acoustics</i>, 4.ª ed., Wiley, 2000, cap. 12; Bies, Hansen y Howard, <i>Engineering Noise Control</i>, 5.ª ed., CRC Press, 2017 (capítulo de sonido en recintos). Los criterios de calificación de una cámara deben leerse en la norma aplicable (ISO 3745; véase «Dónde consultar las normas»).</div>
  </div>
"""
script = LIB + r"""
let S={LW:100,r:2,Lx:8,Ly:6,Lz:3,al:0.15,dc:0.85,f:250,Q:1};
const UN={LW:' dB',r:' m',Lx:' m',Ly:' m',Lz:' m',al:'',dc:' m',f:' Hz'}, C0=343, L10=x=>10*Math.log10(x);
function calc(r){ r=r===undefined?S.r:r; const Sup=2*(S.Lx*S.Ly+S.Lx*S.Lz+S.Ly*S.Lz), V=S.Lx*S.Ly*S.Lz, R=Sup*S.al/(1-S.al), dir=S.Q/(4*Math.PI*r*r), rev=4/R, rc=Math.sqrt(S.Q*R/(16*Math.PI));
  return {Sup,V,R,rc,Lp:S.LW+L10(dir+rev),Ld:S.LW+L10(dir),Lr:S.LW+L10(rev),dev:L10(1+r*r/(rc*rc)),r15:rc*Math.sqrt(Math.pow(10,0.15)-1),T:0.161*V/(-Sup*Math.log(1-S.al)),fc:C0/(4*S.dc)}; }
function dibujar(){
  const q=calc(), g=lienzo($('cn'),340), y1=Math.ceil((S.LW+L10(S.Q/(4*Math.PI*0.01))+3)/10)*10, y0=Math.floor((Math.min(q.Lr,S.LW+L10(S.Q/(4*Math.PI*900)))-3)/10)*10;
  const e=ejes(g,{},{x0:0.1,x1:30,y0:Math.max(y0,y1-90),y1,logx:true,xl:'distancia a la fuente r (m)',yl:'nivel de presión sonora (dB)',tit:'Nivel en función de la distancia  ·  ᾱ = '+S.al+'  ·  Q = '+S.Q,ny:7});
  funcion(e,r=>S.LW+L10(S.Q/(4*Math.PI*r*r)),ORANGE,1.5,[6,4],200); hline(e,q.Lr,GREEN,[6,4],'reverberante: '+q.Lr.toFixed(1)+' dB');
  funcion(e,r=>calc(r).Lp,STEEL,2.6,null,300); vline(e,q.rc,PURPLE,[5,4],'r_c = '+(+q.rc.toPrecision(3))+' m'); punto(e,S.r,q.Lp,RED,5.5);
  let c=g.c; c.fillStyle=RED; c.font='bold 11px Arial'; c.textAlign=S.r>8?'right':'left'; c.textBaseline='bottom'; c.fillText(q.Lp.toFixed(1)+' dB',e.X(S.r)+(S.r>8?-8:8),e.Y(q.Lp)-6);
  // planta
  const g2=lienzo($('cp'),290); c=g2.c; const sc=Math.min((g2.W-60)/S.Lx,220/S.Ly), w=S.Lx*sc, h=S.Ly*sc, x0=(g2.W-w)/2, y0p=36+(220-h)/2;
  c.font='bold 12px Arial'; c.fillStyle=NAVY; c.textAlign='left'; c.textBaseline='top'; c.fillText('Planta del recinto: '+S.Lx+' m × '+S.Ly+' m (alto '+S.Lz+' m)',8,6);
  const gr=Math.max(3,Math.min(16,S.dc*sc))*(S.al>=0.9?1:0); c.fillStyle='#F6F8FC'; c.fillRect(x0,y0p,w,h);
  if(gr>0){ c.fillStyle='rgba(197,90,17,.30)'; const paso=Math.max(5,gr*0.7); for(let x=x0;x<x0+w-1;x+=paso){ const b=Math.min(paso,x0+w-x); c.beginPath(); c.moveTo(x,y0p); c.lineTo(x+b/2,y0p+gr); c.lineTo(x+b,y0p); c.fill(); c.beginPath(); c.moveTo(x,y0p+h); c.lineTo(x+b/2,y0p+h-gr); c.lineTo(x+b,y0p+h); c.fill(); }
    for(let y=y0p;y<y0p+h-1;y+=paso){ const b=Math.min(paso,y0p+h-y); c.beginPath(); c.moveTo(x0,y); c.lineTo(x0+gr,y+b/2); c.lineTo(x0,y+b); c.fill(); c.beginPath(); c.moveTo(x0+w,y); c.lineTo(x0+w-gr,y+b/2); c.lineTo(x0+w,y+b); c.fill(); } }
  c.strokeStyle='#7A8AA8'; c.lineWidth=S.al<0.1?3:1.5; c.strokeRect(x0,y0p,w,h);
  const fx=S.Q>=4?x0+gr+4:x0+w/2, fy=S.Q===8?y0p+gr+4:y0p+h/2;        // fuente: centro; arista y esquina, junto a la pared
  c.save(); c.beginPath(); c.rect(x0,y0p,w,h); c.clip();
  c.fillStyle='rgba(197,90,17,.10)'; c.beginPath(); c.arc(fx,fy,q.r15*sc,0,7); c.fill();
  c.strokeStyle=PURPLE; c.setLineDash([5,4]); c.lineWidth=1.5; c.beginPath(); c.arc(fx,fy,q.rc*sc,0,7); c.stroke(); c.setLineDash([]);
  const ang=S.Q>=4?(S.Q===8?Math.atan2(h,w):0):0, mx=fx+S.r*sc*Math.cos(ang), my=fy+S.r*sc*Math.sin(ang);
  c.strokeStyle=RED; c.lineWidth=1.2; c.beginPath(); c.moveTo(fx,fy); c.lineTo(mx,my); c.stroke(); c.restore();
  c.fillStyle=NAVY; c.beginPath(); c.arc(fx,fy,5,0,7); c.fill(); const dentro=mx<=x0+w&&my<=y0p+h; if(dentro){ c.fillStyle=RED; c.beginPath(); c.arc(mx,my,4.5,0,7); c.fill(); }
  c.fillStyle=GREY; c.font='11px Arial'; c.textAlign='left'; c.textBaseline='top'; c.fillText('zona sombreada: campo libre dentro de 1.5 dB'+(dentro?'':'  ·  el micrófono queda fuera del recinto'),8,270);
  // lecturas
  const d1=v=>v.toFixed(1)+' dB', m3=v=>(+v.toPrecision(3))+' m';
  $('olp').textContent=d1(q.Lp); $('old').textContent=d1(q.Ld); $('olr').textContent=d1(q.Lr); $('odev').textContent='+'+q.dev.toFixed(1)+' dB'; $('odev').parentNode.classList.toggle('al',q.dev>1.5);
  $('orc').textContent=m3(q.rc); $('or15').textContent=m3(q.r15); $('oR').textContent=(+q.R.toPrecision(3))+' m²'; $('oT').textContent=(+q.T.toPrecision(2))+' s'; $('ofc').textContent=(+q.fc.toPrecision(3))+' Hz';
  let a=[q.dev<=1.5?'El micrófono está en campo libre dentro de 1.5 dB: la lectura corresponde al campo directo.':S.r<q.rc?'Zona de transición: el campo directo todavía domina, pero las reflexiones ya suman más de 1.5 dB.':'El micrófono está más allá del radio crítico: la lectura corresponde sobre todo al campo reverberante y casi no depende de la distancia.'];
  if(S.al>=0.9) a.push(S.f>=q.fc?'A '+S.f+' Hz las cuñas de '+S.dc+' m trabajan por encima de su frecuencia de corte ('+(+q.fc.toPrecision(3))+' Hz): es válido suponer ᾱ ≈ 0.99.':'Atención: '+S.f+' Hz queda por debajo de la frecuencia de corte de las cuñas ('+(+q.fc.toPrecision(3))+' Hz). La absorción real es menor que la del deslizador y la cámara no es anecoica a esa frecuencia; harían falta cuñas de '+(C0/(4*S.f)).toFixed(2)+' m.');
  $('olect').textContent=a.join(' ');
}
liga(S,UN,dibujar); practica('pra');
function direct(n){ S.Q=n; document.querySelectorAll('[data-q]').forEach(b=>b.classList.toggle('on',+b.dataset.q===n)); }
document.querySelectorAll('[data-q]').forEach(b=>b.addEventListener('click',()=>{ direct(+b.dataset.q); dibujar(); }));
const PRE={A:{Lx:8,Ly:6,Lz:3,al:0.15,r:2,Q:1}, R:{Lx:6,Ly:5,Lz:4,al:0.02,r:2,Q:1}, N:{Lx:6,Ly:5,Lz:4,al:0.99,r:2,dc:0.85,f:250,Q:1}, S:{Lx:6,Ly:5,Lz:4,al:0.99,r:2,dc:0.85,f:250,Q:2}};
document.querySelectorAll('[data-pre]').forEach(b=>b.addEventListener('click',()=>{ const o=Object.assign({},PRE[b.dataset.pre]); direct(o.Q); delete o.Q; pon(S,UN,o,dibujar); }));
window.addEventListener('resize',dibujar);
window.__an={S,calc};
dibujar();
"""
pagina("anecoica_interactivo.html", "Campo libre y cámara anecoica", "Vibraciones · Pilar 19 · U6",
       "Al variar la absorción del recinto y la distancia a la fuente se observa dónde termina el campo libre y empieza el reverberante, y desde qué frecuencia unas cuñas hacen anecoica una cámara",
       cuerpo, script, "Explorador didáctico del campo libre, el campo reverberante y las cámaras anecoicas · material de apoyo del curso de Vibraciones · funciona sin conexión (un solo archivo).")
