import random
from evaluator import Evaluator
from guesser import Guesser
from bcolors import bcolors

INTERACTIVE_MODE = True
NUM_ITERATIONS = 100

f = open("words.txt")
words = f.read().splitlines()
f.close()

frequency = {}

f = open("words.txt")
words = f.read().splitlines()
f.close()

evaluator = Evaluator(random.choice(words))
print("Word is: " + evaluator.solution)
guesser = Guesser(words)
tries = 0

while guesser.has_guesses():
    guess = "tares" if tries == 0 else guesser.guess_educated()
    tries += 1
    results, is_solved = evaluator.evaluate(guess)
    if INTERACTIVE_MODE:
        results_string = []
        for j in range(5):
            if results[j] == "b":
                results_string.append(guess[j])
            elif results[j] == "g":
                results_string.append(bcolors.OKGREEN + guess[j] + bcolors.ENDC)
            else:
                results_string.append(bcolors.WARNING + guess[j] + bcolors.ENDC)
        print("  ".join(results_string))
    if is_solved:
        break
    guesser.update_search_space_educated(guess, results)

if INTERACTIVE_MODE:
    print("=============")
    print(
        "Solution: "
        + evaluator.solution
        + "\nSolved in: "
        + str(tries)
        + " attempts \n"
    )
