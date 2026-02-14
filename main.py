import pygame
import random
import sys
import math

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_WIDTH = 70
PIPE_GAP = 200
PIPE_VELOCITY = -4
FLOOR_HEIGHT = 100
BACKGROUND_SCROLL_SPEED = 2

# Colors - Night theme
DARK_BLUE = (10, 15, 40)
DARKER_BLUE = (5, 10, 30)
MOON_YELLOW = (255, 245, 200)
STAR_WHITE = (255, 255, 255)
STAR_YELLOW = (255, 255, 200)
STAR_BLUE = (200, 220, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PIPE_GREEN = (40, 180, 70)
PIPE_DARK_GREEN = (30, 140, 55)
FLOOR_BROWN = (80, 50, 30)
FLOOR_DARK_BROWN = (60, 40, 20)
RED = (255, 80, 80)
YELLOW = (255, 220, 50)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird - Night Edition")
clock = pygame.time.Clock()

# Try to load bird image
try:
    bird_img = pygame.image.load("bird.jpg").convert_alpha()
    # Scale the bird image if it's too large
    bird_img = pygame.transform.scale(bird_img, (50, 35))
except:
    # Create a simple bird image if file not found
    print("bird.png not found, creating a simple bird")
    bird_img = pygame.Surface((50, 35), pygame.SRCALPHA)
    # Draw bird body
    pygame.draw.ellipse(bird_img, YELLOW, (5, 5, 40, 25))
    # Draw wing
    pygame.draw.ellipse(bird_img, (200, 150, 0), (15, 15, 25, 15))
    # Draw eye
    pygame.draw.circle(bird_img, BLACK, (40, 15), 4)
    pygame.draw.circle(bird_img, WHITE, (41, 14), 1)
    # Draw beak
    pygame.draw.polygon(bird_img, RED, [(45, 18), (50, 15), (50, 21)])
    # Outline
    pygame.draw.ellipse(bird_img, BLACK, (5, 5, 40, 25), 2)


class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT - FLOOR_HEIGHT - 100)
        self.size = random.uniform(1.0, 3.0)
        self.brightness = random.uniform(0.3, 1.0)
        self.twinkle_speed = random.uniform(0.02, 0.08)
        self.twinkle_offset = random.uniform(0, math.pi * 2)
        self.color = random.choice([STAR_WHITE, STAR_YELLOW, STAR_BLUE])
        self.speed = random.uniform(0.1, 0.5)  # Stars move slowly

    def update(self):
        # Move star
        self.x -= self.speed
        if self.x < -10:
            self.x = SCREEN_WIDTH + 10
            self.y = random.randint(0, SCREEN_HEIGHT - FLOOR_HEIGHT - 100)

        # Update twinkle
        self.brightness = 0.5 + 0.5 * math.sin(pygame.time.get_ticks() * self.twinkle_speed + self.twinkle_offset)

    def draw(self, screen):
        # Draw star with twinkle effect
        current_color = (
            int(self.color[0] * self.brightness),
            int(self.color[1] * self.brightness),
            int(self.color[2] * self.brightness)
        )
        pygame.draw.circle(screen, current_color, (int(self.x), int(self.y)), int(self.size))


class SoundManager:
    def __init__(self):
        self.sounds = {}



        sound_files = {
            "jump": ["jump_sound.mp3", "jump_sound.wav", "jump.mp3", "jump.wav"],
            "dead": ["dead_sound.mp3", "dead_sound.wav", "die.mp3", "die.wav", "game_over.mp3", "game_over.wav"]
        }

        for sound_name, filenames in sound_files.items():
            loaded = False
            for filename in filenames:
                try:
                    self.sounds[sound_name] = pygame.mixer.Sound(filename)
                    print(f"Loaded sound: {filename}")
                    loaded = True
                    break
                except:
                    continue

            if not loaded:
                print(f"Could not load {sound_name} sound, generating one")
                self.generate_sound(sound_name)

        # Set jump sound volume to 50%
        if "jump" in self.sounds:
            self.sounds["jump"].set_volume(0.5)
            print("Jump sound volume set to 50%")

        # Keep dead sound at 100% (default)
        if "dead" in self.sounds:
            self.sounds["dead"].set_volume(1.0)
            print("Dead sound volume kept at 100%")

        # Try to load background music
        self.music_loaded = False
        music_files = ["bg_music.mp3", "bg_music.wav", "background.mp3", "background.wav"]
        for music_file in music_files:
            try:
                pygame.mixer.music.load(music_file)
                self.music_loaded = True
                print(f"Loaded music: {music_file}")
                break
            except:
                continue

    def generate_sound(self, name):
        """Generate simple sounds if files are not found"""
        sample_rate = 22050

        if name == "jump":
            # Short high-pitched beep for jump
            duration = 0.15
            frames = int(sample_rate * duration)
            sound_data = []

            for i in range(frames):
                # 660Hz tone with decay
                t = i / sample_rate
                volume = 0.5 * (1 - t / duration)  # Decay over time
                value = int(32767 * volume * math.sin(t * 660 * 2 * math.pi))
                sound_data.append([value, value])

            self.sounds[name] = pygame.sndarray.make_sound(pygame.sndarray.array(sound_data))
            # Set jump volume to 50% immediately after creation
            self.sounds[name].set_volume(0.5)

        elif name == "dead":
            # Sad descending tone for death
            duration = 0.6
            frames = int(sample_rate * duration)
            sound_data = []

            for i in range(frames):
                t = i / sample_rate
                # Descend from 440Hz to 220Hz with vibrato
                freq = 440 * (1 - t / duration * 0.5)
                vibrato = 0.9 + 0.1 * math.sin(t * 8 * math.pi)
                value = int(32767 * 0.6 * math.sin(t * freq * 2 * math.pi) * vibrato * (1 - t / duration))
                sound_data.append([value, value])

            self.sounds[name] = pygame.sndarray.make_sound(pygame.sndarray.array(sound_data))
            # Keep dead volume at 100%
            self.sounds[name].set_volume(1.0)

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()


class Bird:
    def __init__(self, image):
        self.x = SCREEN_WIDTH // 3
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.alive = True

        # Bird image and animation
        self.image = image
        self.original_image = image.copy()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.rotation = 0
        self.flap_timer = 0
        self.flap_speed = 0.2
        self.current_frame = 0

    def jump(self):
        self.velocity = JUMP_STRENGTH
        self.flap_timer = 10  # Trigger wing flap

    def update(self):
        # Apply gravity
        self.velocity += GRAVITY
        self.y += self.velocity

        # Update rotation based on velocity
        self.rotation = min(max(self.velocity * 2.5, -30), 30)

        # Update flap animation
        if self.flap_timer > 0:
            self.flap_timer -= 1

        # Rotate the bird image
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

        # Check for floor collision
        if self.y + 20 > SCREEN_HEIGHT - FLOOR_HEIGHT:
            self.y = SCREEN_HEIGHT - FLOOR_HEIGHT - 20
            self.alive = False

        # Check for ceiling collision
        if self.y - 20 < 0:
            self.y = 20
            self.velocity = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        # Draw a glow effect around the bird
        glow_radius = 15
        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (255, 255, 200, 30),
                           (glow_radius, glow_radius), glow_radius)
        screen.blit(glow_surface, (self.rect.centerx - glow_radius,
                                   self.rect.centery - glow_radius))


class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = PIPE_WIDTH
        self.gap_y = random.randint(150, SCREEN_HEIGHT - FLOOR_HEIGHT - PIPE_GAP - 100)
        self.passed = False

        # Pipe colors with variation
        self.color_variation = random.uniform(0.8, 1.2)
        self.pipe_color = (
            min(255, int(PIPE_GREEN[0] * self.color_variation)),
            min(255, int(PIPE_GREEN[1] * self.color_variation)),
            min(255, int(PIPE_GREEN[2] * self.color_variation))
        )
        self.pipe_dark_color = (
            min(255, int(PIPE_DARK_GREEN[0] * self.color_variation)),
            min(255, int(PIPE_DARK_GREEN[1] * self.color_variation)),
            min(255, int(PIPE_DARK_GREEN[2] * self.color_variation))
        )

    def update(self):
        self.x += PIPE_VELOCITY

    def draw(self, screen):
        # Draw top pipe
        top_pipe_height = self.gap_y
        pygame.draw.rect(screen, self.pipe_color,
                         (self.x, 0, self.width, top_pipe_height))

        # Draw top pipe cap
        pygame.draw.rect(screen, self.pipe_dark_color,
                         (self.x - 5, top_pipe_height - 30, self.width + 10, 30))

        # Draw bottom pipe
        bottom_pipe_y = self.gap_y + PIPE_GAP
        bottom_pipe_height = SCREEN_HEIGHT - bottom_pipe_y - FLOOR_HEIGHT
        pygame.draw.rect(screen, self.pipe_color,
                         (self.x, bottom_pipe_y, self.width, bottom_pipe_height))

        # Draw bottom pipe cap
        pygame.draw.rect(screen, self.pipe_dark_color,
                         (self.x - 5, bottom_pipe_y, self.width + 10, 30))

        # Draw pipe glow/reflection
        glow_width = 5
        pygame.draw.rect(screen, (255, 255, 255, 30),
                         (self.x + self.width - glow_width, 0, glow_width, top_pipe_height))
        pygame.draw.rect(screen, (255, 255, 255, 30),
                         (self.x + self.width - glow_width, bottom_pipe_y,
                          glow_width, bottom_pipe_height))

    def collide(self, bird):
        # Simple rectangle collision
        bird_rect = pygame.Rect(bird.x - 20, bird.y - 15, 40, 30)

        # Top pipe rectangle
        top_pipe_rect = pygame.Rect(self.x, 0, self.width, self.gap_y)

        # Bottom pipe rectangle
        bottom_pipe_rect = pygame.Rect(self.x, self.gap_y + PIPE_GAP,
                                       self.width, SCREEN_HEIGHT)

        return bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect)


class NightSky:
    def __init__(self):
        self.stars = []
        self.moon_x = SCREEN_WIDTH - 150
        self.moon_y = 80
        self.moon_phase = 0.7  # 0.0 to 1.0
        self.clouds = []
        self.cloud_speed = 0.3

        # Create stars
        for _ in range(150):
            self.stars.append(Star())

        # Create some clouds
        for _ in range(5):
            self.clouds.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(50, 200),
                'width': random.randint(100, 200),
                'height': random.randint(30, 60),
                'speed': random.uniform(0.1, 0.3),
                'opacity': random.randint(20, 60)
            })

        # Create shooting stars
        self.shooting_stars = []
        self.shooting_star_timer = 0

    def update(self):
        # Update stars
        for star in self.stars:
            star.update()

        # Update clouds
        for cloud in self.clouds:
            cloud['x'] -= cloud['speed']
            if cloud['x'] < -cloud['width']:
                cloud['x'] = SCREEN_WIDTH + cloud['width']
                cloud['y'] = random.randint(50, 200)

        # Update shooting stars
        self.shooting_star_timer += 1
        if self.shooting_star_timer > 300:  # Every 5 seconds at 60 FPS
            self.shooting_star_timer = 0
            if random.random() < 0.3:  # 30% chance
                self.create_shooting_star()

        for shooting_star in self.shooting_stars[:]:
            shooting_star['x'] += shooting_star['speed_x']
            shooting_star['y'] += shooting_star['speed_y']
            shooting_star['life'] -= 1

            if shooting_star['life'] <= 0:
                self.shooting_stars.remove(shooting_star)

    def create_shooting_star(self):
        self.shooting_stars.append({
            'x': random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH),
            'y': random.randint(0, SCREEN_HEIGHT // 3),
            'speed_x': -15,
            'speed_y': 3,
            'life': 40,
            'length': random.randint(20, 40)
        })

    def draw(self, screen):
        # Draw gradient night sky
        for y in range(SCREEN_HEIGHT - FLOOR_HEIGHT):
            # Create gradient from dark blue at top to slightly lighter at bottom
            factor = y / (SCREEN_HEIGHT - FLOOR_HEIGHT)
            color = (
                int(DARK_BLUE[0] * (1 - factor) + DARKER_BLUE[0] * factor),
                int(DARK_BLUE[1] * (1 - factor) + DARKER_BLUE[1] * factor),
                int(DARK_BLUE[2] * (1 - factor) + DARKER_BLUE[2] * factor)
            )
            pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

        # Draw moon
        moon_radius = 40
        # Moon phase effect
        phase_radius = int(moon_radius * self.moon_phase)
        pygame.draw.circle(screen, MOON_YELLOW, (self.moon_x, self.moon_y), moon_radius)
        # Draw darker part for phase
        pygame.draw.circle(screen, DARK_BLUE,
                           (self.moon_x + moon_radius - phase_radius, self.moon_y),
                           moon_radius)
        # Moon craters
        for _ in range(5):
            crater_x = self.moon_x + random.randint(-30, 30)
            crater_y = self.moon_y + random.randint(-30, 30)
            crater_size = random.randint(5, 15)
            pygame.draw.circle(screen, (230, 230, 180), (crater_x, crater_y), crater_size)

        # Draw clouds
        for cloud in self.clouds:
            cloud_surface = pygame.Surface((cloud['width'], cloud['height']), pygame.SRCALPHA)
            # Draw cloud shape
            segments = 5
            segment_width = cloud['width'] // segments
            for i in range(segments):
                x = i * segment_width + segment_width // 2
                y = cloud['height'] // 2
                radius = cloud['height'] // 2
                pygame.draw.circle(cloud_surface, (255, 255, 255, cloud['opacity']),
                                   (x, y), radius)
            screen.blit(cloud_surface, (cloud['x'], cloud['y']))

        # Draw stars
        for star in self.stars:
            star.draw(screen)

        # Draw shooting stars
        for shooting_star in self.shooting_stars:
            # Draw shooting star trail
            for i in range(shooting_star['length']):
                alpha = 255 * (shooting_star['length'] - i) / shooting_star['length']
                pos_x = shooting_star['x'] - i * shooting_star['speed_x'] / 5
                pos_y = shooting_star['y'] - i * shooting_star['speed_y'] / 5
                radius = max(1, 3 * (shooting_star['length'] - i) / shooting_star['length'])
                temp_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(temp_surface, (255, 255, 255, int(alpha)),
                                   (radius, radius), radius)
                screen.blit(temp_surface, (pos_x - radius, pos_y - radius))

        # Draw ground
        pygame.draw.rect(screen, FLOOR_BROWN,
                         (0, SCREEN_HEIGHT - FLOOR_HEIGHT, SCREEN_WIDTH, FLOOR_HEIGHT))

        # Draw ground details
        for i in range(0, SCREEN_WIDTH, 20):
            height = random.randint(5, 15)
            pygame.draw.line(screen, FLOOR_DARK_BROWN,
                             (i, SCREEN_HEIGHT - FLOOR_HEIGHT),
                             (i, SCREEN_HEIGHT - FLOOR_HEIGHT - height), 3)

        # Draw ground glow from moon
        glow_surface = pygame.Surface((SCREEN_WIDTH, 30), pygame.SRCALPHA)
        for i in range(30):
            alpha = int(10 * (1 - i / 30))
            pygame.draw.line(glow_surface, (255, 245, 200, alpha),
                             (0, i), (SCREEN_WIDTH, i))
        screen.blit(glow_surface, (0, SCREEN_HEIGHT - FLOOR_HEIGHT - 30))


class Game:
    def __init__(self):
        self.sound_manager = SoundManager()
        self.night_sky = NightSky()
        self.bird = Bird(bird_img)
        self.pipes = []
        self.score = 0
        self.game_state = "START"
        self.pipe_timer = 0
        self.pipe_interval = 100

        # Start background music if loaded
        if self.sound_manager.music_loaded:
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_state == "START":
                        self.game_state = "PLAYING"
                        self.bird.jump()
                        self.sound_manager.play("jump")
                    elif self.game_state == "PLAYING":
                        self.bird.jump()
                        self.sound_manager.play("jump")
                    elif self.game_state == "GAME_OVER":
                        self.reset_game()

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def update(self):
        self.night_sky.update()

        if self.game_state == "PLAYING":
            self.bird.update()

            # Generate new pipes
            self.pipe_timer += 1
            if self.pipe_timer >= self.pipe_interval:
                self.pipes.append(Pipe(SCREEN_WIDTH))
                self.pipe_timer = 0

            # Update pipes and check collisions
            for pipe in self.pipes[:]:
                pipe.update()

                if pipe.collide(self.bird):
                    self.bird.alive = False
                    self.sound_manager.play("dead")

                if not pipe.passed and pipe.x + pipe.width < self.bird.x:
                    pipe.passed = True
                    self.score += 1

                if pipe.x < -pipe.width:
                    self.pipes.remove(pipe)

            if not self.bird.alive:
                self.game_over_sequence()

    def game_over_sequence(self):
        self.game_state = "GAME_OVER"
        if self.sound_manager.music_loaded:
            pygame.mixer.music.stop()

    def draw(self, screen):
        # Draw night sky
        self.night_sky.draw(screen)

        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(screen)

        # Draw bird
        self.bird.draw(screen)

        # Draw score
        score_font = pygame.font.SysFont('Arial', 36)
        score_text = score_font.render(f"Score: {self.score}", True, WHITE)
        score_shadow = score_font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_shadow, (22, 22))
        screen.blit(score_text, (20, 20))

        # Draw game state messages
        if self.game_state == "START":
            self.draw_start_screen()
        elif self.game_state == "GAME_OVER":
            self.draw_game_over_screen()

    def draw_start_screen(self):
        # Draw title with glow effect
        title_font = pygame.font.SysFont('Arial', 64, bold=True)
        title = "FLAPPY BIRD"
        title_text = title_font.render(title, True, YELLOW)
        title_shadow = title_font.render(title, True, (255, 150, 50, 128))

        # Draw glow
        for offset in range(1, 10, 2):
            screen.blit(title_shadow,
                        (SCREEN_WIDTH // 2 - title_text.get_width() // 2,
                         SCREEN_HEIGHT // 3 - 50 + offset))

        screen.blit(title_text,
                    (SCREEN_WIDTH // 2 - title_text.get_width() // 2,
                     SCREEN_HEIGHT // 3 - 50))

        # Draw subtitle
        subtitle_font = pygame.font.SysFont('Arial', 32)
        subtitle = "Night Edition"
        subtitle_text = subtitle_font.render(subtitle, True, (200, 220, 255))
        screen.blit(subtitle_text,
                    (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2,
                     SCREEN_HEIGHT // 3 + 20))

        # Draw instructions
        instruction_font = pygame.font.SysFont('Arial', 28)
        start_text = instruction_font.render("Press SPACE to start", True, WHITE)
        screen.blit(start_text,
                    (SCREEN_WIDTH // 2 - start_text.get_width() // 2,
                     SCREEN_HEIGHT // 2 + 40))

        # Draw moon icon
        moon_icon = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(moon_icon, MOON_YELLOW, (15, 15), 15)
        screen.blit(moon_icon, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 80))

        # Draw controls
        controls_font = pygame.font.SysFont('Arial', 24)
        controls = ["SPACE - Jump", "ESC - Quit"]
        for i, control in enumerate(controls):
            control_text = controls_font.render(control, True, (200, 200, 200))
            screen.blit(control_text,
                        (SCREEN_WIDTH // 2 - control_text.get_width() // 2,
                         SCREEN_HEIGHT // 2 + 120 + i * 40))

    def draw_game_over_screen(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        # Draw game over text
        game_over_font = pygame.font.SysFont('Arial', 72, bold=True)
        game_over_text = game_over_font.render("GAME OVER", True, RED)
        game_over_shadow = game_over_font.render("GAME OVER", True, BLACK)

        # Draw shadow
        screen.blit(game_over_shadow,
                    (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2 + 3,
                     SCREEN_HEIGHT // 3 + 3))

        screen.blit(game_over_text,
                    (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                     SCREEN_HEIGHT // 3))

        # Draw final score
        score_font = pygame.font.SysFont('Arial', 48)
        final_score = score_font.render(f"Final Score: {self.score}", True, WHITE)
        screen.blit(final_score,
                    (SCREEN_WIDTH // 2 - final_score.get_width() // 2,
                     SCREEN_HEIGHT // 2))

        # Draw restart instructions
        restart_font = pygame.font.SysFont('Arial', 32)
        restart_text = restart_font.render("Press SPACE to play again", True, YELLOW)
        screen.blit(restart_text,
                    (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                     SCREEN_HEIGHT // 2 + 80))

    def reset_game(self):
        self.__init__()


# Main game loop
def main():
    game = Game()

    running = True
    while running:
        game.handle_events()
        game.update()
        game.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
