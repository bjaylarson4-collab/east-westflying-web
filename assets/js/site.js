/* East-Westflying – kleines Skript für alle Seiten.
   Seitenspezifische Daten (Quick-Check, Vorbildung) stehen als JSON in <script type="application/json" id="ewf-data">. */
(function () {
  var preview = document.body.hasAttribute('data-preview');
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var data = {};
  try { var dn = $('#ewf-data'); if (dn) data = JSON.parse(dn.textContent); } catch (e) {}

  // Mobiles Menü
  var mb = $('#menu-btn'), mn = $('#mnav');
  if (mb && mn) {
    mb.addEventListener('click', function () {
      var open = mn.classList.toggle('open');
      mb.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    mn.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { mn.classList.remove('open'); mb.setAttribute('aria-expanded', 'false'); }
    });
  }

  // Podcast: ein gemeinsamer Player für alle Folgen (Startseite)
  var player = $('#pod-player');
  $$('.eps button').forEach(function (b) {
    b.addEventListener('click', function () {
      if (!player) return;
      var same = player.getAttribute('src') === b.dataset.src;
      $$('.eps button').forEach(function (x) { x.classList.remove('on'); x.textContent = '▶ Anhören'; });
      if (same && !player.paused) { player.pause(); return; }
      if (!same) player.src = b.dataset.src;
      player.hidden = false;
      b.classList.add('on'); b.textContent = '❚❚ Pause';
      var p = player.play(); if (p && p.catch) p.catch(function () {});
    });
  });

  // Podcast-Seite: Folgen nach Thema filtern
  var pf = $$('#pod-filter button');
  pf.forEach(function (b) {
    b.addEventListener('click', function () {
      var c = b.dataset.cat;
      pf.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      $$('#pod-all .ep').forEach(function (e) { e.hidden = c !== 'alle' && e.dataset.cat !== c; });
    });
  });

  // Videos: erst nach Klick laden (keine Verbindung zu YouTube vorher)
  $$('.yt').forEach(function (yt) {
    if (preview) return;
    yt.addEventListener('click', function (e) {
      e.preventDefault();
      yt.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + yt.dataset.yt +
        '?autoplay=1" title="' + (yt.dataset.title || 'Video') + '" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>';
    });
  });

  // Kalender (Calendly): erst nach Klick laden
  $$('[data-calendly]').forEach(function (a) {
    var box = $(a.dataset.calendly), status = $(a.dataset.status);
    if (!box) return;
    a.addEventListener('click', function (e) {
      if (preview || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      e.preventDefault();
      if (box.firstChild) { box.scrollIntoView({ block: 'start' }); return; }
      var u = new URL(a.href);
      u.searchParams.set('embed_domain', location.hostname);
      u.searchParams.set('embed_type', 'Inline');
      var close = document.createElement('button');
      close.type = 'button'; close.className = 'cbtn'; close.textContent = 'Kalender schließen';
      close.addEventListener('click', function () {
        box.innerHTML = ''; a.setAttribute('aria-expanded', 'false');
        if (status) status.textContent = 'Der Kalender ist geschlossen. Du kannst ihn erneut öffnen oder mir eine E-Mail schreiben.';
      });
      var f = document.createElement('iframe');
      f.title = 'Telefondate mit East-Westflying – Termin bei Calendly auswählen';
      f.referrerPolicy = 'strict-origin-when-cross-origin';
      f.src = u.href;
      box.appendChild(close); box.appendChild(f);
      a.setAttribute('aria-expanded', 'true');
      if (status) status.textContent = 'Der externe Calendly-Kalender wird geladen. Es ist noch kein Termin gebucht.';
      box.scrollIntoView({ block: 'start' });
    });
  });

  // Chat (Chatbase): erst nach Klick laden
  var chat = $('#ewf-chat');
  if (chat) {
    chat.addEventListener('click', function () {
      if (preview) return;
      chat.disabled = true; chat.textContent = 'Chat wird geladen …';
      if (!window.chatbase) {
        var cb = function () { (cb.q = cb.q || []).push(arguments); };
        window.chatbase = window.Proxy ? new Proxy(cb, { get: function (t, p) { return p === 'q' ? t.q : function () { return t.apply(null, [p].concat([].slice.call(arguments))); }; } }) : cb;
      }
      var s = document.createElement('script');
      s.src = 'https://www.chatbase.co/embed.min.js';
      s.id = chat.dataset.bot;
      s.setAttribute('domain', 'www.chatbase.co');
      s.onload = function () {
        chat.hidden = true;
        try { window.chatbase('open'); } catch (e) {}
        var tries = 0, t = setInterval(function () {
          var b = document.getElementById('chatbase-bubble-button');
          if (b) { clearInterval(t); b.click(); } else if (++tries > 40) clearInterval(t);
        }, 150);
      };
      s.onerror = function () { chat.disabled = false; chat.textContent = 'Chat nicht erreichbar'; };
      document.body.appendChild(s);
    });
  }

  // Quick-Check: Regeln aus den Seitendaten
  var res = $('#ewfr');
  if (res && data.rules) {
    var st = {};
    $$('#ewfq .chk').forEach(function (c) {
      c.addEventListener('click', function () {
        var on = c.getAttribute('aria-pressed') !== 'true';
        c.setAttribute('aria-pressed', on ? 'true' : 'false');
        st[c.dataset.k] = on; upd();
      });
    });
    var upd = function () {
      var r = null;
      data.rules.some(function (x) {
        var ok = (x.all || []).every(function (k) { return st[k]; }) &&
          (!x.any || x.any.some(function (k) { return st[k]; })) &&
          (x.none || []).every(function (k) { return !st[k]; });
        if (ok) r = x; return ok;
      });
      if (!r) { res.innerHTML = '<strong>Tipp etwas an</strong>Dann bekommst du eine erste Einschätzung.'; return; }
      res.innerHTML = '<strong>' + r.t + '</strong>' + r.x + ' <a href="' + (r.href || res.dataset.contact) + '">' + (r.link || 'Lass uns sprechen') + '</a>';
    };
  }

  // Ablauf-Etappen
  var tabs = $$('#ewft .tab'), panes = $$('#ablauf .pane');
  tabs.forEach(function (b, i) {
    b.addEventListener('click', function () {
      tabs.forEach(function (x) { x.setAttribute('aria-selected', 'false'); });
      panes.forEach(function (x) { x.hidden = true; });
      b.setAttribute('aria-selected', 'true'); panes[i].hidden = false;
    });
  });

  // Mindestvorgaben je Vorbildung / Lizenzstufe
  var S = $('#ewfv'), seg = $$('#ewfs button');
  if (S && data.vals) {
    seg.forEach(function (b, i) {
      b.addEventListener('click', function () {
        S.innerHTML = data.vals[i].map(function (v) { return '<div class="stat"><b>' + v[0] + '</b><small>' + v[1] + '</small></div>'; }).join('');
        seg.forEach(function (x, j) { x.setAttribute('aria-pressed', j === i ? 'true' : 'false'); });
      });
    });
  }

  // Ausbildungsweg: Gerät + Vorbildung wählen, passende Inhalte zeigen (wie auf der bisherigen Seite)
  var tw = $('#weg');
  if (tw) {
    var dev = null, pri = null, q = new URLSearchParams(location.search);
    var devs = $$('[data-device]', tw), pris = $$('[data-prior]', tw);
    var panel = $('#weg-panel'), row = $('.wdev', tw), home = document.createComment('weg-panel');
    panel.parentNode.insertBefore(home, panel);
    if (devs.some(function (d) { return d.dataset.device === q.get('device'); })) dev = q.get('device');
    if (pris.some(function (d) { return d.dataset.prior === q.get('prior'); })) pri = q.get('prior');
    var mail = $('#weg-mail'), mailBase = mail && mail.getAttribute('href');
    var place = function () {
      var card = dev && $('[data-card="' + dev + '"]', tw);
      var oneCol = row && getComputedStyle(row).gridTemplateColumns.split(' ').length < 2;
      if (card && oneCol) card.parentNode.insertBefore(panel, card.nextSibling);
      else home.parentNode.insertBefore(panel, home.nextSibling);
    };
    var wupd = function (sync) {
      tw.classList.add('ready');
      panel.hidden = !dev;
      $('#weg-result').hidden = !(dev && pri);
      var hint = $('#weg-hint'); if (hint) hint.hidden = !!dev;
      devs.forEach(function (d) {
        var on = d.dataset.device === dev;
        d.setAttribute('aria-pressed', on ? 'true' : 'false');
        d.setAttribute('aria-expanded', on ? 'true' : 'false');
        d.parentNode.classList.toggle('sel', on);
      });
      pris.forEach(function (d) { d.setAttribute('aria-pressed', d.dataset.prior === pri ? 'true' : 'false'); });
      $$('[data-case]', tw).forEach(function (n) { n.hidden = !(dev && pri && (' ' + n.dataset.case + ' ').indexOf(' ' + dev + '-' + pri + ' ') > -1); });
      if (mail && dev && pri) {
        var dl = $('[data-card="' + dev + '"] h3', tw).textContent, pl = $('[data-prior="' + pri + '"] h3', tw).textContent;
        mail.setAttribute('href', mailBase.replace('subject=Mein%20Ausbildungsweg', 'subject=' + encodeURIComponent('Mein Ausbildungsweg – ' + dl + ' / ' + pl)));
      }
      place();
      if (sync !== false && history.replaceState) {
        var u = new URL(location.href);
        dev ? u.searchParams.set('device', dev) : u.searchParams.delete('device');
        pri ? u.searchParams.set('prior', pri) : u.searchParams.delete('prior');
        history.replaceState(null, '', u.href);
      }
    };
    devs.forEach(function (d) { d.addEventListener('click', function () { dev = dev === d.dataset.device ? null : d.dataset.device; wupd(); }); });
    pris.forEach(function (d) { d.addEventListener('click', function () { pri = d.dataset.prior; wupd(); }); });
    var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(place, 120); });
    wupd(false);
  }
})();
