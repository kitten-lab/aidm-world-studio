"""Creator-tool shorthand: .c → create, .s → spawn."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from world_studio.commands import dispatch
from world_studio.db import connect
from world_studio.format import plain
from world_studio.seed import seed_world_story
from world_studio.world import World


def _world() -> World:
    tmp = tempfile.NamedTemporaryFile(suffix=".world.db", delete=False)
    tmp.close()
    conn = connect(Path(tmp.name))
    seed_world_story(conn)
    return World(conn)


class CreatorShorthandTests(unittest.TestCase):
    def setUp(self) -> None:
        self.world = _world()

    def test_dot_c_create(self) -> None:
        r = dispatch(self.world, ".c material Test Filament | Thin test.")
        self.assertTrue(r.ok, r.message)
        msg = plain(r.message)
        self.assertIn("Test Filament", msg)

    def test_dot_s_spawn(self) -> None:
        self.assertTrue(dispatch(self.world, "create object Shorthand Box").ok)
        r = dispatch(self.world, ".s shorthand-box as Pocket Box")
        self.assertTrue(r.ok, r.message)
        msg = plain(r.message)
        self.assertIn("Pocket Box", msg)

    def test_dot_c_usage_when_bare(self) -> None:
        r = dispatch(self.world, ".c")
        self.assertTrue(r.ok)
        self.assertIn("Usage: create", plain(r.message))

    def test_help_dot_c(self) -> None:
        r = dispatch(self.world, "help .c")
        self.assertTrue(r.ok)
        self.assertIn("create", plain(r.message).lower())


if __name__ == "__main__":
    unittest.main()
