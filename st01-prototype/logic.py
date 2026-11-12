"""Business logic for ST-01 (Number Guesser).

Owns every rule: picking the secret, deciding the two numbers shown,
narrowing them after each guess, and deciding when the secret is found.
No print() or input() here; results go back to the caller as plain dicts.

Range rule (the answer to the M4 initial question):
  * "Between" means strictly between: low < secret < high.
  * The game starts by showing 9 and 100, so the secret is picked from 10..99.
  * After a wrong guess, the range narrows TO the guess:
        guess < secret  ->  low  = max(low, guess)
        guess > secret  ->  high = min(high, guess)
  * Bounds only ever move inward. A guess outside the current range
    (e.g. 5, or 95 when high is already 60) counts as a try but cannot
    widen the range, so the secret always stays between the two numbers.
"""

import random

import store

LOWEST = 9
HIGHEST = 100


def narrow(low, high, secret, guess):
    """Return the new (low, high) after a wrong guess. Pure: no store, no I/O."""
    if guess < secret:
        return max(low, guess), high
    return low, min(high, guess)


def new_game(seed=None):
    """Pick a secret strictly between LOWEST and HIGHEST and save a fresh game."""
    rng = random.Random(seed)
    secret = rng.randint(LOWEST + 1, HIGHEST - 1)
    store.start_game(secret, LOWEST, HIGHEST)
    return {"found": False, "low": LOWEST, "high": HIGHEST, "tries": 0}


def submit_guess(guess):
    """Apply one guess. Returns what the interface should show, as data."""
    if not isinstance(guess, int) or isinstance(guess, bool):
        raise TypeError("guess must be a whole number")

    game = store.load_game()
    if "secret" not in game:
        raise RuntimeError("no game in progress; call new_game() first")
    if game["secret"] in game["guesses"]:
        raise RuntimeError("this game is already over; call new_game() to play again")

    secret, low, high = game["secret"], game["low"], game["high"]
    found = guess == secret
    if not found:
        low, high = narrow(low, high, secret, guess)

    store.save_guess(guess, low, high)
    return {"found": found, "low": low, "high": high, "tries": len(game["guesses"]) + 1}
