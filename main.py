import pygame
from characters import Character, BossCharacter
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

enemy_moves = [
    {"name": "Scratch", "damage": 8, "energy_cost": 4, "type": "PHY"},
    {"name": "Bite", "damage": 12, "energy_cost": 8, "type": "PHY"},
    {"name": "Dark Slash", "damage": 20, "energy_cost": 15, "type": "PHY"},
]


def get_json_filepath():
    """Opens a file dialog to let the user choose a JSON character file."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select Character JSON File",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )

    return file_path if file_path else None  # Return None if no file was selected


def load_character(json_path):
    """Loads a character from a user-selected JSON file."""
    if not json_path:
        print("No file selected.")
        return None

    try:
        with open(json_path, "r") as f:
            data = json.load(f)

        # Ensure all required keys exist, using default values where appropriate
        return Character(
            race=data.get("race", "Unknown"),
            name=data.get("name", "Unnamed"),
            combat_style=data.get("combat_style", "None"),
            max_hp=data.get("max_hp", 100),
            hp=data.get("hp", 100),
            attack=data.get("attack", 10),
            spattack=data.get("spattack", 10),
            defense=data.get("defense", 5),
            spdefense=data.get("spdefense", 5),
            max_energy=data.get("max_energy", 50),
            energy=data.get("energy", 50),
            energy_regen=data.get("energy_regen", 5),
            moves=data.get("moves", []),
            sprite_path=data.get("sprite_path", "sprites/default.png"),
            x=data.get("x", 0),
            y=data.get("y", 0)
        )

    except FileNotFoundError:
        print(f"Error: File '{json_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file '{json_path}'.")
    except KeyError as e:
        print(f"Error: Missing expected key {e} in JSON file.")
    except Exception as e:
        print(f"Unexpected error loading character: {e}")

    return None  # Return None if an error occurs


# Load characters
fighter_data = get_json_filepath()  # Ask user to select JSON file
if fighter_data:
    player = load_character(fighter_data)
    if player:
        print(f"Loaded character: {player.get_name()}")
    else:
        print("Failed to load character.")
else:
    print("No file selected.")

if not fighter_data:
    print("No character loaded. Terminating..")
    pygame.quit()
    sys.exit()


# Function for initializing health bars
def draw_health_bar(fighter, x, y):
    bar_width = 200
    bar_height = 20

    health_ratio = fighter.get_hp() / fighter.get_max_hp()  # Percentage of health left

    # Draw the background (red)
    pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))

    # Draw the health (green)
    pygame.draw.rect(screen, GREEN, (x, y, int(bar_width * health_ratio), bar_height))

    # Draw text showing HP
    hp_text = font.render(f"{fighter.get_hp()}/{fighter.get_max_hp()} HP", True, (0, 0, 0))
    screen.blit(hp_text, (x + 50, y - 25))  # Position text above the bar


def draw_energy_bar(fighter, x, y):
    """Draw the energy bar for a fighter."""
    bar_width = 200
    bar_height = 5
    energy_ratio = fighter.get_energy() / fighter.get_max_energy()  # Percentage of energy left

    # Draw the background (gray)
    pygame.draw.rect(screen, (100, 100, 100), (x, y, bar_width, bar_height))

    # Draw the energy (blue)
    pygame.draw.rect(screen, (0, 0, 255), (x, y, int(bar_width * energy_ratio), bar_height))

    # Draw text showing Energy
    energy_text = font.render(f"Energy: {fighter.get_energy()}/{fighter.get_max_energy()}", True, BLACK)
    screen.blit(energy_text, (x, y - 20))  # Position text above the bar


def draw_move_options():
    """Draw move choices on the screen."""
    move_texts = [
        font.render(f"1: {player.get_moves()[0]['name']}", True, BLACK),
        font.render(f"2: {player.get_moves()[1]['name']}", True, BLACK),
        font.render(f"3: {player.get_moves()[2]['name']}", True, BLACK),
        font.render(f"4: {player.get_moves()[3]['name']}", True, BLACK),
    ]

    for i, text in enumerate(move_texts):
        screen.blit(text, (50, 500 + i * 30))  # Position move choices


def boss_choice():
    try:
        difficulty = int(input("Choose between a Boss Fight (0), a Slightly Harder Fight (1), or a Normal Fight (2).\n"))
        return difficulty
    except ValueError as e:
        print(f"Exception occured: {e}. Did you type a number?\n")


def battle_check(in_name, in_damage):
    global message, game_over, turn, victory_text
    if in_damage > 0:
        message = f"Hero used {in_name}! Deals {in_damage} damage!"
        player.regen_energy()

        # Check if the enemy is defeated
        if enemy.get_hp() <= 0:
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
    enemy = BossCharacter("Vampire", "Dio Brando", "The Immortal King - ", "Vamprism", 2200, 2200, 205, 225, 245, 270, 500, 500, 25,
                          [{"name": "MUDA!", "damage": 25, "energy_cost": 40, "type": "VAM"},
                           {"name": "MUDA Barrage", "damage": 60, "energy_cost": 95, "type": "VAM"},
                           {"name": "Impale", "damage": 45, "energy_cost": 75, "type": "VAM"},
                           {"name": "Timestop Impale", "damage": 145, "energy_cost": 115, "type": "VAM"}], 3, 2,

                          [{"name": "Timestop Barrage", "damage": 225, "energy_cost": 50, "type": "VAM"},
                           {"name": "Timestop MUDA! Kicks", "damage": 195, "energy_cost": 35, "type": "VAM"}],
                          "assets/sprites/enemy_blank.png", 450, 300)
elif choice == 1:
    enemy = Character("Human", "Enemy", "Physical", 250, 250, 15, 10, 3, 5, 40, 40, 15, enemy_moves,
                      "assets/sprites/enemy_blank.png",
                      450, 300)
else:
    enemy = Character("Human", "Enemy", "Physical", 250, 250, 15, 10, 3, 5, 40, 40, 15, enemy_moves,
                      "assets/sprites/enemy_blank.png", 450, 300)

while not game_over:
    screen.fill(WHITE)

    # Draw Health bars and Energy bars
    draw_health_bar(player, 50, 50)
    draw_energy_bar(player, 50, 80)

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
                move_name, damage, atk_type = player.use_move(0, enemy, enemy.get_race())
                battle_check(move_name, damage)

            elif event.key == pygame.K_2:  # Second move
                move_name, damage, atk_type = player.use_move(1, enemy, enemy.get_race())
                battle_check(move_name, damage)

            elif event.key == pygame.K_3:  # Third move
                move_name, damage, atk_type = player.use_move(2, enemy, enemy.get_race())

            elif event.key == pygame.K_4:  # Fourth move
                move_name, damage, atk_type = player.use_move(3, enemy, enemy.get_race())
                battle_check(move_name, damage)

            elif event.key == pygame.K_0:  # Default attack
                if player.get_combat_style() == "Hamon":
                    move_name, damage = "Hamon Overdrive", player.attack_target(enemy, enemy.get_race())
                elif player.get_combat_style() == "Physical":
                    move_name, damage = "Simple Jab", player.attack_target(enemy, enemy.get_race())
                else:
                    move_name, damage = "Vampiric Bone-Saw", player.attack_target(enemy, enemy.get_race())

                battle_check(move_name, damage)

            elif event.key == pygame.K_d:
                print("Defending!")
                player.set_defending(True)
                message = "Hero is defending!"

        # Enemy turn (Basic AI)
        elif turn == "enemy" and enemy.is_alive():
            pygame.time.delay(1000)  # Pause before AI moves

            affordable_moves = [i for i in range(len(enemy.get_moves())) if
                                enemy.get_energy() >= enemy.get_moves()[i]["energy_cost"]]
            affordable_leg_moves = [i for i in range(len(enemy.get_leg_moves())) if
                                    enemy.get_energy() >= enemy.get_leg_moves()[i]["energy_cost"]]

            if isinstance(enemy, BossCharacter):  # Boss AI
                if enemy.get_hp() < player.get_hp() * 1.5:
                    action = "leg_action"
                else:
                    action = random.choice(["leg_action", "move", "attack", "defend"])  # Fixed random.choices() issue

                if action == "attack":
                    damage = enemy.attack_target(player, player.get_race())
                    message = f"Villain attacks! Deals {damage} damage!"

                elif action == "move" and affordable_moves:
                    move_index = random.choice(affordable_moves)
                    print(f"Villain used move index {move_index}")  # Debug
                    move_name, damage, atk_type = enemy.use_move(move_index, player, player.get_race())
                    message = f"Villain used {move_name}! Deals {damage} damage!"

                elif action == "leg_action" and affordable_leg_moves and enemy.get_leg_actions() > 0:
                    move_index = random.choice(affordable_leg_moves)
                    move_name, damage, atk_type = enemy.use_move(move_index, player, player.get_race())
                    message = f"Villain used {move_name}! Deals {damage} damage!"

                elif affordable_moves:  # Fallback to a normal move if leg action fails
                    move_index = random.choice(affordable_moves)
                    move_name, damage, atk_type = enemy.use_move(move_index, player, player.get_race())
                    message = f"Villain used {move_name}! Deals {damage} damage!"

            else:  # Normal AI
                if enemy.get_hp() < player.get_hp():
                    action = random.choice(["attack", "move"])
                elif enemy.get_hp() > player.get_hp():
                    action = "move"
                else:
                    action = random.choice(["attack", "defend", "move"])  # Fixed random.choices()

                if action == "attack":
                    damage = enemy.attack_target(player, player.get_race())
                    message = f"Villain attacks! Deals {damage} damage!"

                elif action == "move" and affordable_moves:
                    move_index = random.choice(affordable_moves)
                    move_name, damage, atk_type = enemy.use_move(move_index, player, player.get_race())
                    # print(f"Villain used move index {move_index}")  # Debug
                    print(f"Villain used {move_name} for {damage} {atk_type} damage!")
                    message = f"Villain used {move_name}! Deals {damage} {atk_type} damage!"

                elif action == "defend":
                    enemy.set_defending(True)
                    message = "Villain is defending!"

            # Check for game end
            if player.get_hp() <= 0:
                message = "Villain Wins!"
                screen.fill(WHITE)
                victory_text = font.render("Villain Wins!", True, (255, 0, 0))
                screen.blit(victory_text, (300, 250))
                pygame.display.flip()
                pygame.time.delay(3000)
                game_over = True

            elif enemy.get_hp() <= 0:
                message = "Hero Wins!"
                screen.fill(WHITE)
                victory_text = font.render("Hero Wins!", True, (0, 255, 0))
                screen.blit(victory_text, (300, 250))
                pygame.display.flip()
                pygame.time.delay(3000)
                game_over = True

            if not game_over:
                enemy.regen_energy()  # Regenerate energy if the game isn't over
                turn = "player"  # Switch turn back to player

    # Display messages
    msg_text = font.render(message, True, BLACK)
    screen.blit(msg_text, (WIDTH // 2 - 150, HEIGHT - 100))
    draw_move_options()  # Display move choices

    pygame.display.flip()  # Update screen
    clock.tick(30)  # Limit FPS

if game_over:
    pygame.quit()
    sys.exit()
