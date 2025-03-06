import os
import pygame
import random


class Character:
    def __init__(self, race, name, combat_style, max_hp, hp, attack, spattack, defense, spdefense, max_energy, energy, energy_regen, moves, sprite_path, x, y):
        self.__race = race
        self.__name = name
        self.__combat_style = combat_style
        self.__max_hp = max_hp
        self.__hp = hp
        self.__attack = attack
        self.__spattack = spattack
        self.__defense = defense
        self.__spdefense = spdefense
        self.__max_energy = max_energy
        self.__energy = energy
        self.__energy_regen = energy_regen
        self.__x, self.__y = x, y

        # Moveset
        self.__moves = moves
        self.__is_defending = False

        # Default sprite path
        default_sprite_path = "assets/sprites/hero_blank.png"

        # Use provided sprite path or fall back to default
        if sprite_path and os.path.exists(sprite_path):
            self.__sprite = pygame.image.load(sprite_path).convert_alpha()
        else:
            print(f"Warning: Sprite '{sprite_path}' not found! Using default sprite.")
            self.__sprite = pygame.image.load(default_sprite_path).convert_alpha()

    # Getters for private attributes
    def get_race(self):
        return self.__race

    def get_name(self):
        return self.__name

    def get_combat_style(self):
        return self.__combat_style

    def get_max_hp(self):
        return self.__max_hp

    def get_hp(self):
        return self.__hp

    def set_hp(self, value):
        self.__hp = max(0, min(value, self.__max_hp))  # Clamp between 0 and max_hp

    def get_hp_comp(self):
        return {"hp": self.__hp, "maxhp": self.__max_hp}

    def get_attack(self):
        return self.__attack

    def get_spattack(self):
        return self.__spattack

    def get_defense(self):
        return self.__defense

    def get_spdefense(self):
        return self.__spdefense

    def get_max_energy(self):
        return self.__max_energy

    def get_energy(self):
        return self.__energy

    def set_energy(self, value):
        self.__energy = max(0, min(value, self.__max_energy))  # Clamp between 0 and max_energy

    def get_energy_regen(self):
        return self.__energy_regen

    def get_moves(self):
        return self.__moves

    def get_move_name(self, index):
        move = self.__moves[index]
        return move["name"]

    def get_move(self, index):
        move = self.__moves[index]
        return move["name"], move["damage"], move["energy_cost"], move["type"]

    def get_sprite(self):
        return self.__sprite

    def get_position(self):
        return self.__x, self.__y

    def get_defending(self):
        return self.__is_defending

    def set_defending(self, value: bool):
        self.__is_defending = value

    def use_move(self, move_index, enemy, race):
        """Execute a move if enough energy is available."""
        name, damage, cost, atk_type = self.get_move(move_index)
        if self.__energy >= cost:
            self.__energy -= cost  # Reduce energy
            if self.__combat_style == "Hamon" and race == "Vampire":
                damage = int(max(5, self.__attack + damage + random.randint(-3, 8)))
            elif self.__combat_style == "Vampirism" and race == "Human":
                damage = int(max(5, self.__attack + damage + random.randint(-3, 4)))
            elif self.__race == "Cambion":
                damage = int(max(5, self.__attack + damage + random.randint(-3, 6)) + 5)
            else:
                damage = int(max(5, self.__attack + damage + random.randint(-3, 3)))
            enemy.take_damage(damage, damage)
            print(f"Returning {name}, {damage}, {atk_type}")
            return name, damage, atk_type
        else:
            return "Not enough energy!", 0, None  # Not enough energy warning

    def regen_energy(self):
        """Regenerate energy at the end of the turn."""
        self.__energy = min(self.__max_energy, self.__energy + self.__energy_regen)

    def take_damage(self, damage, atk_type):
        """Reduce HP and check for defeat."""
        damage = int(damage)  # Ensure it's an integer

        if self.__race == "Cambion":  # Check race to identify weaknesses and resistances
            if atk_type == "MAG":  # Check for Magic immunity
                damage = 0  # If the immunity applies, negate the damage taken
                print(f"{self.__name} was immune to the {atk_type} attack! {damage} damage taken... HP left: {self.__hp}")

            elif atk_type == "HAM":  # Check for Hamon weakness
                damage = int(damage * 1.5)
                print(
                    f"{self.__name} was hurt more than normal due to the {atk_type} attack! {damage} damage taken! HP left: {self.__hp}")

            elif atk_type == "RAD":  # Check for Radiant weakness
                damage = int(damage * 2.5)  # If the weakness applies, increase damage by 250%
                print(f"{self.__name} was weak to the {atk_type} attack! {damage} damage taken! HP left: {self.__hp}")

            else:  # If no weaknesses or resistances are identified, resort to default damage.
                print(f"{self.__name} takes {damage} damage! HP left: {self.__hp}")

        elif self.__race == "Vampire":  # Check race to identify weaknesses and resistances
            if atk_type == "HAM":  # Check for Hamon weakness
                damage = int(damage * 3)
                print(f"{self.__name} was weak to the {atk_type} attack! {damage} damage taken! HP left: {self.__hp}")

            elif atk_type == "RAD":  # Check for Radiant weakness
                damage = int(damage * 6)
                print(
                    f"{self.__name} was extremely weak to the {atk_type} attack! {damage} damage taken! HP left: {self.__hp}")

        elif self.__race == "Human":
            if atk_type == "MAG":
                damage = int(damage * 2.5)
                print(f"{self.__name} was weak to the {atk_type} attack! {damage} damage taken! HP left: {self.__hp}")

            elif atk_type == "VMP":
                damage = int(damage * 1.5)
                print(
                    f"{self.__name} was hurt more than normal due to the {atk_type} attack! {damage} damage taken! HP left: {self.__hp}")

        else:
            damage = max(5, self.__attack + random.randint(-3, 3))
            print(f"{self.__name} takes {damage} damage! HP left: {self.__hp}")

        self.__hp = max(0, self.__hp - damage)  # Prevent negative HP
        self.__is_defending = False  # Reset defense after turn

    def attack_target(self, enemy, race):
        damage = int(max(5, self.__attack + random.randint(-10, 10)))
        enemy.take_damage(damage, self.__combat_style)
        return damage

    def is_alive(self):
        return self.__hp > 0

    def draw(self, screen):
        """Draw the fighter's sprite on the screen."""
        screen.blit(self.__sprite, (self.__x, self.__y))


class BossCharacter(Character):
    def __init__(self, race, name, title, combat_style, max_hp, hp, attack, spattack, defense, spdefense, max_energy, energy, energy_regen, moves, leg_resistances: int, leg_actions: int, leg_moves: list,
                 sprite_path, x, y):

        super().__init__(race, name, combat_style, max_hp, hp, attack, spattack, defense, spdefense, max_energy, energy, energy_regen,
                         moves, sprite_path, x, y)

        # Unique Boss Characteristics
        self.__title = title
        self.__leg_resistances = leg_resistances
        self.__leg_actions = leg_actions
        self.__leg_moves = leg_moves

    # Getters for private attributes
    def get_title(self):
        return self.__title

    def get_leg_resistances(self):
        return self.__leg_resistances

    def get_leg_actions(self):
        return self.__leg_actions

    def get_leg_moves(self):
        return self.__leg_moves


class MagicalBeing(Character):
    def __init__(self, name, race, combat_style, magic_level, max_hp, hp, attack, spattack, defense, spdefense,
                 max_energy, energy, energy_regen, moves, sprite_path, x, y):
        self.__magic_level = magic_level
        super().__init__(race, name, combat_style, max_hp, hp, attack, spattack, defense, spdefense, max_energy, energy,
                         energy_regen, moves, sprite_path, x, y)

    # Getter for magic level
    def get_magic_level(self):
        return self.__magic_level

    def attack_target(self, enemy, race):
        if race != "Cambion":
            damage = int(max(5, self.get_attack() + random.randint(-3, 3)) * 1.25 + self.__magic_level // 2)
        else:
            damage = 1
        enemy.take_damage(damage, "MAG")
        return damage  # Return damage dealt
