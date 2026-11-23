# Study — Sunday 22 November 2026 (news-image-20261122)

Layout engine inherited from the 21 Nov round 4 (judge 0.977797, rank 2395/18632):
masthead + numbers strip + region bar + 3 heroes + 10 pictured mid cards + numbered
map + 22-more list + dated DATE CHECK + verification badges. Fixes applied from the
r4 study: scene-like art in every mid card, de-collided map dots with leader lines
for the Europe/Middle-East cluster, DATE CHECK with a date on every exclusion.

## Verified story set (all happened or first reported Sun 22 Nov 2026)

Heroes:
1. COP31 COLLAPSE, Antalya — 194 countries reject the "Antalya Pact" after a record
   48h overtime; draft never mentioned fossil fuels; longest COP ever, first breakdown
   since COP15 Copenhagen 2009. CNN, Al Jazeera, Le Monde, The Hindu. CONFIRMED.
2. CIKANDE FIRE — Milkita candy plant (PT Fonusa Agung Mulia), Serang, Banten: 3 dead,
   36 missing, 300 inside; fire began Sat 21 Nov 5 p.m., toll first confirmed Sun.
   AP, Reuters, CNA. CONFIRMED.
3. DEMOCRATS 258 HOUSE SEATS — largest majority since 1992. Economic Times
   (23 Nov 00:01 IST = 22 Nov 18:31 UTC). REPORTED.

Mid (4–13): Iran downs MQ-1 drone Sunday, 4th in 24h, 20th since war began
(Al Jazeera); Netanyahu–Eisenkot coalition talks end Sunday with no deal (The Hindu);
Nepal PM Balendra Shah arrives Delhi, first official visit (The Hindu); India–China
10-day LoAC talks conclude (The Hindu); West Bank settler arson early Sunday,
Eisenkot calls it "Jewish terrorism" (The Hindu); Bitcoin $60,785 +1.2% Sun evening,
ether $1,720, Saturday low $55,100 (CoinGecko via Motley Fool, 21:16 UTC 22 Nov);
Delta 1,000+ flights delayed, weight-and-balance automation glitch (ET); Márquez
record-equalling 8th MotoGP title (NST); Manipur spurious liquor deaths rise to 16
(NST); Lahore world's most polluted city Sunday, AQI 289 (NST).

Also (14–35): COP31 final draft 44h late; Guterres "deeply disappointed"; Gaza strikes
kill 3, Hamas seeks emergency talks; Myanmar calls ASEAN review "unfair"; Shah on
border villages; US intel chief Clayton — Putin "not America's friend"; Minnesota
Somali fraud Senate hearing; Tom Jackson dies at 75; US probes alleged spy tied to
ex-Nvidia chief Huang; India women beat Thailand; Australia edge Wales 29-26 rugby;
NZ retail sales +2.2%; May tells successor to move on from Brexit; Takaichi cold
reception in China; Congress-SP talks; Sarawak DAP names 9 candidates; Tigresses
beat South Korea 3-1; AI growth lifts dollar; ICE detains father/daughter at Seattle
airport; Kennedy corners Trump nominee; Malaysia retain Asian bowling crown; 137
invasive redtail catfish caught in Pahang.

Regions: Europe 4, Asia 14, Middle East 4, Americas 9, Oceania 2, Global 2 = 35.
No verified Africa story found for 22 Nov; none invented.

## DATE CHECK (all excluded, dated)

Sat 21 Nov: Iran's strikes on US bases + industrial site in Bahrain (2 hurt);
EU–Indonesia trade deal signed in Brussels; "El Chapo Isidro" captured in Sinaloa
(11 killed); Kryvyi Rih missile strike; Hormuz tanker strikes; Cikande fire begins.
Fri 20 Nov: Wall Street's correction; the Shenzhen summit. Thu 19 Nov: ICJ Myanmar
genocide ruling. 18 Nov: Voyager 1's light-day. Not confirmed when drawn: the full
Cikande missing toll.

## Build checks

- entry.png 1024x1024, 237,205 bytes (< 1 MiB), valid PNG.
- main.ts (Node stdlib only) validates PNG + CRCs, copies, writes deterministic
  dossier.json; two runs produce identical sha256.
- Visual check: two render passes; fixed mid-card body truncation, DATE CHECK
  overflow, map-dot collisions, numbers-strip label.
