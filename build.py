#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Statische sitegenerator voor Health4Ever. Output: ./site (kant-en-klare HTML)."""
import os, shutil, html, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")

SITE = "Health4Ever"
DOMAIN = "health4ever.nl"
BASE = "https://health4ever.nl"
EMAIL = "info@health4ever.nl"
TAGLINE = "Betrouwbare gids voor een gezonder leven"

AUTHOR = {
    "name": "Marit Bakker",
    "role": "Hoofdredacteur Health4Ever",
    "img": "/assets/img/marit.svg",
    "bio": ("Marit Bakker is oprichter en hoofdredacteur van Health4Ever. Ze schrijft al ruim "
            "vijftien jaar over gezondheid, leefstijl en herstel, met een voorliefde voor het "
            "vertalen van wetenschap naar begrijpelijke taal. Voor Health4Ever spreekt ze "
            "regelmatig therapeuten, diëtisten en fysiotherapeuten om te horen wat in de "
            "praktijk echt werkt."),
}

CATS = {
    "beweging":     {"name": "Beweging & Fysio",   "bg": "#e7f3ee", "fg": "#2f8f6b", "ink": "#226b50"},
    "voeding":      {"name": "Voeding & Afvallen",  "bg": "#fdf0e3", "fg": "#e0a458", "ink": "#a9702a"},
    "mentaal":      {"name": "Mentaal welzijn",     "bg": "#eaf0f7", "fg": "#5b7fb0", "ink": "#3f5f8c"},
    "zwangerschap": {"name": "Zwangerschap",        "bg": "#f7eaf1", "fg": "#b0678f", "ink": "#8a4a6d"},
    "leefstijl":    {"name": "Leefstijl",           "bg": "#eef3ea", "fg": "#7a9a5b", "ink": "#5c7742"},
}

NAV = [("Home", "/"), ("Over", "/over/"), ("Nieuws", "/nieuws/"), ("Contact", "/contact/")]

# category line-icons (simple, on transparent, drawn white)
ICONS = {
    "beweging":     '<path d="M28 46h8M64 46h8M36 40v12M64 40v12M36 46h28M30 42v8M70 42v8" stroke="#fff" stroke-width="3.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
    "voeding":      '<path d="M50 30c-9 0-16 8-16 18 0 12 9 22 16 22s16-10 16-22c0-10-7-18-16-18z" fill="none" stroke="#fff" stroke-width="3.4"/><path d="M50 30v-6M50 24c0-4 3-7 7-7" stroke="#fff" stroke-width="3.4" fill="none" stroke-linecap="round"/>',
    "mentaal":      '<path d="M50 28c-11 0-20 8-20 19 0 7 4 12 9 15v8h22v-8c5-3 9-8 9-15 0-11-9-19-20-19z" fill="none" stroke="#fff" stroke-width="3.4" stroke-linejoin="round"/><path d="M42 70h16" stroke="#fff" stroke-width="3.4" stroke-linecap="round"/>',
    "zwangerschap": '<circle cx="50" cy="34" r="7" fill="none" stroke="#fff" stroke-width="3.4"/><path d="M45 46c-4 2-6 7-6 12 0 8 5 14 5 14M55 46c8 2 12 10 12 20" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round"/>',
    "leefstijl":    '<circle cx="50" cy="50" r="10" fill="none" stroke="#fff" stroke-width="3.4"/><path d="M50 26v10M50 64v10M26 50h10M64 50h10M34 34l7 7M66 66l-7-7M66 34l-7 7M34 66l7-7" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/>',
}

def thumb(cat, seed=0):
    c = CATS[cat]
    o1 = 6 + (seed*13) % 22
    o2 = 8 + (seed*7) % 18
    return f'''<svg viewBox="0 0 100 62" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
<rect width="100" height="62" fill="{c['bg']}"/>
<circle cx="{18+o1}" cy="{50-o2}" r="34" fill="{c['fg']}" opacity=".16"/>
<circle cx="{78-o2}" cy="{14+o1//2}" r="22" fill="{c['fg']}" opacity=".2"/>
<g transform="translate(25,3) scale(0.5)">{ICONS[cat]}</g>
</svg>'''

def hero_art(cat):
    c = CATS[cat]
    return f'''<svg viewBox="0 0 100 62" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
<rect width="100" height="62" fill="{c['bg']}"/>
<circle cx="24" cy="46" r="40" fill="{c['fg']}" opacity=".14"/>
<circle cx="82" cy="12" r="26" fill="{c['fg']}" opacity=".2"/>
<g transform="translate(28,6) scale(0.62)">{ICONS[cat]}</g>
</svg>'''

LOGO_SVG = ('<svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="23" fill="#e7f3ee"/>'
            '<path d="M24 35.5c-.5 0-1-.18-1.38-.52C17.3 30.2 13 26.4 13 21.7c0-3.15 2.42-5.7 5.5-5.7 '
            '1.9 0 3.7.96 4.75 2.5l.75 1.08.75-1.08A5.72 5.72 0 0 1 29.5 16c3.08 0 5.5 2.55 5.5 5.7 0 '
            '4.7-4.3 8.5-9.62 13.28-.38.34-.88.52-1.38.52z" fill="#2f8f6b"/>'
            '<path d="M15.5 24.2h4.1l1.7-3.4 2.9 6.2 2-3.9h5.8" fill="none" stroke="#fff" '
            'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>')

def brandmark(cls="brand"):
    return f'<a class="{cls}" href="/">{LOGO_SVG}<span>Health<b>4</b>Ever</span></a>'

def nav_html(active):
    items = ""
    for label, href in NAV:
        cl = ' class="active"' if href == active else ""
        items += f'<li><a href="{href}"{cl}>{label}</a></li>'
    return f'''<header class="site-header"><div class="wrap nav">
{brandmark()}
<button class="nav-toggle" aria-label="Menu" aria-expanded="false" onclick="var m=document.getElementById('nav');m.classList.toggle('open');this.setAttribute('aria-expanded',m.classList.contains('open'))"><span></span><span></span><span></span></button>
<ul class="nav-links" id="nav">{items}</ul>
</div></header>'''

def footer_html():
    year = 2026
    return f'''<footer class="site-footer"><div class="wrap">
<div class="foot-grid">
<div>
<div class="foot-brand">{LOGO_SVG}<span>Health<b>4</b>Ever</span></div>
<p style="max-width:34em">Health4Ever is een onafhankelijke gezondheidsgids. We bundelen praktische, goed onderbouwde informatie over voeding, beweging en mentaal welzijn, en verwijzen naar therapeuten en specialisten die er in de praktijk mee werken.</p>
</div>
<div>
<h5>Ontdek</h5>
<ul class="foot-links">
<li><a href="/">Home</a></li>
<li><a href="/over/">Over Health4Ever</a></li>
<li><a href="/nieuws/">Nieuws &amp; artikelen</a></li>
<li><a href="/contact/">Contact</a></li>
</ul>
</div>
<div>
<h5>Juridisch</h5>
<ul class="foot-links">
<li><a href="/privacybeleid/">Privacybeleid</a></li>
<li><a href="/cookiebeleid/">Cookiebeleid</a></li>
<li><a href="/disclaimer/">Disclaimer</a></li>
<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
</ul>
</div>
</div>
<div class="foot-bottom">
<span>&copy; {year} Health4Ever. Alle rechten voorbehouden.</span>
<span>Informatie op deze site vervangt geen medisch advies.</span>
</div>
</div></footer>'''

def page(title, desc, body, active="/", path="/", og_type="website", extra_head=""):
    canonical = BASE + path
    full_title = title if title == SITE else f"{title} | {SITE}"
    doc = f'''<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="nl_NL">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#2f8f6b">
<link rel="icon" href="/assets/img/logo.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/css/style.css">
{extra_head}
</head>
<body>
{nav_html(active)}
<main>
{body}
</main>
{footer_html()}
</body>
</html>'''
    return doc

def write(path, content):
    """path like '/over/' -> site/over/index.html ; '/' -> site/index.html"""
    if path == "/":
        fp = os.path.join(OUT, "index.html")
    else:
        fp = os.path.join(OUT, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)

def fmt_date(d):
    months = ["januari","februari","maart","april","mei","juni","juli","augustus","september","oktober","november","december"]
    return f"{d.day} {months[d.month-1]} {d.year}"


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------
from content_articles import ARTICLES

ARTICLES_SORTED = sorted(ARTICLES, key=lambda a: a["date"], reverse=True)

CAT_DESC = {
    "beweging":"Fysiotherapie, oefentherapie en alles over houding, herstel en verstandig bewegen.",
    "voeding":"Gezond eten, afvallen zonder jojo-effect en praktische kennis over voeding.",
    "mentaal":"Stress, ontspanning, haptotherapie en de verbinding tussen lichaam en geest.",
    "zwangerschap":"Begeleiding, beleving en gezondheid rond zwangerschap en de periode erna.",
    "leefstijl":"Slaap, energie en dagelijkse gewoonten die op de lange termijn het verschil maken.",
}

def url_for(a):
    return f"/nieuws/{a['slug']}/"

def post_card(a, seed=0):
    c = CATS[a["cat"]]
    return f'''<article class="post">
<a href="{url_for(a)}" class="thumb" aria-label="{html.escape(a['title'])}">{thumb(a['cat'], seed)}</a>
<div class="body">
<a class="chip" href="/nieuws/{a['cat']}/">{c['name']}</a>
<h3><a href="{url_for(a)}">{html.escape(a['title'])}</a></h3>
<p>{html.escape(a['excerpt'])}</p>
<div class="meta"><img src="{AUTHOR['img']}" alt="{AUTHOR['name']}" width="30" height="30"><span>{AUTHOR['name']} &middot; {a['mins']} min lezen</span></div>
</div>
</article>'''

def render_home():
    latest = ARTICLES_SORTED[:6]
    cards = "".join(post_card(a, i) for i, a in enumerate(latest))
    cat_cards = ""
    icon_emoji = {"beweging":"Beweging","voeding":"Voeding","mentaal":"Mentaal","zwangerschap":"Zwangerschap","leefstijl":"Leefstijl"}
    for key, c in CATS.items():
        cat_cards += f'''<a class="card" href="/nieuws/{key}/" style="text-decoration:none">
<div class="ico" style="background:{c['bg']}"><svg viewBox="0 0 100 100" width="26" height="26" style="fill:none">{ICONS[key].replace('#fff', c['fg'])}</svg></div>
<h3 style="color:var(--ink)">{c['name']}</h3>
<p>{CAT_DESC[key]}</p>
</a>'''
    body = f'''
<section class="hero"><div class="wrap hero-inner">
<div>
<p class="eyebrow">Gezondheidsgids</p>
<h1>Grip op gezondheid, in begrijpelijke taal</h1>
<p class="lead">Health4Ever bundelt praktische, goed onderbouwde informatie over voeding, beweging en mentaal welzijn. Zonder hypes, wel met aandacht voor wat in de praktijk werkt.</p>
<div class="btn-row">
<a class="btn" href="/nieuws/">Lees de artikelen</a>
<a class="btn btn-ghost" href="/over/">Over Health4Ever</a>
</div>
</div>
<div class="hero-art">{hero_art('beweging')}</div>
</div></section>

<section><div class="wrap">
<div class="section-head center">
<p class="eyebrow">Waar Health4Ever voor staat</p>
<h2 class="mt0">Een gids, geen verkooppraatje</h2>
</div>
<div class="grid grid-3">
<div class="card"><div class="ico">&#10003;</div><h3>Onderbouwd</h3><p>De informatie is gebaseerd op gangbare inzichten uit de praktijk van therapeuten, di&euml;tisten en fysiotherapeuten, vertaald naar heldere taal.</p></div>
<div class="card"><div class="ico">&#9670;</div><h3>Praktisch</h3><p>Geen abstracte theorie, maar bruikbare kennis: wat klachten veroorzaakt, wat helpt en wanneer professionele hulp verstandig is.</p></div>
<div class="card"><div class="ico">&#9788;</div><h3>Onafhankelijk</h3><p>Health4Ever verkoopt zelf niets. Waar een specialist of praktijk relevant is, volgt een eerlijke verwijzing met de volledige bron.</p></div>
</div>
</div></section>

<section class="section-soft"><div class="wrap">
<div class="section-head center">
<p class="eyebrow">Thema's</p>
<h2 class="mt0">Ontdek per onderwerp</h2>
</div>
<div class="grid grid-3">{cat_cards}</div>
</div></section>

<section><div class="wrap">
<div class="section-head center">
<p class="eyebrow">Nieuws</p>
<h2 class="mt0">Nieuwste artikelen</h2>
</div>
<div class="posts">{cards}</div>
<div class="center" style="margin-top:36px"><a class="btn btn-ghost" href="/nieuws/">Alle artikelen bekijken</a></div>
</div></section>

<section class="section-soft"><div class="wrap">
<div class="persona">
<div class="pic">{persona_svg()}</div>
<div>
<p class="eyebrow">De redactie</p>
<h2 class="mt0">Geschreven door Marit Bakker</h2>
<p class="lead-muted">{html.escape(AUTHOR['bio'])}</p>
<a class="btn btn-ghost" href="/over/">Meer over Health4Ever</a>
</div>
</div>
</div></section>
'''
    return page(SITE, f"{SITE}: {TAGLINE}. Praktische, onderbouwde artikelen over voeding, beweging, mentaal welzijn en gezond leven.", body, active="/", path="/")

def persona_svg():
    return f'<img src="{AUTHOR["img"]}" alt="Illustratie van {AUTHOR["name"]}, {AUTHOR["role"]}" width="240" height="240" style="border-radius:20px;background:#fff">'

def render_over():
    body = f'''
<section class="cat-hero"><div class="wrap narrow center">
<p class="eyebrow">Over Health4Ever</p>
<h1 class="mt0">Een betrouwbare gids voor een gezonder leven</h1>
<p class="lead-muted">Health4Ever is ontstaan uit een eenvoudige overtuiging: goede gezondheidsinformatie hoort begrijpelijk, eerlijk en vrij toegankelijk te zijn.</p>
</div></section>

<section><div class="wrap narrow">
<h2>Wat Health4Ever is</h2>
<p>Health4Ever is een onafhankelijk online platform over gezondheid en leefstijl. Waar veel informatie online versnipperd is of vooral bedoeld om iets te verkopen, brengt Health4Ever betrouwbare kennis samen op &eacute;&eacute;n plek. De onderwerpen lopen uiteen van voeding en afvallen tot beweging, herstel, mentaal welzijn en zwangerschap.</p>
<p>Het uitgangspunt is steeds hetzelfde: complexe gezondheidsthema's vertalen naar taal die iedereen begrijpt, zonder de nuance te verliezen. Geen loze beloften of wondermiddelen, maar heldere uitleg over hoe het lichaam werkt en wat er in de praktijk aan klachten gedaan kan worden.</p>

<h2>Hoe de redactie werkt</h2>
<p>De artikelen komen tot stand door bestaande inzichten uit de gezondheidszorg te combineren met wat therapeuten en behandelaars in hun dagelijkse praktijk zien werken. Waar een specifieke praktijk, therapievorm of specialist relevant is voor het onderwerp, verwijst Health4Ever daar transparant naar, altijd met de volledige bron erbij zodat iedereen zelf verder kan kijken.</p>
<p>Health4Ever verkoopt zelf geen producten of behandelingen. Dat maakt het mogelijk om onderwerpen nuchter te benaderen en de lezer voorop te stellen in plaats van een verkoopdoel.</p>

<div class="callout"><p><strong>Belangrijk om te weten.</strong> De informatie op Health4Ever is algemeen van aard en bedoeld ter ori&euml;ntatie. Ze vervangt geen persoonlijk advies van een arts of behandelaar. Bij aanhoudende of ernstige klachten is een bezoek aan de huisarts altijd de eerste stap.</p></div>

<h2>De thema's</h2>
<p>De inhoud is verdeeld over vaste thema's, zodat elk onderwerp makkelijk te vinden is: <a href="/nieuws/beweging/">Beweging &amp; Fysio</a>, <a href="/nieuws/voeding/">Voeding &amp; Afvallen</a>, <a href="/nieuws/mentaal/">Mentaal welzijn</a>, <a href="/nieuws/zwangerschap/">Zwangerschap</a> en <a href="/nieuws/leefstijl/">Leefstijl</a>.</p>
</div></section>

<section class="section-soft"><div class="wrap narrow">
<div class="authorbox" style="max-width:none">
{persona_svg().replace('width="240" height="240"','width="82" height="82"').replace('border-radius:20px','border-radius:50%')}
<div>
<p class="eyebrow mt0">Hoofdredacteur</p>
<h4>{AUTHOR['name']}</h4>
<p>{html.escape(AUTHOR['bio'])}</p>
</div>
</div>
<div class="center" style="margin-top:34px"><a class="btn" href="/contact/">Neem contact op</a></div>
</div></section>
'''
    return page("Over Health4Ever", "Health4Ever is een onafhankelijke gezondheidsgids die betrouwbare, begrijpelijke informatie over voeding, beweging en welzijn samenbrengt.", body, active="/over/", path="/over/")

def render_contact():
    body = f'''
<section class="cat-hero"><div class="wrap narrow center">
<p class="eyebrow">Contact</p>
<h1 class="mt0">Vragen of een tip?</h1>
<p class="lead-muted">Health4Ever is bereikbaar via e-mail. Voor vragen, suggesties voor onderwerpen of opmerkingen over een artikel volstaat een bericht.</p>
</div></section>
<section><div class="wrap">
<div class="contact-card">
<p class="eyebrow mt0">Stuur een bericht naar</p>
<a class="mail" href="mailto:{EMAIL}">{EMAIL}</a>
<p style="margin-top:22px;color:var(--muted)">Berichten worden doorgaans binnen enkele werkdagen beantwoord. Health4Ever geeft geen persoonlijk medisch advies via e-mail; bij gezondheidsklachten is de huisarts het juiste aanspreekpunt.</p>
</div>
</div></section>
'''
    return page("Contact", f"Neem contact op met Health4Ever via {EMAIL} voor vragen, suggesties of opmerkingen.", body, active="/contact/", path="/contact/")

def render_nieuws_index(cat=None):
    if cat:
        items = [a for a in ARTICLES_SORTED if a["cat"] == cat]
        c = CATS[cat]
        title = c["name"]
        desc = CAT_DESC[cat]
        path = f"/nieuws/{cat}/"
        heading = c["name"]
    else:
        items = ARTICLES_SORTED
        title = "Nieuws & artikelen"
        desc = "Alle artikelen van Health4Ever over voeding, beweging, mentaal welzijn, zwangerschap en leefstijl."
        path = "/nieuws/"
        heading = "Nieuws &amp; artikelen"
    # filter bar
    fb = f'<a href="/nieuws/" class="{"active" if not cat else ""}">Alles</a>'
    for key, cc in CATS.items():
        fb += f'<a href="/nieuws/{key}/" class="{"active" if cat==key else ""}">{cc["name"]}</a>'
    cards = "".join(post_card(a, i) for i, a in enumerate(items))
    body = f'''
<section class="cat-hero"><div class="wrap center">
<p class="eyebrow">{'Thema' if cat else 'Nieuws'}</p>
<h1 class="mt0">{heading}</h1>
<p class="lead-muted" style="max-width:44em;margin-left:auto;margin-right:auto">{html.escape(desc)}</p>
<div class="filterbar">{fb}</div>
</div></section>
<section><div class="wrap">
<div class="posts">{cards}</div>
</div></section>
'''
    ptitle = title if cat else SITE + " nieuws"
    return page(title if cat else "Nieuws & artikelen", desc, body, active="/nieuws/", path=path)

def render_article(a):
    c = CATS[a["cat"]]
    related = [x for x in ARTICLES_SORTED if x["cat"] == a["cat"] and x["slug"] != a["slug"]][:3]
    if len(related) < 3:
        extra = [x for x in ARTICLES_SORTED if x["slug"] != a["slug"] and x not in related]
        related += extra[:3-len(related)]
    rel_cards = "".join(post_card(x, i) for i, x in enumerate(related))
    disclaimer = ('<div class="disclaimer-box"><b>Let op:</b> dit artikel is algemeen informatief en vervangt geen '
                  'medisch advies. Bij aanhoudende of ernstige klachten is een bezoek aan de huisarts of een '
                  'gespecialiseerde behandelaar de juiste stap.</div>')
    schema = f'''<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":{__import_json(a['title'])},"datePublished":"{a['date'].isoformat()}","author":{{"@type":"Person","name":"{AUTHOR['name']}"}},"publisher":{{"@type":"Organization","name":"{SITE}"}},"mainEntityOfPage":"{BASE}{url_for(a)}"}}</script>'''
    body = f'''
<article class="article"><div class="wrap">
<div class="article-head">
<p class="eyebrow" style="margin-bottom:14px"><a href="/nieuws/{a['cat']}/" style="text-decoration:none">{c['name']}</a></p>
<h1 class="mt0">{html.escape(a['title'])}</h1>
<div class="byline">
<img src="{AUTHOR['img']}" alt="{AUTHOR['name']}" width="48" height="48">
<div class="who"><b>{AUTHOR['name']}</b><span>{fmt_date(a['date'])} &middot; {a['mins']} min lezen</span></div>
</div>
</div>
</div>
<div class="wrap"><div class="hero-art" style="max-width:900px;margin:0 auto 10px;padding:0;overflow:hidden;border-radius:18px">{hero_art(a['cat'])}</div></div>
<div class="wrap"><div class="prose">
{a['body'].strip()}
{disclaimer}
<div class="authorbox">
<img src="{AUTHOR['img']}" alt="{AUTHOR['name']}" width="82" height="82">
<div><h4>{AUTHOR['name']}</h4><p>{html.escape(AUTHOR['bio'])}</p></div>
</div>
</div></div>
<div class="wrap"><div class="related">
<h2>Meer uit deze thema's</h2>
<div class="posts">{rel_cards}</div>
</div></div>
</article>
'''
    return page(a["title"], a["excerpt"], body, active="/nieuws/", path=url_for(a), og_type="article", extra_head=schema)

def __import_json(s):
    import json
    return json.dumps(s, ensure_ascii=False)

def render_legal(slug, title, desc, inner):
    body = f'''
<section class="cat-hero"><div class="wrap narrow center">
<h1 class="mt0">{title}</h1>
</div></section>
<section><div class="wrap"><div class="prose">
{inner}
</div></div></section>
'''
    return page(title, desc, body, active="/", path=f"/{slug}/")


PRIVACY = """
<p><em>Laatst bijgewerkt: juli 2026.</em></p>
<p>Health4Ever hecht waarde aan de privacy van bezoekers. Dit privacybeleid legt uit welke gegevens de website verwerkt en met welk doel. Health4Ever gaat zorgvuldig met gegevens om en houdt zich aan de Algemene Verordening Gegevensbescherming (AVG).</p>
<h2>Welke gegevens worden verwerkt</h2>
<p>Health4Ever is een informatieve website zonder registratie, account of bestelmogelijkheid. De website bevat geen contactformulier, nieuwsbriefinschrijving of andere invoervelden waarin persoonsgegevens worden gevraagd. Er worden dan ook geen persoonsgegevens via de website verzameld of opgeslagen.</p>
<h2>Contact via e-mail</h2>
<p>Wie zelf contact opneemt via het e-mailadres info@health4ever.nl, deelt daarmee een e-mailadres en de inhoud van het bericht. Deze gegevens worden uitsluitend gebruikt om de betreffende vraag of opmerking te beantwoorden en worden niet voor andere doeleinden ingezet of aan derden verstrekt.</p>
<h2>Cookies en statistieken</h2>
<p>Health4Ever plaatst geen tracking- of marketingcookies en maakt geen gebruik van analysediensten die bezoekers volgen. Meer daarover staat in het <a href="/cookiebeleid/">cookiebeleid</a>.</p>
<h2>Externe links</h2>
<p>De website verwijst naar websites van derden, zoals praktijken en specialisten. Health4Ever is niet verantwoordelijk voor de inhoud of het privacybeleid van die externe websites. Het is verstandig om het privacybeleid van een website te raadplegen die via een link wordt bezocht.</p>
<h2>Rechten</h2>
<p>Iedereen heeft het recht om te vragen welke persoonsgegevens Health4Ever verwerkt en om deze te laten corrigeren of verwijderen. Aangezien de website zelf geen persoonsgegevens verzamelt, beperkt dit zich in de praktijk tot correspondentie die per e-mail is gedeeld. Een verzoek kan worden gestuurd naar info@health4ever.nl.</p>
<h2>Wijzigingen</h2>
<p>Dit privacybeleid kan worden aangepast wanneer de website of de regelgeving daartoe aanleiding geeft. De actuele versie staat altijd op deze pagina.</p>
"""

COOKIES = """
<p><em>Laatst bijgewerkt: juli 2026.</em></p>
<p>Dit cookiebeleid legt uit hoe Health4Ever omgaat met cookies en vergelijkbare technieken.</p>
<h2>Gebruikt Health4Ever cookies?</h2>
<p>Health4Ever plaatst geen tracking-, analyse- of marketingcookies. De website is bewust zo opgezet dat bezoekers niet gevolgd worden en dat er geen gegevens naar externe partijen worden gestuurd voor advertentie- of statistiekdoeleinden. Ook lettertypen en afbeeldingen worden vanaf de eigen website geladen, zodat er geen verzoeken naar externe servers nodig zijn.</p>
<h2>Waarom geen cookiemelding</h2>
<p>Omdat er geen cookies worden geplaatst die toestemming vereisen, toont de website geen cookiemelding. Dat is een bewuste keuze: minder ruis voor de bezoeker en volledige privacy.</p>
<h2>Externe links</h2>
<p>Wanneer een bezoeker via een link doorklikt naar een andere website, gelden daar de cookieregels en het beleid van die website. Health4Ever heeft daar geen invloed op en raadt aan het beleid van de betreffende website te raadplegen.</p>
<h2>Vragen</h2>
<p>Voor vragen over dit cookiebeleid is Health4Ever bereikbaar via info@health4ever.nl.</p>
"""

DISCLAIMER = """
<p><em>Laatst bijgewerkt: juli 2026.</em></p>
<h2>Algemeen</h2>
<p>De informatie op Health4Ever is met zorg samengesteld en bedoeld voor algemene voorlichting over gezondheid en leefstijl. Ondanks de zorgvuldigheid kan Health4Ever niet garanderen dat alle informatie te allen tijde volledig, actueel en juist is.</p>
<h2>Geen medisch advies</h2>
<p>De artikelen op Health4Ever vervangen geen persoonlijk advies, diagnose of behandeling door een arts, fysiotherapeut, di&euml;tist of andere gekwalificeerde zorgverlener. Bij gezondheidsklachten, twijfel of vragen over de eigen situatie is het altijd verstandig om een professional te raadplegen. Bij aanhoudende of ernstige klachten is de huisarts het eerste aanspreekpunt.</p>
<h2>Verwijzingen naar derden</h2>
<p>Health4Ever verwijst in sommige artikelen naar praktijken, therapeuten of producten van derden. Deze verwijzingen zijn informatief bedoeld. Health4Ever is niet verantwoordelijk voor de dienstverlening, producten of informatie van deze externe partijen, en een verwijzing houdt geen garantie of goedkeuring in van een specifieke behandeling of resultaat.</p>
<h2>Aansprakelijkheid</h2>
<p>Het gebruik van de informatie op Health4Ever is voor eigen rekening en risico. Health4Ever aanvaardt geen aansprakelijkheid voor schade die voortvloeit uit het gebruik van of het vertrouwen op de informatie op deze website.</p>
<h2>Auteursrecht</h2>
<p>De teksten en illustraties op Health4Ever mogen niet zonder toestemming worden overgenomen. Voor vragen hierover is Health4Ever bereikbaar via info@health4ever.nl.</p>
"""

NOTFOUND_BODY = """
<section class="cat-hero"><div class="wrap narrow center">
<p class="eyebrow">Foutmelding 404</p>
<h1 class="mt0">Deze pagina bestaat niet</h1>
<p class="lead-muted">De opgevraagde pagina is verplaatst of bestaat niet meer.</p>
<div class="btn-row" style="justify-content:center;margin-top:10px">
<a class="btn" href="/">Naar de homepage</a>
<a class="btn btn-ghost" href="/nieuws/">Bekijk de artikelen</a>
</div>
</div></section>
"""

def build_sitemap():
    urls = ["/", "/over/", "/nieuws/", "/contact/", "/privacybeleid/", "/cookiebeleid/", "/disclaimer/"]
    urls += [f"/nieuws/{k}/" for k in CATS]
    dated = {}
    for a in ARTICLES:
        u = url_for(a)
        urls.append(u)
        dated[u] = a["date"].isoformat()
    today = "2026-07-24"
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lm = dated.get(u, today)
        pr = "1.0" if u == "/" else ("0.8" if u.startswith("/nieuws/") and u.count("/")==3 else "0.6")
        out.append(f"  <url><loc>{BASE}{u}</loc><lastmod>{lm}</lastmod><priority>{pr}</priority></url>")
    out.append("</urlset>")
    return "\n".join(out)

def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)
    # copy static assets from source dir
    shutil.copytree(os.path.join(ROOT, "assets_src"), os.path.join(OUT, "assets"))
    write("/", render_home())
    write("/over/", render_over())
    write("/contact/", render_contact())
    write("/nieuws/", render_nieuws_index())
    for k in CATS:
        write(f"/nieuws/{k}/", render_nieuws_index(k))
    for a in ARTICLES:
        write(url_for(a), render_article(a))
    write("/privacybeleid/", render_legal("privacybeleid", "Privacybeleid", "Privacybeleid van Health4Ever: welke gegevens worden verwerkt en hoe Health4Ever met privacy omgaat.", PRIVACY))
    write("/cookiebeleid/", render_legal("cookiebeleid", "Cookiebeleid", "Cookiebeleid van Health4Ever. De website plaatst geen tracking- of marketingcookies.", COOKIES))
    write("/disclaimer/", render_legal("disclaimer", "Disclaimer", "Disclaimer van Health4Ever. De informatie is algemeen en vervangt geen medisch advies.", DISCLAIMER))
    # 404
    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as f:
        f.write(page("Pagina niet gevonden", "Deze pagina bestaat niet.", NOTFOUND_BODY, active="", path="/404.html"))
    # sitemap + robots + headers
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(build_sitemap())
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % BASE)
    with open(os.path.join(OUT, "_headers"), "w", encoding="utf-8") as f:
        f.write("/*\n  X-Content-Type-Options: nosniff\n  X-Frame-Options: SAMEORIGIN\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: geolocation=(), microphone=(), camera=()\n\n/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n")
    print("Gegenereerd:", sum(len(files) for _,_,files in os.walk(OUT)), "bestanden")

if __name__ == "__main__":
    main()
