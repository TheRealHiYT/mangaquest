import pygame
import random
import os


class Character:
    def __init__(self, race, name, combat_style, max_hp, hp, attack, spattack, defense, spdefense, max_energy, energy, energy_regen, moves, sprite_path, x, y):
        self.race = race
        self.name = name
        self.combat_style = combat_style
        self.maxhp = max_hp
        self.hp = hp
        self.attack = attack
        self.spattack = spattack
        self.defense = defense
        self.spdefense = spdefense
        self.max_energy = max_energy
        self.energy = energy
        self.energy_regen = energy_regen
        self.x, self.y = x, y

        # Moveset
        self.moves = moves
        self.is_defending = False

        # Default sprite path
        default_sprite_path = "assets/sprites/hero_blank.png"

        # Use provided sprite path or fall back to default
        if sprite_path and os.path.exists(sprite_path):
            self.sprite = pygame.image.load(sprite_path).convert_alpha()
        else:
            print(f"Warning: Sprite '{sprite_path}' not found! Using default sprite.")
            self.sprite = pygame.image.load(default_sprite_path).convert_alpha()

    def use_move(self, move_index, enemy, race):
        """Execute a move if enough energy is available."""
        move = self.moves[move_index]
        if self.energy >= move["energy_cost"]:
            self.energy -= move["energy_cost"]  # Reduce energy
            if self.combat_style == "Hamon" and race == "Vampire":
                damage = int(max(5, self.attack + move["damage"] + random.randint(-3, 3)) * 3)
            elif self.combat_style == "Vampirism" and race == "Human":
                damage = int(max(5, self.attack + move["damage"] + random.randint(-3, 3)) * 1.5)
            elif self.race == "Cambion":
                damage = int(max((5, self.attack + move["damage"] + random.randint(-3, 3)) * 2) + 5)
            else:
                damage = int(max(5, self.attack + move["damage"] + random.randint(-3, 3)))
            enemy.take_damage(damage, move["type"])
            return move["name"], damage
        else:
            return "Not enough energy!", 0  # Not enough energy warning

    def regen_energy(self):
        """Regenerate energy at the end of the turn."""
        self.energy = min(self.max_energy, self.energy + self.energy_regen)  # Capped at max

    def take_damage(self, damage, atk_type):
        """Reduce HP and check for defeat."""
        damage = int(damage)  # Ensure it's an integer

        if self.race == "Cambion":  # Check race to identify weaknesses and resistances
            if atk_type == "MAG":  # Check for Magic immunity
                damage = 0  # If the immunity applies, negate the damage taken
                print(f"{self.name} was immune to the {atk_type} attack! {damage} damage taken... HP left: {self.hp}")

            elif atk_type == "HAM":  # Check for Hamon weakness
                damage = int(damage * 1.5)
                print(f"{self.name} was hurt more than normal due to the {atk_type} attack! {damage} damage taken! HP left: {self.hp}")

            elif atk_type == "RAD":  # Check for Radiant weakness
                damage = int(damage * 2.5)  # If the weakness applies, increase damage by 250%
                print(f"{self.name} was weak to the {atk_type} attack! {damage} damage taken! HP left: {self.hp}")

            else:  # If no weaknesses or resistances are identified, resort to default damage.
                print(f"{self.name} takes {damage} damage! HP left: {self.hp}")

        elif self.race == "Vampire":  # Check race to identify weaknesses and resistances
            if atk_type == "HAM":  # Check for Hamon weakness
                damage = int(damage * 3)
                print(f"{self.name} was weak to the {atk_type} attack! {damage} damage taken! HP left: {self.hp}")

            elif atk_type == "RAD":  # Check for Radiant weakness
                damage = int(damage * 6)
                print(f"{self.name} was extremely weak to the {atk_type} attack! {damage} damage taken! HP left: {self.hp}")

        elif self.race == "Human" and atk_type == "VMP":
            damage = max(5, self.attack + random.randint(-3, 3)) * 1.5
            print(f"{self.name} was hurt more than normal due to the {atk_type} attack! {damage} damage taken! HP left: {self.hp}")

        else:
            damage = max(5, self.attack + random.randint(-3, 3))
            print(f"{self.name} takes {damage} damage! HP left: {self.hp}")

        self.hp = max(0, self.hp - damage)  # Prevent negative HP
        self.is_defending = False  # Reset defense after turn

    def attack_target(self, enemy, race):
        damage = int(max(5, self.attack + random.randint(-10, 10)))

        enemy.take_damage(damage, self.combat_style)
        return damage  # Return damage dealt

    def is_alive(self):
        return self.hp > 0

    def draw(self, screen):
        """Draw the fighter's sprite on the screen."""
        screen.blit(self.sprite, (self.x, self.y))  # Display the sprite at its position


class BossCharacter(Character):
    def __init__(self, race, name, combat_style, max_hp, hp, attack, spattack, defense, spdefense, max_energy, energy, energy_regen, moves, leg_resistances, leg_actions,
                 sprite_path, x, y):

        super().__init__(race, name, combat_style, max_hp, hp, attack, spattack, defense, spdefense, max_energy, energy, energy_regen,
                         moves, sprite_path, x, y)

        # Unique Boss Characteristics
        self.leg_resistances = leg_resistances
        self.leg_actions = leg_actions


class MagicalBeing(Character):
    def __init__(self, name, race, combat_style, magic_level, max_hp, hp, attack, spattack, defense, spdefense,
                 max_energy, energy, energy_regen, moves, sprite_path, x, y):
        self.magic_level = magic_level
        super().__init__(race, name, combat_style, max_hp, hp, attack, spattack, defense, spdefense, max_energy, energy,
                         energy_regen, moves, sprite_path, x, y)

    def attack_target(self, enemy, race):
        if race != "Cambion":
            damage = int(max(5, self.attack + random.randint(-3, 3)) * 1.25 + self.magic_level//2)
        else:
            damage = 1
        enemy.take_damage(damage, "MAG")
        return damage  # Return damage dealt
