#This is the main code for Hangman.
#This code initialzied pygame, creates the game object, and runds the main game loop.

import pygame
import sys
from game import Game 

def main():
    #Initialize pygame and run the main game loop.
    pygame.init()

    #Screen dimensions
    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 620

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Hangman")

    clock = pygame.time.Clock()
    game = Game(screen)

    #Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_event(event)

        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()