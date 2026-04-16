"""
Exporta os criativos do ads.html como PNG.

Saída: ~/Desktop/claude-sem-codigo-ads/ads/ (pasta dos favoritos do Lucas)
- Só exporta os 10 favoritos originais + suas 10 duplas complementares.
- Dimensões reais: 1080x1080 (feed) e 1080x1920 (stories).
"""
import asyncio, pathlib
from playwright.async_api import async_playwright

URL = "http://localhost:8765/ads.html"
OUT = pathlib.Path.home() / "Desktop" / "claude-sem-codigo-ads" / "ads"

CREATIVES = [
    # (id, descricao, width, height)
    # ---- Favoritos originais (já existem, mas re-exportamos pra ter tudo sincronizado) ----
    ("f1",    "F1-dor-resultado-1080x1080",        1080, 1080),
    ("f2",    "F2-prova-social-1080x1080",         1080, 1080),
    ("f5",    "F5-oferta-direta-1080x1080",        1080, 1080),
    ("n1",    "N1-domine-claude-dark-1080x1080",   1080, 1080),
    ("n2",    "N2-nao-precisa-dev-1080x1080",      1080, 1080),
    ("n3",    "N3-trinca-dominada-1080x1080",      1080, 1080),
    ("n4",    "N4-domine-vertical-1080x1920",      1080, 1920),
    ("n5",    "N5-antes-depois-1080x1920",         1080, 1920),
    ("n6",    "N6-urgencia-claude-1080x1920",      1080, 1920),
    ("s1",    "S1-dor-expandida-1080x1920",        1080, 1920),
    # ---- Duplas (formato complementar de cada favorito) ----
    ("f1-s",  "F1-dor-resultado-1080x1920",        1080, 1920),
    ("f2-s",  "F2-prova-social-1080x1920",         1080, 1920),
    ("f5-s",  "F5-oferta-direta-1080x1920",        1080, 1920),
    ("n1-s",  "N1-domine-claude-dark-1080x1920",   1080, 1920),
    ("n2-s",  "N2-nao-precisa-dev-1080x1920",      1080, 1920),
    ("n3-s",  "N3-trinca-dominada-1080x1920",      1080, 1920),
    ("n4-f",  "N4-domine-vertical-1080x1080",      1080, 1080),
    ("n5-f",  "N5-antes-depois-1080x1080",         1080, 1080),
    ("n6-f",  "N6-urgencia-claude-1080x1080",      1080, 1080),
    ("s1-f",  "S1-dor-expandida-1080x1080",        1080, 1080),
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
