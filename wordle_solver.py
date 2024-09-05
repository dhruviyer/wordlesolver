import random
import logging
import argparse
import sys
import re

INITIAL_GUESS = "tares"
INITIAL_GUESS_ABSURDLE = "aloes"

logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.NOTSET,
    filename="logs.txt",
    filemode="w",
)


def compare(w, u):
    w = [c for c in w]
    u = [c for c in u]

    results = ["b" for _ in range(len(w))]

    # First pass: mark any letters that are fully correct with 'green'
    for i in range(len(u)):
        if w[i] == u[i]:
            results[i] = "g"
            u[i] = " "

    # Second pass: mark any partially correct letters with yellow
    for i in range(len(u)):
        if w[i] in u and results[i] != "g":
            results[i] = "y"
            u[u.index(w[i])] = " "

    return "".join(results)


def compute_buckets(w, W):
    buckets = {}

    for u in W:
        if w == u:
            continue
        comparison_string = compare(w, u)
        if comparison_string not in buckets:
            buckets[comparison_string] = set()
        buckets[comparison_string].add(u)

    return buckets


def compute_next_guess(W):
    best_guess = ""
    min_expectation = 1e9

    if len(W) == 0:
        print("Error: could not find a valid word")
        sys.exit(0)

    for w in W:
        n = len(W) - 1
        expectation = 0
        buckets = compute_buckets(w, W)
        for key in buckets.keys():
            k = len(buckets[key])
            expectation += k * k / n

        if expectation < min_expectation:
            best_guess = w
            min_expectation = expectation

    return best_guess


def compute_next_guess_absurdle(W):
    best_guess = ""
    best_max_bucket = 1e9

    if len(W) == 0:
        print("Error: could not find a valid word")
        sys.exit(0)

    for w in W:
        max_bucket = -1
        buckets = compute_buckets(w, W)
        for key in buckets.keys():
            k = len(buckets[key])
            max_bucket = max(k, max_bucket)

        if max_bucket < best_max_bucket:
            best_guess = w
            best_max_bucket = max_bucket

    return best_guess


def run_non_interactive(words):
    solution = random.choice(words)
    logging.info("Solution is: %s", solution)

    guess = INITIAL_GUESS
    W = words
    num_guesses = 1

    logging.info("Guess is: %s", guess)

    result_bucket = compare(guess, solution)

    logging.info("Result is: %s", result_bucket)

    while result_bucket != "g" * len(solution):
        guess_buckets = compute_buckets(guess, W)
        W = guess_buckets[result_bucket]

        guess = compute_next_guess(W)
        num_guesses += 1
        logging.info("Guess is: %s", guess)
        result_bucket = compare(guess, solution)
        logging.info("Result is: %s", result_bucket)

    print(f"""Found "{guess}" in {num_guesses} tries""")
    sys.exit(0)


def get_user_input():
    try:
        while True:
            user_input = input("> ").lower()
            user_input = re.sub(r"[^a-z]", "", user_input)

            # Check if the input represents a valid result
            valid_result_pattern = r"^[byg]{5}$"

            if bool(re.match(valid_result_pattern, user_input)):
                return user_input
            else:
                print("Error: Invalid input. Only enter b, y, or g")

    except KeyboardInterrupt:
        sys.exit(0)


def run_interactive(words, absurdle=False):
    W = words
    guess = INITIAL_GUESS if not absurdle else INITIAL_GUESS_ABSURDLE
    num_guesses = 1

    logging.info("Guess is: %s", guess)
    print(f"""Suggested guess is: {guess}""")

    result_bucket = get_user_input()

    logging.info("Result is: %s", result_bucket)

    while result_bucket != "g" * len(result_bucket):
        guess_buckets = compute_buckets(guess, W)
        W = guess_buckets[result_bucket]

        guess = (
            compute_next_guess(W) if not absurdle else compute_next_guess_absurdle(W)
        )
        num_guesses += 1
        print(f"""Suggested guess is: {guess}""")

        result_bucket = get_user_input()

        logging.info("Result is: %s", result_bucket)

    print(f"""Found "{guess}" in {num_guesses} tries""")
    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="WordleSolver",
        description="Solves wordle",
        epilog="Check out the substack! https://dhruviyer.substack.com",
    )
    parser.add_argument("wordlist", help="The list of english words")
    parser.add_argument(
        "-i", "--interactive", help="Run in interactive mode", action="store_true"
    )
    parser.add_argument(
        "-a", "--absurdle", help="Absurdle variant", action="store_true"
    )

    args = parser.parse_args()

    try:
        f = open(args.wordlist)
        words = f.read().splitlines()
        f.close()
    except FileNotFoundError:
        print(f"""\nError: file "{args.wordlist}" not found. Does it exist?\n""")
        sys.exit(-1)

    interactive_mode = args.interactive

    if interactive_mode:
        print(
            """\nWelcome to Interactive Mode!\n============================\nDirections:\n\nI will give you a suggested guess. Feed it to your Wordle app.\n\nThen, come here and enter the result as a 5-character string.\n\nUse "b" for black/grey, "y" for yellow, and "g" for green.\n============================\n"""
        )
        run_interactive(words, absurdle=args.absurdle)
    else:
        run_non_interactive(words)
