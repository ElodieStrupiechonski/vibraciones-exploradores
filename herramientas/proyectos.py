"""QA de las páginas proy_*.html: compara las funciones de cálculo expuestas (window.__se, __ri, __bo, __da)
con cálculos independientes en Python (NumPy/SciPy). Uso: python3 qa/proyectos.py CARPETA"""
import asyncio, math, os, sys, json
import numpy as np
from scipy import special, integrate, optimize
from scipy.linalg import eigh
from playwright.async_api import async_playwright
SITE=sys.argv[1]; G0=9.80665; TP=2*math.pi; MU0=4e-7*math.pi; fails=[]; nchk=0
def chk(name,a,b,tol=1e-6,ab=0):
    global nchk; nchk+=1
    if not (abs(a-b)<=tol*max(abs(a),abs(b))+ab): fails.append('%s: página %.8g, referencia %.8g'%(name,a,b))
AWG={20:0.8128,22:0.6438,24:0.5106,26:0.4049,28:0.3211,30:0.2548,32:0.2019,34:0.1601,36:0.1270}  # mm, tabla ASTM B258
def Brho_loop(a,rho,z,I=1.0):
    # Biot-Savart directo (cuadratura), sin integrales elípticas
    f=lambda ph: a*z*math.cos(ph)/(a*a+rho*rho+z*z-2*a*rho*math.cos(ph))**1.5
    return MU0*I/(4*math.pi)*integrate.quad(f,0,TP,limit=200)[0]
def M_neumann(a,b,d):
    f=lambda ph: math.cos(ph)/math.sqrt(a*a+b*b+d*d-2*a*b*math.cos(ph))
    return MU0*a*b/2*integrate.quad(f,0,TP,limit=200)[0]
def espiras(S):
    dcu=AWG[S['awg']]*1e-3; dex=1.1*dcu; lb=S['lb']*1e-3; tpl=max(1,int(lb/dex+1e-12)); esp=[]; n=0; j=0; L=0
    while n<S['N']:
        r=S['di']/2e3+(j+0.5)*dex; m=min(tpl,S['N']-n)
        for i in range(m): esp.append((r,(i+0.5)*lb/m))
        L+=m*TP*r; n+=m; j+=1
    return esp,L,dcu,j
def beam_fe(E,I,mu,L,Mp,ne=40):
    n=ne+1; K=np.zeros((2*n,2*n)); M=np.zeros((2*n,2*n)); l=L/ne
    ke=E*I/l**3*np.array([[12,6*l,-12,6*l],[6*l,4*l*l,-6*l,2*l*l],[-12,-6*l,12,-6*l],[6*l,2*l*l,-6*l,4*l*l]])
    me=mu*l/420*np.array([[156,22*l,54,-13*l],[22*l,4*l*l,13*l,-3*l*l],[54,13*l,156,-22*l],[-13*l,-3*l*l,-22*l,4*l*l]])
    for e in range(ne):
        s=slice(2*e,2*e+4); K[s,s]+=ke; M[s,s]+=me
    M[-2,-2]+=Mp
    lam=eigh(K[2:,2:],M[2:,2:],eigvals_only=True); return math.sqrt(lam[0])/TP
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        async def abre(f):
            pg=await b.new_page(viewport={'width':1280,'height':900}); pg.on('pageerror',lambda x:errs.append(f+': '+str(x)))
            await pg.goto('file://'+os.path.abspath(os.path.join(SITE,f+'.html'))); await pg.wait_for_timeout(400); return pg
        # ---------- bobina
        pg=await abre('proy_bobina')
        for k in (0.05,0.3,0.7,0.95,0.999):
            K,E=await pg.evaluate("k=>window.__bo.KE(k)",k); chk('K(%g)'%k,K,special.ellipk(k*k),1e-10); chk('E(%g)'%k,E,special.ellipe(k*k),1e-10)
        for a,bb,d in ((0.01,0.014,0.005),(0.012,0.012,0.002),(0.02,0.008,0.03),(0.011,0.014,0.0005)):
            m=await pg.evaluate("v=>window.__bo.mutua(v[0],v[1],v[2])",[a,bb,d]); chk('M(%g,%g,%g)'%(a,bb,d),m,M_neumann(a,bb,d),1e-6)
        casos=[dict(di=20,lb=10,awg=30,N=200,V=5,Il=1,dm=28,tm=5,Br=1.25,s=5,v=0.44),dict(di=30,lb=15,awg=26,N=500,V=12,Il=1,dm=28,tm=5,Br=1.25,s=3,v=0.1),
               dict(di=12,lb=20,awg=32,N=800,V=9,Il=0.5,dm=10,tm=10,Br=1.3,s=1,v=0.2),dict(di=40,lb=5,awg=24,N=60,V=3,Il=2,dm=20,tm=3,Br=1.1,s=12,v=1.0)]
        for S in casos:
            r=await pg.evaluate("S=>{Object.assign(window.__bo.S,S); const c=window.__bo.calc(); return {K:c.K,F:c.F,e:c.e,R:c.b.R,I:c.b.I,P:c.b.P,cap:c.b.cap,n:c.b.esp.length,largo:c.b.largo,Bc:c.b.Bc,mim:c.mim,km:c.km}}",S)
            esp,L,dcu,cap=espiras(S); R=1.72e-8*L/(math.pi*dcu**2/4); I=min(S['V']/R,S['Il'])
            chk('n espiras',r['n'],S['N']); chk('capas',r['cap'],cap); chk('largo',r['largo'],L,2e-3); chk('R',r['R'],R,4e-3); chk('I',r['I'],I,4e-3); chk('P',r['P'],I*I*R,4e-3)
            # fuerza por ampere: suma sobre espiras de 2 pi r B_rho del imán (corriente superficial equivalente integrada en z)
            am=S['dm']/2e3; tm=S['tm']*1e-3; lb=S['lb']*1e-3; s=S['s']*1e-3; Ks=S['Br']/MU0
            # agrupar espiras por capa para acelerar: integrar en z del imán con cuadratura de Gauss de 12 puntos
            xg,wg=np.polynomial.legendre.leggauss(12); K=0
            for (r0,z0) in esp:
                for x,w in zip(xg,wg):
                    zm=lb+s+(x+1)/2*tm; K+=w/2*tm*Ks*TP*r0*Brho_loop(am,r0,z0-zm)
            K=abs(K); chk('K(s) N/A',r['K'],K,1.5e-2); chk('F',r['F'],r['K']*r['I'],1e-9); chk('fem',r['e'],r['K']*S['v'],1e-9)
            chk('masa imán',r['mim'],7500*math.pi*am*am*tm,1e-9)
            Bc=sum(MU0*a*a/(2*(a*a+(z-lb/2)**2)**1.5) for a,z in esp)*I; chk('B centro',r['Bc'],Bc,4e-3)
            print('bobina N=%d: K=%.4f N/A (ref %.4f), R=%.2f ohm, F=%.3f N, fem=%.3f V'%(S['N'],r['K'],K,r['R'],r['F'],r['e']))
        await pg.close()
        # ---------- rigidez
        pg=await abre('proy_rigidez'); rng=np.random.default_rng(3)
        for k in (120.,426.,6000.):
            m=np.array([50,100,150,200,300.]); d=m*1e-3*G0/k*1e3*(1+0.01*rng.standard_normal(5)); t='\n'.join('%g, %.5f'%(a,c) for a,c in zip(m,d))
            r=await pg.evaluate("t=>{const r=window.__ri.estatica(t); return {k:r.k,uk:r.uk,r2:r.r2}}",t)
            x=m*1e-3*G0; y=np.array([float('%.5f'%v) for v in d])*1e-3; (s,a),cov=np.polyfit(x,y,1,cov='unscaled'); res=y-(a+s*x); se=math.sqrt(res@res/3*cov[0,0])
            chk('k estática',r['k'],1/s,1e-6); chk('u(k) estática',r['uk'],se/s**2,1e-5)
            me=0.3; f=np.sqrt(k/(me+m*1e-3))/TP*(1+0.003*rng.standard_normal(5)); t='\n'.join('%g, %.4f'%(a,c) for a,c in zip(m,f))
            r=await pg.evaluate("t=>{const r=window.__ri.dinamica(t); return {k:r.k,uk:r.uk,m:r.m}}",t)
            x=m*1e-3; y=1/np.array([float('%.4f'%v) for v in f])**2; (s,a),cov=np.polyfit(x,y,1,cov='unscaled'); res=y-(a+s*x); se=math.sqrt(res@res/3*cov[0,0])
            chk('k dinámica',r['k'],4*math.pi**2/s,1e-6); chk('m efectiva',r['m'],a/s,1e-6); chk('u(k) dinámica',r['uk'],4*math.pi**2*se/s**2,1e-5)
            if abs(r["k"]/k-1)>0.10: fails.append('k dinámica lejos del valor sembrado: %g vs %g'%(r['k'],k))
        for S in (dict(E=200,rho=7850,b=12.7,h=0.64,L=150,Mp=23),dict(E=69,rho=2700,b=25,h=2,L=250,Mp=0),dict(E=3,rho=1240,b=10,h=2,L=40,Mp=5),dict(E=200,rho=7850,b=12.7,h=0.64,L=100,Mp=200)):
            r=await pg.evaluate("S=>{Object.assign(window.__ri.S,S); return window.__ri.viga()}",S)
            bb,h,L,E=S['b']*1e-3,S['h']*1e-3,S['L']*1e-3,S['E']*1e9; I=bb*h**3/12; mu=S['rho']*bb*h
            chk('k viga',r['k'],3*E*I/L**3,1e-9); chk('deflexión',r['d'],S['Mp']*1e-3*G0*L**3/(3*E*I),1e-9,1e-15)
            chk('f0 sin masa (MEF)',r['f0'],beam_fe(E,I,mu,L,0),1e-4); chk('fn con masa (Rayleigh vs MEF)',r['fn'],beam_fe(E,I,mu,L,S['Mp']*1e-3),1.6e-2)
            print('viga L=%g mm, Mp=%g g: fn página %.3f Hz, MEF %.3f Hz'%(S['L'],S['Mp'],r['fn'],beam_fe(E,I,mu,L,S['Mp']*1e-3)))
        await pg.close()
        # ---------- sensores
        pg=await abre('proy_sensores')
        for S in (dict(f=6,X=0.5,z=0.05,T=20,fa=200,na=0.02,fm=50,fps=240,mt=190,me=300,mont=1),dict(f=140,X=0.02,z=0.01,T=5,fa=100,na=0.05,fm=100,fps=60,mt=200,me=50,mont=0),
                  dict(f=95,X=0.1,z=0.02,T=10,fa=100,na=0.02,fm=50,fps=30,mt=180,me=2000,mont=1),dict(f=420,X=0.005,z=0.004,T=8,fa=400,na=0.01,fm=100,fps=240,mt=170,me=40,mont=1)):
            r=await pg.evaluate("S=>{Object.assign(window.__se.S,S); return window.__se.calc()}",S)
            f=S['f']; w=TP*f; arms=w*w*S['X']*1e-3/math.sqrt(2); chk('a_rms',r['arms'],arms); chk('SNR',r['snr'],20*math.log10(arms/S['na']),1e-9)
            fc=f*math.sqrt(S['me']/(S['me']+S['mt'])) if S['mont'] else f; chk('f con carga',r['carga'],fc); chk('Δf',r['df'],1/S['T'])
            chk('t al 5 %',r['t5'],math.log(20)/(S['z']*TP*f)); chk('puntos en ancho de media potencia',r['ptsHP'],2*S['z']*f*S['T'])
            for s_ in r['sens']:
                fv=s_['fv']; fs=s_['fs']; ny=fs/2; chk(s_['n']+' Nyquist',s_['ny'],ny)
                if fv>=ny:
                    ref=min(abs(fv-k*fs) for k in range(0,200)); chk(s_['n']+' alias',s_['al'],ref,1e-9,1e-9)
                    # comprobación numérica: muestrear un seno y localizar el pico de la FFT
                    n=int(fs*40); x=np.sin(TP*fv*np.arange(n)/fs); X=np.abs(np.fft.rfft(x*np.hanning(n))); fp=np.argmax(X)*fs/n; chk(s_['n']+' alias FFT',s_['al'],fp,0,0.06)
                if s_['ok']!=(fv<=0.8*ny): fails.append('criterio ok '+s_['n'])
        await pg.close()
        # ---------- datos
        pg=await abre('proy_datos')
        Tr=lambda f,fn,z: np.sqrt((1+(2*z*f/fn)**2)/((1-(f/fn)**2)**2+(2*z*f/fn)**2))
        for fn0,z0 in ((6.0,0.06),(11.3,0.15),(4.2,0.02)):
            f=np.array([2,3,4,4.5,5,5.5,6,6.5,7,8,9,10,12,15,20,25,30.]); y=Tr(f,fn0,z0)*(1+0.03*rng.standard_normal(f.size)); P=[[float(a),float(c)] for a,c in zip(f,y)]
            r=await pg.evaluate("P=>window.__da.ajusteA(P)",P)
            o=optimize.least_squares(lambda q: np.log(Tr(f,q[0],q[1]))-np.log(y),[fn0*1.2,z0*2],bounds=([0.5,1e-4],[100,2]),xtol=1e-14,ftol=1e-14)
            chk('ajuste fn',r['fn'],o.x[0],2e-3); chk('ajuste ζ',r['z'],o.x[1],1.5e-2); chk('rms',r['rms'],math.sqrt(np.mean(o.fun**2)),2e-2)
            print('ajuste A: fn %.4f (ref %.4f, sembrado %g), ζ %.4f (ref %.4f, sembrado %g)'%(r['fn'],o.x[0],fn0,r['z'],o.x[1],z0))
        for fd0,z0 in ((7.0,0.004),(7.0,0.012),(6.9,0.03)):
            n=np.arange(14); t=0.012+n/fd0; d0=TP*z0/math.sqrt(1-z0*z0); a=10*np.exp(-d0*n)*(1+0.01*rng.standard_normal(14)); txt='\n'.join('%.4f, %.4f'%(u,v) for u,v in zip(t,a))
            r=await pg.evaluate("t=>{const r=window.__da.serieC(t); return {fd:r.fd,d:r.d,z:r.z,r2:r.r2,zse:r.zse}}",txt)
            tt=np.array([float('%.4f'%u) for u in t]); aa=np.array([float('%.4f'%v) for v in a]); s,c=np.polyfit(tt,np.log(aa),1); fd=13/(tt[-1]-tt[0]); d=-s/fd
            chk('fd',r['fd'],fd); chk('δ',r['d'],d,1e-8); chk('ζ',r['z'],d/math.sqrt(4*math.pi**2+d*d),1e-8)
            if abs(r['z']/z0-1)>0.08: fails.append('ζ de la serie lejos del sembrado: %g vs %g'%(r['z'],z0))
        # Basquin y Miner, leídos de la página
        S=dict(EB=3,hB=2,LB=40,fB=4,d1=6,n1=200,d2=5); dat=[(6,510),(6,310),(6,380),(5.5,820),(5.5,1450),(5.5,1010),(5,4980),(5,4790),(5,4240)]
        await pg.evaluate("v=>{Object.assign(window.__da.S,v[0]); document.getElementById('dB').value=v[1]; document.getElementById('dB').dispatchEvent(new Event('input',{bubbles:true}));}",[S,'\n'.join('%g, %g'%d for d in dat)])
        await pg.wait_for_timeout(300); txt=await pg.evaluate("()=>['ba','bb','br2','bN12','bn2','bt'].map(i=>document.getElementById(i).textContent)")
        sig=lambda d: 3*S['EB']*1e3*S['hB']*d/(2*S['LB']**2); x=np.log10([d[1] for d in dat]); y=np.log10([sig(d[0]) for d in dat]); bq,la=np.polyfit(x,y,1); a=10**la
        N=lambda d:(sig(d)/a)**(1/bq); n2=N(S['d2'])*(1-S['n1']/N(S['d1']))
        chk('Basquin a',float(txt[0].split()[0]),a,6e-3); chk('Basquin b',float(txt[1].replace('−','-')),bq,0,6e-4); chk('Miner n2',float(txt[4].split()[0]),n2,6e-3); chk('tiempo',float(txt[5].split()[0]),n2/S['fB']/60,6e-3)
        print('fatiga: a=%.4g MPa, b=%.4f, N1=%.4g, N2=%.4g, n2=%.4g | página:'%(a,bq,N(S['d1']),N(S['d2']),n2),txt)
        # esfuerzo de flexión en voladizo con desplazamiento impuesto: sigma = 3 E h d / (2 L^2)  (de d = P L^3/(3EI), sigma = P L (h/2)/I)
        E,h,L,d=3e9,2e-3,40e-3,6e-3; I=1*h**3/12; Pf=3*E*I*d/L**3; chk('σ voladizo',sig(6)*1e6,Pf*L*(h/2)/I,1e-12)
        await pg.close(); await b.close()
        for e in errs: fails.append('JS '+e)
asyncio.run(main())
print('%d comprobaciones'%nchk); print('TODO BIEN' if not fails else '\n'.join(['FALLAS:']+fails)); sys.exit(1 if fails else 0)
