import asyncio, math, os, sys
from playwright.async_api import async_playwright
SITE=sys.argv[1]; fails=[]
def chk(name, got, exp, tol=0.006):
    g=float(str(got).replace('−','-').replace(',','').split()[0]); ok=abs(g-exp)<=tol*max(1,abs(exp))+0.051
    print(('ok  ' if ok else 'FAIL'), name, got, 'esperado', round(exp,4));
    if not ok: fails.append(name)
async def setv(pg, rid, v):
    el=pg.locator(f'#{rid} + input.kbnum'); await el.fill(str(v)); await el.press('Enter')
async def T(pg,i): return (await pg.locator('#'+i).text_content()).strip()
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        async def op(f):
            pg=await b.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.route('**/*', lambda r: r.continue_() if r.request.url.startswith('file:') else r.abort())
            await pg.goto('file://'+os.path.abspath(os.path.join(SITE,f))); await pg.wait_for_timeout(400); pg._errs=errs; return pg
        # media potencia
        pg=await op('mediapotencia_interactivo.html'); z,fn=0.073,33.3
        await setv(pg,'sz',z); await setv(pg,'sf',fn)
        Mm=1/(2*z*math.sqrt(1-z*z)); r1=math.sqrt(1-2*z*z-2*z*math.sqrt(1-z*z)); r2=math.sqrt(1-2*z*z+2*z*math.sqrt(1-z*z))
        chk('mp Q',await T(pg,'oQ'),1/(2*z)); chk('mp Mmax',await T(pg,'oM'),Mm); chk('mp df',await T(pg,'oB'),(r2-r1)*fn); chk('mp zmed',await T(pg,'oZ'),(r2-r1)/2); chk('mp fpico',await T(pg,'oFp'),fn*math.sqrt(1-2*z*z))
        f=(await T(pg,'oF')).split('·'); chk('mp f1',f[0],r1*fn); chk('mp f2',f[1],r2*fn); print(pg._errs)
        # Mohr
        pg=await op('mohr_interactivo.html'); sx,sy,t=62.5,-17.3,41.2
        await setv(pg,'sx',sx); await setv(pg,'sy',sy); await setv(pg,'txy',t); await setv(pg,'sylim',250)
        c=(sx+sy)/2; R=math.hypot((sx-sy)/2,t); s1,s2=c+R,c-R; vm=math.sqrt(s1*s1-s1*s2+s2*s2)
        chk('mohr centro',await T(pg,'oSp'),c); chk('mohr R',await T(pg,'oR'),R); chk('mohr s1',await T(pg,'oS1'),s1); chk('mohr s2',await T(pg,'oS2'),s2)
        chk('mohr thp',(await T(pg,'oThp')).replace('°',''),math.degrees(0.5*math.atan2(2*t,sx-sy))); chk('mohr vM',await T(pg,'oVM'),vm); chk('mohr n vM',await T(pg,'oNvm'),250/vm); chk('mohr n Tresca',await T(pg,'oNtr'),250/max(abs(s1-s2),abs(s1),abs(s2)))
        await setv(pg,'th',33.3); th=math.radians(33.3)
        chk('mohr sx′',await T(pg,'oSxp'),c+(sx-sy)/2*math.cos(2*th)+t*math.sin(2*th)); chk('mohr txy′',await T(pg,'oTxp'),-(sx-sy)/2*math.sin(2*th)+t*math.cos(2*th))
        ea,eb,ec,E,nu=612.5,-233,87.5,71.7,0.31
        for i,v in zip(['ea','eb','ec','Eg','nu'],[ea,eb,ec,E,nu]): await setv(pg,i,v)
        g=2*eb-ea-ec; Sx=E*1e3*(ea+nu*ec)/(1-nu*nu)*1e-6; Sy=E*1e3*(ec+nu*ea)/(1-nu*nu)*1e-6; Txy=E*1e3/(2*(1+nu))*g*1e-6
        chk('roseta gxy',await T(pg,'oGxy'),g); r=(await T(pg,'oRos')).split('·'); chk('roseta sx',r[0],Sx); chk('roseta sy',r[1],Sy); chk('roseta txy',r[2],Txy)
        cc=(Sx+Sy)/2; RR=math.hypot((Sx-Sy)/2,Txy); r=(await T(pg,'oRos12')).split('·'); chk('roseta s1',r[0],cc+RR); chk('roseta s2',r[1],cc-RR); print(pg._errs)
        # fatiga (aluminio 6061-T6: Sut 310, Sf 96 a 5e8)
        pg=await op('fatiga_interactivo.html'); sm,sa,kf=55.5,72.3,1.35
        await setv(pg,'sm',sm); await setv(pg,'sa',sa); await setv(pg,'kf',kf)
        sar=kf*sa/(1-sm/310); b_=math.log10(0.9*310/96)/math.log10(1e3/5e8); a_=0.9*310/1e3**b_
        chk('fat sae',await T(pg,'oSae'),kf*sa); chk('fat sar',await T(pg,'oSar'),sar); chk('fat n',await T(pg,'oNg'),1/(kf*sa/96+sm/310))
        N=(sar/a_)**(1/b_); n=await T(pg,'oN'); print('    N explorador:',n,'| independiente: %.3e'%N)
        await setv(pg,'s1s',31.5); await setv(pg,'fn',137); await setv(pg,'tm',12.5); chk('fat Nt',(await T(pg,'oNt')).replace(',','').replace(' ','').replace(' ',''),137*60*12.5)
        D=sum(fr*137*750/((k*31.5/(1-sm/310)/a_)**(1/b_)) for k,fr in ((1,.683),(2,.271),(3,.043))); print('    D explorador:',await T(pg,'oD'),'| independiente (σm del estado, Kf=1): %.3e'%D, '| vida', await T(pg,'oVida')); print(pg._errs)
        # sonido
        pg=await op('sonido_interactivo.html'); L=[70.5,77.5,83,86.5,81,79,73.5,66]; A=[-26.2,-16.1,-8.6,-3.2,0,1.2,1.0,-1.1]
        inp=pg.locator('input[type=range][data-i]')
        for i,v in enumerate(L):
            el=inp.nth(i).locator('xpath=following-sibling::input[1]'); await el.fill(str(v)); await el.press('Enter')
        await setv(pg,'r',3.5); await setv(pg,'nf',3)
        tot=10*math.log10(sum(10**(x/10) for x in L)); totA=10*math.log10(sum(10**((x+a)/10) for x,a in zip(L,A))); d=-20*math.log10(3.5)+10*math.log10(3)
        chk('son L',await T(pg,'oL'),tot+d,0.002); chk('son LA',await T(pg,'oLA'),totA+d,0.002); print('    T:',await T(pg,'oT'),'| independiente: %.2f h'%(8*2**((90-(totA+d))/3))); print(pg._errs)
        # espectro (deslizador logarítmico de fn)
        pg=await op('espectro_interactivo.html'); await setv(pg,'sfn',237); await setv(pg,'sz',0.033); await setv(pg,'sw0',0.12)
        chk('esp fn',(await T(pg,'vfn')).replace('Hz',''),237); chk('esp Q',await T(pg,'oQ'),1/0.066); chk('esp Miles',(await T(pg,'oGm')).replace('g',''),math.sqrt(math.pi/2*237/0.066*0.12)); chk('esp W(fn)',await T(pg,'oWfn'),0.12)
        print('    Gin',await T(pg,'oGin'),'Gn',await T(pg,'oGn'),'3σ',await T(pg,'oG3')); print(pg._errs)
        await b.close(); print('FALLAS:',fails)
asyncio.run(main())
