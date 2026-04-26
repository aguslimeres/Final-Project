"""
renderer.py

Contains the Renderer class, which is responsible for ALL the drawing
operations in the Hangman game using pygame.

The Renderer is intentionally separated from game logic so that
HangmanLogic and ScoreTracker can be understood and tested without
any pygame dependency.
"""

import pygame

#Color palette
BG_COLOR        = (15,  17,  26)   # deep navy
PANEL_COLOR     = (25,  30,  45)   # slightly lighter panel
ACCENT          = (255, 200,  50)  # golden yellow
ACCENT_DIM      = (180, 140,  30)
TEXT_PRIMARY    = (230, 235, 255)  # near-white
TEXT_SECONDARY  = (140, 150, 190)  # muted blue-grey
WRONG_COLOR     = (220,  60,  60)  # red for wrong guesses
CORRECT_COLOR   = ( 60, 210, 120)  # green for correct
GALLOWS_COLOR   = (190, 200, 220)
BODY_COLOR      = (230, 235, 255)
BTN_COLOR       = (40,  50,  75)
BTN_HOVER       = (60,  75, 110)
BTN_BORDER      = ACCENT


class Renderer:
    """
    Draws all game screens using pygame surfaces.

    Is-a: standalone drawing helper (no game logic).
    Has-a: a reference to the pygame display surface and several Font objects.

    Attributes:
        screen (pygame.Surface): The main display surface.
        fonts (dict): Named font objects of various sizes.
        W, H (int): Screen width and height.
    """

    def __init__(self, screen: pygame.Surface):
        """
        Create a Renderer for the given screen surface.

        Args:
            screen (pygame.Surface): The pygame display surface to draw on.
        """
        self.screen = screen
        self.W, self.H = screen.get_size()
        self._load_fonts()

    #Font loading

    def _load_fonts(self):
        #Load all font sizes used throughout the game.
        self.fonts = {
            "title":   pygame.font.SysFont("Georgia", 52, bold=True),
            "large":   pygame.font.SysFont("Georgia", 36, bold=True),
            "medium":  pygame.font.SysFont("Courier New", 26, bold=True),
            "small":   pygame.font.SysFont("Courier New", 20),
            "tiny":    pygame.font.SysFont("Courier New", 16),
            "letter":  pygame.font.SysFont("Courier New", 28, bold=True),
            "word":    pygame.font.SysFont("Courier New", 38, bold=True),
        }

    #Utility helpers
    def _text(self, text: str, font_key: str, color, center):
        #Render a text string centered at the given (x, y) point.
        surf = self.fonts[font_key].render(text, True, color)
        rect = surf.get_rect(center=center)
        self.screen.blit(surf, rect)
        return rect

    def _text_left(self, text: str, font_key: str, color, topleft):
        #Render a text string with the given top-left origin.
        surf = self.fonts[font_key].render(text, True, color)
        rect = surf.get_rect(topleft=topleft)
        self.screen.blit(surf, rect)
        return rect

    def _panel(self, rect: pygame.Rect, radius: int = 12):
        #Draw a rounded-rectangle panel.
        pygame.draw.rect(self.screen, PANEL_COLOR, rect, border_radius=radius)
        pygame.draw.rect(self.screen, ACCENT_DIM, rect, width=1, border_radius=radius)

    #Background
    def draw_background(self):
        """Fill the screen with the background colour."""
        self.screen.fill(BG_COLOR)

    #Hangman figure
    def draw_gallows(self, wrong_count: int):
        """
        Draw the gallows structure and progressively reveal the hanged figure.

        Args:
            wrong_count (int): Number of wrong guesses (0–6).
        """
        ox, oy = 120, 80   # origin of the gallows drawing

        #static gallows
        pygame.draw.line(self.screen, GALLOWS_COLOR, (ox, oy + 320), (ox + 200, oy + 320), 5)  # base
        pygame.draw.line(self.screen, GALLOWS_COLOR, (ox + 80, oy + 320), (ox + 80, oy), 5)    # pole
        pygame.draw.line(self.screen, GALLOWS_COLOR, (ox + 80, oy), (ox + 180, oy), 5)          # top bar
        pygame.draw.line(self.screen, GALLOWS_COLOR, (ox + 180, oy), (ox + 180, oy + 50), 4)    # rope

        cx = ox + 180  # center-x of the figure

        #figure parts revealed in order
        if wrong_count >= 1:  # head
            pygame.draw.circle(self.screen, BODY_COLOR, (cx, oy + 75), 25, 3)
        if wrong_count >= 2:  # body
            pygame.draw.line(self.screen, BODY_COLOR, (cx, oy + 100), (cx, oy + 200), 3)
        if wrong_count >= 3:  # left arm
            pygame.draw.line(self.screen, BODY_COLOR, (cx, oy + 130), (cx - 40, oy + 165), 3)
        if wrong_count >= 4:  # right arm
            pygame.draw.line(self.screen, BODY_COLOR, (cx, oy + 130), (cx + 40, oy + 165), 3)
        if wrong_count >= 5:  # left leg
            pygame.draw.line(self.screen, BODY_COLOR, (cx, oy + 200), (cx - 40, oy + 250), 3)
        if wrong_count >= 6:  # right leg + sad face
            pygame.draw.line(self.screen, BODY_COLOR, (cx, oy + 200), (cx + 40, oy + 250), 3)
            #sad face
            pygame.draw.circle(self.screen, WRONG_COLOR, (cx - 9, oy + 68), 4)
            pygame.draw.circle(self.screen, WRONG_COLOR, (cx + 9, oy + 68), 4)
            pygame.draw.arc(self.screen, WRONG_COLOR,
                            pygame.Rect(cx - 12, oy + 82, 24, 14), 0, 3.14, 2)

    #Word display

    def draw_word(self, display_word: list, category: str):
        """
        Draw the partially-revealed word as spaced letter blanks.
        Spaces between words are shown as a gap with no underline.

        Args:
            display_word (list[str]): Output of HangmanLogic.get_display_word().
            category (str): The category name shown as a hint label.
        """
        # category label
        self._text(f"Category: {category}", "small", TEXT_SECONDARY,
                   (self.W // 2 + 60, 40))

        # letter blanks
        letter_w = 38
        spacing = 12
        total_w = len(display_word) * (letter_w + spacing) - spacing
        start_x = self.W // 2 + 60 - total_w // 2
        y = self.H // 2 - 20

        for i, ch in enumerate(display_word):
            x = start_x + i * (letter_w + spacing)
            center_x = x + letter_w // 2

            if ch == " ":
                # gap between words — no letter, no underline
                pass
            elif ch == "_":
                # blank line
                pygame.draw.line(self.screen, TEXT_SECONDARY,
                                 (x + 3, y + 36), (x + letter_w - 3, y + 36), 2)
            else:
                # revealed letter
                self._text(ch, "word", CORRECT_COLOR, (center_x, y + 18))
                pygame.draw.line(self.screen, ACCENT_DIM,
                                 (x + 3, y + 36), (x + letter_w - 3, y + 36), 2)

    #Keyboard grid

    def draw_keyboard(self, guessed_letters: set, word: str):
        """
        Draw an on-screen A–Z keyboard showing which letters have been used.

        Args:
            guessed_letters (set): Letters already guessed.
            word (str): The secret word (to colour correct letters green).
        """
        rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        key_size = 38
        gap = 6
        start_y = self.H - 200

        for row_i, row in enumerate(rows):
            row_w = len(row) * (key_size + gap) - gap
            start_x = self.W // 2 + 60 - row_w // 2 + row_i * 18

            for col_i, letter in enumerate(row):
                x = start_x + col_i * (key_size + gap)
                rect = pygame.Rect(x, start_y + row_i * (key_size + gap), key_size, key_size)

                if letter in guessed_letters:
                    if letter in word:
                        bg = (30, 100, 55)
                        border = CORRECT_COLOR
                        text_col = CORRECT_COLOR
                    else:
                        bg = (50, 25, 25)
                        border = (100, 40, 40)
                        text_col = (120, 60, 60)
                else:
                    bg = BTN_COLOR
                    border = (70, 85, 120)
                    text_col = TEXT_PRIMARY

                pygame.draw.rect(self.screen, bg, rect, border_radius=6)
                pygame.draw.rect(self.screen, border, rect, width=1, border_radius=6)
                self._text(letter, "tiny", text_col, rect.center)

    #Score panel
    def draw_score_panel(self, summary: dict, wrong_count: int, max_wrong: int):
        """
        Draw the left-side score/stats panel.

        Args:
            summary (dict): Output of ScoreTracker.summary().
            wrong_count (int): Wrong guesses this round.
            max_wrong (int): Max wrong guesses allowed.
        """
        panel = pygame.Rect(20, 80, 220, 340)
        self._panel(panel)

        labels = [
            ("SCORE",       f"{summary['total_score']:,}",  ACCENT),
            ("WINS",        str(summary["wins"]),            CORRECT_COLOR),
            ("LOSSES",      str(summary["losses"]),          WRONG_COLOR),
            ("STREAK",      f"{summary['streak']} 🔥",       ACCENT),
            ("BEST STREAK", str(summary["best_streak"]),     TEXT_SECONDARY),
            ("WRONG",       f"{wrong_count} / {max_wrong}",  WRONG_COLOR),
        ]

        for i, (label, value, color) in enumerate(labels):
            y = 100 + i * 50
            self._text(label, "tiny", TEXT_SECONDARY, (130, y))
            self._text(value, "medium", color, (130, y + 20))

    #Generic button

    def draw_button(self, rect: pygame.Rect, label: str,
                    hovered: bool = False) -> pygame.Rect:
        """
        Draw a single rectangular button and return its Rect.

        Args:
            rect (pygame.Rect): Position and size of the button.
            label (str): Text displayed inside the button.
            hovered (bool): Whether the mouse is over this button.

        Returns:
            pygame.Rect: The same rect (for hit-testing by caller).
        """
        bg = BTN_HOVER if hovered else BTN_COLOR
        pygame.draw.rect(self.screen, bg, rect, border_radius=10)
        pygame.draw.rect(self.screen, BTN_BORDER, rect, width=2, border_radius=10)
        self._text(label, "small", TEXT_PRIMARY, rect.center)
        return rect

    #Menu screen
    def draw_menu(self, category_names: list, hovered_idx: int,
                  summary: dict):
        """
        Draw the main menu / category selection screen.

        Args:
            category_names (list[str]): Available category names.
            hovered_idx (int): Index of the currently hovered button (-1 = none).
            summary (dict): Score summary for the top-right panel.
        """
        self.draw_background()

        # title
        self._text("H A N G M A N", "title", ACCENT, (self.W // 2, 70))
        self._text("Choose a category to begin", "small", TEXT_SECONDARY,
                   (self.W // 2, 120))

        # category buttons
        btn_w, btn_h = 280, 52
        gap = 16
        total_h = len(category_names) * (btn_h + gap) - gap
        start_y = self.H // 2 - total_h // 2 + 20

        rects = []
        for i, name in enumerate(category_names):
            x = self.W // 2 - btn_w // 2
            y = start_y + i * (btn_h + gap)
            r = pygame.Rect(x, y, btn_w, btn_h)
            self.draw_button(r, name, hovered=(hovered_idx == i))
            rects.append(r)

        # stats panel (top-left)
        if summary["rounds_played"] > 0:
            panel = pygame.Rect(30, 30, 200, 180)
            self._panel(panel)
            self._text("SESSION STATS", "tiny", TEXT_SECONDARY, (130, 55))
            self._text(f"Score: {summary['total_score']:,}", "small", ACCENT, (130, 85))
            self._text(f"W {summary['wins']}  /  L {summary['losses']}",
                       "small", TEXT_PRIMARY, (130, 115))
            self._text(f"Best streak: {summary['best_streak']}",
                       "tiny", TEXT_SECONDARY, (130, 145))
            rate = summary["win_rate"] * 100
            self._text(f"Win rate: {rate:.0f}%", "tiny", TEXT_SECONDARY, (130, 165))

        return rects

    #Game screen

    def draw_game(self, logic, category: str, summary: dict):
        """
        Draw the main gameplay screen.

        Args:
            logic (HangmanLogic): Current round's logic object.
            category (str): Name of the active category.
            summary (dict): ScoreTracker.summary() output.
        """
        self.draw_background()

        # divider line between gallows area and right panel
        pygame.draw.line(self.screen, PANEL_COLOR,
                         (self.W // 2 - 30, 20), (self.W // 2 - 30, self.H - 20), 1)

        self.draw_gallows(logic.wrong_count)
        self.draw_word(logic.get_display_word(), category)
        self.draw_keyboard(logic.guessed_letters, logic.word)
        self.draw_score_panel(summary, logic.wrong_count, logic.MAX_WRONG)

        # remaining guesses label
        remaining = logic.remaining_guesses()
        color = CORRECT_COLOR if remaining > 3 else (ACCENT if remaining > 1 else WRONG_COLOR)
        self._text(f"{remaining} guess{'es' if remaining != 1 else ''} remaining",
                   "small", color, (self.W // 2 + 60, self.H - 30))

    #Result overlay
    def draw_result_overlay(self, won: bool, word: str,
                            points_earned: int, mouse_pos):
        """
        Draw a semi-transparent overlay showing the round result.

        Args:
            won (bool): True for win, False for loss.
            word (str): The secret word (revealed).
            points_earned (int): Points awarded this round.
            mouse_pos (tuple): Current mouse position for button hover.
        """
        # dim overlay
        overlay = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        # result panel
        panel = pygame.Rect(self.W // 2 - 220, self.H // 2 - 160, 440, 320)
        self._panel(panel, radius=20)

        if won:
            self._text("🎉 YOU WON!", "large", CORRECT_COLOR,
                       (self.W // 2, self.H // 2 - 110))
            self._text(f"+{points_earned} points", "medium", ACCENT,
                       (self.W // 2, self.H // 2 - 65))
        else:
            self._text("💀 GAME OVER", "large", WRONG_COLOR,
                       (self.W // 2, self.H // 2 - 110))
            self._text("Better luck next time!", "small", TEXT_SECONDARY,
                       (self.W // 2, self.H // 2 - 65))

        self._text(f"The word was:  {word}", "medium", TEXT_PRIMARY,
                   (self.W // 2, self.H // 2 - 20))

        # buttons
        btn_w, btn_h = 180, 48
        play_rect  = pygame.Rect(self.W // 2 - btn_w - 16, self.H // 2 + 60, btn_w, btn_h)
        menu_rect  = pygame.Rect(self.W // 2 + 16,          self.H // 2 + 60, btn_w, btn_h)

        play_hov = play_rect.collidepoint(mouse_pos)
        menu_hov = menu_rect.collidepoint(mouse_pos)

        self.draw_button(play_rect, "Play Again", hovered=play_hov)
        self.draw_button(menu_rect, "Main Menu",  hovered=menu_hov)

        return play_rect, menu_rect