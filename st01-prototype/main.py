"""Text interface for ST-01 (Number Guesser).

Input and output only. Every decision comes from logic.py; this file
never compares numbers or touches the store.

Run:  python main.py          (random secret)
      python main.py 42       (seeded, so the same secret every time)
"""

import sys

import logic


def ask_for_guess():
    """Keep asking until the learner types a whole number."""
    while True:
        text = input("Your guess: ").strip()
        try:
            return int(text)
        except ValueError:
            print("Please type a whole number.")


def show_range(view):
    print(f"   {view['low']}   {view['high']}")


def main(seed=None):
    view = logic.new_game(seed)
    print("I picked a secret number. It is between these two numbers:")
    show_range(view)
    while True:
        view = logic.submit_guess(ask_for_guess())
        if view["found"]:
            print(f"You found it in {view['tries']} tries!  * * * light show * * *")
            return
        show_range(view)


if __name__ == "__main__":
    try:
        main(int(sys.argv[1]) if len(sys.argv) > 1 else None)
    except (EOFError, KeyboardInterrupt):
        print("\nBye!")
