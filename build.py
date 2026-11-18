#!/usr/bin/env python3
"""Baut die statische East-Westflying-Seite aus Bausteinen zusammen.

  python3 build.py preview   -> dist/preview  (relative Links, noindex, für Vorschau/Testadresse)
  python3 build.py live      -> dist/live     (saubere Adressen wie bisher, indexierbar)

Eine neue Seite: Datei in src/pages anlegen und unten in PAGES eintragen.
"""
import hashlib, html, json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://east-westflying.de"

# Besucherstatistik (Umami, ohne Cookies). Die ID steht in Umami unter
# Einstellungen > Websites. Leer = Statistik aus.
UMAMI_ID = "da9a7a2d-8a28-4c75-b0b6-f7f44137fe72"
UMAMI_DOMAINS = "east-westflying.de,www.east-westflying.de,neu.east-westflying.de"

# Klicks, die als Anfrage gezählt werden (Name des Ereignisses in Umami)
EVENTS = [("tel:", "Anruf"), ("mailto:", "E-Mail"), ("calendly.com", "Termin"), ("wa.me", "WhatsApp")]

# slug = Adresse wie auf der bisherigen Seite ("" = Startseite)
def P(slug, src, title, desc, crumb=None, ogtype="article", **kw):
    return dict(slug=slug, src=src, title=title, desc=desc, crumb=crumb, ogtype=ogtype, **kw)


PAGES = [
    P("", "home.html", "Motorschirm-Flugschule Hannover | East-Westflying",
      "Gleitschirm mit Motor fliegen lernen: Motorschirm-Flugschule am Flugplatz Hodenhagen bei Hannover. Fußstart oder Trike, 1:1 betreut. Schnuppern ab 399 €.",
      ogtype="website"),
    P("paramotor-ausbildung-fussstart", "fussstart.html", "Paramotor-Ausbildung im Fußstart bei Hannover | East-Westflying",
      "Paramotor-Schein im Fußstart: persönliche 1:1-Ausbildung am Flugplatz Hodenhagen bei Hannover. Ablauf, Voraussetzungen, Anrechnung und Kosten auf einen Blick.",
      "Paramotor-Ausbildung im Fußstart"),
    P("motorschirm-trike", "trike.html", "Motorschirm-Trike fliegen lernen: Einsitzer-Ausbildung",
      "Motorschirm-Trike fliegen lernen auf dem Einsitzer bis 120 kg, am Flugplatz Hodenhagen bei Hannover. Ablauf, Lizenz, Kosten und Ausrüstung auf einen Blick.",
      "Motorschirm-Trike Einsitzer"),
    P("motorschirm-trike-doppelsitzer", "doppelsitzer.html", "Motorschirm-Trike 2-Sitzer (z. B. XCitor): Ausbildung",
      "Doppelsitzer-Trike wie den XCitor fliegen lernen: Lizenz, Passagierberechtigung, Ablauf und Kosten. Trike über die Flugschule kaufen, mit Rabatt.",
      "Motorschirm-Trike Doppelsitzer"),
    P("motorschirm-ausbildungsweg", "ausbildungsweg.html", "Paramotor-Schein: Ausbildung zum Motorschirm-Flugschein",
      "Flugschein für den Gleitschirm mit Motor: im Fußstart, auf dem Einsitzer- oder Doppelsitzer-Trike. Welcher Weg zu dir passt, Ablauf und Voraussetzungen.",
      "Dein Ausbildungsweg"),
    P("ewf-one", "ewf-one.html", "EWF_ONE – Deine exklusive Motorschirm-Ausbildung | East-Westflying",
      "Deine Motorschirm-Ausbildung mit exklusiver 1:1-Betreuung: ein Schüler, ein Fluglehrer, 30 Tage Fokus. Bewirb dich für deinen EWF_ONE-Ausbildungsmonat.",
      "EWF_ONE"),
    P("termine-motorschirmfliegen-in-der-toskana", "toskana.html", "Motorschirmreise Toskana 2027: Fliegerlager im Frühjahr | East-Westflying",
      "Motorschirmreise und Fliegerlager in der Toskana, April 2027: zwei feste Reiseblöcke, Unterkunft direkt am Flugplatz Castiglion Fiorentino, Preise und FAQ.",
      "Motorschirmreise Toskana"),
    P("popopropeller-podcast", "podcast.html", "Popopropeller Podcast: Paramotor-Ratgeber zum Hören | East-Westflying",
      "Der deutschsprachige Paramotor-Podcast mit Björn Lürßen und Florian Rauls: Ausbildung, Technik, Sicherheit und Fly-Ins in 17 Folgen. Direkt hier anhören.",
      "Popopropeller Podcast"),
    P("reflexprofil-motorschirm", "reflex.html", "Reflexprofil beim Motorschirm: Trimmer, Speedbar, Bremsen | East-Westflying",
      "Shownotes zur Popopropeller-Folge mit Udo Hülscher: Wie ein Reflexprofil funktioniert, wie du es richtig fliegst und wo seine Grenzen liegen. Mit 8 Szenarien.",
      "Reflexprofil beim Motorschirm"),
    P("propeller-motorschirm", "propeller.html", "Propeller am Motorschirm: 2-Blatt oder 3-Blatt? | East-Westflying",
      "Shownotes zur Popopropeller-Folge mit Björn Souren von Helix: 2-Blatt oder 3-Blatt, groß oder klein, Auswahl, Pflege und Schäden am Paramotor-Propeller.",
      "Propeller am Motorschirm"),
    P("gleitschirm-mit-motor", "gleitschirm-mit-motor.html", "Gleitschirm mit Motor: Schein, Kosten & Ablauf erklärt",
      "Paragleiter mit Motor einfach erklärt: wie ein Motorschirm fliegt, Fußstart oder Trike, welchen Flugschein du brauchst und was Motorschirmfliegen kostet.",
      "Gleitschirm mit Motor"),
    P("dulv-formulare-motorschirm", "dulv.html", "DULV-Formulare für die Motorschirm-Ausbildung | East-Westflying",
      "Die DULV-Formulare für die Motorschirm-Lizenz auf einen Blick: Ausbildungsmeldung, Grundausbildung Doppelsitzer, Antrag auf Lizenz und Mitgliedschaft.",
      "DULV-Formulare"),
    P("ueber-mich", "ueber-mich.html", "Björn Lürßen – Motorschirm-Fluglehrer | East-Westflying",
      "Björn Lürßen fliegt seit 2008, ist seit 2011 Motorschirm-Fluglehrer und hat rund 200 Schüler ausgebildet. Flugschule am Flugplatz Hodenhagen bei Hannover.",
      "Über mich"),
    P("kontakt", "kontakt.html", "East-Westflying Kontakt – Dein persönlicher Kontakt",
      "East-Westflying Kontakt: Fragen zur Motorschirm-Ausbildung, zum Schnuppertraining oder Rundflug? Buche dein Telefondate oder schreibe mir eine E-Mail.",
      "Kontakt"),
    P("impressum", "impressum.html", "Impressum | East-Westflying", "Impressum von East-Westflying, Motorschirm-Flugschule am Flugplatz Hodenhagen.", "Impressum"),
    P("datenschutzerklaerung", "datenschutz.html", "Datenschutzerklärung | East-Westflying", "Datenschutzerklärung von East-Westflying.", "Datenschutzerklärung"),
    P("sitemap", "sitemap.html", "Sitemap | East-Westflying", "Alle Seiten von East-Westflying auf einen Blick.", "Sitemap"),
]
MIGRATED = {p["slug"] for p in PAGES}

ORG = {
    "@type": ["School", "Organization"], "@id": SITE + "/#organization", "name": "East-Westflying",
    "url": SITE + "/", "email": "info@east-westflying.de", "telephone": "+4915778959694",
    "sameAs": ["https://www.facebook.com/eastwestflying"],
    "address": {"@type": "PostalAddress", "addressLocality": "Schwarmstedt", "postalCode": "29690", "addressCountry": "DE"},
}


def read(p):
    return (ROOT / "src" / p).read_text(encoding="utf-8")


def jsonld(page, body):
    url = SITE + "/" + (page["slug"] + "/" if page["slug"] else "")
    graph = [ORG, {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "East-Westflying",
                   "inLanguage": "de", "publisher": {"@id": SITE + "/#organization"}},
             {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": page["title"],
              "description": page["desc"], "inLanguage": "de", "isPartOf": {"@id": SITE + "/#website"}}]
    if page["slug"]:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Startseite", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": page["crumb"], "item": url}]})
    faq = re.findall(r"<details[^>]*><summary><h3>(.*?)</h3></summary><p>(.*?)</p></details>", body, re.S)
    if faq:
        strip = lambda s: html.unescape(re.sub(r"<[^>]+>", "", s)).strip()
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faq]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


def track(doc):
    """Zählskript einsetzen und Kontakt-Links als Ereignis markieren."""
    if UMAMI_ID:
        tag = (f'<script defer src="/s.js" data-website-id="{UMAMI_ID}" '
               f'data-domains="{UMAMI_DOMAINS}"></script>\n</head>')
        doc = doc.replace("</head>", tag, 1)

    def mark(m):
        a = m.group(0)
        if "data-umami-event" in a:
            return a
        for needle, name in EVENTS:
            if needle in m.group(1):
                return a[:2] + f' data-umami-event="{name}"' + a[2:]
        return a
    return re.sub(r'<a\b[^>]*\bhref="([^"]*)"[^>]*>', mark, doc)


def build(mode):
    out = ROOT / "dist" / mode
    shutil.rmtree(out, ignore_errors=True)
    shutil.copytree(ROOT / "assets", out / "assets")
    head, header, footer = read("partials/head.html"), read("partials/header.html"), read("partials/footer.html")

    for page in PAGES:
        depth = 1 if page["slug"] else 0
        rel = "../" * depth

        def url(slug):
            if slug not in MIGRATED:          # noch nicht umgezogen: zeigt auf die bisherige Seite
                return f"{SITE}/{slug}/"
            if mode == "live":
                return "/" + (slug + "/" if slug else "")
            return rel + (slug + "/index.html" if slug else "index.html")

        body = read("pages/" + page["src"])
        if page["src"] == "sitemap.html":
            body = body.replace("{{LIST}}", "".join(
                f'<li><a href="{("{{X:" + p["slug"] + "}}") if p["slug"] else "{{HOME}}"}">{html.escape(p["crumb"] or "Startseite")}</a></li>'
                for p in PAGES if p["slug"] != "sitemap"))
        for _ in range(3):
            body = re.sub(r"\{\{INC:([\w-]+)\}\}", lambda m: read("partials/" + m.group(1) + ".html"), body)
            body = re.sub(r"\{\{W:([\w-]+)\}\}", lambda m: read("widgets/" + m.group(1) + ".html"), body)
        doc = head + header + body + footer
        home = url("")
        rep = {
            "{{TITLE}}": html.escape(page["title"]), "{{DESC}}": html.escape(page["desc"]),
            "{{CANON}}": SITE + "/" + (page["slug"] + "/" if page["slug"] else ""),
            "{{OGTYPE}}": page["ogtype"],
            "{{ROBOTS}}": "index, follow, max-image-preview:large" if mode == "live" else "noindex, nofollow",
            "{{BODYATTR}}": "" if mode == "live" else " data-preview",
            "{{JSONLD}}": jsonld(page, body).replace("</", "<\\/"),
            "{{A}}": ("/" if mode == "live" else rel) + "assets/",
            "{{HOME}}": home, "{{H}}": "" if not page["slug"] else home, "{{YEAR}}": "2026",
            "{{FUSS}}": url("paramotor-ausbildung-fussstart"),
        }
        for k, v in rep.items():
            doc = doc.replace(k, v)
        # Versionsnummer an CSS/JS hängen, damit Browser nach Änderungen nicht die alte Fassung nutzen
        for f in ("css/site.css", "js/site.js"):
            h = hashlib.md5((ROOT / "assets" / f).read_bytes()).hexdigest()[:8]
            doc = doc.replace(f + '"', f + "?v=" + h + '"')
        doc = re.sub(r"\{\{X:([\w-]+)\}\}", lambda m: url(m.group(1)), doc)
        old_links = sorted(set(re.findall(r'href="(?:https://east-westflying\.de)?/(?!assets/)([\w-]+)/"', doc)) - MIGRATED)
        if old_links:
            print(f"  Hinweis {page['src']}: Links ohne neue Seite: {old_links}")
        doc = track(doc)
        left = re.findall(r"\{\{[^}]*\}\}", doc)
        assert not left, f"Platzhalter offen in {page['src']}: {left}"
        target = out / page["slug"] / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(doc, encoding="utf-8")
        print(f"{mode}: {target.relative_to(ROOT)}  ({len(doc) / 1024:.0f} KB)")

    if mode == "live":
        urls = "".join(f"<url><loc>{SITE}/{p['slug'] + '/' if p['slug'] else ''}</loc></url>" for p in PAGES)
        (out / "sitemap.xml").write_text(
            f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>',
            encoding="utf-8")
        (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")


if __name__ == "__main__":
    for m in (sys.argv[1:] or ["preview", "live"]):
        build(m)
