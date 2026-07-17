"""Installed apps: portal bind + run into real places (not room exits)."""

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


class RunPortalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.world = _world()
        # Device + app + world
        self.assertTrue(
            dispatch(self.world, "create object Terminal IO | Humming beige.").ok
        )
        self.assertTrue(dispatch(self.world, "spawn terminal-io").ok)
        self.assertTrue(
            dispatch(self.world, "create object/app Mail | Never sleeps.").ok
        )
        self.assertTrue(dispatch(self.world, "spawn mail").ok)
        dig = dispatch(self.world, "dig place/app Mailroom")
        self.assertTrue(dig.ok, dig.message)
        self.assertIn("place/app", plain(dig.message))

    def test_not_installed_on_floor(self) -> None:
        self.assertTrue(dispatch(self.world, "portal mail -> Mailroom").ok)
        r = dispatch(self.world, "run mail")
        self.assertFalse(r.ok)
        self.assertIn("not installed", plain(r.message).lower())

    def test_run_from_device(self) -> None:
        self.assertTrue(dispatch(self.world, "portal mail -> Mailroom").ok)
        self.assertTrue(dispatch(self.world, "put mail in terminal").ok)
        # Not on exits
        exits = plain(dispatch(self.world, "exits").message).lower()
        self.assertNotIn("mail", exits)
        self.assertNotIn("mailroom", exits)

        r = dispatch(self.world, "run mail from terminal")
        self.assertTrue(r.ok, r.message)
        loc = self.world.player_location()
        assert loc is not None
        self.assertIn("Mailroom", loc.name)
        self.assertEqual(loc.ven_subtype, "app")
        look = plain(dispatch(self.world, "look").message)
        self.assertIn("Mailroom", look)
        # Location trailer: place: app (subtype when present)
        self.assertRegex(look, r"place\s*:\s*app")

    def test_soft_run_unique_installed(self) -> None:
        self.assertTrue(dispatch(self.world, "portal mail -> Mailroom").ok)
        self.assertTrue(dispatch(self.world, "put mail in terminal").ok)
        r = dispatch(self.world, "run mail")
        self.assertTrue(r.ok, r.message)
        loc = self.world.player_location()
        assert loc is not None
        self.assertIn("Mailroom", loc.name)

    def test_no_portal_bound(self) -> None:
        self.assertTrue(dispatch(self.world, "put mail in terminal").ok)
        r = dispatch(self.world, "run mail from terminal")
        self.assertFalse(r.ok)
        self.assertIn("portal", plain(r.message).lower())

    def test_examine_device_marks_runnable(self) -> None:
        self.assertTrue(dispatch(self.world, "portal mail -> Mailroom").ok)
        self.assertTrue(dispatch(self.world, "put mail in terminal").ok)
        ex = plain(dispatch(self.world, "examine terminal").message)
        self.assertIn("Mail", ex)
        self.assertIn("run", ex.lower())

    def test_storybook_place_and_game_object(self) -> None:
        self.assertTrue(
            dispatch(
                self.world,
                "create object/game Kat Moire: Kitten Detective | Soft paws.",
            ).ok
        )
        self.assertTrue(dispatch(self.world, "spawn kat-moire").ok)
        dig = dispatch(
            self.world, "dig place/storybook City of Soft Alibis"
        )
        self.assertTrue(dig.ok, dig.message)
        self.assertTrue(
            dispatch(
                self.world, "portal kat-moire -> City of Soft Alibis"
            ).ok
        )
        self.assertTrue(dispatch(self.world, "put kat-moire in terminal").ok)
        r = dispatch(self.world, "run kat from terminal")
        self.assertTrue(r.ok, r.message)
        loc = self.world.player_location()
        assert loc is not None
        self.assertIn("Soft Alibis", loc.name)
        self.assertEqual(loc.ven_subtype, "storybook")

    def test_portal_clear_and_undo(self) -> None:
        self.assertTrue(dispatch(self.world, "portal mail -> Mailroom").ok)
        mail = self.world.resolve_here_named("mail")
        assert mail is not None
        self.assertIsNotNone(self.world.get_portal_to(mail.id))
        self.assertTrue(dispatch(self.world, "portal clear mail").ok)
        self.assertIsNone(self.world.get_portal_to(mail.id))
        self.assertTrue(dispatch(self.world, "undo").ok)
        self.assertIsNotNone(self.world.get_portal_to(mail.id))

    def test_portal_survives_take_and_reinstall(self) -> None:
        """Binding is on the app; take/put never require re-portal."""
        self.assertTrue(dispatch(self.world, "portal mail -> Mailroom").ok)
        self.assertTrue(dispatch(self.world, "put mail in terminal").ok)
        mail = None
        term = self.world.resolve_here_named("terminal")
        assert term is not None
        for c in self.world.contents(term.id):
            if "mail" in c.name.lower():
                mail = c
                break
        assert mail is not None
        dest_id = self.world.get_portal_to(mail.id)
        self.assertIsNotNone(dest_id)

        take = dispatch(self.world, "take mail from terminal")
        self.assertTrue(take.ok, take.message)
        self.assertIn("portal still", plain(take.message).lower())
        mail2 = self.world.resolve_here_named("mail")
        assert mail2 is not None
        self.assertEqual(self.world.get_portal_to(mail2.id), dest_id)
        # Not installed → run fails, but link is intact
        r_loose = dispatch(self.world, "run mail")
        self.assertFalse(r_loose.ok)
        self.assertIn("not installed", plain(r_loose.message).lower())

        put = dispatch(self.world, "install mail in terminal")
        self.assertTrue(put.ok, put.message)
        self.assertIn("binding kept", plain(put.message).lower())
        r = dispatch(self.world, "run mail")
        self.assertTrue(r.ok, r.message)
        loc = self.world.player_location()
        assert loc is not None
        self.assertIn("Mailroom", loc.name)

    def test_logout_returns_to_entry_not_link(self) -> None:
        origin = self.world.player_location()
        assert origin is not None
        origin_id = origin.id
        self.assertTrue(dispatch(self.world, "portal mail -> Mailroom").ok)
        self.assertTrue(dispatch(self.world, "put mail in terminal").ok)
        self.assertTrue(dispatch(self.world, "run mail from terminal").ok)
        # Dig deeper inside the app world and walk there — logout still returns
        self.assertTrue(dispatch(self.world, "dig Inner Inbox").ok)
        self.assertTrue(
            dispatch(self.world, "link deeper -> Inner Inbox").ok
        )
        self.assertTrue(dispatch(self.world, "go deeper").ok)
        inner = self.world.player_location()
        assert inner is not None
        self.assertIn("Inner", inner.name)

        r = dispatch(self.world, "logout")
        self.assertTrue(r.ok, r.message)
        self.assertIn("logout", plain(r.message).lower())
        back = self.world.player_location()
        assert back is not None
        self.assertEqual(back.id, origin_id)
        self.assertIsNone(self.world.peek_portal_session())

    def test_logout_when_not_in_session(self) -> None:
        r = dispatch(self.world, "logout")
        self.assertTrue(r.ok)
        self.assertIn("nothing", plain(r.message).lower())


if __name__ == "__main__":
    unittest.main()
