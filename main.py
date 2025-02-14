import pygame
from characters import Character
import random

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(), 24)  # Uses a default system font
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fight Simulator")

player_moves = [
    {"name": "Punch", "damage": 10, "energy_cost": 5},
    {"name": "Kick", "damage": 15, "energy_cost": 10},
    {"name": "Fireball", "damage": 25, "energy_cost": 20},  # Strong but costly
]

enemy_moves = [
    {"name": "Scratch", "damage": 8, "energy_cost": 4},
    {"name": "Bite", "damage": 12, "energy_cost": 8},
    {"name": "Dark Slash", "damage": 20, "energy_cost": 15},
]


# Load characters
player = Character("Hero", 100, 100, 20, 5, 5, 10, 50, 50, 10, player_moves, "assets/sprites/hero_blank.png", -50, 300)
enemy = Character("Enemy", 80, 80, 15, 10, 3, 5, 40, 40, 15, enemy_moves, "assets/sprites/enemy_blank.png", 450, 300)


# Function for initializing health bars
def draw_health_bar(fighter, x, y):
    bar_width = 200
    bar_height = 20

    health_ratio = fighter.hp / fighter.maxhp  # Percentage of health left

    # Draw the background (red)
    pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width, bar_height))

    # Draw the health (green)
    pygame.draw.rect(screen, (0, 255, 0), (x, y, int(bar_width * health_ratio), bar_height))

    # Draw text showing HP
    hp_text = font.render(f"{fighter.hp}/{fighter.maxhp} HP", True, (0, 0, 0))
    screen.blit(hp_text, (x + 50, y - 25))  # Position text above the bar


def draw_move_options():
    """Draw move choices on the screen."""
    move_texts = [
        font.render(f"1: {player.moves[0]['name']}", True, (0, 0, 0)),
        font.render(f"2: {player.moves[1]['name']}", True, (0, 0, 0)),
        font.render(f"3: {player.moves[2]['name']}", True, (0, 0, 0)),
    ]

    for i, text in enumerate(move_texts):
        screen.blit(text, (50, 500 + i * 30))  # Position move choices


# Game variables
turn = "player"  # Who goes first
game_over = False
message = ""  # Display messages

while not game_over:
    screen.fill((255, 255, 255))

    # Draw health bars
    draw_health_bar(player, 50, 50)
    draw_health_bar(enemy, 550, 50)

    # Draw characters
    player.draw(screen)
    enemy.draw(screen)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN and turn == "player":
            if event.key == pygame.K_a:  # Attack
                damage = player.melee_target(enemy)
                message = f"Hero attacks! Deals {damage} damage!"
                turn = "enemy"
            elif event.key == pygame.K_d:  # Defend
                player.is_defending = True
                message = "Hero is defending!"
                turn = "enemy"
            elif event.key == pygame.K_1:  # First move
                move_name, damage = player.use_move(0, enemy)
                message = f"Hero used {move_name}! Deals {damage} damage!"
                turn = "enemy"
            elif event.key == pygame.K_2:  # Second move
                move_name, damage = player.use_move(1, enemy)
                message = f"Hero used {move_name}! Deals {damage} damage!"
                turn = "enemy"
            elif event.key == pygame.K_3:  # Third move
                move_name, damage = player.use_move(2, enemy)
                message = f"Hero used {move_name}! Deals {damage} damage!"
                turn = "enemy"

    # Enemy turn (Basic AI)
    if turn == "enemy" and enemy.is_alive():
        pygame.time.delay(1000)  # Pause before AI moves
        action = random.choice(["attack", "defend", "move"])  # Random action
        if action == "attack":
            damage = enemy.melee_target(player)
            message = f"Villain attacks! Deals {damage} damage!"
        elif action == "move":
            move_index = random.randint(0, len(enemy.moves) - 1)  # Pick random move
            move_name, damage = enemy.use_move(move_index, player)
            message = f"Villain used {move_name}! Deals {damage} damage!"
        else:
            enemy.is_defending = True
            message = "Villain is defending!"

        turn = "player"  # Switch turn back to player

    # Check for winner
    if not player.is_alive():
        message = "Villain wins!"

        # Update health bars
        draw_health_bar(player, 50, 50)
        draw_health_bar(enemy, 550, 50)

        pygame.time.delay(4000)
        game_over = True
    elif not enemy.is_alive():
        message = "Hero wins!"

        # Update health bars
        draw_health_bar(player, 50, 50)
        draw_health_bar(enemy, 550, 50)

        pygame.time.delay(4000)
        game_over = True

    # Display messages
    msg_text = font.render(message, True, (0, 0, 0))
    screen.blit(msg_text, (WIDTH // 2 - 150, HEIGHT - 100))
    draw_move_options()  # Display move choices

    pygame.display.flip()  # Update screen
    clock.tick(30)  # Limit FPS


pygame.quit()
