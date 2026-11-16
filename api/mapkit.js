// Short-lived Apple Maps (MapKit JS) token for the map on the site.
// Set MAPKIT_TEAM_ID, MAPKIT_KEY_ID and MAPKIT_PRIVATE_KEY (the .p8 contents) in the Vercel project to switch it on.
// The key stays on the server; each token is good for 30 minutes and only on the site it was issued for.
const crypto = require("crypto");
const SITE = "https://tfouttahere.com";
const b64 = v => Buffer.from(typeof v === "string" ? v : JSON.stringify(v)).toString("base64url");

module.exports = (req, res) => {
  const team = process.env.MAPKIT_TEAM_ID, kid = process.env.MAPKIT_KEY_ID, pem = process.env.MAPKIT_PRIVATE_KEY;
  if (!team || !kid || !pem) return res.status(503).json({error: "not_configured"});
  const host = String(req.headers.host || "");
  const origin = /^(www\.)?tfouttahere\.com$/.test(host) ? `https://${host}` : /^localhost(:\d+)?$/.test(host) ? `http://${host}` : SITE;
  try {
    const now = Math.floor(Date.now() / 1000);
    const body = `${b64({alg: "ES256", kid, typ: "JWT"})}.${b64({iss: team, iat: now, exp: now + 1800, origin})}`;
    const sig = crypto.sign("sha256", Buffer.from(body), {key: pem.replace(/\\n/g, "\n"), dsaEncoding: "ieee-p1363"}).toString("base64url");
    res.setHeader("Cache-Control", "private, max-age=600");
    return res.status(200).json({token: `${body}.${sig}`});
  } catch (e) {
    return res.status(500).json({error: "bad_key"});
  }
};
