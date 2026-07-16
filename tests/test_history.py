"""Story-when history: timeline nodes + life-of-item entries."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from world_studio.commands import dispatch
from world_studio.db import connect
from world_studio.format import plain
from world_studio.story_when import normalize_story_when, peel_story_when_suffix
from world_studio.seed import seed_world_bootstrap
from world_studio.world import World


class StoryWhenParseTests(unittest.TestCase):
    def test_peel_suffix(self) -> None:
        rest, sw, n = peel_story_when_suffix("quill as Pocket when @3")
        self.assertEqual(rest, "quill as Pocket")
        self.assertEqual(sw, "@3")
        self.assertEqual(n, 3)
        rest, sw, n = peel_story_when_suffix("thing X | soft. when @unknown")
        self.assertTrue(rest.endswith("soft."))
        self.assertEqual(sw, "@unknown")
        self.assertIsNone(n)

    def test_normalize(self) -> None:
        self.assertEqual(normalize_story_when("@0"), ("@0", 0))
        self.assertEqual(normalize_story_when("@unknown"), ("@unknown", None))
        self.assertEqual(normalize_story_when("Cow Jump"), ("@unknown", None))


class HistoryCommandTests(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.NamedTemporaryFile(suffix=".world.db", delete=False)
        tmp.close()
        self.conn = connect(Path(tmp.name))
        seed_world_bootstrap(self.conn)
        self.world = World(self.conn)

    def test_create_and_spawn_record_story_when(self) -> None:
        r = dispatch(
            self.world,
            "create thing Story Quill | Soft graphite. when @0",
        )
        self.assertTrue(r.ok, msg=r.message)
        self.assertIn("@0", plain(r.message))
        ven = self.world.find_ven("Story Quill")
        assert ven is not None
        rows = self.world.history_for("ven", ven.id)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["story_when"], "@0")
        self.assertEqual(rows[0]["verb"], "create")
        self.assertEqual(rows[0]["node_index"], 0)

        r2 = dispatch(
            self.world, "spawn story-quill as Pocket Quill when @2"
        )
        self.assertTrue(r2.ok, msg=r2.message)
        self.assertIn("@2", plain(r2.message))
        insts = self.world.list_instances_of_ven(ven.id)
        self.assertEqual(len(insts), 1)
        h = self.world.history_for("instance", insts[0].id)
        self.assertEqual(len(h), 1)
        self.assertEqual(h[0]["story_when"], "@2")
        self.assertEqual(h[0]["node_index"], 2)

        nodes = plain(dispatch(self.world, "history nodes").message)
        self.assertIn("@0", nodes)
        self.assertIn("@2", nodes)

        listed = plain(dispatch(self.world, "history on pocket").message)
        self.assertIn("@2", listed)
        self.assertIn("spawn", listed.lower())

        ven_hist = plain(dispatch(self.world, "history ven Story Quill").message)
        self.assertIn("@0", ven_hist)
        self.assertIn("create", ven_hist.lower())

    def test_omitted_when_is_unknown(self) -> None:
        r = dispatch(self.world, "create thing Bare Stick | wood.")
        self.assertTrue(r.ok, msg=r.message)
        ven = self.world.find_ven("Bare Stick")
        assert ven is not None
        rows = self.world.history_for("ven", ven.id)
        self.assertEqual(rows[0]["story_when"], "@unknown")
        self.assertIsNone(rows[0]["node_index"])

    def test_lore_when_at_node(self) -> None:
        r = dispatch(
            self.world, "lore add Founding | Raised for travelers. when @1"
        )
        self.assertTrue(r.ok, msg=r.message)
        self.assertIn("@1", plain(r.message))
        loc = self.world.player_location()
        assert loc is not None
        # lore history is on lore id â€” find via nodes + any history with @1
        # place itself may have no instance history; check lore entry recorded
        # by scanning connection
        rows = self.conn.execute(
            "SELECT * FROM history_entries WHERE story_when = '@1' AND verb = 'lore'"
        ).fetchall()
        self.assertGreaterEqual(len(rows), 1)


if __name__ == "__main__":
    unittest.main()
