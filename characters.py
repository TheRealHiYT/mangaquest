import pygame
import random


class Character:
    def __init__(self, name, max_hp, hp, attack, spattack, defense, spdefense, max_energy, energy, energy_regen, moves, sprite_path, x, y):
        self.name = name
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

    def use_move(self, move_index, enemy):
        """Execute a move if enough energy is available."""
        move = self.moves[move_index]
        if self.energy >= move["energy_cost"]:
            self.energy -= move["energy_cost"]  # Reduce energy
            damage = max(5, self.attack + move["damage"] + random.randint(-3, 3))
            enemy.take_damage(damage)
            return move["name"], damage
        else:
            return "Not enough energy!", 0  # Not enough energy message

    def regen_energy(self):
        """Regenerate energy at the end of the turn."""
        self.energy = min(self.max_energy, self.energy + self.energy_regen)  # Capped at max

    def take_damage(self, damage):
        if self.is_defending:
            damage = int(damage * 0.5)  # Reduce damage by 50% when defending
        self.hp -= max(0, damage - self.defense)  # Reduce HP but not below 0
        if self.hp < 0:
            self.hp = 0
        self.is_defending = False  # Reset defense after turn

    def melee_target(self, enemy):
        damage = max(5, self.attack + random.randint(-3, 3))  # Randomized attack power
        enemy.take_damage(damage)
        return damage  # Return damage dealt

    def is_alive(self):
        return self.hp > 0

    def draw(self, screen):
        """Draw the fighter's sprite on the screen."""
        screen.blit(self.sprite, (self.x, self.y))  # Display the sprite at its position
