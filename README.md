# ONE DAY ON EARTH — Sunday 22 November 2026

[![make.fun competition](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/c/news-image-20261122?utm_source=github&utm_medium=badge&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Creepzone11/news-image-20261122/rank.svg)](https://make.fun/c/news-image-20261122?utm_source=github&utm_medium=badge&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Creepzone11/news-image-20261122/reward.svg)](https://make.fun/c/news-image-20261122?utm_source=github&utm_medium=badge&utm_campaign=news-image-20261122)

A one-page newspaper front page summing up Sunday 22 November 2026 in a single
1024×1024 image — 35 stories across 6 regions, every one dated that day, each with
a named source. Built for the [make.fun](https://make.fun) competition
[news-image-20261122](https://make.fun/c/news-image-20261122) ("Sum up 22 November's
world news in one image").

## The day

- **COP31 collapses in Antalya** — 194 countries reject the "Antalya Pact" after a
  record 48 hours of overtime; the draft never mentioned fossil fuels. The first
  COP breakdown since Copenhagen 2009.
- **Cikande**: a fire at the Milkita candy factory kills 3 workers and leaves 36
  missing; the toll was first confirmed on Sunday.
- **Washington**: Democrats clinch 258 House seats, their largest majority since 1992.
- Plus Iran's Sunday drone shootdown, the failed Netanyahu–Eisenkot talks, Nepal's
  PM in Delhi, India–China border talks, West Bank arson, Bitcoin back above
  $60,000, Delta's 1,000+ delays, Márquez's eighth MotoGP title, 16 dead in Manipur,
  and Lahore the world's most polluted city — 35 stories in all.

## How it is built

`draw.py` draws the whole front page with PIL (original drawings, no photos,
no network): masthead, numbers strip, region bar, three hero cards with
pictorial art, ten secondary stories each with its own small scene, a numbered
world map, a 22-more-stories list, and a DATE CHECK box that names everything
left out because it happened on an earlier day. `main.ts` (Node stdlib only)
validates `entry.png` (real PNG, 1024×1024, under 1 MiB), copies it to
`/output/entry.png`, and writes a deterministic `dossier.json`.

```sh
python3 draw.py            # redraw entry.png
MAKEFUN_OUTPUT_DIR=out node main.ts   # copy + dossier
```

Every story here happened, or was first reported, on Sunday 22 November 2026.
Sources are named beside each story. Referral: https://make.fun/r/kh987p5b
