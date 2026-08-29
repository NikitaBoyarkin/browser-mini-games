# 🕹️ Browser Mini-Games

Playable browser mini-games — some about analytics, some just for fun. Each game is a **self-contained SVG** (HTML + CSS + JS embedded, zero dependencies, no build step). Works on phone (swipe / drag / tap) and desktop (keyboard / mouse).

## 🎮 Games

| Game | File | How to play | Goal |
|------|------|-------------|------|
| 🐍 Snake | [`snake.svg`](snake.svg) | Swipe / arrows | Eat, grow, don't crash |
| 🏓 Pong | [`pong.svg`](pong.svg) | Drag / W·S | Beat the CPU — first to 11 |
| 🔢 2048 | [`2048.svg`](2048.svg) | Swipe / arrows | Merge tiles to reach 2048 |
| 🧪 A/B Test | [`ab-test.svg`](ab-test.svg) | Tap / click | Collect data until p < 0.05 |
| 🔻 Funnel Drop | [`funnel-drop.svg`](funnel-drop.svg) | Drag / ←·→ | Catch falling users to convert |

## ▶️ How to run

Open the [arcade hub](index.html) in any browser, or open any `.svg` directly — no server, no dependencies.

```bash
open index.html        # macOS
xdg-open index.html    # Linux
```

## 📦 Stack

- Pure SVG + embedded vanilla JS — each file is the whole game
- Shared arcade hub (`index.html`) with dark / light / cyberpunk themes
- No frameworks, no bundlers, no external requests (except optional PostHog analytics)

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

## 🔑 PostHog key (required for analytics)

Analytics are off until you insert your **client-side** PostHog key (a public `phc_…` token — it ships in the browser, so it is not a secret).

Replace the placeholder `__PH_KEY__` in `index.html` and every `.svg`:

```bash
# one-shot across all files (key from your .env, value never printed)
KEY=$(grep '^PUBLIC_POSTHOG_KEY=' ../<path-to-portfolio>/.env | cut -d= -f2 | tr -d '"' )
sed -i '' "s/__PH_KEY__/$KEY/g" index.html *.svg
```

Without the key the games work fully — retention + contacts included; only analytics are skipped.

## 📜 License

[MIT](LICENSE)
