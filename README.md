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
- No frameworks, no bundlers, no external requests

## 📜 License

[MIT](LICENSE)
