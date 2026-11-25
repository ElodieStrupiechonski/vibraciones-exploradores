#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera proy_datos.html · Apoyo a los proyectos · Del dato al resultado: A transmisibilidad (ajuste de f_n y ζ),
B curva de vida (Basquin y Miner), C decremento logarítmico por configuración. Uso: python3 gen_proy_datos.py CARPETA"""
from base_pag import *

cuerpo = f"""
<style>
  .dat{{width:100%;min-height:170px;font:13px/1.45 'IBM Plex Mono',Consolas,monospace;border:1px solid var(--line);border-radius:8px;padding:8px;box-sizing:border-box}}
  .tabs{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px}} .pan{{display:none}} .pan.on{{display:block}}
  .err{{color:var(--red);font-size:12.5px;margin-top:4px}} .tres{{display:grid;grid-template-columns:1fr;gap:8px}} @media(min-width:700px){{.tres{{grid-template-columns:1fr 1fr 1fr}}}}
  .tres label{{font-size:12.5px;color:var(--grey)}} .tres input{{width:100%;box-sizing:border-box;font:inherit;font-size:13px;border:1px solid var(--line);border-radius:7px;padding:4px 6px;margin-bottom:4px}}
  table.tb td,table.tb th{{font-size:13px}}
</style>
  <div class="intro full">
    <b>¿Qué resuelve?</b> Cada equipo pega aquí sus mediciones y obtiene el resultado que va en el póster, con el procedimiento de la ficha del proyecto: <b>A</b>, la transmisibilidad medida, el ajuste de <i>f</i><sub>n</sub> y ζ y el porcentaje de aislamiento; <b>B</b>, la curva de vida de Basquin, su dispersión y la predicción de Miner; <b>C</b>, el decremento logarítmico de cada configuración y el amortiguamiento que aporta cada placa. Los datos de ejemplo son <b>inventados</b>, sólo para probar la página: hay que borrarlos y pegar los propios. Lo escrito se conserva en este navegador.
  </div>
  <div class="card full">
    <div class="tabs"><button class="btn on" data-t="A">Equipo A · transmisibilidad</button><button class="btn" data-t="B">Equipo B · curva de vida</button><button class="btn" data-t="C">Equipo C · decremento</button></div>

    <div class="pan on" id="p-A"><div class="two"><div>
      <p>Un renglón por velocidad del motor: <b>frecuencia (Hz), <i>T</i><sub>r</sub> medida</b> = aceleración rms de la plataforma entre aceleración rms de la base, en el mismo eje.</p>
      <textarea class="dat" id="dA" spellcheck="false"></textarea><div class="err" id="eA"></div>
      {fila("Rigidez de las ligas <i>k</i> (para la predicción)", "kA", 10, 5000, 1, 426, "N/m")}
      {fila("Masa de la plataforma con teléfono <i>m</i>", "mA", 10, 3000, 1, 300, "g")}
      <div class="tiles t3" style="margin-top:10px">{tile("<i>f</i><sub>n</sub> ajustada", "afn", "hl")}{tile("ζ ajustada", "az", "hl")}{tile("<i>f</i><sub>n</sub> predicha √(<i>k</i>/<i>m</i>)/2π", "afp")}
        {tile("<i>T</i><sub>r</sub> = 1 en √2 <i>f</i><sub>n</sub>", "acr")}{tile("Aislamiento a la frecuencia mayor", "ais")}{tile("Error rms del ajuste", "arms")}</div>
      <div class="nota" id="nA"></div>
    </div><div><canvas id="cA" width="420" height="330" aria-label="Transmisibilidad medida y ajustada"></canvas></div></div></div>

    <div class="pan" id="p-B"><div class="two"><div>
      <p>Un renglón por probeta: <b>amplitud δ en la punta (mm), ciclos hasta la rotura <i>N</i></b>. El esfuerzo se calcula con la geometría de abajo (usar el espesor medido con micrómetro).</p>
      <textarea class="dat" id="dB" spellcheck="false"></textarea><div class="err" id="eB"></div>
      {fila("Módulo <i>E</i> del PLA", "EB", 1, 5, 0.05, 3, "GPa")}
      {fila("Espesor <i>h</i>", "hB", 0.5, 5, 0.01, 2, "mm")}
      {fila("Longitud libre <i>L</i>", "LB", 10, 100, 0.5, 40, "mm")}
      {fila("Frecuencia de la máquina", "fB", 0.5, 20, 0.1, 4, "Hz")}
      <div class="grp"><div class="t">Ensayo de Miner en dos niveles</div>
      {fila("Primer nivel δ<sub>1</sub>", "d1", 1, 10, 0.1, 6, "mm")}
      {fila("Ciclos aplicados en el primer nivel <i>n</i><sub>1</sub>", "n1", 0, 20000, 10, 200)}
      {fila("Segundo nivel δ<sub>2</sub>", "d2", 1, 10, 0.1, 5, "mm")}</div>
      <div class="tiles t3" style="margin-top:10px">{tile("Basquin: <i>a</i>", "ba")}{tile("Basquin: exponente <i>b</i>", "bb", "hl")}{tile("Ajuste <i>R</i>²", "br2")}
        {tile("<i>N</i><sub>1</sub> y <i>N</i><sub>2</sub> del ajuste", "bN12")}{tile("Miner: ciclos restantes en δ<sub>2</sub>", "bn2", "hl")}{tile("Tiempo de máquina del segundo nivel", "bt")}</div>
      <div class="nota" id="nB"></div>
    </div><div><canvas id="cB" width="420" height="330" aria-label="Curva de vida en escala logarítmica"></canvas></div></div></div>

    <div class="pan" id="p-C">
      <p>Un renglón por máximo sucesivo del decaimiento: <b>tiempo (s), amplitud</b> (en cualquier unidad: mV del osciloscopio, mm, m/s²). Una columna por configuración; la primera es la referencia sin placa.</p>
      <div class="tres">
        <div><input id="nC1" value="sin placa (acrílico)" aria-label="Nombre de la configuración 1"><textarea class="dat" id="dC1" spellcheck="false"></textarea></div>
        <div><input id="nC2" value="aluminio a 4 mm" aria-label="Nombre de la configuración 2"><textarea class="dat" id="dC2" spellcheck="false"></textarea></div>
        <div><input id="nC3" value="cobre a 4 mm" aria-label="Nombre de la configuración 3"><textarea class="dat" id="dC3" spellcheck="false"></textarea></div>
      </div><div class="err" id="eC"></div>
      <div class="two" style="margin-top:8px"><div><table class="tb" id="tC"></table><div class="nota" id="nC"></div></div><div><canvas id="cC" width="420" height="330" aria-label="Logaritmo de la amplitud contra el tiempo"></canvas></div></div>
    </div>
  </div>
  <div class="card full">
    <h2>Las fórmulas en pantalla</h2>
    <div class="two"><div>
    {eq("A · Transmisibilidad (excitación por la base)", M(r"T_r=\sqrt{\frac{1+(2\zeta r)^2}{(1-r^2)^2+(2\zeta r)^2}},\qquad r=\frac{f}{f_n}") + nota("f<sub>n</sub> y ζ se ajustan por mínimos cuadrados sobre log T<sub>r</sub> (búsqueda en malla y refinamiento), para que los puntos pequeños de la zona de aislamiento pesen igual que los del pico"))}
    {eq("B · Esfuerzo en el empotramiento y Basquin", M(r"\sigma_a=\frac{3Eh\,\delta}{2L^2},\qquad \sigma_a=a\,N^{b}\ \Rightarrow\ \log\sigma_a=\log a+b\log N") + nota("la recta se ajusta con log N como variable independiente; como la dispersión está en N, conviene al menos tres probetas por nivel"))}
    </div><div>
    {eq("B · Regla de Miner en dos niveles", M(r"\frac{n_1}{N_1}+\frac{n_2}{N_2}=1\quad\Rightarrow\quad n_2=N_2\left(1-\frac{n_1}{N_1}\right)"))}
    {eq("C · Decremento por regresión", M(r"\ln x_i=\ln x_0-\sigma t_i,\qquad f_d=\frac{n-1}{t_{n}-t_1}") + M(r"\delta=\frac{\sigma}{f_d},\qquad \zeta=\frac{\delta}{\sqrt{4\pi^2+\delta^2}}") + nota("usar todos los máximos con una recta es más robusto que sólo el primero y el último; ζ<sub>placa</sub> = ζ − ζ<sub>sin placa</sub>"))}
    </div></div>
    <div class="takeaway" style="margin-top:10px"><b>Qué reportar en el póster.</b> Cada resultado con su incertidumbre y su número de repeticiones; la gráfica de los datos con el ajuste encima; y la comparación con la predicción de la ficha. <b>A:</b> la <i>T</i><sub>r</sub> que miden con dos teléfonos depende sólo de la plataforma (<i>k</i>, <i>m</i>): su máximo está en la frecuencia de la plataforma, aunque el motor también excite la resonancia del conjunto con la placa base (sesión del 20/11). <b>B:</b> la dispersión de la fatiga es grande; un factor 2 entre probetas del mismo nivel es normal. <b>C:</b> si la frecuencia cambia al poner la placa de acero, no es amortiguamiento: es la atracción del imán. Referencias: Rao, <i>Mechanical Vibrations</i>, 5.ª ed., Pearson (transmisibilidad y decremento logarítmico); Basquin, «The exponential law of endurance tests», <i>Proc. ASTM</i> 10, 625–630 (1910); Miner, «Cumulative damage in fatigue», <i>J. Appl. Mech.</i> 12, A159–A164 (1945), doi:10.1115/1.4009458.</div>
  </div>
"""
script = LIB + r"""
const TP=2*Math.PI;
let S={kA:426,mA:300,EB:3,hB:2,LB:40,fB:4,d1:6,n1:200,d2:5};
const UN={kA:' N/m',mA:' g',EB:' GPa',hB:' mm',LB:' mm',fB:' Hz',d1:' mm',n1:'',d2:' mm'};
const EJ={A:'# datos inventados para probar la página\n2, 1.12\n3, 1.36\n4, 1.76\n4.5, 2.13\n5, 3.04\n5.5, 4.88\n6, 8.42\n6.5, 5.02\n7, 2.53\n8, 1.23\n9, 0.828\n10, 0.582\n12, 0.344\n15, 0.187\n20, 0.106\n25, 0.0712\n30, 0.0447',
 B:'# datos inventados para probar la página\n6, 510\n6, 310\n6, 380\n5.5, 820\n5.5, 1450\n5.5, 1010\n5, 4980\n5, 4790\n5, 4240',
 C1:'# inventados\n0.0120, 9.748\n0.1549, 9.639\n0.2977, 9.386\n0.4406, 9.111\n0.5834, 8.684\n0.7263, 8.506\n0.8692, 8.201\n1.0120, 7.961\n1.1549, 7.860\n1.2977, 7.476\n1.4406, 7.302\n1.5834, 7.141\n1.7263, 6.819\n1.8692, 6.640\n2.0120, 6.449\n2.1549, 6.246\n2.2977, 5.975\n2.4406, 5.867\n2.5835, 5.758\n2.7263, 5.420',
 C2:'# inventados\n0.0120, 10.086\n0.1549, 9.111\n0.2977, 8.229\n0.4406, 7.688\n0.5835, 6.911\n0.7264, 6.167\n0.8692, 5.685\n1.0121, 5.199\n1.1550, 4.696\n1.2979, 4.311\n1.4407, 3.894\n1.5836, 3.569',
 C3:'# inventados\n0.0120, 10.144\n0.1549, 8.225\n0.2978, 6.872\n0.4408, 5.653\n0.5837, 4.709\n0.7266, 3.849\n0.8695, 3.207\n1.0125, 2.666\n1.1554, 2.232\n1.2983, 1.853\n1.4412, 1.497\n1.5841, 1.246'};
function leer(t){ const P=[], mal=[]; t.split(/\n/).forEach((l,i)=>{ l=l.trim(); if(!l||l[0]==='#') return; const v=l.split(/[\s;,\t]+/).map(x=>Number(x.replace('−','-'))); if(v.length<2||!isFinite(v[0])||!isFinite(v[1])) mal.push(i+1); else P.push([v[0],v[1]]); }); return {P,mal}; }
function recta(P){ const n=P.length, mx=P.reduce((a,p)=>a+p[0],0)/n, my=P.reduce((a,p)=>a+p[1],0)/n; let sxx=0,sxy=0,syy=0; P.forEach(p=>{ sxx+=(p[0]-mx)**2; sxy+=(p[0]-mx)*(p[1]-my); syy+=(p[1]-my)**2; });
  const s=sxy/sxx, a=my-s*mx, ssr=P.reduce((q,p)=>q+(p[1]-a-s*p[0])**2,0); return {s,a,se:n>2?Math.sqrt(ssr/(n-2)/sxx):NaN,r2:syy>0?1-ssr/syy:1,n}; }
const Tr=(f,fn,z)=>{ const r=f/fn; return Math.sqrt((1+(2*z*r)**2)/((1-r*r)**2+(2*z*r)**2)); };
// ---------------- A
function ajusteA(P){ const fmin=Math.min(...P.map(p=>p[0])), fmax=Math.max(...P.map(p=>p[0])); const err=(fn,z)=>P.reduce((s,p)=>s+(Math.log(Tr(p[0],fn,z))-Math.log(p[1]))**2,0);
  let best=[1,0.1,Infinity]; for(let i=0;i<=240;i++){ const fn=0.5*fmin*Math.pow(2*fmax/(0.5*fmin),i/240); for(let j=0;j<=80;j++){ const z=0.003*Math.pow(0.6/0.003,j/80); const e=err(fn,z); if(e<best[2]) best=[fn,z,e]; } }
  let [fn,z,e]=best, sf=fn*0.02, sz=z*0.1; for(let it=0;it<60;it++){ let mej=false; for(const [a,b] of [[sf,0],[-sf,0],[0,sz],[0,-sz]]){ const f2=fn+a, z2=Math.max(1e-4,z+b), e2=err(f2,z2); if(e2<e){ fn=f2; z=z2; e=e2; mej=true; } } if(!mej){ sf/=2; sz/=2; } }
  return {fn,z,rms:Math.sqrt(e/P.length)}; }
function pA(){ const {P,mal}=leer($('dA').value); $('eA').textContent=mal.length?'Renglones no válidos: '+mal.join(', '):''; const g=lienzo($('cA'),330);
  if(P.length<4||P.some(p=>!(p[1]>0)||!(p[0]>0))){ $('eA').textContent='Hacen falta al menos cuatro renglones con frecuencia y T_r positivas.'; return; }
  const R=ajusteA(P), fp=Math.sqrt(S.kA/(S.mA/1e3))/TP, fmax=Math.max(...P.map(p=>p[0]));
  const e=ejes(g,{mL:52},{x0:Math.min(...P.map(p=>p[0]))*0.8,x1:fmax*1.2,y0:0.01,y1:Math.max(30,Math.max(...P.map(p=>p[1]))*2),logx:true,logy:true,xl:'frecuencia (Hz)',yl:'T_r',tit:'Transmisibilidad medida y ajuste'});
  hline(e,1,GREY,[3,3]); funcion(e,f=>Tr(f,fp,R.z),ORANGE,1.3,[6,4]); funcion(e,f=>Tr(f,R.fn,R.z),STEEL,2.2); P.forEach(p=>punto(e,p[0],p[1],RED,4)); vline(e,Math.SQRT2*R.fn,GREEN,[4,3],'√2 f_n');
  $('afn').textContent=(+R.fn.toPrecision(3))+' Hz'; $('az').textContent=(+R.z.toPrecision(2))+''; $('afp').textContent=(+fp.toPrecision(3))+' Hz ('+(100*(R.fn/fp-1)>=0?'+':'−')+Math.abs(100*(R.fn/fp-1)).toFixed(0)+' %)';
  $('acr').textContent=(+(Math.SQRT2*R.fn).toPrecision(3))+' Hz'; const tr=Tr(fmax,R.fn,R.z); $('ais').textContent=(tr<1?(100*(1-tr)).toFixed(0)+' %':'no aísla')+' a '+fmax+' Hz'; $('arms').textContent=(100*(Math.exp(R.rms)-1)).toFixed(0)+' %';
  $('nA').textContent='Curva azul: ajuste; naranja punteada: predicción con k y m (con la ζ ajustada). '+(Math.abs(R.fn/fp-1)>0.15?'La f_n medida difiere más de 15 % de la predicha: revisar k (medida con la carga de trabajo) y m (con teléfono).':'La f_n medida coincide con la predicha a menos de 15 %.'); }
// ---------------- B
function pB(){ const {P,mal}=leer($('dB').value); $('eB').textContent=mal.length?'Renglones no válidos: '+mal.join(', '):''; const g=lienzo($('cB'),330);
  if(P.length<3||P.some(p=>!(p[0]>0)||!(p[1]>0))){ $('eB').textContent='Hacen falta al menos tres probetas con δ y N positivos.'; return; }
  const sig=d=>3*S.EB*1e3*S.hB*d/(2*S.LB*S.LB); const Q=P.map(p=>[Math.log10(p[1]),Math.log10(sig(p[0]))]); const r=recta(Q); const a=Math.pow(10,r.a), b=r.s;
  const Nde=d=>Math.pow(sig(d)/a,1/b), N1=Nde(S.d1), N2=Nde(S.d2), n2=N2*(1-S.n1/N1);
  const xs=Q.map(p=>p[0]), ys=Q.map(p=>Math.pow(10,p[1])); const e=ejes(g,{mL:52},{x0:Math.pow(10,Math.floor(Math.min(...xs))),x1:Math.pow(10,Math.ceil(Math.max(...xs))),y0:Math.min(...ys)*0.7,y1:Math.max(...ys)*1.4,logx:true,logy:true,xl:'ciclos hasta la rotura N',yl:'σ_a (MPa)',tit:'Curva de vida: σ_a = a N^b'});
  funcion(e,N=>a*Math.pow(N,b),STEEL,2.2); Q.forEach(p=>punto(e,Math.pow(10,p[0]),Math.pow(10,p[1]),RED,4));
  $('ba').textContent=(+a.toPrecision(3))+' MPa'; $('bb').textContent=b.toFixed(3); $('bb').parentNode.classList.toggle('al',!(b<-0.04&&b>-0.3)); $('br2').textContent=r.r2.toFixed(3);
  $('bN12').textContent=(+N1.toPrecision(3))+' y '+(+N2.toPrecision(3)); $('bn2').textContent=n2>0?(+n2.toPrecision(3))+' ciclos':'ya falló en el primer nivel'; $('bt').textContent=n2>0?(+(n2/S.fB/60).toPrecision(3))+' min':'…';
  const niveles={}; P.forEach(p=>{ (niveles[p[0]]=niveles[p[0]]||[]).push(p[1]); }); const disp=Object.entries(niveles).filter(([k,v])=>v.length>1).map(([k,v])=>'δ = '+k+' mm: σ_a = '+(+sig(+k).toPrecision(3))+' MPa, N de '+Math.min(...v)+' a '+Math.max(...v)+' (factor '+(Math.max(...v)/Math.min(...v)).toFixed(1)+')');
  $('nB').textContent=(disp.length?'Dispersión por nivel: '+disp.join('; ')+'. ':'')+(b<-0.04&&b>-0.3?'El exponente está en el intervalo esperado para polímeros (entre −0.04 y −0.3, orientativo).':'El exponente sale fuera del intervalo esperado: revisar datos o la geometría.'); }
// ---------------- C
function serieC(t){ const {P}=leer(t); if(P.length<3||P.some(p=>!(p[1]>0))) return null; P.sort((x,y)=>x[0]-y[0]); const r=recta(P.map(p=>[p[0],Math.log(p[1])])); const sg=-r.s, fd=(P.length-1)/(P[P.length-1][0]-P[0][0]), d=sg/fd;
  return {n:P.length,fd,d,z:d/Math.sqrt(4*Math.PI*Math.PI+d*d),r2:r.r2,r,P,zse:r.se/fd/TP}; }
function pC(){ const g=lienzo($('cC'),330), cols=[STEEL,ORANGE,GREEN], R=[1,2,3].map(i=>({nom:$('nC'+i).value,s:serieC($('dC'+i).value)}));
  const val=R.filter(x=>x.s); $('eC').textContent=val.length?'':'Cada columna necesita al menos tres máximos con amplitud positiva.'; if(!val.length){ $('tC').innerHTML=''; return; }
  const tmax=Math.max(...val.map(x=>x.s.P[x.s.P.length-1][0])), ys=val.flatMap(x=>x.s.P.map(p=>Math.log(p[1])));
  const e=ejes(g,{mL:52},{x0:0,x1:tmax*1.05,y0:Math.min(...ys)-0.2,y1:Math.max(...ys)+0.2,xl:'tiempo (s)',yl:'ln(amplitud)',tit:'Rectas de decaimiento'});
  R.forEach((x,i)=>{ if(!x.s) return; funcion(e,t=>x.s.r.a+x.s.r.s*t,cols[i],2); x.s.P.forEach(p=>punto(e,p[0],Math.log(p[1]),cols[i],3.5)); });
  const z0=R[0].s?R[0].s.z:null;
  $('tC').innerHTML='<tr><th>Configuración</th><th>máximos</th><th>f_d (Hz)</th><th>ζ</th><th>R²</th><th>ζ − ζ<sub>ref</sub></th></tr>'+R.map((x,i)=>x.s?'<tr><td><span style="color:'+cols[i]+'">■</span> '+x.nom.replace(/</g,'&lt;')+'</td><td>'+x.s.n+'</td><td>'+(+x.s.fd.toPrecision(4))+'</td><td>'+(+x.s.z.toPrecision(3))+' ± '+(+x.s.zse.toPrecision(1))+'</td><td>'+x.s.r2.toFixed(4)+'</td><td>'+(i&&z0!==null?(+(x.s.z-z0).toPrecision(3)):'referencia')+'</td></tr>':'').join('');
  let t=[]; if(R[0].s) R.slice(1).forEach(x=>{ if(x.s&&Math.abs(x.s.fd/R[0].s.fd-1)>0.02) t.push('«'+x.nom+'» cambia la frecuencia '+(100*(x.s.fd/R[0].s.fd-1)).toFixed(1)+' %: no es sólo amortiguamiento (atracción del imán o sujeción).'); });
  if(R[1].s&&R[2].s&&z0!==null) t.push('Razón de amortiguamientos añadidos: '+(+((R[2].s.z-z0)/(R[1].s.z-z0)).toPrecision(3))+' (con igual espesor y hueco, la teoría espera la razón de conductividades, 5.96/3.77 = 1.58 para cobre frente a aluminio).');
  $('nC').textContent=t.join(' '); }
liga(S,UN,()=>{ pA(); pB(); });
const guardar=()=>{ try{ localStorage.setItem('datos-vib',JSON.stringify(['dA','dB','dC1','dC2','dC3','nC1','nC2','nC3'].map(i=>$(i).value))); }catch(e){} };
let G=null; try{ G=JSON.parse(localStorage.getItem('datos-vib')||'null'); }catch(e){}
[['dA','A'],['dB','B'],['dC1','C1'],['dC2','C2'],['dC3','C3']].forEach(([i,k],j)=>{ $(i).value=(G&&G[j])||EJ[k]; });
if(G) ['nC1','nC2','nC3'].forEach((i,j)=>{ if(G[5+j]) $(i).value=G[5+j]; });
['dA','dB','dC1','dC2','dC3','nC1','nC2','nC3'].forEach(i=>$(i).addEventListener('input',()=>{ guardar(); if(i==='dA') pA(); else if(i==='dB') pB(); else pC(); }));
document.querySelectorAll('[data-t]').forEach(bt=>bt.addEventListener('click',()=>{ document.querySelectorAll('[data-t]').forEach(x=>x.classList.toggle('on',x===bt)); document.querySelectorAll('.pan').forEach(p=>p.classList.toggle('on',p.id==='p-'+bt.dataset.t)); pA(); pB(); pC(); }));
window.addEventListener('resize',()=>{ pA(); pB(); pC(); });
window.__da={S,ajusteA,serieC,Tr,recta,leer};
pA(); pB(); pC();
"""
pagina("proy_datos.html", "Del dato al resultado: análisis por proyecto", "Vibraciones · Apoyo a los proyectos",
       "Cada equipo pega sus mediciones y obtiene su resultado: transmisibilidad con ajuste de f_n y ζ (A), curva de vida y Miner (B) y decremento por configuración (C)",
       cuerpo, script, "Apoyo a los proyectos del curso de Vibraciones: análisis de datos de los equipos A, B y C · funciona sin conexión (un solo archivo).")
