# evchargecost.co.uk — research notes for the car & tariff pages
Compiled 29 September 2026. Companion to `cars.json`.

## 1. Which 25 cars, and why

Selection = 2025 full-year UK sales (SMMT) + August 2026 momentum + size of the *existing* owner base (people who search "how much to charge my X" are owners, not just buyers).

| # | Car | Why it's in |
|---|-----|-------------|
| 1 | Tesla Model Y | #1 UK EV 2022–2025 (24,298 in 2025) |
| 2 | Tesla Model 3 | #2 in 2025, #1 in Aug 2026; most efficient EV on sale |
| 3 | Audi Q4 e-tron | #3 in 2025; huge fleet population |
| 4 | Audi Q6 e-tron | #4 in 2025, still top-10 in 2026 |
| 5 | Ford Explorer | #5 in 2025 |
| 6 | BMW i4 | #6 in 2025 |
| 7 | Skoda Enyaq | #7 in 2025, #6 Aug 2026; large used pool |
| 8 | Kia EV3 | #8 in 2025, #9 Aug 2026 |
| 9 | Skoda Elroq | #9 in 2025, #7 Aug 2026 |
| 10 | Volvo EX30 | #10 in 2025 |
| 11 | Renault 5 | best-selling EV to private buyers early 2026 |
| 12 | MG4 | top-5 2023–24; biggest "cheap EV" owner base |
| 13 | Vauxhall Corsa Electric | top-10 2021–23; big used pool |
| 14 | Peugeot e-208 | twin of the Corsa; high search volume |
| 15 | VW ID.3 | top-10 2020–22; very common used |
| 16 | Hyundai IONIQ 5 | top-10 2022–23 |
| 17 | Kia EV6 | top-10 2022–23 |
| 18 | Polestar 2 | top-10 2021–23 |
| 19 | BYD Seal | BYD = #1 EV brand Jan–Apr 2026 |
| 20 | BYD Sealion 7 | fastest-rising SUV 2026 |
| 21 | BYD Dolphin (+ Surf) | BYD volume hatch; Surf is a top cheap EV |
| 22 | Nissan Leaf | largest older-EV population in UK; new Mk3 launched 2026 |
| 23 | Hyundai Kona Electric | top-10 2019–21; very common used |
| 24 | Mercedes CLA | #5 Aug 2026; 2nd most efficient EV on sale |
| 25 | Vauxhall Frontera Electric | #3 Aug 2026; Electric Car Grant bargain |

**Next 25 (week 2 batch):** Jaecoo E5, Omoda E5, Mini Cooper Electric, Fiat 500e, Renault Megane E-Tech, Cupra Born, VW ID.4, VW ID.7, BMW iX1, BMW iX3 (new), Ford Capri, Peugeot e-2008, Vauxhall Mokka Electric, Citroën ë-C3, Dacia Spring, Hyundai Inster, Kia EV4, Kia Niro EV, Renault Zoe, Nissan Ariya, MG ZS EV / MGS5, Toyota bZ4X, Ford Puma Gen-E, Mercedes EQA, Kia EV9.

## 2. Data sources and verification log (29 Sep 2026)

- **Usable battery + real-world Wh/mi**: EV Database UK cheatsheets, fetched today. Real-world combined figures, not WLTP — deliberately, so our cost numbers are honest.
- **AC/DC charging kW**: checked one by one against the EV Database UK car pages where a doubt existed. Corrections made today:

| Car | Was | Now (verified) |
|---|---|---|
| Tesla Model Y RWD | 170 kW DC | **175 kW** |
| Audi Q4 e-tron 45 (59 kWh) | 145 kW DC, heat pump optional | **160 kW**; heat pump standard from MY2026 |
| Audi Q6 e-tron quattro | 270 kW | **269 kW**; 22 kW AC optional |
| Hyundai IONIQ 5 63 kWh | 175 kW | **195 kW** |
| Hyundai IONIQ 5 84 kWh | 258 kW | **263 kW** |
| Mercedes CLA 200 | — | 200 kW, LFP, 22 kW AC optional (confirmed) |
| BYD Seal 61.4 kWh Comfort | listed | **removed — not sold in the UK** |
| MG4 Urban Long Range (2026) | 271 Wh/mi, 120 kW | **264 Wh/mi, 87 kW DC**, 11 kW AC; Premium LR added (271 Wh/mi) |
| Skoda Elroq 60 / Enyaq 60 | — | 276 / 270 Wh/mi (cheatsheet) |

Confirmed without change: Tesla Model 3 (60 / 79 kWh, 218–232 Wh/mi, 11 kW AC), Audi Q6 e-tron RWD 225 kW, BYD Seal 82.5 kWh 150 kW.

**Still from manufacturer specs / memory rather than a page I opened today** (all low-risk, but if you know otherwise, change them):
- Tesla Model 3 RWD DC peak: Tesla says 170 kW; same pack as Model Y RWD which EV Database lists at 175. Page copy should say "up to 170 kW".
- Kia EV3: heat pump is standard on Long Range trims, not on Air Standard Range — check Kia UK if you want to state it.
- Volvo EX30 Extended Range: 22 kW AC (Volvo UK spec).
- Vauxhall Frontera Electric: 7.4 kW AC standard, 11 kW optional (Stellantis).
- BYD Dolphin Surf Active (30 kWh): 65 kW DC; AC may be 11 kW rather than 7 — confirm on BYD UK.
- Discontinued variants marked `legacy: true` (Leaf Mk2, Kona Mk1, ID.3 Pro/Pro S, MG4 SE/Trophy, Corsa-e 50 kWh, Q4 35, IONIQ 5 58 kWh, Polestar 2 FWD): well-documented cars, figures from the EV Database archive as I remember them. Worth a 5-minute skim, not a rebuild.

Formulas the pages will use:
- mi/kWh = 1000 ÷ Wh/mi
- Full charge from empty (kWh from the socket) = usable kWh ÷ 0.9
- Home charge time at 7 kW ≈ usable kWh ÷ 7 ÷ 0.9 hours (ignores the slow taper at the very top)
- Cost per mile = Wh/mi ÷ 1000 ÷ 0.9 × p/kWh

## 3. What people actually search (keyword targets)

Exact monthly volumes need Google Keyword Planner (free with a Google Ads account, no spend required) — worth 20 minutes once the pages are live. After ~4 weeks Search Console will show real queries and we tune from those. Until then, the patterns below are the ones that consistently appear for UK EV running-cost queries.

**Per-car page — title pattern:** `[Car] charging cost UK: per charge, per mile & per month (2026)`
Queries each page should answer, in this order on the page:
1. "how much does it cost to charge a [car]" / "[car] charging cost"
2. "[car] cost per mile" / "[car] running costs"
3. "how long to charge [car] at home" / "[car] charging time 7kw"
4. "[car] full charge cost" / "[car] battery size kwh"
5. "[car] cheapest tariff" / "[car] octopus intelligent go"
6. "[car] real range" / "[car] miles per kwh"
7. "is a [car] cheaper than petrol" / "[car] vs petrol running costs"

**Per-tariff page — title pattern:** `[Tariff] review 2026: rates, hours, who it suits & what you'd pay`
Queries:
- "[tariff] rate", "[tariff] hours", "[tariff] compatible cars/chargers"
- "[tariff] vs [other tariff]" — especially *Intelligent Octopus Go vs EDF GoElectric*, *Octopus Go vs Intelligent Octopus Go*, *OVO Charge Anytime vs Octopus*
- "[tariff] worth it", "[tariff] exit fee", "[tariff] standing charge"
- "best ev tariff no smart charger" (EDF/Octopus Go win this), "ev tariff without compatible car"

**Site-wide informational pages worth adding soon** (high volume, low competition):
- "cost to charge electric car UK 2026" (the homepage already targets this)
- "electric car cost per mile vs petrol vs diesel"
- "how much does a home charger cost to install UK"
- "public charging cost per kwh UK" (Tesla Supercharger, Instavolt, Gridserve, BP Pulse prices)
- "does an EV tariff make the rest of my house more expensive" (the peak-rate question — nobody answers it well)

## 4. Comparison pages — first 10 pairs
Pick pairs people genuinely cross-shop and that Google shows "vs" suggestions for:
1. Tesla Model 3 vs Polestar 2
2. Tesla Model Y vs Skoda Enyaq
3. Tesla Model Y vs Kia EV6
4. MG4 vs Renault 5
5. MG4 vs Vauxhall Corsa Electric
6. Kia EV3 vs Volvo EX30
7. Skoda Elroq vs Kia EV3
8. BYD Seal vs Tesla Model 3
9. Hyundai IONIQ 5 vs Kia EV6
10. Nissan Leaf vs MG4 (used-buyer pair)
Tariffs: Intelligent Octopus Go vs EDF GoElectric; Octopus Go vs Intelligent Octopus Go; E.ON Next Drive vs Intelligent Octopus Go.

## 5. Tariff pages — the 8 to build
Same data as the calculator's `TARIFFS` block plus, per page: who's eligible, smart-charging requirement, window length, peak rate and the "whole-house" effect, exit fees, a worked example for a typical (8,000-mile, 3.5 mi/kWh) driver, and the affiliate button.
Intelligent Octopus Go · Octopus Go · EDF GoElectric · E.ON Next Drive Smart · British Gas EV Power · Utility Warehouse EV · OVO Charge Anytime · Standard price cap (explainer: "why the cap is the wrong tariff for an EV").

## 6. Quality rules for every generated page (so this is never "spam")
- Real, model-specific numbers in the first screen (battery, efficiency, charge time, per-charge cost).
- At least 2–3 sentences that could only be written about *this* car (from `notes` in cars.json — expand, don't copy).
- Variant selector where the model has meaningfully different batteries; default to the most common UK variant.
- A "last checked" date and a one-line source note.
- Internal links: car → 2–3 comparison pairs, car → best tariff for that car, tariff → 5 most popular cars.
- No page under ~400 words of real content; no two pages with the same paragraph.

## 7. Your checklist before tonight
- [ ] Open `cars.json`, scan the `verify` flags — fix anything you know is wrong.
- [ ] Decide the site name to show in titles ("EV Charge Cost" is fine; change now if you want a brand).
- [ ] Awin application (5 min): awin.com → Publisher sign-up → site evchargecost.co.uk → category Utilities/Energy + Automotive.
