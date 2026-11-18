#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Andamiaje común de los exploradores generados (hoja de estilo, tema, pie y contador tomados de mediapotencia).
Origen: cabecera de gen_nuevos.py. Uso: from base_pag import *   (sys.argv[1] = carpeta del sitio)
(texto original de gen_nuevos.py:)
  senales_interactivo.html  · Pilar 11 · Laboratorio de señales (U7, temas 7.1 y 7.2)
  dosgdl_interactivo.html   · Pilar 12 · Dos grados de libertad y absorbedor (U8)
Toman la hoja de estilo, el tema, el pie y el contador de un explorador existente (mediapotencia), de modo que
el aspecto es idéntico. Uso: python3 gen_nuevos.py CARPETA   (después: mejoras.py e integra.py)"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mml import M
D = sys.argv[1]
I = lambda t: M(t, inline=True)
base = open(os.path.join(D, "mediapotencia_interactivo.html"), encoding="utf-8").read()
_limpia = re.sub(r"<!-- (\w+):inicio -->.*?<!-- \1:fin -->\n?", "", base, flags=re.S)   # sin bloques inyectados
CSS = re.search(r"<style>.*?</style>", _limpia, re.S).group(0)
TEMA = re.search(r"<!-- tema:inicio -->.*?<!-- tema:fin -->", base, re.S).group(0)
CONT = re.search(r"<!-- contador:inicio -->.*?<!-- contador:fin -->", base, re.S).group(0)
PIE = re.search(r"<footer>.*?</footer>", base, re.S).group(0)
EXTRA = """<style>
  .grp{border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin-bottom:10px}
  .grp .t{font-size:11.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--orange);margin-bottom:6px}
  .nota{font-size:12px;color:var(--grey);margin:6px 0 0}
  select,.archivo{font:inherit;font-size:13px;border:1px solid var(--line);border-radius:8px;padding:5px 8px;background:#fff}
  .tiles.t3{grid-template-columns:1fr 1fr 1fr} @media(max-width:520px){.tiles.t3{grid-template-columns:1fr 1fr}}
  .tile .v{font-size:18px} .tile.al .v{color:var(--red)}
  .two{display:grid;grid-template-columns:1fr;gap:12px} @media(min-width:900px){.two{grid-template-columns:1fr 1fr}}
  .eqbox{overflow-x:auto} .two>div{min-width:0}
  .oculto .tile .v,.oculto table.res td,.oculto .resp{filter:blur(7px);user-select:none}
  .tile .v{overflow-wrap:anywhere}
  table.tb{border-collapse:collapse;font-size:13px;width:100%} table.tb td,table.tb th{border-bottom:1px solid var(--line);padding:5px 8px;text-align:left} table.tb th{color:var(--navy)}
</style>"""

def pagina(archivo, titulo, hk, lede, cuerpo, script, pie1):
    pie = re.sub(r'<div style="margin-bottom:8px">.*?</div>', '<div style="margin-bottom:8px">%s</div>' % pie1, PIE, count=1, flags=re.S)
    s = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="author" content="Elodie Strupiechonski; Andrés de Luna Bugallo">
<title>{titulo} · Explorador · Vibraciones · ENES Juriquilla</title>
{CSS}
{EXTRA}
{TEMA}
</head>
<body>
<header>
  <div class="in">
    <h1>{titulo}</h1>
    <p><span class="hk">{hk}</span>{lede}</p>
  </div>
</header>

<div class="wrap">
{cuerpo}
</div>

{pie}

<script>
"use strict";
{script}
</script>
{CONT}
</body>
</html>
"""
    open(os.path.join(D, archivo), "w", encoding="utf-8").write(s); print("generado", archivo, len(s))

def fila(lab, i, mn, mx, st, v, u=""):
    return f'<div class="row"><label>{lab}</label><input id="{i}" type="range" min="{mn}" max="{mx}" step="{st}" value="{v}"><span class="val" id="v{i}">{v}{(" " + u) if u else ""}</span></div>'
def tile(k, i, cls=""):
    return f'<div class="tile {cls}"><div class="k">{k}</div><div class="v" id="{i}">…</div></div>'
def eq(lab, cuerpo, st=""): return f'<div class="eqbox" style="margin-top:10px;{st}"><span class="lab">{lab}</span>{cuerpo}</div>'
def nota(t): return '<div class="eqnote">%s</div>' % t


LIB = r"""
const NAVY='#1F3864',STEEL='#4472C4',ORANGE='#C55A11',GREEN='#2E7D46',GREY='#5B5B5B',RED='#B23A3A',PURPLE='#6B3FA0';
const $=id=>document.getElementById(id);
function lienzo(cv,H){ const c=cv.getContext('2d'), dpr=Math.min(window.devicePixelRatio||1,2), W=cv.clientWidth||760; cv.width=W*dpr; cv.height=H*dpr; cv.style.height=H+'px'; c.setTransform(dpr,0,0,dpr,0,0); c.clearRect(0,0,W,H); return {c,W,H}; }
function pasos(a,b,n){ const d=(b-a)/n, p=Math.pow(10,Math.floor(Math.log10(d))), q=d/p, s=(q<1.5?1:q<3?2:q<7?5:10)*p, o=[]; for(let v=Math.ceil(a/s-1e-9)*s; v<=b+1e-9*s; v+=s) o.push(+v.toPrecision(12)); return o; }
function num(v){ const a=Math.abs(v); if(v===0) return '0'; if(a>=1e4||a<1e-2){ const e=Math.floor(Math.log10(a)+1e-9), m=+(v/Math.pow(10,e)).toPrecision(2); return (String(m)+'×10^'+e).replace(/-/g,'−'); } return String(+v.toPrecision(3)).replace('-','−'); }
// notación de ingeniería con prefijo SI
function ing(v,u){ if(!isFinite(v)) return '∞'; if(!(v>0)) return '0 '+u; const P=[[1e9,'G'],[1e6,'M'],[1e3,'k'],[1,''],[1e-3,'m'],[1e-6,'µ'],[1e-9,'n'],[1e-12,'p']]; for(const [f,p] of P){ if(v>=f*0.9995) return (+(v/f).toPrecision(3))+' '+p+u; } return num(v)+' '+u; }
// modo práctica: oculta las lecturas hasta que se pulse de nuevo
function practica(id){ const b=$(id); if(!b) return; b.addEventListener('click',()=>{ const on=document.body.classList.toggle('oculto'); b.classList.toggle('on',on); b.textContent=on?'Mostrar lecturas':'Ocultar lecturas (modo práctica)'; }); }
// Ejes: o={x0,x1,y0,y1,logx,logy,xl,yl,tit}; devuelve los mapeos X, Y y el rectángulo de trazo
function ejes(g,box,o){ const c=g.c, mL=box.mL||56, mR=box.mR||14, mT=box.mT||24, mB=box.mB||36, x=box.x||0, y=box.y||0, w=(box.w||g.W)-mL-mR, h=(box.h||g.H)-mT-mB, px=x+mL, py=y+mT;
  const lx=o.logx, ly=o.logy, ax=lx?Math.log10(o.x0):o.x0, bx=lx?Math.log10(o.x1):o.x1, ay=ly?Math.log10(o.y0):o.y0, by=ly?Math.log10(o.y1):o.y1;
  const X=v=>px+((lx?Math.log10(Math.max(v,1e-300)):v)-ax)/(bx-ax)*w, Y=v=>py+(1-((ly?Math.log10(Math.max(v,1e-300)):v)-ay)/(by-ay))*h;
  c.lineWidth=1; c.strokeStyle='#E3E9F3'; c.fillStyle=GREY; c.font='11px Arial';
  const tx=lx?decadas(o.x0,o.x1):pasos(o.x0,o.x1,o.nx||8), ty=ly?decadas(o.y0,o.y1):pasos(o.y0,o.y1,o.ny||5);
  c.textAlign='center'; c.textBaseline='top'; tx.forEach(v=>{ c.beginPath(); c.moveTo(X(v),py); c.lineTo(X(v),py+h); c.stroke(); c.fillText(lx?pot(v):num(v),X(v),py+h+5); });
  c.textAlign='right'; c.textBaseline='middle'; ty.forEach(v=>{ c.beginPath(); c.moveTo(px,Y(v)); c.lineTo(px+w,Y(v)); c.stroke(); c.fillText(ly?pot(v):num(v),px-6,Y(v)); });
  c.strokeStyle='#9AA7BF'; c.strokeRect(px,py,w,h);
  c.fillStyle=NAVY; c.textAlign='left'; c.textBaseline='top'; if(o.tit){ let fs=12; do{ c.font='bold '+fs+'px Arial'; fs-=0.5; } while(fs>8.5&&c.measureText(o.tit.replace(/[_^]/g,'')).width>w+mR-2); c.fillText(o.tit,px,y+5); } c.font='bold 12px Arial';
  c.textAlign='center'; if(o.xl) c.fillText(o.xl,px+w/2,py+h+20);
  if(o.yl){ c.save(); c.translate(x+12,py+h/2); c.rotate(-Math.PI/2); c.textBaseline='middle'; c.fillText(o.yl,0,0); c.restore(); }
  return {X,Y,px,py,w,h,c,o}; }
function pot(v){ const e=Math.round(Math.log10(v)); return (e>=-2&&e<=3)?String(+Math.pow(10,e).toPrecision(1)):'10^'+(e<0?'−'+(-e):e); }
function decadas(a,b){ const o=[]; for(let e=Math.ceil(Math.log10(a)-1e-9); e<=Math.log10(b)+1e-9; e++) o.push(Math.pow(10,e)); return o; }
function curva(e,pts,color,lw,dash){ const c=e.c; c.save(); c.beginPath(); c.rect(e.px,e.py,e.w,e.h); c.clip(); c.strokeStyle=color; c.lineWidth=lw||1.6; c.setLineDash(dash||[]); c.beginPath(); let on=false;
  for(const p of pts){ if(!isFinite(p[1])){ on=false; continue; } const x=e.X(p[0]), y=e.Y(p[1]); on?c.lineTo(x,y):c.moveTo(x,y); on=true; } c.stroke(); c.restore(); }
function funcion(e,f,color,lw,dash,n){ n=n||Math.round(e.w); const o=e.o, pts=[]; for(let i=0;i<=n;i++){ const u=i/n, x=o.logx?o.x0*Math.pow(o.x1/o.x0,u):o.x0+(o.x1-o.x0)*u; pts.push([x,f(x)]); } curva(e,pts,color,lw,dash); }
function vline(e,x,color,dash,txt,dy){ const c=e.c; if(x<Math.min(e.o.x0,e.o.x1)||x>Math.max(e.o.x0,e.o.x1)) return; c.save(); c.strokeStyle=color; c.setLineDash(dash||[5,4]); c.lineWidth=1.2; c.beginPath(); c.moveTo(e.X(x),e.py); c.lineTo(e.X(x),e.py+e.h); c.stroke(); c.setLineDash([]);
  if(txt){ c.fillStyle=color; c.font='bold 11px Arial'; const der=e.X(x)>e.px+e.w-110; c.textAlign=der?'right':'left'; c.textBaseline='top'; c.fillText(txt,e.X(x)+(der?-4:4),e.py+4+(dy||0)); } c.restore(); }
function hline(e,y,color,dash,txt){ const c=e.c; c.save(); c.strokeStyle=color; c.setLineDash(dash||[5,4]); c.lineWidth=1.2; c.beginPath(); c.moveTo(e.px,e.Y(y)); c.lineTo(e.px+e.w,e.Y(y)); c.stroke(); c.setLineDash([]);
  if(txt){ c.fillStyle=color; c.font='bold 11px Arial'; c.textAlign='right'; c.textBaseline='bottom'; c.fillText(txt,e.px+e.w-4,e.Y(y)-2); } c.restore(); }
function punto(e,x,y,color,r){ const c=e.c; c.fillStyle=color; c.strokeStyle='#fff'; c.lineWidth=1.5; c.beginPath(); c.arc(e.X(x),e.Y(y),r||5,0,7); c.fill(); c.stroke(); }
// Enlaza deslizadores: UN = {id:' unidad'}; llama a cb en cada cambio
function liga(S,UN,cb){ Object.keys(UN).forEach(id=>$(id).addEventListener('input',ev=>{ S[id]=+ev.target.value; $('v'+id).textContent=(+S[id].toPrecision(6))+UN[id]; cb(); })); }
function pon(S,UN,o,cb){ Object.keys(o).forEach(k=>{ S[k]=o[k]; if($(k)&&UN[k]!==undefined){ $(k).value=o[k]; $('v'+k).textContent=o[k]+UN[k]; } }); cb(); }
"""
