# PRD: Browser Mini-Games — портфолио-аркада по аналитике

**Автор:** Nikita Boyarkin
**Дата:** 2026-09-02
**Статус:** Approved (v1 реализована)
**Версия:** 1.0

---

## 1. Executive Summary

Портфолио аналитика сложно показать интерактивно: рекрутер видит статичные кейсы и дашборды, но не видит, как аналитик мыслит. Решение — браузерная аркада из 8 self-contained SVG-игр, где 5 игр обучают аналитическим концепциям (A/B-тесты, funnels, cohorts, SQL, метрики) в игровой форме, а retention-механики (best score, daily challenge, streak) возвращают пользователя. Ожидаемый эффект: интерактивная витрина скиллов + контакт-CTA в момент победы → конверсия в контакт с рекрутером.

## 2. Problem Statement

### Текущая ситуация
Портфолио-проекты (volta-banking, fit-trek) — статичные отчёты и дашборды. Рекрутер не вовлекается и не запоминает кандидата. Нет интерактивного артефакта, который демонстрирует продуктовое мышление и аналитические скиллы в действии.

### Влияние на пользователя
- **Кто затронут:** рекрутеры и нанимающие менеджеры BI/DA-позиций.
- **Как затронут:** не могут оценить аналитические скиллы в действии; кандидат не выделяется среди сотен откликов.
- **Серьёзность:** Medium — влияет на конверсию отклика в интервью.

### Бизнес-влияние
- **Стоимость проблемы:** пропущенные интервью, слабый личный бренд.
- **Стратегическая важность:** аркада — часть портфолио-системы (Personal_Projects.github.io), усиливает остальные кейсы и даёт повод для контакта.

### Почему решать сейчас
- Технологии готовы: SVG + vanilla JS, zero-deps, GitHub Pages — бесплатно и без build-шага.
- Уникальность: мало кто из кандидатов делает интерактивные обучающие артефакты.
- Retention-механики уже спроектированы (PLAN-retention.md) и реализованы.

## 3. Goals & Success Metrics

### Goal 1: Интерактивная витрина аналитических скиллов
- **Описание:** рекрутер играет в аналитические игры и видит глубину знаний.
- **Метрика:** WAP (weekly active players) — unique `distinct_id` с событием `game_started` за 7 дней.
- **Baseline:** не измерено (запуск).
- **Target:** ≥ 20 WAP через 4 недели после публикации.
- **Срок:** 4 недели после публикации.
- **Метод измерения:** PostHog.

### Goal 2: Возвращаемость
- **Описание:** daily challenge + streak возвращают пользователя.
- **Метрика:** D1 retention — вернувшиеся в игры в течение 24ч после первого `game_started`.
- **Baseline:** не измерено (запуск).
- **Target:** ≥ 30%.
- **Срок:** 4 недели после публикации.
- **Метод измерения:** PostHog.

### Goal 3: Конверсия в контакт
- **Описание:** CTA в момент победы и в hub приводят к контакту.
- **Метрика:** `contact_click` — клики по LinkedIn/Telegram.
- **Baseline:** не измерено (запуск).
- **Target:** ≥ 5 кликов/мес.
- **Срок:** 1 месяц после публикации.
- **Метод измерения:** PostHog.

## 4. User Stories

### Story 1: Рекрутер оценивает скиллы
**As a** рекрутер, **I want to** поиграть в A/B-тест и увидеть, как объясняется p-value, **So that I can** оценить глубину аналитических знаний кандидата.

**Acceptance Criteria:**
- [ ] A/B-игра доводит до p < 0.05 и объясняет результат.
- [ ] Игра запускается без инструкций и внешних зависимостей.
- [ ] На экране победы виден контакт автора.

**Dependencies:** REQ-001, REQ-003, REQ-006

### Story 2: Возвращение за daily challenge
**As a** посетитель, **I want to** выполнить ежедневный челлендж, **So that I can** поддерживать streak и возвращаться в аркаду.

**Acceptance Criteria:**
- [ ] Каждый день одна игра помечена как «сегодняшняя».
- [ ] Выполнение цели фиксируется как `daily_completed`.
- [ ] Streak виден в hub и растёт при подряд выполненных днях.

**Dependencies:** REQ-005

### Story 3: Контакт в момент победы
**As a** посетитель, **I want to** увидеть CTA после new best, **So that I can** связаться с автором, пока я вовлечён.

**Acceptance Criteria:**
- [ ] CTA появляется при `game_over` + `new_best: true`.
- [ ] CTA не мешает restart.
- [ ] Клик фиксируется как `contact_click` с `location: game_over`.

**Dependencies:** REQ-005, REQ-006

## 5. Functional Requirements

### Must Have (P0) — реализовано

#### REQ-001: Self-contained SVG-игры
**Описание:** каждая игра — один `.svg` файл со встроенными HTML/CSS/JS, без внешних зависимостей и build-шага.

**Acceptance Criteria:**
- [ ] Каждая игра открывается напрямую в браузере без сервера и без ошибок консоли.
- [ ] Игра работает на телефоне (swipe/tap/drag) и на десктопе (клавиатура/мышь).
- [ ] В файле нет внешних запросов, кроме опционального PostHog CDN.
- [ ] Размер каждого файла < 30 KB.

**Техническая спецификация:**
```
8 файлов: snake.svg, pong.svg, 2048.svg, ab-test.svg,
          funnel-drop.svg, cohort-catch.svg, sql-query.svg, metric-match.svg
```

**Task Breakdown:**
- [Игры]: реализовано (v1)
- [Тесты]: реализовано (REQ-007)

**Dependencies:** None

#### REQ-002: Arcade hub
**Описание:** `index.html` — единая точка входа с карточками игр, темами (dark/light/cyberpunk), best-бейджами и daily-стрипом.

**Acceptance Criteria:**
- [ ] Hub открывается локально (`file://`) и на GitHub Pages.
- [ ] Переключение темы работает и сохраняется.
- [ ] На карточках видны best score и статус daily challenge.
- [ ] Hub имеет контакт-секцию.

**Task Breakdown:**
- [Hub UI]: реализовано
- [Темы]: реализовано

**Dependencies:** REQ-001, REQ-005

#### REQ-003: Аналитические игры
**Описание:** 5 игр обучают аналитическим концепциям: A/B (p < 0.05), Funnel (конверсия), Cohort (retention), SQL (синтаксис), Metric Match (пары метрик).

**Acceptance Criteria:**
- [ ] A/B-тест собирает данные до p < 0.05 и показывает сигнификантность.
- [ ] Funnel Drop конвертирует падающих «пользователей».
- [ ] Cohort Catch различает Returning и Churned.
- [ ] SQL Query заполняет пропущенный токен в запросе.
- [ ] Metric Match сопоставляет метрики парами за минимальное число ходов.

**Task Breakdown:**
- [Игры]: реализовано

**Dependencies:** REQ-001

#### REQ-004: PostHog аналитика
**Описание:** client-side события в PostHog; `IS_LOCAL` guard не инициализирует аналитику на localhost.

**Acceptance Criteria:**
- [ ] События: `game_started`, `game_over`, `game_win`, `sig_reached`, `milestone`, `best_broken`, `daily_completed`, `contact_click`, `game_selected`, `theme_switched`.
- [ ] На `localhost`/`127.0.0.1`/`::1` PostHog не инициализируется (нет запросов к `us.i.posthog.com`).
- [ ] Без ключа (placeholder `__PH_KEY__`) игры работают полностью, аналитика пропускается.
- [ ] Нет cookies, нет PII.

**Task Breakdown:**
- [Интеграция]: реализовано

**Dependencies:** None

#### REQ-005: Retention-механики
**Описание:** best score (`localStorage` `arcade_best_<game>`), daily challenge (ротация по дням), streak (`arcade_streak`).

**Acceptance Criteria:**
- [ ] Best сохраняется при `game_over`, если score лучше предыдущего.
- [ ] На экране game over — «NEW BEST!» + `Best: N`.
- [ ] Daily challenge: каждый день одна игра «сегодняшняя»; выполнение цели → `daily_completed`.
- [ ] Streak: +1 за подряд выполненные daily, сброс при пропуске дня.
- [ ] Ключи: `arcade_daily_date`, `arcade_daily_completed`, `arcade_streak`.

**Task Breakdown:**
- [Механики]: реализовано

**Dependencies:** REQ-001

#### REQ-006: Контакт-CTA
**Описание:** LinkedIn + Telegram ссылки в момент победы (new best / daily done / win) и в hub.

**Acceptance Criteria:**
- [ ] CTA появляется при `game_over` + `new_best: true`, не мешает restart.
- [ ] Hub имеет контакт-секцию.
- [ ] Клик → `contact_click` с `location` (game_over/hub) и `channel`.
- [ ] Ссылки: Telegram `https://t.me/lofinibo`, LinkedIn `https://www.linkedin.com/in/nikita-boyarkin`.

**Task Breakdown:**
- [CTA]: реализовано

**Dependencies:** REQ-005

#### REQ-007: Автотесты
**Описание:** Playwright smoke-тесты через `lvh.me` (не-localhost путь PostHog, как на GitHub Pages).

**Acceptance Criteria:**
- [ ] Каждая из 8 игр загружается без page errors, элемент рендерится, `window.posthog` инициализирован.
- [ ] Snake реагирует на клавишу; 2048 двигает плитки; Pong подаёт; A/B собирает клик; Funnel/Cohort спавнят точки; SQL заполняет токен; Metric считает ходы.
- [ ] `python3 -m pytest tests/ -v` — все тесты зелёные.

**Task Breakdown:**
- [Тесты]: реализовано (11 тестов)

**Dependencies:** REQ-001

#### REQ-008: Deploy и синк
**Описание:** GitHub Pages workflow + `sync_games.py` в `Personal_Projects.github.io/public/games`.

**Acceptance Criteria:**
- [ ] Пуш в `main` → авто-деплой на GitHub Pages.
- [ ] `sync_games.py --check` сообщает drift и завершается с exit 1 при расхождении.
- [ ] `sync_games.py` копирует изменённые файлы в портфолио-сайт.
- [ ] `--dry-run` показывает, что будет скопировано, без записи.

**Task Breakdown:**
- [CI/CD]: реализовано
- [Синк]: реализовано

**Dependencies:** REQ-001, REQ-002

### Should Have (P1) — roadmap

#### REQ-009: Новые аналитические игры
**Описание:** расширить каталог: retention curve, p-value simulator, cohort matrix.

**Acceptance Criteria:**
- [ ] Каждая новая игра проходит REQ-001 и REQ-007.
- [ ] Игра обучает ровно одной концепции.
- [ ] Игра добавлена в hub и в `FILES` в `sync_games.py`.

**Task Breakdown:**
- [Игра]: Medium (6-8h)
- [Тесты]: Small (2-4h)

**Dependencies:** REQ-001, REQ-007

#### REQ-010: Шеринг и leaderboard
**Описание:** share-кнопка результата + публичный leaderboard по каждой игре.

**Acceptance Criteria:**
- [ ] Поделиться результатом (score/best) копированием или в соцсеть.
- [ ] Leaderboard показывает топ-10 по каждой игре.
- [ ] Не требует авторизации (анонимный id).

**Task Breakdown:**
- [Шеринг]: Medium (4-6h)
- [Leaderboard]: Large (8-12h)

**Dependencies:** REQ-005

#### REQ-011: i18n RU/EN
**Описание:** переключение языка интерфейса.

**Acceptance Criteria:**
- [ ] Hub и игры имеют RU/EN строки.
- [ ] Переключатель языка в hub, выбор сохраняется.
- [ ] Дефолт по `navigator.language`.

**Task Breakdown:**
- [i18n]: Large (10-14h)

**Dependencies:** REQ-002

### Nice to Have (P2) — будущее улучшение

#### REQ-012: Звуковые эффекты
**Описание:** лёгкие звуки на события (победа, new best, ошибка), с отключением.

**Acceptance Criteria:**
- [ ] Звук на new best и win.
- [ ] Переключатель звука, выбор сохраняется.
- [ ] Без внешних аудио-файлов (WebAudio/синтез).

**Dependencies:** REQ-001

#### REQ-013: PWA / offline
**Описание:** service worker для офлайн-доступа к аркаде.

**Acceptance Criteria:**
- [ ] Аркада открывается офлайн после первого визита.
- [ ] Манифест с иконкой и названием.

**Dependencies:** REQ-002

#### REQ-014: Уровни сложности
**Описание:** сложность в аналитических играх (размер выборки, число шагов).

**Acceptance Criteria:**
- [ ] Минимум 2 уровня на игру.
- [ ] Прогресс уровня сохраняется.

**Dependencies:** REQ-003

## 6. Non-Functional Requirements

### Performance
- Загрузка каждой игры: < 1s (SVG < 30 KB).
- Hub: < 2s.
- Нет build-шага, zero-deps.

### Security
- Только client-side; публичный PostHog key (`phc_…`) — не секрет.
- `localStorage`: только best/daily/streak, без PII.
- Нет cookies.

### Scalability
- GitHub Pages static — достаточно для портфолио-трафика.
- PostHog: бесплатный тир.

### Reliability
- Игры работают без сети (кроме PostHog).
- Без ключа — полный функционал.

## 7. Technical Considerations

### Архитектура
```
browser-mini-games/
├── *.svg                    # 8 игр, self-contained (HTML+CSS+JS inline)
├── index.html               # arcade hub (темы, карточки, daily strip)
├── sync_games.py            # синк → Personal_Projects.github.io/public/games
├── tests/test_games_smoke.py# Playwright smoke (11 тестов)
└── .github/workflows/       # GitHub Pages deploy
```

### Технологический стек
- **Frontend:** SVG + vanilla JS, zero-deps.
- **Analytics:** PostHog (CDN, client-side).
- **CI/CD:** GitHub Pages.
- **Тесты:** pytest + Playwright.

### Внешние зависимости
1. **PostHog:** аналитика; CDN; `IS_LOCAL` guard; fallback — без ключа всё работает.

### Тестирование
- E2E: Playwright smoke (11 тестов) через `lvh.me`.
- Валидация: открытие в браузере, dev tools Network (нет запросов на localhost).

## 8. Implementation Roadmap

### Phase 1: Foundation (DONE)
**Goal:** 8 игр + hub + деплой.
**Tasks:**
- [x] 8 self-contained SVG-игр (REQ-001, REQ-003)
- [x] Arcade hub с темами (REQ-002)
- [x] GitHub Pages deploy + sync_games.py (REQ-008)
**Validation Checkpoint:** все игры открываются, hub работает, деплой зелёный.

### Phase 2: Retention & Analytics (DONE)
**Goal:** возвращаемость + контакт + измерение.
**Tasks:**
- [x] Best score, daily challenge, streak (REQ-005)
- [x] Контакт-CTA (REQ-006)
- [x] PostHog события + IS_LOCAL guard (REQ-004)
- [x] Playwright smoke-тесты (REQ-007)
**Validation Checkpoint:** retention работает, PostHog не инициализируется на localhost, тесты зелёные.

### Phase 3: Portfolio polish (PLANNED)
**Goal:** усилить витрину и шеринг.
**Tasks:**
- [ ] OG-теги и превью для шеринга ссылки (REQ-010, часть)
- [ ] Share-кнопка результата (REQ-010)
- [ ] 1 новая аналитическая игра (REQ-009)
**Validation Checkpoint:** WAP ≥ 20 через 4 недели; D1 ≥ 30%; contact_click ≥ 5/мес.

### Phase 4: Expansion (FUTURE)
**Goal:** масштаб и локализация.
**Tasks:**
- [ ] i18n RU/EN (REQ-011)
- [ ] Leaderboard (REQ-010)
- [ ] PWA / offline (REQ-013)
- [ ] Звук (REQ-012)
**Validation Checkpoint:** D7 retention ≥ 10%; рост WAP после i18n.

### Зависимости задач
```
Phase 1 → Phase 2 → Phase 3 → Phase 4
Critical Path: REQ-001 → REQ-005 → REQ-010
```

### Оценка усилий
- Phase 1: реализовано
- Phase 2: реализовано
- Phase 3: ~12-16h
- Phase 4: ~24-32h
- **Итого (осталось):** ~36-48h
- **Риск-буфер:** +20%

## 9. Out of Scope

1. **Backend и авторизация** — статический сайт, анонимность; leaderboard без аккаунтов.
2. **Нативные мобильные приложения** — только браузер.
3. **Монетизация** — портфолио-проект, цель — контакт, не выручка.
4. **Изменение геймплея существующих игр** — баланс и механики заморожены.

## 10. Open Questions & Risks

### Open Questions

#### Q1: Публиковать ли реальный PostHog key в репо?
- **Статус:** решено — client-side key не секрет (как в Astro-портфолио), заинлайнен в `index.html` и `.svg`.
- **Влияние:** Low.

#### Q2: Нужен ли leaderboard без авторизации?
- **Статус:** открыт.
- **Варианты:** (A) анонимный id в localStorage, (B) отложить до i18n, (C) не делать.
- **Владелец:** автор.
- **Влияние:** Medium.

### Risks & Mitigation

| Риск | Вероятность | Влияние | Severity | Митигация | Контингенция |
|------|-------------|---------|----------|-----------|--------------|
| Большой diff в SVG при новых механиках | Medium | Medium | Medium | общий inline-helper, пошаговая проверка каждой игры | откат к прошлому коммиту |
| PostHog key в публичном репо | Low | Low | Low | client-side key не секрет | ротация ключа |
| Низкий трафик (портфолио) | High | Medium | Medium | OG-теги, шеринг, LinkedIn-пост | расширить каталог игр |
| Дрейф синка с портфолио-сайтом | Low | Low | Low | `sync_games.py --check` в CI | ручной синк |

## 11. Validation Checkpoints

### Checkpoint 1: Конец Phase 2 (DONE)
**Критерии:**
- [x] Все 8 игр проходят smoke-тесты.
- [x] Retention работает (best/daily/streak).
- [x] PostHog не инициализируется на localhost.
**Если провален:** фикс до публикации.

### Checkpoint 2: Конец Phase 3
**Критерии:**
- [ ] WAP ≥ 20 через 4 недели.
- [ ] D1 retention ≥ 30%.
- [ ] contact_click ≥ 5/мес.
**Если провален:** усилить шеринг/распространение, добавить игру.

---

**Конец PRD**
