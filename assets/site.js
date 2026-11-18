/* Selepe & Associates Inc – site behaviour (no dependencies) */
(function () {
  'use strict';

  /* ---- Contact form --------------------------------------------------
     Set FORM_ENDPOINT to a Formspree / Laravel / Netlify endpoint to post
     enquiries. While it is empty the form falls back to opening the visitor's
     email app addressed to info@selepe.co. */
  var FORM_ENDPOINT = '';
  var FORM_TO = 'info@selepe.co';

  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  // Year
  $$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // Header: solidify on scroll
  var header = $('#site-header');
  function onScroll() {
    if (!header) return;
    var scrolled = window.scrollY > 24;
    header.classList.toggle('bg-navy-950', scrolled);
    header.classList.toggle('bg-navy-950/85', !scrolled);
    header.classList.toggle('shadow-lift', scrolled);
  }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // Mobile menu
  var btn = $('#menu-btn');
  var menu = $('#mobile-menu');
  if (btn && menu) {
    btn.addEventListener('click', function () {
      var open = menu.classList.toggle('hidden') === false;
      btn.setAttribute('aria-expanded', String(open));
      btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      document.body.classList.toggle('overflow-hidden', open);
    });
    $$('a', menu).forEach(function (a) {
      a.addEventListener('click', function () {
        menu.classList.add('hidden');
        document.body.classList.remove('overflow-hidden');
        btn.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Scroll reveal
  var items = $$('.reveal');
  if ('IntersectionObserver' in window && items.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    items.forEach(function (el, i) {
      el.style.transitionDelay = (el.dataset.delay || 0) + 'ms';
      io.observe(el);
    });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  // Count-up stats
  $$('[data-count]').forEach(function (el) {
    var target = parseInt(el.dataset.count, 10);
    var suffix = el.dataset.suffix || '';
    if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      el.textContent = target + suffix; return;
    }
    var obs = new IntersectionObserver(function (en) {
      if (!en[0].isIntersecting) return;
      obs.disconnect();
      var start = null, dur = 1200;
      function step(ts) {
        if (!start) start = ts;
        var p = Math.min((ts - start) / dur, 1);
        el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))) + suffix;
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }, { threshold: 0.6 });
    obs.observe(el);
  });

  // Subscription tabs
  var tabs = $$('[data-tab]');
  if (tabs.length) {
    function show(name) {
      tabs.forEach(function (t) {
        var on = t.dataset.tab === name;
        t.setAttribute('aria-selected', String(on));
        t.classList.toggle('bg-navy-900', on);
        t.classList.toggle('text-white', on);
        t.classList.toggle('text-navy-700', !on);
      });
      $$('[data-panel]').forEach(function (p) { p.classList.toggle('hidden', p.dataset.panel !== name); });
    }
    tabs.forEach(function (t) { t.addEventListener('click', function () { show(t.dataset.tab); }); });
    show(tabs[0].dataset.tab);
  }

  // Pre-fill the contact form from ?plan=... links (subscriptions, pilots, training)
  (function () {
    var plan = new URLSearchParams(window.location.search).get('plan');
    var form = $('form[data-contact]');
    if (!plan || !form || !form.elements.message) return;
    var topic = form.elements.topic;
    var map = [
      [/LEAP/i, 'LEAP Academy training'],
      [/proof/i, 'Recoveries and collections'],
      [/.*/, 'Legal-as-a-Service plan']
    ];
    if (topic && topic.tagName === 'SELECT') {
      for (var i = 0; i < map.length; i++) {
        if (map[i][0].test(plan)) { topic.value = map[i][1]; break; }
      }
    }
    form.elements.message.value = /LEAP|proof/i.test(plan)
      ? 'I would like to enquire about: ' + plan + '.'
      : 'I would like to enquire about the ' + plan + ' plan.';
  })();

  // Contact / enquiry forms
  $$('form[data-contact]').forEach(function (form) {
    var status = $('[data-status]', form);
    function say(msg, ok) {
      if (!status) return;
      status.textContent = msg;
      status.className = 'text-sm ' + (ok ? 'text-emerald-700' : 'text-red-700');
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var data = new FormData(form);
      var name = (data.get('name') || '').toString().trim();
      var email = (data.get('email') || '').toString().trim();
      var message = (data.get('message') || '').toString().trim();
      if (!name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || message.length < 5) {
        say('Please add your name, a valid email address and a short message.', false);
        return;
      }
      if (data.get('company_website')) return; // honeypot
      if (FORM_ENDPOINT) {
        fetch(FORM_ENDPOINT, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
          .then(function (r) { if (!r.ok) throw new Error(); form.reset(); say('Thank you. We will be in touch shortly.', true); })
          .catch(function () { say('Something went wrong. Please email ' + FORM_TO + ' or call 076 984 8560.', false); });
      } else {
        var topic = (data.get('topic') || 'Enquiry').toString();
        var phone = (data.get('phone') || '').toString();
        var body = message + '\n\n— ' + name + (phone ? '\nPhone: ' + phone : '') + '\nEmail: ' + email;
        window.location.href = 'mailto:' + FORM_TO + '?subject=' + encodeURIComponent('Website enquiry: ' + topic) + '&body=' + encodeURIComponent(body);
        say('Opening your email app. If nothing happens, write to ' + FORM_TO + '.', true);
      }
    });
  });
})();
