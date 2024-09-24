from src.states.BaseState import BaseState
import pygame, sys
from src.constants import *
from src.Dependency import *

class StartState(BaseState):
    def __init__(self):
        super(StartState, self).__init__()
        #start = 1,       ranking = 2
        self.option = 1

    def Exit(self):
        pass

    def Enter(self, params):
        self.high_scores = params['high_scores']

    def render(self, screen):
        # title
        t_title = gFonts['large'].render("BREAKOUT", False, (255, 255, 255))
        rect = t_title.get_rect(center=(WIDTH / 2, HEIGHT / 3))
        screen.blit(t_title, rect)

        t_start_color = (133, 113, 207)
        t_highscore_color = (133, 113, 207)

        if self.option == 1:
            t_start_color = (255, 255, 255)

        if self.option == 2:
            t_highscore_color = (255, 255, 255)

        t_start = gFonts['medium'].render("START", False, t_start_color)
        rect = t_start.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))
        screen.blit(t_start, rect)
        t_highscore = gFonts['medium'].render("HIGH SCORES", False, t_highscore_color)
        rect = t_highscore.get_rect(center=(WIDTH/2, HEIGHT/2 + 120))
        screen.blit(t_highscore, rect)

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    if self.option==1:
                        self.option=2
                    else:
                        self.option=1
                    gSounds['paddle-hit'].play()

                if event.key == pygame.K_RETURN:
                    gSounds['confirm'].play()

                    if self.option == 1:
                        g_state_manager.Change('paddle-select', {
                            'high_scores': self.high_scores
                        })
                    else:
                        g_state_manager.Change('high-scores', {
                            'high_scores': self.high_scores
                        })
                
                if event.key == pygame.K_1:
                    print("Debug: Warping to Level 1")
                    self.start_game_at_level(1)
                elif event.key == pygame.K_2:
                    print("Debug: Warping to Level 11")
                    self.start_game_at_level(11)
                elif event.key == pygame.K_3:
                    print("Debug: Warping to Level 21")
                    self.start_game_at_level(21)
                elif event.key == pygame.K_4:
                    print("Debug: Warping to Level 31")
                    self.start_game_at_level(31)
                elif event.key == pygame.K_5:
                    print("Debug: Warping to Level 41")
                    self.start_game_at_level(41)
                elif event.key == pygame.K_6:
                    print("Debug: Warping to Level 51")
                    self.start_game_at_level(51)


    def start_game_at_level(self, level):
        """Warp the player to a specific level for testing."""
        gSounds['confirm'].play()
        g_state_manager.Change('serve', {
            'level': level,
            'paddle': Paddle(),
            'bricks': LevelMaker.CreateMap(level),
            'health': 3,
            'score': 0,
            'high_scores': self.high_scores,
            'recover_points': 5000
        })