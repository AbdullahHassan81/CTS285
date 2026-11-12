"""Business logic layer for ST-01: Guess the Secret Number Using Range Hints.

Responsibility: own every rule and decision. Nothing here prints, reads
input, or knows what the screen looks like. Every function returns plain
data (dicts) so a text interface today and a Flask route in Module 5 can
both use it unchanged.

Rules owned here (from the M4 investigation record, Layer Boundary Notes):
    * pick the secret number between 9 and 100
    * hold the current low and high bounds
    * update the bounds after each guess
    * keep the secret number strictly between the bounds (the invariant)
    * count guesses and decide when the game is over

Range interpretation (a design decision, see README "Revisions"):
    "between 9 and 100" is read as STRICTLY between, so the secret is
    10..99 and the starting hint is 9 and 100. This is the only reading
    under which the manual's promise "the secret number is always between
    the two numbers I show you" holds on the very first display.
"""

import random
from typing import Optional

from dataman.store import GameStore

GAME_NAME = "number_guesser"
LOW_LIMIT = 9      # exclusive: the secret is never 9
HIGH_LIMIT = 100   # exclusive: the secret is never 100

STATUS_IN_PROGRESS = "in_progress"
STATUS_SOLVED = "solved"
STATUS_ABANDONED = "abandoned"


# ---------------------------------------------------------------------------
# Pure rules (no store, no interface) - easiest to test on their own
# ---------------------------------------------------------------------------
def pick_secret(rng: random.Random) -> int:
    """Pick a secret strictly between LOW_LIMIT and HIGH_LIMIT."""
    return rng.randint(LOW_LIMIT + 1, HIGH_LIMIT - 1)


def is_valid_guess(guess: int) -> bool:
    """A guess must be a whole number that could be the secret (10..99)."""
    return isinstance(guess, int) and LOW_LIMIT < guess < HIGH_LIMIT


def update_range(low: int, high: int, secret: int, guess: int) -> tuple[int, int]:
    """Return the new (low, high) after a wrong guess.

    The range only ever narrows. A guess outside the current range (or equal
    to a bound) teaches nothing new, so the range stays the same instead of
    widening. This is what keeps the invariant true.
    """
    if guess < secret:
        low = max(low, guess)
    elif guess > secret:
        high = min(high, guess)
    return low, high


def secret_is_between(low: int, high: int, secret: int) -> bool:
    """The acceptance-criterion invariant: low < secret < high."""
    return low < secret < high


# ---------------------------------------------------------------------------
# Use-case operations (talk to the store boundary, return data)
# ---------------------------------------------------------------------------
def start_game(store: GameStore, rng: Optional[random.Random] = None,
               secret: Optional[int] = None) -> dict:
    """Start a new game. A new secret is picked every time (manual: "I'll pick
    a new secret number each time you press [???]").

    `secret` may be passed in only for demos and tests; it must still obey
    the range rule.
    """
    rng = rng or random.Random()
    if secret is None:
        secret = pick_secret(rng)
    elif not is_valid_guess(secret):
        raise ValueError(f"secret must be between {LOW_LIMIT} and {HIGH_LIMIT}")

    play_state = {
        "secret": secret,
        "low": LOW_LIMIT,
        "high": HIGH_LIMIT,
        "guess_count": 0,
        "status": STATUS_IN_PROGRESS,
    }
    session_id = store.create_session(GAME_NAME, play_state)
    # Note: the secret is NOT returned. The interface never needs it.
    return {"session_id": session_id, "low": LOW_LIMIT, "high": HIGH_LIMIT}


def submit_guess(store: GameStore, session_id: int, guess: int) -> dict:
    """Apply one guess and return the decision as data.

    Possible outcomes:
        "rejected"  - not a possible secret (outside 10..99); not counted
        "hint"      - wrong; returns the new low/high to display
        "correct"   - found it; returns the total number of guesses
        "game_over" - session already finished; nothing changes
    """
    state = store.get_play_state(session_id)
    if state is None:
        raise KeyError(f"no session {session_id}")

    if state["status"] != STATUS_IN_PROGRESS:
        return {"outcome": "game_over", "status": state["status"]}

    if not is_valid_guess(guess):
        return {"outcome": "rejected", "reason": "out_of_range",
                "low": state["low"], "high": state["high"]}

    state["guess_count"] += 1
    guess_number = state["guess_count"]
    secret = state["secret"]

    if guess == secret:
        state["status"] = STATUS_SOLVED
        # Save the attempt as an event the moment it happens.
        store.save_attempt(session_id, {
            "guess_number": guess_number, "guess": guess, "correct": True,
            "low_shown": None, "high_shown": None,
        })
        store.save_play_state(session_id, state)
        store.save_result(session_id, {
            "game": GAME_NAME, "status": STATUS_SOLVED,
            "guesses": guess_number, "secret": secret,
        })
        return {"outcome": "correct", "guesses": guess_number, "secret": secret}

    low, high = update_range(state["low"], state["high"], secret, guess)

    # Defensive check of the acceptance criterion. If this ever fires, the
    # rule above is wrong - fail loudly rather than show a false hint.
    if not secret_is_between(low, high, secret):
        raise AssertionError(f"range invariant broken: {low} < {secret} < {high}")

    state["low"], state["high"] = low, high
    store.save_attempt(session_id, {
        "guess_number": guess_number, "guess": guess, "correct": False,
        "low_shown": low, "high_shown": high,
    })
    store.save_play_state(session_id, state)
    return {"outcome": "hint", "low": low, "high": high, "guess_number": guess_number}


def abandon_game(store: GameStore, session_id: int) -> dict:
    """Mark an unfinished game as abandoned (learner quit early).

    Attempts already saved are kept - this is the "early close" scenario
    from the investigation record: a quit must not erase history.
    """
    state = store.get_play_state(session_id)
    if state is None:
        raise KeyError(f"no session {session_id}")
    if state["status"] == STATUS_IN_PROGRESS:
        state["status"] = STATUS_ABANDONED
        store.save_play_state(session_id, state)
        store.save_result(session_id, {
            "game": GAME_NAME, "status": STATUS_ABANDONED,
            "guesses": state["guess_count"], "secret": state["secret"],
        })
    return {"status": state["status"], "guesses": state["guess_count"]}


def session_review(store: GameStore, session_id: int) -> dict:
    """What a later reader (e.g. a curator) could see. Minimal on purpose;
    what a curator review should really show is still unresolved."""
    return {
        "result": store.get_result(session_id),
        "attempts": store.list_attempts(session_id),
    }
