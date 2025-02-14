import pygame
import random


class Character:
    def __init__(self, name, maxhp, hp, attack, spattack, defense, spdefense, stamina, mana, sprite_path, x, y):
        self.name = name
        self.maxhp = maxhp
        self.hp = hp
        self.attack = attack  # Physical damage
        self.spattack = spattack  # Spell damage
        self.defense = defense  # Physical defense
        self.spdefense = spdefense  # Spell defense
        self.stamina = stamina  # Energy consumed by techniques
        self.mana = mana  # Energy consumed by spells

        # Load the sprite image
        self.sprite = pygame.image.load(sprite_path).convert_alpha()  # Load with transparency
        self.x, self.y = x, y  # Selected position of character
        self.is_defending = False

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
