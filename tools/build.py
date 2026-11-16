"""Assemble sun-finder.html from src.html plus the map, climate and forecast data."""
import pathlib
root = pathlib.Path(__file__).resolve().parent.parent
d = root / "data"
s = (root / "src.html").read_text()
for marker, f in [("/*WORLD*/null", "countries-110m.json"), ("/*CLIMATE*/[]", "climate.json"), ("/*FORECAST*/{d: {}}", "forecast.json"), ("/*AIRPORTS*/[]", "airports.json")]:
    assert marker in s, marker
    s = s.replace(marker, (d / f).read_text())
(root / "sun-finder.html").write_text(s)
# Standalone copy for the website (Vercel serves public/); the artifact host adds this skeleton itself
# The website serves fonts and scripts itself, so visitors talk to no third party; the artifact keeps the CDN links
site = s
for cdn, local in [
    ('<link rel="preconnect" href="https://fonts.googleapis.com">\n', ''),
    ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500;600&display=swap">',
     '<link rel="stylesheet" href="/fonts/fonts.css">'),
    ('https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js', '/vendor/d3-7.9.0.min.js'),
    ('https://cdnjs.cloudflare.com/ajax/libs/topojson/3.0.2/topojson.min.js', '/vendor/topojson-3.0.2.min.js')]:
    assert cdn in site, cdn
    site = site.replace(cdn, local)
page = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<meta name="description" content="Find where the sun is on your dates: sunshine, daylight, weather and rough fares from your airport, plus today\'s departures.">'
        '<meta property="og:title" content="tf outta here"><meta property="og:type" content="website">'
        '<meta property="og:description" content="Sunshine, weather and rough fares for every sunny place you can fly to on your dates, plus today\'s departures from your airport.">'
        '<meta property="og:site_name" content="tf outta here"><meta property="og:locale" content="en_GB">'
        '<meta property="og:url" content="https://tfouttahere.com/"><meta property="og:image" content="https://tfouttahere.com/og-card.png"><meta property="og:image:type" content="image/png">'
        '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
        '<meta property="og:image:alt" content="tf outta here: a boarding pass from Berlin to Luxor with 10.6 hours of sun a day, over a map of sunshine zones">'
        '<meta name="twitter:title" content="tf outta here"><meta name="twitter:description" content="Where the sun is on your dates, from your airport.">'
        '<meta name="twitter:image" content="https://tfouttahere.com/og-card.png">'
        '<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#16181c">'
        '<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/svg+xml" href="/favicon.svg">'
        '<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">'
        '<link rel="apple-touch-icon" href="/apple-touch-icon.png">'
        '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
        'body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style></head><body>' + site + '</body></html>')
(root / "public").mkdir(exist_ok=True)
# The departures API only pays for lookups of real airports
import json
codes = sorted({a[0] for a in json.loads((d / "airports.json").read_text())})
(root / "api" / "_codes.json").write_text(json.dumps(codes, separators=(",", ":")))
(root / "public" / "index.html").write_text(page)
print("built", root / "sun-finder.html", "and public/index.html")
