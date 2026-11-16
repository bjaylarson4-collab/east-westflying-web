#!/usr/bin/env python3
"""Baut die statische East-Westflying-Seite aus Bausteinen zusammen.

  python3 build.py preview   -> dist/preview  (relative Links, noindex, für Vorschau/Testadresse)
  python3 build.py live      -> dist/live     (saubere Adressen wie bisher, indexierbar)

Eine neue Seite: Datei in src/pages anlegen und unten in PAGES eintragen.
"""
import html, json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://east-westflying.de"

# Besucherstatistik (Umami, ohne Cookies). Die ID steht in Umami unter
# Einstellungen > Websites. Leer = Statistik aus.
UMAMI_ID = ""
UMAMI_DOMAINS = "east-westflying.de,www.east-westflying.de,neu.east-westflying.de"

# Klicks, die als Anfrage gezählt werden (Name des Ereignisses in Umami)
EVENTS = [("tel:", "Anruf"), ("mailto:", "E-Mail"), ("calendly.com", "Termin"), ("wa.me", "WhatsApp")]

# slug = Adresse wie auf der bisherigen Seite ("" = Startseite)
PAGES = [
    dict(slug="", src="home.html", ogtype="website",
         title="Motorschirm & Paramotor Flugschule bei Hannover | East-Westflying",
         desc="Motorschirm fliegen lernen bei Hannover: Ausbildung im Fußstart oder Trike am Flugplatz Hodenhagen, persönlich 1:1 betreut. Schnuppertraining & Rundflug."),
    dict(slug="paramotor-ausbildung-fussstart", src="fussstart.html", ogtype="article",
         title="Paramotor-Ausbildung im Fußstart bei Hannover | East-Westflying",
         desc="Paramotor-Schein im Fußstart: persönliche 1:1-Ausbildung am Flugplatz Hodenhagen bei Hannover. Ablauf, Voraussetzungen, Anrechnung und Kosten auf einen Blick.",
         crumb="Paramotor-Ausbildung im Fußstart"),
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
            "{{HOME}}": home, "{{H}}": "" if not page["slug"] else home,
            "{{FUSS}}": url("paramotor-ausbildung-fussstart"),
        }
        for k, v in rep.items():
            doc = doc.replace(k, v)
        doc = re.sub(r"\{\{X:([\w-]+)\}\}", lambda m: url(m.group(1)), doc)
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
