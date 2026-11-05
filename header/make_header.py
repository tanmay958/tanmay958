#!/usr/bin/env python3
"""Builds header-light.svg and header-dark.svg for the profile README.

Looks like a plain README. Then a little AI sparkle wakes up the letters of
the name and they go off to play, while its spark minions help (badly) and two
ninjas duel on the rooftops nearby.
Pure SMIL: no JavaScript, no CSS, no external fonts, so GitHub's image proxy
renders it as-is.

    python3 header/make_header.py          # write both SVGs
    python3 header/make_header.py --check  # fail if they are out of date
"""
import pathlib
import sys

from scene import build

HERE = pathlib.Path(__file__).resolve().parent

PALETTES = {
    "light": dict(
        bg="#ffffff", fg="#1f2328", muted="#59636e", line="#d1d9e0", rule="#d1d9e0",
        red="#cf222e", gold="#e3a008", smoke="#afb8c1", pupil="#1f2328",
        ai1="#f0a27f", ai2="#d97757", ai3="#b9532f", spark="#d97757", spark_edge="#a24b2b",
        cloud="#c6ced8", cloud_dark="#8c959f", rain="#3b82f6",
        ninja="#24292f", plate="#afb8c1", scarf_blue="#0969da", scarf_red="#cf222e",
        roof="#f2f4f7", roof_dark="#d0d7de", window="#f6d58e", steel="#6e7781",
        wood="#d4a373", wood_dark="#8a5a2b", leaf="#2da44e", leaf_dark="#1a7f37", can="#57606a",
        petal1="#f778ba", petal2="#ff9f43", petal3="#a371f7", petal4="#ff6b6b",
    ),
    "dark": dict(
        bg="#0d1117", fg="#e6edf3", muted="#9198a1", line="#3d444d", rule="#3d444d",
        red="#f85149", gold="#e3b341", smoke="#6e7681", pupil="#0d1117",
        ai1="#f4b393", ai2="#e0805e", ai3="#c4623e", spark="#e0805e", spark_edge="#f4b393",
        cloud="#57606a", cloud_dark="#30363d", rain="#58a6ff",
        ninja="#c9d1d9", plate="#6e7681", scarf_blue="#4493f8", scarf_red="#f85149",
        roof="#151b23", roof_dark="#30363d", window="#5a4718", steel="#9198a1",
        wood="#9c7a52", wood_dark="#5c4327", leaf="#3fb950", leaf_dark="#2ea043", can="#8b949e",
        petal1="#f778ba", petal2="#ffa657", petal3="#bc8cff", petal4="#ff7b72",
    ),
}


def main(argv):
    check = "--check" in argv
    stale = []
    for name, pal in PALETTES.items():
        svg = build(pal)
        path = HERE / f"header-{name}.svg"
        if check:
            if not path.exists() or path.read_text() != svg:
                stale.append(path.name)
            continue
        path.write_text(svg)
        print(f"{path.name}: {len(svg) / 1024:.0f} KB")
    if stale:
        print("out of date, run python3 header/make_header.py:", ", ".join(stale))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
