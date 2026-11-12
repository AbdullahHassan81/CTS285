"""Text interface layer for ST-01 (Number Guesser).

Responsibility: input and output ONLY.
    * reads what the learner types
    * turns text into a number (or reports that it is not one)
    * calls the logic layer
    * formats whatever the logic layer returns

It never checks whether a guess is right, never changes the range, and never
sees the secret number until the logic layer reveals it on a correct guess.

Run:
    python app.py               # random secret
    python app.py --secret 37   # fixed secret, for demonstrating the AC
    python app.py --seed 1      # repeatable random secrets
"""

import argparse
import random

from dataman import logic
from dataman.store import InMemoryStore


def show_review(store, session_id):
    review = logic.session_review(store, session_id)
    print("\n  Saved history for this game:")
    for a in review["attempts"]:
        if a["correct"]:
            print(f"    guess {a['guess_number']}: {a['guess']}  -> correct")
        else:
            print(f"    guess {a['guess_number']}: {a['guess']}  -> showed "
                  f"{a['low_shown']} ... {a['high_shown']}")
    result = review["result"]
    if result:
        print(f"  Result: {result['status']}, {result['guesses']} counted guess(es)\n")


def play_one_game(store, rng, secret=None):
    game = logic.start_game(store, rng=rng, secret=secret)
    session_id = game["session_id"]

    print("\nI picked a secret number. It is between these two numbers:")
    print(f"    {game['low']}   ...   {game['high']}")

    while True:
        text = input("Your guess (q to quit): ").strip().lower()

        if text == "q":
            outcome = logic.abandon_game(store, session_id)
            print(f"Game stopped after {outcome['guesses']} guess(es).")
            break

        # Converting typed text to a number is an input concern, so it stays
        # here. Deciding if that number is ALLOWED is a rule, so it does not.
        try:
            guess = int(text)
        except ValueError:
            print("  Please type a whole number.")
            continue

        result = logic.submit_guess(store, session_id, guess)

        if result["outcome"] == "rejected":
            print(f"  {guess} can't be the secret. It is between "
                  f"{result['low']} and {result['high']}.")
        elif result["outcome"] == "hint":
            print(f"  *flash*   {result['low']}   ...   {result['high']}")
        elif result["outcome"] == "correct":
            print(f"\n  YES! The secret was {result['secret']}.")
            print(f"  Tries: {result['guesses']}")
            print("  * * * * *  L I G H T   S H O W  * * * * *")
            break
        elif result["outcome"] == "game_over":
            print("  This game is already over.")
            break

    show_review(store, session_id)


def main():
    parser = argparse.ArgumentParser(description="DataMan Number Guesser (text prototype)")
    parser.add_argument("--secret", type=int, help="fixed secret for demos (10-99)")
    parser.add_argument("--seed", type=int, help="seed for repeatable random secrets")
    args = parser.parse_args()

    store = InMemoryStore()          # swap this line for a real store later
    rng = random.Random(args.seed)

    print("=== DataMan: NUMBER GUESSER [???] ===")
    first = True
    while True:
        play_one_game(store, rng, secret=args.secret if first else None)
        first = False
        again = input("Press Enter for a new secret number, or q to turn off: ")
        if again.strip().lower() == "q":
            print("DataMan OFF.")
            break


if __name__ == "__main__":
    main()
