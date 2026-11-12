# DataMan Text-Only Prototype — ST-01: Guess the Secret Number Using Range Hints

Module 4 prototype. This is **not** the finished app. It tests whether the design decisions in my M4 Design Investigation Record still hold when the code has to run. Flask comes in Module 5.

## How to run

```bash
python app.py               # random secret number
python app.py --secret 37   # fixed secret, to demonstrate the acceptance criterion
python app.py --seed 1      # repeatable random secrets
python -m unittest discover -s tests -v   # logic tests, no interface involved
```

Python 3.9+ and the standard library only. Nothing to install.

## Three layers

| Layer | File | Owns | Must not do |
|---|---|---|---|
| Text interface | `app.py` | Reading typed input, turning text into a number, printing results | Decide whether a guess is right, change the range, see the secret before it is revealed |
| Business logic | `dataman/logic.py` | Picking the secret, holding and narrowing the range, the "secret is always between" invariant, counting guesses, deciding when a game ends | Print, read input, or touch stored data directly |
| Stubbed data | `dataman/store.py` | Storing and retrieving sessions, play state, attempts, and results | Make any decision. It validates nothing |

The logic layer only calls the store's methods (`create_session`, `get_play_state`, `save_play_state`, `save_attempt`, `list_attempts`, `save_result`, `get_result`). These are written down as the `GameStore` protocol. `app.py` creates the store in one line (`store = InMemoryStore()`), so a JSON or database store can replace it later.

Every logic function returns plain data, for example:

```python
{"outcome": "hint", "low": 25, "high": 50, "guess_number": 2}
{"outcome": "correct", "guesses": 4, "secret": 37}
{"outcome": "rejected", "reason": "out_of_range", "low": 25, "high": 50}
```

A Flask route in Module 5 can return these same dicts as JSON without changing the logic.

## State, represented on purpose

Each game is a **session**. Its play state, which the logic owns and the store holds, is:

| Field | Why it exists |
|---|---|
| `secret` | The number to find. It stays inside logic/store and is never sent to the interface until the guess is correct |
| `low`, `high` | The current hint. They start at 9 and 100 and only narrow |
| `guess_count` | Counts guesses toward the "number of tries it took" display |
| `status` | `in_progress`, `solved`, or `abandoned` |

Each guess is also saved as its own **attempt** event as soon as it happens (`guess_number`, `guess`, `correct`, `low_shown`, `high_shown`). When a game ends, a **result** record is saved (`status`, `guesses`, `secret`).

## Acceptance criterion demonstrated

> **Given** the system has picked a secret number between 9 and 100, **when** the learner enters a guess, **then** the system displays two numbers and the secret number is between them.

**Through the prototype** (`python app.py --secret 37`, guesses 50, 25, 200, abc, 30, 37):

```
I picked a secret number. It is between these two numbers:
    9   ...   100
Your guess (q to quit):   *flash*   9   ...   50
Your guess (q to quit):   *flash*   25   ...   50
Your guess (q to quit):   200 can't be the secret. It is between 25 and 50.
Your guess (q to quit):   Please type a whole number.
Your guess (q to quit):   *flash*   30   ...   50
Your guess (q to quit):
  YES! The secret was 37.
  Tries: 4
  * * * * *  L I G H T   S H O W  * * * * *
```

Every pair displayed (9–100, 9–50, 25–50, 30–50) has 37 strictly between its two numbers.

**Through the logic alone:** `test_secret_always_between_shown_numbers` plays every possible secret (10–99) with 20 random guess sequences each and checks `low < secret < high` after every hint. `submit_guess` also checks the invariant itself and raises an error instead of displaying a false hint.

## Intentionally stubbed

- **All storage is in memory.** Plain dicts and lists, lost when the program exits. The store boundary is where persistent storage plugs in later.
- **No learner identity.** Sessions aren't attached to a learner yet. The learner → session → attempts structure from the investigation is only partly built (session → attempts).
- **Light show** is one printed line.
- **Curator review** is a basic printout of saved attempts (`session_review`). It shows that the history exists, not how a curator should see it.
- `--secret` exists only for demos and tests. Logic still checks that it is in range.

## Revisions caused by building and running the prototype

1. **The two-try / reveal rule doesn't belong to ST-01.** My investigation's Behavior/State and Interaction findings (EEE on try 1, reveal after try 2, the 10-problem limit, the Memory Bank) come from the manual's Answer Checker / Electro Flash rules. Number Guesser works differently. The manual says the learner keeps guessing until they find the number, and then sees "the number of tries it took." There is no try limit and no reveal. Writing `submit_guess` made this obvious, because no rule in ST-01 needs a "try 2" branch. **What carried over:** the general conclusion still holds. The try count is a decision input owned by logic, not a screen detail. For ST-01 it decides what is reported at the end, not when to reveal the answer. Attempts are still saved as separate events.
2. **"Between 9 and 100" means strictly between.** The secret is 10–99. That is the only reading where the first display (9 … 100) already keeps the manual's promise that the secret is always between the two numbers shown. Guesses of 9 or 100 are rejected because they can never be correct.
3. **The range must only narrow.** My first idea for the update was "a low guess becomes the new low." A guess *below* the current low (for example 15 when the hint is 30–100) would then widen the range back to 15–100. The secret would still be inside, but the learner would lose information they had already earned. `update_range` now uses `max`/`min`, so the range never widens. A guess outside the current range still counts as a try.
4. **The secret never crosses into the interface early.** `start_game` and hint results don't include it. This wasn't in my investigation. Building the interface showed that if the dict contains the secret, the interface can show it by mistake.
5. **First answer to my Next Question ("a session that was never finished").** Quitting with `q` calls `abandon_game`, which marks the session `abandoned` and saves a result while **keeping all saved attempts** (tested in `test_early_quit_keeps_saved_attempts`). This is the early-close scenario from my investigation's New Complication: the history survives. Resuming the game is still deferred, as I decided in Build-Readiness.

## Unresolved uncertainty

- **Cross-session resume** is deferred as its own story. It depends on persistent storage and learner identity.
- **What a curator review shows** is undecided. The data is there, but which view is useful (number of tries per game, range of the search, good vs. wasted guesses) is not.
- **What the timer measures.** The Number Guesser pages in the manual mention no timer, so ST-01 doesn't use one. This is still open for the Electro Flash slices.
- **Should rejected guesses be recorded?** Right now 0, 200, and 9 are not counted and not saved. A curator might want to see them as evidence of confusion. To decide: count them, save them uncounted, or ignore them.
- **Should a "wasted" guess count as a try?** A guess outside the current range (or equal to a bound) currently counts. The manual's "number of tries it took" suggests every real guess counts, but this hasn't been confirmed.
- **The 10-problem limit and Memory Bank constraint** from my investigation are not exercised by ST-01. They belong to a future practice-set slice, and `add_problem_to_set` is not built here.

## Files

```
app.py                  text interface
dataman/__init__.py
dataman/logic.py        business rules
dataman/store.py        stubbed data layer (GameStore protocol + InMemoryStore)
tests/test_logic.py     11 tests, run without the interface
README.md               this file
prompts.md              AI prompts used
```
