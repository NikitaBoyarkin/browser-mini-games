"""Static contract ratchet over the arcade's shared patterns.

These tests parse source text — they never run the games. Each one binds a
claim the project makes about itself, so fixing a regression is the only way
to get back to green. See the sibling test_games_smoke.py for behavioral tests.

Deliberately NOT covered (honest gaps, see PLAN-arcade-improvements.md):
  * SVG-namespace <script href> loader actually executing in Firefox/Safari.
  * sync_games.py drift check — needs the sibling Personal_Projects.github.io
    checkout, absent in CI. Not asserted here so the gate stays honest.
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SVG_DIR = ROOT / "public"
INDEX = ROOT / "src" / "pages" / "index.astro"
POSTHOG = ROOT / "src" / "components" / "PostHogInit.astro"
CARD = ROOT / "src" / "components" / "GameCard.astro"

SVGS = sorted(SVG_DIR.glob("*.svg"))
SVG_CASES = [(p.name, p.read_text()) for p in SVGS]
SVG_IDS = [p.name for p in SVGS]

RE_GAME = re.compile(r"var GAME = '([^']+)'")
RE_DAILY = re.compile(r"var DAILY_GAMES = \[([^\]]*)\]")
RE_FRONTMATTER_KEY = re.compile(r'gameKey:\s*"([^"]+)"')
RE_INLINE_KEY = re.compile(r'\{\s*key:\s*"([^"]+)"')


def _quoted(blob: str) -> list[str]:
    return re.findall(r"'([^']+)'", blob)


def svg_texts() -> dict[str, str]:
    return {p.name: p.read_text() for p in SVGS}


def game_of(text: str) -> str:
    m = RE_GAME.search(text)
    assert m, "every SVG must declare `var GAME = '<key>'`"
    return m.group(1)


def daily_of(text: str) -> list[str]:
    m = RE_DAILY.search(text)
    assert m, "every SVG must declare DAILY_GAMES"
    return _quoted(m.group(1))


# --------------------------------------------------------------------------
# Registry: three copies of the game list must not drift
# --------------------------------------------------------------------------


def test_ten_games_present():
    assert len(SVGS) == 10, f"expected 10 SVGs, found {len(SVGS)}"


def test_daily_registry_identical_in_every_svg():
    registries = {name: daily_of(text) for name, text in svg_texts().items()}
    unique = {tuple(v) for v in registries.values()}
    assert len(unique) == 1, f"DAILY_GAMES drifted between SVGs: {registries}"


def test_svg_game_keys_match_daily_registry():
    daily = set(daily_of(next(iter(svg_texts().values()))))
    assert len(daily) == 10
    for name, text in svg_texts().items():
        assert game_of(text) in daily, f"{name}: GAME not in DAILY_GAMES"


def test_daily_registry_is_one_of_each_game():
    daily = daily_of(next(iter(svg_texts().values())))
    assert len(daily) == len(set(daily)), "DAILY_GAMES has duplicates"
    assert set(daily) == {game_of(t) for t in svg_texts().values()}


def test_hub_inline_registry_matches_daily_order():
    """The hub computes today's game by index, so ORDER is load-bearing."""
    inline = RE_INLINE_KEY.findall(INDEX.read_text())
    daily = daily_of(next(iter(svg_texts().values())))
    assert inline == daily, (
        "index.astro inline GAMES order must equal DAILY_GAMES — the hub "
        f"picks by index. inline={inline} daily={daily}"
    )


def test_hub_frontmatter_keys_cover_the_same_set():
    keys = RE_FRONTMATTER_KEY.findall(INDEX.read_text())
    daily = daily_of(next(iter(svg_texts().values())))
    assert len(keys) == 10
    assert set(keys) == set(daily)


# --------------------------------------------------------------------------
# Daily-challenge gating: markDaily() must only fire for today's game
# --------------------------------------------------------------------------


@pytest.mark.parametrize("name,text", SVG_CASES, ids=SVG_IDS)
def test_mark_daily_is_guarded_by_today_game(name, text):
    calls = text.count("markDaily();")
    guards = text.count("todayGame() === GAME")
    assert calls >= 1, f"{name}: never marks the daily challenge"
    assert guards == calls, (
        f"{name}: {calls} markDaily() call(s) but {guards} "
        "`todayGame() === GAME` guard(s) — an ungated call credits the "
        "challenge on the wrong day and emits daily_completed with a wrong game"
    )


@pytest.mark.parametrize("name,text", SVG_CASES, ids=SVG_IDS)
def test_streak_survives_same_day_replay(name, text):
    assert "prev === t" in text, (
        f"{name}: markDaily() must treat a same-day replay as a no-op, "
        "otherwise re-playing resets the streak to 1"
    )


@pytest.mark.parametrize("name,text", SVG_CASES, ids=SVG_IDS)
def test_old_streak_reset_pattern_is_gone(name, text):
    assert "=== yst ? (parseInt" not in text, f"{name}: old streak bug returned"


@pytest.mark.parametrize("name,text", SVG_CASES, ids=SVG_IDS)
def test_every_game_emits_game_started(name, text):
    assert "ph('game_started'" in text, (
        f"{name}: WAP (the north-star metric) is defined on game_started; "
        "without it the game is invisible in that metric"
    )


# --------------------------------------------------------------------------
# Per-game fixes
# --------------------------------------------------------------------------


def test_2048_checks_the_whole_grid():
    """A `return` inside the scan truncates maxTile and hides the 2048 win."""
    text = (SVG_DIR / "2048.svg").read_text()
    assert "if (!grid[i][j]) return;" not in text, "early return is back"
    assert "if (!full) return;" in text, "game-over must require a full board"
    assert "maxTile >= 2048" in text, "the win condition must be reachable"


def test_2048_win_text_is_not_overwritten_by_game_over():
    text = (SVG_DIR / "2048.svg").read_text()
    check_end = text[text.index("function checkEnd") : text.index("function draw")]
    win_at = check_end.index("finish('win')")
    over_at = check_end.index("finish('over')")
    assert win_at < over_at
    assert "return;" in check_end[win_at:over_at], (
        "checkEnd() must return after a win so the game-over branch cannot "
        "overwrite the win overlay"
    )


def test_snake_food_placement_is_bounded():
    """Rejection sampling hangs forever on a full board."""
    text = (SVG_DIR / "snake.svg").read_text()
    assert "do {" not in text, "placeFood() retry loop is back"
    assert "if (!free.length)" in text, "placeFood() must handle a full board"


def test_ab_test_reports_both_start_events():
    text = (SVG_DIR / "ab-test.svg").read_text()
    assert "ph('game_started'" in text
    assert "ph('experiment_started'" in text, "keep the experiment-specific event"


# --------------------------------------------------------------------------
# Hub analytics: canonical game key, no fictional config
# --------------------------------------------------------------------------


def test_card_exposes_canonical_game_key():
    assert "data-game={gameKey}" in CARD.read_text()


def test_hub_event_uses_canonical_key():
    text = POSTHOG.read_text()
    assert 'getAttribute("data-game")' in text, (
        "game_selected must use the canonical key — href-derived keys "
        "mismatched 7 of 10 games (ab-test vs abtest, sql-query vs sql, …)"
    )


def test_no_fictional_env_override_claim():
    assert "PUBLIC_POSTHOG_KEY" not in POSTHOG.read_text(), (
        "the comment claimed a build-time env override that does not exist"
    )
