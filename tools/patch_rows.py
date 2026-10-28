import sys
p=sys.argv[1]; s=open(p).read()
def rep(old,new):
    global s
    assert s.count(old)==1, old[:80]
    s=s.replace(old,new)
# data: per-day series for the sparkline
rep('''daily.push({d, sun: row[0], t: row[1], mm: row[2], code: row[5]}); }''','''daily.push({d, sun: row[0], t: row[1], mm: row[2], code: row[5]}); series.push({sun: row[0], dl, rain: row[2] >= 1, fc: 1}); }''')
rep('''else { const m = c.m[d.getUTCMonth()]; sun += Math.min(m[0], dl); temp += m[2]; rain += m[3] / 30; cloud += m[4]; }''','''else { const m = c.m[d.getUTCMonth()]; sun += Math.min(m[0], dl); temp += m[2]; rain += m[3] / 30; cloud += m[4]; series.push({sun: m[0], dl, rain: m[3] / 30 >= 0.3, fc: 0}); }''')
rep('let sun = 0, day = 0, temp = 0, rain = 0, cloud = 0, nf = 0; const daily = [];','let sun = 0, day = 0, temp = 0, rain = 0, cloud = 0, nf = 0; const daily = [], series = [];')
rep('cloud: cloud/n, nf, nd: n, daily,','cloud: cloud/n, nf, nd: n, daily, series,')
# CSS: replace tile styles with compact row styles
a=s.index('.tiles { display: grid;'); b=s.index('\n',s.index('.meter i.on {'))+1
s=s[:a]+'''.cols, #results li button { display: grid; grid-template-columns: minmax(0, 1fr) 112px 42px 50px; gap: 10px; align-items: center; }
.cols { padding: 8px 14px 6px; font: 600 10px var(--mono); text-transform: uppercase; letter-spacing: .07em; color: var(--muted); border-bottom: 1px solid var(--line); }
.cols span:nth-child(n+3) { text-align: right; }
.key { display: flex; flex-wrap: wrap; gap: 4px 12px; font-size: 11.5px; color: var(--muted); }
.key i { display: inline-block; width: 6px; height: 10px; border-radius: 1px; vertical-align: -1px; margin-right: 4px; background: var(--sun); }
.key i.t { opacity: .4; } .key i.r { width: 5px; height: 5px; border-radius: 50%; background: var(--rain); vertical-align: 1px; }
.pl { display: flex; flex-direction: column; min-width: 0; }
.pl .nm { font: 700 14.5px/1.2 var(--display); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.pl .meta { font-size: 11.5px; color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.spark { display: flex; align-items: center; gap: 6px; }
.spark b { font: 700 15px var(--display); font-variant-numeric: tabular-nums; width: 30px; text-align: right; flex: none; }
.spark svg { display: block; overflow: visible; }
.spark .dl { fill: color-mix(in srgb, var(--ink) 9%, transparent); }
.spark .s { fill: var(--sun); } .spark .s.t { opacity: .42; }
.spark .rn { fill: var(--rain); } .spark .rn.t { opacity: .45; }
.tmp { display: flex; align-items: center; justify-content: flex-end; gap: 3px; font: 600 14px var(--body); font-variant-numeric: tabular-nums; }
.tmp svg { width: 14px; height: 14px; color: var(--muted); } .tmp.clear svg { color: var(--sun); }
.fare { font: 700 14.5px var(--display); text-align: right; font-variant-numeric: tabular-nums; }
'''+s[b:]
rep('#results li button { all: unset; box-sizing: border-box; width: 100%; display: flex; flex-direction: column; gap: 8px; padding: 12px 14px;','#results li button { all: unset; box-sizing: border-box; width: 100%; padding: 9px 14px;')
# rain colour token
rep('--halo: #ffffff;','--halo: #ffffff; --rain: #3b7dd8;')
s=s.replace('--halo: #0f1420;','--halo: #0f1420; --rain: #6ea8ff;')
# list header: key + column labels
rep('''    <ul id="results"></ul>''','''    <div class="cols" aria-hidden="true"><span>Place</span><span>Sun each day</span><span>High</span><span>Fare</span></div>
    <ul id="results"></ul>''')
rep('''      </select>
    </div>''','''      </select>
      <div class="key"><span><i></i>Forecast sun</span><span><i class="t"></i>Typical sun</span><span><i class="r"></i>Rain</span><span>Grey: daylight</span></div>
    </div>''')
# row template
a=s.index('  $("results").innerHTML = ok.length ? ok.map('); b=s.index('    : `<li class="empty">')
s=s[:a]+'''  $("results").innerHTML = ok.length ? ok.map(r => {
    const [, place, area] = r.n.match(/^(.*?)(?: \\((.*)\\))?$/), w = sky(r);
    const src = r.nf === r.nd ? "forecast" : r.nf ? `forecast for ${r.nf} of ${r.nd} days` : "typical weather";
    return `<li><button data-i="${r.i}" class="${r.i === S.sel ? "sel" : ""}" title="${r.sun.toFixed(1)} h sun a day, ${r.day.toFixed(1)} h daylight, ${rainText(r)} (${src})">
      <span class="pl"><span class="nm">${place}</span><span class="meta">${area ? area + ", " : ""}${r.c} · ${r.hrs.toFixed(1)} h</span></span>
      <span class="spark"><b>${r.sun.toFixed(1)}</b>${spark(r)}</span>
      <span class="tmp ${w.k}">${ICON[w.k]}${Math.round(r.temp)}°</span>
      <span class="fare">€${r.eur}</span>
    </button></li>`; }).join("")
'''+s[b:]
rep('const short = n =>','''// Sun hours per trip day as tiny bars over a daylight track; solid = forecast, pale = typical, dot = rain
function spark(r) {
  const W = 74, H = 22, n = r.series.length, g = n > 12 ? 1 : 2, bw = Math.max(1.2, (W - g * (n - 1)) / n), y = v => Math.min(v, 14) / 14 * H;
  return `<svg width="${W}" height="${H + 6}" viewBox="0 0 ${W} ${H + 6}" aria-hidden="true">${r.series.map((x, i) => { const X = (i * (bw + g)).toFixed(1);
    return `<rect class="dl" x="${X}" y="${(H - y(x.dl)).toFixed(1)}" width="${bw.toFixed(1)}" height="${y(x.dl).toFixed(1)}" rx="1"/>` +
      `<rect class="s${x.fc ? "" : " t"}" x="${X}" y="${(H - y(Math.min(x.sun, x.dl))).toFixed(1)}" width="${bw.toFixed(1)}" height="${y(Math.min(x.sun, x.dl)).toFixed(1)}" rx="1"/>` +
      (x.rain ? `<circle class="rn${x.fc ? "" : " t"}" cx="${(+X + bw / 2).toFixed(1)}" cy="${H + 3.5}" r="1.6"/>` : ""); }).join("")}</svg>`;
}
const short = n =>''')
rep('aside.list { right: var(--gut-r); top: var(--panel-top, 130px); width: 330px;','aside.list { right: var(--gut-r); top: var(--panel-top, 130px); width: 350px;')
open(p,'w').write(s)
