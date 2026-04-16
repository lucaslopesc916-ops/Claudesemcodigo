"""
Exporta os 20 criativos do ads-v2.html (10 ângulos × 2 formatos) como PNG.
Saída: ~/Desktop/Novos ads/
"""
import asyncio, pathlib
from playwright.async_api import async_playwright

URL = "http://localhost:8765/ads-v2.html"
OUT = pathlib.Path.home() / "Desktop" / "Novos ads"

CREATIVES = [
    ("v1-f",  "V1-custo-nao-fazer-1080x1080",      1080, 1080),
    ("v1-s",  "V1-custo-nao-fazer-1080x1920",      1080, 1920),
    ("v2-f",  "V2-curiosidade-1080x1080",          1080, 1080),
    ("v2-s",  "V2-curiosidade-1080x1920",          1080, 1920),
    ("v3-f",  "V3-contra-dev-1080x1080",           1080, 1080),
    ("v3-s",  "V3-contra-dev-1080x1920",           1080, 1920),
    ("v4-f",  "V4-velocidade-fds-1080x1080",       1080, 1080),
    ("v4-s",  "V4-velocidade-fds-1080x1920",       1080, 1920),
    ("v5-f",  "V5-identidade-1080x1080",           1080, 1080),
    ("v5-s",  "V5-identidade-1080x1920",           1080, 1920),
    ("v6-f",  "V6-fomo-concorrente-1080x1080",     1080, 1080),
    ("v6-s",  "V6-fomo-concorrente-1080x1920",     1080, 1920),
    ("v7-f",  "V7-pergunta-1080x1080",             1080, 1080),
    ("v7-s",  "V7-pergunta-1080x1920",             1080, 1920),
    ("v8-f",  "V8-setores-1080x1080",              1080, 1080),
    ("v8-s",  "V8-setores-1080x1920",              1080, 1920),
    ("v9-f",  "V9-era-2026-1080x1080",             1080, 1080),
    ("v9-s",  "V9-era-2026-1080x1920",             1080, 1920),
    ("v10-f", "V10-garantia-1080x1080",            1080, 1080),
    ("v10-s", "V10-garantia-1080x1920",            1080, 1920),
]

RESET_TRANSFORM_JS = """
() => {
  document.querySelectorAll('.scaled-feed, .scaled-stories').forEach(el => {
    el.style.transform = 'none';
    el.style.margin = '0';
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
        ctx = await browser.new_context(
            viewport={"width": 1200, "height": 2200},
            device_scale_factor=1,
        )
        page = await ctx.new_page()
        await page.goto(URL, wait_until="networkidle")
        await page.evaluate(RESET_TRANSFORM_JS)
        await page.wait_for_load_state("networkidle")

        for ad_id, name, w, h in CREATIVES:
            selector = f"#{ad_id} .creative"
            el = page.locator(selector)
            await el.scroll_into_view_if_needed()
            out_path = OUT / f"{name}.png"
            await el.screenshot(path=str(out_path), type="png")
            size_kb = out_path.stat().st_size / 1024
            print(f"✓ {name}.png  ({w}x{h}, {size_kb:.1f} KB)")

        await browser.close()
    print(f"\n→ Salvos em: {OUT}")

if __name__ == "__main__":
    asyncio.run(main())
