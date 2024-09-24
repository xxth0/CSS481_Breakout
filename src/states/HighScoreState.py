from src.states.BaseState import BaseState
from src.constants import *
from src.resources import *
from src.Dependency import *

import pygame, sys

class HighScoreState(BaseState):
    def __init__(self):
        super(HighScoreState, self).__init__()

    def Exit(self):
        pass

    def Enter(self, params):
        self.high_scores = params['high_scores']

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gSounds['wall-hit'].play()
                    g_state_manager.Change('start', {
                        'high_scores': self.high_scores
                    })

    def render(self, screen):
        """Render the high score screen."""
        t_high_score = gFonts['large'].render("High Scores", False, (255, 255, 255))
        rect = t_high_score.get_rect(center=(WIDTH / 2, 60))
        screen.blit(t_high_score, rect)

        for i in range(10):
            name = self.high_scores[i]['name']
            score = self.high_scores[i]['score']
            level = self.high_scores[i]['level']  # Retrieve the player's level

            # Render the name, score, and level text
            t_name = gFonts['medium'].render(f"{i + 1}. {name}", False, (255, 255, 255))
            t_score = gFonts['medium'].render(f"{score}", False, (255, 255, 255))
            t_level = gFonts['medium'].render(f"Level {level}", False, (255, 255, 255))

            # Center-align the name
            name_rect = t_name.get_rect(centerx=WIDTH / 2 - 200, top=180 + i * 39)
            screen.blit(t_name, name_rect)

            # Center-align the score just to the right of the name
            score_rect = t_score.get_rect(centerx=WIDTH / 2, top=180 + i * 39)
            screen.blit(t_score, score_rect)

            # Center-align the level to the right of the score
            level_rect = t_level.get_rect(centerx=WIDTH / 2 + 200, top=180 + i * 39)
            screen.blit(t_level, level_rect)



        # Display escape message at the bottom
        t_escape_message = gFonts['small'].render("Press Escape to return to the main menu", False, (255, 255, 255))
        rect = t_escape_message.get_rect(center=(WIDTH / 2, HEIGHT - 54))
        screen.blit(t_escape_message, rect)