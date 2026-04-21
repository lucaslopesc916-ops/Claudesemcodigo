/* ============================================================
   Claude sem Código — motor da página
   - Contador regressivo (header + CTA final)
   - Scroll reveal (IntersectionObserver, respeita reduced-motion)
   - Tracking plugável (GA4 / Meta Pixel / webhook / console)
   - Scroll depth + CTA click + page exit
   ============================================================ */

(function () {
  'use strict';

  var CFG = window.FLOW || {};
  var TRACKING = (CFG.tracking || {});

  // ---------------------------------------------------------
  // Tracking — sempre loga; dispara para ferramentas se houver ID
  // ---------------------------------------------------------
  function track(name, data) {
    data = data || {};
    data.timestamp = new Date().toISOString();

    try { console.log('[TRACK]', name, data); } catch (_) {}

    if (TRACKING.ga4_id && typeof window.gtag === 'function') {
      try { window.gtag('event', name, data); } catch (_) {}
    }
    if (TRACKING.meta_pixel_id && typeof window.fbq === 'function') {
      try { window.fbq('trackCustom', name, data); } catch (_) {}
    }
    if (TRACKING.custom_webhook && navigator.sendBeacon) {
      try {
        var payload = JSON.stringify({ event: name, data: data });
        var blob = new Blob([payload], { type: 'application/json' });
        navigator.sendBeacon(TRACKING.custom_webhook, blob);
      } catch (_) {}
    }
  }

  // ---------------------------------------------------------
  // Contador regressivo
  // ---------------------------------------------------------
  function pad(n) { return n < 10 ? '0' + n : '' + n; }

  function updateCountdown() {
    if (!CFG.deadline) return false;
    var target = new Date(CFG.deadline).getTime();
    if (isNaN(target)) return false;

    var diff = target - Date.now();
    var els = document.querySelectorAll('#countdown, #countdown-2');

    if (diff <= 0) {
      var fallback = CFG.deadlineFallback || '';
      for (var i = 0; i < els.length; i++) {
        els[i].textContent = fallback;
        var parent = els[i].parentNode;
        if (parent && parent.firstChild && parent.firstChild.nodeType === 3) {
          parent.firstChild.nodeValue = '';
        }
      }
      return true;
    }

    var dias = Math.floor(diff / 86400000);
    var horas = Math.floor((diff % 86400000) / 3600000);
    var mins = Math.floor((diff % 3600000) / 60000);
    var secs = Math.floor((diff % 60000) / 1000);

    var txt = dias + 'd ' + pad(horas) + 'h ' + pad(mins) + 'm ' + pad(secs) + 's';
    for (var j = 0; j < els.length; j++) els[j].textContent = txt;
    return false;
  }

  function startCountdown() {
    if (updateCountdown()) return;
    var id = setInterval(function () {
      if (updateCountdown()) clearInterval(id);
    }, 1000);
  }

  // ---------------------------------------------------------
  // Scroll reveal (IntersectionObserver)
  // ---------------------------------------------------------
  function setupReveal() {
    var els = document.querySelectorAll('.reveal');
    if (!els.length) return;

    // Sem suporte (ex: navegadores antigos) ou reduced-motion → mostra tudo
    var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduced || !('IntersectionObserver' in window)) {
      for (var i = 0; i < els.length; i++) els[i].classList.add('is-in');
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.15,
      rootMargin: '0px 0px -40px 0px'
    });

    els.forEach(function (el) { io.observe(el); });
  }

  // ---------------------------------------------------------
  // Scroll depth (25/50/75/100)
  // ---------------------------------------------------------
  function bindScrollDepth() {
    var marks = [25, 50, 75, 100];
    var fired = {};
    function onScroll() {
      var h = document.documentElement;
      var scrolled = (h.scrollTop + window.innerHeight) / h.scrollHeight * 100;
      for (var i = 0; i < marks.length; i++) {
        var m = marks[i];
        if (!fired[m] && scrolled >= m) {
          fired[m] = true;
          track('scroll_depth', { percent: m });
        }
      }
    }
    var throttled = false;
    window.addEventListener('scroll', function () {
      if (throttled) return;
      throttled = true;
      setTimeout(function () { throttled = false; onScroll(); }, 400);
    }, { passive: true });
  }

  // ---------------------------------------------------------
  // CTA clicks
  // ---------------------------------------------------------
  function bindCtas() {
    var ctas = document.querySelectorAll('[data-cta]');
    for (var i = 0; i < ctas.length; i++) {
      ctas[i].addEventListener('click', function (e) {
        var where = e.currentTarget.getAttribute('data-cta');
        track('cta_click', { position: where });
      });
    }
  }

  // ---------------------------------------------------------
  // Exit
  // ---------------------------------------------------------
  function bindExit() {
    var start = Date.now();
    window.addEventListener('beforeunload', function () {
      var seconds = Math.round((Date.now() - start) / 1000);
      track('page_exit', { seconds_on_page: seconds });
    });
  }

  // ---------------------------------------------------------
  // Year stamp no footer
  // ---------------------------------------------------------
  function setYear() {
    var y = document.getElementById('year');
    if (y) y.textContent = new Date().getFullYear();
  }

  // ---------------------------------------------------------
  // Boot
  // ---------------------------------------------------------
  function boot() {
    track('page_view', { url: location.href, referrer: document.referrer || '(direct)' });
    setYear();
    startCountdown();
    setupReveal();
    bindCtas();
    bindScrollDepth();
    bindExit();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

})();
