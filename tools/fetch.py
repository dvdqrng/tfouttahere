import json, urllib.request, time, sys
from collections import defaultdict
C = [
# name, country, iata, lat, lon, region
("Berlin","Germany","BER",52.52,13.40,"Home"),
("Hamburg","Germany","HAM",53.55,9.99,"Home"),
("Munich","Germany","MUC",48.14,11.58,"Home"),
("Frankfurt","Germany","FRA",50.11,8.68,"Home"),
("Cologne","Germany","CGN",50.94,6.96,"Home"),
("Vienna","Austria","VIE",48.21,16.37,"Home"),
("Zurich","Switzerland","ZRH",47.38,8.54,"Home"),
("Amsterdam","Netherlands","AMS",52.37,4.90,"Home"),
("London","UK","LHR",51.51,-0.13,"Home"),
("Copenhagen","Denmark","CPH",55.68,12.57,"Home"),
("Stockholm","Sweden","ARN",59.33,18.07,"Home"),
("Oslo","Norway","OSL",59.91,10.75,"Home"),
("Lisbon","Portugal","LIS",38.72,-9.14,"Europe"),
("Faro","Portugal","FAO",37.02,-7.93,"Europe"),
("Porto","Portugal","OPO",41.15,-8.61,"Europe"),
("Funchal (Madeira)","Portugal","FNC",32.65,-16.91,"Atlantic"),
("Ponta Delgada (Azores)","Portugal","PDL",37.74,-25.67,"Atlantic"),
("Seville","Spain","SVQ",37.39,-5.98,"Europe"),
("Málaga","Spain","AGP",36.72,-4.42,"Europe"),
("Valencia","Spain","VLC",39.47,-0.38,"Europe"),
("Barcelona","Spain","BCN",41.39,2.17,"Europe"),
("Palma (Mallorca)","Spain","PMI",39.57,2.65,"Europe"),
("Santa Cruz (Tenerife)","Spain","TFS",28.05,-16.71,"Atlantic"),
("Las Palmas (Gran Canaria)","Spain","LPA",27.76,-15.57,"Atlantic"),
("Arrecife (Lanzarote)","Spain","ACE",28.96,-13.55,"Atlantic"),
("Fuerteventura","Spain","FUE",28.45,-13.86,"Atlantic"),
("Nice","France","NCE",43.70,7.27,"Europe"),
("Rome","Italy","FCO",41.90,12.50,"Europe"),
("Naples","Italy","NAP",40.85,14.27,"Europe"),
("Catania (Sicily)","Italy","CTA",37.50,15.09,"Europe"),
("Palermo (Sicily)","Italy","PMO",38.12,13.36,"Europe"),
("Cagliari (Sardinia)","Italy","CAG",39.22,9.12,"Europe"),
("Valletta","Malta","MLA",35.90,14.51,"Europe"),
("Athens","Greece","ATH",37.98,23.73,"Europe"),
("Heraklion (Crete)","Greece","HER",35.34,25.13,"Europe"),
("Rhodes","Greece","RHO",36.43,28.22,"Europe"),
("Larnaca","Cyprus","LCA",34.92,33.63,"Europe"),
("Paphos","Cyprus","PFO",34.77,32.42,"Europe"),
("Antalya","Türkiye","AYT",36.90,30.70,"Europe"),
("Istanbul","Türkiye","IST",41.01,28.98,"Europe"),
("Marrakech","Morocco","RAK",31.63,-8.01,"Africa"),
("Agadir","Morocco","AGA",30.42,-9.60,"Africa"),
("Djerba","Tunisia","DJE",33.81,10.86,"Africa"),
("Hurghada","Egypt","HRG",27.26,33.81,"Africa"),
("Sharm el-Sheikh","Egypt","SSH",27.92,34.33,"Africa"),
("Luxor","Egypt","LXR",25.69,32.64,"Africa"),
("Eilat","Israel","ETM",29.56,34.95,"Middle East"),
("Aqaba","Jordan","AQJ",29.53,35.01,"Middle East"),
("Dubai","UAE","DXB",25.20,55.27,"Middle East"),
("Abu Dhabi","UAE","AUH",24.45,54.38,"Middle East"),
("Muscat","Oman","MCT",23.59,58.41,"Middle East"),
("Doha","Qatar","DOH",25.29,51.53,"Middle East"),
("Sal","Cape Verde","SID",16.74,-22.94,"Africa"),
("Dakar","Senegal","DSS",14.72,-17.47,"Africa"),
("Cape Town","South Africa","CPT",-33.92,18.42,"Africa"),
("Zanzibar","Tanzania","ZNZ",-6.16,39.19,"Africa"),
("Mauritius","Mauritius","MRU",-20.16,57.50,"Indian Ocean"),
("Mahé","Seychelles","SEZ",-4.62,55.45,"Indian Ocean"),
("Malé","Maldives","MLE",4.18,73.51,"Indian Ocean"),
("Goa","India","GOI",15.30,74.12,"Asia"),
("Colombo","Sri Lanka","CMB",6.93,79.86,"Asia"),
("Bangkok","Thailand","BKK",13.76,100.50,"Asia"),
("Phuket","Thailand","HKT",7.88,98.39,"Asia"),
("Ho Chi Minh City","Vietnam","SGN",10.82,106.63,"Asia"),
("Singapore","Singapore","SIN",1.35,103.82,"Asia"),
("Bali","Indonesia","DPS",-8.65,115.22,"Asia"),
("Cancún","Mexico","CUN",21.16,-86.85,"Americas"),
("Mexico City","Mexico","MEX",19.43,-99.13,"Americas"),
("Havana","Cuba","HAV",23.11,-82.37,"Americas"),
("Punta Cana","Dominican Rep.","PUJ",18.58,-68.40,"Americas"),
("Bridgetown","Barbados","BGI",13.10,-59.62,"Americas"),
("Miami","USA","MIA",25.76,-80.19,"Americas"),
("Los Angeles","USA","LAX",34.05,-118.24,"Americas"),
("Phoenix","USA","PHX",33.45,-112.07,"Americas"),
("Lima","Peru","LIM",-12.05,-77.04,"Americas"),
("Rio de Janeiro","Brazil","GIG",-22.91,-43.17,"Americas"),
("Buenos Aires","Argentina","EZE",-34.60,-58.38,"Americas"),
("Sydney","Australia","SYD",-33.87,151.21,"Oceania"),
("Perth","Australia","PER",-31.95,115.86,"Oceania"),
]
VARS="sunshine_duration,daylight_duration,temperature_2m_max,precipitation_sum,cloud_cover_mean"
out=[]
B=8
for i in range(0,len(C),B):
    chunk=C[i:i+B]
    url=("https://archive-api.open-meteo.com/v1/archive?latitude="+",".join(str(c[3]) for c in chunk)+
         "&longitude="+",".join(str(c[4]) for c in chunk)+"&start_date=2022-01-01&end_date=2025-12-31&daily="+VARS+"&timezone=auto")
    for attempt in range(4):
        try:
            data=json.load(urllib.request.urlopen(url,timeout=120)); break
        except Exception as e:
            print("retry",i,e,file=sys.stderr); time.sleep(20)
    if isinstance(data,dict): data=[data]
    for c,d in zip(chunk,data):
        dd=d["daily"]; acc=defaultdict(lambda: defaultdict(list))
        for k,t in enumerate(dd["time"]):
            m=int(t[5:7])-1
            for v in VARS.split(","):
                x=dd[v][k]
                if x is not None: acc[m][v].append(x)
        months=[]
        for m in range(12):
            a=acc[m]; avg=lambda v: sum(a[v])/len(a[v])
            months.append([round(avg("sunshine_duration")/3600,1), round(avg("daylight_duration")/3600,2),
                           round(avg("temperature_2m_max"),1),
                           round(sum(1 for x in a["precipitation_sum"] if x>=1)/len(a["precipitation_sum"])*30,1),
                           round(avg("cloud_cover_mean"))])
        out.append({"n":c[0],"c":c[1],"i":c[2],"la":c[3],"lo":c[4],"r":c[5],"m":months})
    print("done",i+len(chunk),file=sys.stderr); time.sleep(3)
json.dump(out,open("climate.json","w"),separators=(",",":"),ensure_ascii=False)
