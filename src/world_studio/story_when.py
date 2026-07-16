"""Story-when along timeline nodes: @N / @unknown (not craft created_at)."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .world import World

# Trailing: when @3  ·  when @unknown
_STORY_WHEN_SUFFIX_RE = re.compile(
    r"\s+when\s+@(?P<body>\d+|unknown)\s*$",
    re.IGNORECASE,
)

# Bare mythic lore stamp that is only @N / @unknown
_STORY_WHEN_ONLY_RE = re.compile(
    r"^@(?P<body>\d+|unknown)$",
    re.IGNORECASE,
)


def normalize_story_when(raw: str | None) -> tuple[str, int | None]:
    """
    Return (story_when token, node_index|None).

    Tokens are always ``@N`` or ``@unknown``.
    """
    s = (raw or "").strip()
    if not s:
        return "@unknown", None
    m = _STORY_WHEN_ONLY_RE.match(s)
    if not m:
        # Freeform mythic stamp is not a node — still unknown structurally
        return "@unknown", None
    body = m.group("body").lower()
    if body == "unknown":
        return "@unknown", None
    return f"@{int(body)}", int(body)


def peel_story_when_suffix(text: str) -> tuple[str, str, int | None]:
    """
    Strip trailing ``when @N`` / ``when @unknown`` from a command tail.

    Returns (remaining_text, story_when, node_index).
    """
    s = text or ""
    m = _STORY_WHEN_SUFFIX_RE.search(s)
    if not m:
        return s.strip(), "@unknown", None
    remaining = s[: m.start()].rstrip()
    body = m.group("body").lower()
    if body == "unknown":
        return remaining, "@unknown", None
    n = int(body)
    return remaining, f"@{n}", n


def story_when_from_lore_label(when_label: str | None) -> tuple[str, int | None]:
    """If lore when is exactly @N / @unknown, use it; else @unknown."""
    return normalize_story_when(when_label)


def format_history_line(
    *,
    verb: str,
    story_when: str,
    crafted_at: str,
    realm_name: str | None,
    timeline_name: str | None,
    note: str = "",
) -> str:
    """Plain one-line summary for history lists."""
    r = realm_name or "—"
    t = timeline_name or "—"
    base = f"{crafted_at}  ·  {verb}  ·  story {story_when}  ·  {r} / {t}"
    if note:
        return f"{base}  ·  {note}"
    return base


def resolve_strand_for_record(
    world: World,
    *,
    realm_instance_id: str | None = None,
    timeline_instance_id: str | None = None,
) -> tuple[str | None, str | None]:
    """Prefer explicit ids; else player's current place layers."""
    if realm_instance_id or timeline_instance_id:
        return realm_instance_id, timeline_instance_id
    loc = world.player_location()
    if loc is None:
        return None, None
    return loc.realm_instance_id, loc.timeline_instance_id
