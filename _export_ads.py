"""
Exporta os 9 criativos do ads.html como PNG em ~/Desktop/claude-sem-codigo-ads/
Dimensões reais: 1080x1080 (feed) e 1080x1920 (stories).
"""
import asyncio, os, pathlib
from playwright.async_api import async_playwright

URL = "http://localhost:8765/ads.html"
OUT = pathlib.Path.home() / "Desktop" / "claude-sem-codigo-ads"

CREATIVES = [
    # (id, descricao, width, height)
    # --- novos (ângulo "Domine o Claude") ---
    ("n1", "N1-domine-claude-dark",   1080, 1080),
    ("n2", "N2-nao-precisa-dev",      1080, 1080),
    ("n3", "N3-trinca-dominada",      1080, 1080),
    ("n4", "N4-domine-vertical",      1080, 1920),
    ("n5", "N5-antes-depois",         1080, 1920),
    ("n6", "N6-urgencia-claude",      1080, 1920),
    # --- originais ---
    ("f1", "F1-dor-resultado",        1080, 1080),
    ("f2", "F2-prova-social",         1080, 1080),
    ("f3", "F3-trinca-mecanismo",     1080, 1080),
    ("f4", "F4-autoridade-foto",      1080, 1080),
    ("f5", "F5-oferta-direta",        1080, 1080),
    ("s1", "S1-dor-expandida",        1080, 1920),
    ("s2", "S2-stack-completo",       1080, 1920),
    ("s3", "S3-depoimento",           1080, 1920),
    ("s4", "S4-urgencia",             1080, 1920),
]

RESET_TRANSFORM_JS = """
() => {
  // Remove escala visual; criativos voltam a 1080x1080 / 1080x1920 reais
  document.querySelectorAll('.scaled-feed, .scaled-stories').forEach(el => {
    el.style.transform = 'none';
    el.style.margin = '0';
  });
  // Esconde shell da página (header, nav, meta) pra não atrapalhar
  document.querySelectorAll('.page > header, .creative-meta').forEach(el => el.style.display = 'none');
  // Fundo transparente no wrap pra não ficar listra
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
            device_scale_factor=1,  # 1080px = 1080px reais, nada de retina scaling
        )
        page = await ctx.new_page()
        await page.goto(URL, wait_until="networkidle")
        await page.evaluate(RESET_TRANSFORM_JS)
        # espera imagens carregarem
        await page.wait_for_load_state("networkidle")

        for ad_id, name, w, h in CREATIVES:
            selector = f"#{ad_id} .creative"
            el = page.locator(selector)
            await el.scroll_into_view_if_needed()
            out_path = OUT / f"{name}.png"
            await el.screenshot(
                path=str(out_path),
                omit_background=False,
                type="png",
            )
            size_kb = out_path.stat().st_size / 1024
            print(f"✓ {name}.png  ({w}x{h}, {size_kb:.1f} KB)")

        await browser.close()
    print(f"\n→ Salvos em: {OUT}")

if __name__ == "__main__":
    asyncio.run(main())
