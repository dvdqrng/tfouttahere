// Airline logo by IATA code, fetched on the server so visitors' browsers never contact the logo host,
// and served from this site so the page can read its colours. Cached at the edge for a month.
module.exports = async (req, res) => {
  const c = String((req.query && req.query.c) || "").toUpperCase();
  if (!/^[A-Z0-9]{2}$/.test(c)) return res.status(400).end();
  try {
    const r = await fetch(`https://pics.avs.io/240/80/${c}.png`);
    const type = r.headers.get("content-type") || "";
    if (!r.ok || !type.startsWith("image/")) return res.status(404).end();
    res.setHeader("Content-Type", type);
    res.setHeader("Cache-Control", "public, s-maxage=2592000, max-age=86400, stale-while-revalidate=604800");
    res.status(200).send(Buffer.from(await r.arrayBuffer()));
  } catch (e) { res.status(502).end(); }
};
