# Wordle Solver

Author: Dhruv Iyer

Usage:

```shell
python3 wordle_solver.py <wordlist> [-h] [-i] [-a]
```

`wordlist` is a text file of words in the dictionary. To make things easy, I have included `words.zip`, which you just need to unzip into `words.txt`

If you run `wordle_solver.py` without any additional flags, the program will select a random word from the corpus and guess it.

If you add `-i`, then you launch interactive mode, which helps you solve your own Wordles. The code will give you a guess to enter into a wordle app of your choice. When you get the results, use 'b' to represent black/grey letters, 'y' to represent yellow letters, and 'g' to represent green letters. For example, you might enter `ggbgy`

If you add `-a` (which is only supported if you also set the interactive mode flag `-i`), then the solver can be used to solve the game [Absurdle](https://qntm.org/absurdle). In practice, this means having the solver minimize the size of maximum bucket instead of the size of the expected bucket
