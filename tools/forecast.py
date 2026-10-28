import json, urllib.request, time, sys, datetime
C=json.load(open(sys.argv[1]))
V="sunshine_duration,temperature_2m_max,precipitation_sum,cloud_cover_mean,precipitation_probability_max,weather_code"
out={}; start=None; B=10
for i in range(0,len(C),B):
    ch=C[i:i+B]
    url=("https://api.open-meteo.com/v1/forecast?latitude="+",".join(str(c["la"]) for c in ch)+"&longitude="+",".join(str(c["lo"]) for c in ch)+
         "&daily="+V+"&forecast_days=16&timezone=auto")
    data=None
    for a in range(5):
        try: data=json.load(urllib.request.urlopen(url,timeout=60)); break
        except Exception as e: print("retry",i,e,file=sys.stderr); time.sleep(15)
    if data is None: sys.exit("failed batch %d"%i)
    if isinstance(data,dict): data=[data]
    for c,d in zip(ch,data):
        dd=d["daily"]; start=start or dd["time"][0]
        rows=[]
        for k in range(len(dd["time"])):
            g=lambda v: dd[v][k]
            if g("sunshine_duration") is None or g("temperature_2m_max") is None: break
            rows.append([round(g("sunshine_duration")/3600,1),round(g("temperature_2m_max"),1),round(g("precipitation_sum") or 0,1),
                         round(g("cloud_cover_mean") or 0),g("precipitation_probability_max") or 0,g("weather_code") or 0])
        out[c["i"]]={"s":dd["time"][0],"d":rows}
    time.sleep(2)
json.dump({"asOf":datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%MZ"),"d":out},open(sys.argv[2] if len(sys.argv) > 2 else "forecast.json","w"),separators=(",",":"))
print("ok",len(out),start)
