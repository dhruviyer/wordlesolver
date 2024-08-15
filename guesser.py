import random
import numpy as np


class Guesser:
    def __init__(self, initial_wordlist):
        self.wordlist = initial_wordlist

        options = ["b", "g", "y"]
        self.results_list = [
            [a, b, c, d, e]
            for a in options
            for b in options
            for c in options
            for d in options
            for e in options
        ]

    def count_e_in_str(self, e, str):
        count = 0
        for i in range(5):
            if str[i] == e:
                count += 1
        return count

    def get_sample_size(self):
        return len(self.wordlist)

    def has_guesses(self):
        return len(self.wordlist) >= 1

    def guess_random(self):
        return random.choice(self.wordlist)

    def prune_search_space(self, guess, results, simulation=False):
        """Takes the current wordlist and prunes it based on the current list of acceptable results

        simulation -- True if we are testing a word/result pair for guess, False for when we are pruning for real

        """

        letter_dict = {}
        wordlist = self.wordlist.copy()

        # use the result to create waypoint around letter freq. in final word
        for i in range(5):
            if guess[i] not in letter_dict.keys():
                letter_dict[guess[i]] = [0, False]
            if results[i] != "b":
                letter_dict[guess[i]][0] = letter_dict[guess[i]][0] + 1
            else:
                letter_dict[guess[i]][1] = True

        # prune initial search space based on green (inclusion) and yellow (exclusion) criteria
        for i in range(5):
            if results[i] == "g":
                wordlist = [cand for cand in wordlist if cand[i] == guess[i]]
            if results[i] == "y":
                wordlist = [cand for cand in wordlist if cand[i] != guess[i]]

        # Preserve words where letter frequency > known frequency > 0 or letter frequency = known frequnecy = 0, keep track of hard and soft limits
        for letter in letter_dict.keys():

            def validate(cand):
                both_zero = (
                    self.count_e_in_str(letter, cand) == 0
                    and letter_dict[letter][0] == 0
                )
                hard_limit_frequency_match = (
                    self.count_e_in_str(letter, cand) == letter_dict[letter][0]
                    and letter_dict[letter][1]
                )
                soft_limit_plausibility = (
                    self.count_e_in_str(letter, cand) >= letter_dict[letter][0]
                    and not letter_dict[letter][1]
                )
                return (
                    both_zero or hard_limit_frequency_match or soft_limit_plausibility
                )

            wordlist = list(filter(validate, wordlist))

        if not simulation:
            self.wordlist = wordlist

        return len(wordlist)

    def prune_result_space(self, guess, results):
        """Prunes the list of acceptable results to only those that align with our current knowledge of correct letters"""

        for i in range(5):
            if results[i] == "g":
                self.results_list = [
                    cand for cand in self.results_list if cand[i] == results[i]
                ]

        self.prune_search_space(guess, results)

    def guess_educated(self):
        """Selects the next guess based on the word that has the minimum expected # of words based on all possible results"""

        guess = random.choice(self.wordlist)
        best_word_count = 6000

        for candidate in self.wordlist:
            totals = []

            for result in self.results_list:
                totals.append(
                    self.prune_search_space(candidate, result, simulation=True)
                )

            total_words = np.sum(totals)
            expected_num_words = 0
            for value in totals:
                expected_num_words += (value * value) / total_words
            if expected_num_words < best_word_count:
                guess = candidate
                best_word_count = expected_num_words

        return guess
