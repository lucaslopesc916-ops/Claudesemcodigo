/* ===========================================================
   Claude sem Código — configuração editável
   Mexa aqui para mudar preço, prazo, link, tracking.
   Não precisa tocar em app.js.
   =========================================================== */

window.FLOW = {

  // ---- Oferta ---------------------------------------------------------------
  offer: {
    productName: 'Claude sem Código',
    priceFull: 247,
    pricePromo: 127,
    checkoutUrl: 'https://pay.kiwify.com.br/aH5fe5K',
  },

  // ---- Prazo da pré-venda (usado no contador regressivo) -------------------
  // Formato ISO. Fuso horário do Brasil (-03:00).
  // Após esta data, o contador some e a faixa superior muda para fallback.
  deadline: '2026-04-20T23:59:59-03:00',

  // Texto de fallback exibido quando a pré-venda expira.
  // Se você estender a pré-venda, basta alterar `deadline` acima.
  deadlineFallback: 'Pré-venda encerrada — preço cheio R$247',

  // ---- Tracking -------------------------------------------------------------
  // Preencha só o que for usar. Vazio = apenas log no console.
  tracking: {
    ga4_id: '',                    // Ex: 'G-XXXXXXXXXX'
    meta_pixel_id: '880818017355660',
    custom_webhook: '',            // Ex: 'https://hooks.zapier.com/...'
  },

};
