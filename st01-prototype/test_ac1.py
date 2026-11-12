"""AC-1 for ST-01.

Given the system has picked a secret number between 9 and 100,
when the learner enters a guess,
then the system displays two numbers and the secret number is between them.

Run:  python -m unittest test_ac1 -v
"""

import random
import unittest

import logic
import store


class TestAC1SecretAlwaysBetween(unittest.TestCase):
    def test_secret_is_strictly_between_the_two_numbers_after_every_guess(self):
        rng = random.Random(2026)
        secrets_seen = set()

        for seed in range(3000):
            # Given: the system has picked a secret (through the real logic layer).
            view = logic.new_game(seed)
            secret = store.load_game()["secret"]
            secrets_seen.add(secret)
            self.assertLess(view["low"], secret)
            self.assertLess(secret, view["high"])

            # When: the learner enters guesses, including silly ones outside the range.
            for _ in range(500):
                if rng.random() < 0.2:
                    guess = rng.randint(0, 110)  # careless guess, may be outside the range
                else:
                    guess = rng.randint(view["low"] + 1, view["high"] - 1)  # sensible guess
                view = logic.submit_guess(guess)
                if view["found"]:
                    break
                # Then: two numbers are shown and the secret is strictly between them.
                self.assertLess(view["low"], secret, f"seed={seed} guess={guess}")
                self.assertLess(secret, view["high"], f"seed={seed} guess={guess}")
            self.assertTrue(view["found"], f"seed={seed} never found the secret")

        # The games above covered every possible secret, 10 through 99.
        self.assertEqual(secrets_seen, set(range(10, 100)))


if __name__ == "__main__":
    unittest.main()
