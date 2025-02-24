import pygame
import json
import sys
import subprocess

pygame.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Custom Fighter Menu")

# Colors & Font
WHITE, BLACK, GREEN = (255, 255, 255), (0, 0, 0), (0, 255, 0)
font = pygame.font.Font(None, 36)

# Fighter list
fighters_file = "fighters.json"
selected_fighter_file = "selected_fighter.json"


# Load saved fighters
def load_fighters():
    try:
        with open(fighters_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# Save the selected fighter
def save_selected_fighter(fighter):
    with open(selected_fighter_file, "w") as file:
        json.dump(fighter, file, indent=4)


# Fighter selection menu
def fighter_menu():
    fighters = load_fighters()
    if not fighters:
        print("No fighters available! Create one first.")
        return None

    selected_index = 0
    running = True

    while running:
        screen.fill(WHITE)
        title_text = font.render("Select Your Fighter", True, BLACK)
        screen.blit(title_text, (300, 50))

        y_offset = 100
        for i, (name, fighter) in enumerate(fighters.items()):
            color = GREEN if i == selected_index else BLACK
            text = font.render(f"{i+1}. {name} (HP: {fighter['hp']})", True, color)
            screen.blit(text, (250, y_offset + i * 40))

        instructions = font.render("Use Up/Down to Select, Enter to Confirm", True, BLACK)
        screen.blit(instructions, (200, 500))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(fighters)
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(fighters)
                elif event.key == pygame.K_RETURN:
                    selected_fighter = list(fighters.values())[selected_index]
                    save_selected_fighter(selected_fighter)
                    return selected_fighter


# Run the menu and save selection
if __name__ == "__main__":
    chosen_fighter = fighter_menu()
    if chosen_fighter:
        print(f"Selected Fighter: {chosen_fighter['name']}")
        print("Starting game...")
        pygame.quit()
        subprocess.run(["python", "main.py"])  # Start the game
        sys.exit()
