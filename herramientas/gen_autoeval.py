#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera autoevaluacion.html · Repaso para el examen final: problemas de las unidades 1 a 8 con datos aleatorios,
verificación con 2 % de tolerancia y solución paso a paso. Uso: python3 gen_autoeval.py CARPETA"""
from base_pag import *

cuerpo = """
<style>
  .ae-barra{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
  .ae-prob{border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin:0 0 12px;background:#fff}
  .ae-prob h3{margin:0 0 4px;font-size:15px;color:var(--navy)} .ae-prob .u{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--orange);font-weight:700}
  .ae-prob .enun{margin:6px 0 10px;line-height:1.5}
  .ae-campos{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px 14px}
  .ae-campo label{display:block;font-size:12.5px;color:var(--grey);margin-bottom:3px}
  .ae-campo .in{display:flex;align-items:center;gap:6px} .ae-campo input{width:120px;font:inherit;font-size:14px;padding:5px 7px;border:1px solid var(--line);border-radius:7px}
  .ae-campo .un{font-size:13px;color:var(--grey)} .ae-campo .mk{font-weight:700;min-width:1.2em}
  .ae-campo.ok input{border-color:var(--green);background:#EEF7F0} .ae-campo.mal input{border-color:var(--red);background:#FBEFEF}
  .ae-campo .mk.ok{color:var(--green)} .ae-campo .mk.mal{color:var(--red)}
  .ae-acc{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
  .ae-sol{display:none;margin-top:10px;padding:10px 12px;border-left:3px solid var(--steel);background:#F4F6FA;border-radius:0 8px 8px 0;line-height:1.55;font-size:14px}
  .ae-sol.on{display:block} .ae-sol ol{margin:4px 0 0;padding-left:20px} .ae-sol li{margin:2px 0}
  .ae-msg{font-size:13px;margin-top:6px;color:var(--grey)}
  .ae-res{font-weight:700;color:var(--navy)}
</style>
  <div class="intro full">
    <b>¿Para qué sirve?</b> Para practicar el examen final con problemas de las ocho unidades del curso. Cada problema trae datos distintos cada vez: se escriben los resultados, se pulsa «Comprobar» y la página marca cada casilla como correcta o incorrecta con una tolerancia de 2 %, la misma que se usa al calificar (en los resultados en decibeles, 0.2 dB). «Ver solución» muestra el procedimiento completo con los números del problema. Conviene intentarlo antes de abrir la solución y repetir con «Datos nuevos» hasta resolverlo sin ayuda. Los resultados se escriben con punto o coma decimal y en las unidades indicadas.
  </div>
  <div class="card full">
    <div class="ae-barra">
      <b style="margin-right:4px">Unidad:</b>
      <button class="btn on" data-f="0">Todas</button><button class="btn" data-f="1">U1</button><button class="btn" data-f="2">U2</button><button class="btn" data-f="3">U3</button><button class="btn" data-f="4">U4</button><button class="btn" data-f="5">U5</button><button class="btn" data-f="6">U6</button><button class="btn" data-f="7">U7</button><button class="btn" data-f="8">U8</button>
      <button class="btn" id="todo-nuevo" style="margin-left:auto">Datos nuevos en todos</button>
    </div>
    <div class="ae-msg" id="marcador"></div>
  </div>
  <div class="full" id="lista"></div>
  <div class="card full">
    <div class="takeaway"><b>Cómo usarla para estudiar:</b> (1) resolver primero con lápiz, papel y calculadora, como en el examen; (2) comprobar; (3) si una casilla sale mal, revisar unidades y el paso donde se separa del procedimiento, sin abrir todavía la solución; (4) abrir la solución sólo después de dos intentos; (5) pedir «Datos nuevos» y repetir hasta acertar a la primera. Los problemas son de práctica: no reproducen el examen ni sustituyen las tareas, las guías de las sesiones y los exploradores de cada tema. El avance se guarda sólo en este navegador. Referencias: Rao, <i>Mechanical Vibrations</i>, 5.ª ed., Pearson; Inman, <i>Engineering Vibration</i>, 4.ª ed., Pearson; Beer, Johnston, DeWolf y Mazurek, <i>Mecánica de materiales</i>, 7.ª ed., McGraw-Hill; Kinsler, Frey, Coppens y Sanders, <i>Fundamentals of Acoustics</i>, 4.ª ed., Wiley.</div>
  </div>
"""
script = r"""
const NAVY='#1F3864'; const $=id=>document.getElementById(id);
const TOL=0.02, G0=9.80665, TP=2*Math.PI;
function rng(seed){ let a=seed>>>0; return ()=>{ a=(a+0x6D2B79F5)>>>0; let t=a; t=Math.imul(t^(t>>>15),t|1); t^=t+Math.imul(t^(t>>>7),t|61); return ((t^(t>>>14))>>>0)/4294967296; }; }
const uni=(r,a,b,p)=>{ const v=a+(b-a)*r(); const f=Math.pow(10,p); return Math.round(v*f)/f; };       // p decimales
const pick=(r,L)=>L[Math.floor(r()*L.length)];
const s3=v=>{ if(!isFinite(v)) return '∞'; const a=Math.abs(v); if(a===0) return '0'; const e=Math.floor(Math.log10(a)); let t=(a>=1e5||a<1e-3)?(v/Math.pow(10,e)).toPrecision(3)+' × 10<sup>'+e+'</sup>':String(+v.toPrecision(3)); return t.replace('-','−'); };
const f2=(v,d)=>(+v).toFixed(d).replace('-','−');
// ---------------------------------------------------------------- problemas
// cada problema: u, tit, gen(r) -> D, enun(D), res(D) -> [{k,lab,un,v}], pasos(D,R) -> [html]
const P=[
{u:1, tit:'Una señal armónica', gen:r=>({N:Math.round(uni(r,8,40,0)), T:uni(r,0.5,4,1), pp:uni(r,0.6,8,1)}),
 enun:D=>`Un registro de desplazamiento muestra <b>${D.N} ciclos</b> completos en <b>${D.T} s</b>, con una amplitud pico a pico de <b>${D.pp} mm</b>. Supongan un movimiento armónico simple.`,
 res:D=>{ const f=D.N/D.T, w=TP*f, X=D.pp/2e3; return [{k:'f',lab:'Frecuencia <i>f</i>',un:'Hz',v:f},{k:'w',lab:'Frecuencia angular ω',un:'rad/s',v:w},{k:'a',lab:'Aceleración máxima',un:'m/s²',v:w*w*X}]; },
 pasos:(D,R)=>[`<i>f</i> = <i>N</i>/<i>T</i> = ${D.N}/${D.T} = ${s3(R[0].v)} Hz.`,`ω = 2π<i>f</i> = ${s3(R[1].v)} rad/s.`,`La amplitud es la mitad del pico a pico: <i>X</i> = ${D.pp}/2 = ${s3(D.pp/2)} mm = ${s3(D.pp/2e3)} m.`,`En un movimiento armónico <i>a</i><sub>máx</sub> = ω²<i>X</i> = (${s3(R[1].v)})² × ${s3(D.pp/2e3)} = ${s3(R[2].v)} m/s² (${s3(R[2].v/G0)} <i>g</i>).`]},
{u:2, tit:'Oscilador libre amortiguado', gen:r=>({m:uni(r,0.2,5,2), k:Math.round(uni(r,200,20000,0)), z:uni(r,0.02,0.4,2)}),
 enun:D=>{ const c=2*D.z*Math.sqrt(D.k*D.m); return `Un sistema masa-resorte-amortiguador tiene <i>m</i> = <b>${D.m} kg</b>, <i>k</i> = <b>${D.k} N/m</b> y <i>c</i> = <b>${s3(c)} N·s/m</b>. Calculen su frecuencia natural, su factor de amortiguamiento y su frecuencia natural amortiguada.`; },
 res:D=>{ const c=+(2*D.z*Math.sqrt(D.k*D.m)).toPrecision(3), wn=Math.sqrt(D.k/D.m), z=c/(2*Math.sqrt(D.k*D.m)); return [{k:'fn',lab:'<i>f</i><sub>n</sub>',un:'Hz',v:wn/TP},{k:'z',lab:'ζ',un:'',v:z},{k:'fd',lab:'<i>f</i><sub>d</sub>',un:'Hz',v:wn*Math.sqrt(1-z*z)/TP}]; },
 pasos:(D,R)=>{ const c=+(2*D.z*Math.sqrt(D.k*D.m)).toPrecision(3), wn=Math.sqrt(D.k/D.m); return [`ω<sub>n</sub> = √(<i>k</i>/<i>m</i>) = √(${D.k}/${D.m}) = ${s3(wn)} rad/s; <i>f</i><sub>n</sub> = ω<sub>n</sub>/2π = ${s3(R[0].v)} Hz.`,`<i>c</i><sub>c</sub> = 2√(<i>km</i>) = ${s3(2*Math.sqrt(D.k*D.m))} N·s/m; ζ = <i>c</i>/<i>c</i><sub>c</sub> = ${s3(c)}/${s3(2*Math.sqrt(D.k*D.m))} = ${s3(R[1].v)}.`,`<i>f</i><sub>d</sub> = <i>f</i><sub>n</sub>√(1 − ζ²) = ${s3(R[0].v)} × √(1 − ${s3(R[1].v)}²) = ${s3(R[2].v)} Hz. ${R[1].v<1?'Como ζ &lt; 1, el sistema es subamortiguado.':''}`]; }},
{u:2, tit:'Decremento logarítmico', gen:r=>{ const n=Math.round(uni(r,3,12,0)); const z=uni(r,0.005,0.08,3); const x0=uni(r,5,30,1); const d=2*Math.PI*z/Math.sqrt(1-z*z); return {n, x0, xn:+(x0*Math.exp(-n*d)).toPrecision(3)}; },
 enun:D=>`En un decaimiento libre, un máximo vale <b>${D.x0} mm</b> y el máximo que está <b>${D.n} ciclos</b> después vale <b>${D.xn} mm</b>. Calculen el decremento logarítmico y el factor de amortiguamiento.`,
 res:D=>{ const d=Math.log(D.x0/D.xn)/D.n; return [{k:'d',lab:'Decremento δ',un:'',v:d},{k:'z',lab:'ζ',un:'',v:d/Math.sqrt(4*Math.PI*Math.PI+d*d)}]; },
 pasos:(D,R)=>[`δ = (1/<i>n</i>) ln(<i>x</i><sub>0</sub>/<i>x</i><sub>n</sub>) = (1/${D.n}) ln(${D.x0}/${D.xn}) = ${s3(R[0].v)}.`,`ζ = δ/√(4π² + δ²) = ${s3(R[0].v)}/√(${s3(4*Math.PI*Math.PI)} + ${s3(R[0].v*R[0].v)}) = ${s3(R[1].v)}.`,`Comprobación rápida: para ζ pequeño, ζ ≈ δ/2π = ${s3(R[0].v/TP)}.`]},
{u:3, tit:'Respuesta forzada', gen:r=>({F:uni(r,2,50,1), k:Math.round(uni(r,1000,40000,0)), z:uni(r,0.02,0.3,2), r:uni(r,0.3,3,2)}),
 enun:D=>`Una fuerza armónica de amplitud <b>${D.F} N</b> actúa sobre un sistema con <i>k</i> = <b>${D.k} N/m</b> y ζ = <b>${D.z}</b>, a una frecuencia <i>r</i> = ω/ω<sub>n</sub> = <b>${D.r}</b>. Calculen la deflexión estática, el factor de amplificación y la amplitud de la respuesta permanente.`,
 res:D=>{ const X0=D.F/D.k, M=1/Math.sqrt((1-D.r*D.r)**2+(2*D.z*D.r)**2); return [{k:'x0',lab:'<i>X</i><sub>0</sub> = <i>F</i><sub>0</sub>/<i>k</i>',un:'mm',v:X0*1e3},{k:'M',lab:'Factor de amplificación <i>M</i>',un:'',v:M},{k:'X',lab:'Amplitud <i>X</i>',un:'mm',v:M*X0*1e3}]; },
 pasos:(D,R)=>[`<i>X</i><sub>0</sub> = <i>F</i><sub>0</sub>/<i>k</i> = ${D.F}/${D.k} = ${s3(R[0].v/1e3)} m = ${s3(R[0].v)} mm.`,`<i>M</i> = 1/√[(1 − <i>r</i>²)² + (2ζ<i>r</i>)²] = 1/√[(1 − ${s3(D.r*D.r)})² + (${s3(2*D.z*D.r)})²] = ${s3(R[1].v)}.`,`<i>X</i> = <i>M X</i><sub>0</sub> = ${s3(R[2].v)} mm. ${D.r>Math.SQRT2?'Con <i>r</i> &gt; √2 la amplitud queda por debajo de la deflexión estática.':D.r>0.8&&D.r<1.2?'Cerca de la resonancia la amplitud depende sobre todo de ζ.':''}`]},
{u:3, tit:'Media potencia', gen:r=>{ const fr=uni(r,5,200,1), z=uni(r,0.01,0.08,3); return {fr, f1:+(fr*(1-z)).toFixed(2), f2:+(fr*(1+z)).toFixed(2)}; },
 enun:D=>`Una curva de respuesta en frecuencia tiene su pico en <i>f</i><sub>r</sub> = <b>${D.fr} Hz</b> y sus puntos de media potencia en <i>f</i><sub>1</sub> = <b>${D.f1} Hz</b> y <i>f</i><sub>2</sub> = <b>${D.f2} Hz</b>. Estimen ζ y el factor de calidad.`,
 res:D=>{ const z=(D.f2-D.f1)/(2*D.fr); return [{k:'z',lab:'ζ',un:'',v:z},{k:'Q',lab:'<i>Q</i>',un:'',v:1/(2*z)}]; },
 pasos:(D,R)=>[`Ancho de banda: <i>f</i><sub>2</sub> − <i>f</i><sub>1</sub> = ${D.f2} − ${D.f1} = ${s3(D.f2-D.f1)} Hz. Se restan los valores completos: redondear antes cambia mucho el resultado.`,`ζ ≈ (<i>f</i><sub>2</sub> − <i>f</i><sub>1</sub>)/(2<i>f</i><sub>r</sub>) = ${s3(D.f2-D.f1)}/(2 × ${D.fr}) = ${s3(R[0].v)}.`,`<i>Q</i> = 1/(2ζ) = <i>f</i><sub>r</sub>/(<i>f</i><sub>2</sub> − <i>f</i><sub>1</sub>) = ${s3(R[1].v)}. El método supone ζ pequeño y un modo aislado.`]},
{u:4, tit:'Vibración aleatoria: de la PSD a la carga', gen:r=>({W:pick(r,[0.01,0.02,0.04,0.05,0.08,0.1]), fa:pick(r,[20,20,50]), fb:pick(r,[500,1000,2000]), fn:Math.round(uni(r,60,400,0)), Q:pick(r,[10,10,15,20])}),
 enun:D=>`Un ensayo aleatorio aplica una densidad espectral plana de <b>${D.W} g²/Hz</b> entre <b>${D.fa}</b> y <b>${D.fb} Hz</b>. Un componente tiene <i>f</i><sub>n</sub> = <b>${D.fn} Hz</b> y <i>Q</i> = <b>${D.Q}</b>. Calculen el valor eficaz de la entrada, el de la respuesta del componente con la ecuación de Miles y el valor de 3σ de la respuesta.`,
 res:D=>{ const gi=Math.sqrt(D.W*(D.fb-D.fa)), gr=Math.sqrt(Math.PI/2*D.fn*D.Q*D.W); return [{k:'gi',lab:'<i>G</i><sub>rms</sub> de la entrada',un:'g',v:gi},{k:'gr',lab:'<i>G</i><sub>rms</sub> de la respuesta',un:'g',v:gr},{k:'g3',lab:'3σ de la respuesta',un:'g',v:3*gr}]; },
 pasos:(D,R)=>[`PSD plana: <i>G</i><sub>rms</sub> = √(<i>W</i> Δ<i>f</i>) = √(${D.W} × ${D.fb-D.fa}) = ${s3(R[0].v)} g.`,`Miles: <i>G</i><sub>rms</sub> ≈ √(π/2 · <i>f</i><sub>n</sub> <i>Q W</i>(<i>f</i><sub>n</sub>)) = √(1.571 × ${D.fn} × ${D.Q} × ${D.W}) = ${s3(R[1].v)} g. Vale si la PSD es plana cerca de <i>f</i><sub>n</sub> y el amortiguamiento es pequeño.`,`Con distribución gaussiana, 3σ = 3 × ${s3(R[1].v)} = ${s3(R[2].v)} g; se excede sólo 0.27 % del tiempo.`]},
{u:5, tit:'Unión con pernos: esfuerzos directos', gen:r=>({P:uni(r,2,40,1), d:pick(r,[4,5,6,8,10]), n:Math.round(uni(r,1,4,0)), ns:pick(r,[1,2]), t:pick(r,[2,3,4,5,6])}),
 enun:D=>`Una unión a traslape transmite <b>${D.P} kN</b> con <b>${D.n}</b> perno${D.n>1?'s':''} de <b>${D.d} mm</b> de diámetro en cortante <b>${D.ns===1?'simple':'doble'}</b>. La placa${D.ns===2?' central':''} tiene <b>${D.t} mm</b> de espesor. Calculen el esfuerzo cortante en los pernos y el esfuerzo de aplastamiento en la placa.`,
 res:D=>{ const A=Math.PI*D.d*D.d/4; return [{k:'A',lab:'Área de un perno',un:'mm²',v:A},{k:'tau',lab:'Cortante τ',un:'MPa',v:D.P*1e3/(D.n*D.ns*A)},{k:'sb',lab:'Aplastamiento σ<sub>b</sub>',un:'MPa',v:D.P*1e3/(D.n*D.d*D.t)}]; },
 pasos:(D,R)=>[`<i>A</i> = π<i>d</i>²/4 = π(${D.d})²/4 = ${s3(R[0].v)} mm².`,`Hay ${D.n} × ${D.ns} = ${D.n*D.ns} plano${D.n*D.ns>1?'s':''} de corte: τ = <i>P</i>/(<i>n n</i><sub>s</sub> <i>A</i>) = ${D.P*1e3} N/(${D.n*D.ns} × ${s3(R[0].v)} mm²) = ${s3(R[1].v)} MPa (N/mm² = MPa).`,`Aplastamiento sobre el área proyectada <i>d t</i>: σ<sub>b</sub> = <i>P</i>/(<i>n d t</i>) = ${D.P*1e3}/(${D.n} × ${D.d} × ${D.t}) = ${s3(R[2].v)} MPa. El cortante doble reduce τ a la mitad, pero no cambia σ<sub>b</sub>.`]},
{u:5, tit:'Esfuerzos principales (círculo de Mohr)', gen:r=>({sx:Math.round(uni(r,-80,120,0)), sy:Math.round(uni(r,-80,80,0)), txy:Math.round(uni(r,-60,60,0))}),
 enun:D=>`En un punto de una placa, σ<sub>x</sub> = <b>${f2(D.sx,0)} MPa</b>, σ<sub>y</sub> = <b>${f2(D.sy,0)} MPa</b> y τ<sub>xy</sub> = <b>${f2(D.txy,0)} MPa</b> (estado plano). Calculen el centro y el radio del círculo de Mohr y los esfuerzos principales.`,
 res:D=>{ const C=(D.sx+D.sy)/2, R=Math.hypot((D.sx-D.sy)/2,D.txy); return [{k:'C',lab:'Centro <i>C</i>',un:'MPa',v:C},{k:'R',lab:'Radio <i>R</i> = τ<sub>máx</sub> en el plano',un:'MPa',v:R},{k:'s1',lab:'σ<sub>1</sub>',un:'MPa',v:C+R},{k:'s2',lab:'σ<sub>2</sub>',un:'MPa',v:C-R}]; },
 pasos:(D,R)=>[`<i>C</i> = (σ<sub>x</sub> + σ<sub>y</sub>)/2 = (${f2(D.sx,0)} + ${f2(D.sy,0)})/2 = ${s3(R[0].v)} MPa.`,`<i>R</i> = √[((σ<sub>x</sub> − σ<sub>y</sub>)/2)² + τ<sub>xy</sub>²] = √[(${s3((D.sx-D.sy)/2)})² + (${f2(D.txy,0)})²] = ${s3(R[1].v)} MPa.`,`σ<sub>1,2</sub> = <i>C</i> ± <i>R</i>: σ<sub>1</sub> = ${s3(R[2].v)} MPa, σ<sub>2</sub> = ${s3(R[3].v)} MPa. Ángulo principal: tan 2θ<sub>p</sub> = 2τ<sub>xy</sub>/(σ<sub>x</sub> − σ<sub>y</sub>).`]},
{u:6, tit:'Suma de niveles y distancia', gen:r=>({L1:Math.round(uni(r,70,95,0)), L2:Math.round(uni(r,65,95,0)), k:pick(r,[2,4])}),
 enun:D=>`Dos máquinas producen, cada una sola, <b>${D.L1} dB</b> y <b>${D.L2} dB</b> en el mismo punto. Calculen el nivel con las dos encendidas. Después, en campo libre, ¿cuánto vale ese nivel total si la distancia a las fuentes se multiplica por <b>${D.k}</b>?`,
 res:D=>{ const L=10*Math.log10(Math.pow(10,D.L1/10)+Math.pow(10,D.L2/10)); return [{k:'L',lab:'Nivel total',un:'dB',v:L,abs:0.2},{k:'L2',lab:'Nivel a '+D.k+' veces la distancia',un:'dB',v:L-20*Math.log10(D.k),abs:0.2}]; },
 pasos:(D,R)=>[`Los niveles no se suman; se suman las intensidades: <i>L</i> = 10 log<sub>10</sub>(10<sup>${D.L1}/10</sup> + 10<sup>${D.L2}/10</sup>) = ${f2(R[0].v,1)} dB.`,`${D.L1===D.L2?'Dos fuentes iguales suman 3 dB.':'La fuente más débil aporta menos de 3 dB, y casi nada si está más de 10 dB por debajo de la otra.'}`,`En campo libre, <i>L</i> baja 20 log<sub>10</sub>(${D.k}) = ${f2(20*Math.log10(D.k),1)} dB: ${f2(R[0].v,1)} − ${f2(20*Math.log10(D.k),1)} = ${f2(R[1].v,1)} dB.`]},
{u:6, tit:'Transmisibilidad de un aislador', gen:r=>({m:uni(r,0.3,20,1), fn:uni(r,3,15,1), z:uni(r,0.02,0.2,2), f:Math.round(uni(r,15,80,0))}),
 enun:D=>`Un equipo de <b>${D.m} kg</b> descansa sobre aisladores con <i>f</i><sub>n</sub> = <b>${D.fn} Hz</b> y ζ = <b>${D.z}</b>. La base vibra a <b>${D.f} Hz</b>. Calculen la rigidez total de los aisladores, la razón de frecuencias y la transmisibilidad.`,
 res:D=>{ const k=D.m*(TP*D.fn)**2, r=D.f/D.fn, T=Math.sqrt((1+(2*D.z*r)**2)/((1-r*r)**2+(2*D.z*r)**2)); return [{k:'k',lab:'Rigidez <i>k</i>',un:'N/m',v:k},{k:'r',lab:'<i>r</i> = <i>f</i>/<i>f</i><sub>n</sub>',un:'',v:r},{k:'T',lab:'<i>T</i><sub>r</sub>',un:'',v:T}]; },
 pasos:(D,R)=>[`<i>k</i> = <i>m</i>(2π<i>f</i><sub>n</sub>)² = ${D.m} × (${s3(TP*D.fn)})² = ${s3(R[0].v)} N/m.`,`<i>r</i> = ${D.f}/${D.fn} = ${s3(R[1].v)}.`,`<i>T</i><sub>r</sub> = √{[1 + (2ζ<i>r</i>)²]/[(1 − <i>r</i>²)² + (2ζ<i>r</i>)²]} = ${s3(R[2].v)}: se transmite el ${s3(100*R[2].v)} % del movimiento${R[1].v>Math.SQRT2?' (hay aislamiento porque <i>r</i> &gt; √2)':''}.`]},
{u:7, tit:'Muestreo, aliasing y resolución', gen:r=>{ const fs=pick(r,[100,120,150,200,250,400,500]); return {fs, f:Math.round(uni(r,0.55*fs,1.45*fs,0)), T:pick(r,[2,4,5,8,10,20])}; },
 enun:D=>`Un teléfono registra a <i>f</i><sub>s</sub> = <b>${D.fs} Hz</b> una vibración de <b>${D.f} Hz</b> durante <b>${D.T} s</b>. Calculen la frecuencia de Nyquist, la frecuencia a la que aparece el pico en el espectro y la resolución en frecuencia.`,
 res:D=>{ const ny=D.fs/2; let fa=D.f; if(D.f>ny){ const k=Math.round(D.f/D.fs); fa=Math.abs(D.f-k*D.fs); } return [{k:'ny',lab:'Frecuencia de Nyquist',un:'Hz',v:ny},{k:'fa',lab:'Frecuencia aparente',un:'Hz',v:fa},{k:'df',lab:'Resolución Δ<i>f</i>',un:'Hz',v:1/D.T}]; },
 pasos:(D,R)=>[`<i>f</i><sub>Nyquist</sub> = <i>f</i><sub>s</sub>/2 = ${s3(R[0].v)} Hz.`,D.f>D.fs/2?`${D.f} Hz &gt; ${s3(R[0].v)} Hz: hay aliasing. El pico aparece en |<i>f</i> − <i>k f</i><sub>s</sub>| con el entero <i>k</i> que lo deja entre 0 y <i>f</i><sub>s</sub>/2: |${D.f} − ${Math.round(D.f/D.fs)} × ${D.fs}| = ${s3(R[1].v)} Hz.`:`${D.f} Hz ≤ ${s3(R[0].v)} Hz: no hay aliasing y el pico aparece en su frecuencia real.`,`Δ<i>f</i> = 1/<i>T</i> = 1/${D.T} = ${s3(R[2].v)} Hz.`]},
{u:7, tit:'Coherencia y error de la FRF', gen:r=>({g2:uni(r,0.7,0.98,2), nd:Math.round(uni(r,8,60,0))}),
 enun:D=>`Un ensayo de impacto da, en el pico, una coherencia γ² = <b>${D.g2}</b> con <i>n</i><sub>d</sub> = <b>${D.nd}</b> promedios. Calculen la relación señal a ruido equivalente de la salida (en veces y en dB) y el error aleatorio normalizado de |<i>H</i><sub>1</sub>|.`,
 res:D=>{ const snr=D.g2/(1-D.g2); return [{k:'snr',lab:'SNR',un:'veces',v:snr},{k:'db',lab:'SNR',un:'dB',v:10*Math.log10(snr),abs:0.2},{k:'e',lab:'Error ε de |<i>H</i><sub>1</sub>|',un:'%',v:100*Math.sqrt(1-D.g2)/(Math.sqrt(D.g2)*Math.sqrt(2*D.nd))}]; },
 pasos:(D,R)=>[`SNR = γ²/(1 − γ²) = ${D.g2}/${s3(1-D.g2)} = ${s3(R[0].v)}; en dB, 10 log<sub>10</sub>(${s3(R[0].v)}) = ${f2(R[1].v,2)} dB.`,`ε[|<i>H</i><sub>1</sub>|] ≈ √(1 − γ²)/(|γ| √(2<i>n</i><sub>d</sub>)) = √${s3(1-D.g2)}/(${s3(Math.sqrt(D.g2))} × √${2*D.nd}) = ${s3(R[2].v/100)} = ${s3(R[2].v)} %.`,`Para reducir el error a la mitad hacen falta cuatro veces más promedios.`]},
{u:8, tit:'Dos grados de libertad: frecuencias y modos', gen:r=>{ const m1=uni(r,1,10,1), k1=Math.round(uni(r,2000,50000,-2)), mu=pick(r,[0.1,0.2,0.3,0.5]), be=pick(r,[0.5,0.7,1.5,2]); const m2=+(mu*m1).toPrecision(3); return {m1,k1,m2,k2:+(m2*be*be*k1/m1).toPrecision(3)}; },
 enun:D=>`Una estructura (<i>m</i><sub>1</sub> = <b>${D.m1} kg</b>, <i>k</i><sub>1</sub> = <b>${D.k1} N/m</b>, unida al suelo) sostiene un equipo (<i>m</i><sub>2</sub> = <b>${D.m2} kg</b>) montado sobre un resorte <i>k</i><sub>2</sub> = <b>${D.k2} N/m</b>. Sin amortiguamiento, calculen las dos frecuencias naturales del sistema y la forma del primer modo, <i>X</i><sub>2</sub>/<i>X</i><sub>1</sub>.`,
 res:D=>{ const a=D.m1*D.m2, b=D.m1*D.k2+D.m2*(D.k1+D.k2), c=D.k1*D.k2, q=Math.sqrt(b*b-4*a*c), l1=(b-q)/(2*a), l2=(b+q)/(2*a); return [{k:'f1',lab:'<i>f</i><sub>1</sub>',un:'Hz',v:Math.sqrt(l1)/TP},{k:'f2',lab:'<i>f</i><sub>2</sub>',un:'Hz',v:Math.sqrt(l2)/TP},{k:'r1',lab:'Modo 1: <i>X</i><sub>2</sub>/<i>X</i><sub>1</sub>',un:'',v:D.k2/(D.k2-D.m2*l1)}]; },
 pasos:(D,R)=>{ const a=D.m1*D.m2, b=D.m1*D.k2+D.m2*(D.k1+D.k2), c=D.k1*D.k2, q=Math.sqrt(b*b-4*a*c), l1=(b-q)/(2*a), l2=(b+q)/(2*a); return [`<b>M</b> = diag(${D.m1}, ${D.m2}) kg; <b>K</b> = [[<i>k</i><sub>1</sub> + <i>k</i><sub>2</sub>, −<i>k</i><sub>2</sub>], [−<i>k</i><sub>2</sub>, <i>k</i><sub>2</sub>]] = [[${s3(D.k1+D.k2)}, −${s3(D.k2)}], [−${s3(D.k2)}, ${s3(D.k2)}]] N/m.`,`det(<b>K</b> − λ<b>M</b>) = 0 con λ = ω²: <i>m</i><sub>1</sub><i>m</i><sub>2</sub>λ² − [<i>m</i><sub>1</sub><i>k</i><sub>2</sub> + <i>m</i><sub>2</sub>(<i>k</i><sub>1</sub> + <i>k</i><sub>2</sub>)]λ + <i>k</i><sub>1</sub><i>k</i><sub>2</sub> = 0, es decir ${s3(a)} λ² − ${s3(b)} λ + ${s3(c)} = 0.`,`λ = [${s3(b)} ∓ √(${s3(b*b-4*a*c)})]/(2 × ${s3(a)}): λ<sub>1</sub> = ${s3(l1)} y λ<sub>2</sub> = ${s3(l2)} rad²/s².`,`<i>f</i> = √λ/2π: <i>f</i><sub>1</sub> = ${s3(R[0].v)} Hz y <i>f</i><sub>2</sub> = ${s3(R[1].v)} Hz. Comprobación: λ<sub>1</sub>λ<sub>2</sub> = <i>k</i><sub>1</sub><i>k</i><sub>2</sub>/(<i>m</i><sub>1</sub><i>m</i><sub>2</sub>) = ${s3(c/a)}.`,`Modo 1, de la segunda ecuación: <i>X</i><sub>2</sub>/<i>X</i><sub>1</sub> = <i>k</i><sub>2</sub>/(<i>k</i><sub>2</sub> − <i>m</i><sub>2</sub>λ<sub>1</sub>) = ${s3(D.k2)}/(${s3(D.k2)} − ${s3(D.m2*l1)}) = ${s3(R[2].v)}: positivo, las masas se mueven en fase.`]; }},
];
// ---------------------------------------------------------------- estado y dibujo
let filtro=0, EST={};
function lee(){ try{ return JSON.parse(localStorage.getItem('ae-vib')||'{}'); }catch(e){ return {}; } }
function guarda(){ try{ localStorage.setItem('ae-vib',JSON.stringify(EST)); }catch(e){} }
EST=lee();
const semillas=P.map((_,i)=>Math.floor(Math.random()*1e9)+i);
function datos(i){ return P[i].gen(rng(semillas[i])); }
function num(t){ t=String(t).trim().replace(/\s/g,'').replace(',','.').replace('−','-'); if(t==='') return NaN; return Number(t); }
function correcto(v,x,c){ if(!isFinite(x)) return false; const tol=(c&&c.abs!==undefined)?c.abs:Math.max(TOL*Math.abs(v),1e-9); return Math.abs(x-v)<=tol+1e-12; }
function tarjeta(i){
  const p=P[i], D=datos(i), R=p.res(D), id='p'+i;
  const campos=R.map((c,j)=>`<div class="ae-campo" id="${id}c${j}"><label>${c.lab}</label><div class="in"><input inputmode="decimal" autocomplete="off" aria-label="${c.lab.replace(/<[^>]+>/g,'')}" id="${id}i${j}"><span class="un">${c.un}</span><span class="mk" id="${id}m${j}"></span></div></div>`).join('');
  return `<div class="ae-prob" data-u="${p.u}" id="${id}"><div class="u">Unidad ${p.u} · problema ${i+1}</div><h3>${p.tit}</h3><div class="enun">${p.enun(D)}</div>
    <div class="ae-campos">${campos}</div>
    <div class="ae-acc"><button class="btn on" data-a="comp" data-i="${i}">Comprobar</button><button class="btn" data-a="sol" data-i="${i}">Ver solución</button><button class="btn" data-a="nuevo" data-i="${i}">Datos nuevos</button></div>
    <div class="ae-msg" id="${id}msg"></div>
    <div class="ae-sol" id="${id}sol"><b>Solución</b><ol>${p.pasos(D,R).map(s=>'<li>'+s+'</li>').join('')}</ol><div style="margin-top:6px">Resultados: ${R.map(c=>c.lab+' = <span class="ae-res">'+s3(c.v)+(c.un?' '+c.un:'')+'</span>').join(' · ')}</div></div></div>`;
}
function pinta(){ $('lista').innerHTML=P.map((_,i)=>tarjeta(i)).join(''); aplicaFiltro(); marcador(); }
function repinta(i){ const el=$('p'+i), tmp=document.createElement('div'); tmp.innerHTML=tarjeta(i); el.replaceWith(tmp.firstElementChild); aplicaFiltro(); }
function aplicaFiltro(){ document.querySelectorAll('.ae-prob').forEach(e=>{ e.style.display=(filtro===0||+e.dataset.u===filtro)?'':'none'; }); }
function marcador(){ const n=Object.keys(EST).length, a=Object.values(EST).filter(v=>v==='a').length; $('marcador').textContent='Problemas resueltos en este navegador: '+n+' de '+P.length+(n?' ('+a+' a la primera)':'')+'. Tolerancia de comprobación: 2 % (0.2 dB en los niveles).'; }
function comprueba(i){
  const p=P[i], R=p.res(datos(i)); let bien=0, vacios=0;
  R.forEach((c,j)=>{ const x=num($('p'+i+'i'+j).value), box=$('p'+i+'c'+j), mk=$('p'+i+'m'+j); box.classList.remove('ok','mal'); mk.className='mk';
    if(isNaN(x)){ vacios++; mk.textContent=''; return; } const ok=correcto(c.v,x,c); box.classList.add(ok?'ok':'mal'); mk.classList.add(ok?'ok':'mal'); mk.textContent=ok?'\u2713':'\u2717'; if(ok) bien++; });
  const k='p'+i, intentos=(window.__int=window.__int||{}); let m;
  if(vacios===R.length) m='Escriban al menos un resultado.';
  else { intentos[k]=(intentos[k]||0)+1;
    if(bien===R.length){ m='Todo correcto.'; if(!EST[k]){ EST[k]=intentos[k]===1?'a':'b'; guarda(); marcador(); } }
    else m=bien+' de '+R.length+' correctos. Revisen unidades y el paso donde se separan'+(intentos[k]>=2?'; ya pueden abrir la solución.':'.'); }
  $('p'+i+'msg').textContent=m;
}
document.addEventListener('click',ev=>{ const b=ev.target.closest('button'); if(!b) return;
  if(b.dataset.f!==undefined){ filtro=+b.dataset.f; document.querySelectorAll('[data-f]').forEach(x=>x.classList.toggle('on',x===b)); aplicaFiltro(); return; }
  if(b.id==='todo-nuevo'){ for(let i=0;i<P.length;i++) semillas[i]=Math.floor(Math.random()*1e9); window.__int={}; pinta(); return; }
  const i=+b.dataset.i; if(b.dataset.a==='comp') comprueba(i);
  if(b.dataset.a==='sol'){ const s=$('p'+i+'sol'); s.classList.toggle('on'); b.textContent=s.classList.contains('on')?'Ocultar solución':'Ver solución'; }
  if(b.dataset.a==='nuevo'){ semillas[i]=Math.floor(Math.random()*1e9); if(window.__int) delete window.__int['p'+i]; repinta(i); }
});
document.addEventListener('keydown',ev=>{ if(ev.key==='Enter'&&ev.target.matches('.ae-campo input')){ const i=+ev.target.id.slice(1).split('i')[0]; comprueba(i); } });
window.__ae={P,datos,semillas,rng,correcto};
pinta();
"""
pagina("autoevaluacion.html", "Autoevaluación para el examen final", "Vibraciones · Repaso · U1 a U8",
       "Problemas de las ocho unidades con datos nuevos cada vez, comprobación inmediata con 2 % de tolerancia y solución paso a paso con los números del problema",
       cuerpo, script, "Autoevaluación del curso de Vibraciones (unidades 1 a 8) · material de apoyo para el examen final · funciona sin conexión (un solo archivo).")
