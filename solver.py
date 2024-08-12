from guesser import Guesser
from bcolors import bcolors

INTERACTIVE_MODE = False

f = open("words.txt")
words = f.read().splitlines()
f.close()

frequency = {}

dictionary = words
guesser = Guesser(dictionary)
tries = 0

while True:
    if not guesser.has_guesses():
        print("=============")
        print("Failed")
        break
    if tries == 0:
        guess = "tares"  # guesser.guess_educated()
    else:
        guess = guesser.guess_educated()
    tries += 1
    print(
        "Guess #"
        + str(tries)
        + ": "
        + guess
        + " ("
        + str(guesser.get_sample_size())
        + " possibilities remain)"
    )
    try:
        results = input("--> ").split(" ")

    except KeyboardInterrupt:
        print("")
        break
    print("=============")
    results_string = []
    for j in range(5):
        if results[j] == "b":
            results_string.append(guess[j])
        elif results[j] == "g":
            results_string.append(bcolors.OKGREEN + guess[j] + bcolors.ENDC)
        else:
            results_string.append(bcolors.WARNING + guess[j] + bcolors.ENDC)
    print("  ".join(results_string))
    if results == ["g", "g", "g", "g", "g"]:
        print("=============")
        print("SOLVED!")
        break
    guesser.update_educated(guess, results)
