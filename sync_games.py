#!/usr/bin/env python3
"""Sync browser-mini-games -> Personal_Projects.github.io/public/games.

Canonical source: browser-mini-games/ (deployed via its own GitHub Pages workflow).
Target: Personal_Projects.github.io/public/games/ (portfolio site copy).

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
DST = ROOT.parent / "Personal_Projects.github.io" / "public" / "games"

FILES = [
    "snake.svg",
    "ab-test.svg",
    "pong.svg",
    "2048.svg",
    "funnel-drop.svg",
    "index.html",
]


def sha1(p: pathlib.Path) -> str:
    return hashlib.sha1(p.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="report drift, exit 1 if any")
    ap.add_argument("--dry-run", action="store_true", help="show what would be copied")
    args = ap.parse_args()

    if not DST.is_dir():
        print(f"ERROR: target dir missing: {DST}")
        return 2

    drift = []
    for f in FILES:
        src = ROOT / f
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
        src, dst = ROOT / f, DST / f
        if args.dry_run:
            print(f"would copy: {f}")
        else:
            dst.write_bytes(src.read_bytes())
            print(f"copied: {f}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
