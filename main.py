import pygame
from characters import Character, EnemyGen, BossGen
import random
import sys
import json

import tkinter as tk
from tkinter import filedialog

# Initialize Pygame and Default Variables
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(), 24)  # Uses a default system font
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fight Simulator")
RED, GREEN, WHITE, BLACK = (255, 0, 0), (0, 255, 0), (255, 255, 255), (0, 0, 0)

enemy_types = ["Hamon User", "Vampire"]  # To implement later: random.choice(["Human", "Hamon User", "Vampire", "Cambion"])


def get_json_filepath():
    """Opens a file dialog to let the user choose a JSON character file."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select Character JSON File",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    return file_path  # Returns the selected JSON file path


def load_character(json_path):
    """Loads a character from a user-selected JSON file."""
    try:
        with open(json_path, "r") as f:
            data = json.load(f)

        # Ensure a sprite path exists, otherwise set a default
        sprite_path = data.get("sprite_path", "sprites/default.png")
        if not data["x"]:
            data["x"] = 100
        if not data["y"]:
            data["y"] = 100

        return Character(
            race=data["race"],
            name=data["name"],
            combat_style=data["combat_style"],
            max_hp=data["max_hp"],
            hp=data["hp"],
            attack=data["attack"],
            spattack=data["spattack"],
            defense=data["defense"],
            spdefense=data["spdefense"],
            max_energy=data["max_energy"],
            energy=data["energy"],
            energy_regen=data["energy_regen"],
            moves=data["moves"],
            sprite_path=sprite_path,  # Use default if missing
            x=data["x"],
            y=data["y"]
        )
    except Exception as e:
        print(f"Error loading character: {e}")
        return None


def generate_enemy(multi=1):
    # Choose an enemy type and run the corresponding function
    Selection = EnemyGen(enemy_types)
    enemy_data, enemy_json = Selection.gen_enemy(multi)
    # Save the enemy to JSON
    filename = f"assets/enemies/{enemy_data.name}.json"
    with open(filename, "w") as f:
        json.dump(enemy_json, f, indent=4)
    print("Enemy saved to", filename)
    return enemy_data


def generate_boss(multi=1):
    # Choose an enemy type and run the corresponding function
    Selection = BossGen(enemy_types)
    enemy_data, enemy_json = Selection.gen_boss(multi)
    # Save the enemy to JSON
    filename = f"assets/enemies/bosses/{enemy_data.name}.json"
    with open(filename, "w") as f:
        json.dump(enemy_json, f, indent=4)
    print("Enemy saved to", filename)
    return enemy_data


# Load characters
fighter_data = get_json_filepath()  # Ask user to select JSON file
if fighter_data:
    player = load_character(fighter_data)
    if player:
        print(f"Loaded character: {player.name}")
    else:
        print("Failed to load character.")
else:
    print("No file selected, attempting to use 'selected_character.json'...")
    player = load_character('selected_character.json')
    if player:
        print(f"Loaded character: {player.name}")
    else:
        print("Failed to load character. Please run 'create_custom.py' to make a character, or run 'select_character.py' to use a saved one!")


if not fighter_data:
    pygame.quit()
    sys.exit()


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
        font.render(f"4: {player.moves[3]['name']}", True, BLACK),
    ]

    for i, text in enumerate(move_texts):
        screen.blit(text, (50, 500 + i * 30))  # Position move choices


def boss_choice():
    try:
        diff_choice = int(input("Choose between a Boss Fight (0), a Slightly Harder Fight (1), or a Normal Fight (2).\n"))
        return diff_choice
    except ValueError as e:
        print(f"Exception occured: {e}. Did you type a number?\n")


def battle_check(in_name, in_damage):
    global message, game_over, turn, victory_text
    if in_damage > 0:
        message = f"Hero used {in_name}! Deals {in_damage} damage!"
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


# Game variables
turn = "player"  # Who goes first
game_over = False
message = ""  # Display messages

choice = boss_choice()
if choice == 0:
    enemy = generate_boss()


elif choice == 1:
    enemy = generate_enemy(multi=2)

else:
    enemy = generate_enemy()

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
                move_name, damage = player.use_move(0, enemy, enemy.race)

                battle_check(move_name, damage)
            elif event.key == pygame.K_2:  # Second move
                move_name, damage = player.use_move(1, enemy, enemy.race)

                battle_check(move_name, damage)
            elif event.key == pygame.K_3:  # Third move
                move_name, damage = player.use_move(2, enemy, enemy.race)

            elif event.key == pygame.K_4:  # Fourth move
                move_name, damage = player.use_move(3, enemy, enemy.race)

                battle_check(move_name, damage)
            elif event.key == pygame.K_0:  # Default attack
                if player.combat_style == "Hamon":
                    move_name, damage = "Hamon Strike", player.attack_target(enemy, enemy.race)
                elif player.combat_style == "Physical":
                    move_name, damage = "Simple Jab", player.attack_target(enemy, enemy.race)
                else:
                    move_name, damage = "Vampiric Slash", player.attack_target(enemy, enemy.race)

                battle_check(move_name, damage)

            elif event.key == pygame.K_d:
                print("Defending!")
                player.is_defending = True
                message = "Hero is defending!"

    # Enemy turn (Basic AI)
    if turn == "enemy" and enemy.is_alive():
        pygame.time.delay(1000)  # Pause before AI moves
        affordable_moves = [i for i in range(len(enemy.moves)) if enemy.energy >= enemy.moves[i]["energy_cost"]]
        if enemy.hp > player.hp * 1.5:
            action = random.choice(["attack", "move"])
        elif enemy.hp * 2 < player.hp:
            action = "move"
        else:
            action = random.choice(["attack", "defend", "move"])  # Random action
        if action == "attack":
            damage = enemy.attack_target(player, player.race)
            message = f"Villain attacks! Deals {damage} damage!"
        elif action == "move":
            if affordable_moves:  # If the enemy has a move it can use
                move_index = random.choice(affordable_moves)  # Pick a random affordable move
                move_name, damage = enemy.use_move(move_index, player, player.race)
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

        pygame.display.flip()
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
