// Scheduled departures from (or with dir=arr, arrivals into) one airport on one day, airport local time.
// One answer per airport and day, so every destination from the same home airport shares it at the edge.
// Data: AeroDataBox via RapidAPI, the same AERODATABOX_KEY as the live board. Two 12-hour calls make a day.
const HOST = "aerodatabox.p.rapidapi.com";
const CODES = new Set(require("./_codes.json"));

module.exports = async (req, res) => {
  const code = String((req.query && req.query.iata) || "").toUpperCase(), date = String((req.query && req.query.date) || "");
  const arr = String((req.query && req.query.dir) || "") === "arr";
  if (!/^[A-Z]{3}$/.test(code) || !CODES.has(code)) return res.status(400).json({error: "bad_iata"});
  // Today up to a year ahead; anything else is rejected before it costs an upstream call
  const day = Date.parse(date + "T00:00:00Z"), now = Date.now();
  if (!/^\d{4}-\d\d-\d\d$/.test(date) || !(day > now - 2 * 864e5) || day > now + 360 * 864e5) return res.status(400).json({error: "bad_date"});
  const key = process.env.AERODATABOX_KEY;
  if (!key) return res.status(503).json({error: "not_configured"});

  const get = async (from, to) => {
    const q = new URLSearchParams({direction: arr ? "Arrival" : "Departure", withLeg: "true", withCancelled: "false", withCodeshared: "false",
      withCargo: "false", withPrivate: "false", withLocation: "false"});
    const r = await fetch(`https://${HOST}/flights/airports/iata/${code}/${date}T${from}/${date}T${to}?${q}`, {headers: {"X-RapidAPI-Key": key, "X-RapidAPI-Host": HOST}});
    if (r.status === 204) return [];
    if (!r.ok) { const e = new Error("upstream"); e.status = r.status; throw e; }
    const j = await r.json();
    return (arr ? j.arrivals : j.departures) || [];
  };
  const hm = t => String((t && t.local) || "").slice(11, 16);
  const ymd = t => String((t && t.local) || "").slice(0, 10);

  try {
    const list = (await Promise.all([get("00:00", "11:59"), get("12:00", "23:59")])).flat();
    const seen = new Set();
    const flights = list.map(f => {
      // With legs, each flight carries both ends: where it leaves (local time there) and where it lands (local time there)
      const dp = f.departure || {}, ar = f.arrival || {}, d0 = ymd(dp.scheduledTime), d1 = ymd(ar.scheduledTime);
      const at = hm(ar.scheduledTime), plus = at && d0 && d1 > d0 ? Math.round((Date.parse(d1) - Date.parse(d0)) / 864e5) : 0;
      return {t: hm(dp.scheduledTime), a: at || null, p: plus || 0, no: f.number || "", al: (f.airline && f.airline.name) || "",
        from: arr ? (dp.airport && dp.airport.iata) || "" : code, to: arr ? code : (ar.airport && ar.airport.iata) || "", term: (arr ? ar : dp).terminal || ""};
    }).filter(f => f.t && f.from && f.to && !seen.has(f.no + f.t) && seen.add(f.no + f.t)).sort((a, b) => a.t < b.t ? -1 : a.t > b.t ? 1 : 0);
    // Schedules move slowly; a day's answer is good for hours, and closer to the day it refreshes more often
    const soon = day - now < 3 * 864e5;
    res.setHeader("Cache-Control", `public, s-maxage=${soon ? 3600 : 21600}, stale-while-revalidate=86400`);
    return res.status(200).json({airport: code, date, dir: arr ? "arr" : "dep", flights});
  } catch (e) {
    return res.status(502).json({error: e.status === 429 ? "rate_limited" : e.status === 401 || e.status === 403 ? "bad_key" : e.status === 400 ? "out_of_range" : "upstream"});
  }
};
