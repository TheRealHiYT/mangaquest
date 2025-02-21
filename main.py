import pygame
from characters import Character
import random
import sys

# Initialize Pygame and Default Variables
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(), 24)  # Uses a default system font
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fight Simulator")
RED, GREEN, WHITE, BLACK = (255, 0, 0), (0, 255, 0), (255, 255, 255), (0, 0, 0)



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
    pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))

    # Draw the health (green)
    pygame.draw.rect(screen, GREEN, (x, y, int(bar_width * health_ratio), bar_height))

    # Draw text showing HP
    hp_text = font.render(f"{fighter.hp}/{fighter.maxhp} HP", True, (0, 0, 0))
    screen.blit(hp_text, (x + 50, y - 25))  # Position text above the bar


def draw_energy_bar(fighter, x, y):
    """Draw the energy bar for a fighter."""
    bar_width = 200
    bar_height = 10
    energy_ratio = fighter.energy / fighter.max_energy  # Percentage of energy left

    # Draw the background (gray)
    pygame.draw.rect(screen, (100, 100, 100), (x, y, bar_width, bar_height))

    # Draw the energy (blue)
    pygame.draw.rect(screen, (0, 0, 255), (x, y, int(bar_width * energy_ratio), bar_height))

    # Draw text showing Energy
    energy_text = font.render(f"Energy: {fighter.energy}/{fighter.max_energy}", True, BLACK)
    screen.blit(energy_text, (x, y - 20))  # Position text above the bar


def draw_move_options():
    """Draw move choices on the screen."""
    move_texts = [
        font.render(f"1: {player.moves[0]['name']}", True, BLACK),
        font.render(f"2: {player.moves[1]['name']}", True, BLACK),
        font.render(f"3: {player.moves[2]['name']}", True, BLACK),
    ]

    for i, text in enumerate(move_texts):
        screen.blit(text, (50, 500 + i * 30))  # Position move choices


# Game variables
turn = "player"  # Who goes first
game_over = False
message = ""  # Display messages

while not game_over:
    screen.fill(WHITE)

    # Draw health bars
    draw_health_bar(player, 50, 50)
    draw_energy_bar(player, 50, 80)  # Energy bar below HP bar

    draw_health_bar(enemy, 550, 50)
    draw_energy_bar(enemy, 550, 80)

    # Draw characters
    player.draw(screen)
    enemy.draw(screen)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN and turn == "player":
            if event.key == pygame.K_1:  # First move
                move_name, damage = player.use_move(0, enemy)
            elif event.key == pygame.K_2:  # Second move
                move_name, damage = player.use_move(1, enemy)
            elif event.key == pygame.K_3:  # Third move
                move_name, damage = player.use_move(2, enemy)

            if damage > 0:
                message = f"Hero used {move_name}! Deals {damage} damage!"
                player.regen_energy()

                # Check if the enemy is defeated
                if enemy.hp <= 0:
                    message = "Hero Wins!"
                    screen.fill(WHITE)  # Clear screen
                    victory_text = font.render("Hero Wins!", True, (0, 255, 0))
                    screen.blit(victory_text, (300, 250))  # Show victory message
                    pygame.display.flip()
                    pygame.time.delay(3000)  # Wait 3 seconds
                    game_over = True  # Exit the loop
                else:
                    turn = "enemy"
            else:
                message = "Not enough energy!"

    # Enemy turn (Basic AI)
    if turn == "enemy" and enemy.is_alive():
        pygame.time.delay(1000)  # Pause before AI moves
        affordable_moves = [i for i in range(len(enemy.moves)) if enemy.energy >= enemy.moves[i]["energy_cost"]]
        action = random.choice(["attack", "defend", "move"])  # Random action
        if action == "attack":
            damage = enemy.melee_target(player)
            message = f"Villain attacks! Deals {damage} damage!"
        elif action == "move":
            if affordable_moves:  # If the enemy has a move it can use
                move_index = random.choice(affordable_moves)  # Pick a random affordable move
                move_name, damage = enemy.use_move(move_index, player)
                message = f"Villain used {move_name}! Deals {damage} damage!"
        if player.hp <= 0:
            message = "Villain Wins!"
            screen.fill(WHITE)
            victory_text = font.render("Villain Wins!", True, (255, 0, 0))
            screen.blit(victory_text, (300, 250))
            pygame.display.flip()
            pygame.time.delay(3000)
            game_over = True
        else:
            enemy.is_defending = True
            message = "Villain is defending!"

        enemy.regen_energy()  # Enemy regenerates energy
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
    msg_text = font.render(message, True, BLACK)
    screen.blit(msg_text, (WIDTH // 2 - 150, HEIGHT - 100))
    draw_move_options()  # Display move choices

    pygame.display.flip()  # Update screen
    clock.tick(30)  # Limit FPS


if game_over:
    pygame.quit()
    sys.exit()

