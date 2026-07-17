"""Named flags for create/spawn (free order): --type --name --desc --when …"""

from __future__ import annotations

import re
import shlex
from dataclasses import dataclass, field

from .story_when import normalize_story_when

# Long and short names → canonical key
_FLAG_ALIASES: dict[str, str] = {
    "type": "type",
    "kind": "type",
    "t": "type",
    "name": "name",
    "n": "name",
    "desc": "desc",
    "description": "desc",
    "d": "desc",
    "when": "when",
    "w": "when",
    "of": "of",
    "parent": "of",
    "as": "as",
    "a": "as",
    "title": "as",
    "ven": "ven",
    "prime": "ven",
    "from": "ven",
}


@dataclass
class NamedFlags:
    """Parsed free-order flags + leftover positionals."""

    flags: dict[str, str] = field(default_factory=dict)
    positionals: list[str] = field(default_factory=list)
    error: str | None = None

    def get(self, key: str, default: str = "") -> str:
        return (self.flags.get(key) or default).strip()


_FLAG_START = re.compile(r"(^|\s)--?[A-Za-z]")


def looks_like_flag_command(text: str) -> bool:
    """True if the user used --type / -n style markers."""
    return bool(_FLAG_START.search(text or ""))


def parse_named_flags(text: str) -> NamedFlags:
    """
    Parse ``--key value``, ``--key=value``, ``-k value`` (single-letter).

    Values may be quoted. Order of flags does not matter.
    """
    raw = (text or "").strip()
    if not raw:
        return NamedFlags()
    try:
        tokens = shlex.split(raw, posix=True)
    except ValueError as e:
        return NamedFlags(error=f"Could not parse flags: {e}")

    def take_value(start: int) -> tuple[str, int]:
        """Value runs until next flag token (so --as Hiking Stick works)."""
        if start >= len(tokens):
            return "", start
        parts: list[str] = []
        j = start
        while j < len(tokens) and not tokens[j].startswith("-"):
            parts.append(tokens[j])
            j += 1
        return " ".join(parts), j

    flags: dict[str, str] = {}
    positionals: list[str] = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok.startswith("--"):
            body = tok[2:]
            if not body:
                return NamedFlags(error="Empty flag --")
            if "=" in body:
                key, _, val = body.partition("=")
                canon = _FLAG_ALIASES.get(key.lower())
                if not canon:
                    return NamedFlags(error=f"Unknown flag --{key}")
                flags[canon] = val
                i += 1
                continue
            canon = _FLAG_ALIASES.get(body.lower())
            if not canon:
                return NamedFlags(error=f"Unknown flag --{body}")
            if i + 1 >= len(tokens) or tokens[i + 1].startswith("-"):
                return NamedFlags(error=f"Flag --{body} needs a value")
            val, i = take_value(i + 1)
            flags[canon] = val
            continue
        if tok.startswith("-") and len(tok) >= 2 and tok[1].isalpha():
            letters = tok[1:]
            if len(letters) == 1:
                canon = _FLAG_ALIASES.get(letters.lower())
                if not canon:
                    return NamedFlags(error=f"Unknown flag -{letters}")
                if i + 1 >= len(tokens) or tokens[i + 1].startswith("-"):
                    return NamedFlags(error=f"Flag -{letters} needs a value")
                val, i = take_value(i + 1)
                flags[canon] = val
                continue
            return NamedFlags(
                error=f"Use long flags or single -x (got {tok!r})"
            )
        positionals.append(tok)
        i += 1
    return NamedFlags(flags=flags, positionals=positionals)


def story_when_from_flag(raw: str | None) -> tuple[str, int | None]:
    """
    Normalize ``--when`` values: ``0``, ``@0``, ``unknown``, ``@unknown``.
    """
    s = (raw or "").strip()
    if not s:
        return "@unknown", None
    if s.isdigit():
        return f"@{int(s)}", int(s)
    if s.lower() in ("unknown", "@unknown"):
        return "@unknown", None
    if s.startswith("@"):
        return normalize_story_when(s)
    # freeform not a node
    return normalize_story_when(s)
