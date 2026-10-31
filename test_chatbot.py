import subprocess
import sys
import unittest
from unittest import mock

import functions


class FakeBot:
    """A stand-in bot so the chat loop can run without ChatterBot."""

    def __init__(self):
        self.asked = []

    def get_response(self, text):
        self.asked.append(text)
        return "fake answer"


def run_loop(inputs):
    bot = FakeBot()
    printed = []
    with mock.patch("builtins.input", side_effect=inputs), \
            mock.patch("builtins.print", side_effect=lambda *a, **k: printed.append(a)):
        functions.start_chatbot(bot)
    return bot, printed


class IsQuitTests(unittest.TestCase):
    def test_plain_bye_words(self):
        for text in ("bye", "bye jordan", "good bye", "goodbye"):
            self.assertTrue(functions.is_quit(text), text)

    def test_case_and_surrounding_space_do_not_matter(self):
        self.assertTrue(functions.is_quit(" Bye "))
        self.assertTrue(functions.is_quit("GOODBYE"))

    def test_non_quit_text(self):
        for text in ("hello", "bye!", "", "good"):
            self.assertFalse(functions.is_quit(text), text)


class StartChatbotTests(unittest.TestCase):
    def test_trailing_space_bye_ends_without_asking_bot(self):
        bot, printed = run_loop(["bye "])
        self.assertEqual(bot.asked, [])
        self.assertIn(("Jordan: Good bye and have a blessed day!",), printed)

    def test_empty_line_is_reprompted_not_answered(self):
        bot, _ = run_loop(["", "   ", "bye"])
        self.assertEqual(bot.asked, [])

    def test_question_goes_to_bot_and_answer_prints(self):
        bot, printed = run_loop(["Who is the owner of the house?", "bye"])
        self.assertEqual(bot.asked, ["Who is the owner of the house?"])
        self.assertIn(("Jordan:", "fake answer"), printed)

    def test_eof_ends_with_goodbye(self):
        bot, printed = run_loop([EOFError()])
        self.assertEqual(bot.asked, [])
        self.assertIn(("Jordan: Good bye and have a blessed day!",), printed)


class EntryPointTests(unittest.TestCase):
    def run_main(self, *args, text=""):
        return subprocess.run(
            [sys.executable, "main.py", *args],
            input=text, capture_output=True, text=True, timeout=30)

    def test_help_exits_0_without_chatterbot(self):
        result = self.run_main("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Usage: python main.py", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_unknown_argument_exits_2(self):
        result = self.run_main("--nope")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Usage: python main.py", result.stderr)

    def test_missing_chatterbot_is_a_hint_not_a_traceback(self):
        try:
            import chatterbot  # noqa: F401
        except ModuleNotFoundError:
            pass
        else:
            self.skipTest("ChatterBot is installed on this machine")
        result = self.run_main(text="bye\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn("ChatterBot is not installed", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
