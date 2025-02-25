import pygame
import random


class Character:
    def __init__(self, race, name, attack_type, max_hp, hp, attack, spattack, defense, spdefense, max_energy, energy, energy_regen, moves, sprite_path, x, y):
        self.race = race
        self.name = name
        self.attack_type = attack_type
        self.maxhp = max_hp
        self.hp = hp
        self.attack = attack  # Physical damage
        self.spattack = spattack  # Spell damage
        self.defense = defense  # Physical defense
        self.spdefense = spdefense  # Spell defense
        self.max_energy = max_energy  # Maximum energy
        self.energy = energy  # Current energy
        self.energy_regen = energy_regen  # Energy regenerated every turn

        # Load the sprite image
        self.sprite = pygame.image.load(sprite_path).convert_alpha()  # Load with transparency
        self.x, self.y = x, y  # Selected position of character
        self.is_defending = False

        # Moveset (list of dictionaries)
        self.moves = moves

    def use_move(self, move_index, enemy, race):
        """Execute a move if enough energy is available."""
        weakness = False
        move = self.moves[move_index]
        if self.energy >= move["energy_cost"]:
            self.energy -= move["energy_cost"]  # Reduce energy
            if self.attack_type == "Hamon" and race == "Vampire":
                weakness = True
                damage = max(5, self.attack + move["damage"] + random.randint(-3, 3)) * 3
            elif self.attack_type == "Vampirism" and race == "Human":
                weakness = True
                damage = (5, self.attack + move["damage"] + random.randint(-3, 3))
            else:
                damage = max(5, self.attack + move["damage"] + random.randint(-3, 3))
            enemy.take_damage(damage, weakness)
            return move["name"], damage
        else:
            return "Not enough energy!", 0  # Not enough energy warning

    def regen_energy(self):
        """Regenerate energy at the end of the turn."""
        self.energy = min(self.max_energy, self.energy + self.energy_regen)  # Capped at max

    def take_damage(self, damage, weakness=False):
        """Reduce HP and check for defeat."""
        if self.is_defending and weakness is not True:
            damage = int(damage * 0.5)  # Reduce damage by 50% when defending
        elif self.is_defending and weakness is True:
            damage = int(damage)
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0  # Ensure HP doesn't go negative
        self.is_defending = False  # Reset defense after turn

    def attack_target(self, enemy, race):
        weakness = False

        if self.attack_type == "Hamon" and race == "Vampire":
            weakness = True
            damage = max(5, self.attack + random.randint(-3, 3)) * 2.5

        elif self.attack_type == "Vampirism" and race == "Human":
            weakness = True
            damage = max(5, self.attack + random.randint(-3, 3)) * 1.5

        else:
            damage = max(5, self.attack + random.randint(-3, 3))

        enemy.take_damage(damage, weakness)
        return damage  # Return damage dealt

    def is_alive(self):
        return self.hp > 0

    def draw(self, screen):
        """Draw the fighter's sprite on the screen."""
        screen.blit(self.sprite, (self.x, self.y))  # Display the sprite at its position


class BossCharacter(Character):
    def __init__(self, race, name, attack_type, max_hp, hp, attack, spattack, defense, spdefense, max_energy, energy, energy_regen, moves, leg_resistances, leg_actions,
                 sprite_path, x, y):

        super().__init__(race, name, attack_type, max_hp, hp, attack, spattack, defense, spdefense, max_energy, energy, energy_regen,
                         moves, sprite_path, x, y)

        # Unique Boss Characteristics
        self.leg_resistances = leg_resistances
        self.leg_actions = leg_actions
