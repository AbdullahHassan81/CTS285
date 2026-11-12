"""Stubbed data layer for the DataMan prototype.

Responsibility: store and retrieve. This layer decides NOTHING.
It does not validate guesses, does not know the range rule, and does not
know when a game is finished. Every rule lives in dataman/logic.py.

STUBBED ON PURPOSE:
    Everything is held in plain Python dicts and lists, so all data is lost
    when the program exits. That is acceptable for the Module 4 prototype.
    A JSON-file or database store can replace InMemoryStore later by
    implementing the same methods (see the GameStore protocol below);
    logic.py and app.py should not need to change.
"""

from copy import deepcopy
from typing import Optional, Protocol


class GameStore(Protocol):
    """The store boundary. Logic talks only to these methods."""

    def create_session(self, game: str, play_state: dict) -> int: ...
    def get_play_state(self, session_id: int) -> Optional[dict]: ...
    def save_play_state(self, session_id: int, play_state: dict) -> None: ...
    def save_attempt(self, session_id: int, attempt: dict) -> None: ...
    def list_attempts(self, session_id: int) -> list: ...
    def save_result(self, session_id: int, result: dict) -> None: ...
    def get_result(self, session_id: int) -> Optional[dict]: ...


class InMemoryStore:
    """In-memory implementation of GameStore (the stub)."""

    def __init__(self) -> None:
        self._sessions: dict[int, dict] = {}   # session_id -> {"game", "play_state"}
        self._attempts: list[dict] = []        # one row per guess event
        self._results: dict[int, dict] = {}    # session_id -> final result
        self._next_session_id = 1

    # --- sessions / play state -------------------------------------------
    def create_session(self, game: str, play_state: dict) -> int:
        session_id = self._next_session_id
        self._next_session_id += 1
        self._sessions[session_id] = {"game": game, "play_state": deepcopy(play_state)}
        return session_id

    def get_play_state(self, session_id: int) -> Optional[dict]:
        session = self._sessions.get(session_id)
        # Return a copy so callers cannot change stored state by accident.
        return deepcopy(session["play_state"]) if session else None

    def save_play_state(self, session_id: int, play_state: dict) -> None:
        self._sessions[session_id]["play_state"] = deepcopy(play_state)

    # --- attempts (separate events, saved when they happen) --------------
    def save_attempt(self, session_id: int, attempt: dict) -> None:
        row = deepcopy(attempt)
        row["session_id"] = session_id
        self._attempts.append(row)

    def list_attempts(self, session_id: int) -> list:
        return [deepcopy(a) for a in self._attempts if a["session_id"] == session_id]

    # --- results (meant to outlive the session in a real store) ----------
    def save_result(self, session_id: int, result: dict) -> None:
        self._results[session_id] = deepcopy(result)

    def get_result(self, session_id: int) -> Optional[dict]:
        result = self._results.get(session_id)
        return deepcopy(result) if result else None
