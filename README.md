# 🕹️ Browser Mini-Games

Playable browser mini-games — some about analytics, some just for fun. The arcade **hub is built with Astro**; each game is a **self-contained SVG** (HTML + CSS + JS embedded, zero dependencies, no build step). Works on phone (swipe / drag / tap) and desktop (keyboard / mouse).

## 🎮 Games

Self-contained games live in [`public/`](public/) (SVG files are copied as-is, one file = the whole game). The hub is `src/pages/index.astro`.

| Game | File | How to play | Goal |
|------|------|-------------|------|
| 🐍 Snake | [`snake.svg`](public/snake.svg) | Swipe / arrows | Eat, grow, don't crash |
| 🏓 Pong | [`pong.svg`](public/pong.svg) | Drag / W·S | Beat the CPU — first to 11 |
| 🔢 2048 | [`2048.svg`](public/2048.svg) | Swipe / arrows | Merge tiles to reach 2048 |
| 🧪 A/B Test | [`ab-test.svg`](public/ab-test.svg) | Tap / click | Collect data until p < 0.05 |
| 🔻 Funnel Drop | [`funnel-drop.svg`](public/funnel-drop.svg) | Drag / ←·→ | Catch falling users to convert |
| 📊 Cohort Catch | [`cohort-catch.svg`](public/cohort-catch.svg) | Drag / ←·→ | Catch Returning users, dodge Churned |
| 🧩 SQL Query | [`sql-query.svg`](public/sql-query.svg) | Tap / click | Pick the token that completes the SQL |
| 🃏 Metric Match | [`metric-match.svg`](public/metric-match.svg) | Tap / click | Match metric pairs in fewest moves |
| 📅 Retention Day | [`retention-day.svg`](public/retention-day.svg) | Tap / click | Pick the right retention day |
| 🔍 Funnel Bottleneck | [`funnel-bottleneck.svg`](public/funnel-bottleneck.svg) | Tap / click | Find the biggest funnel drop |

## ▶️ How to run

```bash
npm install          # first time
npm run dev          # dev server (astro dev)
npm run build        # production build -> dist/
npm run preview      # preview the built site
```

You can also open any `.svg` directly in a browser — no server, no dependencies.

## 📦 Stack

- **Hub:** Astro v7, static output, deployed to GitHub Pages (`base: /browser-mini-games`)
- **Games:** pure SVG + embedded vanilla JS — each file is the whole game
- **Themes:** dark / light / cyberpunk via `data-theme` + `localStorage`
- The built `dist/` is fully self-contained (inline CSS/JS) — the hub works from any subpath, including the portfolio copy at `/games/`

## 🔄 Deploy & portfolio sync

**GitHub Pages:** `.github/workflows/deploy.yml` runs `npm ci && npm run build` and deploys `dist/` on push to `main`.

**Portfolio copy:** `Personal_Projects.github.io/public/games/` is a synced copy.

```bash
npm run build
python3 sync_games.py --dry-run   # preview what would change
python3 sync_games.py             # copy drift from dist/ -> ../Personal_Projects.github.io/public/games/
python3 sync_games.py --check     # CI-style check, exit 1 on drift
```

## 🧪 Tests

[`tests/test_games_smoke.py`](tests/test_games_smoke.py) loads each game from `public/` via Playwright (pytest). Requires `pytest` + `playwright`:

```bash
pip install pytest playwright && playwright install chromium
python3 -m pytest tests/ -v
```

## 📈 Retention & Contact design

Goal: bring users back daily and turn engagement into a contact request.

| Mechanic | Where | How it works |
|---|---|---|
| **Best score** | every game | `arcade_best_<game>` persisted in `localStorage`; shown in game HUD and hub card badge |
| **Daily challenge** | every game | each day a different game is "today's" game; finishing its goal fires `daily_completed` |
| **Streak** | hub | consecutive daily completions counted in `arcade_streak`, shown in the daily strip |
| **Contact CTA** | games + hub | on new best / daily done / win the game reveals LinkedIn + Telegram links; hub has a contact section |
| **Analytics** | all files | PostHog client-side events (see below) — no cookies, `IS_LOCAL` guard skips `localhost` |

**Events sent** (via PostHog): `game_started`, `game_over`, `game_win`, `sig_reached`, `milestone`, `best_broken`, `daily_completed`, `contact_click`, `game_selected`.

## 🔑 PostHog key

A public client-side `phc_…` token ships in the browser (not a secret). It is hardcoded in `src/components/PostHogInit.astro` and inside each SVG. The `IS_LOCAL` guard skips tracking on localhost; local-only development can also test via `lvh.me` (the Playwright suite does).

## 📜 License

[MIT](LICENSE)
