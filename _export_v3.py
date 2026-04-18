"""
Exporta as 10 variações do N5 (antes/depois) × 2 formatos = 20 PNGs.
Saída: ~/Desktop/Novos ads/
"""
import asyncio, pathlib
from playwright.async_api import async_playwright

URL = "http://localhost:8765/ads-v3.html"
OUT = pathlib.Path.home() / "Desktop" / "Novos ads"

CREATIVES = [
    ("a1-s",  "A1-relatorio-1080x1920",     1080, 1920),
    ("a1-f",  "A1-relatorio-1080x1080",     1080, 1080),
    ("a2-s",  "A2-custo-dev-1080x1920",     1080, 1920),
    ("a2-f",  "A2-custo-dev-1080x1080",     1080, 1080),
    ("a3-s",  "A3-reuniao-1080x1920",       1080, 1920),
    ("a3-f",  "A3-reuniao-1080x1080",       1080, 1080),
    ("a4-s",  "A4-conteudo-1080x1920",      1080, 1920),
    ("a4-f",  "A4-conteudo-1080x1080",      1080, 1080),
    ("a5-s",  "A5-planilha-1080x1920",      1080, 1920),
    ("a5-f",  "A5-planilha-1080x1080",      1080, 1080),
    ("a6-s",  "A6-gargalo-1080x1920",       1080, 1920),
    ("a6-f",  "A6-gargalo-1080x1080",       1080, 1080),
    ("a7-s",  "A7-proposta-1080x1920",      1080, 1920),
    ("a7-f",  "A7-proposta-1080x1080",      1080, 1080),
    ("a8-s",  "A8-email-1080x1920",         1080, 1920),
    ("a8-f",  "A8-email-1080x1080",         1080, 1080),
    ("a9-s",  "A9-financeiro-1080x1920",    1080, 1920),
    ("a9-f",  "A9-financeiro-1080x1080",    1080, 1080),
    ("a10-s", "A10-jornada12h-1080x1920",   1080, 1920),
    ("a10-f", "A10-jornada12h-1080x1080",   1080, 1080),
]

RESET_JS = """
() => {
  document.querySelectorAll('.scaled-feed, .scaled-stories').forEach(el => {
    el.style.transform = 'none'; el.style.margin = '0';
  });
  document.querySelectorAll('.page > header, .creative-meta').forEach(el => el.style.display = 'none');
  document.body.style.background = 'transparent';
  document.querySelector('.page').style.padding = '0';
}
"""

async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1200, "height": 2200}, device_scale_factor=1)
        page = await ctx.new_page()
        await page.goto(URL, wait_until="networkidle")
        await page.evaluate(RESET_JS)

        for ad_id, name, w, h in CREATIVES:
            el = page.locator(f"#{ad_id} .creative")
            await el.scroll_into_view_if_needed()
            out_path = OUT / f"{name}.png"
            await el.screenshot(path=str(out_path), type="png")
            size_kb = out_path.stat().st_size / 1024
            print(f"✓ {name}.png  ({w}x{h}, {size_kb:.1f} KB)")

        await browser.close()
    print(f"\n→ Salvos em: {OUT}")

if __name__ == "__main__":
    asyncio.run(main())
