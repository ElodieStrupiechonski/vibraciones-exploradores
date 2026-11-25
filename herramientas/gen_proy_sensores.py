#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera proy_sensores.html · Apoyo a los proyectos · ¿Mi teléfono puede medirlo? (acelerómetro, micrófono,
magnetómetro y cámara). Uso: python3 gen_proy_sensores.py CARPETA"""
from base_pag import *

cuerpo = f"""
<style>
  table.sens{{border-collapse:collapse;width:100%;font-size:13.5px}} table.sens th,table.sens td{{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}}
  table.sens th{{color:var(--navy);font-size:12.5px}} .ok{{color:var(--green);font-weight:700}} .med{{color:var(--orange);font-weight:700}} .no{{color:var(--red);font-weight:700}}
  .reco{{border-left:3px solid var(--green);background:#EEF7F0;padding:8px 12px;border-radius:0 8px 8px 0;margin-top:10px;line-height:1.5}}
  .tw{{overflow-x:auto}}
</style>
  <div class="intro full">
    <b>¿Qué resuelve?</b> Antes de medir conviene saber si el teléfono puede ver la vibración que buscamos y con qué sensor. Se escriben la frecuencia esperada, la amplitud, el amortiguamiento y la duración del registro, y la página revisa para cada sensor (acelerómetro, micrófono, magnetómetro y cámara) cuatro condiciones: <b>muestreo</b> (la frecuencia queda por debajo de la de Nyquist o aparece como alias), <b>señal</b> (la aceleración supera el ruido del sensor), <b>carga</b> (la masa del teléfono no cambia lo que se mide) y <b>resolución</b> (el registro alcanza para medir la frecuencia y el amortiguamiento).
  </div>

  <div class="card">
    <canvas id="cb" width="760" height="290" aria-label="Bandas de frecuencia de cada sensor y frecuencia buscada"></canvas>
    <div class="legend">
      <span><i class="sw" style="border-top-color:var(--steel)"></i> banda útil de cada sensor (tono fuerte: hasta 0.8 de Nyquist; tenue: hasta Nyquist; naranja en el micrófono: zona que muchos teléfonos filtran)</span>
      <span><i class="sw" style="border-top-color:var(--red)"></i> frecuencia buscada</span>
      <span><i class="sw" style="border-top-color:var(--orange);border-top-style:dashed"></i> frecuencia con el teléfono montado</span>
      <span><i class="sw" style="border-top-color:var(--purple)"></i> alias, donde aparecería</span>
    </div>
    <div class="tw" style="margin-top:10px"><table class="sens" id="tabla"></table></div>
    <div class="reco" id="reco"></div>
  </div>

  <div class="card">
    <h2>Controles</h2>
    <div class="btns"><button class="btn" data-pre="A">Equipo A: plataforma</button><button class="btn" data-pre="B">Equipo B: probeta</button><button class="btn" data-pre="C">Equipo C: segueta</button></div>
    <div class="grp"><div class="t">La vibración</div>
      {fila("Frecuencia esperada <i>f</i>", "f", 0.5, 2000, 0.1, 6, "Hz")}
      {fila("Amplitud de desplazamiento <i>X</i>", "X", 0.001, 30, 0.001, 0.5, "mm")}
      {fila("Amortiguamiento ζ", "z", 0.001, 0.3, 0.001, 0.05)}
      {fila("Duración del registro <i>T</i>", "T", 1, 300, 1, 20, "s")}
    </div>
    <div class="grp"><div class="t">El teléfono</div>
      {fila("Muestreo del acelerómetro", "fa", 50, 1000, 1, 200, "Hz")}
      {fila("Ruido del acelerómetro (rms)", "na", 0.002, 0.2, 0.001, 0.02, "m/s²")}
      {fila("Muestreo del magnetómetro", "fm", 10, 200, 1, 50, "Hz")}
      {fila("Cuadros por segundo del video", "fps", 24, 960, 1, 240, "")}
      {fila("Masa del teléfono", "mt", 100, 300, 1, 190, "g")}
      {fila("Masa efectiva de la pieza que vibra", "me", 0.1, 5000, 0.1, 300, "g")}
      <div class="btns"><button class="btn on" data-mont="1">El teléfono va sobre la pieza</button><button class="btn" data-mont="0">El teléfono está aparte</button></div>
    </div>
    <div class="nota">El muestreo real del acelerómetro y del magnetómetro se lee en Phyphox: al abrir un experimento de sensor, el ícono «i» o la pestaña de datos muestran la frecuencia de muestreo. El ruido se mide dejando el teléfono quieto 10 s sobre la mesa: es la desviación estándar de la aceleración.</div>
  </div>

  <div class="card full">
    <h2>Las fórmulas en pantalla</h2>
    <div class="two"><div>
    {eq("1 · Muestreo y alias", M(r"f_{\mathrm{Nyq}}=\frac{f_s}{2},\qquad f_{\mathrm{alias}}=\left|f-k\,f_s\right|,\ \ k=\text{entero más cercano a}\ f/f_s") + nota("conviene quedarse por debajo de 0.8 <i>f</i><sub>Nyq</sub>: cerca del límite el filtro interno del teléfono atenúa la señal"))}
    {eq("2 · Señal frente a ruido", M(r"a_{\mathrm{rms}}=\frac{(2\pi f)^2X}{\sqrt2},\qquad \mathrm{SNR}=20\log_{10}\frac{a_{\mathrm{rms}}}{\sigma_{\mathrm{ruido}}}") + nota("con menos de 10 dB la línea espectral se confunde con el ruido; con más de 20 dB se lee sin dificultad"))}
    {eq("3 · Carga de masa", M(r"f'=f\sqrt{\frac{m_{\mathrm{ef}}}{m_{\mathrm{ef}}+m_{\mathrm{tel}}}}") + nota("vale si el teléfono queda en el punto que más se mueve; si la pieza pesa menos que el teléfono, el teléfono no puede ir montado"))}
    </div><div>
    {eq("4 · Resolución y duración", M(r"\Delta f=\frac1T,\qquad \text{media potencia con 4 puntos:}\ \ T\geq\frac{2}{\zeta f}") + nota("el ancho del pico es 2ζ<i>f</i>; con Δ<i>f</i> mayor, la FFT no lo resuelve"))}
    {eq("5 · Cuánto dura un decaimiento", M(r"t_{5\%}=\frac{\ln20}{2\pi\zeta f}=\frac{0.477}{\zeta f}") + nota("como <i>t</i><sub>5 %</sub> es siempre menor que 2/(ζ<i>f</i>), un solo golpe nunca alcanza para la media potencia: en un decaimiento, ζ se mide con el decremento"))}
    {eq("6 · Imán frente al magnetómetro (eje del imán)", M(r"B(r)\approx\frac{\mu_0}{2\pi}\frac{m}{r^3},\qquad m=\frac{B_rV}{\mu_0},\qquad \Delta B\approx3B\,\frac{X}{r}") + nota("aproximación de dipolo, válida para <i>r</i> varias veces mayor que el imán"))}
    </div></div>
    <div class="intro" style="margin-top:12px"><b>Cuatro reglas prácticas.</b> (1) <b>Acelerómetro</b> para lo lento y pesado: plataformas, placas y estructuras por debajo de unos 0.4 <i>f</i><sub>s</sub>, con el teléfono bien sujeto (cinta doble cara o liga, nunca suelto). (2) <b>Micrófono</b> para lo rápido y ligero que suena: probetas, hojas y láminas golpeadas por encima de unos 100 Hz; el teléfono no toca la pieza, así que no la carga. Muchos micrófonos de teléfono filtran por debajo de unos 50 a 100 Hz. (3) <b>Magnetómetro</b> cuando la pieza lleva un imán: el teléfono se queda aparte a unos centímetros, mide el movimiento sin tocarlo y no lo carga; hay que alejarlo si satura. (4) <b>Cámara en cámara lenta</b> para frecuencias bajas y amplitudes visibles, analizando el video con un programa de seguimiento como Tracker. En los cuatro casos: varias repeticiones y anotar el muestreo real. Referencias: Staacks, Hütz, Heinke y Stampfer, «Advanced tools for smartphone-based experiments: phyphox», <i>Phys. Educ.</i> 53, 045009 (2018), doi:10.1088/1361-6552/aac05e; Welch, «The use of fast Fourier transform for the estimation of power spectra», <i>IEEE Trans. Audio Electroacoust.</i> 15, 70–73 (1967), doi:10.1109/TAU.1967.1161901.</div>
  </div>
"""
script = LIB + r"""
let S={f:6,X:0.5,z:0.05,T:20,fa:200,na:0.02,fm:50,fps:240,mt:190,me:300,mont:1};
const UN={f:' Hz',X:' mm',z:'',T:' s',fa:' Hz',na:' m/s²',fm:' Hz',fps:'',mt:' g',me:' g'}, TP=2*Math.PI;
function alias(f,fs){ const k=Math.round(f/fs); return Math.abs(f-k*fs); }
function calc(){
  const f=S.f, X=S.X*1e-3, w=TP*f, arms=w*w*X/Math.SQRT2, snr=20*Math.log10(arms/S.na);
  const carga=S.mont? f*Math.sqrt(S.me/(S.me+S.mt)) : f, dcarga=(1-carga/f)*100;
  const Tmin=2/(S.z*f), t5=Math.log(20)/(TP*S.z*f), df=1/S.T;
  const sens=[{n:'Acelerómetro',fs:S.fa,monta:true},{n:'Micrófono',fs:48000,monta:false},{n:'Magnetómetro',fs:S.fm,monta:false},{n:'Cámara (video)',fs:S.fps,monta:false}];
  sens.forEach(s=>{ const fv=s.monta?carga:f; s.ny=s.fs/2; s.ok=fv<=0.8*s.ny; s.borde=!s.ok&&fv<s.ny; s.al=fv>=s.ny?alias(fv,s.fs):null; s.fv=fv; });
  return {f,arms,snr,carga,dcarga,Tmin,t5,df,sens,ptsHP:2*S.z*f*S.T};
}
function est(c,t){ return '<span class="'+c+'">'+t+'</span>'; }
function dibujar(){
  const q=calc(), g=lienzo($('cb'),290), e=ejes(g,{mL:110,mR:16,mT:26,mB:36},{x0:0.5,x1:50000,y0:0,y1:4.4,logx:true,xl:'frecuencia (Hz)',tit:'¿Dónde cae la vibración en la banda de cada sensor?',ny:1});
  const c=g.c, fil=[...q.sens].reverse();
  fil.forEach((s,i)=>{ const y0=e.Y(i+0.75), y1=e.Y(i+0.25), xa=e.X(0.5), xb=e.X(Math.min(50000,0.8*s.ny)), xn=e.X(Math.min(50000,s.ny));
    c.fillStyle='rgba(68,114,196,.28)'; c.fillRect(xa,y0,xb-xa,y1-y0); c.fillStyle='rgba(68,114,196,.10)'; c.fillRect(xb,y0,xn-xb,y1-y0);
    if(s.n==='Micrófono'){ c.fillStyle='rgba(197,90,17,.18)'; c.fillRect(xa,y0,e.X(80)-xa,y1-y0); }
    c.fillStyle=NAVY; c.font='bold 12px Arial'; c.textAlign='right'; c.textBaseline='middle'; c.fillText(s.n.replace(' (video)',''),e.px-8,(y0+y1)/2);
    if(s.al!==null&&s.al>0.5){ c.fillStyle=PURPLE; c.beginPath(); c.arc(e.X(s.al),(y0+y1)/2,5,0,7); c.fill(); c.font='11px Arial'; c.textAlign='left'; c.fillText('alias '+(+s.al.toPrecision(3))+' Hz',e.X(s.al)+8,(y0+y1)/2); } });
  vline(e,q.f,RED,[],'f = '+(+q.f.toPrecision(4))+' Hz'); if(S.mont&&q.dcarga>0.5) vline(e,q.carga,ORANGE,[5,4],'',14);
  // tabla
  const fila=(s)=>{ const mu=s.ok?est('ok','sí'):s.borde?est('med','cerca del límite'):est('no','no: alias en '+(+s.al.toPrecision(3))+' Hz');
    let sen='', car='';
    if(s.n==='Acelerómetro'){ sen=(q.snr>=20?est('ok','clara'):q.snr>=10?est('med','justa'):est('no','débil'))+' · '+(+q.arms.toPrecision(3))+' m/s² rms, '+q.snr.toFixed(0)+' dB'; car=S.mont?(q.dcarga<2?est('ok','despreciable'):q.dcarga<10?est('med','baja '+q.dcarga.toFixed(1)+' %'):est('no','baja '+q.dcarga.toFixed(0)+' %: no montar'))+(q.dcarga>=2?' ('+(+q.carga.toPrecision(3))+' Hz)':''):est('ok','no aplica'); }
    if(s.n==='Micrófono'){ sen=q.f<80?est('no','casi nula por debajo de unos 80 Hz'):est('ok','si la pieza suena'); car=est('ok','ninguna (no la toca)'); }
    if(s.n==='Magnetómetro'){ sen=est('med','sólo con un imán en la pieza'); car=est('ok','ninguna (a distancia)'); }
    if(s.n==='Cámara (video)'){ sen=S.X>=1?est('ok','visible ('+S.X+' mm)'):est('med','amplitud pequeña para video'); car=est('ok','ninguna'); }
    return '<tr><td><b>'+s.n+'</b></td><td>'+(+s.fs.toPrecision(4))+' Hz</td><td>'+(+s.ny.toPrecision(4))+' Hz</td><td>'+mu+'</td><td>'+sen+'</td><td>'+car+'</td></tr>'; };
  $('tabla').innerHTML='<tr><th>Sensor</th><th>Muestreo</th><th>Nyquist</th><th>¿Lo muestrea?</th><th>Señal</th><th>Carga de masa</th></tr>'+q.sens.map(fila).join('');
  // recomendación
  const acc=q.sens[0], mic=q.sens[1], mag=q.sens[2], cam=q.sens[3]; let r=[];
  const accOk=acc.ok&&q.snr>=10&&(!S.mont||q.dcarga<5);
  if(accOk) r.push('<b>Acelerómetro:</b> sirve'+(S.mont?' con el teléfono bien sujeto a la pieza.':'.'));
  else if(acc.ok&&S.mont&&q.dcarga>=5) r.push('<b>Acelerómetro:</b> la frecuencia cabe, pero el teléfono carga la pieza ('+q.dcarga.toFixed(0)+' % menos de frecuencia): sólo si se corrige con <i>f</i>′ o si se mide algo más pesado.');
  else if(acc.ok) r.push('<b>Acelerómetro:</b> la frecuencia cabe, pero la señal es débil ('+q.snr.toFixed(0)+' dB): aumentar la amplitud o promediar varios registros.');
  else r.push('<b>Acelerómetro:</b> no sirve a esta frecuencia'+(acc.al!==null?' (el pico aparecería en '+(+acc.al.toPrecision(3))+' Hz, un alias).':'.'));
  if(mic.ok&&q.f>=80) r.push('<b>Micrófono:</b> buena opción si la pieza suena al golpearla; no la toca y muestrea a 48 kHz.');
  if(mag.ok) r.push('<b>Magnetómetro:</b> opción sin contacto si se pega un imán pequeño a la pieza o si ya lo lleva.');
  if(cam.ok&&S.X>=1) r.push('<b>Video en cámara lenta:</b> sirve para contar ciclos y comprobar la frecuencia.');
  r.push(S.T>=q.Tmin?'<b>Resolución:</b> con <i>T</i> = '+S.T+' s hay '+q.ptsHP.toFixed(1)+' puntos dentro del ancho de media potencia; alcanza.':'<b>Resolución:</b> para la media potencia hace falta <i>T</i> ≥ '+(+q.Tmin.toPrecision(3))+' s (ahora hay '+q.ptsHP.toFixed(1)+' puntos en el pico). Si es un golpe, el decaimiento dura unos '+(+q.t5.toPrecision(2))+' s: usar el decremento logarítmico para ζ.');
  $('reco').innerHTML=r.join('<br>');
}
liga(S,UN,dibujar);
function monta(v){ S.mont=v; document.querySelectorAll('[data-mont]').forEach(b=>b.classList.toggle('on',+b.dataset.mont===v)); }
document.querySelectorAll('[data-mont]').forEach(b=>b.addEventListener('click',()=>{ monta(+b.dataset.mont); dibujar(); }));
const PRE={A:[{f:6,X:0.5,z:0.05,T:20,me:300},1], B:[{f:314,X:0.05,z:0.02,T:2,me:0.3},0], C:[{f:7,X:10,z:0.005,T:20,me:25.3},0]};
document.querySelectorAll('[data-pre]').forEach(b=>b.addEventListener('click',()=>{ const p=PRE[b.dataset.pre]; monta(p[1]); pon(S,UN,p[0],dibujar); }));
window.addEventListener('resize',dibujar);
window.__se={S,calc};
dibujar();
"""
pagina("proy_sensores.html", "¿Mi teléfono puede medirlo?", "Vibraciones · Apoyo a los proyectos",
       "Con la frecuencia, la amplitud y el amortiguamiento esperados se revisa qué sensor del teléfono sirve: acelerómetro, micrófono, magnetómetro o cámara",
       cuerpo, script, "Apoyo a los proyectos del curso de Vibraciones: elección del sensor del teléfono · funciona sin conexión (un solo archivo).")
