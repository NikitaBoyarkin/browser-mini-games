#!/usr/bin/env python3
"""Sync browser-mini-games build output -> Personal_Projects.github.io/public/games.

Canonical source: browser-mini-games/dist/ (Astro build output; run `npm run
build` first). Target: Personal_Projects.github.io/public/games/ (portfolio
site copy). The built hub is self-contained (inline CSS/JS), so it works from
any subpath.

Usage:
  python3 sync_games.py            # copy changed files
  python3 sync_games.py --check     # report drift, exit 1 if any
  python3 sync_games.py --dry-run   # show what would be copied
"""

import argparse
import hashlib
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "dist"  # Astro build output
DST = ROOT.parent / "Personal_Projects.github.io" / "public" / "games"

FILES = [
    "snake.svg",
    "ab-test.svg",
    "pong.svg",
    "2048.svg",
    "funnel-drop.svg",
    "cohort-catch.svg",
    "sql-query.svg",
    "metric-match.svg",
    "index.html",
]


def sha1(p: pathlib.Path) -> str:
    return hashlib.sha1(p.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="report drift, exit 1 if any")
    ap.add_argument("--dry-run", action="store_true", help="show what would be copied")
    args = ap.parse_args()

    if not SRC.is_dir():
        print(f"ERROR: source build missing: {SRC}")
        print("  Run `npm run build` first.")
        return 2
    if not DST.is_dir():
        print(f"ERROR: target dir missing: {DST}")
        return 2

    drift = []
    for f in FILES:
        src = SRC / f
        dst = DST / f
        if not src.is_file():
            print(f"WARN: source missing: {src}")
            continue
        if not dst.is_file() or sha1(src) != sha1(dst):
            drift.append(f)

    if not drift:
        print("OK: all files in sync")
        return 0

    if args.check:
        print(f"DRIFT ({len(drift)}):")
        for f in drift:
            print(f"  {f}")
        return 1

    for f in drift:
        src, dst = SRC / f, DST / f
        if args.dry_run:
            print(f"would copy: {f}")
        else:
            dst.write_bytes(src.read_bytes())
            print(f"copied: {f}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
