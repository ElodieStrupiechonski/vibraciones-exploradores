import asyncio, math, os, sys
from playwright.async_api import async_playwright
SITE=sys.argv[1]; fails=[]
def chk(n,got,exp,tol=0.01):
    g=float(str(got).replace('−','-').replace(',','').split()[0]); ok=abs(g-exp)<=tol*max(abs(exp),1e-9)+1e-9; print('ok  ' if ok else 'FAIL',n,got,'esperado',round(exp,4)); 
    if not ok: fails.append(n)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        async def op(f):
            pg=await b.new_page(); pg._e=[]; pg.on('pageerror',lambda e:pg._e.append(str(e)))
            await pg.route('**/*', lambda r: r.continue_() if r.request.url.startswith('file:') else r.abort())
            await pg.goto('file://'+os.path.abspath(os.path.join(SITE,f))); await pg.wait_for_timeout(400); return pg
        T=lambda pg,i: pg.locator('#'+i).text_content()
        async def setv(pg,rid,v):
            el=pg.locator(f'#{rid} + input.kbnum'); await el.fill(str(v)); await el.press('Enter')
        pg=await op('senales_interactivo.html')
        chk('N',(await T(pg,'oN')).replace(',',''),4000); chk('df',await T(pg,'oDf'),0.25); chk('nd',await T(pg,'oNd'),5); chk('Be Hann',await T(pg,'oBe'),0.375); chk('eps',(await T(pg,'oEr')).replace('%',''),100/math.sqrt(5))
        print('   alias:',await T(pg,'oA2')); chk('Parseval',await T(pg,'oRp'),float((await T(pg,'oRt')).split()[0]),0.02)
        # rms exacto de la suma coherente: A1 sin(θ) + A2 sin(-θ+1)·(alias de 170 con fs=200 invierte la frecuencia)
        a=complex(1,0)-0.5*complex(math.cos(-1),math.sin(-1)); chk('rms muestreado (fasores + ruido)',await T(pg,'oRt'),math.sqrt(abs(a)**2/2+0.04),0.02)
        await setv(pg,'fs',400); print('   fs=400 ->',await T(pg,'oA2')); chk('rms sin alias',await T(pg,'oRt'),math.sqrt(0.5+0.125+0.04),0.02)
        await pg.click('[data-pre=F]'); d=0.4; rect=math.sin(math.pi*d)/(math.pi*d)
        chk('fuga rectangular',await T(pg,'oPk'),rect,0.005); await pg.click('#wH'); chk('fuga Hann',await T(pg,'oPk'),rect/(1-d*d),0.005)
        await setv(pg,'ts',10); chk('sin fuga (T_seg = 10 s)',await T(pg,'oPk'),1.0,0.005)
        await pg.click('[data-pre=W]'); chk('Welch nd',await T(pg,'oNd'),100); chk('Welch eps',(await T(pg,'oEr')).replace('%',''),10); chk('Welch Parseval',await T(pg,'oRp'),math.sqrt(0.045+0.005+0.25),0.02)
        piso=await pg.evaluate("()=>{const r=__lab.calc(),G=r.W.G;let s=0,n=0;for(let k=20;k<G.length-20;k++){const f=k*r.W.df;if(Math.abs(f-30)>3&&Math.abs(f-70)>3){s+=G[k];n++;}}return s/n}"); chk('piso de ruido 2σ²/fs',piso,2*0.25/200,0.05)
        # FFT de longitud no potencia de 2 frente a DFT directa
        e=await pg.evaluate("()=>{const n=300,x=Array.from({length:n},(_,i)=>Math.sin(0.37*i)+0.3*Math.cos(1.1*i*i%7));const [re,im]=__lab.fft(x);let m=0;for(let k=0;k<n;k+=17){let a=0,b=0;for(let j=0;j<n;j++){a+=x[j]*Math.cos(2*Math.PI*k*j/n);b-=x[j]*Math.sin(2*Math.PI*k*j/n);}m=Math.max(m,Math.abs(a-re[k]),Math.abs(b-im[k]));}return m}"); print('   error máx. FFT Bluestein vs DFT:',e); 
        if e>1e-8: fails.append('fft')
        csv='"Time (s)","ax","ay","az"\n'+'\n'.join('%.4f,%.5f,%.5f,%.5f'%(i/250,0.1,0.2,9.0+0.8*math.sin(2*math.pi*12.5*i/250)) for i in range(5000))
        r=await pg.evaluate("(t)=>{const c=__lab.leerCSV(t);return [c.fs,c.cols.length,c.sel,c.nombres[2]]}",csv); print('   CSV:',r); chk('CSV fs',r[0],250,0.001)
        print(pg._e)
        pg=await op('dosgdl_interactivo.html'); wn=20; q1=math.sqrt((2.1-math.sqrt(2.1**2-4))/2); q2=math.sqrt((2.1+math.sqrt(2.1**2-4))/2)
        chk('w1',await T(pg,'oW1'),q1*wn,0.001); chk('w2',await T(pg,'oW2'),q2*wn,0.001); chk('u1',await T(pg,'oU1'),1/(1-q1*q1),0.001); chk('u2',await T(pg,'oU2'),1/(1-q2*q2),0.001)
        # verificación independiente con numpy: valores propios y respuesta compleja
        import numpy as np
        M_=np.diag([10,1.0]); K_=np.array([[4400,-400],[-400,400.0]]); w=np.sqrt(np.linalg.eigvals(np.linalg.solve(M_,K_))); print('   numpy ω:',sorted(w))
        C_=np.array([[2*.01*10*20+2*.02*1*20,-2*.02*20],[-2*.02*20,2*.02*20]]); om=20*1.0; X=np.linalg.solve(K_-om**2*M_+1j*om*C_,[1,0])*4000
        chk('|X1|/X0 en r=1',await T(pg,'oX1'),abs(X[0]),0.02); chk('|X2|/X0 en r=1',await T(pg,'oX2'),abs(X[1]),0.01); chk('sola',await T(pg,'oXs'),50,0.01)
        await pg.click('#bT'); chk('antirresonancia X1',float(await T(pg,'oX1'))+1,1,0.001); chk('X2 = k1/k2',await T(pg,'oX2'),10,0.005)
        await pg.click('#bDH'); chk('Den Hartog pico',await T(pg,'oPk'),math.sqrt(1+2/0.1),0.03); print('   β, ζ2:',await pg.evaluate('()=>[__gdl.S.be,__gdl.S.z2]'),'esperado',1/1.1,math.sqrt(0.3/(8*1.1**3)))
        await setv(pg,'mu',0.25); await setv(pg,'be',0.8); await setv(pg,'m1',12.5); await setv(pg,'k1',7200)
        m1,k1,m2=12.5,7200,3.125; k2=m2*(0.8*math.sqrt(k1/m1))**2; w=np.sqrt(np.sort(np.linalg.eigvals(np.linalg.solve(np.diag([m1,m2]),np.array([[k1+k2,-k2],[-k2,k2]])))))
        chk('w1 (teclado)',await T(pg,"oW1"),float(w[0].real),0.001); chk('w2 (teclado)',await T(pg,"oW2"),float(w[1].real),0.001); print(pg._e)
        await b.close(); print('FALLAS:',fails)
asyncio.run(main())
