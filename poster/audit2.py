import asyncio,pathlib,json
from playwright.async_api import async_playwright
HERE=pathlib.Path(__file__).resolve().parent
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=["--no-sandbox"]); pg=await b.new_page(viewport={"width":1024,"height":1024})
        await pg.goto((HERE/"poster.html").as_uri()); await pg.wait_for_timeout(200)
        r=await pg.evaluate("""()=>[...document.querySelectorAll('.lead,.row3,.ticker,.mast,.lead>.panel,.row3 .panel')]
          .map(e=>{const b=e.getBoundingClientRect();return {c:e.className,t:Math.round(b.top),h:Math.round(b.height),w:Math.round(b.width),b:Math.round(b.bottom)}})""")
        print(json.dumps(r))
        await b.close()
asyncio.run(main())
