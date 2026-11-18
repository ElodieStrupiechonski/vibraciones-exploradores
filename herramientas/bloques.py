# -*- coding: utf-8 -*-
"""Bloques comunes del sitio de exploradores de Vibraciones (se inyectan entre marcas, de forma idempotente)."""

# --------------------------------------------------------------------------- tipografía y notación
TIPO_INI, TIPO_FIN = "<!-- tipografia:inicio -->", "<!-- tipografia:fin -->"
TIPOGRAFIA = TIPO_INI + r'''
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Questrial&family=STIX+Two+Text:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<style>
  /* Tipografías del Manual de identidad gráfica de la ENES Juriquilla (nov. 2025): Century Gothic en títulos,
     Arial en texto y lecturas, Cambria en fórmulas. Mismo bloque que el sitio de Teoría Electromagnética. */
  :root:root{
    --f-tit:"Century Gothic","Questrial","URW Gothic","Avant Garde",sans-serif;
    --sans:Arial,"Helvetica Neue",Helvetica,"Liberation Sans",Calibri,sans-serif;
    --serif:Cambria,"STIX Two Text","Times New Roman",serif;
    --mono:Arial,"Helvetica Neue",Helvetica,"Liberation Sans",sans-serif;
  }
  body,button,input,select,textarea{font-family:var(--sans)}
  body{font-variant-numeric:tabular-nums}
  h1,h2,h3,.ct,.eyebrow,header .hk{font-family:var(--f-tit)!important;letter-spacing:0}
  header .hk{letter-spacing:.08em}
  sub,sup{font-size:.72em;line-height:0;position:relative;vertical-align:baseline}
  sub{bottom:-.25em} sup{top:-.45em}
  math{font-family:"Cambria Math","STIX Two Math","Latin Modern Math","Noto Sans Math",math,serif;font-size:1.08em}
  math[display="block"]{margin:.35em 0}
  .eqbox math[display="block"]{font-size:1.16em;margin:.5em 0}
  .eqbox{overflow-x:auto;overflow-y:hidden;max-width:100%}
  .wrap>*,.card,.two>*,.grid3>*{min-width:0}
  @media(max-width:560px){.eqbox math[display="block"]{font-size:.95em}}
  body .btn{color:var(--blue,#2E5496)} body .btn.on{color:#fff}
  .eqnote{font-family:var(--sans);font-size:12.5px;color:var(--grey,#5a5a5a);text-align:center;margin:.15em 0 .1em}
  .mth,.val,.tile .v,.eqbox{font-family:var(--serif)!important}
  .legend>span,.reglegend .it{display:inline-block!important}
  .legend .sw,.legend .dot,.reglegend .gl{margin-right:6px;vertical-align:middle}
</style>
<script>
(function(){
  var UNI="₀₁₂₃₄₅₆₇₈₉ₐₑₒₓₕₖₗₘₙₚₛₜᵢᵣᵤᵥⱼ", ASC="0123456789aeoxhklmnpstiruvj";
  function asc(s){return s.split('').map(function(c){return ASC[UNI.indexOf(c)];}).join('');}
  // ---- lienzos: subíndices y superíndices (M_máx, f_n, fₙ, 10^3) con tamaño y posición correctos ----
  var RX=/([A-Za-zΑ-Ωα-ω′])_(\{[^}]+\}|[A-Za-z0-9áéíóúñ,]{1,6})|\^(\{[^}]+\}|\([^)]+\)|[−-]?\d{1,3})|([₀-₉ₐₑₒₓₕₖₗₘₙₚₛₜᵢᵣᵤᵥⱼ]+)/g;
  var P=CanvasRenderingContext2D.prototype, F=P.fillText;
  P.fillText=function(t,x,y,mw){
    t=String(t);
    if(!/[_^₀-₉ₐₑₒₓₕₖₗₘₙₚₛₜᵢᵣᵤᵥⱼ]/.test(t)||/\.(html|py|png|csv|txt|svg|jpg|pdf)\b/i.test(t)) return F.call(this,t,x,y,mw);
    var sg=[],last=0,m; RX.lastIndex=0;
    while((m=RX.exec(t))){
      if(m[1]){sg.push([t.slice(last,m.index)+m[1],0]);sg.push([m[2].replace(/[{}]/g,''),1]);}
      else if(m[3]){sg.push([t.slice(last,m.index),0]);sg.push([m[3].replace(/[{}()]/g,''),2]);}
      else{sg.push([t.slice(last,m.index),0]);sg.push([asc(m[4]),1]);}
      last=RX.lastIndex;
    }
    if(!sg.length) return F.call(this,t,x,y,mw);
    sg.push([t.slice(last),0]);
    var f0=this.font, mm=/(\d+(?:\.\d+)?)px/.exec(f0), px=mm?+mm[1]:12,
        fs=mm?f0.replace(mm[0],(px*0.72).toFixed(1)+'px'):f0, W=0,i;
    for(i=0;i<sg.length;i++){this.font=sg[i][1]?fs:f0;sg[i][2]=this.measureText(sg[i][0]).width;W+=sg[i][2];}
    var a=this.textAlign, x0=x;
    if(a==='center') x0=x-W/2; else if(a==='right'||a==='end') x0=x-W;
    this.textAlign='left';
    for(i=0;i<sg.length;i++){
      this.font=sg[i][1]?fs:f0;
      F.call(this,sg[i][0],x0,y+(sg[i][1]===1?0.28*px:sg[i][1]===2?-0.38*px:0));
      x0+=sg[i][2];
    }
    this.font=f0; this.textAlign=a;
  };
  // ---- texto generado por los scripts: la misma notación en <sub>/<sup> ----
  var US=/([A-Za-zΑ-Ωα-ω′])_(\{[^}]+\}|[A-Za-z0-9áéíóúñ]{1,6})|\^(\{[^}]+\}|\([^)]+\)|[−-]?\d{1,3})|([₀-₉ₐₑₒₓₕₖₗₘₙₚₛₜᵢᵣᵤᵥⱼ]+)/g;
  var SALTA={SCRIPT:1,STYLE:1,TEXTAREA:1,OPTION:1,PRE:1,CODE:1,TITLE:1,INPUT:1,SELECT:1,BUTTON:0};
  function dentroDe(p){for(;p;p=p.parentNode){var n=p.nodeName; if(SALTA[n]||n==='math'||n==='MATH'||n==='svg') return true;} return false;}
  function arreglar(n){
    var p=n.parentNode; if(!p||dentroDe(p)) return;
    var t=n.nodeValue; US.lastIndex=0; if(!US.test(t)||/\.(html|py|png|csv)\b/.test(t)) return;
    US.lastIndex=0; var fr=document.createDocumentFragment(), last=0, m, e;
    while((m=US.exec(t))){
      var antes=t.slice(last,m.index);
      if(m[1]){fr.appendChild(document.createTextNode(antes+m[1]));e=document.createElement('sub');e.textContent=m[2].replace(/[{}]/g,'');}
      else if(m[3]){fr.appendChild(document.createTextNode(antes));e=document.createElement('sup');e.textContent=m[3].replace(/[{}()]/g,'');}
      else{fr.appendChild(document.createTextNode(antes));e=document.createElement('sub');e.textContent=asc(m[4]);}
      fr.appendChild(e); last=US.lastIndex;
    }
    fr.appendChild(document.createTextNode(t.slice(last)));
    p.replaceChild(fr,n);
  }
  function recorrer(r){
    if(r.nodeType===3){arreglar(r);return;}
    if(r.nodeType!==1||SALTA[r.nodeName]) return;
    var w=document.createTreeWalker(r,NodeFilter.SHOW_TEXT,null), l=[], n;
    while((n=w.nextNode())) l.push(n);
    l.forEach(arreglar);
  }
  function inicio(){
    recorrer(document.body);
    new MutationObserver(function(ms){ms.forEach(function(m){
      if(m.type==='characterData') arreglar(m.target); else m.addedNodes.forEach(recorrer);
    });}).observe(document.body,{childList:true,subtree:true,characterData:true});
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',inicio); else inicio();
})();
</script>
''' + TIPO_FIN

# --------------------------------------------------------------------------- entrada por teclado
TEC_INI, TEC_FIN = "<!-- teclado:inicio -->", "<!-- teclado:fin -->"
TECLADO = TEC_INI + r'''
<style>
  .kbnum{width:84px;font:inherit;font-family:var(--serif,Cambria,serif);font-weight:700;font-size:15px;color:var(--orange,#C55A11);text-align:right;
    border:1px solid var(--line,#d3deee);border-radius:6px;padding:3px 6px;background:var(--card,#fff);font-variant-numeric:tabular-nums}
  .kbnum:focus{outline:2px solid var(--steel,#4472C4);outline-offset:1px}
  .kbnum.kbmal{border-color:#B23A3A;background:#fdeeee}
  .kbunit{min-width:26px;font-size:12.5px;color:var(--grey,#5a5a5a);font-family:var(--sans,Arial,sans-serif)}
  .kbhid{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
  .row input[type=range]{min-width:90px!important;flex:1 1 90px}
  .row label{min-width:0!important;flex:0 1 132px}
  .kbrow{flex-wrap:nowrap!important}
  .kbunit:empty{display:none}
  .kbayuda{font-size:11.5px;color:var(--grey,#5a5a5a);margin:6px 0 0}
  @media print{.kbnum{border:0}}
</style>
<script>
/* Entrada por teclado: cada deslizador recibe una casilla numérica sincronizada. El valor escrito no queda
   limitado al paso del deslizador; se valida contra su intervalo (Enter o Tab lo aplican, Esc lo descarta). */
(function(){
  var ENTEROS={nf:1};
  function mapa(id){ try{ if(id==='sfn'&&typeof fnFromSlider==='function') return {s2v:function(s){return Math.round(fnFromSlider(s));},v2s:function(v){return sliderFromFn(v);},min:Math.round(fnFromSlider(0)),max:Math.round(fnFromSlider(1000)),dec:0}; }catch(e){} return null; }
  function ndec(x){ var s=String(x); var i=s.indexOf('.'); return i<0?0:Math.min(6,s.length-i-1); }
  function limpio(v,d){ return String(+(+v).toFixed(Math.max(d,0))); }
  function cablear(r){
    if(r.dataset.kb) return; r.dataset.kb='1';
    var mp=mapa(r.id), paso=parseFloat(r.getAttribute('step'))||1, mn=parseFloat(r.min), mx=parseFloat(r.max);
    if(isNaN(mn)) mn=0; if(isNaN(mx)) mx=100;
    var d=mp?mp.dec:Math.max(ndec(paso),ndec(mn)), vmin=mp?mp.min:mn, vmax=mp?mp.max:mx;
    var span=null, s=r.nextElementSibling; if(s&&s.classList&&s.classList.contains('val')) span=s;
    var n=document.createElement('input'); n.type='text'; n.inputMode='decimal'; n.className='kbnum'; n.autocomplete='off'; n.spellcheck=false;
    var lab=r.parentNode.querySelector('label'); var nombre=(lab?lab.textContent:(r.getAttribute('aria-label')||r.id)).replace(/\s+/g,' ').trim();
    n.setAttribute('aria-label',nombre+': escribir el valor');
    n.title='Escribir un valor entre '+limpio(vmin,6).replace('-','−')+' y '+limpio(vmax,6)+' y pulsar Enter';
    var u=document.createElement('span'); u.className='kbunit';
    r.parentNode.insertBefore(n,r.nextSibling); r.parentNode.insertBefore(u,n.nextSibling);
    if(span) span.classList.add('kbhid');
    if(r.parentNode.classList.contains('row')) r.parentNode.classList.add('kbrow');
    if(!mp) r.step='any';
    function actual(){ return mp?mp.s2v(+r.value):+r.value; }
    function mostrar(){
      if(document.activeElement!==n){ n.value=limpio(actual(),6).replace('-','−'); n.classList.remove('kbmal'); }
      if(span){ var t=span.textContent.replace(/^\s*[−+\-]?[\d.,\s]*/,'').trim(); u.textContent=/^[^\d]{0,12}$/.test(t)?t:''; }
    }
    // arrastre con el ratón o las flechas: se conserva el paso original del deslizador
    r.addEventListener('input',function(e){
      if(!e.kb&&!mp){ var v=mn+Math.round((+r.value-mn)/paso)*paso; v=Math.min(mx,Math.max(mn,v)); r.value=limpio(v,ndec(paso)+ndec(mn)); }
    },true);
    r.addEventListener('input',function(){ mostrar(); });
    function aplicar(){
      var v=parseFloat(n.value.replace('−','-').replace(',','.'));
      if(isNaN(v)){ n.classList.add('kbmal'); n.value=limpio(actual(),6).replace('-','−'); setTimeout(function(){ n.classList.remove('kbmal'); },900); return; }
      if(ENTEROS[r.id]) v=Math.round(v);
      if(v<vmin||v>vmax){ n.classList.add('kbmal'); v=Math.min(vmax,Math.max(vmin,v)); } else n.classList.remove('kbmal');
      r.value=mp?mp.v2s(v):v;
      var ev=new Event('input',{bubbles:true}); ev.kb=true; r.dispatchEvent(ev);
      var ev2=new Event('change',{bubbles:true}); ev2.kb=true; r.dispatchEvent(ev2);
      n.value=limpio(mp?v:+r.value,6).replace('-','−');
    }
    n.addEventListener('change',aplicar);
    n.addEventListener('keydown',function(e){ e.stopPropagation(); if(e.key==='Enter'){ aplicar(); n.select(); } else if(e.key==='Escape'){ n.blur(); mostrar(); } });
    n.addEventListener('focus',function(){ n.select(); });
    n.addEventListener('blur',function(){ setTimeout(mostrar,0); });
    if(span) new MutationObserver(mostrar).observe(span,{childList:true,characterData:true,subtree:true});
    mostrar();
  }
  function todos(raiz){ (raiz.querySelectorAll?raiz.querySelectorAll('input[type=range]'):[]).forEach(cablear); }
  function inicio(){
    todos(document);
    new MutationObserver(function(ms){ ms.forEach(function(m){ m.addedNodes.forEach(function(x){ if(x.nodeType===1){ if(x.matches&&x.matches('input[type=range]')) cablear(x); todos(x); } }); }); }).observe(document.body,{childList:true,subtree:true});
    // las casillas numéricas ya existentes aceptan coma decimal y no disparan la navegación con flechas
    document.querySelectorAll('input[type=number]').forEach(function(x){ x.addEventListener('keydown',function(e){ e.stopPropagation(); }); });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',inicio); else inicio();
})();
</script>
''' + TEC_FIN
