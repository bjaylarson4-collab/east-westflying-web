/* East-Westflying – kleines Skript für Menü, Podcast, Video und die Bausteine der Fußstart-Seite. */
(function () {
  var preview = document.body.hasAttribute('data-preview');

  // Mobiles Menü
  var mb = document.getElementById('menu-btn'), mn = document.getElementById('mnav');
  if (mb && mn) {
    mb.addEventListener('click', function () {
      var open = mn.classList.toggle('open');
      mb.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    mn.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { mn.classList.remove('open'); mb.setAttribute('aria-expanded', 'false'); }
    });
  }

  // Podcast: ein gemeinsamer Player für alle Folgen
  var player = document.getElementById('pod-player');
  document.querySelectorAll('.eps button').forEach(function (b) {
    b.addEventListener('click', function () {
      if (!player) return;
      var same = player.getAttribute('src') === b.dataset.src;
      document.querySelectorAll('.eps button').forEach(function (x) { x.classList.remove('on'); x.textContent = '▶ Anhören'; });
      if (same && !player.paused) { player.pause(); return; }
      if (!same) player.src = b.dataset.src;
      player.hidden = false;
      b.classList.add('on'); b.textContent = '❚❚ Pause';
      var p = player.play(); if (p && p.catch) p.catch(function () {});
    });
  });

  // Video: erst nach Klick laden (keine Verbindung zu YouTube vorher)
  var yt = document.querySelector('.yt');
  if (yt && !preview) {
    yt.addEventListener('click', function (e) {
      e.preventDefault();
      yt.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + yt.dataset.yt +
        '?autoplay=1" title="Deine Motorschirmreise in die Toskana" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>';
    });
  }

  // Fußstart: Quick-Check
  var res = document.getElementById('ewfr');
  if (res) {
    var st = {}, contact = res.dataset.contact;
    document.querySelectorAll('#ewfq .chk').forEach(function (c) {
      c.addEventListener('click', function () {
        var on = c.getAttribute('aria-pressed') !== 'true';
        c.setAttribute('aria-pressed', on ? 'true' : 'false');
        st[c.dataset.k] = on; upd();
      });
    });
    var upd = function () {
      var t, x;
      if (st.knie) { t = 'Eher Trike'; x = 'Wenn Knie oder Rücken nicht mitmachen, ist das Einsitzer-Trike die entspanntere Wahl: Du startest im Sitzen auf Rädern. Sprich mich gern an.'; }
      else if (st.pax && !st.fit) { t = 'Schau dir das Doppelsitzer-Trike an'; x = 'Mit dem Doppelsitzer-Trike nimmst du am einfachsten jemanden mit. Tandem im Fußstart ist zwar nicht ausgeschlossen, aber deutlich komplizierter: Meist brauchst du dafür einen stärkeren Motor und/oder einen größeren Schirm.'; }
      else if (st.fit || st.mobil) { t = 'Fußstart passt'; x = 'Mobil, kompakt und ursprünglich: Der Fußstart ist genau dein Ding.' + (st.pax ? ' Jemanden mitnehmen geht im Fußstart grundsätzlich auch, ist aber deutlich komplizierter: Meist brauchst du dafür einen stärkeren Motor und/oder einen größeren Schirm. Einfacher geht das mit dem Doppelsitzer-Trike.' : ''); }
      else { t = 'Tipp etwas an'; x = 'Dann bekommst du eine erste Einschätzung.'; }
      res.innerHTML = '<strong>' + t + '</strong>' + x + ' <a href="' + contact + '">Lass uns sprechen</a>';
    };
  }

  // Fußstart: Ablauf-Etappen
  var tabs = document.querySelectorAll('#ewft .tab'), panes = document.querySelectorAll('#ablauf .pane');
  tabs.forEach(function (b, i) {
    b.addEventListener('click', function () {
      tabs.forEach(function (x) { x.setAttribute('aria-selected', 'false'); });
      panes.forEach(function (x) { x.hidden = true; });
      b.setAttribute('aria-selected', 'true'); panes[i].hidden = false;
    });
  });

  // Fußstart: Mindestvorgaben je Vorbildung
  var S = document.getElementById('ewfv'), seg = document.querySelectorAll('#ewfs button');
  if (S) {
    var V = [
      [['40', 'Starts und Landungen (mindestens)'], ['4', 'Flugtage (mindestens)'], ['3', 'Überlandflüge, je 1 h oder 30 km']],
      [['20', 'Starts und Landungen (mindestens)'], ['2', 'Flugtage (mindestens)'], ['3', 'Überlandflüge, je 1 h oder 30 km']],
      [['40', 'Starts und Landungen (mindestens)'], ['3', 'Überlandflüge, je 1 h oder 30 km'], ['?', 'Anrechnung klären wir persönlich']]
    ];
    seg.forEach(function (b, i) {
      b.addEventListener('click', function () {
        S.innerHTML = V[i].map(function (v) { return '<div class="stat"><b>' + v[0] + '</b><small>' + v[1] + '</small></div>'; }).join('');
        seg.forEach(function (x, j) { x.setAttribute('aria-pressed', j === i ? 'true' : 'false'); });
      });
    });
  }
})();
