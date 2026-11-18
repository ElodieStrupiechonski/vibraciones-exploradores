#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera modal_interactivo.html · Pilar 15 · Extracción de parámetros modales (U7, tema 7.3; U3, tema 3.2).
Uso: python3 gen_modal.py CARPETA"""
from base_pag import *

cuerpo = f"""
  <div class="intro full">
    <b>¿Qué muestra?</b> De un ensayo de impacto o de un barrido se obtiene la <b>función de respuesta en frecuencia</b> (FRF) <i>H</i>(<i>f</i>) = <i>X</i>/<i>F</i>, un número complejo por cada frecuencia medida. Aquí la FRF es sintética (dos modos y ruido de medición), de manera que se conocen los valores verdaderos. Se elige una banda alrededor de un pico y se extraen <i>f</i><sub>n</sub> y ζ por tres métodos: <b>pico y media potencia</b>, <b>ajuste de círculo</b> en el plano de Nyquist y <b>recta de la FRF inversa</b>. La tabla compara cada resultado con el valor verdadero.
  </div>

  <div class="card">
    <canvas id="cm" width="760" height="330" aria-label="Magnitud de la FRF con la banda de análisis"></canvas>
    <div class="legend">
      <span><i class="sw" style="border-top-color:var(--steel)"></i> |<i>H</i>| medida</span>
      <span><i class="sw" style="border-top-color:var(--orange);border-top-style:dashed"></i> modelo de 1 GDL con los parámetros del círculo</span>
      <span><i class="sw" style="border-top-color:var(--green);border-top-style:dashed"></i> <i>f</i><sub>n</sub> verdaderas</span>
      <span><i class="sw" style="border-top-color:var(--red)"></i> puntos de media potencia</span>
    </div>
    <canvas id="cn" width="760" height="330" style="margin-top:10px" aria-label="Diagrama de Nyquist con el círculo ajustado y rectas de la FRF inversa"></canvas>
  </div>

  <div class="card">
    <h2>Controles</h2>
    <div class="grp"><div class="t">Estructura (valores verdaderos)</div>
      {fila("Modo 1: <i>f</i><sub>1</sub>", "f1", 5, 90, 0.1, 20, "Hz")}
      {fila("Modo 1: ζ<sub>1</sub>", "z1", 0.002, 0.2, 0.001, 0.02)}
      {fila("Modo 2: <i>f</i><sub>2</sub>", "f2", 5, 95, 0.1, 60, "Hz")}
      {fila("Modo 2: ζ<sub>2</sub>", "z2", 0.002, 0.2, 0.001, 0.01)}
      {fila("Modo 2: constante modal <i>A</i><sub>2</sub>/<i>A</i><sub>1</sub>", "a2", 0, 3, 0.05, 1)}
    </div>
    <div class="grp"><div class="t">Medición</div>
      {fila("Duración del registro <i>T</i>", "T", 1, 100, 0.5, 10, "s")}
      {fila("Ruido (% del pico mayor)", "ns", 0, 10, 0.1, 0.5, "%")}
    </div>
    <div class="grp"><div class="t">Banda de análisis</div>
      {fila("Centro <i>f</i><sub>c</sub>", "fc", 5, 95, 0.1, 20, "Hz")}
      {fila("Semiancho <i>b</i>", "b", 0.2, 20, 0.1, 2, "Hz")}
      <div class="btns"><button class="btn" id="c1">Centrar en el modo 1</button><button class="btn" id="c2">Centrar en el modo 2</button></div>
    </div>
    <div class="btns" style="margin-bottom:8px"><button class="btn" id="nr">Nueva realización del ruido</button><button class="btn" id="pra">Ocultar lecturas (modo práctica)</button>
    </div>
    <div class="btns">
      <button class="btn" data-pre="U">Un solo modo</button><button class="btn" data-pre="S">Modos separados</button><button class="btn" data-pre="C">Modos cercanos</button><button class="btn" data-pre="R">Resolución insuficiente</button><button class="btn" data-pre="N">Mucho ruido</button>
    </div>
    <div class="tiles t3" style="margin-top:10px">
      {tile("Resolución Δ<i>f</i> = 1/<i>T</i>", "odf")}{tile("Puntos en la banda", "onp")}{tile("Ancho de media potencia 2ζ<i>f</i><sub>n</sub>", "obw")}
      {tile("Puntos dentro de ese ancho", "onb", "hl")}{tile("Separación modal / ancho", "osep")}{tile("Diámetro del círculo", "odia")}
    </div>
    <div style="overflow-x:auto;margin-top:10px"><table class="tb res" id="res"></table></div>
    <div class="nota" id="aviso"></div>
    <div class="nota"><b>Glosario.</b> Receptancia: desplazamiento por unidad de fuerza. Constante modal <i>A</i><sub>r</sub>: peso de cada modo en la FRF (1/kg). Separación modal / ancho: distancia entre las dos frecuencias naturales dividida entre el mayor ancho de media potencia; por debajo de 2 los picos se traslapan.</div>
  </div>

  <div class="card full">
    <h2>Las fórmulas en pantalla</h2>
    <div class="two"><div>
    {eq("1 · Receptancia de una estructura con dos modos", M(r"H(\omega)=\frac{X}{F}=\sum_{r=1}^{2}\frac{A_r}{\omega_r^2-\omega^2+i\,2\zeta_r\omega_r\omega}") + nota("<i>A</i><sub>r</sub> es la constante modal (1/kg para un modo normalizado con la masa)"))}
    {eq("2 · Pico y media potencia", M(r"f_n\approx f_{\text{pico}},\qquad \zeta\approx\frac{f_b-f_a}{2f_n},\qquad |H(f_a)|=|H(f_b)|=\frac{|H|_{\max}}{\sqrt2}") + nota("válido si ζ ≪ 1 y si hay al menos cuatro o cinco puntos entre <i>f</i><sub>a</sub> y <i>f</i><sub>b</sub>"))}
    {eq("3 · Recta de la FRF inversa (un solo modo)", M(r"\frac{1}{H}=\frac{\omega_r^2-\omega^2}{A}+i\,\frac{2\zeta\omega_r}{A}\,\omega") + nota("la parte real es una recta en ω<sup>2</sup> (pendiente −1/<i>A</i>, cruce por cero en ω<sub>r</sub><sup>2</sup>); la imaginaria es una recta en ω que pasa por el origen. Supone <i>A</i> real (modos normales)"))}
    </div><div>
    {eq("4 · Círculo de Nyquist de un modo", M(r"\text{diámetro}\approx\frac{A}{2\zeta\omega_r^2},\qquad \tan\frac{\theta}{2}\approx\frac{\omega_r^2-\omega^2}{2\zeta\omega_r^2}") + nota("θ es el ángulo visto desde el centro, medido desde el punto de resonancia; tan(θ/2) es una recta en ω<sup>2</sup>. Con amortiguamiento viscoso la receptancia describe una circunferencia solo de forma aproximada (ζ ≪ 1); es exacta para la movilidad, o para la receptancia con amortiguamiento histerético"))}
    {eq("5 · Ajuste del círculo por mínimos cuadrados", M(r"x^2+y^2=2x_c\,x+2y_c\,y+\left(R^2-x_c^2-y_c^2\right)") + nota("lineal en las incógnitas <i>x</i><sub>c</sub>, <i>y</i><sub>c</sub> y <i>R</i><sup>2</sup> − <i>x</i><sub>c</sub><sup>2</sup> − <i>y</i><sub>c</sub><sup>2</sup>; el residuo de los demás modos solo desplaza el círculo"))}
    {eq("6 · Resolución necesaria", M(r"\Delta f=\frac{1}{T}\leq\frac{2\zeta f_n}{4}\qquad\Rightarrow\qquad T\geq\frac{2}{\zeta f_n}") + nota("criterio práctico: al menos cuatro intervalos dentro del ancho de media potencia"))}
    </div></div>
    <div class="intro" style="margin-top:12px"><b>Lectura para el ensayo.</b> El método de media potencia usa tres puntos de la curva y depende de la resolución y de dónde cae el pico entre dos líneas espectrales; el círculo y la recta usan todos los puntos de la banda y promedian el ruido. La recta de la FRF inversa supone que en la banda solo responde un modo y, como invierte <i>H</i>, amplifica el ruido de los puntos alejados de la resonancia, donde |<i>H</i>| es pequeña. El círculo absorbe la cola de los demás modos como un desplazamiento casi constante, por lo que resiste mejor los modos cercanos. Como criterio práctico, cuando dos modos están a menos de dos anchos de media potencia ningún método de un grado de libertad es fiable y se recurre a un ajuste de varios modos. <b>Hipótesis:</b> sistema lineal, modos reales y FRF muestreada sin fuga (la duración del registro solo fija Δ<i>f</i>); el segundo modo se trata con detalle en el explorador de dos grados de libertad.</div>
    <div class="takeaway" style="margin-top:10px"><b>Cómo explorar:</b> (1) con «Un solo modo» y la banda en 20 ± 2 Hz los tres métodos recuperan <i>f</i><sub>1</sub> = 20 Hz y ζ<sub>1</sub> = 0.02 con error menor que 1 %. (2) Con «Modos separados» aparece un segundo modo en 60 Hz: su cola es casi constante en la banda y los tres resultados apenas cambian. (3) Con «Modos cercanos» (20 y 23 Hz) la recta de la FRF inversa sobrestima ζ a más del doble, mientras que el círculo se mantiene a unos 5 %. (4) Con «Resolución insuficiente» (<i>T</i> = 2 s, Δ<i>f</i> = 0.5 Hz, <i>f</i><sub>1</sub> = 20.25 Hz, de modo que el pico cae entre dos líneas espectrales) la media potencia sobrestima ζ cerca de 30 %; el círculo y la recta, que usan toda la banda, conservan un error del orden de 1 %. (5) Con «Mucho ruido», al pulsar varias veces «Nueva realización del ruido» la media potencia oscila del orden de ±10 % y el círculo menos de la mitad. (6) Para practicar: «Ocultar lecturas», estimar <i>f</i><sub>n</sub> y ζ sobre la gráfica con los puntos de media potencia y comprobar. Referencias: Ewins, <i>Modal Testing: Theory, Practice and Application</i>, 2.ª ed., Research Studies Press, 2000, caps. 2 y 4; Inman, <i>Engineering Vibration</i>, 4.ª ed., cap. 7; Dobson (1987), «A straight-line technique for extracting modal properties from frequency response data», Mech. Syst. Signal Process. 1(1), 29–40, <a href="https://doi.org/10.1016/0888-3270(87)90081-1">doi:10.1016/0888-3270(87)90081-1</a>.</div>
  </div>
"""
script = LIB + r"""
let S={f1:20,z1:0.02,f2:60,z2:0.01,a2:1,T:10,ns:0.5,fc:20,b:2};
const UN={f1:' Hz',z1:'',f2:' Hz',z2:'',a2:'',T:' s',ns:' %',fc:' Hz',b:' Hz'}, FMAX=100, TP=2*Math.PI;
function rng(seed){ let a=seed>>>0; return function(){ a|=0; a=a+0x6D2B79F5|0; let t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }
function Hmodo(f,fr,z,A){ const w=TP*f, wr=TP*fr, dr=wr*wr-w*w, di=2*z*wr*w, d=dr*dr+di*di; return [A*dr/d,-A*di/d]; }
function Hteo(f){ const a=Hmodo(f,S.f1,S.z1,1), b=Hmodo(f,S.f2,S.z2,S.a2); return [a[0]+b[0],a[1]+b[1]]; }
let SEM=20261118;
function medir(){ const df=1/S.T, n=Math.floor(FMAX/df), f=new Float64Array(n), re=new Float64Array(n), im=new Float64Array(n), u=rng(SEM); let mx=0;
  for(let k=0;k<n;k++){ f[k]=(k+1)*df; const h=Hteo(f[k]); re[k]=h[0]; im[k]=h[1]; mx=Math.max(mx,Math.hypot(h[0],h[1])); }
  const sg=S.ns/100*mx/Math.SQRT2; for(let k=0;k<n;k++){ const r=Math.sqrt(-2*Math.log(1-u())), t=TP*u(); re[k]+=sg*r*Math.cos(t); im[k]+=sg*r*Math.sin(t); }
  return {f,re,im,df,n,mx}; }
function recta(x,y){ const n=x.length; let sx=0,sy=0,sxx=0,sxy=0; for(let i=0;i<n;i++){ sx+=x[i]; sy+=y[i]; sxx+=x[i]*x[i]; sxy+=x[i]*y[i]; } const d=n*sxx-sx*sx, m=(n*sxy-sx*sy)/d; return [m,(sy-m*sx)/n]; }
function resolver3(M,v){ // eliminación de Gauss 3×3
  const A=M.map((r,i)=>r.concat(v[i])); for(let i=0;i<3;i++){ let p=i; for(let j=i+1;j<3;j++) if(Math.abs(A[j][i])>Math.abs(A[p][i])) p=j; [A[i],A[p]]=[A[p],A[i]]; for(let j=i+1;j<3;j++){ const q=A[j][i]/A[i][i]; for(let k=i;k<4;k++) A[j][k]-=q*A[i][k]; } }
  const x=[0,0,0]; for(let i=2;i>=0;i--){ let s=A[i][3]; for(let k=i+1;k<3;k++) s-=A[i][k]*x[k]; x[i]=s/A[i][i]; } return x; }
function extraer(D){
  const i0=D.f.findIndex(v=>v>=S.fc-S.b-1e-9); let i1=D.n-1; while(i1>0&&D.f[i1]>S.fc+S.b+1e-9) i1--; const np=i1-i0+1; if(i0<0||np<5) return {np:Math.max(0,np),i0,i1};
  const f=D.f.subarray(i0,i1+1), re=D.re.subarray(i0,i1+1), im=D.im.subarray(i0,i1+1), m=Array.from(f,(_,i)=>Math.hypot(re[i],im[i]));
  // --- 1 · pico (parábola en ln|H|) y media potencia (interpolación lineal)
  let k=0; for(let i=1;i<np;i++) if(m[i]>m[k]) k=i; let fp=f[k], mp=m[k];
  if(k>0&&k<np-1){ const y0=Math.log(m[k-1]), y1=Math.log(m[k]), y2=Math.log(m[k+1]), d=0.5*(y0-y2)/(y0-2*y1+y2); fp=f[k]+d*D.df; mp=Math.exp(y1-0.25*(y0-y2)*d); }
  const hp=mp/Math.SQRT2; let i=k, fa=NaN, fb=NaN; while(i>0&&m[i]>hp) i--; if(m[i]<=hp) fa=f[i]+(hp-m[i])/(m[i+1]-m[i])*D.df;
  i=k; while(i<np-1&&m[i]>hp) i++; if(m[i]<=hp) fb=f[i-1]+(hp-m[i-1])/(m[i]-m[i-1])*D.df;
  const P={fn:fp,z:(fb-fa)/(2*fp),fa,fb,hp,mp};
  // --- 2 · recta de la FRF inversa
  const w=Array.from(f,v=>TP*v), w2=w.map(v=>v*v), gr=[], gi=[]; for(let j=0;j<np;j++){ const d=re[j]*re[j]+im[j]*im[j]; gr.push(re[j]/d); gi.push(-im[j]/d); }
  let swg=0, sww=0; for(let j=0;j<np;j++){ swg+=w[j]*gi[j]; sww+=w[j]*w[j]; }                 // Im(1/H) = (2ζω_r/A)·ω: recta por el origen
  const pr=recta(w2,gr), pi=[swg/sww,0], Ai=-1/pr[0], wri=Math.sqrt(pr[1]*Ai), I={fn:wri/TP,z:pi[0]*Ai/(2*wri),A:Ai,pr,pi,w,w2,gr,gi};
  // --- 3 · círculo por mínimos cuadrados y recta de tan(θ/2) en ω²
  const N=[[0,0,0],[0,0,0],[0,0,0]], v=[0,0,0]; for(let j=0;j<np;j++){ const r=[re[j],im[j],1], q=re[j]*re[j]+im[j]*im[j]; for(let a=0;a<3;a++){ v[a]+=r[a]*q; for(let b2=0;b2<3;b2++) N[a][b2]+=r[a]*r[b2]; } }
  const s=resolver3(N,v), xc=s[0]/2, yc=s[1]/2, R=Math.sqrt(s[2]+xc*xc+yc*yc), xx=[], yy=[];
  for(let j=0;j<np;j++){ const th=Math.atan2(re[j]-xc,-(im[j]-yc)); if(Math.abs(th)<2.2){ xx.push(w2[j]); yy.push(Math.tan(th/2)); } }
  let C={xc,yc,R,fn:NaN,z:NaN,A:NaN}; if(xx.length>=3){ const pt=recta(xx,yy), wr2=-pt[1]/pt[0], zc=-1/(2*wr2*pt[0]); C={xc,yc,R,fn:Math.sqrt(wr2)/TP,z:zc,A:2*R*2*zc*wr2}; }
  return {np,i0,i1,f,re,im,m,P,I,C};
}
let D=null, E=null;
function verdad(){ return Math.abs(S.fc-S.f1)<=Math.abs(S.fc-S.f2)||S.a2===0 ? {fn:S.f1,z:S.z1,n:1} : {fn:S.f2,z:S.z2,n:2}; }
function dibujar(){
  D=medir(); E=extraer(D); const V=verdad();
  // ---------- magnitud
  let g=lienzo($('cm'),330), mn=Infinity; for(let k=0;k<D.n;k++){ mn=Math.min(mn,Math.hypot(D.re[k],D.im[k])); }
  const y1=Math.pow(10,Math.ceil(Math.log10(D.mx)+0.1)), y0=Math.max(y1*1e-5,Math.pow(10,Math.floor(Math.log10(Math.max(mn,1e-12)))));
  let e=ejes(g,{},{x0:0,x1:FMAX,y0,y1,logy:true,xl:'f (Hz)',yl:'|H| (m/N)',tit:'Magnitud de la FRF  ·  Δf = '+(+D.df.toPrecision(3))+' Hz  ·  banda de análisis sombreada',nx:10}), c=g.c;
  c.fillStyle='rgba(197,90,17,.10)'; c.fillRect(e.X(Math.max(0,S.fc-S.b)),e.py,e.X(Math.min(FMAX,S.fc+S.b))-e.X(Math.max(0,S.fc-S.b)),e.h);
  vline(e,S.f1,GREEN,[5,4],'f_1'); if(S.a2>0) vline(e,S.f2,GREEN,[5,4],'f_2');
  const pts=[]; for(let k=0;k<D.n;k++) pts.push([D.f[k],Math.hypot(D.re[k],D.im[k])]); curva(e,pts,STEEL,1.5);
  if(E.C&&isFinite(E.C.fn)&&E.C.z>0){ const C=E.C, p2=[]; for(let x=Math.max(0.1,S.fc-S.b);x<=S.fc+S.b;x+=S.b/60){ const h=Hmodo(x,C.fn,C.z,C.A); p2.push([x,Math.hypot(h[0],h[1])]); } curva(e,p2,ORANGE,2,[6,4]); }
  if(E.P&&isFinite(E.P.fa)&&isFinite(E.P.fb)){ punto(e,E.P.fa,E.P.hp,RED,4); punto(e,E.P.fb,E.P.hp,RED,4); }
  // ---------- Nyquist (izquierda) y rectas de la FRF inversa (derecha)
  const ang=($('cn').clientWidth||760)<560; g=lienzo($('cn'),ang?640:330); c=g.c; const half=ang?g.W:g.W/2, bN=ang?{x:0,w:g.W,y:0,h:330}:{x:0,w:half,h:330}, bI=ang?{x:0,w:g.W,y:330,h:310}:{x:half,w:half,h:330};
  if(E.np>=5){
    const hN=330-24-36, wN=half-56-14, asp=wN/hN, rr=1.3*E.C.R/Math.min(1,asp);
    e=ejes(g,bN,{x0:E.C.xc-rr*asp,x1:E.C.xc+rr*asp,y0:E.C.yc-rr,y1:E.C.yc+rr,xl:'Re H (m/N)',yl:'Im H (m/N)',tit:'Nyquist en la banda y círculo ajustado',nx:4,ny:5});
    c.save(); c.beginPath(); c.rect(e.px,e.py,e.w,e.h); c.clip(); c.strokeStyle=ORANGE; c.lineWidth=1.6; c.setLineDash([6,4]); c.beginPath();
    for(let a=0;a<=360;a+=3){ const x=e.X(E.C.xc+E.C.R*Math.cos(a*Math.PI/180)), y=e.Y(E.C.yc+E.C.R*Math.sin(a*Math.PI/180)); a?c.lineTo(x,y):c.moveTo(x,y); } c.stroke(); c.setLineDash([]); c.restore();
    for(let j=0;j<E.np;j++){ c.fillStyle=STEEL; c.beginPath(); c.arc(e.X(E.re[j]),e.Y(E.im[j]),2.6,0,7); c.fill(); }
    punto(e,E.C.xc,E.C.yc,ORANGE,3.5);
    // rectas: parte real de 1/H contra ω² (normalizada) e imaginaria contra ω
    const I=E.I, sc=1/Math.max(...I.gr.map(Math.abs),...I.gi.map(Math.abs)), fa=E.f[0], fb=E.f[E.np-1];
    const e2=ejes(g,bI,{x0:fa,x1:fb,y0:-1.1,y1:1.1,xl:'f (Hz)',yl:'1/H (normalizada)',tit:'FRF inversa: Re (azul) e Im (naranja)',nx:5,ny:4});
    hline(e2,0,GREY,[2,3]);
    for(let j=0;j<E.np;j++){ c.fillStyle=STEEL; c.beginPath(); c.arc(e2.X(E.f[j]),e2.Y(I.gr[j]*sc),2.4,0,7); c.fill(); c.fillStyle=ORANGE; c.beginPath(); c.arc(e2.X(E.f[j]),e2.Y(I.gi[j]*sc),2.4,0,7); c.fill(); }
    funcion(e2,x=>(I.pr[0]*Math.pow(TP*x,2)+I.pr[1])*sc,STEEL,1.4); funcion(e2,x=>I.pi[0]*TP*x*sc,ORANGE,1.4);
    if(isFinite(I.fn)) vline(e2,I.fn,GREEN,[5,4],'Re = 0: f_n');
  } else { c.fillStyle=GREY; c.font='13px Arial'; c.textAlign='center'; c.fillText('La banda contiene menos de cinco puntos: ampliar el semiancho o la duración del registro.',g.W/2,160); }
  // ---------- lecturas
  const bw=2*V.z*V.fn, sep=S.a2>0?Math.abs(S.f2-S.f1)/Math.max(2*S.z1*S.f1,2*S.z2*S.f2):Infinity;
  $('odf').textContent=(+D.df.toPrecision(4))+' Hz'; $('onp').textContent=E.np; $('obw').textContent=bw.toPrecision(3)+' Hz'; $('onb').textContent=(bw/D.df).toFixed(1); $('onb').parentNode.classList.toggle('al',bw/D.df<4);
  $('osep').textContent=isFinite(sep)?sep.toFixed(1):'un solo modo'; $('odia').textContent=E.np>=5?num(2*E.C.R)+' m/N':'…';
  const pc=(a,b)=>isFinite(a)&&a>0?((a-b)/b*100).toFixed(1).replace('-','−')+' %':'…', fx=(v,n)=>isFinite(v)&&v>0?v.toFixed(n):'…';
  const filas=[['Método','f_n (Hz)','ζ','Error en f_n','Error en ζ'],['Valor verdadero (modo '+V.n+')',V.fn.toFixed(3),V.z.toFixed(4),'',''] ];
  if(E.np>=5){ [['Pico y media potencia',E.P],['Círculo de Nyquist',E.C],['Recta de la FRF inversa',E.I]].forEach(([n,r])=>filas.push([n,fx(r.fn,3),fx(r.z,4),pc(r.fn,V.fn),pc(r.z,V.z)])); }
  $('res').innerHTML=filas.map((r,i)=>'<tr>'+r.map(()=>i?'<td></td>':'<th></th>').join('')+'</tr>').join(''); [...$('res').rows].forEach((tr,i)=>[...tr.cells].forEach((td,j)=>td.textContent=filas[i][j]));
  const av=[]; if(E.np<5) av.push('La banda contiene menos de cinco puntos: ampliar el semiancho o la duración del registro.');
  if(Math.abs(S.fc-V.fn)>S.b) av.push('La banda no contiene ninguna frecuencia natural: los resultados no tienen significado. Centrar la banda en un pico.');
  if(E.np>=5&&[E.P,E.C,E.I].some(r=>!(r.z>0))) av.push('Algún método no produjo un amortiguamiento positivo; se muestra «…».');
  if(bw/D.df<4) av.push('Hay menos de cuatro puntos dentro del ancho de media potencia: conviene un registro de al menos '+(2/(V.z*V.fn)).toFixed(1)+' s.');
  if(sep<2) av.push('Los modos están a menos de dos anchos de media potencia: los métodos de un grado de libertad no son fiables.');
  if(E.np>=5&&!(isFinite(E.P.fa)&&isFinite(E.P.fb))) av.push('La banda no contiene los dos puntos de media potencia: ampliar el semiancho.');
  $('aviso').textContent=av.join(' ');
}
liga(S,UN,dibujar); practica('pra');
$('nr').onclick=()=>{ SEM=(SEM*1103515245+12345)>>>0; dibujar(); };
$('c1').onclick=()=>pon(S,UN,{fc:S.f1,b:+Math.max(0.2,Math.min(20,5*S.z1*S.f1)).toFixed(1)},dibujar);
$('c2').onclick=()=>pon(S,UN,{fc:S.f2,b:+Math.max(0.2,Math.min(20,5*S.z2*S.f2)).toFixed(1)},dibujar);
const PRE={U:{f1:20,z1:0.02,f2:60,z2:0.01,a2:0,T:10,ns:0.5,fc:20,b:2}, S:{f1:20,z1:0.02,f2:60,z2:0.01,a2:1,T:10,ns:0.5,fc:20,b:2}, C:{f1:20,z1:0.02,f2:23,z2:0.02,a2:1,T:20,ns:0.5,fc:20,b:1.5}, R:{f1:20.25,z1:0.02,f2:60,z2:0.01,a2:1,T:2,ns:0.5,fc:20.25,b:3}, N:{f1:20,z1:0.02,f2:60,z2:0.01,a2:1,T:10,ns:5,fc:20,b:2}};
document.querySelectorAll('[data-pre]').forEach(b=>b.addEventListener('click',()=>pon(S,UN,PRE[b.dataset.pre],dibujar)));
window.addEventListener('resize',dibujar);
window.__mod={S,medir,extraer,Hteo,res:()=>E};
dibujar();
"""
pagina("modal_interactivo.html", "Extracción de parámetros modales", "Vibraciones · Pilar 15 · U7",
       "Al elegir una banda de la función de respuesta en frecuencia se obtienen la frecuencia natural y el amortiguamiento por tres métodos y se comparan con los valores verdaderos",
       cuerpo, script, "Explorador didáctico de extracción de parámetros modales (media potencia, círculo de Nyquist y FRF inversa) · material de apoyo del curso de Vibraciones · funciona sin conexión (un solo archivo).")
