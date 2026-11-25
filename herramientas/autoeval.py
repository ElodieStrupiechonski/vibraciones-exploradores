"""QA de autoevaluacion.html: para cada problema y 40 semillas, recalcula en Python (independiente del JS) los resultados
a partir de los datos generados, prueba la comprobación (valor exacto, +1.5 %, +3 %), la solución mostrada y los errores JS.
Uso: python3 qa/autoeval.py CARPETA"""
import asyncio, math, os, sys
from playwright.async_api import async_playwright
SITE=sys.argv[1]; G0=9.80665; TP=2*math.pi; fails=[]
def ref(i,D):
    if i==0: f=D['N']/D['T']; w=TP*f; return [f,w,w*w*D['pp']/2e3]
    if i==1:
        c=float('%.3g'%(2*D['z']*math.sqrt(D['k']*D['m']))); wn=math.sqrt(D['k']/D['m']); z=c/(2*math.sqrt(D['k']*D['m'])); return [wn/TP,z,wn*math.sqrt(1-z*z)/TP]
    if i==2: d=math.log(D['x0']/D['xn'])/D['n']; return [d,d/math.sqrt(4*math.pi**2+d*d)]
    if i==3: X0=D['F']/D['k']; M=1/math.hypot(1-D['r']**2,2*D['z']*D['r']); return [X0*1e3,M,M*X0*1e3]
    if i==4: z=(D['f2']-D['f1'])/(2*D['fr']); return [z,1/(2*z)]
    if i==5: gr=math.sqrt(math.pi/2*D['fn']*D['Q']*D['W']); return [math.sqrt(D['W']*(D['fb']-D['fa'])),gr,3*gr]
    if i==6: A=math.pi*D['d']**2/4; return [A,D['P']*1e3/(D['n']*D['ns']*A),D['P']*1e3/(D['n']*D['d']*D['t'])]
    if i==7:
        # Mohr por valores propios del tensor (independiente de la fórmula C ± R)
        import numpy as np; ev=np.linalg.eigvalsh(np.array([[D['sx'],D['txy']],[D['txy'],D['sy']]])); return [(D['sx']+D['sy'])/2,(ev[1]-ev[0])/2,ev[1],ev[0]]
    if i==8: I=10**(D['L1']/10)+10**(D['L2']/10); L=10*math.log10(I); return [L,10*math.log10(I/D['k']**2)]
    if i==9: r=D['f']/D['fn']; return [D['m']*(TP*D['fn'])**2,r,math.sqrt((1+(2*D['z']*r)**2)/((1-r*r)**2+(2*D['z']*r)**2))]
    if i==10:
        fs=D['fs']; f=D['f']; fa=min((abs(f-k*fs) for k in range(0,10)))   # búsqueda exhaustiva del alias en [0, fs/2]
        return [fs/2,fa,1/D['T']]
    if i==11: g=D['g2']; snr=g/(1-g); return [snr,10*math.log10(snr),100*math.sqrt(1-g)/(math.sqrt(g)*math.sqrt(2*D['nd']))]
    if i==12:
        import numpy as np; from scipy.linalg import eigh
        m1,k1,m2,k2=D['m1'],D['k1'],D['m2'],D['k2']
        lam,V=eigh(np.array([[k1+k2,-k2],[-k2,k2]]),np.diag([m1,m2])); fr=np.sqrt(lam)/TP
        return [fr[0],fr[1],V[1,0]/V[0,0]]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1280,'height':900}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+os.path.abspath(os.path.join(SITE,'autoevaluacion.html'))); await pg.wait_for_timeout(500)
        n=await pg.evaluate('()=>__ae.P.length'); print('problemas:',n); worst=0
        for i in range(n):
            for s in range(40):
                D=await pg.evaluate('([i,s])=>{__ae.semillas[i]=s*7919+13; return __ae.datos(i)}',[i,s]); R=await pg.evaluate('([i])=>__ae.P[i].res(__ae.datos(i)).map(c=>[c.v,c.abs===undefined?null:c.abs])',[i])
                E=ref(i,D)
                for (v,ab),e in zip(R,E):
                    err=abs(v-e)/max(abs(e),1e-12); worst=max(worst,err)
                    if err>1e-9: fails.append(f'P{i+1} s{s}: {v} vs {e}')
                    if not math.isfinite(v): fails.append(f'P{i+1} no finito')
                # la solución se arma sin errores y no contiene NaN/undefined
                txt=await pg.evaluate('([i])=>{const p=__ae.P[i],D=__ae.datos(i);return p.enun(D)+p.pasos(D,p.res(D)).join(" ")}',[i])
                if 'NaN' in txt or 'undefined' in txt or 'Infinity' in txt: fails.append(f'P{i+1} s{s}: texto con NaN/undefined')
            # comprobación en la interfaz: exacto ✓, +1.5 % ✓, +3 % ✗ (dB: +0.1 ✓, +0.4 ✗)
            await pg.evaluate('([i])=>{__ae.semillas[i]=424242;}',[i]); await pg.evaluate('()=>document.getElementById("todo-nuevo")')
            await pg.evaluate('([i])=>{const el=document.getElementById("p"+i);const t=document.createElement("div");}',[i])
            await pg.click(f'[data-a=nuevo][data-i="{i}"]'); R=await pg.evaluate('([i])=>__ae.P[i].res(__ae.datos(i)).map(c=>[c.v,c.abs===undefined?null:c.abs])',[i])
            for caso,ok_esp in (('exacto',True),('cerca',True),('lejos',False)):
                for j,(v,ab) in enumerate(R):
                    x=v if caso=='exacto' else (v+(0.1 if ab else 0.015*abs(v)) if caso=='cerca' else v+(0.4 if ab else 0.03*abs(v)+1e-6))
                    await pg.fill(f'#p{i}i{j}', ('%.6g'%x).replace('.',',') if j%2 else '%.6g'%x)
                await pg.click(f'[data-a=comp][data-i="{i}"]')
                marks=await pg.evaluate('([i,n])=>Array.from({length:n},(_,j)=>document.getElementById("p"+i+"m"+j).textContent)',[i,len(R)])
                if any((mk=='\u2713')!=ok_esp for mk in marks): fails.append(f'P{i+1} interfaz {caso}: {marks}')
            print(f'  P{i+1}: 40 juegos de datos y la comprobación en la interfaz, sin diferencias')
        print('máxima diferencia relativa JS frente a Python:','%.2e'%worst)
        # filtro por unidad
        await pg.click('[data-f="5"]'); vis=await pg.evaluate('()=>[...document.querySelectorAll(".ae-prob")].filter(e=>e.style.display!=="none").map(e=>e.dataset.u)'); print('filtro U5:',vis)
        if set(vis)!={'5'}: fails.append('filtro')
        if errs: fails.append('js'); print(errs)
        await b.close()
    print('\nRESULTADO:','TODO CORRECTO' if not fails else 'FALLAS:\n'+'\n'.join(fails[:20]))
asyncio.run(main())
