"""Command history (↑ previous inputs) + studio multiline line recall."""

from __future__ import annotations

import inspect
import unittest

from world_studio import cli
from world_studio.cli import (
    MultilineDescDraft,
    _collect_multiline_desc,
)
from world_studio.history import CommandHistory


class CommandHistoryTests(unittest.TestCase):
    def test_up_down_browse(self) -> None:
        h = CommandHistory()
        h.push("look")
        h.push("go south")
        h.push("inv")
        self.assertEqual(h.up(""), "inv")
        self.assertEqual(h.up("inv"), "go south")
        self.assertEqual(h.up("go south"), "look")
        # stay at oldest
        self.assertEqual(h.up("look"), "look")
        self.assertEqual(h.down("look"), "go south")
        self.assertEqual(h.down("go south"), "inv")
        # past newest restores empty draft
        self.assertEqual(h.down("inv"), "")

    def test_draft_preserved(self) -> None:
        h = CommandHistory()
        h.push("look")
        self.assertEqual(h.up("half-typed"), "look")
        self.assertEqual(h.down("look"), "half-typed")

    def test_no_duplicate_consecutive(self) -> None:
        h = CommandHistory()
        h.push("look")
        h.push("look")
        self.assertEqual(len(h), 1)

    def test_empty_up(self) -> None:
        h = CommandHistory()
        self.assertIsNone(h.up(""))


class StudioMultilineHistoryTests(unittest.TestCase):
    """Shipped collect path stores accepted content lines for up/down."""

    def test_desc_studio_collect_pushes_content_lines(self) -> None:
        h = CommandHistory()
        h.push("@desc <<studio")  # opener (as REPL/TUI do)
        inputs = iter(
            [
                "# Terminal-Prolog",
                "**Boot** sequence.",
                "Line three.",
                ".",
            ]
        )
        body = _collect_multiline_desc(
            lambda: next(inputs),
            history=h,
        )
        self.assertEqual(
            body, "# Terminal-Prolog\n**Boot** sequence.\nLine three."
        )
        items = h.items()
        self.assertIn("@desc <<studio", items)
        self.assertIn("# Terminal-Prolog", items)
        self.assertIn("**Boot** sequence.", items)
        self.assertIn("Line three.", items)
        # Not opener/stub only — at least 3 content lines recallable
        content = [x for x in items if x != "@desc <<studio"]
        self.assertGreaterEqual(len(content), 3)
        # End marker not required as content history
        self.assertNotIn(".", items)

        # up/down newest-first: last content then earlier
        self.assertEqual(h.up(""), "Line three.")
        self.assertEqual(h.up("Line three."), "**Boot** sequence.")
        self.assertEqual(h.up("**Boot** sequence."), "# Terminal-Prolog")
        self.assertEqual(h.down("# Terminal-Prolog"), "**Boot** sequence.")
        self.assertEqual(h.down("**Boot** sequence."), "Line three.")
        self.assertEqual(h.down("Line three."), "")

    def test_book_studio_collect_pushes_content_lines(self) -> None:
        h = CommandHistory()
        opener = "book page add field-notes Prolog <<studio"
        h.push(opener)
        inputs = iter(["# Call", "Second line", "Third line", "."])
        body = _collect_multiline_desc(lambda: next(inputs), history=h)
        self.assertEqual(body, "# Call\nSecond line\nThird line")
        items = h.items()
        self.assertEqual(items[0], opener)
        self.assertEqual(items[1:], ["# Call", "Second line", "Third line"])
        self.assertEqual(h.up(""), "Third line")
        self.assertEqual(h.up("Third line"), "Second line")
        self.assertEqual(h.up("Second line"), "# Call")

    def test_mid_collection_up_after_each_accept(self) -> None:
        """After accepting A,B,C, up from empty draft yields C then B then A."""
        h = CommandHistory()
        for text in ("A", "B", "C"):
            h.push_content_line(text)
            # still at "new draft" after each push
        self.assertEqual(h.up(""), "C")
        self.assertEqual(h.up("C"), "B")
        self.assertEqual(h.up("B"), "A")
        self.assertEqual(h.down("A"), "B")
        self.assertEqual(h.down("B"), "C")
        self.assertEqual(h.down("C"), "")

    def test_undo_and_end_not_pushed_by_collect(self) -> None:
        h = CommandHistory()
        inputs = iter(["keep me", "undo", "replacement", "."])
        body = _collect_multiline_desc(lambda: next(inputs), history=h)
        self.assertEqual(body, "replacement")
        # "keep me" was accepted then undone from draft, but was history-pushed
        # (intentional: typed line is recallable). undo token itself is not content.
        self.assertIn("keep me", h.items())
        self.assertIn("replacement", h.items())
        self.assertNotIn("undo", h.items())
        self.assertNotIn(".", h.items())

    def test_cli_wires_history_on_accept_paths(self) -> None:
        """Opener lines for << editor are history-pushed; buffer replaces line collect."""
        src = inspect.getsource(cli)
        self.assertIn("parse_multiline_opener", src)
        self.assertIn("run_text_editor", src)
        self.assertIn("make_studio_buffer_screen", src)
        # Opener still stored for ↑ recall
        self.assertIn("cmd.cmd_history.push(line)", src)
        self.assertIn("history.push(line)", src)
        # No longer store summary-only stub instead of content lines
        self.assertNotIn('hist = "@desc <<studio"', src)
        self.assertNotIn("cmd.cmd_history.push(hist)", src)


if __name__ == "__main__":
    unittest.main()
