from src.states.BaseState import BaseState
from src.LevelMaker import LevelMaker
import src.CommonRender as CommonRender
from src.constants import *
from src.resources import *
from src.Dependency import *

class VictoryState(BaseState):
    def __init__(self):
        super(VictoryState, self).__init__()

    def Exit(self):
        pass

    def Enter(self, params):
        self.level = params['level']
        self.paddle = params['paddle']
        self.health = params['health']
        self.score = params['score']
        self.ball = params['ball']

        # added
        self.high_scores = params['high_scores']
        self.recover_point = params['recover_points']

        # Clear any active power-ups from the previous level, including lasers
        if 'play_state' in params and hasattr(params['play_state'], 'clear_powerups'):
            print("Log: Current Level Completed! Clearing all active power-ups and lasers...")
            params['play_state'].clear_powerups()

    def update(self, dt, events):
        self.paddle.update(dt)

        # put ball above the paddle
        self.ball.rect.x = self.paddle.rect.x + (self.paddle.width/2) - 12
        self.ball.rect.y = self.paddle.rect.y - 24

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    g_state_manager.Change('serve', {
                        'paddle': Paddle(self.paddle.skin),
                        'level': self.level + 1,
                        'bricks': LevelMaker.CreateMap(self.level + 1),
                        'health': self.health,
                        'score': self.score,
                        'high_scores': self.high_scores,
                        'recover_points': self.recover_point,
                        'ball': self.ball
                    })


    def render(self, screen):
        self.paddle.render(screen)
        self.ball.render(screen)

        CommonRender.RenderHealth(screen, self.health)
        CommonRender.RenderScore(screen, self.score)

        t_level = gFonts['large'].render("Level" + str(self.level)+" Complete", False, (255, 255, 255))
        rect = t_level.get_rect(center=(WIDTH / 2, HEIGHT / 4))
        screen.blit(t_level, rect)

        t_serve = gFonts['medium'].render("Press Enter to Serve", False, (255, 255, 255))
        rect = t_serve.get_rect(center=(WIDTH / 2, HEIGHT / 3))
        screen.blit(t_serve, rect)
