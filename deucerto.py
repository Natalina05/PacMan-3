import pygame
import random
import math


# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLUE = (255, 0, 0,)
RED = (255,0,0)


# Set up the game window
window_width = 606
window_height = 606
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Pacman Game")

# Define wall positions
walls = [
    [0, 0, 6, 600],
    [0, 0, 600, 6],
    [0, 600, 606, 6],
    [600, 0, 6, 606],
    [300, 0, 6, 66],
    [60, 60, 186, 6],
    [360, 60, 186, 6],
    [60, 120, 66, 6],
    [60, 120, 6, 126],
    [180, 120, 246, 6],
    [300, 120, 6, 66],
    [480, 120, 66, 6],
    [540, 120, 6, 126],
    [120, 180, 126, 6],
    [120, 180, 6, 126],
    [360, 180, 126, 6],
    [480, 180, 6, 126],
    [180, 240, 6, 126],
    [180, 360, 246, 6],
    [420, 240, 6, 126],
    [240, 240, 42, 6],
    [324, 240, 42, 6],
    [240, 240, 6, 66],
    [240, 300, 126, 6],
    [360, 240, 6, 66],
    [0, 300, 66, 6],
    [540, 300, 66, 6],
    [60, 360, 66, 6],
    [60, 360, 6, 186],
    [480, 360, 66, 6],
    [540, 360, 6, 186],
    [120, 420, 366, 6],
    [120, 420, 6, 66],
    [480, 420, 6, 66],
    [180, 480, 246, 6],
    [300, 480, 6, 66],
    [120, 540, 126, 6],
    [360, 540, 126, 6],
]

# Set up game variables
clock = pygame.time.Clock()
pacman_position = [window_width // 2, window_height // 2.5] # Posiciona o Pacman no centro da tela
pacman_radius = 15
pacman_speed = 5
reward_radius = 10
rewards = []
score = 0

# Generate rewards
num_rewards = 10
for _ in range(num_rewards):
    x = random.randint(30, window_width - 30)
    y = random.randint(30, window_height - 30)
    rewards.append((x, y))

# Game states
GAME_STATE_PLAYING = "playing"
GAME_STATE_WIN = "win"
GAME_STATE_GAME_OVER = "game_over"

game_state = GAME_STATE_PLAYING

# Carregar a imagem do inimigo
enemy_image = pygame.image.load('PapaiNoelDireita.gif')
enemy_image = pygame.transform.scale(enemy_image, (60, 60))  # Redimensiona a imagem se necessario

# Carregar a imagem do Pac-Man
pac_image = pygame.image.load('GrinchDireita.gif')
pac_image = pygame.transform.scale(pac_image, (70, 70))  # Redimensiona a imagem se necessario

# Carregar a imagem do Presente
presente_image = pygame.image.load('Presente Gode Girls.png')
presente_image = pygame.transform.scale(presente_image, (40, 40))  # Redimensiona a imagem se necessario

#Enemies class
class Enemy:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.direction = random.choice(['left', 'right', 'up', 'down'])

    
    def move(self):
        # Temporary copy of the enemy's current position
        temp_x = self.x
        temp_y = self.y

        # Try to move in the current direction
        if self.direction == 'left':
            temp_x -= self.speed
        elif self.direction == 'right':
            temp_x += self.speed
        elif self.direction == 'up':
            temp_y -= self.speed
        elif self.direction == 'down':
            temp_y += self.speed

        # Check for collision with walls in current direction
        enemy_rect = pygame.Rect(temp_x - self.radius, temp_y - self.radius, 2 * self.radius, 2 * self.radius)
        for wall in walls:
            wall_rect = pygame.Rect(wall[0], wall[1], wall[2], wall[3])
            if enemy_rect.colliderect(wall_rect):
                # If there is a collision, select a new random address
                self.direction = random.choice(['left', 'right', 'up', 'down'])
                break
        else:
            # No collision, update enemy position
            self.x = temp_x
            self.y = temp_y


    def check_collision(self, pacman_position, pacman_radius):
        distance = math.hypot(self.x - pacman_position[0], self.y - pacman_position[1])
        if distance < self.radius + pacman_radius:
            return True
        return False

# Set up game variables

# Classe Pacman
class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y 
        
enemies = []
num_enemies = 2

# Generate enemies
for _ in range(num_enemies):
    valid_position = False
    while not valid_position: #dist colisao
        x = random.randint(30, window_width - 30)
        y = random.randint(30, window_height - 30)
        if not any(pygame.Rect(wall).colliderect(pygame.Rect(x - pacman_radius, y - pacman_radius, 2 * pacman_radius, 2 * pacman_radius)) for wall in walls):
            valid_position = True
            for enemy in enemies:
                if math.hypot(x - enemy.x, y - enemy.y) < 2 * enemy.radius:
                    valid_position = False
                    break
    enemies.append(Enemy(x, y, 10, 2))

    
# Game loop
running = True
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if game_state == GAME_STATE_WIN and event.key == pygame.K_RETURN:
                # Reset the game if in win state and Enter key is pressed
                rewards = []
                for _ in range(num_rewards):
                    x = random.randint(30, window_width - 30)
                    y = random.randint(30, window_height - 30)
                    rewards.append((x, y))
                score = 0
                game_state = GAME_STATE_PLAYING

    window.fill(BLACK)

    # Draw walls
    for wall in walls:
        pygame.draw.rect(window, BLUE, wall)

    if game_state == GAME_STATE_PLAYING:
        # Draw rewards
        for reward in rewards:
           # pygame.draw.circle(window, WHITE, reward, reward_radius)
            window.blit(presente_image, (reward[0] - reward_radius, reward[1] - reward_radius))

        # Move Pacman
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and pacman_position[0] > pacman_radius:
            pacman_position[0] -= pacman_speed
        if keys[pygame.K_RIGHT] and pacman_position[0] < window_width - pacman_radius:
            pacman_position[0] += pacman_speed
        if keys[pygame.K_UP] and pacman_position[1] > pacman_radius:
            pacman_position[1] -= pacman_speed
        if keys[pygame.K_DOWN] and pacman_position[1] < window_height - pacman_radius:
            pacman_position[1] += pacman_speed

        # Check for collision with walls
        pacman_rect = pygame.Rect(
            pacman_position[0] - pacman_radius,
            pacman_position[1] - pacman_radius,
            2 * pacman_radius,
            2 * pacman_radius
        )

        for wall in walls:
            wall_rect = pygame.Rect(wall[0], wall[1], wall[2], wall[3])
            if pacman_rect.colliderect(wall_rect):
                # Pacman collided with a wall, revert its position
                if pacman_position[0] < wall_rect.left:
                    pacman_position[0] = wall_rect.left - pacman_radius
                elif pacman_position[0] > wall_rect.right:
                    pacman_position[0] = wall_rect.right + pacman_radius
                if pacman_position[1] < wall_rect.top:
                    pacman_position[1] = wall_rect.top - pacman_radius
                elif pacman_position[1] > wall_rect.bottom:
                    pacman_position[1] = wall_rect.bottom + pacman_radius

        # Check for collision with rewards
        for reward in rewards:
            reward_pos = pygame.Rect(reward[0], reward[1], 2 * reward_radius, 2 * reward_radius)
            if reward_pos.colliderect(pacman_rect):
                rewards.remove(reward)
                score += 1

                # Check if all rewards are collected
                if score == num_rewards:
                    game_state = GAME_STATE_WIN

        
        # Desenhando o inimigo
        for enemy in enemies:
            window.blit(enemy_image, (enemy.x + 15, enemy.y + 15))  # Ajusta a posição para centralizar a imagem

        for enemy in enemies:
            enemy.move()

        for enemy in enemies:
            if enemy.check_collision(pacman_position, pacman_radius):
                game_state = GAME_STATE_GAME_OVER
                
     # Criação do Pacman
        # Draw Pacman
        window.blit(pac_image, (pacman_position[0] - pacman_radius, pacman_position[1] - pacman_radius))

        # Draw score
        score_text = f"Score: {score}"
        font = pygame.font.Font(None, 36)
        text = font.render(score_text, True, WHITE)
        window.blit(text, (10, 10))

    elif game_state == GAME_STATE_WIN:
        pacman_position = [window_width // 2, window_height // 2.5]
        
        # Draw win message
        win_text = "You Win! Press Enter to play again."
        font = pygame.font.Font(None, 48)
        text = font.render(win_text, True, WHITE)
        text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(text, text_rect)


    elif game_state == GAME_STATE_GAME_OVER:
          # Draw game over message
        game_over_text = "Game over. Press Enter to play again."
        font = pygame.font.Font(None, 48)
        text = font.render(game_over_text, True, WHITE)
        text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(text, text_rect)

        # Check if Enter key is pressed to restart the game
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            # Reset game variables
            pacman_position = [window_width // 2, window_height // 2.5]
            score = 0
            enemies = []
            for _ in range(num_enemies):
                valid_position = False
                while not valid_position:
                    x = random.randint(30, window_width - 30)
                    y = random.randint(30, window_height - 30)
                    if not any(pygame.Rect(wall).colliderect(pygame.Rect(x - pacman_radius, y - pacman_radius, 2 * pacman_radius, 2 * pacman_radius)) for wall in walls):
                        valid_position = True
                        for enemy in enemies:
                            if math.hypot(x - enemy.x, y - enemy.y) < 2 * enemy.radius:
                                valid_position = False
                                break
                enemies.append(Enemy(x, y, 10, 2))

            # Reset rewards
            rewards = []
            for _ in range(num_rewards):
                x = random.randint(30, window_width - 30)
                y = random.randint(30, window_height - 30)
                rewards.append((x, y))

            # Reset game state
            game_state = GAME_STATE_PLAYING

    # Update the window
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Quit the game
pygame.quit() 



