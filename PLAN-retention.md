# План: retention + contact intent для browser-mini-games

> Цель: чтобы игры удерживали пользователя и приводили к контакту.

---

## 1. Продуктовая гипотеза (FINER)

- **Feasible** — трафик бесплатный (GitHub Pages), доработки в рамках статического HTML/JS/SVG.
- **Interesting** — повышает ценность arcade как портфолио-штуки: видно прогресс и аналитику.
- **Novel** — сейчас нет retention-механик и нет контакт-CTA в момент победы.
- **Ethical** — только опциональные localStorage + публичная аналитика PostHog.
- **Relevant** — нативно связано с личным брендом аналитика/продукта.

**Гипотеза:** если добавить persistent best score, ежедневный челлендж + streak и контекстный контакт-CTA при new best, то пользователь чаще возвращается и чаще идёт в контакт.

---

## 2. Метрики

| Тип | Метрика | Как считать |
|---|---|---|
| North Star | **WAP** — weekly active players | Unique `distinct_id` с событием `game_started` за 7 дней |
| Leading | **D1 retention** | Вернувшиеся в игры в течение 24ч после первого `game_started` |
| Lagging | **D7 retention** | Вернувшиеся в течение 7 дней |
| Secondary | **best_broken rate** | Доля `game_over` с `new_best: true` |
| Secondary | **daily_completed** | Событие при выполнении дневного челленджа |
| Counter | **contact_click** | Клики по контакт-ссылкам в играх и hub |

---

## 3. Scope изменений

> 8 файлов. Каждый изменение — retention/contact/аналитика. Геймплей не трогаем.

| Файл | Что изменится | Почему |
|---|---|---|
| `index.html` | PostHog init; best score badges на карточках; daily challenge strip; contact CTA; capture событий | Hub должен возвращать |
| `snake.svg` | localStorage best; NEW BEST overlay; daily check; contact CTA на game over; PostHog events | Retention внутри игры |
| `2048.svg` | localStorage best; NEW BEST overlay; daily check; contact CTA на game over; PostHog events | Retention внутри игры |
| `pong.svg` | localStorage best streak/score; NEW BEST overlay; daily check; contact CTA; PostHog events | Retention внутри игры |
| `ab-test.svg` | localStorage best (fastest p<0.05); daily check; contact CTA; PostHog events | Retention внутри игры |
| `funnel-drop.svg` | localStorage best (conversions); daily check; contact CTA; PostHog events | Retention внутри игры |
| `README.md` | Разделы metrics, retention design, analytics events | Документация для портфолио |
| `.github/workflows/deploy.yml` | Без изменений | static deploy уже работает |

---

## 4. Механики retention

### 4.1 Best score (localStorage)
- Ключ: `arcade_best_<game>`.
- Сохраняется при `game_over`, если score лучше предыдущего.
- На экране game over — текст "NEW BEST!" + `Best: N`.
- В hub — badge в каждой карточке: `Best: N`.

### 4.2 Daily challenge + streak
- Каждый день одна игра становится "daily" (простая ротация по дням недели × неделе месяца).
- Цели:
  - Snake: ≥ 100 очков
  - 2048: получить плитку ≥ 512
  - Pong: победить CPU
  - A/B Test: достичь p < 0.05 за ≤ N taps
  - Funnel Drop: конвертировать ≥ N "пользователей"
- Ключи: `arcade_daily_date` (YYYY-MM-DD), `arcade_daily_completed` (bool), `arcade_streak` (int).
- Streak: +1 за выполнение daily подряд; сброс если пропустил день.
- В hub — strip: "Сегодня: 🐍 Snake 100+ — 🔥 streak 3".

### 4.3 Hub как retention-интерфейс
- Карточки показывают best + сегодняшний daily-статус.
- Если daily не выполнен — визуальный акцент (border/dot), чтобы тянуло вернуться.

---

## 5. Механики контакта

### 5.1 Контакт-CTA в момент победы
- При `game_over` + `new_best: true` появляется небольшой блок:
  - "🎉 New best! Need analytics/games like this?"
  - `[LinkedIn]` `[Telegram]`
- Не мешает restart.
- Capture: `contact_click` с `location: game_over`, `game: <name>`.

### 5.2 Hub CTA
- Новая секция под карточками или в footer:
  - "Сделаю такие штуки для продукта / аналитики"
  - `[LinkedIn]` `[Telegram]`
- Capture: `contact_click` с `location: hub`.

### 5.3 Ссылки
- Telegram: `https://t.me/lofinibo`
- LinkedIn: `https://www.linkedin.com/in/nikita-boyarkin`

---

## 6. Аналитика (PostHog)

### 6.1 Конфиг
- Тот же проект, что и в портфолио: `PUBLIC_POSTHOG_KEY` + `https://us.i.posthog.com`.
- `IS_LOCAL` guard: при `localhost/127.0.0.1/::1` не инициализируем (как в портфолио).
- client-side init через inline script в `index.html`; игры используют `window.posthog` (если есть).

### 6.2 События

| Событие | Свойства |
|---|---|
| `game_started` | `game`, `from_hub: true/false` |
| `game_over` | `game`, `score`, `best`, `new_best: bool` |
| `best_broken` | `game`, `old_best`, `new_best`, `score` |
| `daily_completed` | `game`, `streak` |
| `contact_click` | `location`, `channel`, `game` (если в игре) |
| `theme_switched` | `theme` (existing) |

---

## 7. Реализационные ограничения

- SVG-игры **self-contained** по дизайну проекта. Поэтому общий retention-код будет заинлайнен в каждый SVG как маленький helper. Дублирование минимально (~20–30 строк inline).
- Не добавляем новые внешние зависимости: PostHog загружается по CDN, vanilla JS.
- Не меняем механику игр, баланс, управление, визуальный стиль.
- Git: коммит по запросу, push только после явного approve.

---

## 8. Проверка (definition of done)

- [ ] `index.html` открывается локально, theme-toggle работает.
- [ ] В hub видны best scores и daily strip.
- [ ] Игра (любая) сохраняет best в localStorage; new best показывает "NEW BEST!" + CTA.
- [ ] Daily challenge выполняется при достижении порога; streak обновляется.
- [ ] PostHog не инициализируется на `localhost` (dev tools Network — нет запросов к us.i.posthog.com).
- [ ] README описывает retention и analytics events.
- [ ] `ruff`/линтер не применим (нет Python). Валидируем HTML вручную / открытием в браузере.

---

## 9. Риски

- **Большой diff в 5 SVG.** Решение: одинаковый helper, пошаговая проверка каждой игры.
- **PostHog публичный key.** Это норма для client-side, но коммитим только placeholder/instruction; реальный key можно оставить в `.env` и подставлять через deploy? Для static GitHub Pages — проще заинлайнить публичный token. Решение: пишем его в `index.html` как в портфолио (Astro тоже bake'ит его на build).
- **localStorage quota.** Минимальные данные, без риска.

---

## 10. Первый шаг после approve

1. Backup git state.
2. Изменить `index.html` (PostHog + hub UI).
3. Изменить `snake.svg` как пилот (полный retention-набор).
4. Протестировать snake.
5. Скопировать pattern в остальные 4 SVG.
6. Обновить README.
7. Финальная проверка всех 5 игр.
