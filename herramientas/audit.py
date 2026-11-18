import asyncio, glob, json, sys, os
from playwright.async_api import async_playwright
SITE=sys.argv[1]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); out={}
        for f in sorted(glob.glob(os.path.join(SITE,'*.html'))):
            pg=await b.new_page(viewport={'width':1280,'height':900}); errs=[]
            pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: errs.append(m.text) if m.type=='error' and 'net::' not in m.text and 'Failed to load resource' not in m.text else None)
            await pg.route('**/*', lambda r: r.continue_() if r.request.url.startswith('file:') else r.abort())
            await pg.goto('file://'+os.path.abspath(f)); await pg.wait_for_timeout(500)
            vals=await pg.evaluate("""()=>{const o={};document.querySelectorAll('[id]').forEach(e=>{if(e.children.length<=2 && !['SCRIPT','STYLE','CANVAS','DIV','DETAILS','NAV','A','BUTTON'].includes(e.tagName)||(e.classList.contains('v')||e.classList.contains('val'))){const t=(e.value!==undefined&&e.tagName=='INPUT')?e.value:e.textContent.trim(); if(t&&t.length<60)o[e.id]=t;}});return o}""")
            out[os.path.basename(f)]={'errors':errs,'vals':vals}; await pg.close()
        await b.close(); json.dump(out,open('qa/audit.json','w'),ensure_ascii=False,indent=1)
        for k,v in out.items(): print(k,'ERRORS:',v['errors'][:3],'n=',len(v['vals']))
asyncio.run(main())
