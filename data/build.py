#!/usr/bin/env python3
"""Generates /cars/*, /tariffs/*, /cars/index.html, /tariffs/index.html, sitemap.xml
from data/cars.json and the TARIFFS list below. Run: python3 data/build.py
Re-run any time the data changes; pages are fully regenerated."""
import json, os, html, math, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://evchargecost.co.uk"
TODAY = "29 September 2026"; ISO = "2026-09-29"
LOSS = 0.9          # charging losses socket->battery
MILES = 8000        # reference annual mileage
PETROL_MPG, PETROL_PPL = 42, 1.38
PUBLIC_RAPID = 79   # p/kWh
CAP = 26.32

TARIFFS = [
 dict(slug="standard-price-cap", name="Standard price cap", supplier="Ofgem cap (any supplier)", off=26.32, peak=26.32, flat=True, hours=0, window="No off-peak window",
      url="https://www.ofgem.gov.uk/energy-price-cap", smart=False, exit_fee="None", eligibility="Everyone — it's the default tariff",
      blurb="The cap is what you pay if you've never switched. It is the wrong tariff for an EV: every kWh into the car costs the full daytime rate."),
 dict(slug="intelligent-octopus-go", name="Intelligent Octopus Go", supplier="Octopus Energy", off=8.00, peak=27.00, hours=6, window="23:30–05:30, plus extra smart slots Octopus schedules for you",
      url="https://octopus.energy/smart/intelligent-octopus-go/", smart=True, exit_fee="None", eligibility="Smart meter + a compatible car or charger (most major EV brands, Ohme, Zappi, Wallbox and others)",
      blurb="The most popular EV tariff in Britain. You tell the app when you need the car ready and how full; Octopus picks the charging slots, and any slot it schedules outside the window is billed at the cheap rate too — often 7–8 hours of cheap charging a night in practice."),
 dict(slug="octopus-go", name="Octopus Go", supplier="Octopus Energy", off=8.50, peak=27.00, hours=5, window="00:30–05:30",
      url="https://octopus.energy/smart/go/", smart=False, exit_fee="None", eligibility="Smart meter; works with any car and any charger",
      blurb="The simple version of Octopus's EV tariff: a fixed five-hour window, no app scheduling, no compatibility list. Half a penny dearer than Intelligent Go and one hour shorter."),
 dict(slug="edf-goelectric", name="EDF GoElectric", supplier="EDF", off=6.99, peak=30.00, hours=7, window="23:00–06:00",
      url="https://www.edfenergy.com/electric-cars/ev-tariffs", smart=False, exit_fee="Yes — a fixed-term tariff, typically two years", eligibility="Smart meter; any car and charger",
      blurb="The lowest headline off-peak rate on the market and the longest fixed window, at the cost of a high peak rate for the rest of the house. Works well for high-mileage drivers who charge every night and keep daytime usage low."),
 dict(slug="eon-next-drive", name="E.ON Next Drive Smart", supplier="E.ON Next", off=8.50, peak=30.87, hours=6, window="00:00–06:00",
      url="https://www.eonnext.com/electric-vehicles", smart=True, exit_fee="None", eligibility="Smart meter; smart charging through the E.ON Next app with a compatible charger",
      blurb="Six hours at 8.5p with app-based scheduling. The peak rate is one of the higher ones, so it suits households that can push most electricity use into the window."),
 dict(slug="british-gas-ev-power", name="British Gas EV Power", supplier="British Gas", off=9.00, peak=27.50, hours=5, window="00:00–05:00",
      url="https://www.britishgas.co.uk/energy/electric-vehicles.html", smart=False, exit_fee="None", eligibility="Smart meter; any car and charger",
      blurb="British Gas's answer to Octopus Go: a five-hour window at 9p. Slightly dearer than the Octopus tariffs but convenient if you're already a British Gas customer."),
 dict(slug="utility-warehouse-ev", name="Utility Warehouse EV", supplier="Utility Warehouse", off=6.90, peak=27.16, hours=5, window="00:00–05:00 GMT (01:00–06:00 in summer time)",
      url="https://uw.co.uk/", smart=False, exit_fee="None on energy; bundle services have their own terms", eligibility="Smart meter and at least two other UW services (broadband, mobile or boiler cover)",
      blurb="The cheapest off-peak rate of all, but only if you bundle. If you already want UW broadband or mobile it's a bargain; if not, the bundle usually eats the saving."),
 dict(slug="ovo-charge-anytime", name="OVO Charge Anytime", supplier="OVO", off=14.00, peak=14.00, flat=True, hours=24, window="Any time of day — the cheap rate applies to the car's charging only",
      url="https://www.ovoenergy.com/electric-cars/charge-anytime", smart=True, exit_fee="None", eligibility="OVO customer, smart meter, compatible car or charger so OVO can measure what the car used",
      blurb="Different from the rest: the house stays on OVO's normal rate and every kWh that goes into the car is credited back down to 14p, whenever you charge. Unbeatable if you can't charge overnight; dearer than a 7–9p window if you can."),
]
T = {t["slug"]: t for t in TARIFFS}
POPULAR_FOR_TARIFF = ["tesla-model-y","tesla-model-3","mg4","skoda-enyaq","kia-ev3","renault-5"]

cars = json.load(open(os.path.join(ROOT,"data","cars.json")))["cars"]
C = {c["slug"]: c for c in cars}
COMPARE_PAIRS = [("tesla-model-3","polestar-2"),("tesla-model-y","skoda-enyaq"),("tesla-model-y","kia-ev6"),("mg4","renault-5"),
 ("mg4","vauxhall-corsa-electric"),("kia-ev3","volvo-ex30"),("skoda-elroq","kia-ev3"),("byd-seal","tesla-model-3"),
 ("hyundai-ioniq-5","kia-ev6"),("nissan-leaf","mg4"),("peugeot-e-208","vauxhall-corsa-electric"),("audi-q4-e-tron","skoda-enyaq"),
 ("ford-explorer","skoda-enyaq"),("bmw-i4","tesla-model-3"),("byd-sealion-7","tesla-model-y"),("mercedes-cla","tesla-model-3"),
 ("audi-q6-e-tron","byd-sealion-7"),("hyundai-kona-electric","kia-ev3"),("volkswagen-id3","mg4"),("byd-dolphin","renault-5"),
 ("vauxhall-frontera-electric","byd-dolphin"),("skoda-elroq","skoda-enyaq")]
def partners(slug):
    out=[b if a==slug else a for a,b in COMPARE_PAIRS if slug in (a,b)]
    if len(out)<2: out += [s for s in ["tesla-model-y","mg4","kia-ev3"] if s!=slug and s not in out][:2-len(out)]
    return out[:3]

# ---------- maths ----------
def kwh_per_mile(v): return v["wh_per_mi"]/1000/LOSS
def mi_per_kwh(v): return round(1000/v["wh_per_mi"],1)
def full_charge_kwh(v): return v["usable_kwh"]/LOSS
def cost_full(v, rate): return full_charge_kwh(v)*rate/100
def ppm(v, rate): return kwh_per_mile(v)*rate
def home_hours(v, kw=7.0): return v["usable_kwh"]/kw/LOSS
def monthly(v, tariff, miles=MILES, off_share=0.9, home_share=1.0):
    off=tariff["off"]; peak=tariff["peak"]; share = 1.0 if tariff.get("flat") else off_share
    rate = share*off+(1-share)*peak
    return miles/12*kwh_per_mile(v)*rate/100
def petrol_monthly(miles=MILES): return miles/12/PETROL_MPG*4.546*PETROL_PPL
def gbp(x): return f"£{x:,.0f}" if x>=20 else f"£{x:,.2f}"
def pence(x): return f"{x:.1f}p"
def hrs(h):
    hh=int(h); mm=int(round((h-hh)*60/15)*15); 
    if mm==60: hh+=1; mm=0
    return f"{hh}h" + (f" {mm:02d}m" if mm else "")
def E(s): return html.escape(str(s))
def art(name): return "an" if name[:1].upper() in "AEIOU" or name.startswith(("MG","BMW","E.ON")) else "a"

# ---------- shared shell ----------
CSS = """:root{--bg:#F6F7F5;--surface:#FFFFFF;--ink:#16211C;--ink-soft:#4E5C56;--line:#D9DED9;--night:#0E2A3A;--night-ink:#EAF2F6;--night-soft:#9DB5C3;--amber:#F2B84B;--green:#1E9E6A;--red:#C8553D;--focus:#1E9E6A;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0F1614;--surface:#182220;--ink:#E8EEEA;--ink-soft:#A6B4AD;--line:#2A3632;--night:#08202D}}
:root[data-theme="dark"]{--bg:#0F1614;--surface:#182220;--ink:#E8EEEA;--ink-soft:#A6B4AD;--line:#2A3632;--night:#08202D}
*,*::before,*::after{box-sizing:inherit}html{scroll-padding-top:env(safe-area-inset-top,0px)}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;font-size:16px;line-height:1.5;font-feature-settings:"tnum" 1}
a{color:inherit}h1,h2,h3{margin:0;line-height:1.15;letter-spacing:-0.01em}h1{font-size:clamp(1.6rem,3.2vw,2.3rem);font-weight:700;max-width:26ch}h2{font-size:1.3rem;font-weight:600;margin-top:36px;margin-bottom:12px}h3{font-size:1.02rem;font-weight:600}p{margin:0 0 12px}
.wrap{max-width:1040px;margin:0 auto;padding:0 20px}
nav.top{display:flex;gap:18px;align-items:center;padding:16px 0;font-size:.92rem;border-bottom:1px solid var(--line)}nav.top a{text-decoration:none;color:var(--ink-soft)}nav.top a.brand{font-weight:700;color:var(--ink)}nav.top a:hover{color:var(--ink)}
.crumbs{font-size:.82rem;color:var(--ink-soft);margin:18px 0 10px}.crumbs a{text-decoration:none}
header.hero{padding:6px 0 18px}header.hero p.lead{color:var(--ink-soft);max-width:66ch;margin-top:10px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:18px 0}.stat{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px 16px}.stat b{display:block;font-size:1.35rem;font-weight:600}.stat span{font-size:.8rem;color:var(--ink-soft)}
.panel{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:22px}
.night{background:var(--night);color:var(--night-ink);border-radius:14px;padding:22px}.night .k{color:var(--night-soft);font-size:.85rem}.night b.big{font-size:2.2rem;font-weight:700;letter-spacing:-.02em}
.controls{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:6px 0 16px}@media (max-width:560px){.controls{grid-template-columns:1fr}}
label{display:block;font-size:.85rem;color:var(--ink-soft);margin-bottom:6px}select,input[type=number]{width:100%;font:inherit;color:var(--ink);background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:10px 12px;height:44px}
select:focus,input:focus,a:focus-visible{outline:3px solid var(--focus);outline-offset:2px}
table{width:100%;border-collapse:collapse;font-size:.95rem}th,td{text-align:left;padding:9px 8px;border-top:1px solid var(--line)}th{font-weight:600;font-size:.82rem;color:var(--ink-soft);border-top:0}td.num,th.num{text-align:right;white-space:nowrap}tr.sel td{font-weight:600}tr.cap td{color:var(--red)}
.scroll{overflow-x:auto}
.btn{display:inline-block;font:inherit;font-weight:600;padding:11px 16px;border-radius:9px;text-decoration:none;text-align:center;background:var(--ink);color:var(--bg);border:0;cursor:pointer}.btn.amber{background:var(--amber);color:#1B1B1B}.btn.quiet{background:transparent;color:var(--ink);border:1px solid var(--line)}
.prose{max-width:70ch}.prose p{margin-bottom:12px}.prose ul{padding-left:20px;margin:0 0 12px}
details{border-top:1px solid var(--line);padding:12px 0}details:last-of-type{border-bottom:1px solid var(--line)}summary{cursor:pointer;font-weight:600;list-style:none;display:flex;justify-content:space-between;gap:12px}summary::after{content:"+";color:var(--ink-soft);font-weight:400}details[open] summary::after{content:"–"}details p{margin-top:10px;color:var(--ink-soft)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px}@media (max-width:760px){.grid2{grid-template-columns:1fr}}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px}.card{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:16px;text-decoration:none;display:block}.card b{display:block;margin-bottom:4px}.card span{font-size:.85rem;color:var(--ink-soft)}
.links{display:flex;flex-wrap:wrap;gap:10px}.links a{font-size:.9rem;padding:8px 12px;border:1px solid var(--line);border-radius:999px;text-decoration:none;background:var(--surface)}
.checked{font-size:.82rem;color:var(--ink-soft);margin-top:10px}
footer{margin:56px 0 40px;font-size:.85rem;color:var(--ink-soft)}footer p{max-width:80ch;margin-bottom:8px}
"""
def shell(title, desc, canonical, body, jsonld=None, extra_head=""):
    ld = f'<script type="application/ld+json">{json.dumps(jsonld,ensure_ascii=False)}</script>' if jsonld else ""
    return f"""<!DOCTYPE html>
<html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<link rel="canonical" href="{canonical}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="article"><meta property="og:url" content="{canonical}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>{ld}{extra_head}
</head><body><div class="wrap">
<nav class="top"><a class="brand" href="/">EV Charge Cost</a><a href="/">Calculator</a><a href="/cars/">Cars</a><a href="/tariffs/">Tariffs</a></nav>
{body}
<footer><p>Estimates based on real-world efficiency data (EV Database) and tariff prices checked {TODAY}. Tariff prices, eligibility and windows change – confirm with the supplier before switching. Some links may earn a commission at no cost to you; this never affects the figures.</p><p>© 2026 EV Charge Cost. Made in the UK.</p></footer>
</div><script>{JS}</script></body></html>"""

JS = r"""
const LOSS=0.9, CAP=26.32;
const gbp=n=>n>=20?"£"+Math.round(n).toLocaleString("en-GB"):"£"+n.toFixed(2);
const T = window.TARIFFS; const CARS=window.CARS;
function calc(v,miles,tid){const t=T.find(x=>x.slug===tid);const share=t.flat?1:0.9;const rate=share*t.off+(1-share)*t.peak;
  const kpm=v.wh_per_mi/1000/LOSS;return {monthly:miles/12*kpm*rate/100, ppm:kpm*rate, full:v.usable_kwh/LOSS*rate/100};}
function fmtH(h){const hh=Math.floor(h),mm=Math.round((h-hh)*4)*15;return hh+"h"+(mm?(" "+String(mm).padStart(2,"0")+"m"):"");}
function renderCar(){
  const page=window.PAGE; if(!page||page.kind!=='car') return;
  const car=CARS[page.slug]; const vi=+document.getElementById('variant').value; const v=car.variants[vi];
  const miles=+document.getElementById('miles').value||8000; const tid=document.getElementById('tariff').value;
  const r=calc(v,miles,tid), cap=calc(v,miles,'standard-price-cap');
  const set=(id,t)=>{const el=document.getElementById(id); if(el) el.textContent=t;};
  set('m-monthly',gbp(r.monthly)); set('m-ppm',r.ppm.toFixed(1)+"p"); set('m-full',gbp(r.full));
  set('m-cap',gbp(cap.monthly)); set('m-save',gbp((cap.monthly-r.monthly)*12));
  set('m-kwh',v.usable_kwh); set('m-eff',(1000/v.wh_per_mi).toFixed(1)); set('m-home',fmtH(v.usable_kwh/7/LOSS)); set('m-dc',v.dc_kw+" kW"); set('m-ac',v.ac_kw+" kW");
  const petrol=miles/12/42*4.546*1.38; set('m-petrol',gbp(petrol));
  // tariff table
  const rows=T.map(t=>({t,c:calc(v,miles,t.slug)})).sort((a,b)=>a.c.monthly-b.c.monthly);
  document.getElementById('ttable').innerHTML=rows.map(x=>`<tr class="${x.t.slug===tid?'sel':''} ${x.t.slug==='standard-price-cap'?'cap':''}"><td><a href="/tariffs/${x.t.slug}/">${x.t.name}</a></td><td class="num">${x.t.off}p</td><td class="num">${gbp(x.c.monthly)}</td><td class="num">${x.c.ppm.toFixed(1)}p</td><td class="num">${gbp(x.c.full)}</td></tr>`).join('');
  renderCompare(v,miles,tid);
}
function renderCompare(v,miles,tid){
  const sel=document.getElementById('cmp'); if(!sel) return; const other=CARS[sel.value]; if(!other){document.getElementById('cmpwrap').hidden=true;return;}
  const ov=other.variants[other.default_variant]; const a=calc(v,miles,tid), b=calc(ov,miles,tid);
  const row=(k,x,y)=>`<tr><th>${k}</th><td class="num">${x}</td><td class="num">${y}</td></tr>`;
  document.getElementById('cmptable').innerHTML=
   `<tr><th></th><th class="num">${window.PAGE.name}<br><small>${v.name}</small></th><th class="num">${other.make} ${other.model}<br><small>${ov.name}</small></th></tr>`+
   row('Usable battery',v.usable_kwh+' kWh',ov.usable_kwh+' kWh')+row('Real efficiency',(1000/v.wh_per_mi).toFixed(1)+' mi/kWh',(1000/ov.wh_per_mi).toFixed(1)+' mi/kWh')+
   row('Cost per mile',a.ppm.toFixed(1)+'p',b.ppm.toFixed(1)+'p')+row('Monthly charging cost',gbp(a.monthly),gbp(b.monthly))+row('Full charge',gbp(a.full),gbp(b.full))+
   row('Home charge 0–100% (7 kW)',fmtH(v.usable_kwh/7/LOSS),fmtH(ov.usable_kwh/7/LOSS))+row('Peak rapid charging',v.dc_kw+' kW',ov.dc_kw+' kW');
  document.getElementById('cmpwrap').hidden=false;
  document.getElementById('cmplink').href='/cars/'+sel.value+'/';
}
function renderTariff(){
  const page=window.PAGE; if(!page||page.kind!=='tariff') return;
  const miles=+document.getElementById('miles').value||8000; const eff=+document.getElementById('eff').value||3.5;
  const v={wh_per_mi:1000/eff,usable_kwh:60}; const r=calc(v,miles,page.slug), cap=calc(v,miles,'standard-price-cap');
  const set=(id,t)=>{const el=document.getElementById(id); if(el) el.textContent=t;};
  set('m-monthly',gbp(r.monthly)); set('m-ppm',r.ppm.toFixed(1)+"p"); set('m-cap',gbp(cap.monthly)); set('m-save',gbp((cap.monthly-r.monthly)*12));
  const tbody=document.getElementById('ctable'); if(tbody){tbody.innerHTML=page.popular.map(s=>{const c=CARS[s],cv=c.variants[c.default_variant];const x=calc(cv,miles,page.slug),y=calc(cv,miles,'standard-price-cap');
    return `<tr><td><a href="/cars/${s}/">${c.make} ${c.model}</a> <small>${cv.name}</small></td><td class="num">${(1000/cv.wh_per_mi).toFixed(1)}</td><td class="num">${gbp(x.monthly)}</td><td class="num">${gbp(y.monthly)}</td><td class="num">${gbp((y.monthly-x.monthly)*12)}</td></tr>`;}).join('');}
}
document.addEventListener('DOMContentLoaded',()=>{
  ['variant','miles','tariff','cmp','eff'].forEach(id=>{const el=document.getElementById(id); if(el) el.addEventListener('input',()=>{renderCar();renderTariff();});});
  const q=new URLSearchParams(location.search).get('compare'); const cmp=document.getElementById('cmp'); if(q&&cmp&&CARS[q]) cmp.value=q;
  renderCar(); renderTariff();
});
"""

def data_script(page):
    slim={s:{"make":c["make"],"model":c["model"],"default_variant":c["default_variant"],"variants":[{k:v[k] for k in ("name","usable_kwh","wh_per_mi","ac_kw","dc_kw")} for v in c["variants"]]} for s,c in C.items()}
    tar=[{k:t.get(k) for k in ("slug","name","off","peak","flat")} for t in TARIFFS]
    return f"<script>window.CARS={json.dumps(slim)};window.TARIFFS={json.dumps(tar)};window.PAGE={json.dumps(page)};</script>"

# ---------- car page ----------
def car_page(c):
    v=c["variants"][c["default_variant"]]; name=f'{c["make"]} {c["model"]}'; slug=c["slug"]
    iog=T["intelligent-octopus-go"]; edf=T["edf-goelectric"]
    m_iog=monthly(v,iog); m_cap=monthly(v,T["standard-price-cap"]); m_pet=petrol_monthly()
    cheapest=min(TARIFFS,key=lambda t:monthly(v,t)); best=min((t for t in TARIFFS if not t.get("flat") or t["slug"]=="ovo-charge-anytime"),key=lambda t:monthly(v,t))
    if best["slug"]=="utility-warehouse-ev": best=sorted(TARIFFS,key=lambda t:monthly(v,t))[1]
    eff=mi_per_kwh(v); ppm_iog=ppm(v,iog["off"]); ppm_cap=ppm(v,CAP); ppm_pub=ppm(v,PUBLIC_RAPID); ppm_pet=PETROL_PPL*4.546/PETROL_MPG*100
    title=f"{name} charging cost UK 2026: per charge, per mile & per month"
    desc=f"What it costs to charge a {name} at home and in public: about {gbp(cost_full(v,iog['off']))} for a full charge on an EV tariff, {gbp(cost_full(v,CAP))} on the price cap, {pence(ppm_iog)}–{pence(ppm_cap)} per mile. Real-world figures, all UK EV tariffs compared."
    canonical=f"{SITE}/cars/{slug}/"
    variants_opts="".join(f'<option value="{i}"{" selected" if i==c["default_variant"] else ""}>{E(x["name"])} – {x["usable_kwh"]} kWh</option>' for i,x in enumerate(c["variants"]))
    tariff_opts="".join(f'<option value="{t["slug"]}"{" selected" if t["slug"]=="intelligent-octopus-go" else ""}>{E(t["name"])}</option>' for t in TARIFFS)
    cmp_opts='<option value="">Choose a car…</option>'+"".join(f'<option value="{s}">{E(C[s]["make"]+" "+C[s]["model"])}</option>' for s in sorted(C) if s!=slug)
    pts=partners(slug)
    legacy=[x for x in c["variants"] if x.get("legacy")]
    variant_rows="".join(f'<tr><td>{E(x["name"])}</td><td class="num">{x["usable_kwh"]} kWh</td><td class="num">{mi_per_kwh(x)}</td><td class="num">{gbp(cost_full(x,iog["off"]))}</td><td class="num">{gbp(cost_full(x,CAP))}</td><td class="num">{hrs(home_hours(x))}</td><td class="num">{x["ac_kw"]} / {x["dc_kw"]} kW</td></tr>' for x in c["variants"])
    notes="".join(f"<p>{E(n)}.</p>" for n in c["notes"])
    hp=c.get("heat_pump","")
    winter = ("It has a heat pump as standard, so winter consumption typically rises 15–25% rather than the 30–40% you see on cars without one." if hp.startswith("standard")
              else f"Heat pump: {E(hp)}. Without one, expect winter consumption 30–40% above the figure used here; with it, closer to 15–25%.")
    faq=[
     (f"How much does it cost to fully charge {art(name)} {name}?", f"From empty, the {v['name']} version needs about {full_charge_kwh(v):.0f} kWh from the socket once charging losses are included. On Intelligent Octopus Go (8p) that is around {gbp(cost_full(v,iog['off']))}; on the standard price cap it is around {gbp(cost_full(v,CAP))}; at a 79p public rapid charger about {gbp(cost_full(v,PUBLIC_RAPID))}."),
     (f"What is the {name}'s cost per mile?", f"Using EV Database's real-world figure of {eff} mi/kWh: about {pence(ppm_iog)} per mile on an 8p EV tariff, {pence(ppm_cap)} on the price cap and {pence(ppm_pub)} on public rapid chargers. A 42 mpg petrol car at £1.38 a litre costs about {pence(ppm_pet)} per mile."),
     (f"How long does {art(name)} {name} take to charge at home?", f"On a 7 kW home charger the {v['usable_kwh']} kWh battery goes from empty to full in roughly {hrs(home_hours(v))}. Most nights you'll only be topping up 20–40%, which takes {hrs(home_hours(v)*0.3)} or so and fits inside any EV tariff window."),
     (f"Which tariff is cheapest for {art(name)} {name}?", f"For an 8,000-mile-a-year driver charging at home, {cheapest['name']} gives the lowest charging bill in our comparison, but it has conditions. {best['name']} is the best mainstream choice, costing about {gbp(monthly(v,best))} a month for charging against {gbp(m_cap)} on the price cap."),
    ]
    jsonld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}
    body=f"""
<div class="crumbs"><a href="/">Home</a> › <a href="/cars/">Cars</a> › {E(name)}</div>
<header class="hero"><h1>{E(name)} charging cost in the UK</h1>
<p class="lead">Real-world figures for the {E(v['name'])}: <b>{eff} mi/kWh</b>, <b>{v['usable_kwh']} kWh</b> usable battery. A full charge costs about <b>{gbp(cost_full(v,iog['off']))}</b> on an 8p EV tariff, <b>{gbp(cost_full(v,CAP))}</b> on the price cap. Change the version, mileage and tariff below.</p></header>

<section class="grid2">
 <div class="panel">
  <div class="controls">
   <div><label for="variant">Version</label><select id="variant">{variants_opts}</select></div>
   <div><label for="tariff">Home tariff</label><select id="tariff">{tariff_opts}</select></div>
   <div><label for="miles">Miles per year</label><input id="miles" type="number" min="1000" max="50000" step="500" value="{MILES}"></div>
  </div>
  <div class="stats">
   <div class="stat"><b id="m-kwh">{v['usable_kwh']}</b><span>kWh usable</span></div>
   <div class="stat"><b id="m-eff">{eff}</b><span>mi/kWh, real world</span></div>
   <div class="stat"><b id="m-home">{hrs(home_hours(v))}</b><span>0–100% on 7 kW</span></div>
   <div class="stat"><b id="m-dc">{v['dc_kw']} kW</b><span>peak rapid charging</span></div>
  </div>
 </div>
 <aside class="night" aria-live="polite">
  <p class="k">Charging cost on the selected tariff</p>
  <b class="big" id="m-monthly">{gbp(m_iog)}</b> <span class="k">per month</span>
  <div class="stats" style="margin-bottom:0"><div><b id="m-ppm" style="font-size:1.2rem">{pence(ppm_iog)}</b><br><span class="k">per mile</span></div><div><b id="m-full" style="font-size:1.2rem">{gbp(cost_full(v,iog['off']))}</b><br><span class="k">full charge</span></div><div><b id="m-cap" style="font-size:1.2rem">{gbp(m_cap)}</b><br><span class="k">on the price cap</span></div></div>
  <p class="k" style="margin-top:14px">You'd save about <b id="m-save" style="color:var(--amber)">{gbp((m_cap-m_iog)*12)}</b> a year versus the price cap, and the same miles in a 42 mpg petrol car cost about <b id="m-petrol">{gbp(m_pet)}</b> a month.</p>
 </aside>
</section>

<h2>What {art(name)} {E(name)} costs on every UK EV tariff</h2>
<div class="panel scroll"><table><thead><tr><th>Tariff</th><th class="num">Off-peak</th><th class="num">Per month</th><th class="num">Per mile</th><th class="num">Full charge</th></tr></thead><tbody id="ttable"></tbody></table>
<p class="checked">Assumes 90% of home charging lands in the off-peak window. Standing charges and daytime household use aren't included. Rates checked {TODAY}.</p></div>

<h2>Compare the {E(name)} with another EV</h2>
<div class="panel"><div class="controls"><div><label for="cmp">Compare with</label><select id="cmp">{cmp_opts}</select></div></div>
<div id="cmpwrap" hidden><div class="scroll"><table id="cmptable"></table></div><p style="margin-top:12px"><a class="btn quiet" id="cmplink" href="#">Open the other car's page →</a></p></div>
<div class="links" style="margin-top:8px">{"".join(f'<a href="/cars/{slug}/?compare={p}">vs {E(C[p]["make"]+" "+C[p]["model"])}</a>' for p in pts)}</div></div>

<h2>Every {E(name)} version at a glance</h2>
<div class="panel scroll"><table><thead><tr><th>Version</th><th class="num">Usable</th><th class="num">mi/kWh</th><th class="num">Full charge, 8p</th><th class="num">Full charge, cap</th><th class="num">0–100% on 7 kW</th><th class="num">AC / DC max</th></tr></thead><tbody>{variant_rows}</tbody></table>
{"<p class='checked'>Versions marked as older model years are no longer sold new but are common on the used market.</p>" if legacy else ""}</div>

<section class="prose"><h2>About charging the {E(name)}</h2>
{notes}
<p>{winter} The efficiency figure on this page is EV Database's real-world combined number, which sits between the official WLTP figure and a cold motorway run; it's the honest one to budget with.</p>
<p>On sale {E(c['on_sale'])}. Home charging at 7 kW ({E(str(v['ac_kw']))} kW AC on-board charger on this version) adds about {7*LOSS*eff:.0f} miles of range per hour. Public rapid charging peaks at {v['dc_kw']} kW on the {E(v['name'])}; at typical UK rapid-charger prices of 75–85p/kWh that works out at {pence(ppm_pub)} per mile — roughly the same as petrol — so the whole saving with this car comes from charging at home on a tariff with a cheap window.</p>
<h2>Which tariff suits {art(name)} {E(name)}?</h2>
<p>Charging {MILES:,} miles a year at home, the {E(name)} needs about {MILES*kwh_per_mile(v)/365:.0f} kWh a night on average — {hrs(MILES*kwh_per_mile(v)/365/7)} of charging at 7 kW — so it fits comfortably inside a five- or six-hour window. Our pick is <a href="/tariffs/{best['slug']}/">{E(best['name'])}</a>: about {gbp(monthly(v,best))} a month for charging, {gbp((m_cap-monthly(v,best))*12)} a year less than the price cap. <a href="/tariffs/edf-goelectric/">EDF GoElectric</a> is fractionally cheaper per kWh and works with any charger, but has a higher peak rate and exit fees. If you can't charge overnight, <a href="/tariffs/ovo-charge-anytime/">OVO Charge Anytime</a> gives 14p at any time of day.</p>
<p>Run your own numbers, including public charging and your petrol comparison, in the <a href="/">EV charging cost calculator</a>.</p>
</section>

<h2>Common questions</h2>
{"".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q,a in faq)}
<p class="checked">Battery and efficiency data: EV Database (real-world). Charging power: manufacturer specifications. Last checked {TODAY}.</p>
{data_script({"kind":"car","slug":slug,"name":name})}"""
    return shell(title,desc,canonical,body,jsonld)

# ---------- tariff page ----------
def tariff_page(t):
    slug=t["slug"]; name=t["name"]; ref={"wh_per_mi":1000/3.5,"usable_kwh":60}
    m=monthly(ref,t); mcap=monthly(ref,T["standard-price-cap"]); p=ppm(ref, t["off"] if t.get("flat") else 0.9*t["off"]+0.1*t["peak"])
    title=f"{name} review 2026: rates, hours, who it suits and what you'd pay"
    desc=f"{name} from {t['supplier']}: {t['off']}p/kWh off-peak, {t['window']}. What an average EV driver pays per month, how it compares with the price cap and other EV tariffs, eligibility and exit fees."
    canonical=f"{SITE}/tariffs/{slug}/"
    others=[x for x in TARIFFS if x["slug"] not in (slug,"standard-price-cap")]
    rows="".join(f'<tr><td><a href="/tariffs/{x["slug"]}/">{E(x["name"])}</a></td><td class="num">{x["off"]}p</td><td class="num">{"—" if x.get("flat") else str(x["peak"])+"p"}</td><td class="num">{x["hours"] if x["hours"]<24 else "24"} h</td><td class="num">{gbp(monthly(ref,x))}</td></tr>' for x in sorted(TARIFFS,key=lambda x:monthly(ref,x)))
    faq=[(f"What is the {name} off-peak rate?", f"{t['off']}p per kWh, {t['window'].lower() if not t.get('flat') else 'at any time of day for the car'}. {'Outside the window electricity costs about '+str(t['peak'])+'p per kWh.' if not t.get('flat') else ''} Rates checked {TODAY}."),
          (f"Who can get {name}?", t["eligibility"]+"."),
          (f"Does {name} have an exit fee?", t["exit_fee"]+"."),
          (f"How much would I save with {name}?", f"An 8,000-mile driver in a typical 3.5 mi/kWh EV, charging at home, pays about {gbp(m)} a month for charging on {name} against {gbp(mcap)} on the price cap — around {gbp((mcap-m)*12)} a year. The rest of the house {'pays the same flat rate.' if t.get('flat') else 'pays the peak rate outside the window, which can eat into the saving if you use a lot of daytime electricity.'}")]
    jsonld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}
    peak_note = "" if t.get("flat") else f"<p><b>The whole-house question.</b> The cheap rate applies to everything you use in the window, not just the car — so a dishwasher or immersion heater on a timer also gets {t['off']}p. But everything outside the window is billed at {t['peak']}p, {'above' if t['peak']>CAP else 'close to'} the price cap. A household using 3,000 kWh a year of daytime electricity would pay about {gbp(3000*(t['peak']-CAP)/100)} a year {'more' if t['peak']>CAP else 'less'} on the house than on the cap; a {'high' if t['peak']>29 else 'moderate'} peak rate like this one only makes sense if the car saving is bigger than that.</p>"
    body=f"""
<div class="crumbs"><a href="/">Home</a> › <a href="/tariffs/">Tariffs</a> › {E(name)}</div>
<header class="hero"><h1>{E(name)}: rates, hours and what you'd pay</h1><p class="lead">{E(t['blurb'])}</p></header>
<div class="stats">
 <div class="stat"><b>{t['off']}p</b><span>per kWh {'flat, car only' if slug=='ovo-charge-anytime' else ('flat' if t.get('flat') else 'off-peak')}</span></div>
 <div class="stat"><b>{'—' if t.get('flat') else str(t['peak'])+'p'}</b><span>peak rate</span></div>
 <div class="stat"><b>{'Any time' if t['hours']>=24 else (str(t['hours'])+' hours' if t['hours'] else 'None')}</b><span>cheap window</span></div>
 <div class="stat"><b>{'Yes' if t['smart'] else 'No'}</b><span>smart charging needed</span></div>
</div>
<section class="grid2">
 <div class="panel"><h3>Try your own numbers</h3><div class="controls" style="margin-top:12px">
  <div><label for="miles">Miles per year</label><input id="miles" type="number" min="1000" max="50000" step="500" value="{MILES}"></div>
  <div><label for="eff">Your car's efficiency (mi/kWh)</label><input id="eff" type="number" min="2" max="6" step="0.1" value="3.5"></div></div>
  <p class="checked">Assumes home charging with 90% of it in the window (100% for flat tariffs). Not sure of your efficiency? Pick your car from the <a href="/cars/">car list</a>.</p></div>
 <aside class="night" aria-live="polite"><p class="k">Charging cost on {E(name)}</p><b class="big" id="m-monthly">{gbp(m)}</b> <span class="k">per month</span>
  <div class="stats" style="margin-bottom:0"><div><b id="m-ppm" style="font-size:1.2rem">{pence(p)}</b><br><span class="k">per mile</span></div><div><b id="m-cap" style="font-size:1.2rem">{gbp(mcap)}</b><br><span class="k">on the price cap</span></div><div><b id="m-save" style="font-size:1.2rem;color:var(--amber)">{gbp((mcap-m)*12)}</b><br><span class="k">saved per year</span></div></div>
  <p style="margin-top:16px"><a class="btn amber" href="{t['url']}" rel="nofollow sponsored noopener" target="_blank">{'See the price cap explained' if slug=='standard-price-cap' else 'See '+E(name)}</a></p></aside>
</section>
<section class="prose"><h2>Key facts</h2>
<ul><li><b>Supplier:</b> {E(t['supplier'])}</li><li><b>Cheap window:</b> {E(t['window'])}</li><li><b>Eligibility:</b> {E(t['eligibility'])}</li><li><b>Exit fee:</b> {E(t['exit_fee'])}</li><li><b>Smart meter:</b> required{' — every time-of-use tariff needs one' if not t.get('flat') or slug=='ovo-charge-anytime' else ''}</li></ul>
{peak_note}
<p><b>Will your car fill up in the window?</b> A 7 kW charger delivers about {7*LOSS:.1f} kWh an hour into the battery. {'There is no window to worry about.' if t['hours']>=24 or t['hours']==0 else f"In {t['hours']} hours that is roughly {7*LOSS*t['hours']:.0f} kWh, enough to add {7*LOSS*t['hours']*3.5:.0f} miles at 3.5 mi/kWh — more than most people drive in a day, but not a full charge on a 75–80 kWh battery from empty. If you regularly arrive home nearly flat, a longer window or a smart tariff that adds slots matters more than a fraction of a penny per kWh."}</p>
</section>
<h2>What popular EVs cost on {E(name)}</h2>
<div class="panel scroll"><table><thead><tr><th>Car</th><th class="num">mi/kWh</th><th class="num">Per month</th><th class="num">On the cap</th><th class="num">Saving / yr</th></tr></thead><tbody id="ctable"></tbody></table></div>
<h2>{E(name)} versus the other EV tariffs</h2>
<div class="panel scroll"><table><thead><tr><th>Tariff</th><th class="num">Off-peak</th><th class="num">Peak</th><th class="num">Window</th><th class="num">Per month*</th></tr></thead><tbody>{rows}</tbody></table><p class="checked">*8,000 miles a year, 3.5 mi/kWh, home charging. Standing charges excluded. Rates checked {TODAY}.</p></div>
<h2>Common questions</h2>
{"".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q,a in faq)}
<p class="checked">Not financial advice. Prices and conditions change; confirm with {E(t['supplier'])} before switching. Use the <a href="/">calculator</a> to include public charging and your petrol comparison.</p>
{data_script({"kind":"tariff","slug":slug,"popular":POPULAR_FOR_TARIFF})}"""
    return shell(title,desc,canonical,body,jsonld)

# ---------- index pages ----------
def cars_index():
    iog=T["intelligent-octopus-go"]
    cards="".join(f'<a class="card" href="/cars/{c["slug"]}/"><b>{E(c["make"]+" "+c["model"])}</b><span>{mi_per_kwh(c["variants"][c["default_variant"]])} mi/kWh · full charge {gbp(cost_full(c["variants"][c["default_variant"]],iog["off"]))} on 8p / {gbp(cost_full(c["variants"][c["default_variant"]],CAP))} on the cap</span></a>' for c in sorted(cars,key=lambda c:c["make"]+c["model"]))
    body=f"""<div class="crumbs"><a href="/">Home</a> › Cars</div><header class="hero"><h1>Charging costs by car</h1><p class="lead">Real-world running costs for the {len(cars)} most popular EVs in Britain: cost per charge, per mile and per month on every UK EV tariff, with every battery version covered. Ranked by 2025 sales and how many are on the road.</p></header><div class="cards">{cards}</div>
<section class="prose" style="margin-top:36px"><h2>How to read these pages</h2><p>Each page uses EV Database's real-world efficiency rather than the official WLTP figure, adds 10% for charging losses, and prices the electricity at the tariff you choose. The default is Intelligent Octopus Go at 8p per kWh because it is the most widely used EV tariff; the standard price cap ({CAP}p) is shown alongside so you can see what switching is worth. Cost per mile is the cleanest way to compare cars with different battery sizes.</p></section>"""
    return shell("EV charging cost by car: every popular UK electric car compared (2026)", f"Charging cost per mile, per charge and per month for the {len(cars)} best-selling electric cars in the UK, on every EV tariff. Real-world efficiency data.", f"{SITE}/cars/", body)
def tariffs_index():
    ref={"wh_per_mi":1000/3.5,"usable_kwh":60}
    cards="".join(f'<a class="card" href="/tariffs/{t["slug"]}/"><b>{E(t["name"])}</b><span>{t["off"]}p {"flat" if t.get("flat") else "off-peak"} · {E(t["window"].split(",")[0])} · {gbp(monthly(ref,t))}/month for 8,000 miles</span></a>' for t in sorted(TARIFFS,key=lambda t:monthly(ref,t)))
    body=f"""<div class="crumbs"><a href="/">Home</a> › Tariffs</div><header class="hero"><h1>UK EV tariffs compared</h1><p class="lead">Every mainstream electric-car tariff in Britain: the cheap rate, the hours, the catches, and what a typical driver pays. Rates checked {TODAY}.</p></header><div class="cards">{cards}</div>
<section class="prose" style="margin-top:36px"><h2>Choosing between them</h2><p>Three things decide it. First, whether your car or charger can do smart scheduling — if not, Octopus Go, EDF GoElectric and British Gas EV Power work with anything. Second, how much electricity the rest of your house uses in the daytime: tariffs with a 30p peak rate punish heavy daytime use. Third, whether you can charge overnight at all; if not, OVO Charge Anytime's 14p at any hour is the one to look at. The <a href="/">calculator</a> ranks them for your own mileage and car.</p></section>"""
    return shell("Best EV tariffs UK 2026: Intelligent Octopus Go, EDF GoElectric, E.ON Next Drive and more compared", "All UK electric-car tariffs compared: off-peak rates, windows, compatibility, exit fees and what an average EV driver pays per month on each.", f"{SITE}/tariffs/", body)

# ---------- write ----------
def w(path, content):
    full=os.path.join(ROOT,path); os.makedirs(os.path.dirname(full),exist_ok=True); open(full,"w").write(content)
w("assets/site.css",CSS); w("assets/site.js",JS)
urls=[("",1.0),("cars/",0.8),("tariffs/",0.8)]
for c in cars: w(f"cars/{c['slug']}/index.html",car_page(c)); urls.append((f"cars/{c['slug']}/",0.7))
for t in TARIFFS: w(f"tariffs/{t['slug']}/index.html",tariff_page(t)); urls.append((f"tariffs/{t['slug']}/",0.7))
w("cars/index.html",cars_index()); w("tariffs/index.html",tariffs_index())
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"  <url><loc>{SITE}/{u}</loc><lastmod>{ISO}</lastmod><changefreq>monthly</changefreq><priority>{p}</priority></url>\n" for u,p in urls)+"</urlset>\n"
w("sitemap.xml",sm)
print(f"built {len(cars)} car pages, {len(TARIFFS)} tariff pages, 2 index pages, sitemap with {len(urls)} URLs")
