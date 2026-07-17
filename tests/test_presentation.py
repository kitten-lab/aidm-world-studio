"""Presentation tests drive the real dispatch/seed path (no reimplementation)."""

from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path

from world_studio.commands import dispatch
from world_studio.db import connect
from world_studio.format import plain, safe
from world_studio.seed import seed_world_classic as seed_world
from world_studio.world import World


def _seeded_world() -> World:
    # temp file so tests never touch the user's seed.world.db
    tmp = tempfile.NamedTemporaryFile(suffix=".world.db", delete=False)
    tmp.close()
    path = Path(tmp.name)
    conn = connect(path)
    seed_world(conn)
    return World(conn)


class LookHierarchyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.world = _seeded_world()

    def test_look_has_title_prose_meta_exits_sections(self) -> None:
        result = dispatch(self.world, "look")
        self.assertTrue(result.ok)
        text = plain(result.message)

        # Distinct title line (cathedral) — plain readable display form
        self.assertIn("The Cathedral of Ordinary Light", text)
        self.assertNotIn("THE-CATHEDRAL-OF-ORDINARY-LIGHT", text)
        # Prose separate from lists (descriptions stay mixed case)
        self.assertIn("White stone", text)
        self.assertIn("cracked mirror", text)
        # Layered context under title: kind | realm | timeline
        self.assertIn("place", text.lower())
        self.assertIn("Material", text)
        self.assertIn("Prime", text)
        self.assertRegex(text, r"place\s+\|\s+Material\s+\|\s+Prime")
        # look only hints at paths — full list is `paths`
        self.assertRegex(text, r"\d+ path\(s\)")
        self.assertNotIn("through the mirror", text)
        self.assertNotIn("Spatial", text)
        # Things / feelings
        self.assertIn("Silver Thread", text)
        self.assertIn("Liturgical Hush", text)

        # Hierarchy: location line → description → path hint
        i_title = text.index("The Cathedral of Ordinary Light")
        i_realm = text.lower().index("material")  # realm on location line
        i_prose = text.index("White stone")
        i_paths = text.lower().index("path(s)")
        self.assertLess(i_title, i_realm)
        self.assertLess(i_realm, i_prose)
        self.assertLess(i_prose, i_paths)
        self.assertIn("Location:", text)

    def test_locate_self_aligned_fields(self) -> None:
        result = dispatch(self.world, "locate self")
        self.assertTrue(result.ok)
        text = plain(result.message)
        self.assertIn("Locate", text)
        self.assertIn("place", text)
        self.assertIn("The Cathedral of Ordinary Light", text)
        self.assertIn("Material", text)
        self.assertIn("Prime", text)
        # bare locate and temporary aliases match
        bare = plain(dispatch(self.world, "locate").message)
        self.assertEqual(text, bare)
        w = plain(dispatch(self.world, "status").message)
        self.assertEqual(text, w)

    def test_go_then_look_readable_multisection(self) -> None:
        result = dispatch(self.world, "go through the mirror")
        self.assertTrue(result.ok)
        text = plain(result.message)
        self.assertIn("Hall of Shelved Years", text)
        self.assertIn("Memory-Archive", text)
        self.assertRegex(text, r"\d+ path\(s\)")
        # full paths list not dumped on look after go
        self.assertNotIn("years later", text)
        # travel cue then room
        self.assertIn("through the mirror", text)

    def test_world_names_with_brackets_do_not_break_markup(self) -> None:
        # dig keeps formal name; markup-looking brackets must still be safe in Rich
        evil = "Evil [bold red]Hack[/bold red]"
        r = dispatch(self.world, f"dig {evil}")
        self.assertTrue(r.ok)
        rendered = plain(r.message)
        # formal name preserved (not forced to cute ALL-CAPS)
        self.assertIn("Evil", rendered)
        self.assertIn("Hack", rendered)
        self.assertNotIn("EVIL-BOLD-RED-HACK", rendered)
        # Dynamic world/user strings still escape via hint/ok when not normalized
        from world_studio.format import hint

        h = hint(f"→ {evil}")
        self.assertIn(r"\[bold red]", h)
        self.assertIn(safe(evil), h)
        self.assertEqual(plain(h).count("Hack"), 1)

    def test_hint_escapes_like_ok_err(self) -> None:
        from world_studio.format import hint, ok, err

        payload = "x [bold]inject[/bold] y"
        for fn in (hint, ok, err):
            out = fn(payload)
            self.assertIn(safe(payload), out)
            self.assertIn(r"\[bold]", out)

    def test_no_raw_half_tags_from_unescaped_exit_types_in_plain(self) -> None:
        result = dispatch(self.world, "exits")
        text = plain(result.message)
        # link types as group headers (title case), not swallowed by markup
        self.assertIn("Dimensional", text)
        self.assertIn("Spatial", text)
        # no orphan closing tags typical of broken markup
        self.assertIsNone(re.search(r"\[/bold(?!\s)", text))


if __name__ == "__main__":
    unittest.main()
