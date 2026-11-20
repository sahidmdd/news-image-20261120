import asyncio, pathlib, json
from playwright.async_api import async_playwright
HERE=pathlib.Path(__file__).resolve().parent
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=["--no-sandbox"])
        pg=await b.new_page(viewport={"width":1024,"height":1024})
        await pg.goto((HERE/"poster.html").as_uri()); await pg.wait_for_timeout(300)
        r=await pg.evaluate("""()=>{
          const out={docH:document.documentElement.scrollHeight,docW:document.documentElement.scrollWidth,over:[],crowd:[]};
          for(const el of document.querySelectorAll('h1,h2,h3,p,.kicker,.ticker span,.date,.brand')){
            const b=el.getBoundingClientRect();
            if(b.right>1024.5||b.bottom>1024.5||b.left<-0.5||b.top<-0.5)
              out.over.push({t:el.textContent.slice(0,28),l:Math.round(b.left),t2:Math.round(b.top),r:Math.round(b.right),b2:Math.round(b.bottom)});
            if(el.scrollWidth>el.clientWidth+1) out.crowd.push({t:el.textContent.slice(0,24),sw:el.scrollWidth,cw:el.clientWidth});
          }
          return out;}""")
        print(json.dumps(r,indent=1))
        await b.close()
asyncio.run(main())
