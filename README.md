# Claude sem Código — Página de pré-venda

Página estática em HTML/CSS/JS puro. Zero dependências externas. Funciona em qualquer servidor estático (Netlify, Vercel, Cloudflare Pages, GitHub Pages, S3, Kiwify, etc.).

---

## Estrutura

```
claude-sem-codigo/
├── index.html     → Página principal (CSS crítico inline)
├── styles.css     → Estilos não-críticos
├── app.js         → Motor: contador, tracking, scroll depth
├── flow.js        → Configuração editável (preço, prazo, link, IDs)
├── README.md      → Este arquivo
└── DEPLOY.md      → Como publicar
```

---

## Rodar localmente

Basta abrir o `index.html` no navegador. Ou, para servir num servidor local:

```bash
npx serve .
# ou
python3 -m http.server 8000
```

Abre em `http://localhost:8000`.

---

## Personalizar (sem tocar em código complexo)

### Mudar preço, prazo ou link de checkout

Abra **`flow.js`** e edite:

```javascript
offer: {
  productName: 'Claude sem Código',
  priceFull: 247,
  pricePromo: 127,
  checkoutUrl: 'https://pay.kiwify.com.br/aH5fe5K',
},

deadline: '2026-04-20T23:59:59-03:00',
```

> ⚠️ Os valores em `flow.js` são para referência/tracking. Os números que aparecem na página estão no `index.html` (busca por `R$247` e `R$127` e altera). O link de checkout aparece em 3 lugares no HTML — busca por `pay.kiwify.com.br` e substitui em todos.

### Adicionar depoimentos

Abra **`index.html`** e procure por `DEPOIMENTO 1`. Cole o texto real no lugar de cada placeholder. Pode adicionar ou remover `<li>...</li>` à vontade.

Estrutura:

```html
<li>
  <p>Texto do depoimento aqui.</p>
  <span class="quote-who">— Nome do aluno, cargo/empresa</span>
</li>
```

### Trocar o nome do criador

Busque por `Lucas Lopes` no `index.html` (aparece 2x: no bloco "Quem sou" e no footer) e substitua.

### Trocar cores da marca

Abra **`index.html`** e procure pelo bloco `:root{` no `<style>` do `<head>`. As variáveis de cor estão lá:

```css
:root{
  --cream:#F5F0E8;   /* fundo */
  --coral:#D97757;   /* acento e CTA */
  --dark:#1F1F1F;    /* texto principal */
  --brown:#8B6F47;   /* secundário */
}
```

---

## Tracking (opcional)

Abra **`flow.js`** e preencha as chaves que for usar:

```javascript
tracking: {
  ga4_id: 'G-XXXXXXXXXX',         // Google Analytics 4
  meta_pixel_id: '1234567890',    // Meta (Facebook) Pixel
  custom_webhook: 'https://...',  // Webhook para Zapier/Make/etc.
},
```

Se deixar vazio, os eventos só vão pro console do navegador (pressione F12 → aba Console para ver).

### Instalar scripts do GA4 / Pixel

Se quiser usar GA4 ou Meta Pixel, você precisa **também** carregar os scripts oficiais deles antes do `app.js`. Cole dentro do `<head>` do `index.html`, logo antes do `</head>`:

**GA4:**
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

**Meta Pixel:** pegue o snippet oficial em [business.facebook.com](https://business.facebook.com) e cole no mesmo lugar.

> ⚠️ Adicionar esses scripts aumenta o peso e o tempo de carregamento. Só adicione se for usar de verdade.

### Eventos disparados automaticamente

| Evento | Quando |
|---|---|
| `page_view` | Ao carregar a página |
| `cta_click` | Ao clicar em qualquer botão de compra (dado `position` identifica qual: `hero`, `offer`, `final`) |
| `scroll_depth` | A cada 25%, 50%, 75%, 100% de scroll |
| `page_exit` | Ao sair da página (com tempo total em segundos) |

---

## Depois que a pré-venda acabar

O contador muda sozinho para o texto definido em `deadlineFallback`. **Mas os números R$247 e R$127 no HTML continuam fixos** — você precisa abrir o `index.html` e atualizar manualmente:

1. Remover os blocos `.price-old` (preço antigo riscado)
2. Trocar `R$127` por `R$247`
3. Atualizar a ancoragem `.anchor` da seção de oferta

Ou, mais simples: trocar o link de checkout para um novo produto pós-lançamento.

---

## Variações de headline para teste A/B

Se quiser testar, troque o `<h1>` principal por uma destas:

1. **(original)** Automatize **8 horas por semana** do seu negócio com Claude — sem virar programador.
2. O método que empresário usa pra fazer Claude trabalhar sozinho — sem abrir uma linha de código.
3. Pare de pagar R$3-8k/mês pra dev automatizar o que Claude faz em 1 fim de semana.
4. Você já sabe usar Claude. Agora aprende a fazer ele trabalhar por você (mesmo não sendo dev).
5. A Trinca Claude: o jeito mais rápido de um não-dev eliminar 8h/semana de tarefa manual.

---

## Performance

- Página total < 30KB (sem tracking externo)
- Zero requisições a CDNs
- System fonts (carregamento instantâneo)
- CSS crítico inline, não-crítico com `<link>`
- JS com `defer` (não bloqueia render)

Meta: **LCP < 1.5s**, **CLS 0**, **INP < 100ms**.

Teste com:
- [PageSpeed Insights](https://pagespeed.web.dev)
- [WebPageTest](https://webpagetest.org)

---

## Acessibilidade

- Navegação por teclado (Tab/Shift+Tab/Enter) funcional
- Foco visível em todos os interativos
- `prefers-reduced-motion` respeitado
- Contraste AA (4.5:1 para texto)
- FAQ usa `<details>` nativo (funciona sem JS)
- Semântica correta (`<header>`, `<main>`, `<section>`, `<footer>`)

---

## Checklist antes de publicar

- [ ] Link do checkout correto em **todos os 3 CTAs** do HTML
- [ ] 4 depoimentos reais colados (ou reduzir o bloco)
- [ ] Nome correto do criador no bloco "Quem sou" e no footer
- [ ] `deadline` em `flow.js` com a data certa no fuso `-03:00`
- [ ] IDs de tracking preenchidos (se for usar)
- [ ] Testar contador regressivo (abre o console e confere o `page_view`)
- [ ] Testar clique em cada um dos 3 CTAs (deve abrir a Kiwify)
- [ ] Ver no mobile (Chrome DevTools → modo device)
- [ ] Rodar PageSpeed Insights
