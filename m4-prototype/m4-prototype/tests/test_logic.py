"""Tests for the business logic, run with NO text interface.

Run from the project root:
    python -m unittest discover -s tests -v
"""

import random
import unittest

from dataman import logic
from dataman.store import InMemoryStore


class AcceptanceCriterionTest(unittest.TestCase):
    """AC (Trace Back to Product Work):
    Given the system has picked a secret number between 9 and 100,
    when the learner enters a guess,
    then the system displays two numbers and the secret number is between them.
    """

    def test_secret_always_between_shown_numbers(self):
        rng = random.Random(2026)
        for secret in range(10, 100):            # every possible secret
            for _ in range(20):                  # many random guess sequences
                store = InMemoryStore()
                sid = logic.start_game(store, secret=secret)["session_id"]
                while True:
                    result = logic.submit_guess(store, sid, rng.randint(10, 99))
                    if result["outcome"] == "correct":
                        break
                    self.assertEqual(result["outcome"], "hint")
                    self.assertLess(result["low"], secret)
                    self.assertLess(secret, result["high"])

    def test_first_display_already_contains_secret(self):
        store = InMemoryStore()
        game = logic.start_game(store, rng=random.Random(5))
        secret = store.get_play_state(game["session_id"])["secret"]
        self.assertTrue(logic.secret_is_between(game["low"], game["high"], secret))


class RangeRuleTest(unittest.TestCase):
    def test_range_narrows_from_both_sides(self):
        store = InMemoryStore()
        sid = logic.start_game(store, secret=37)["session_id"]
        self.assertEqual(logic.submit_guess(store, sid, 50)["high"], 50)
        r = logic.submit_guess(store, sid, 20)
        self.assertEqual((r["low"], r["high"]), (20, 50))

    def test_guess_outside_current_range_does_not_widen_it(self):
        store = InMemoryStore()
        sid = logic.start_game(store, secret=37)["session_id"]
        logic.submit_guess(store, sid, 30)   # low = 30
        r = logic.submit_guess(store, sid, 15)
        self.assertEqual((r["low"], r["high"]), (30, 100))
        self.assertEqual(r["guess_number"], 2)   # still counts as a guess

    def test_impossible_guess_is_rejected_and_not_counted(self):
        store = InMemoryStore()
        sid = logic.start_game(store, secret=37)["session_id"]
        for bad in (9, 100, 0, 500, -3):
            self.assertEqual(logic.submit_guess(store, sid, bad)["outcome"], "rejected")
        self.assertEqual(store.get_play_state(sid)["guess_count"], 0)
        self.assertEqual(store.list_attempts(sid), [])


class StateAndDataTest(unittest.TestCase):
    def test_correct_guess_reports_total_tries_and_saves_result(self):
        store = InMemoryStore()
        sid = logic.start_game(store, secret=37)["session_id"]
        logic.submit_guess(store, sid, 50)
        logic.submit_guess(store, sid, 25)
        r = logic.submit_guess(store, sid, 37)
        self.assertEqual(r, {"outcome": "correct", "guesses": 3, "secret": 37})
        self.assertEqual(store.get_result(sid)["status"], "solved")
        self.assertEqual(len(store.list_attempts(sid)), 3)

    def test_no_guesses_accepted_after_game_is_solved(self):
        store = InMemoryStore()
        sid = logic.start_game(store, secret=37)["session_id"]
        logic.submit_guess(store, sid, 37)
        self.assertEqual(logic.submit_guess(store, sid, 40)["outcome"], "game_over")

    def test_early_quit_keeps_saved_attempts(self):
        """The investigation's early-close scenario: quitting must not erase
        the guesses already made."""
        store = InMemoryStore()
        sid = logic.start_game(store, secret=37)["session_id"]
        logic.submit_guess(store, sid, 60)
        logic.submit_guess(store, sid, 20)
        logic.abandon_game(store, sid)
        review = logic.session_review(store, sid)
        self.assertEqual(review["result"]["status"], "abandoned")
        self.assertEqual([a["guess"] for a in review["attempts"]], [60, 20])

    def test_each_game_gets_a_new_session(self):
        store = InMemoryStore()
        a = logic.start_game(store, rng=random.Random(1))["session_id"]
        b = logic.start_game(store, rng=random.Random(2))["session_id"]
        self.assertNotEqual(a, b)

    def test_start_game_does_not_leak_secret_to_caller(self):
        game = logic.start_game(InMemoryStore(), secret=37)
        self.assertNotIn("secret", game)


class StoreIsReplaceableTest(unittest.TestCase):
    """Logic must work with ANY object that has the store methods."""

    def test_logic_runs_against_a_different_store(self):
        class CountingStore(InMemoryStore):
            def __init__(self):
                super().__init__()
                self.attempt_writes = 0

            def save_attempt(self, session_id, attempt):
                self.attempt_writes += 1
                super().save_attempt(session_id, attempt)

        store = CountingStore()
        sid = logic.start_game(store, secret=42)["session_id"]
        logic.submit_guess(store, sid, 50)
        logic.submit_guess(store, sid, 42)
        self.assertEqual(store.attempt_writes, 2)   # saved as each guess happened


if __name__ == "__main__":
    unittest.main()
