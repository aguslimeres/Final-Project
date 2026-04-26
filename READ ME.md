Hangman Final Project
Course: CMSI-1010-02
Author: Agustina Limeres
Spring 2026

How to Run the Game:
Step 1 — Make sure pygame is installed. 
pip3 install pygame

Step 2 — Run the game (always run hangman.py, not any other files).
python3 hangman.py

How to Play 
1. Category Screen

When the game launches, you'll see the Category Selection screen. Click one of the five buttons to pick a 
word categroyr and start a round:

 Category    |   Example Words
 ——————————————————————————————————————————
 Animals     |   ELEPHANT, POLAR BEAR
 Countries   |   ARGENTINA, ICELAND
 Food        |   GUACAMOLE, CROISSANT
 Sports      |   BADMINTON, TRIATHLON
 Science     |   PHOTOSYNTHESIS, CATALYST

 2. Gameplay Screen
 - The hidden word appears as blank dashes (_) at the center of the screen. 
 - If the word is a two-word phrase, there will be a gap between the two sets of blanks. Spaces are revealed automatically and don't need to be gussed. 
 - Press any letter key (A-Z) on youe keyboard to guess that letter. 
 - If your guess is correct → the letter is revealed in green on the word and highlighted green on the on-screen keybaord. 
 - If your guess is wrong → a body part will be added to the hangman figure, and the letter turns red on the keyboard. 
 - You have a total of 6 wrong guesses before the game is over. The hangman is drawn one pieced at a time: head → body → left arm → right arm → left leg → right leg. 

 3. Result Screen
 After the round ends, a message appears showing one of two things:

 - You Won! or Game over
 - The secret word (always revealed at the end)
 - Points earned this round
 - Two buttons: Play Again (same category) or Main Menu (Choose a new category)

 Controls

 Input                            |   Action
————————————————————————————————————————————————————————————————————
 Letter keys A–Z                  |  Guess a letter
 Mouse click — category button    |  Start a round
 Mouse click — Play Again         |  Replay with same category
 Mouse click — Main Menu          |  Return to category selection
 Window close (✕)                 |  Quit the game

Scoring System

Event                    |     Points
——————————————————————————————————————————————————————————————————
Win                      |     100 × current win streak
Remaining guess bonus    |     +10 per guess left when you win
Loss                     |     0 points, streak resets to 0

Example: You win your 3rd round in a row with 4 guesses still remaining: (100 × 3) + (10 × 4) = ** 340 points **

Your running Sessions Stats(score, wins, losses, best streak, win rate) are shown on the left panel during gameplay and on the menu screen after your first round. Stats rest when you close the game. 

File Overview
The porject is split into 5 giles so that each piece of the game has one clear job. Here's what each one does:

hangman.py — Entry Point
This is the file you run to start the game. It initializes pygame, creates the game window (900 × 620 pixels), and runs the main loop — the loop that runs 60 times per second, handling input, updating state, and drawing to the screen.

***This is the file that should always be run, not any of the other. 

hangman_logic.py — Game logic
The file contains the HangmanLogic class, which tracks everything about a single round:

- The secret word
- Which letters have been gussed so far
- How many wrong guesses have been made
- Whether the round has been won or lost

It has no pygame code at all, it's just Python logic. Key methods:

- guess(letter) —— processes a letter guess, returns True if correct
- get_display_word() —— returns the word as a list like ['H', '_', '_', 'S', '_'], with spaces that are auto-revealed for two-word phrases
- is_won() / is_lost() / is_over() —— check the round status
- remaining_guesses() —— how many wrong guesses are left

words.py —— Word Bank
This file has rhe WordBank class and all the word lists. Words are organized into 5 categories (Animals, Countries, Food, Sports, Science, LMU), each with 15+ words including some two-word phrases like POLAR BEAR and PALM TREE.

Key methods:

- get_random_word(category) —— picks a random word from the chosen category
- get_category_names() —— returns the list of availabe category names

score_tracker.py —— Score Tracking 
This file contains the ScoreTracker class, which keeps a running tally across all rounds played in a session:

- Wins, losses, current streak, best streak, and total score
- Win points are calculated with a streak multiplier and a remaining-guess bonus
- Losing resets the streak to 0

Key methods:

- record_win(remaining_guesses) — logs a win and returns points earned
- record_loss() — logs a loss and resets the streak
- summary() — returns a dictionary of all stats for display

render.py — Drawing
This file contains the Renderer class, which handles all pygame drawing. It is the only file that uses pygame, keeping all visual code in one place and separate from the logic.

Key methods:

- draw_menu(...) — draws the category selection screen
- draw_game(...) — draws the main gameplay screen (gallows, word, keyboard, score panel)
- draw_gallows(wrong_count) — draws the gallows and reveals the figure part by part
- draw_word(display_word, category) — draws the letter blanks; spaces show as gaps between words
- draw_keyboard(guessed_letters, word) — draws the A–Z keyboard with color-coded letter states
- draw_result_overlay(...) — draws the win/loss popup with Play Again and Main Menu buttons

game.py — Game Controller
This file contains the Game class, which connects all the other pieces together. It works as a state machine with three states:

"menu"  →  "playing"  →  "result"  →  back to "menu" or "playing"

- In "menu" state: waits for the player to click a category
- In "playing" state: passes keyboard input to HangmanLogic and checks for win/loss
- In "result" state: shows the overlay and waits for Play Again or Main Menu

Each frame, hangman.py calls game.handle_event(), game.update(), and game.draw() — and Game delegates those calls to the right objects.