"""QA de la revisión 1.2: cálculo independiente (Python/NumPy/SciPy) de las cuatro páginas nuevas, entrada por teclado,
navegación lateral, desbordamiento en móvil y ligas locales. Uso: python3 qa/rev12.py CARPETA"""
import asyncio, math, os, sys, json, re
import numpy as np
from scipy import signal
from playwright.async_api import async_playwright
SITE=sys.argv[1]; fails=[]
def chk(n,got,exp,tol=0.005):
    g=float(re.sub(r'[^0-9eE.+\-]','',str(got).replace('−','-').split()[0])) if not isinstance(got,(int,float)) else got
    ok=abs(g-exp)<=tol*max(abs(exp),1e-12)+1e-12; print('ok  ' if ok else 'FAIL',n,got,'esperado',f'{exp:.6g}')
    if not ok: fails.append(n)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        async def op(f,w=1280):
            pg=await b.new_page(viewport={'width':w,'height':900}); pg._e=[]; pg.on('pageerror',lambda e:pg._e.append(str(e)))
            await pg.route('**/*', lambda r: r.continue_() if r.request.url.startswith('file:') else r.abort())
            await pg.goto('file://'+os.path.abspath(os.path.join(SITE,f))); await pg.wait_for_timeout(400); return pg
        T=lambda pg,i: pg.locator('#'+i).text_content()
        async def setv(pg,rid,v):
            el=pg.locator(f'#{rid} + input.kbnum'); await el.fill(str(v)); await el.press('Enter')
        # ---------------- transmisibilidad
        print('== transmisibilidad'); pg=await op('transmisibilidad_interactivo.html')
        Tr=lambda r,z: math.sqrt((1+(2*z*r)**2)/((1-r*r)**2+(2*z*r)**2))
        for (m,k,z,f,Y) in [(0.3,426,0.05,15,1),(2.5,12000,0.12,7.3,2.4),(12,800,0.6,40,0.7)]:
            for i,v in zip('mkzfY',(m,k,z,f,Y)): await setv(pg,i,v)
            wn=math.sqrt(k/m); fn=wn/2/math.pi; r=f/fn; t=Tr(r,z)
            chk('fn',await T(pg,'ofn'),fn); chk('dst mm',await T(pg,'odst'),9.80665/wn**2*1e3); chk('Tr',await T(pg,'oT'),t); chk('dB',await T(pg,'odB'),20*math.log10(t),0.01)
            chk('X m',await pg.evaluate('()=>__tr.calc().X'),t*Y*1e-3,1e-9); chk('fase',(await T(pg,'ofase')).replace('°',''),math.degrees(math.atan2(2*z*r**3,1-r*r+(2*z*r)**2)),0.01)
            # máximo por búsqueda numérica
            rr=np.linspace(0.2,3,400001); tt=np.sqrt((1+(2*z*rr)**2)/((1-rr**2)**2+(2*z*rr)**2)); chk('Tmax',await T(pg,'opk'),tt.max(),0.005)
            q=await pg.evaluate('()=>{const q=__tr.calc();return [q.rq,q.fnq,q.FT,q.acc]}'); chk('Tr(r_req)=1-R',Tr(q[0],z),0.2,1e-6); chk('acc',q[3],(2*math.pi*f)**2*t*Y*1e-3,1e-9)
        await pg.click('[data-modo=desb]'); 
        for i,v in zip(['m','k','z','f','m0','e'],(0.3,426,0.05,30,5,10)): await setv(pg,i,v)
        wn=math.sqrt(426/0.3); w=2*math.pi*30; r=w/wn; F0=5e-3*10e-3*w*w; D=math.sqrt((1-r*r)**2+(0.1*r)**2)
        q=await pg.evaluate('()=>{const q=__tr.calc();return [q.F0,q.X,q.FT]}'); chk('F0 desb',q[0],F0,1e-9); chk('X desb',q[1],5e-3*10e-3/0.3*r*r/D,1e-9); chk('FT desb',q[2],Tr(r,0.05)*F0,1e-9)
        # integración temporal independiente: base móvil, amplitud estacionaria
        m,k,z,f=0.3,426,0.05,15.; c=2*z*math.sqrt(k*m); w=2*math.pi*f
        sys1=signal.lti([c,k],[m,c,k]); tt=np.linspace(0,12,240001); _,y,_=signal.lsim(sys1,np.sin(w*tt),tt); chk('Tr por integración temporal',np.abs(y[-20000:]).max(),Tr(f/(math.sqrt(k/m)/2/math.pi),z),0.002)
        if pg._e: fails.append('js trans'); print(pg._e)
        # ---------------- analogías
        print('== analogías'); pg=await op('analogias_interactivo.html')
        for (m,c,k,la,an) in [(1,2,100,0,'serie'),(3.5,12.5,2400,2.3,'serie'),(0.4,30,150,-1.2,'par'),(2,40,200,1,'par')]:
            await pg.click(f'[data-an={an}]')
            for i,v in zip(['m','c','k','la'],(m,c,k,la)): await setv(pg,i,v)
            q=await pg.evaluate('()=>__an.calc()'); a=10**la; wn=math.sqrt(k/m); z=c/(2*math.sqrt(k*m))
            L,R,C=(a*m,a*c,1/(a*k)) if an=='serie' else (a/k,a/c,m/a)
            chk('L',q['L'],L,1e-9); chk('R',q['R'],R,1e-9); chk('C',q['C'],C,1e-9); chk('wn elec',q['we'],1/math.sqrt(L*C),1e-9); chk('wn mec',q['wn'],wn,1e-9)
            chk('z elec',q['ze'],(R/2*math.sqrt(C/L)) if an=='serie' else (1/(2*R)*math.sqrt(L/C)),1e-9); chk('z mec',q['z'],z,1e-9)
            # respuesta al escalón frente a SciPy
            tt=np.linspace(0,3,301); _,y=signal.step(signal.lti([wn*wn],[1,2*z*wn,wn*wn]),T=tt); js=await pg.evaluate('([wn,z])=>Array.from({length:301},(_,i)=>__an.escalon(i*0.01,wn,z))',[wn,z]); chk('escalón máx. error',float(np.abs(np.array(js)-y).max())+1,1,2e-4)
            if z<1: chk('sobrepaso %',await T(pg,'osp'),100*math.exp(-math.pi*z/math.sqrt(1-z*z)),0.002)
        if pg._e: fails.append('js an'); print(pg._e)
        # ---------------- modal
        print('== modal'); pg=await op('modal_interactivo.html')
        await pg.click('[data-pre=U]'); await setv(pg,'ns',0)
        r=await pg.evaluate('()=>{const e=__mod.res();return {P:[e.P.fn,e.P.z],C:[e.C.fn,e.C.z,e.C.A,e.C.R],I:[e.I.fn,e.I.z,e.I.A],f:Array.from(e.f),re:Array.from(e.re),im:Array.from(e.im)}}')
        chk('1 modo, sin ruido: pico fn',r['P'][0],20*math.sqrt(1-2*0.02**2),0.001); chk('media potencia ζ',r['P'][1],0.02,0.03); chk('círculo fn',r['C'][0],20,0.001); chk('círculo ζ',r['C'][1],0.02,0.01); chk('círculo A',r['C'][2],1,0.01)
        chk('inversa fn',r['I'][0],20,1e-6); chk('inversa ζ',r['I'][1],0.02,1e-6); chk('inversa A',r['I'][2],1,1e-6)
        chk('diámetro = A/(2ζω²)',2*r['C'][3],1/(2*0.02*(2*math.pi*20)**2),0.01)
        # FRF de la página frente a NumPy, y los tres métodos reimplementados
        await pg.click('[data-pre=S]'); await setv(pg,'ns',0)
        r=await pg.evaluate('()=>{const e=__mod.res();return {P:[e.P.fn,e.P.z],C:[e.C.fn,e.C.z],I:[e.I.fn,e.I.z],f:Array.from(e.f),re:Array.from(e.re),im:Array.from(e.im)}}')
        f=np.array(r['f']); w=2*np.pi*f; H=sum(A/((2*np.pi*fr)**2-w**2+2j*zz*2*np.pi*fr*w) for fr,zz,A in [(20,.02,1),(60,.01,1)])
        chk('FRF máx. error relativo',float(np.abs(np.array(r['re'])+1j*np.array(r['im'])-H).max()/np.abs(H).max())+1,1,1e-9)
        g=1/H; pr=np.polyfit(w**2,g.real,1); pi_=np.polyfit(w,g.imag,1); A=-1/pr[0]; wr=math.sqrt(pr[1]*A); chk('inversa fn (NumPy)',r['I'][0],wr/2/math.pi,1e-6); chk('inversa ζ (NumPy, recta por el origen)',r['I'][1],float(np.sum(w*g.imag)/np.sum(w*w))*A/(2*wr),1e-6)
        x,y=H.real,H.imag; s=np.linalg.lstsq(np.c_[x,y,np.ones_like(x)],x*x+y*y,rcond=None)[0]; xc,yc=s[0]/2,s[1]/2; th=np.arctan2(x-xc,-(y-yc)); ok=np.abs(th)<2.2; pp=np.polyfit(w[ok]**2,np.tan(th[ok]/2),1); wr2=-pp[1]/pp[0]
        chk('círculo fn (NumPy)',r['C'][0],math.sqrt(wr2)/2/math.pi,1e-6); chk('círculo ζ (NumPy)',r['C'][1],-1/(2*wr2*pp[0]),1e-6)
        print('   modos separados: ζ círculo %.4f, ζ inversa %.4f (sesgo %+.0f %%)'%(r['C'][1],r['I'][1],100*(r['I'][1]/0.02-1)))
        chk('Δf',await T(pg,'odf'),0.1); chk('puntos en el ancho',await T(pg,'onb'),8.0)
        await pg.click('[data-pre=R]'); chk('resolución insuficiente: puntos',await T(pg,'onb'),1.6); print('   aviso:',await T(pg,'aviso'))
        if pg._e: fails.append('js modal'); print(pg._e)
        # ---------------- tutorial
        print('== tutorial'); pg=await op('tutorial_phyphox.html')
        d=np.loadtxt(os.path.join(SITE,'segueta_10cm.csv'),delimiter=',',skiprows=1); t=d[:,0]; a=d[:,3]; fs=(len(t)-1)/(t[-1]-t[0])
        chk('fs',await T(pg,'ofs'),fs,0.001)
        # tratamiento independiente (el del cuaderno: Butterworth + Hilbert de SciPy)
        x=a-a.mean(); n0=np.argmax(np.abs(x)); seg=x[n0:]; X=np.abs(np.fft.rfft(seg*(0.5+0.5*np.cos(np.pi*np.arange(len(seg))/len(seg))),8*len(seg))); ff=np.fft.rfftfreq(8*len(seg),1/fs); fp=ff[np.argmax(np.where(ff>2,X,0))]
        chk('f pico (NumPy)',await T(pg,'ofp'),fp,0.005)
        sos=signal.butter(4,[0.8*fp,1.2*fp],btype='band',fs=fs,output='sos'); xf=signal.sosfiltfilt(sos,x); env=np.abs(signal.hilbert(xf)); i0=n0+round(0.05*fs); i1=i0+np.argmax(env[i0:]<0.25*env[i0])
        m_,b_=np.polyfit(np.arange(i1-i0)/fs,np.log(env[i0:i1]),1); zpy=-m_/(2*math.pi*fp); print('   ζ envolvente SciPy (Butterworth): %.4f'%zpy); chk('ζ envolvente',await T(pg,'oze'),zpy,0.12)
        # señal sintética: recuperación de valores conocidos
        await pg.select_option('#origen','sint')
        for (fn,ze,fs_,ru) in [(40,0.004,200,2),(25,0.01,150,1),(60,0.002,400,5)]:
            for i,v in zip(['fn','ze','fs','ru'],(fn,ze,fs_,ru)): await setv(pg,i,v)
            chk(f'sintética fn={fn}',await T(pg,'ofp'),fn*math.sqrt(1-ze*ze),0.003); chk(' ζ envolvente',await T(pg,'oze'),ze,0.06); chk(' ζ decremento',await T(pg,'ozd'),ze,0.06)
        for i,v in zip(['fn','ze','fs','ru'],(150,0.004,200,2)): await setv(pg,i,v)
        chk('alias de 150 Hz con fs = 200',await T(pg,'ofp'),50,0.005); print('   aviso:',(await T(pg,'aviso'))[:110])
        # CSV propio
        await pg.select_option('#origen','csv'); await pg.set_input_files('#csv',os.path.join(SITE,'segueta_10cm.csv')); await pg.wait_for_timeout(500); print('  ',await T(pg,'csvinfo')); chk('CSV: f pico',await T(pg,'ofp'),fp,0.005)
        # avance y pestañas
        await pg.check('input[data-paso="1"]'); wdt=await pg.evaluate("()=>document.getElementById('barra').style.width"); print('   barra de avance:',wdt); await pg.click('#tabV'); assert await pg.locator('#panV').is_visible() and not await pg.locator('#panC').is_visible()
        hrefs=await pg.evaluate("()=>[...document.querySelectorAll('.paso a[href]')].map(a=>a.getAttribute('href'))"); print('   ligas:',len(hrefs)); [print('     ',h) for h in sorted(set(hrefs)) if h.startswith('http')]
        if pg._e: fails.append('js tut'); print(pg._e)
        # ---------------- choque
        print('== choque'); pg=await op('choque_interactivo.html')
        def srs_ref(forma,D,fn,Q):
            z=1/(2*Q); w=2*np.pi*fn; Tn=1/fn; tt=np.linspace(0,D+4*Tn,int(max(4000,(D+4*Tn)/min(D/400,Tn/200)))+1); u=tt/D
            a=np.where(u<=1,{'sen':np.sin(np.pi*u),'sie':u,'rec':np.ones_like(u)}[forma],0.0)
            import warnings; warnings.simplefilter('ignore')
            _,y,_=signal.lsim(signal.lti([2*z*w,w*w],[1,2*z*w,w*w]),a,tt); return float(np.abs(y).max())
        for forma in ('sen','sie','rec'):
            await pg.click(f'[data-p={forma}]')
            for (A,D,fn,Q) in [(20,11,73,10),(20,11,5,10),(35,4.5,410,25),(8,30,12,4)]:
                for i,v in zip(['A','D','fn','Q'],(A,D,fn,Q)): await setv(pg,i,v)
                q=await pg.evaluate('()=>{const q=__ch.calc();return [q.pk,q.dv,q.zmax,q.smax]}'); ref=srs_ref(forma,D*1e-3,fn,Q)
                chk(f'{forma} A={A} D={D} fn={fn} Q={Q}: pico',q[0],A*ref,0.004); chk(' Δv',q[1],{'sen':2/math.pi,'sie':0.5,'rec':1}[forma]*A*9.80665*D*1e-3,1e-9)
            js=await pg.evaluate('()=>__ch.calc().sr'); FR=await pg.evaluate('()=>__ch.FR'); k=[5,25,40,55,70]; chk(f'{forma}: SRS en 5 frecuencias (máx. error rel.)',1+max(abs(js[i]/srs_ref(forma,30e-3,FR[i],4)-1) for i in k),1,0.006)
        await pg.click('[data-pre=C]'); print('   clásico:',await T(pg,'opk'),await T(pg,'oam'),'| máx:',await T(pg,'osm'),await T(pg,'ofm'))
        await pg.click('[data-pre=B]'); print('   blando:',await T(pg,'opk'),'asíntota',round(2*math.pi*5*2/math.pi*20*0.011,2)); await pg.click('[data-pre=R]'); print('   rígido:',await T(pg,'opk'))
        await pg.click('[data-p=sie]'); print('   sierra máx:',await T(pg,'osm')); await pg.click('[data-p=rec]'); print('   rectangular máx:',await T(pg,'osm'))
        if pg._e: fails.append('js choque'); print(pg._e)
        # ---------------- esfuerzos directos
        print('== esfuerzos'); pg=await op('esfuerzos_interactivo.html')
        for (P,d,n,sb,t,w,e,sy,ns) in [(5,6,1,640,3,30,12,345,1),(8,4,1,640,6,40,12,345,1),(20,8,2,640,3,28,20,345,2),(6,6,1,640,3,40,5,345,2),(33.5,9.5,2,900,4.2,61,22.5,480,1)]:
            await pg.click(f'[data-ns="{ns}"]')
            for i,v in zip(['P','d','n','sb','t','w','e','sy'],(P,d,n,sb,t,w,e,sy)): await setv(pg,i,v)
            F=P*1e3; tau=F/(n*ns*math.pi*d*d/4); ap=F/(n*d*t); net=F/((w-n*d)*t); des=F/(n*2*t*(e-d/2)); k3=1/math.sqrt(3)
            us=[tau/(k3*sb),ap/min(sy,sb),net/sy,des/(k3*sy)]; fs=1/max(us)
            chk('τ perno',await T(pg,'otau'),tau); chk('aplast.',await T(pg,'oap'),ap); chk('neta',await T(pg,'onet'),net); chk('desgarre',await T(pg,'odes'),des); chk('bruta',await T(pg,'obr'),F/(w*t))
            chk('FS',await T(pg,'ofs'),fs,0.006); chk('Pmáx',await T(pg,'opm'),fs*P)
            mod=await T(pg,'omod'); esp=['perno','aplastamiento','sección neta','desgarre'][us.index(max(us))]; print('    modo:',mod)
            if mod!=esp: fails.append('modo esfuerzos')
        if pg._e: fails.append('js esfuerzos'); print(pg._e)
        # ---------------- pérdida por transmisión
        print('== pérdida por transmisión'); pg=await op('perdida_interactivo.html')
        from scipy import integrate
        def tl_ref(E,rho,h,eta,nu,f,th=None):
            h=h*1e-3; m=rho*h; B=E*1e9*h**3/(12*(1-nu*nu)); c=343.0; z0=1.204*c; fc=c*c/(2*math.pi)*math.sqrt(m/B); w=2*math.pi*f
            def tau(theta):
                Z=1j*w*m*(1-(f/fc)**2*math.sin(theta)**4*(1+1j*eta)); return 1/abs(1+Z*math.cos(theta)/(2*z0))**2
            if th is not None: return -10*math.log10(tau(math.radians(th))), fc, m
            tl=math.radians(78); thc=math.asin(math.sqrt(fc/f)) if f>fc else None
            pts=[thc] if (thc and thc<tl) else None
            num=integrate.quad(lambda x: tau(x)*math.sin(2*x),0,tl,points=pts,limit=400,epsabs=0,epsrel=1e-9)[0]; return -10*math.log10(num/math.sin(tl)**2), fc, m
        for mat,(E,rho,nu) in {'al':(70,2700,0.33),'ac':(200,7850,0.30),'vi':(70,2500,0.22),'co':(30,2300,0.20)}.items():
            await pg.click(f'[data-mat={mat}]')
            for (h,eta,f,th) in [(2,0.01,1000,60),(6,0.02,2000,35),(100,0.02,500,70),(1,0.005,9000,80),(12,0.1,4000,50)]:
                for i,v in zip(['E','rho','h','eta','f','th'],(E,rho,h,eta,f,th)): await setv(pg,i,v)
                rd,fc,m=tl_ref(E,rho,h,eta,nu,f); ro,_,_=tl_ref(E,rho,h,eta,nu,f,th); q=await pg.evaluate('()=>{const q=__tl.calc();return [q.tld,q.tlo,q.tln,q.p.fc,q.p.m,q.dup]}')
                r2,_,_=tl_ref(E,rho,2*h,eta,nu,f)
                chk(f'{mat} h={h} η={eta} f={f}: TL difuso',q[0],rd,0.004); chk(' TL θ',q[1],ro,1e-6); chk(' ley de masa',q[2],10*math.log10(1+(math.pi*f*m/(1.204*343))**2),1e-9); chk(' fc',q[3],fc,1e-9); chk(' duplicar',q[5]+100,r2-rd+100,0.001)
        for pre in 'FVM': await pg.click(f'[data-pre={pre}]'); print('   preajuste',pre,'m″',await T(pg,'om'),'fc',await T(pg,'ofc'),'TL',await T(pg,'otl'),'duplicar',await T(pg,'odup'))
        await pg.click('[data-pre=M]'); a=float((await T(pg,'otl')).split()[0]); await pg.click('[data-pre=A]'); b_=float((await T(pg,'otl')).split()[0]); print('   capa amortiguadora sobre el muro a 500 Hz: +%.1f dB'%(b_-a))
        if pg._e: fails.append('js perdida'); print(pg._e)
        # ---------------- cámara anecoica
        print('== anecoica'); pg=await op('anecoica_interactivo.html')
        for (LW,r,Lx,Ly,Lz,al,dc,f,Q) in [(100,2,8,6,3,0.15,0.85,250,1),(100,2,6,5,4,0.02,0.85,250,1),(100,2,6,5,4,0.99,0.85,250,2),(123,7.3,21.5,12,9.5,0.37,0.3,60,8),(88,0.4,4,3.5,2.5,0.9,1.2,45,4)]:
            await pg.click(f'[data-q="{Q}"]')
            for i,v in zip(['LW','r','Lx','Ly','Lz','al','dc','f'],(LW,r,Lx,Ly,Lz,al,dc,f)): await setv(pg,i,v)
            Sup=2*(Lx*Ly+Lx*Lz+Ly*Lz); V=Lx*Ly*Lz; R=Sup*al/(1-al); rc=math.sqrt(Q*R/(16*math.pi)); Ld=LW+10*math.log10(Q/(4*math.pi*r*r)); Lr=LW+10*math.log10(4/R); Lp=10*math.log10(10**(Ld/10)+10**(Lr/10))
            chk(f'ᾱ={al} Q={Q}: Lp',await T(pg,'olp'),Lp,0.001); chk(' directo',await T(pg,'old'),Ld,0.001); chk(' reverb.',await T(pg,'olr'),Lr,0.001); chk(' desviación',float((await T(pg,'odev')).replace('+','').split()[0])+50,Lp-Ld+50,0.0012)
            chk(' rc',await T(pg,'orc'),rc); chk(' r1.5',await T(pg,'or15'),rc*math.sqrt(10**0.15-1)); chk(' R',await T(pg,'oR'),R); chk(' T60',await T(pg,'oT'),0.161*V/(-Sup*math.log(1-al)),0.03); chk(' f corte',await T(pg,'ofc'),343/(4*dc))
        for pre in 'ARNS': await pg.click(f'[data-pre={pre}]'); print('   preajuste',pre,'Lp',await T(pg,'olp'),'desv.',await T(pg,'odev'),'rc',await T(pg,'orc'),'T',await T(pg,'oT'))
        await pg.click('[data-pre=N]'); await setv(pg,'f',50); print('   aviso:',(await T(pg,'olect'))[-150:])
        if pg._e: fails.append('js anecoica'); print(pg._e)
        # ---------------- navegación y sitio
        print('== navegación'); TJ=json.load(open(os.path.join(SITE,'temario.json'),encoding='utf-8')); rec=TJ['recorrido']
        for i,f in enumerate(rec):
            pg=await op(f); o=await pg.evaluate("()=>[...document.querySelectorAll('#nv-lista a[data-nv]')].map(a=>a.dataset.nv)"); assert o==rec,(f,o)
            ant=await pg.get_attribute('#nv-ant','href'); sig=await pg.get_attribute('#nv-sig','href')
            if (i>0 and ant!=rec[i-1]) or (i<len(rec)-1 and sig!=rec[i+1]): fails.append('nav '+f)
            cur=await pg.locator('#nv-lista a.nv-aqui').count(); 
            if cur!=1: fails.append('aqui '+f)
            if pg._e: fails.append('js '+f); print(f,pg._e)
            await pg.close()
        print('   orden y anterior/siguiente correctos en',len(rec),'páginas')
        pg=await op('index.html'); await pg.keyboard.press('/'); await pg.keyboard.type('modal'); vis=await pg.evaluate("()=>[...document.querySelectorAll('#nv-lista a[data-nv]')].filter(a=>a.style.display!=='none').map(a=>a.dataset.nv)"); print('   búsqueda «modal»:',vis)
        if vis[:1]!=['modal_interactivo.html']: fails.append('busca')
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(400); print('   Enter ->',pg.url.split('/')[-1]); await pg.keyboard.press('ArrowLeft'); await pg.wait_for_timeout(400); print('   ← ->',pg.url.split('/')[-1])
        # ligas locales y desbordamiento a 390 px
        htmls=sorted(f for f in os.listdir(SITE) if f.endswith('.html'))
        for f in htmls:
            pg=await op(f,390); ov=await pg.evaluate("()=>document.documentElement.scrollWidth-document.documentElement.clientWidth")
            hs=await pg.evaluate("()=>[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href'))")
            falt=[h for h in set(hs) if not h.startswith(('http','#','mailto')) and not os.path.exists(os.path.join(SITE,h.split('#')[0]))]
            btn=await pg.locator('#nv-abre').is_visible()
            if ov>1 or falt or not btn or pg._e: fails.append('movil/ligas '+f); print('FAIL',f,'desborde',ov,'faltan',falt,'botón',btn,pg._e)
            await pg.close()
        print('   390 px: sin desbordamiento horizontal ni ligas locales rotas en',len(htmls),'páginas')
        await b.close()
    print('\nRESULTADO:', 'TODO CORRECTO' if not fails else 'FALLAS: '+', '.join(fails))
asyncio.run(main())
