class Evaluator:
    def __init__(self, solution):
        self.solution = solution

    def evaluate(self, guess, debug=False):
        comparison_string = list(self.solution)
        results = ["b", "b", "b", "b", "b"]

        # First pass: mark any letters that are fully correct with 'green'
        for i in range(5):
            if debug:
                print(comparison_string)
            if guess[i] == comparison_string[i]:
                results[i] = "g"
                comparison_string[i] = " "

        # Second pass: mark any partially correct letters with yellow
        for i in range(5):
            if guess[i] in comparison_string and results[i] != "g":
                results[i] = "y"
                comparison_string[comparison_string.index(guess[i])] = " "

        return results, results == ["g", "g", "g", "g", "g"]
