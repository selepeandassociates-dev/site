#!/usr/bin/env python3
"""Static page builder for the Selepe & Associates Inc site.

Each file in src/pages/ holds only the <main> content. The first line is a
metadata comment:  <!-- title: Page title | desc: Meta description -->
This script wraps every page in the shared <head>, header and footer and writes
the finished HTML next to this script's parent folder (the site root).

Run:  python3 src/build.py     (or  npm run build  to also compile Tailwind)
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "src" / "pages"

SITE = {
    "name": "Selepe & Associates Inc",
    "tagline": "Above and Beyond Legal Services",
    "url": "https://www.selepe.co",
    "phone": "076 984 8560",
    "phone_href": "+27769848560",
    "wa_number": "27769848560",
    "email": "info@selepe.co",
    "address": "1300 Umabu Str and Koekoekvalk, Soshanguve East, 0152",
    "region": "City of Tshwane, Gauteng, South Africa",
    "reg": "2026/894017/21",
}

# ----------------------------------------------------------------------------
# Icons (24px line icons, drawn with currentColor)
# ----------------------------------------------------------------------------
ICONS = {
    "scales": '<path d="M12 3v17M7 20h10M4 7h16"/><path d="M4 7l-2.5 7a3.5 3.5 0 0 0 5 0L4 7zM20 7l-2.5 7a3.5 3.5 0 0 0 5 0L20 7z"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6l8-3z"/><path d="M8.5 12l2.5 2.5L16 9.5"/>',
    "building": '<path d="M4 21V4h10v17M14 9h6v12M2 21h20M8 8h2M8 12h2M8 16h2"/>',
    "users": '<path d="M16 20v-1a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v1"/><circle cx="10" cy="8" r="3"/><path d="M20 20v-1a3 3 0 0 0-2-2.8M16 5.2a3 3 0 0 1 0 5.6"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
    "bulb": '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/>',
    "gavel": '<path d="M13 5l6 6M9 9l6 6M3.5 20.5L10 14M11 3L7 7l7 7 4-4-7-7z"/>',
    "filepen": '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9l-6-6z"/><path d="M14 3v6h6M8 13h8M8 17h5"/>',
    "home": '<path d="M3 11l9-8 9 8M5 10v10h14V10M10 20v-6h4v6"/>',
    "coins": '<ellipse cx="12" cy="6" rx="8" ry="3"/><path d="M4 6v6c0 1.7 3.6 3 8 3s8-1.3 8-3V6M4 12v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><circle cx="12" cy="12" r="7"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14"/><path d="M3 7l9 6 9-6"/>',
    "pin": '<path d="M12 21s7-6.2 7-11a7 7 0 0 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "chart": '<path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 5-6"/>',
    "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9L12 3z"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "headset": '<path d="M4 14v-2a8 8 0 0 1 16 0v2"/><path d="M4 14h3v5H5a1 1 0 0 1-1-1v-4zM20 14h-3v5h2a1 1 0 0 0 1-1v-4z"/>',
    "book": '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2V5z"/><path d="M4 19a2 2 0 0 0 2 2h13"/>',
    "briefcase": '<rect x="3" y="8" width="18" height="12"/><path d="M9 8V5h6v3M3 13h18"/>',
    "layers": '<path d="M12 3l9 5-9 5-9-5 9-5z"/><path d="M3 13l9 5 9-5"/>',
    "check": '<path d="M5 12l5 5 9-10"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6L6 18"/>',
    "chevron": '<path d="M6 9l6 6 6-6"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "lock": '<rect x="5" y="11" width="14" height="10"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    "handshake": '<path d="M3 11l4-4 4 2 3-2 7 6"/><path d="M3 11l5 6a2 2 0 0 0 3 0M11 17l2 2a2 2 0 0 0 3 0l4-5M7 7L3 11M21 12l-3 3"/>',
    "chat": '<path d="M3 21l1.7-5A8.5 8.5 0 1 1 8 19.3L3 21z"/>',
    "doc": '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9l-6-6z"/><path d="M14 3v6h6"/>',
    "cap": '<path d="M2 9l10-5 10 5-10 5L2 9z"/><path d="M6 11.5V16c0 1.5 2.7 3 6 3s6-1.5 6-3v-4.5M22 9v6"/>',
    "tower": '<path d="M5 21V8l7-5 7 5v13M2 21h20M9 12h2M13 12h2M9 16h2M13 16h2"/>',
    "scale-up": '<path d="M4 20V10M10 20V6M16 20v-8M22 20V3M2 20h20"/>',
}


def icon(name, cls="h-6 w-6"):
    body = ICONS[name]
    return (
        f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>'
    )


# ----------------------------------------------------------------------------
# Navigation
# ----------------------------------------------------------------------------
MAIN_NAV = [
    ("index.html", "Home"),
    ("about.html", "About"),
    ("services.html", "Legal Services"),
    ("subscriptions.html", "Subscriptions"),
    ("corporate.html", "Corporate"),
    ("industries.html", "Industries"),
]
MORE_NAV = [
    ("how-we-work.html", "How We Work"),
    ("academy.html", "LEAP Academy"),
    ("leadership.html", "Leadership & Governance"),
]
CONTACT = ("contact.html", "Contact")


def nav_link(href, label, current, extra=""):
    cur = ' aria-current="page"' if href == current else ""
    return f'<a href="{href}" class="nav-link {extra}"{cur}>{label}</a>'


def header(current):
    desktop = "\n".join(nav_link(h, l, current) for h, l in MAIN_NAV)
    more_active = " text-white" if current in [h for h, _ in MORE_NAV] else ""
    more_items = "\n".join(
        f'<a href="{h}" class="block px-5 py-3 text-sm text-silver-200 hover:bg-navy-800 hover:text-gold-300"'
        f'{" aria-current=page" if h == current else ""}>{l}</a>'
        for h, l in MORE_NAV
    )
    mobile = "\n".join(
        f'<a href="{h}" class="block border-b border-white/10 py-3 text-base text-silver-100 hover:text-gold-300"'
        f'{" aria-current=page" if h == current else ""}>{l}</a>'
        for h, l in MAIN_NAV + MORE_NAV + [CONTACT]
    )
    return f"""
<a href="#main" class="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-[60] focus:bg-gold-400 focus:px-4 focus:py-2 focus:text-navy-950">Skip to content</a>
<header id="site-header" class="fixed inset-x-0 top-0 z-50 border-b border-white/5 bg-navy-950/85 backdrop-blur-md transition-colors duration-300">
  <div class="wrap flex h-[4.5rem] items-center justify-between gap-6">
    <a href="index.html" class="flex items-center gap-3" aria-label="Selepe &amp; Associates Inc – home">
      <img src="img/logo-sm.png" alt="" width="44" height="44" class="h-11 w-11 rounded-full">
      <span class="leading-none">
        <span class="block font-display text-[0.95rem] font-medium tracking-wider text-white sm:text-base">SELEPE &amp; ASSOCIATES <span class="text-gold-400">INC</span></span>
        <span class="mt-1 hidden whitespace-nowrap text-[0.54rem] font-medium uppercase tracking-[0.26em] text-gold-400 sm:block">Above and Beyond Legal Services</span>
      </span>
    </a>
    <nav class="hidden items-center gap-6 xl:flex" aria-label="Main">
      {desktop}
      <div class="group relative">
        <button type="button" class="nav-link inline-flex items-center gap-1{more_active}" aria-haspopup="true">More {icon("chevron", "h-3.5 w-3.5")}</button>
        <div class="invisible absolute right-0 top-full w-60 translate-y-1 border border-white/10 bg-navy-900 py-2 opacity-0 shadow-lift transition group-hover:visible group-hover:translate-y-0 group-hover:opacity-100 group-focus-within:visible group-focus-within:translate-y-0 group-focus-within:opacity-100">
          {more_items}
        </div>
      </div>
      {nav_link(*CONTACT, current)}
    </nav>
    <div class="flex items-center gap-3">
      <a href="contact.html" class="btn-gold hidden !px-5 !py-2.5 text-[0.8rem] md:inline-flex">Request a Consultation {icon("arrow", "h-4 w-4")}</a>
      <button id="menu-btn" type="button" class="p-2 text-white xl:hidden" aria-expanded="false" aria-controls="mobile-menu" aria-label="Open menu">{icon("menu", "h-7 w-7")}</button>
    </div>
  </div>
  <div id="mobile-menu" class="hidden max-h-[calc(100vh-4.5rem)] overflow-y-auto border-t border-white/10 bg-navy-950 xl:hidden">
    <div class="wrap py-4">
      {mobile}
      <a href="contact.html" class="btn-gold mt-5 w-full">Request a Consultation {icon("arrow", "h-4 w-4")}</a>
    </div>
  </div>
</header>
"""


def footer():
    explore = "\n".join(
        f'<li><a href="{h}" class="text-sm text-silver-300 transition hover:text-gold-300">{l}</a></li>'
        for h, l in MAIN_NAV + MORE_NAV + [CONTACT]
    )
    wa = f"https://wa.me/{SITE['wa_number']}?text=Hello%20Selepe%20%26%20Associates%2C%20I%27d%20like%20to%20make%20an%20enquiry."
    return f"""
<a href="{wa}" target="_blank" rel="noopener" aria-label="Chat with us on WhatsApp"
   class="fixed bottom-5 right-5 z-40 grid h-14 w-14 place-items-center rounded-full bg-[#25D366] text-white shadow-lift transition hover:scale-105">
  {icon("chat", "h-7 w-7")}
</a>
<footer class="on-dark relative overflow-hidden bg-navy-950 text-silver-300">
  <div class="motif absolute inset-0 opacity-60" aria-hidden="true"></div>
  <div class="gold-line absolute inset-x-0 top-0 h-px"></div>
  <div class="wrap relative grid gap-12 py-16 md:grid-cols-12">
    <div class="md:col-span-5">
      <a href="index.html" class="flex items-center gap-4">
        <img src="img/logo-sm.png" alt="" width="64" height="64" class="h-16 w-16 rounded-full">
        <span>
          <span class="block font-display text-lg tracking-wider text-white">SELEPE &amp; ASSOCIATES <span class="text-gold-400">INC</span></span>
          <span class="mt-1 block text-[0.6rem] font-medium uppercase tracking-[0.3em] text-gold-400">Above and Beyond Legal Services</span>
        </span>
      </a>
      <p class="mt-6 max-w-md text-sm leading-relaxed">Attorneys, conveyancers, notaries, litigators and external legal operations partners. Legal solutions, business support and recovery expertise under one accountable partnership.</p>
    </div>
    <div class="md:col-span-3">
      <h3 class="eyebrow-dark eyebrow !font-sans">Explore</h3>
      <ul class="mt-5 space-y-2.5">{explore}</ul>
    </div>
    <div class="md:col-span-4">
      <h3 class="eyebrow-dark eyebrow !font-sans">Get in touch</h3>
      <ul class="mt-5 space-y-4 text-sm">
        <li class="flex gap-3"><span class="mt-0.5 text-gold-400">{icon("phone", "h-5 w-5")}</span><a href="tel:{SITE['phone_href']}" class="hover:text-gold-300">{SITE['phone']}</a></li>
        <li class="flex gap-3"><span class="mt-0.5 text-gold-400">{icon("mail", "h-5 w-5")}</span><a href="mailto:{SITE['email']}" class="hover:text-gold-300">{SITE['email']}</a></li>
        <li class="flex gap-3"><span class="mt-0.5 text-gold-400">{icon("globe", "h-5 w-5")}</span><a href="{SITE['url']}" class="hover:text-gold-300">www.selepe.co</a></li>
        <li class="flex gap-3"><span class="mt-0.5 text-gold-400">{icon("pin", "h-5 w-5")}</span><span>{SITE['address']}<br>{SITE['region']}</span></li>
      </ul>
    </div>
  </div>
  <div class="relative border-t border-white/10">
    <div class="wrap flex flex-col gap-3 py-6 text-xs text-silver-400 md:flex-row md:items-center md:justify-between">
      <p>&copy; <span data-year>2026</span> Selepe &amp; Associates Inc. All rights reserved. Reg. No. {SITE['reg']}</p>
      <p class="max-w-xl md:text-right">The information on this website is general in nature and is not legal advice. Fees and plan content are subject to a written agreement with each client.</p>
    </div>
  </div>
</footer>
"""


def head(title, desc, filename):
    full_title = f"{title} | {SITE['name']}" if filename != "index.html" else f"{SITE['name']} | {SITE['tagline']}"
    canonical = f"{SITE['url']}/" if filename == "index.html" else f"{SITE['url']}/{filename}"
    jsonld = f"""{{
  "@context": "https://schema.org",
  "@type": "LegalService",
  "name": "{SITE['name']}",
  "slogan": "{SITE['tagline']}",
  "url": "{SITE['url']}",
  "telephone": "+27 76 984 8560",
  "email": "{SITE['email']}",
  "address": {{"@type": "PostalAddress", "streetAddress": "{SITE['address']}", "addressLocality": "Tshwane", "addressRegion": "Gauteng", "addressCountry": "ZA"}},
  "areaServed": "ZA"
}}"""
    return f"""<!doctype html>
<html lang="en-ZA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0c1b3f">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{desc}">
<link rel="icon" type="image/png" href="img/logo-sm.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;1,500;1,600&family=Inter:wght@400;500;600&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/tailwind.css">
<script>document.documentElement.classList.add('js')</script>
<script type="application/ld+json">{jsonld}</script>
</head>
<body>
"""


def tail():
    return '<script src="assets/site.js" defer></script>\n</body>\n</html>\n'


CTA = """
<section class="on-dark motif relative overflow-hidden bg-navy-900 py-16 sm:py-20">
  <div class="wrap flex flex-col items-start justify-between gap-8 lg:flex-row lg:items-center">
    <div>
      <p class="eyebrow">Let&rsquo;s talk</p>
      <h2 class="h-section mt-3 max-w-xl">Judge us by what we deliver.</h2>
      <p class="lead mt-3 max-w-xl">Start with a single plan, a single matter or a proof of concept on part of your portfolio. There is no obligation to extend the relationship afterwards.</p>
    </div>
    <div class="flex flex-wrap gap-4">
      <a href="contact.html" class="btn-gold">Request a Consultation {{icon:arrow:h-4 w-4}}</a>
      <a href="tel:{{phone_href}}" class="btn-outline-light">{{icon:phone:h-4 w-4}} {{phone}}</a>
    </div>
  </div>
</section>
"""


def render_tokens(html):
    html = html.replace("{{cta}}", CTA)
    def repl(m):
        name, cls = m.group(1), m.group(2)
        return icon(name, cls) if cls else icon(name)

    html = re.sub(r"\{\{icon:([a-z0-9-]+)(?::([^}]*))?\}\}", repl, html)
    for k, v in SITE.items():
        html = html.replace("{{" + k + "}}", v)
    return html


def build():
    META = re.compile(r"<!--\s*title:\s*(.*?)\s*\|\s*desc:\s*(.*?)\s*-->")
    for src in sorted(PAGES.glob("*.html")):
        text = src.read_text(encoding="utf-8")
        m = META.match(text)
        if not m:
            raise SystemExit(f"{src.name}: missing '<!-- title: ... | desc: ... -->' first line")
        title, desc = m.group(1), m.group(2)
        body = text[m.end():].strip()
        out = (
            head(title, desc, src.name)
            + header(src.name)
            + '<main id="main">\n'
            + render_tokens(body)
            + "\n</main>\n"
            + footer()
            + tail()
        )
        (ROOT / src.name).write_text(out, encoding="utf-8")
        print("built", src.name)


if __name__ == "__main__":
    build()
