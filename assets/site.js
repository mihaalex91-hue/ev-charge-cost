
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
