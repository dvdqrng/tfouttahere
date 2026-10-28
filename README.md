# Sun Finder

A world map for finding sunny places to travel to: filter destinations by daylight, hours of direct sun, warmth, rain, estimated fare and flight time for your dates.

- **Weather:** the 16-day Open-Meteo forecast for trip days it covers, otherwise the 2022–2025 average for that time of year (ERA5 via Open-Meteo).
- **Fares:** rough estimates from distance and season. Check the Google Flights / Skyscanner links for live prices.

## Layout

- `src.html`: the page (markup, styles, script) with data placeholders
- `data/`: climate averages, latest forecast, world map
- `tools/build.py`: inlines the data, writes `sun-finder.html` and `public/index.html`
- `tools/forecast.py`, `tools/fetch.py`: fetch the forecast and climate averages
- `refresh.sh`: fetch the latest forecast and rebuild

## Update the forecast

```bash
./refresh.sh
```

`public/` is what Vercel serves; push to `main` and it redeploys.
