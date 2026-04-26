"""
words.py

Contains all word categories and the WordBank class used to select
random words during the game.

Each category is a list of uppercase strings. The WordBank class
is a way for picking a random word from a chosen
category or from options.

"""

import random

#Word lists by category
CATEGORIES = {
    "Animals": [
        "ELEPHANT", "GIRAFFE", "PENGUIN", "DOLPHIN", "CHEETAH",
        "KANGAROO", "POLAR BEAR", "CROCODILE", "FLAMINGO", "PORCUPINE",
        "GREAT WHITE SHARK", "WOLF", "SEA TURTLE", "CAT", "OCTOPUS",
    ],
    "Countries": [
        "ARGENTINA", "AUSTRALIA", "BRAZIL", "CANADA", "DENMARK",
        "ETHIOPIA", "FINLAND", "GERMANY", "HUNGARY", "ICELAND",
        "JAMAICA", "KENYA", "LUXEMBOURG", "MOROCCO", "NETHERLANDS",
        "PORTUGAL", "SINGAPORE", "THAILAND", "UKRAINE", "VIETNAM",
    ],
    "Food": [
        "AVOCADO", "BLUEBERRY", "STRAWBERRY", "DUMPLING", "ENCHILADA",
        "FALAFEL", "GUACAMOLE", "HUMMUS", "JALAPENO", "YOGURT",
        "LASAGNA", "MOZZARELLA", "PANCAKE", "QUESADILLA", "RISOTTO",
        "BAGEL", "TIRAMISU", "WAFFLE", "ZUCCHINI", "CROISSANT",
    ],
    "Sports": [
        "BASKETBALL", "VOLLEYBALL", "BADMINTON", "LACROSSE", "SWIMMING",
        "GYMNASTICS", "WRESTLING", "ARCHERY", "POLO", "HANDBALL",
        "SKATEBOARD", "SNOWBOARD", "KAYAKING", "SOCCER", "WATERPOLO",
    ],
    "LMU": [
        "IGGY", "PALM TREE", "SEAVER", "ENGINEER", "COMP SCI",
        "THE BLUFF", "SUN", "BEACH", "LIBRARY", "LAIR",
        "THE DEN", "PALM NORTH", "UHALL", "VDA", "ST ROBERTS",
    ],
}

CATEGORY_NAMES = list(CATEGORIES.keys())

class WordBank:
    """
    Manages word selection for the Hangman game.

    Has-a: a dictionary of category → word list (CATEGORIES).

    Attributes:
        categories (dict): Maps category name strings to lists of words.
    """

    def __init__(self):
        """Create a WordBank loaded with all built-in categories."""
        self.categories = CATEGORIES

    def get_random_word(self, category: str) -> str:
        """
        Return a random word from the given category.

        Args:
            category (str): A key from self.categories.

        Returns:
            str: An uppercase word string.

        Raises:
            KeyError: If the category does not exist.
        """
        return random.choice(self.categories[category])

    def get_category_names(self) -> list:
        #Return a sorted list of all available category names.
        return sorted(self.categories.keys())