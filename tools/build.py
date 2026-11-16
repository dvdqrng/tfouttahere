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
page = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<meta name="description" content="Find where the sun is on your dates: sunshine, daylight, weather and rough fares from your airport, plus today\'s departures.">'
        '<meta property="og:title" content="Sun Finder · tfouttahere.com"><meta property="og:type" content="website">'
        '<meta property="og:description" content="Where the sun is on your dates, from your airport.">'
        '<meta property="og:url" content="https://tfouttahere.com/"><meta property="og:image" content="https://tfouttahere.com/og.png">'
        '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
        '<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#16181c">'
        '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
        'body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style></head><body>' + s + '</body></html>')
(root / "public").mkdir(exist_ok=True)
(root / "public" / "index.html").write_text(page)
print("built", root / "sun-finder.html", "and public/index.html")
