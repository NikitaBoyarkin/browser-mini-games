# Plan: Astro rewrite for browser-mini-games

**Chosen approach:** A — Astro hub + self-contained SVG games in `public/`.

**Why:** PRD defines each game as a self-contained SVG (REQ-001) with zero external deps and no build step. Converting 8 games into Astro components would invalidate that core property, multiply the test/bug surface, and break the `sync_games.py` path into the Astro portfolio (`public/games/` keeps `.svg` files). Keeping the games as static assets and rewriting only the hub gives us Astro's component model, build pipeline, OG tags, and i18n readiness while preserving every existing game URL and behavior.

---

## 1. Goal

Replace the hand-written `index.html` hub with an Astro static site while preserving the 8 SVG games unchanged and keeping the same runtime behavior (themes, daily challenge, best scores, PostHog, contact CTA).

## 2. Files to create

| File | Purpose |
|---|---|
| `astro.config.mjs` | Static output, `base: '/browser-mini-games'`, site URL, sitemap (optional) |
| `package.json` | Astro v7.x, `posthog-js`, npm scripts |
| `tsconfig.json` | Standard Astro TS |
| `src/layouts/Base.astro` | HTML shell, meta tags, theme anti-flash script |
| `src/components/ThemeToggle.astro` | dark/light/cyberpunk toggle + persistence |
| `src/components/GameCard.astro` | Game card (thumb, title, controls, goal, best badge, play link) |
| `src/components/DailyStrip.astro` | Daily challenge strip with streak status |
| `src/components/ContactCTA.astro` | Hub contact section |
| `src/components/Footer.astro` | Social links + source/portfolio links |
| `src/components/PostHogInit.astro` | Client-side PostHog init with `IS_LOCAL` guard |
| `src/components/RetentionScript.astro` | localStorage best/daily/streak logic + event wiring |
| `src/pages/index.astro` | Hub page composing all components |
| `src/styles/global.css` | CSS variables for themes + base layout |
| `public/*.svg` (8 files) | Copy existing games as static assets |
| `public/robots.txt` | Allow all |

## 3. Files to modify

| File | Change |
|---|---|
| `README.md` | Update stack/docs (Astro hub, SVG games, build/test commands) |
| `.github/workflows/deploy.yml` | Run `npm ci && npm run build`, deploy `dist/` |
| `sync_games.py` | Sync from `dist/` to portfolio `public/games/`; update `FILES` list if needed |
| `tests/test_games_smoke.py` | Target Astro dev server or built `dist/` instead of project root; keep tests otherwise unchanged |

## 4. Files to remove

| File | Reason |
|---|---|
| `index.html` (root) | Becomes `src/pages/index.astro` → built `dist/index.html` |

## 5. Technical decisions

- **Base path:** `base: '/browser-mini-games'` in `astro.config.mjs` so all relative links work both on `nikitaboyarkin.github.io/browser-mini-games/` and when synced into the portfolio subpath.
- **Games:** copied to `public/*.svg`. Astro copies `public/` as-is, so URLs like `/snake.svg` stay valid and games remain openable directly.
- **Analytics:** use the same public PostHog key via `import.meta.env.PUBLIC_POSTHOG_KEY`; bake in a fallback if env is absent. Keep `IS_LOCAL` guard identical to current regex.
- **Theme anti-flash:** inline `<script is:inline>` in `Base.astro` runs before first paint, same logic as current `index.html`.
- **Retention JS:** inline `<script is:inline>` at the bottom of `index.astro` reads/writes the same localStorage keys (`arcade_best_*`, `arcade_daily_date`, `arcade_daily_done`, `arcade_streak`).
- **No framework islands:** no React/Svelte needed; the only JS is the existing inline logic, now split across components.
- **Styling:** CSS variables on `:root` + `[data-theme="..."]`; move component-specific styles into `<style>` blocks inside Astro components to keep co-location.

## 6. Verification plan

1. `npm install` succeeds.
2. `npm run build` produces `dist/` with `dist/index.html` + 8 SVGs.
3. `npm run dev` serves the hub locally; manual check: theme toggle, daily strip, cards, contact section render.
4. `npm test` (or `python3 -m pytest tests/ -v`) passes with updated Playwright paths.
5. `python3 sync_games.py --dry-run` reports the expected copy set.
6. Compare current `index.html` output with built `dist/index.html` for visible regressions (text content, links, IDs used by tests).
7. Open one SVG directly from `dist/` to confirm it still works standalone.

## 7. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Theme flash if anti-flash script misses | Keep the exact inline pre-paint script from current `index.html` |
| PostHog not initializing on non-localhost dev | Test on `lvh.me` via Playwright, same as current tests |
| Broken relative links after `base` path | Use `import.meta.env.BASE_URL` for root links; keep game card `href` as relative `.svg` |
| Sync to portfolio breaks | Update `sync_games.py` to read from `dist/` and validate with `--check` |
| Tests fail because element IDs moved | Preserve all test-critical IDs (`score`, `status`, `overlay`, `ball`, `#tiles text`, `#dots circle`, `#opts rect`, `#board g`, `daily-text`, etc.) |

## 8. Out of scope

- Converting SVG games to Astro components (would be follow-up work requiring per-game rewrite).
- Adding i18n in this pass; Astro i18n can be wired in a later phase if desired.
- PWA/service worker (future PRD REQ-013).
- New games or game mechanics.

## 9. Estimated effort

- Setup + config: 1 h
- Layout + components: 3–4 h
- Hub page assembly + styling: 2 h
- Update sync/tests/deploy: 1–1.5 h
- Verification + fixes: 1–1.5 h
- **Total: ~8–10 h**

---

**Next step:** user approval, then create branch and implement.
