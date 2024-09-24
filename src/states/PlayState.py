import random, pygame, sys
from src.states.BaseState import BaseState
from src.constants import *
from src.Dependency import *
import src.CommonRender as CommonRender
from src.Powerups import PowerUp  # Ensure this import is at the top of PlayState.py


class PlayState(BaseState):
    def __init__(self):
        super(PlayState, self).__init__()
        self.paused = False

        # Related Power-ups params tracking

        self.powerup_spawn_timer = random.uniform(10, 20)  # Random time interval between 10 to 20 seconds

        self.active_powerups = []  # Add a list to store active power-ups
        self.balls = []  # List to hold multiple balls

        self.paddle_widen_active = False
        self.paddle_widen_timer = 0

        self.ghost_ball_active = False  # Add this initialization
        self.ghost_ball_timer = 0       # Initialize the ghost ball timer

        self.catch_net_active = False  # Add this line to initialize the catch net state
        self.catch_net_rect = pygame.Rect(0, HEIGHT - 5, WIDTH, 10)  # Position of the catch net (bottom of the screen)

        self.laser_paddle_active = False  # Track if laser paddle is active
        self.laser_paddle_timer = 0       # Timer for laser paddle
        self.lasers = []  # List to hold active lasers
        self.laser_shot_interval = 0.5    # Interval between laser shots (0.2 seconds for faster firing)
        self.time_since_last_shot = 0     # Timer to track time since last shot

        # SUPER BUFF Power-ups
        self.super_buff_active = False  # Track if the super buff is active

    def Enter(self, params):
        self.paddle = params['paddle']
        self.original_paddle_width = self.paddle.width  # Now, we can safely set the original width after paddle is initialized

        self.bricks = params['bricks']
        self.health = params['health']
        self.score = params['score']
        self.high_scores = params['high_scores']
        self.ball = params['ball']
        self.level = params['level']

        self.recover_points = 5000

        self.ball.dx = random.randint(-600, 600)  # -200 200
        self.ball.dy = random.randint(-180, -150)

        self.create_powerup_callback = self.create_powerup

    ## POWER-UPS STUFFS HERE ##

    def create_powerup(self, x, y, power_type="life"):
        """Create a power-up at the specified position."""
        new_powerup = PowerUp(x, y, power_type)
        self.active_powerups.append(new_powerup)

    def create_ball(self, x=None, y=None):
        """Create a new ball at the specified position or the current ball's position."""
        new_ball = Ball(skin=1)  # Assuming Ball is defined, skin can be adjusted

        if x is None or y is None:
            # Spawn near the current ball's position
            new_ball.x = self.ball.x
            new_ball.y = self.ball.y
        else:
            new_ball.x = x
            new_ball.y = y

        # Randomize the velocity for variety
        new_ball.dx = random.choice([-200, 200])
        new_ball.dy = random.choice([-150, -200])

        # Add the new ball to the list of active balls
        self.balls.append(new_ball)

    def widen_paddle(self, multiplier, duration):
        """Widen the paddle by a multiplier for a specified duration."""
        if self.paddle_widen_active:
            # Refresh the timer if the power-up is already active
            self.paddle_widen_timer = duration
            print("Log: Paddle widen timer is refreshed!")
        if not self.paddle_widen_active:  # Only widen if it's not already active
            self.paddle.width *= multiplier
            self.paddle.widen(multiplier)
            self.paddle.rect.width = self.paddle.width  # Adjust the rect width
            self.paddle_widen_timer = duration  # Set timer
            self.paddle_widen_active = True

    def enable_ghost_ball(self, duration):
        """Enable the ghost ball effect for a limited time."""
        self.ghost_ball_active = True
        self.ghost_ball_timer = duration
        if self.ghost_ball_active:
            print("Log: Ghost ball timer is refreshed!")

        # Enable ghost mode for all balls
        for ball in self.balls:
            ball.set_ghost_mode(True)

    def disable_ghost_ball(self):
        """Disable the ghost ball effect, returning the ball to normal."""
        self.ghost_ball_active = False
        for ball in self.balls:
            ball.set_ghost_mode(False)

            # Ensure the ball keeps moving vertically after ghost mode ends
            if ball.dy == 0:  # If the ball's vertical velocity is zero, restore it
                ball.dy = -200  # Reset to a reasonable default value

    def enable_catch_net(self, duration):
        """Enable the catch net for a limited time."""
        self.catch_net_active = True
        self.catch_net_timer = duration
        print("Log: Catch net is activated!")

    def disable_catch_net(self):
        """Disable the catch net after the timer runs out."""
        self.catch_net_active = False
        print("Log: Catch net deactivated.")

    def enable_laser_paddle(self, duration):
        """Enable laser paddle mode for a limited time."""
        self.laser_paddle_active = True
        self.laser_paddle_timer = duration
        print("Log: Laser paddle is activated!")

    def disable_laser_paddle(self):
        """Disable laser paddle mode."""
        self.laser_paddle_active = False
        self.disable_super_buff()
        print("Log: Laser paddle deactivated.")

    def disable_super_buff(self):
        """Deactivate the super buff."""
        self.super_buff_active = False
        print("Log: Super Buff deactivated.")


    def update(self,  dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                    gSounds['pause'].play()
                    #music_channel.play(sounds_list['pause'])

                # **Debugging commands for power-up spawning**
                if event.key == pygame.K_o:  # "O" key spawns paddle widen power-up
                    print("Debug command: Spawn a power-up Paddle Widen!")
                    self.spawn_debug_powerup("paddle_widen")
                if event.key == pygame.K_p:  # "P" key spawns life power-up
                    self.spawn_debug_powerup("life")
                    print("Debug command: Spawn a power-up Extra Life!")
                if event.key == pygame.K_i:  # "I" key spawns ghost ball power-up
                    self.spawn_debug_powerup("ghost_ball")
                    print("Debug command: Spawn a power-up Ghost Ball!")
                if event.key == pygame.K_u:  # "U" key spawns catch net power-up
                    self.spawn_debug_powerup("catch_net")
                    print("Debug command: Spawn a power-up Catch Net!")
                if event.key == pygame.K_l:  # "L" key spawns catch net power-up
                    self.spawn_debug_powerup("laser_paddle")
                    print("Debug command: Spawn a power-up Laser Paddle!")

        if self.paused:
            return

        self.paddle.update(dt)

        # Update power-up spawn timer (This can randomly spawn anywhere on screen even if player didn't break blocks')
        self.powerup_spawn_timer -= dt
        if self.powerup_spawn_timer <= 0:
            self.spawn_random_powerup()
            self.powerup_spawn_timer = random.uniform(10, 20)  # Reset the timer for the next power-up

        ## Paddle widen power up
        if self.paddle_widen_active:
            self.paddle_widen_timer -= dt
            if self.paddle_widen_timer <= 0:
                self.paddle.restore()
                self.paddle.width /= 1.5
                self.paddle.rect.width = self.paddle.width  # Adjust the rect width
                self.paddle_widen_active = False
                self.disable_super_buff()
                print("Log: Paddle width reverted to original size.")

        ## Ghost ball power up
        if self.ghost_ball_active:   
            self.ghost_ball_timer -= dt
            if self.ghost_ball_timer <= 0:
                self.disable_ghost_ball()
                print("Log: Ball becomes tangible again.")

        # Check if the catch net is active and update the timer
        if self.catch_net_active:
            self.catch_net_timer -= dt
            if self.catch_net_timer <= 0:
                self.disable_catch_net()

        ## Laser paddle power up
    # If laser paddle is active, shoot lasers at regular intervals
        if self.laser_paddle_active and not self.super_buff_active:
            self.laser_paddle_timer -= dt
            self.time_since_last_shot += dt

            # Shoot a laser if the interval has passed
            if self.time_since_last_shot >= self.laser_shot_interval:
                self.shoot_laser()
                self.time_since_last_shot = 0  # Reset the timer after shooting

            if self.laser_paddle_timer <= 0:
                self.disable_laser_paddle()

        # Update lasers
        lasers_to_remove = []
        for laser in self.lasers:
            laser.update(dt)

            # Remove lasers that are off-screen or hit bricks
            if laser.rect.y <= 0:
                self.lasers.remove(laser)

            # Check for collisions with bricks
            for brick in self.bricks:
                if brick.alive and laser.rect.colliderect(brick.rect):
                    brick.Hit(self.create_powerup_callback)  # Destroy the brick
                    lasers_to_remove.append(laser)
                    self.score = self.score + ((brick.tier + brick.color))

                
                    # **Check for victory after destroying the brick**
                    if self.CheckVictory():
                        gSounds['victory'].play()

                        # Clear all active power-ups and buffs before transitioning to the next level
                        self.clear_powerups()

                        g_state_manager.Change('victory', {
                            'level': self.level,
                            'paddle': self.paddle,
                            'health': self.health,
                            'score': self.score,
                            'high_scores': self.high_scores,
                            'ball': self.ball,
                            'recover_points': self.recover_points
                        })
                    break  # Exit brick loop after laser hits

        # Remove the lasers that were marked for removal
        for laser in lasers_to_remove:
            if laser in self.lasers:  # Check to ensure the laser is still in the list
                self.lasers.remove(laser)

        # Activate SUPER BUFF!!
        # Check if both paddle_widen and laser_paddle are active
        if self.paddle_widen_active and self.laser_paddle_active and not self.super_buff_active:
            print("Log: Activating Super Buff...")
            self.enable_super_buff()

        # Update lasers, including shooting three lasers if super buff is active
        if self.laser_paddle_active:
            self.laser_paddle_timer -= dt
            self.time_since_last_shot += dt

            if self.time_since_last_shot >= self.laser_shot_interval:
                if self.super_buff_active:
                    self.shoot_triple_laser()  # Shoot three lasers if super buff is active
                else:
                    self.shoot_laser()  # Shoot single laser if super buff is not active
                self.time_since_last_shot = 0  # Reset the timer after shooting

            if self.laser_paddle_timer <= 0:
                self.disable_laser_paddle()

        self.ball.update(dt)

        if self.ball.Collides(self.paddle):
            # raise ball above paddle
            ####can be fixed to make it natural####
            self.ball.rect.y = self.paddle.rect.y - 24
            self.ball.dy = -abs(self.ball.dy)

            # half left hit while moving left (side attack) the more side, the faster
            if self.ball.rect.x + self.ball.rect.width < self.paddle.rect.x + (self.paddle.width / 2) and self.paddle.dx < 0:
                self.ball.dx = -150 + -(8 * (self.paddle.rect.x + self.paddle.width / 2 - self.ball.rect.x))
            # right paddle and moving right (side attack)
            elif self.ball.rect.x > self.paddle.rect.x + (self.paddle.width / 2) and self.paddle.dx > 0:
                self.ball.dx = 150 + (8 * abs(self.paddle.rect.x + self.paddle.width / 2 - self.ball.rect.x))
            gSounds['paddle-hit'].play()


        # Update and render bricks, check for collisions, and power-ups
        # This part is when ghost mode activated, ignores the brick toughness
        if self.ghost_ball_active:
            for brick in self.bricks:
                if brick.alive and self.ball.Collides(brick):
                    self.score = self.score + ((brick.tier + brick.color))
                    brick.Hit(self.create_powerup_callback)  # Pass PlayState object (self) to trigger power-ups

                    if self.score > self.recover_points:
                        self.health = min(3, self.health + 1)
                        self.recover_points = min(100000, self.recover_points * 2)
                        gSounds['recover'].play()

                    if self.CheckVictory():
                        gSounds['victory'].play()

                        # Clear all active power-ups and buffs before transitioning to the next level
                        self.clear_powerups()

                        g_state_manager.Change('victory', {
                            'level': self.level,
                            'paddle': self.paddle,
                            'health': self.health,
                            'score': self.score,
                            'high_scores': self.high_scores,
                            'ball': self.ball,
                            'recover_points': self.recover_points,
                            'play_state': self  # Pass the current PlayState instance
                        })

        else:
            for k, brick in enumerate(self.bricks):
                if brick.alive and self.ball.Collides(brick):
                    self.score = self.score + ((brick.tier + brick.color))
                    brick.Hit(self.create_powerup_callback)

                    if self.score > self.recover_points:
                        self.health = min(3, self.health + 1)
                        self.recover_points = min(100000, self.recover_points * 2)

                        gSounds['recover'].play()
                        #music_channel.play(sounds_list['recover'])

                    if self.CheckVictory():
                        gSounds['victory'].play()

                        # Clear all active power-ups and buffs before transitioning to the next level
                        self.clear_powerups()

                        g_state_manager.Change('victory', {
                            'level':self.level,
                            'paddle':self.paddle,
                            'health':self.health,
                            'score':self.score,
                            'high_scores':self.high_scores,
                            'ball':self.ball,
                            'recover_points':self.recover_points,
                            'play_state': self  # Pass the current PlayState instance
                        })

                    # hit brick from left while moving right -> x flip
                    if self.ball.rect.x + 6 < brick.rect.x and self.ball.dx > 0:
                        self.ball.dx = -self.ball.dx
                        self.ball.rect.x = brick.rect.x - 24

                    # hit brick from right while moving left -> x flip
                    elif self.ball.rect.x + 18 > brick.rect.x + brick.width and self.ball.dx < 0:
                        self.ball.dx = -self.ball.dx
                        self.ball.rect.x = brick.rect.x + 96

                    # hit from above -> y flip
                    elif self.ball.rect.y < brick.rect.y:
                        self.ball.dy = -self.ball.dy
                        self.ball.rect.y = brick.rect.y - 24

                    # hit from bottom -> y flip
                    else:
                        self.ball.dy = -self.ball.dy
                        self.ball.rect.y = brick.rect.y + 48

                    # whenever hit, speed is slightly increase, maximum is 450
                    if abs(self.ball.dy) < 450:
                        self.ball.dy = self.ball.dy * 1.02

                    break

        # Check if the ball falls below the screen
        if self.ball.rect.y >= HEIGHT - self.catch_net_rect.height * 2:
            # Check if the catch net is active
            if self.catch_net_active:
                # Deflect the ball upwards when it hits the catch net
                self.ball.rect.y = HEIGHT - self.catch_net_rect.height - 24  # Position the ball just above the net
                self.ball.dy = -abs(self.ball.dy)  # Ensure the ball is moving upwards
                gSounds['paddle-hit'].play()  # Play deflect sound

                # Optionally increase speed slightly, as with other collisions
                if abs(self.ball.dy) < 450:
                    self.ball.dy *= 1.02

            else:
                # No catch net, so reduce health as normal
                self.health -= 1
                gSounds['hurt'].play()

                if self.health == 0:
                    g_state_manager.Change('game-over', {
                        'score': self.score,
                        'high_scores': self.high_scores,
                        'level': self.level,  # Ensure the level is passed here
                    })
                else:
                    g_state_manager.Change('serve', {
                        'level': self.level,
                        'paddle': self.paddle,
                        'ball': self.ball,
                        'bricks': self.bricks,
                        'health': self.health,
                        'score': self.score,
                        'high_scores': self.high_scores,
                        'recover_points': self.recover_points
                    })

        # Update and check for power-ups
        for powerup in self.active_powerups:
            powerup.update(dt)
            if powerup.rect.colliderect(self.paddle.rect):  # Paddle collects power-up
                powerup.activate(self)  # Activate the power-up's effect
                self.active_powerups.remove(powerup)

        self.active_powerups = [pu for pu in self.active_powerups if pu.alive]

    def spawn_debug_powerup(self, power_type):
        """Spawn a specific power-up at the paddle's position for debugging."""
        # Spawn the power-up directly above the paddle
        powerup_x = self.paddle.rect.x + self.paddle.width / 2
        powerup_y = self.paddle.rect.y - 50  # Place it slightly above the paddle
        new_powerup = PowerUp(powerup_x, powerup_y, power_type)
        self.active_powerups.append(new_powerup)
        print(f"Debug: {power_type} power-up spawned at ({powerup_x}, {powerup_y})")

    def spawn_random_powerup(self):
        """Spawn a random power-up somewhere on the screen."""
        powerup_type = random.choice(['paddle_widen', 'ghost_ball', 'laser_paddle'])
        powerup_x = random.randint(0, WIDTH - 32)  # Random x position (ensure it¡¯s within screen bounds)
        powerup_y = random.randint(0, 100)  # Random y position within the top 100px

        new_powerup = PowerUp(powerup_x, powerup_y, powerup_type)
        self.active_powerups.append(new_powerup)
        print(f"Log: Random Power-up spawned: {powerup_type} at ({powerup_x}, {powerup_y})!")

    def clear_powerups(self):
        """Clear all active power-ups and lasers."""
        self.active_powerups = []  # Clear all falling power-ups

        # Reset any active power-up effects
        if self.paddle_widen_active:
            self.paddle.restore()  # Reset paddle size
            self.paddle_widen_active = False

        if self.ghost_ball_active:
            self.disable_ghost_ball()  # Disable ghost ball mode

        if self.catch_net_active:
            self.disable_catch_net()  # Disable the catch net

        if self.laser_paddle_active:
            self.disable_laser_paddle()  # Disable the laser paddle mode

        if self.super_buff_active:
            self.disable_super_buff()   # Disable SUPER BUFF

        # Clear active lasers
        self.lasers.clear()

        print("Log: All active/falling power-ups and lasers cleared!")


    def shoot_laser(self):
        """Shoot a laser from the paddle's position."""
        laser_x = self.paddle.rect.centerx  # Shoot laser from the center of the paddle
        laser_y = self.paddle.rect.y
        new_laser = Laser(laser_x, laser_y)
        self.lasers.append(new_laser)
        gSounds['laser'].play()  # Play laser shoot sound

    def enable_super_buff(self):
        """Activate the super buff that shoots three lasers at once."""
        self.super_buff_active = True
        print("Log: Super Buff activated: Triple lasers!")

    def shoot_triple_laser(self):
        """Shoot three lasers from the paddle's position."""
        # Middle laser
        laser_x_middle = self.paddle.rect.centerx
        laser_y = self.paddle.rect.y

        # Left laser
        laser_x_left = self.paddle.rect.centerx - 60  # Adjust position for left laser

        # Right laser
        laser_x_right = self.paddle.rect.centerx + 60  # Adjust position for right laser

        # Create the three lasers
        middle_laser = Laser(laser_x_middle, laser_y)
        left_laser = Laser(laser_x_left, laser_y)
        right_laser = Laser(laser_x_right, laser_y)

        # Add them to the active lasers list
        self.lasers.append(middle_laser)
        self.lasers.append(left_laser)
        self.lasers.append(right_laser)

        gSounds['laser'].play()  # Play laser shoot sound


    def Exit(self):
        pass

    def render(self, screen):
        for brick in self.bricks:
            brick.render(screen)

        self.paddle.render(screen)
        self.ball.render(screen)

        # Render all active power-ups
        for powerup in self.active_powerups:
            powerup.render(screen)

        # Render the catch net if it's active
        if self.catch_net_active:
            pygame.draw.rect(screen, (255, 255, 255), self.catch_net_rect)  # Draw a green net at the bottom

        # Render lasers
        for laser in self.lasers:
            laser.render(screen)

        CommonRender.RenderScore(screen, self.score)
        CommonRender.RenderHealth(screen, self.health)

        if self.paused:
            t_pause = gFonts['large'].render("PAUSED", False, (255, 255, 255))
            rect = t_pause.get_rect(center = (WIDTH/2, HEIGHT/2))
            screen.blit(t_pause, rect)


    def CheckVictory(self):
        for brick in self.bricks:
            if brick.alive:
                return False

        return True

class Laser:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 20)  # Size of the laser
        self.speed = 300  # Laser speed

    def update(self, dt):
        self.rect.y -= self.speed * dt  # Move the laser upwards

    def render(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)  # Draw laser as red rectangle
