"""@desc show / set / append / clear / line breaks."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from world_studio.commands import dispatch
from world_studio.db import connect
from world_studio.format import plain
from world_studio.seed import seed_world_story
from world_studio.textutil import escape_desc, unescape_desc
from world_studio.world import World


def _world() -> World:
    tmp = tempfile.NamedTemporaryFile(suffix=".world.db", delete=False)
    tmp.close()
    conn = connect(Path(tmp.name))
    seed_world_story(conn)
    return World(conn)


class UnescapeTests(unittest.TestCase):
    def test_newline_and_backslash(self) -> None:
        self.assertEqual(unescape_desc(r"a\nb"), "a\nb")
        self.assertEqual(unescape_desc(r"a\\b"), "a\\b")
        self.assertEqual(unescape_desc(r"a\\nb"), "a\\nb")

    def test_escape_roundtrip_for_multiline_commit(self) -> None:
        raw = "# Title\n\n**Bold**\n---\ntail"
        encoded = escape_desc(raw)
        self.assertNotIn("\n", encoded)
        self.assertEqual(unescape_desc(encoded), raw)
        # Existing typed \\n literal survives escape→unescape
        typed = r"keep\nliteral"
        self.assertEqual(unescape_desc(escape_desc(typed)), typed)


class DescCommandTests(unittest.TestCase):
    def setUp(self) -> None:
        self.world = _world()

    def test_show_and_set(self) -> None:
        r = dispatch(self.world, "@desc")
        self.assertTrue(r.ok)
        self.assertIn("Description", plain(r.message))

        r = dispatch(self.world, r"@desc Line one.\nLine two.")
        self.assertTrue(r.ok)
        loc = self.world.player_location()
        assert loc is not None
        self.assertEqual(loc.description, "Line one.\nLine two.")

        look = plain(dispatch(self.world, "look").message)
        self.assertIn("Line one.", look)
        self.assertIn("Line two.", look)

    def test_append_and_clear(self) -> None:
        dispatch(self.world, "@desc First.")
        dispatch(self.world, "@desc + Second.")
        loc = self.world.player_location()
        assert loc is not None
        self.assertEqual(loc.description, "First.\nSecond.")

        dispatch(self.world, "@desc ++ Third para.")
        loc = self.world.player_location()
        assert loc is not None
        self.assertEqual(loc.description, "First.\nSecond.\n\nThird para.")

        dispatch(self.world, "@desc clear")
        loc = self.world.player_location()
        assert loc is not None
        # VEN default returns
        self.assertIn("half-inked", loc.description.lower())


if __name__ == "__main__":
    unittest.main()
