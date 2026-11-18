"""Erzeugt den Caddy-Block mit allen alten WordPress-Adressen."""
S = "https://shop.east-westflying.de"
P = lambda h: f"{S}/products/{h}"
C = lambda h: f"{S}/collections/{h}"

# Genaue Adressen (ohne/mit Schrägstrich am Ende)
EXACT = [
    # Seiten der alten WordPress-Seite
    ("/motorschirm-ausbildung", "/motorschirm-ausbildungsweg/"),
    ("/ausbildungspreise", "/motorschirm-ausbildungsweg/"),
    ("/motorschirm-performance-training", "/motorschirm-ausbildungsweg/"),
    ("/fussstarter", "/paramotor-ausbildung-fussstart/"),
    ("/xcitor", "/motorschirm-trike-doppelsitzer/"),
    ("/120-kg-schein-erweiterung", "/motorschirm-trike-doppelsitzer/"),
    ("/trike-2", "/motorschirm-trike/"),
    ("/rundflug-motorschirm", P("rundflug-mit-einem-motorschirm")),
    ("/downloads", "/dulv-formulare-motorschirm/"),
    ("/das-team", "/ueber-mich/"),
    ("/anfahrt-zum-flugplatz", "/kontakt/"),
    ("/east-westflying-shop", S + "/"),
    ("/warenkorb", S + "/"),
    ("/mein-konto", S + "/"),
    ("/kasse", S + "/"),
    ("/widerrufsbelehrung", S + "/policies/refund-policy"),
    ("/versandarten", S + "/"),
    ("/termine", "/"),
    ("/termine/east-westflying-store-schwarmstedt", S + "/"),
    ("/termine/motorschirmausbildung-termine", "/motorschirm-ausbildungsweg/"),
    ("/termine/motorschirmausbildung-termine-2025", "/motorschirm-ausbildungsweg/"),
    ("/termine/termine_motorschirmschulung", "/motorschirm-ausbildungsweg/"),
    ("/termine/italien-toskana-last-minute", "/termine-motorschirmfliegen-in-der-toskana/"),
    ("/termine/motorschirmfliegen-in-the-toskana", "/termine-motorschirmfliegen-in-der-toskana/"),
    ("/fliegen-meistern-durch-neuromentaltraining", "/"),
    ("/jordanien", "/"),
    ("/bilder-und-filme", "/"),
    ("/funk-navigation", "/"),
    ("/elementor-17173", "/"),
    ("/startseite-neu-schule", "/"),
    ("/xc-training-barssel-2019", "/"),
    # Alte Shop-Produkte (Stand der WordPress-Weiterleitungen vom 15.11.2026)
    ("/produkt/scout-paramotor-carbon", P("scout-one-carbon")),
    ("/produkt/scout-moster-atom-paramotor-carbon-enduro", P("scout-one-enduro")),
    ("/produkt/nvolo", C("nvolo-helme")),
    ("/produkt/nvolo-headsets-funk", P("nvolo-headset")),
    ("/produkt/nvolo-visiere", P("nvolo-visier")),
    ("/produkt/nvolo-brillen", P("nvolo-flugbrille")),
    ("/produkt/nvolo-kopfband-fuer-headsets", P("nvolo-kopfbuegel")),
    ("/produkt/nvolo-lynx-kompatible-headsets", C("helm-headsets-funk")),
    ("/produkt/nvolo-funkgeraetekabel", C("helm-kabel")),
    ("/produkt/nvolo-radiokabel-mit-splitter-zur-verbindung-mit-dem-funkgeraet", C("helm-kabel")),
    ("/produkt/nvolo-intercom-cable-to-connect-two-headsets", C("helm-kabel")),
    ("/produkt/rundflug-mit-dem-motorschirm", P("rundflug-mit-einem-motorschirm")),
    ("/produkt/paramotor-parajet-maverick", P("parajet-maverick-evo-1")),
    ("/produkt/paramotor-parajet-maverick-atom80", P("parajet-maverick-evo-1")),
    ("/produkt/paramotor-parajet-maverick-2-atom-80", P("parajet-maverick-3")),
    ("/produkt/custom-colors-parajet", C("parajet")),
    ("/produkt/eclipse-atom80-by-fly-products", C("fly-products")),
    ("/produkt/eclipse-moster-my22-by-fly-products", C("fly-products")),
    ("/produkt/fresh-breeze-vittorazi-moster", C("paramotoren")),
    ("/produkt/off-grid-motorschirm-gasgriff", P("off-grid-aviation-gasgriff-paramotor")),
    ("/produkt/dudek-cabrio", P("dudek-cabrio")),
    ("/produkt/dudek-universal-1-1", P("dudek-universal-1-1")),
    ("/produkt/dudek-universal-1-1-demo-sale", P("dudek-universal-1-1")),
    ("/produkt/dudek-solo", P("dudek-solo-2")),
    ("/produkt/nucleon-4", P("dudek-nucleon-4")),
    ("/produkt/dudek-hadron", C("motorschirme")),
    ("/produkt/dudek-hadron-sale", C("motorschirme")),
    ("/produkt/pegasus_3", C("motorschirme")),
    ("/produkt/vantage-3", C("motorschirme")),
    ("/produkt/airone-pro-unique-single", P("airone-unique-single")),
    ("/produkt/airone-pro-unique-tandem", P("airone-unique-tandem")),
    ("/produkt/airone-pro-trike-phoenix-2", P("airone-phoenix-2")),
    ("/produkt/atom-80-propeller-130m-original-vittorazi-propeller", P("helix-propeller-vittorazi-atom-80")),
    ("/produkt/h31f-125m-atom-80-original-vittorazi-propeller", P("helix-propeller-vittorazi-atom-80")),
    ("/produkt/helix-h30f-122m-l-gml-10-2", C("propeller")),
    ("/produkt/e-props-carbonpropeller-fuer-motorschirm-thor190-hf-getriebe-1283", C("propeller")),
    ("/produkt/gin-gliders-rescue-cockpit", C("rettungsschirme")),
    ("/produkt/frontcontainer-fuer-rettungen", C("rettungsschirme")),
    ("/produkt/evo-cross", C("rettungsschirme")),
    ("/produkt/yeti-ul", C("rettungsschirme")),
    ("/produkt/yeti-light", C("rettungsschirme")),
    ("/produkt/concertina-compress-bag-2", P("gin-concertina-kompressionssack")),
    ("/produkt/gin-gliders-flight-deck-classic", C("zubehoer")),
    ("/produkt/ppg-float", C("zubehoer")),
    ("/produkt/fast-packing-rucksack", C("zubehoer")),
    ("/produkt/gin-gliders-soft-shackle", C("zubehoer")),
    ("/produkt/smart-case", C("zubehoer")),
    ("/produkt/gin-gliders-g-wrap-schlauchtuch", C("zubehoer")),
    ("/produkt/syride-sysnav-xl", S + "/"),
    ("/produkt/syride-sysevolution", S + "/"),
    ("/produkt/icom", C("helm-headsets-funk")),
    ("/produkt/performancetraining", "/motorschirm-ausbildungsweg/"),
    ("/produkt/motorschirmausbildung-so-individuell-wie-du", "/motorschirm-ausbildungsweg/"),
    ("/produkt/motorschirmreise-in-die-toskana", "/termine-motorschirmfliegen-in-der-toskana/"),
    ("/produkt/motorschirmreise-begleitperson-toskana", "/termine-motorschirmfliegen-in-der-toskana/"),
    ("/produkt-kategorie/motoren-trikes/parajet", C("parajet")),
    ("/produkt-kategorie/motoren-trikes/fly_products", C("fly-products")),
    ("/produkt-kategorie/nvolo-helme-und-headsets/nvolo-helme", C("nvolo-helme")),
    ("/produkt-kategorie/nvolo-helme-und-headsets/nvolo-brille", C("helm-brillen")),
    ("/produkt-kategorie/nvolo-helme-und-headsets/nvolo-headset", C("helm-headsets-funk")),
    ("/produkt-kategorie/nvolo-helme-und-headsets/nvolo-visier", C("helm-visiere")),
    ("/produkt-kategorie/nvolo/nvolo-visier", C("helm-visiere")),
    ("/produkt-kategorie/nvolo/nvolo-helme", C("nvolo-helme")),
    ("/produkt-kategorie/nvolo-zubehoer", C("helm-zubehoer-ersatzteile")),
    ("/produkt-kategorie/ppgsmoke", C("zubehoer")),
]
# Ganze Bereiche (Präfix), nach den genauen Adressen geprüft; Reihenfolge zählt
PREFIX = [
    ("/termine/motorschirmfliegen-in-der-toskana*", "/termine-motorschirmfliegen-in-der-toskana/"),
    ("/wp-content/uploads/*", "/dulv-formulare-motorschirm/"),
    ("/das-team/*", "/ueber-mich/"),
    ("/produkt/nvolo-*", C("helme")),
    ("/produkt-kategorie/nvolo*", C("helme")),
    ("/produkt-kategorie/ausruestung*", C("zubehoer")),
    ("/produkt-kategorie/motoren-trikes*", C("paramotoren")),
    ("/produkt-kategorie/helix-propeller*", C("propeller")),
    ("/produkt-kategorie/motorschirme*", C("motorschirme")),
    ("/produkt-kategorie/rettungen*", C("rettungsschirme")),
    ("/produkt-kategorie/*", S + "/"),
    ("/produkt/*", S + "/"),
]

def block():
    srcs = [s for s, _ in EXACT]
    assert len(srcs) == len(set(srcs)), "doppelte Quelle"
    # gleiche Ziele zusammenfassen, Reihenfolge des ersten Auftretens behalten
    groups = {}
    for s, t in EXACT:
        groups.setdefault(t, []).append(s)
    out = ["\t# Alte WordPress-Adressen (Seiten und Shop-Produkte), erzeugt mit tools/redirects.py.",
           "\t# In \"route\" gilt die Reihenfolge: erst genaue Adressen, dann ganze Bereiche.",
           "\troute {"]
    for i, (t, ss) in enumerate(groups.items(), 1):
        paths = " ".join(p for s in ss for p in (s, s + "/"))
        out.append(f"\t\t@alt{i} path {paths}")
        out.append(f"\t\tredir @alt{i} {t} 301")
    for j, (s, t) in enumerate(PREFIX, 1):
        out.append(f"\t\tredir {s} {t} 301")
    out.append("\t}")
    return "\n".join(out) + "\n", len(EXACT), len(PREFIX)

if __name__ == "__main__":
    b, n, m = block()
    print(b); print(n, m)
