"""
hangman_logic.py

Contains the HangmanLogic class, which manages all game-state logic
independent of rendering: the secret word, guessed letters, win/loss
detection, and remaining attempts.

This separation of logic from display makes the code easier to test
and extend.

"""

class HangmanLogic:
    """
    Tracks the state of a single Hangman round.

    Is-a: standalone model object (no pygame dependency).
    Has-a: a secret word, a set of guessed letters.

    Attributes:
        MAX_WRONG (int): Number of wrong guesses allowed before game over.
        word (str): The secret uppercase word.
        guessed_letters (set): Letters the player has already tried.
        wrong_count (int): Number of incorrect guesses so far.
    """

    MAX_WRONG = 6  # corresponds to 6 hangman drawing stages

    def __init__(self, word: str):
        """
        Initialize a new round with the given secret word.

        Args:
            word (str): The uppercase secret word to guess.
        """
        self.word = word.upper()
        self.guessed_letters: set = set()
        self.wrong_count: int = 0

    #Guessing
    def guess(self, letter: str) -> bool:
        """
        Process a single letter guess.

        Args:
            letter (str): A single uppercase letter A–Z.

        Returns:
            bool: True if the letter is in the word, False otherwise.
                  Returns False (no effect) if the letter was already guessed.
        """
        letter = letter.upper()
        if letter in self.guessed_letters:
            return False  # already guessed; ignore

        self.guessed_letters.add(letter)

        if letter in self.word:
            return True
        else:
            self.wrong_count += 1
            return False

    def already_guessed(self, letter: str) -> bool:
        #Return True if this letter has already been tried.
        return letter.upper() in self.guessed_letters

    #Status helpers
    def get_display_word(self) -> list:
        """
        Return the word as a list of revealed characters and blanks.

        Each element is either the letter (str) if it has been guessed,
        or '_' if it is still hidden.

        Returns:
            list[str]: e.g. ['H', '_', '_', 'S', '_'] for "HORSE"
                       when only H and S have been guessed.
        """
        return [ch if (ch in self.guessed_letters or ch == " ") else "_" for ch in self.word]


    def is_won(self) -> bool:
        #Return True if every letter in the word has been guessed.
        return all(ch in self.guessed_letters or ch == " " for ch in self.word)

    def is_lost(self) -> bool:
        #Return True if the player has used up all allowed wrong guesses.
        return self.wrong_count >= self.MAX_WRONG

    def is_over(self) -> bool:
        #Return True if the round has ended (win or loss).
        return self.is_won() or self.is_lost()

    def remaining_guesses(self) -> int:
        #Return how many wrong guesses the player still has left.
        return self.MAX_WRONG - self.wrong_count