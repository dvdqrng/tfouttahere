# tf outta here

A world map for finding sunny places to travel to: filter destinations by daylight, hours of direct sun, warmth, rain, estimated fare and flight time for your dates.

- **Weather:** the 16-day Open-Meteo forecast for trip days it covers, otherwise the 2022–2025 average for that time of year (ERA5 via Open-Meteo).
- **Fares:** rough estimates from distance and season. Check the Google Flights / Skyscanner links for live prices.
- **Home:** any airport with scheduled service (`data/airports.json`, from OurAirports), or the nearest one to your location.
- **Departures today:** live board from AeroDataBox via `api/departures.js` (website only). Needs the `AERODATABOX_KEY` env var in Vercel:

  ```bash
  vercel env add AERODATABOX_KEY production
  vercel deploy --prod --yes
  ```

- **Map:** Apple Maps (MapKit JS) on the website, with the sunshine drawn on top by a WebGL shader. `api/mapkit.js` signs a short-lived token from a MapKit JS key in your Apple Developer account. Without the three env vars below (and in the standalone `sun-finder.html`) the page falls back to its built-in outline map, with the same shader:

  ```bash
  vercel env add MAPKIT_TEAM_ID production
  vercel env add MAPKIT_KEY_ID production
  vercel env add MAPKIT_PRIVATE_KEY production
  ```

  `MAPKIT_PRIVATE_KEY` is the full contents of the `.p8` file.

## Layout

- `src.html`: the page (markup, styles, script) with data placeholders
- `data/`: climate averages, latest forecast, world map, airports
- `api/departures.js`: Vercel function for the live departures board
- `api/mapkit.js`: Vercel function that issues Apple Maps tokens
- `tools/build.py`: inlines the data, writes `sun-finder.html` and `public/index.html`
- `tools/forecast.py`, `tools/fetch.py`: fetch the forecast and climate averages
- `refresh.sh`: fetch the latest forecast and rebuild

## Update the forecast

```bash
./refresh.sh
```

`public/` is what Vercel serves; push to `main` and it redeploys.
