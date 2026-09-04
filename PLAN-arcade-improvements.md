# PLAN: Arcade improvements — WH Arcade reference + PRD roadmap

**Дата:** 2026-09-04
**Статус:** Draft (на утверждение)
**Источник:** референс whitehouse.gov/arcade + собственный PRD (`docs/prd.md`, Phase 3–4)

---

## 0. Референс: что даёт whitehouse.gov/arcade

| WH Arcade элемент | В проекте сейчас | Разрыв | Ценность |
|---|---|---|---|
| Тематические группы игр (граница/экономика/здоровье) | Плоская сетка 10 карточек | Нет категорий/фильтров | **High** — навигация по 10 играм |
| Карточки с превью-скриншотом | Есть (SVG как статичный `img`) | Превью статично (первый кадр) | Medium — hover-анимация |
| «Coming Soon» карточка | Нет | Нет анонса следующей игры | Low — сигнал активности |
| Featured-карусель | DailyStrip (текстовый) | Нет hero-блока | Medium |
| Отдельные страницы игр `/arcade/<game>/` | Прямые ссылки на `.svg` | Нет навигации назад, нет OG, нет инструкций | **High** — UX + шеринг |
| Простые казуальные жанры | Есть (10 игр) | — | — |

**Что НЕ брать:** политическая тематика; карусель-ротация (для 10 игр не нужна); отдельные страницы как обязательный паттерн (конфликт с self-contained SVG, см. §2.3).

---

## 1. Quick wins (P0) — витрина hub, ~4–6h

### 1.1 Категории и фильтры
- Разбить 10 игр: **Analytics** (ab-test, funnel-drop, cohort-catch, sql-query, metric-match, retention-day, funnel-bottleneck) и **Classic** (snake, pong, 2048).
- Filter chips: All / Analytics / Classic + сортировка (по best, по названию).
- **Файлы:** `src/pages/index.astro` (поле `category` в GAMES), `src/components/GameCard.astro` (`data-category`), inline-скрипт фильтрации.
- **Проверка:** клик по чипу фильтрует сетку без перезагрузки; активный чип подсвечен.

### 1.2 «Coming Soon» карточка
- Teaser следующей игры из REQ-009 (retention curve / p-value simulator / cohort matrix).
- **Файлы:** `src/components/ComingSoon.astro`, вставка в grid.
- **Проверка:** карточка рендерится, не кликабельна (или ведёт на PRD).

### 1.3 Общий прогресс
- «X/10 games played» + суммарный best в шапке или под DailyStrip.
- Считать игры с `arcade_best_*` > 0 (уже в localStorage, без новых событий).
- **Файлы:** inline-скрипт в `index.astro`.
- **Проверка:** счётчик растёт после игры.

### 1.4 Hover-превью
- На hover карточки — движение вместо статичного кадра.
- **Вариант A (рекомендую):** CSS-эффект на существующем превью (zoom/pan/лёгкая анимация) — дёшево, без новых файлов.
- **Вариант B:** отдельные мини-демо SVG (10 файлов) — дорого, отложить.
- **Файлы:** `src/components/GameCard.astro` (CSS).
- **Проверка:** hover показывает движение; `prefers-reduced-motion` отключает.

---

## 2. Retention & sharing (P1) — ~8–12h

### 2.1 Достижения/бейджи
- localStorage `arcade_achievements`: «First win», «3-day streak», «Play all 10», «Perfect round».
- Секция бейджей на hub.
- **Файлы:** `src/components/Achievements.astro` + inline-скрипт.
- **Проверка:** достижение разблокируется и видно; событие `achievement_unlocked` в PostHog.

### 2.2 Share-кнопка результата (REQ-010, часть)
- Кнопка «Share score» на экране победы в SVG + в hub.
- Копирует текст: «I scored 200 in Snake at Nikita's arcade 🕹️».
- **Файлы:** правки в 10 SVG + hub; событие `share_click`.
- **Проверка:** клик копирует текст; `navigator.clipboard` с fallback.

### 2.3 OG-теги + навигация из игр
- **Сейчас:** `Base.astro` без OG → шеринг ссылки даёт пустую карточку. Плюс из SVG-игры нет выхода назад (grep: только localStorage-ключи `arcade_*`, ссылок нет).
- **Шаг 1 (быстро):** OG-теги в `Base.astro` (`og:title`, `og:description`, `og:image` — превью SVG).
- **Шаг 2 (решение):** два варианта навигации:
  - **A:** добавить «← Arcade» ссылку внутрь каждого SVG (10 правок, сохраняет self-contained, но дублирует код).
  - **B:** Astro-страницы-обёртки `/games/<game>/` с iframe-embed SVG + back-to-hub + инструкции + related games + per-game OG. Ломает «открыть SVG напрямую» как единственный путь, но даёт полноценные страницы (паттерн WH Arcade).
- **Рекомендация:** сначала Шаг 1 + вариант A (дёшево, закрывает главный UX-разрыв). Вариант B — отдельным решением, если нужен SEO/шеринг per-game.
- **Файлы:** `src/layouts/Base.astro`, 10 SVG (вариант A) или `src/pages/games/[game].astro` (вариант B).
- **Проверка:** share-тест в Telegram/Slack показывает карточку; из игры есть выход в hub.

---

## 3. PRD roadmap (P2) — ~16–24h

### 3.1 Leaderboard (REQ-010)
- Анонимный id в localStorage + PostHog (или Supabase, как в других портфолио-проектах).
- Топ-10 по каждой игре.
- **Файлы:** `src/components/Leaderboard.astro`, PostHog-события.
- **Проверка:** два браузера видят общий топ.

### 3.2 i18n RU/EN (REQ-011)
- Hub + игры. Дефолт по `navigator.language`.
- **Файлы:** `src/i18n/`, переключатель в шапке.
- **Проверка:** переключение без перезагрузки, выбор сохраняется.

### 3.3 PWA / offline (REQ-013)
- Service worker + manifest.
- **Файлы:** `public/sw.js`, `public/manifest.webmanifest`, регистрация в `Base.astro`.
- **Проверка:** аркада открывается офлайн после первого визита.

### 3.4 Звук (REQ-012)
- WebAudio-синтез на win / new best / ошибку, переключатель.
- **Файлы:** общий inline-helper в SVG.
- **Проверка:** звук на события, mute сохраняется.

---

## 4. Техдолг / CI — ~3–4h

### 4.1 Тесты в CI
- `deploy.yml` не гоняет pytest. Добавить шаг `python3 -m pytest tests/ -v` (или отдельный workflow).
- **Проверка:** красный тест блокирует деплой.

### 4.2 `sync_games.py --check` в CI
- Добавить шаг проверки дрейфа после build.
- **Проверка:** дрейф → exit 1.

### 4.3 Авто-добавление игр в FILES
- Сейчас `FILES` — хардкод; новая игра требует ручной правки. Заменить на glob `*.svg` + `index.html`.
- **Проверка:** новая игра попадает в синк без правки списка.

### 4.4 Доступность
- `prefers-reduced-motion` для hover-анимаций, aria-labels на фильтрах.
- **Проверка:** reduced-motion отключает анимации.

---

## 5. Out of scope

- Конвертация SVG в Astro-компоненты (ломает self-contained + `sync_games.py`).
- Изменение геймплея существующих игр (PRD §9.4).
- Backend / авторизация (PRD §9.1).
- Политическая тематика WH Arcade.

---

## 6. Приоритет и порядок

| Фаза | Что | Effort | Ценность |
|---|---|---|---|
| **P0** | Категории, Coming Soon, прогресс, hover | 4–6h | High (витрина) |
| **CI** | Тесты, sync-check, glob | 3–4h | High (надёжность) |
| **P1** | Достижения, share, OG + навигация | 8–12h | High (retention + шеринг) |
| **P2** | Leaderboard, i18n, PWA, звук | 16–24h | Medium (масштаб) |

**Рекомендуемый порядок:** P0 → CI → P1 → P2. P0 и CI независимы — можно параллельно.

**Метрики успеха (из PRD Checkpoint 2):** WAP ≥ 20 / 4 нед, D1 ≥ 30%, `contact_click` ≥ 5/мес. Категории и OG-теги напрямую влияют на WAP и шеринг; достижения и share — на D1 и контакт.
