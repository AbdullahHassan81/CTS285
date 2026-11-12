"""Stubbed data layer for ST-01 (Number Guesser).

This layer stores and retrieves. It decides nothing: no comparisons,
no range rules, no "is this guess right?". A JSON or database store can
replace this file later by providing the same three functions.

Stub: everything lives in one in-memory dict and is lost when the
program exits.
"""

_game = {}


def start_game(secret, low, high):
    """Replace any current game with a new one."""
    _game.clear()
    _game.update({"secret": secret, "low": low, "high": high, "guesses": []})


def save_guess(guess, low, high):
    """Record one guess and the bounds the logic layer decided on."""
    _game["guesses"].append(guess)
    _game["low"] = low
    _game["high"] = high


def load_game():
    """Return a copy of the current game, so callers cannot edit the store directly."""
    return {**_game, "guesses": list(_game.get("guesses", []))}
