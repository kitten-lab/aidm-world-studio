"""Look presence buckets: Here / Things / Happened Here / Force / Also present."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from world_studio.commands import dispatch
from world_studio.db import connect
from world_studio.format import plain
from world_studio.seed import seed_world_void
from world_studio.world import World


def _world() -> World:
    tmp = tempfile.NamedTemporaryFile(suffix=".world.db", delete=False)
    tmp.close()
    conn = connect(Path(tmp.name))
    seed_world_void(conn)
    return World(conn)


class LookBucketTests(unittest.TestCase):
    def setUp(self) -> None:
        self.world = _world()

    def test_event_and_archetype_sections(self) -> None:
        self.assertTrue(
            dispatch(self.world, "create event The Knock | Three soft taps.").ok
        )
        self.assertTrue(dispatch(self.world, "spawn the-knock").ok)
        self.assertTrue(
            dispatch(
                self.world, "create archetype The Watcher | Eyes in the grain."
            ).ok
        )
        self.assertTrue(dispatch(self.world, "spawn the-watcher").ok)
        self.assertTrue(
            dispatch(self.world, "create feeling Distant Hum | Pressure.").ok
        )
        self.assertTrue(dispatch(self.world, "spawn distant-hum").ok)

        text = plain(dispatch(self.world, "look").message)
        self.assertIn("Happened Here", text)
        self.assertIn("The Knock", text)
        self.assertIn("Force", text)
        self.assertIn("The Watcher", text)
        self.assertIn("Also present", text)
        self.assertIn("Distant Hum", text)

        i_happened = text.index("Happened Here")
        i_force = text.index("Force")
        i_also = text.index("Also present")
        self.assertLess(i_happened, i_force)
        self.assertLess(i_force, i_also)
        # Not dumped into Also present as the only home
        also = text[i_also:]
        self.assertNotIn("The Knock", also)
        self.assertNotIn("The Watcher", also)
        # No per-section column headers / rules
        self.assertNotIn("NAME", text)
        self.assertNotIn("TYPE", text)
        self.assertNotIn("PRIME", text)

    def test_shared_column_widths_across_sections(self) -> None:
        """Longest name in any section pads shorter rows in other sections."""
        long = "A Book That Loves You Backwards"
        self.assertTrue(
            dispatch(self.world, f"create object {long} | spine.").ok
        )
        # seed void already has a long book; add a short force for comparison
        self.assertTrue(
            dispatch(self.world, "create archetype Hymn | Soft force.").ok
        )
        self.assertTrue(dispatch(self.world, "spawn hymn").ok)
        text = plain(dispatch(self.world, "look").message)
        # Find the Hymn data line (after Force section title)
        lines = text.splitlines()
        hymn_line = next(ln for ln in lines if "Hymn" in ln and "archetype" in ln)
        book_line = next(
            ln for ln in lines if "Loves You Backwards" in ln and "book" in ln
        )
        # KIND column starts at the same visual index on both rows
        self.assertEqual(hymn_line.index("archetype"), book_line.index("book"))

    def test_kind_and_subtype_are_separate_columns(self) -> None:
        """Subtypes never jam into kind as feeling/longing in look lists."""
        self.assertTrue(
            dispatch(
                self.world,
                "create feeling/longing Soft Ache | A quieter cousin.",
            ).ok
        )
        self.assertTrue(dispatch(self.world, "spawn soft-ache").ok)
        self.assertTrue(
            dispatch(self.world, "create place/app Mailroom | Soft list.").ok
        )
        self.assertTrue(dispatch(self.world, "spawn mailroom").ok)
        # put mailroom elsewhere so it doesn't steal focus — spawn is on floor
        text = plain(dispatch(self.world, "look").message)
        self.assertNotIn("feeling/longing", text)
        self.assertNotIn("place/app", text)
        # Also present / Things rows show kind then subtype as separate tokens
        ache = next(
            ln
            for ln in text.splitlines()
            if "Soft Ache" in ln or "Ache" in ln
        )
        self.assertRegex(ache, r"sense\s+longing")
        # bare sense without extra subtype still shows em-dash or default subtype
        self.assertTrue(
            dispatch(self.world, "create sense Bare Hum | x.").ok
        )
        self.assertTrue(dispatch(self.world, "spawn bare-hum").ok)
        text2 = plain(dispatch(self.world, "look").message)
        bare = next(ln for ln in text2.splitlines() if "Bare Hum" in ln)
        self.assertRegex(bare, r"sense\s+—")


if __name__ == "__main__":
    unittest.main()
