import pygame, math, os
from pygame import mixer
from src.constants import *


pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()

music_channel = mixer.Channel(0)
music_channel.set_volume(0.2)

from src.Dependency import *

# Cleaned up all messy code

class GameMain:
    def __init__(self):
        self.max_frame_rate = 60
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.bg_image = pygame.image.load("./graphics/background_menu_dark.png")
        self.bg_image_light = pygame.image.load("./graphics/background_menu_light.png")
        self.bg_image_dark = pygame.image.load("./graphics/background_menu_dark.png")

        self.lightmode = False

        self.scroll = 0
        self.scroll_bg = False

        self.bg_music = pygame.mixer.Sound('sounds/music.wav')

        # Set music volume to 30%
        self.bg_music.set_volume(0.3)
        self.music_muted = False  # Music is on by default
        self.bg_music.play(-1)  # Play music in a loop by default

        g_state_manager.SetScreen(self.screen)

        states = {
            'start': StartState(),
            'play': PlayState(),
            'serve': ServeState(),
            'game-over': GameOverState(),
            'victory': VictoryState(),
            'high-scores': HighScoreState(),
            'enter-high-score': EnterHighScoreState(),
            'paddle-select': PaddleSelectState()
        }
        g_state_manager.SetStates(states)

    def LoadHighScores(self):
        # Check if the file exists, and if not, initialize it with default values
        if not os.path.exists(RANK_FILE_NAME):
            with open(RANK_FILE_NAME, "w") as fp:
                for i in range(10, 0, -1):
                    # Initialize default scores with a level
                    scores = "AAA\n" + str(i*10) + "\n" + "Level 1\n"
                    fp.write(scores)
            fp.close()

        # Open the high scores file
        file = open(RANK_FILE_NAME, "r+")
        all_lines = file.readlines()
        file.close()

        # Prepare to store the scores
        scores = []

        # Flip between name, score, and level
        for i in range(0, len(all_lines), 3):  # Each entry takes 3 lines (name, score, level)
            name = all_lines[i].strip()  # Name is on the first line
            score = int(all_lines[i+1].strip())  # Score is on the second line
        
            # Check if the level line exists and is correctly formatted
            try:
                level_line = all_lines[i+2].strip()
                level = int(level_line.split(' ')[1])  # Level is on the third line after "Level"
            except (IndexError, ValueError):
                # If there is an error reading the level, set it to a default value (e.g., 1)
                level = 1

            # Append the score with name, score, and level to the list
            scores.append({
                'name': name,
                'score': score,
                'level': level  # Include the level in the scores
            })

        return scores


    def RenderBackground(self):
        # Get the current state from the state manager
        current_state_name = type(g_state_manager.current).__name__

        # Scale the background image to fit the screen
        scaled_bg = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))

        # Scroll background if enabled
        if self.scroll_bg:
            i = 0
            while i < self.num_dup_images:
                self.screen.blit(scaled_bg,
                                 (scaled_bg.get_width() * i + self.scroll, 0))  # append same images to the back
                i += 1
            self.scroll -= 6
            if abs(self.scroll) > scaled_bg.get_width():
                self.scroll = 0
        else:
            # Render the scaled background to fill the screen
            self.screen.blit(scaled_bg, (0, 0))



    def PlayGame(self):
        current_state = 'play'
        self.bg_music.play(-1)
        clock = pygame.time.Clock()
        g_state_manager.Change('start', {
            'high_scores': self.LoadHighScores(),
        })

        while True:
            pygame.display.set_caption("breakout game running with {:d} FPS".format(int(clock.get_fps())))
            dt = clock.tick(self.max_frame_rate) / 1000.0

            #input
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:  # M key pressed for mute/unmute
                        if self.music_muted:
                            self.bg_music.set_volume(0.3)
                            self.music_muted = False
                            print("Log: Music unmuted!")
                        else:
                            self.bg_music.set_volume(0)
                            self.music_muted = True
                            print("Log: Music muted!")

                    if event.key == pygame.K_n:   # N key pressed for light/dark mode
                        if self.lightmode:
                           self.bg_image = self.bg_image_dark
                           self.lightmode = False
                           print("Log: Switched to dark mode!")
                        else:
                            self.bg_image = self.bg_image_light
                            self.lightmode = True
                            print("Log: Switched to light mode!")

            #update
            g_state_manager.update(dt, events)

            #bg render
            self.RenderBackground()

            #render
            g_state_manager.render()

            #screen update
            pygame.display.update()


if __name__ == '__main__':
    main = GameMain()

    main.PlayGame()
