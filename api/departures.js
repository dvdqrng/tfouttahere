// Live departures for one airport for the rest of today (airport local time).
// Data: AeroDataBox via RapidAPI. Set AERODATABOX_KEY in the Vercel project to switch it on.
const HOST = "aerodatabox.p.rapidapi.com";
// Known airport codes; anything else is rejected before it costs an upstream call
const CODES = new Set(require("./_codes.json"));

module.exports = async (req, res) => {
  const code = String((req.query && req.query.iata) || "").toUpperCase();
  if (!/^[A-Z]{3}$/.test(code) || !CODES.has(code)) return res.status(400).json({error: "bad_iata"});
  const key = process.env.AERODATABOX_KEY;
  if (!key) return res.status(503).json({error: "not_configured"});

  const get = async (offset, duration) => {
    const q = new URLSearchParams({offsetMinutes: offset, durationMinutes: duration, direction: "Departure", withLeg: "false",
      withCancelled: "true", withCodeshared: "false", withCargo: "false", withPrivate: "false", withLocation: "false"});
    const r = await fetch(`https://${HOST}/flights/airports/iata/${code}?${q}`, {headers: {"X-RapidAPI-Key": key, "X-RapidAPI-Host": HOST}});
    if (r.status === 204) return [];
    if (!r.ok) { const e = new Error("upstream"); e.status = r.status; throw e; }
    const j = await r.json();
    return j.departures || [];
  };
  const utc = f => Date.parse(String(f.movement?.scheduledTime?.utc || "").replace(" ", "T"));
  const local = f => String(f.movement?.scheduledTime?.local || "");

  try {
    const now = Date.now();
    let list = await get(-20, 720);
    // The airport's UTC offset comes from the local timestamps, e.g. "2026-11-16 14:05+01:00"
    const m = list.map(local).map(s => s.match(/([+-])(\d\d):(\d\d)$/)).find(Boolean);
    const off = m ? (m[1] === "-" ? -1 : 1) * (+m[2] * 60 + +m[3]) * 60e3 : 0;
    const today = new Date(now + off).toISOString().slice(0, 10);
    const toMidnight = 1440 - Math.floor(((now + off) % 864e5) / 60e3);
    if (list.length && toMidnight > 700) list = list.concat(await get(700, Math.min(720, toMidnight - 699)));

    const seen = new Set();
    const flights = list
      .filter(f => local(f).slice(0, 10) === today && utc(f) >= now - 15 * 60e3)
      .map(f => {
        const mv = f.movement || {}, ap = mv.airport || {};
        return {t: local(f).slice(11, 16), u: utc(f), r: String(mv.revisedTime?.local || "").slice(11, 16) || null,
          no: f.number || "", al: f.airline?.name || "", to: ap.iata || "", tn: ap.municipalityName || ap.shortName || ap.name || "",
          st: f.status || "Unknown", term: mv.terminal || "", gate: mv.gate || ""};
      })
      .filter(f => !seen.has(f.no + f.u) && seen.add(f.no + f.u))
      .sort((a, b) => a.u - b.u);
    res.setHeader("Cache-Control", "s-maxage=900, stale-while-revalidate=3600");
    return res.status(200).json({airport: code, today, asOf: new Date(now).toISOString(), flights});
  } catch (e) {
    return res.status(502).json({error: e.status === 429 ? "rate_limited" : e.status === 401 || e.status === 403 ? "bad_key" : "upstream"});
  }
};
