"""Smoke tests for the browser-mini-games arcade.

Loads each self-contained SVG game from public/ via a local HTTP server on
lvh.me (resolves to 127.0.0.1 but is NOT in the IS_LOCAL regex), exercising the
same non-localhost PostHog path that runs on GitHub Pages. Asserts the game
element renders, no page errors, PostHog initializes, and the game responds to
input.

Requires: pytest, playwright
  pip install pytest playwright && playwright install chromium
Run:      python3 -m pytest tests/ -v
"""

import http.server
import pathlib
import socketserver
import threading

import pytest
from playwright.sync_api import sync_playwright

GAMES_DIR = pathlib.Path(__file__).resolve().parent.parent / "public"

GAMES = [
    ("snake", "snake.svg", "score"),
    ("2048", "2048.svg", "score"),
    ("pong", "pong.svg", "score"),
    ("abtest", "ab-test.svg", "status"),
    ("funnel", "funnel-drop.svg", "status"),
    ("cohort", "cohort-catch.svg", "status"),
    ("sql", "sql-query.svg", "status"),
    ("metric", "metric-match.svg", "status"),
    ("retention", "retention-day.svg", "status"),
    ("bottleneck", "funnel-bottleneck.svg", "status"),
]


@pytest.fixture(scope="module")
def server_url():
    handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(
        *a, directory=str(GAMES_DIR), **kw
    )
    with socketserver.TCPServer(("127.0.0.1", 0), handler) as httpd:
        port = httpd.server_address[1]
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        yield f"http://lvh.me:{port}"
        httpd.shutdown()


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch()
        yield b
        b.close()


@pytest.mark.parametrize("name,file,el", GAMES)
def test_game_loads_and_initializes(server_url, browser, name, file, el):
    page = browser.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(f"{server_url}/{file}", wait_until="load")
    page.wait_for_timeout(1200)
    assert not errors, f"{name}: page errors: {errors}"
    assert page.evaluate(f"!!document.getElementById('{el}')"), f"{name}: game element missing"
    assert page.evaluate("typeof window.posthog") == "object", f"{name}: PostHog not initialized"
    page.close()


def test_snake_responds_to_key(server_url, browser):
    page = browser.new_page()
    page.goto(f"{server_url}/snake.svg", wait_until="load")
    page.wait_for_timeout(500)
    page.keyboard.press("ArrowRight")
    page.wait_for_timeout(300)
    overlay = page.evaluate("document.getElementById('overlay').textContent")
    assert overlay == "", f"snake: overlay not cleared after key: {overlay!r}"
    page.close()


def test_2048_moves_tiles(server_url, browser):
    page = browser.new_page()
    page.goto(f"{server_url}/2048.svg", wait_until="load")
    page.wait_for_timeout(500)

    def grid():
        return page.evaluate(
            "Array.from(document.querySelectorAll('#tiles text')).map(t => "
            "t.getAttribute('x') + ',' + t.getAttribute('y') + ':' + t.textContent"
            ").sort().join('|')"
        )

    before = grid()
    for key in ("ArrowUp", "ArrowLeft", "ArrowDown", "ArrowRight"):
        page.keyboard.press(key)
        page.wait_for_timeout(120)
    after = grid()
    assert before != after, "2048: grid unchanged after 4 moves"
    page.close()


def test_pong_serves_on_key(server_url, browser):
    page = browser.new_page()
    page.goto(f"{server_url}/pong.svg", wait_until="load")
    page.wait_for_timeout(500)
    cx_before = page.evaluate("document.getElementById('ball').getAttribute('cx')")
    page.keyboard.press("ArrowUp")
    page.wait_for_timeout(400)
    cx_after = page.evaluate("document.getElementById('ball').getAttribute('cx')")
    assert cx_before == "170", f"pong: ball moved before serve (cx={cx_before})"
    assert cx_after != "170", "pong: ball did not move after serve"
    page.close()


def test_abtest_collects_on_click(server_url, browser):
    page = browser.new_page()
    page.goto(f"{server_url}/ab-test.svg", wait_until="load")
    page.wait_for_timeout(500)
    page.mouse.click(200, 340)
    page.wait_for_timeout(200)
    status = page.evaluate("document.getElementById('status').textContent")
    assert "n = 150 / arm" in status, f"abtest: click did not collect: {status!r}"
    page.close()


def test_funnel_spawns_dots(server_url, browser):
    page = browser.new_page()
    page.goto(f"{server_url}/funnel-drop.svg", wait_until="load")
    page.wait_for_timeout(1500)
    dots = page.evaluate("document.querySelectorAll('#dots circle').length")
    assert dots >= 3, f"funnel: expected >=3 dots, got {dots}"
    page.close()


def test_cohort_spawns_dots(server_url, browser):
    page = browser.new_page()
    page.goto(f"{server_url}/cohort-catch.svg", wait_until="load")
    page.wait_for_timeout(1500)
    dots = page.evaluate("document.querySelectorAll('#dots circle').length")
    assert dots >= 3, f"cohort: expected >=3 dots, got {dots}"
    page.close()


def test_sql_answers_on_click(server_url, browser):
    page = browser.new_page()
    page.goto(f"{server_url}/sql-query.svg", wait_until="load")
    page.wait_for_timeout(500)
    box = page.locator("#opts rect").first.bounding_box()
    assert box, "sql: no option rect found"
    page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    page.wait_for_timeout(200)
    query = page.evaluate("document.getElementById('query').textContent")
    assert "___" not in query, f"sql: query not filled after click: {query!r}"
    page.close()


def test_metric_flips_cards(server_url, browser):
    page = browser.new_page()
    page.goto(f"{server_url}/metric-match.svg", wait_until="load")
    page.wait_for_timeout(500)
    cards = page.locator("#board g")
    assert cards.count() >= 2, "metric: expected >=2 cards"
    for i in (0, 1):
        box = cards.nth(i).bounding_box()
        page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    page.wait_for_timeout(200)
    status = page.evaluate("document.getElementById('status').textContent")
    assert "moves 1" in status, f"metric: two flips did not register a move: {status!r}"
    page.close()


def test_retention_answers_on_click(server_url, browser):
    page = browser.new_page()
    page.goto(f"{server_url}/retention-day.svg", wait_until="load")
    page.wait_for_timeout(500)
    box = page.locator("#opts rect").first.bounding_box()
    assert box, "retention: no option rect found"
    page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    page.wait_for_timeout(200)
    status = page.evaluate("document.getElementById('status').textContent")
    assert "Round 2" in status or "score" in status, f"retention: click did not advance: {status!r}"
    page.close()


def test_bottleneck_answers_on_click(server_url, browser):
    page = browser.new_page()
    page.goto(f"{server_url}/funnel-bottleneck.svg", wait_until="load")
    page.wait_for_timeout(500)
    box = page.locator("#opts rect").first.bounding_box()
    assert box, "bottleneck: no option rect found"
    page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    page.wait_for_timeout(200)
    status = page.evaluate("document.getElementById('status').textContent")
    assert "Round 2" in status or "score" in status, f"bottleneck: click did not advance: {status!r}"
    page.close()
