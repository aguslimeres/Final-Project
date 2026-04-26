"""
game.py

Contains the Game class, which ties together all components:
  - WordBank (word selection)
  - HangmanLogic (round state)
  - ScoreTracker (session scoring)
  - Renderer (all drawing)

The Game class implements a simple state machine with three states:
  "menu"   → category selection screen
  "playing" → active gameplay
  "result" → win/loss overlay

"""
import pygame
from words import WordBank
from hangman_logic import HangmanLogic
from score_tracker import ScoreTracker
from renderer import Renderer


class Game:
    """
    Top-level game controller that manages state transitions and
    delegates drawing and logic to specialised objects.

    Has-a:
      - WordBank     (word section)
      - HangmanLogic (current-round logic)
      - ScoreTracker (session scoring)
      - Renderer     (all drawing)

    Attributes:
        state (str): One of "menu", "playing", "result".
        word_bank (WordBank): Source of secret words.
        logic (HangmanLogic | None): Logic for the current round, or None.
        score (ScoreTracker): Running session score.
        renderer (Renderer): Handles all pygame drawing.
        category (str): Currently selected category name.
        category_names (list[str]): Sorted list of available categories.
        hovered_category (int): Index of menu button under the mouse (-1 = none).
        points_this_round (int): Points awarded in the most recently finished round.
        play_again_rect, menu_rect (pygame.Rect | None): Result-screen button rects.
    """

    def __init__(self, screen: pygame.Surface):
        """
        Set up the game with all sub-components and enter the menu state.

        Args:
            screen (pygame.Surface): The main pygame display surface.
        """
        self.screen = screen
        self.word_bank = WordBank()
        self.score = ScoreTracker()
        self.renderer = Renderer(screen)

        self.category_names = self.word_bank.get_category_names()
        self.category: str = self.category_names[0]

        self.logic: HangmanLogic | None = None
        self.state: str = "menu"

        self.hovered_category: int = -1
        self.menu_button_rects: list = []

        self.points_this_round: int = 0
        self.play_again_rect: pygame.Rect | None = None
        self.menu_rect: pygame.Rect | None = None

    #State transitions
    def _start_round(self, category: str):
        """
        Begin a new round with the given category.

        Args:
            category (str): Name of the category to draw a word from.
        """
        self.category = category
        word = self.word_bank.get_random_word(category)
        self.logic = HangmanLogic(word)
        self.state = "playing"

    def _end_round(self):
        #Called when a round ends (win or loss).
        #Records the result in ScoreTracker and transitions to the result state.
        if self.logic is None:
            return
        if self.logic.is_won():
            self.points_this_round = self.score.record_win(self.logic.remaining_guesses())
        else:
            self.points_this_round = self.score.record_loss()
        self.state = "result"

    #Event handling
    def handle_event(self, event: pygame.event.Event):
        """
        Route pygame events to the appropriate handler based on current state.

        Args:
            event (pygame.event.Event): The event to process.
        """
        if self.state == "menu":
            self._handle_menu_event(event)
        elif self.state == "playing":
            self._handle_playing_event(event)
        elif self.state == "result":
            self._handle_result_event(event)

    def _handle_menu_event(self, event: pygame.event.Event):
        #Handle events on the category-selection screen.
        if event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            self.hovered_category = -1
            for i, rect in enumerate(self.menu_button_rects):
                if rect.collidepoint(mx, my):
                    self.hovered_category = i
                    break

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for i, rect in enumerate(self.menu_button_rects):
                if rect.collidepoint(mx, my):
                    self._start_round(self.category_names[i])
                    break

    def _handle_playing_event(self, event: pygame.event.Event):
        #Handle keyboard input during an active round.
        if event.type == pygame.KEYDOWN:
            if event.unicode.isalpha() and len(event.unicode) == 1:
                letter = event.unicode.upper()
                if not self.logic.already_guessed(letter):
                    self.logic.guess(letter)
                    # check for round end immediately after each guess
                    if self.logic.is_over():
                        self._end_round()

    def _handle_result_event(self, event: pygame.event.Event):
        #Handle button clicks on the result overlay.
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if self.play_again_rect and self.play_again_rect.collidepoint(mx, my):
                self._start_round(self.category)
            elif self.menu_rect and self.menu_rect.collidepoint(mx, my):
                self.state = "menu"
                self.logic = None

    #Update
    def update(self):
        """
        Per-frame logic update.
        Currently a no-op (all state changes happen in handle_event),
        but kept here as a hook for future animation timers.
        """
        pass

    #Drawing
    def draw(self):
        #Dispatch drawing to the Renderer based on the current state.
        if self.state == "menu":
            self.menu_button_rects = self.renderer.draw_menu(
                self.category_names,
                self.hovered_category,
                self.score.summary(),
            )

        elif self.state == "playing" and self.logic is not None:
            self.renderer.draw_game(
                self.logic,
                self.category,
                self.score.summary(),
            )

        elif self.state == "result" and self.logic is not None:
            #re-draw the game screen underneath the overlay
            self.renderer.draw_game(
                self.logic,
                self.category,
                self.score.summary(),
            )
            mouse_pos = pygame.mouse.get_pos()
            self.play_again_rect, self.menu_rect = self.renderer.draw_result_overlay(
                won = self.logic.is_won(),
                word = self.logic.word,
                points_earned = self.points_this_round,
                mouse_pos = mouse_pos,
            )