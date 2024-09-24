import pygame
from src.Util import SpriteManager
from src.StateMachine import StateMachine

g_state_manager = StateMachine()

sprite_collection = SpriteManager().spriteCollection

 # Powerups
powerup_image_list = [sprite_collection["powerups_widepaddle"].image, sprite_collection["powerups_catchnet"].image,
                     sprite_collection["powerups_laser"].image, sprite_collection["powerups_heart"].image,
                     sprite_collection["powerups_ghostball"].image]

 # Ball
ball_image_list = [sprite_collection["blue_ball"].image, sprite_collection["green_ball"].image,
                                sprite_collection["purple_ball"].image, sprite_collection["pink_ball"].image,
                                sprite_collection["ghost_ball"].image]
# Paddle
s_paddle_image_list = [sprite_collection["p_blue_1"].image, sprite_collection["p_green_1"].image,
                     sprite_collection["p_purple_1"].image, sprite_collection["p_pink_1"].image]

paddle_image_list = [sprite_collection["p_blue_2"].image, sprite_collection["p_green_2"].image,
                     sprite_collection["p_purple_2"].image, sprite_collection["p_pink_2"].image]

widened_paddle_image_list = [sprite_collection["p_blue_3"].image, sprite_collection["p_green_3"].image,
                             sprite_collection["p_purple_3"].image, sprite_collection["p_pink_3"].image]

gFonts = {
        'small': pygame.font.Font('./fonts/font.ttf', 24),
        'medium': pygame.font.Font('./fonts/font.ttf', 48),
        'large': pygame.font.Font('./fonts/font.ttf', 96)
}

gSounds = {
    'confirm': pygame.mixer.Sound('sounds/confirm.wav'),
    'paddle-hit': pygame.mixer.Sound('sounds/paddle_hit.wav'),
    'pause': pygame.mixer.Sound('sounds/pause.wav'),
    'recover': pygame.mixer.Sound('sounds/recover.wav'),
    'victory': pygame.mixer.Sound('sounds/victory.wav'),
    'hurt': pygame.mixer.Sound('sounds/hurt.wav'),
    'select': pygame.mixer.Sound('sounds/select.wav'),
    'no-select': pygame.mixer.Sound('sounds/no-select.wav'),
    'wall-hit': pygame.mixer.Sound('sounds/wall_hit.wav'),
    'high-score': pygame.mixer.Sound('sounds/high_score.wav'),
    'brick-hit1': pygame.mixer.Sound('sounds/brick-hit-1.wav'),
    'brick-hit2': pygame.mixer.Sound('sounds/brick-hit-2.wav'),
    'item': pygame.mixer.Sound('sounds/item.wav'),
    'laser': pygame.mixer.Sound('sounds/laser.wav')
}

brick_image_list = [sprite_collection["b_blue_1"].image, sprite_collection["b_blue_2"].image,
                   sprite_collection["b_blue_3"].image, sprite_collection["b_blue_4"].image,
                   sprite_collection["b_green_1"].image, sprite_collection["b_green_2"].image,
                   sprite_collection["b_green_3"].image, sprite_collection["b_green_4"].image,
                   sprite_collection["b_purple_1"].image, sprite_collection["b_purple_2"].image,
                   sprite_collection["b_purple_3"].image, sprite_collection["b_purple_4"].image,
                   sprite_collection["b_pink_1"].image, sprite_collection["b_pink_2"].image,
                   sprite_collection["b_pink_3"].image, sprite_collection["b_pink_4"].image,
                   sprite_collection["b_gold_1"].image, sprite_collection["b_gold_2"].image,
                   sprite_collection["b_gold_3"].image, sprite_collection["b_gold_4"].image,
                   sprite_collection["b_gray"].image]


def get_brick_image(color, tier):
    """Return the correct brick image based on color and tier."""
    # Map color ranges from 1-5 to the appropriate sprite prefix
    color_map = {
        1: "blue",
        2: "green",
        3: "purple",
        4: "pink",
        5: "gold"
    }
    
    # Get color prefix from the map
    color_prefix = color_map.get(color, "blue")  # Default to blue if color is out of range
    
    # Build the sprite key for the correct tier
    sprite_key = f"b_{color_prefix}_{tier}"
    
    # Fetch the correct image from the sprite collection or fallback to a gray brick
    return sprite_collection.get(sprite_key, sprite_collection["b_gray"]).image
