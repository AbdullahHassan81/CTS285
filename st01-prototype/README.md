# ST-01 Prototype: Guess the Secret Number Using Range Hints

A small three-layer text prototype of DataMan's *Number Guesser*. The learner guesses, the system shows two numbers, and the secret number is always between them.

## How to run

```
python main.py          # random secret
python main.py 7        # seeded: secret is 51 every time (handy for demos)
python -m unittest test_ac1 -v
```

Needs only Python 3 (standard library). Tested with Python 3.13.

## The range rule (answer to the M4 initial question)

The design record asked how the system picks the two numbers and what it must remember. This prototype answers it:

1. **"Between" means strictly between:** `low < secret < high`. The manual says the secret is "between 9 and 100" and that it is "always between the two numbers shown." Reading "between" the same way in both places means the secret is picked from **10 to 99**, and the first screen shows **9 and 100**.
2. **The range narrows to the guess.** After a wrong guess:
   - guess too low → `low = max(low, guess)`
   - guess too high → `high = min(high, guess)`
3. **Bounds only move inward.** A guess outside the current range still counts as a try, but it can't widen the range. If the learner guesses 150 while the range is 9–100, the range stays 9–100.

I considered one alternative and rejected it: showing the tightest possible range (`guess + 1` / `guess - 1`). That would display numbers the learner never typed, and "between" would have to mean "including." Narrowing to the guess matches the manual and keeps one meaning of "between" everywhere.

**State that has to persist between guesses:** the secret, the current low, the current high, and the list of guesses (its length is the try count shown at the end).

## Where each layer is

| Layer | File | Job | Never does |
|---|---|---|---|
| Text interface | `main.py` | Reads a guess, turns the text into an int, prints the two numbers or the "found it" message | Compare numbers, change the range, touch the store |
| Business logic | `logic.py` | Picks the secret, holds the range rule (`narrow()`), decides when the secret is found, counts tries | `print()` or `input()`. It returns plain dicts such as `{"found": False, "low": 50, "high": 75, "tries": 2}` |
| Stubbed data | `store.py` | Holds `secret`, `low`, `high`, `guesses` in one dict behind `start_game()`, `save_guess()`, `load_game()` | Make any decision. `load_game()` returns a copy, so nothing outside the store can edit the stored data |

The interface only calls `logic.new_game()` and `logic.submit_guess()`. Only `logic.py` imports `store.py`.

## What is stubbed

- **Storage:** an in-memory dict. Everything is lost when the program exits. A JSON or database store can replace `store.py` later by providing the same three functions, with no change to `logic.py` or `main.py`.
- **One game at a time, one learner.** The record's learner → session → attempts structure isn't built yet. Right now the store holds one game.
- **The light show** is a line of asterisks.
- **Not part of ST-01, so not built:** Answer Checker's two-tries/EEE/reveal logic, Memory Bank sets and the 10-problem limit, the timer, and curator review.

## What running it showed

**A normal game (`python main.py 7`, secret 51):**

```
I picked a secret number. It is between these two numbers:
   9   100
Your guess: 50
   50   100
Your guess: 75
   50   75
Your guess: 62
   50   62
Your guess: 56
   50   56
Your guess: 53
   50   53
Your guess: 51
You found it in 6 tries!  * * * light show * * *
```

**Bad and out-of-range input (same secret):**

```
   9   100
Your guess: abc
Please type a whole number.
Your guess: 5
   9   100
Your guess: 150
   9   100
Your guess: 60
   9   60
Your guess: 51
You found it in 4 tries!  * * * light show * * *
```

What the runs showed:

- Each wrong guess becomes one of the two numbers, and the secret (51) stays strictly between them every time.
- Guesses of 5 and 150 counted as tries but didn't widen the range. That is the case the "bounds only move inward" rule exists for. A naive `low = guess` would have shown `5 100`. That's still true, but it would *widen* the range and throw away information the learner had already earned.
- "abc" is rejected by the interface and doesn't count as a try. Turning text into a number is input handling. Deciding what a number means is logic.

**AC-1 test (`test_ac1.py`):**

```
test_secret_is_strictly_between_the_two_numbers_after_every_guess ... ok
Ran 1 test in 0.067s
OK
```

The test plays 3,000 seeded games through the real `logic.new_game()` and `logic.submit_guess()`, covering every possible secret from 10 to 99. It mixes sensible guesses with careless ones from 0 to 110. After the start and after every wrong guess, it checks `low < secret < high`. It also checks that every game ends with the secret found.

**Layer check:** `grep` for `print(` and `input(` in `logic.py` and `store.py` matches only the docstring line that says there are none.

## Trace back to product work

**AC-1:** *Given* the system has picked a secret number between 9 and 100, *when* the learner enters a guess, *then* the system displays two numbers and the secret number is between them. → `test_ac1.py`, passing.

## Open questions carried forward

- How should the system represent a game that was never finished (the learner quits mid-game)? Right now it is simply lost.
- Should guesses outside 9–100 be rejected outright instead of counted as a try? The manual doesn't say. This prototype counts them.
