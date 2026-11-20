import asyncio, sys, pathlib
from playwright.async_api import async_playwright
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent


async def shoot(src: pathlib.Path, out: pathlib.Path):
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--no-sandbox", "--font-render-hinting=none"])
        pg = await b.new_page(viewport={"width": 1024, "height": 1024}, device_scale_factor=2)
        await pg.goto(src.as_uri())
        await pg.wait_for_timeout(400)
        await pg.screenshot(path=str(out.with_suffix(".2x.png")), clip={"x": 0, "y": 0, "width": 1024, "height": 1024})
        await b.close()
    im = Image.open(out.with_suffix(".2x.png")).convert("RGB")
    im = im.resize((1024, 1024), Image.LANCZOS)
    im.save(out, "PNG", optimize=True)
    print(out, out.stat().st_size, im.size)


if __name__ == "__main__":
    src = HERE / (sys.argv[1] if len(sys.argv) > 1 else "poster.html")
    out = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else HERE.parent / "entry.png")
    asyncio.run(shoot(src, out))
