"""Canonical content measure for AIDM World Studio.

Authors should compose look-critical text (books, studio layout, rules) as if
the content column is this many characters wide. Side rails and OS chrome are
secondary; they must not redefine the artboard.
"""

from __future__ import annotations

# Design measure for prose, book pages, turn HRs, and <<studio wrap guides.
CONTENT_MEASURE = 72


def measure_ruler(width: int = CONTENT_MEASURE) -> str:
    """
    Classic column ruler for the studio editor (ASCII, no Rich markup).

    Example (first 20): ``....+....1....+....2``
    """
    if width < 1:
        return ""
    chars: list[str] = []
    for i in range(1, width + 1):
        if i % 10 == 0:
            chars.append(str((i // 10) % 10))
        elif i % 5 == 0:
            chars.append("+")
        else:
            chars.append(".")
    return "".join(chars)


def turn_rule_ascii(width: int = CONTENT_MEASURE) -> str:
    """Plain ASCII horizontal rule of *width* dashes."""
    return "-" * max(1, width)
