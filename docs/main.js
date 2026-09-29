/* Behaviour layer. Progressive throughout: with JavaScript off every page still
   renders complete, readable and navigable. The only thing gated on JS is the
   reveal animation, and that is gated on html.js so it can never hide content.
   Multi-page site, so every hook checks that its element exists first. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- masthead ---------- */
  var masthead = $('#masthead');
  if (masthead) {
    var onScroll = function () { masthead.classList.toggle('is-stuck', window.scrollY > 24); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------- mobile drawer ---------- */
  var burger = $('.burger'), drawer = $('#drawer');
  if (burger && drawer) {
    var closeDrawer = function () {
      drawer.hidden = true;
      burger.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    };
    burger.addEventListener('click', function () {
      if (burger.getAttribute('aria-expanded') === 'true') { closeDrawer(); return; }
      drawer.hidden = false;
      burger.setAttribute('aria-expanded', 'true');
      document.body.style.overflow = 'hidden';
    });
    $$('#drawer a').forEach(function (a) { a.addEventListener('click', closeDrawer); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !drawer.hidden) closeDrawer();
    });
  }

  /* ---------- reveal on scroll ---------- */
  var reveals = $$('.reveal');
  if (reveals.length) {
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          var el = e.target;
          var i = Array.prototype.slice.call(el.parentNode.children).indexOf(el);
          el.style.transitionDelay = Math.min(i, 5) * 85 + 'ms';
          el.classList.add('is-in');
          io.unobserve(el);
        });
      }, { rootMargin: '0px 0px -10% 0px', threshold: 0.08 });
      reveals.forEach(function (el) { io.observe(el); });
    } else {
      reveals.forEach(function (el) { el.classList.add('is-in'); });
    }
  }

  /* ---------- gallery lightbox ---------- */
  var figs = $$('.mosaic__item'), box = $('#lightbox');
  if (figs.length && box) {
    var boxImg = $('img', box), boxCap = $('figcaption', box), at = 0;
    var show = function (i) {
      at = (i + figs.length) % figs.length;
      var img = $('img', figs[at]);
      boxImg.src = img.currentSrc || img.src;
      boxImg.alt = img.alt || '';
      var cap = $('figcaption span', figs[at]), where = $('figcaption i', figs[at]);
      boxCap.textContent = [cap && cap.textContent, where && where.textContent]
        .filter(function (t) { return t; }).join(' · ');
      box.hidden = false;
      document.body.style.overflow = 'hidden';
    };
    var hide = function () { box.hidden = true; document.body.style.overflow = ''; };
    figs.forEach(function (f, i) { f.addEventListener('click', function () { show(i); }); });
    $('.lightbox__close', box).addEventListener('click', hide);
    $('.lightbox__nav--prev', box).addEventListener('click', function () { show(at - 1); });
    $('.lightbox__nav--next', box).addEventListener('click', function () { show(at + 1); });
    box.addEventListener('click', function (e) { if (e.target === box) hide(); });
    document.addEventListener('keydown', function (e) {
      if (box.hidden) return;
      if (e.key === 'Escape') hide();
      if (e.key === 'ArrowLeft') show(at - 1);
      if (e.key === 'ArrowRight') show(at + 1);
    });
  }

  /* ---------- enquiry form (draft — no endpoint yet) ---------- */
  var form = $('.enq__form');
  if (form) {
    var status = $('.enq__status');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var bad = false;
      $$('input[required],textarea[required]', form).forEach(function (el) {
        var ok = el.value.trim() !== '' &&
                 (el.type !== 'email' || /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(el.value));
        el.closest('.field').classList.toggle('is-bad', !ok);
        if (!ok) bad = true;
      });
      status.textContent = bad
        ? 'Please complete the highlighted fields.'
        : 'Thank you — on the live site this arrives in your inbox. (Draft: nothing was sent.)';
    });
  }
})();
