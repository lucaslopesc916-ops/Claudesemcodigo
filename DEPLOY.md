# Deploy — Claude sem Código

Escolha uma das opções abaixo. Todas são grátis para esse volume de tráfego.

---

## Opção 1 — Netlify (mais rápido, recomendado)

**Sem CLI, drag-and-drop:**

1. Vai em [app.netlify.com/drop](https://app.netlify.com/drop)
2. Arrasta a pasta `claude-sem-codigo/` inteira
3. Pronto — te dão uma URL tipo `random-name.netlify.app`
4. Opcional: em **Domain settings**, aponte um domínio seu

**Com CLI (se vai atualizar muito):**

```bash
npm install -g netlify-cli
cd "claude-sem-codigo"
netlify deploy --prod
```

Primeiro deploy pergunta se cria novo site. Diga sim. Próximos deploys só rodar o comando.

---

## Opção 2 — Vercel

```bash
npm install -g vercel
cd "claude-sem-codigo"
vercel --prod
```

Primeira vez pede login e nome do projeto. Depois, cada `vercel --prod` publica.

---

## Opção 3 — Cloudflare Pages

**Via upload direto (sem Git):**

1. Vai em [dash.cloudflare.com](https://dash.cloudflare.com) → **Workers & Pages** → **Create** → **Upload assets**
2. Arrasta a pasta
3. Recebe URL `.pages.dev`

**Via Git:**

1. Suba a pasta num repo GitHub
2. No Cloudflare: **Pages** → **Connect to Git**
3. Framework preset: **None**
4. Build command: (vazio)
5. Build output directory: `/`

---

## Opção 4 — GitHub Pages

1. Cria um repo público no GitHub: `claude-sem-codigo`
2. Sobe os arquivos (no root, não dentro de subpasta)
3. **Settings** → **Pages** → **Source**: Deploy from branch → `main` → `/`
4. Em 1-2 min abre em `https://seu-usuario.github.io/claude-sem-codigo`

> GitHub Pages exige que o repo seja público no plano grátis.

---

## Opção 5 — Amazon S3 (se quiser AWS)

```bash
aws s3 mb s3://claude-sem-codigo-site
aws s3 website s3://claude-sem-codigo-site --index-document index.html
aws s3 sync "./" s3://claude-sem-codigo-site --acl public-read \
  --exclude "README.md" --exclude "DEPLOY.md"
```

URL: `http://claude-sem-codigo-site.s3-website-<região>.amazonaws.com`

Para HTTPS + domínio próprio, coloca CloudFront na frente.

---

## Opção 6 — Firebase Hosting

```bash
npm install -g firebase-tools
cd "claude-sem-codigo"
firebase login
firebase init hosting
# "public directory": .
# "single-page app": No
# "overwrite index.html": No
firebase deploy
```

---

## Domínio próprio

Independente do host escolhido, o fluxo é:

1. Compra o domínio (Registro.br, Cloudflare Registrar, Namecheap)
2. No painel do host (Netlify / Vercel / etc.), adiciona o domínio
3. No registrador do domínio, aponta os **DNS** que o host pedir (CNAME ou A)
4. Espera propagar (até 24h, normalmente 5-30min)
5. O host emite certificado SSL automático

---

## Depois de publicar

1. Abre a URL no navegador
2. F12 → **Console** → confere se aparecem os `[TRACK] page_view ...`
3. Clica em cada um dos 3 botões "Quero..." e confere se chega na Kiwify
4. Abre no celular (manda o link pra você mesmo via WhatsApp e clica)
5. Roda [PageSpeed Insights](https://pagespeed.web.dev) — esperado score **95+** em mobile
6. Se usar GA4/Pixel: confere se os eventos chegam nas ferramentas

---

## Atualizando a página

- **Netlify / Vercel / Cloudflare (com Git):** `git push` e atualiza sozinho
- **Netlify drag-and-drop:** arrasta de novo em [app.netlify.com/drop](https://app.netlify.com/drop) — mantém mesmo URL
- **S3:** roda o `aws s3 sync ...` de novo
- **Firebase:** `firebase deploy`
- **GitHub Pages:** commit no repo

---

## Troubleshooting

**"Contador não aparece / não atualiza"**
Abre o console (F12). Se aparece erro, provavelmente o `flow.js` não carregou. Confere se o arquivo está na mesma pasta do `index.html`.

**"Cliquei no botão e não foi pra lugar nenhum"**
Confere o `href="https://pay.kiwify.com.br/..."` nos 3 CTAs do HTML. Link quebrado = botão morto.

**"PageSpeed deu nota baixa"**
Se instalou GA4 ou Pixel, eles pesam. É trade-off esperado. Sem eles, a nota volta pra 95+.

**"Página sem CSS quando abro"**
`styles.css` tem que estar na mesma pasta do `index.html`. Ou você abriu via `file://` em um navegador que bloqueia isso — use `npx serve .` pra servir local.
