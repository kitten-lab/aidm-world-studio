"""Nested container take/put via real dispatch."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from world_studio.commands import dispatch
from world_studio.db import connect
from world_studio.format import plain
from world_studio.seed import seed_world_classic as seed_world
from world_studio.world import World


def _seeded_world() -> World:
    tmp = tempfile.NamedTemporaryFile(suffix=".world.db", delete=False)
    tmp.close()
    conn = connect(Path(tmp.name))
    seed_world(conn)
    return World(conn)


class NestedContainerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.world = _seeded_world()

    def test_put_in_box_then_take_from_box_in_inventory(self) -> None:
        # Create a box on the floor, put silver in it, pick up the box, take silver out
        self.assertTrue(dispatch(self.world, "create object Ritual Box | A small glass box.").ok)
        self.assertTrue(dispatch(self.world, "spawn ritual-box").ok)
        put = dispatch(self.world, "put silver in box")
        self.assertTrue(put.ok, msg=put.message)
        self.assertIn("Put", plain(put.message))
        # silver no longer on floor — bare take should hint "from"
        take_floor = dispatch(self.world, "take silver")
        floor_msg = plain(take_floor.message).lower()
        self.assertNotIn("taken · silver", floor_msg)
        self.assertTrue(
            "from" in floor_msg or "don't see" in floor_msg or "inside" in floor_msg,
            msg=take_floor.message,
        )

        take_box = dispatch(self.world, "take box")
        self.assertIn("Taken", plain(take_box.message), msg=take_box.message)
        inv = plain(dispatch(self.world, "inv").message)
        self.assertIn("Ritual Box", inv)
        self.assertIn("Silver", inv)  # nested hint in inv

        got = dispatch(self.world, "take silver from box")
        self.assertIn("Taken", plain(got.message), msg=got.message)
        self.assertIn("from", plain(got.message).lower())

        inv2 = plain(dispatch(self.world, "inv").message)
        self.assertIn("Silver Thread", inv2)
        # box still carried
        self.assertIn("Ritual Box", inv2)

    def test_get_alias_and_examine_contents(self) -> None:
        dispatch(self.world, "create object Pouch | Soft.")
        dispatch(self.world, "spawn pouch")
        dispatch(self.world, "put silver in pouch")
        ex = dispatch(self.world, "examine pouch")
        self.assertTrue(ex.ok)
        self.assertIn("Silver Thread", plain(ex.message))
        dispatch(self.world, "take pouch")
        g = dispatch(self.world, "get silver from pouch")
        self.assertTrue(g.ok, msg=g.message)


if __name__ == "__main__":
    unittest.main()
