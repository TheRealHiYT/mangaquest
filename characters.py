import os
import random

import pygame


class EnemyGen:

    def __init__(self, race_list):
        self.enemy_type = enemy_type = random.choice(race_list)

    def gen_enemy(self, multi=1):
        if self.enemy_type == "Hamon User":
            enemy, json = self.gen_hamon(multi)

            return enemy, json

        elif self.enemy_type == "Vampire":
            enemy, json = self.gen_vampire(multi)

            return enemy, json

    @staticmethod
    def gen_vampire(multi):
        beta_char = {
            "race": "Vampire",
            "name": f"{random.choice(['Enrico', 'Straizo', 'Vanilla'])} {random.choice(['Brando', 'Pucci', 'Ice'])}",
            "combat_style": "Vampirism",
            "hp": random.randint(450, 750),
            "attack": random.randint(25, 90),
            "spattack": random.randint(35, 115),
            "defense": random.randint(30, 115),
            "spdefense": random.randint(15, 90),
            "energy": random.randint(50, 140),
            "regen": random.randint(5, 20),
            "moves": [
                {"name": "Superhuman Barrage", "damage": 15, "energy_cost": random.randint(5, 15),
                 "type": "VMP"},
                {"name": "Bloodsuck", "damage": 20, "energy_cost": random.randint(10, 20),
                 "type": "VMP"},
                {"name": "Vaporization Freeze", "damage": 30, "energy_cost": random.randint(15, 25),
                 "type": "VAM"},
                {"name": "Space Ripper Stingy Eyes", "damage": 45,
                 "energy_cost": random.randint(25, 35), "type": "PHY"}
            ],
            "sprite": None
        }

        enemy = Character(beta_char['race'], beta_char['name'], beta_char['combat_style'], beta_char['hp'],
                          beta_char['hp'], beta_char['attack'], beta_char['spattack'], beta_char['defense'],
                          beta_char['spdefense'], beta_char['energy'], beta_char['energy'], beta_char['regen'],
                          beta_char['moves'], beta_char["sprite"], x=450, y=300)
        return enemy, beta_char

    @staticmethod
    def gen_hamon(multi):
        beta_char = {
            "race": "Hamon User",
            "name": f"{random.choice(['Toregall', 'Lisa', 'Ball', 'Koopall'])} {random.choice(['Allstar', 'Lisa', 'Smith', 'Rallstar'])}",
            "combat_style": "Hamon",
            "hp": random.randint(200, 750) * multi,
            "attack": random.randint(15, 90) * multi,
            "spattack": random.randint(35, 115) * multi,
            "defense": random.randint(30, 115) * multi,
            "spdefense": random.randint(15, 90) * multi,
            "energy": random.randint(60, 160) * multi,
            "regen": random.randint(10, 25) * multi,
            "moves": [
                {"name": "Hamon Overdrive", "damage": 20, "energy_cost": random.randint(15, 25), "type": "HAM"},
                {"name": "Zoom Punch", "damage": random.randint(20, 30), "energy_cost": random.randint(20, 30),
                 "type": "HAM"},
                {"name": "Metal Silver Overdrive", "damage": random.randint(15, 60),
                 "energy_cost": random.randint(30, 50)},
                {"name": "Sunlight Yellow Overdrive", "damage": random.randint(25, 80),
                 "energy_cost": random.randint(50, 125)}
            ],
            "sprite": None
        }

        enemy = Character(beta_char['race'], beta_char['name'], beta_char['combat_style'], beta_char['hp'],
                          beta_char['hp'], beta_char['attack'], beta_char['spattack'], beta_char['defense'],
                          beta_char['spdefense'], beta_char['energy'], beta_char['energy'], beta_char['regen'],
                          beta_char['moves'], beta_char["sprite"], x=450, y=300)
        return enemy, beta_char


class BossGen:
    def __init__(self, race_list):
        self.enemy_type = enemy_type = random.choice(race_list)

    def gen_boss(self, multi):
        char_race = self.enemy_type
        if char_race == "Human":
            boss_style = "Cursed Arts"
        elif char_race == "Hamon User":
            boss_style = "Hamon"
            boss_moves = [
                {"name": "Zoom Punch", "damage": 45, "energy_cost": 20, "type": "HAM"},
                {"name": "Scarlet Overdrive", "damage": 70, "energy_cost": 40, "type": "HAM"},
                {"name": "Metal Silver Overdrive", "damage": 90, "energy_cost": 65, "type": "HAM"},
                {"name": "Sunlight Yellow Overdrive", "damage": 140, "energy_cost": 100, "type": "RAD"}
            ]
            boss_actions = [
                {"name": "!Ultimate Skill! Crimson Bubble Overdrive!!", "damage": 999, "energy_cost": 200,
                 "type": "RAD"}
            ]
        elif char_race == "Vampire":
            boss_style = "Vampirism"
            boss_moves = [
                {"name": "MUDA!", "damage": 20, "energy_cost": 10, "type": "MAG"},
                {"name": "MUDA Barrage", "damage": 50, "energy_cost": 35, "type": "MAG"},
                {"name": "Impale", "damage": 35, "energy_cost": 25, "type": "MAG"},
                {"name": "Timestop Impale", "damage": 100, "energy_cost": 75, "type": "PHY"}
            ]
            boss_actions = [
                {"name": "!Ultimate Skill! Checkmate!", "damage": 360, "energy_cost": 50, "leg_cost": 1, "type": "PHY"},
                {"name": "!Ultimate Skill! ROAD ROLLER!!", "damage": 520, "energy_cost": 75, "leg_cost": 2, "type": "PHY"}
            ]
        elif char_race == "Cambion":
            boss_style = "Devil Arms"
        else:
            boss_style = "MMA"
            boss_moves = [
                {"name": "Quick Jab", "damage": random.randint(55, 90), "energy_cost": random.randint(20, 40),
                 "type": "PHY"},
                {"name": "Liver Blow", "damage": random.randint(65, 115), "energy_cost": random.randint(20, 55),
                 "type": "PHY"},
                {"name": "Uppercut", "damage": random.randint(80, 140), "energy_cost": random.randint(20, 85),
                 "type": "PHY"},
                {"name": "Right Hook", "damage": random.randint(85, 150), "energy_cost": random.randint(20, 110),
                 "type": "PHY"}
            ]
            boss_actions = [
                {"name": "!Ultimate Skill! Eye Jab!", "damage": random.randint(110, 180),
                 "energy_cost": random.randint(10, 55), "leg_cost": 1, "type": "PHY"}]

        leg_actions = random.randint(1, 4) * multi
        leg_resistances = random.randint(1, 5) * multi
        regen = random.randint(30, 75) * multi
        energy = random.randint(115, 600) * multi
        spdefense = random.randint(120, 255) * multi
        defense = random.randint(120, 255) * multi
        spattack = random.randint(135, 300) * multi
        attack = random.randint(135, 300) * multi
        hp = random.randint(950, 3500) * multi
        name = f'{random.choice(["Dio", "Jonathan", "Alice", "Allegore", "Enrico", "Dante", "Vergil", "Ruby"])} {random.choice(["Brando", "Joestar", "Allstar", "Brawlstar", "Pucci", "Sparda", "Rose"])}'

        beta_char = {
            "race": char_race,
            "name": name,
            "combat_style": boss_style,
            "max_hp": hp,
            "hp": hp,
            "attack": attack,
            "spattack": spattack,
            "defense": defense,
            "spdefense": spdefense,
            "max_energy": energy,
            "energy": energy,
            "regen": regen,
            "moves": boss_moves,
            "leg_resistances": leg_resistances,
            "leg_actions": leg_actions,
            "leg_moves": boss_actions,
            "sprite": "assets/sprites/enemy_blank.png",
            "x": 450,
            "y": 300
        }

        return BossCharacter(
            race=char_race,
            name=name,
            combat_style=boss_style,
            max_hp=hp,
            hp=hp,
            attack=attack,
            spattack=spattack,
            defense=defense,
            spdefense=spdefense,
            max_energy=energy,
            energy=energy,
            energy_regen=regen,
            moves=boss_moves,
            leg_resistances=leg_resistances,
            leg_actions=leg_actions,
            leg_moves=boss_actions,
            sprite_path="assets/sprites/enemy_blank.png",  # Use default if missing
            x=450,
            y=300
        ), beta_char


def give_healing(target, value, heal_type):
    val = int(value)

    if heal_type == "HAM":
        val = val * 2.5
        target.recieve_healing(val)


class Character:
    def __init__(self, race, name, combat_style, max_hp, hp, attack, spattack, defense, spdefense, max_energy, energy,
                 energy_regen, moves, sprite_path, x, y):
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
            elif self.combat_style == "Vampirism" and race != "Hamon User" or "Angel":
                damage = int(max(5, self.attack + move["damage"] + random.randint(-3, 3)) * 1.5)
                self.recieve_healing(damage // 2)
                print(f"{self.name} healed {damage // 2} HP due to being a Vampire!")
            elif self.race == "Cambion" and race != "Angel":
                damage = int(max((5, self.attack + move["damage"] + random.randint(-3, 3)) * 2) + 5)
            else:
                damage = int(max(5, self.attack + move["damage"] + random.randint(-3, 3)))
            enemy.take_damage(damage, move["type"])
            return move["name"], damage
        else:
            return "Not enough energy!", 0  # Not enough energy warning

    def recieve_healing(self, value):
        val = int(value)
        self.hp = min(self.maxhp, self.hp + val)
        return val

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
                print(
                    f"{self.name} was hurt more than normal due to the {atk_type} attack! {damage} damage taken! HP left: {self.hp}")

            elif atk_type == "RAD":  # Check for Radiant weakness
                damage = int(damage * 2.5)  # If the weakness applies, increase damage by 250%
                print(f"{self.name} was weak to the {atk_type} attack! {damage} damage taken! HP left: {self.hp}")

            else:  # If no weaknesses or resistances are identified, resort to default damage.
                print(f"{self.name} takes {damage} damage! HP left: {self.hp}")

        elif self.race == "Vampire":  # Check race to identify weaknesses and resistances
            if atk_type == "HAM":  # Check for Hamon weakness
                damage = int(damage * 2)
                print(f"{self.name} was weak to the {atk_type} attack! {damage} damage taken! HP left: {self.hp}")

            elif atk_type == "RAD":  # Check for Radiant weakness
                damage = int(damage * 6)
                print(
                    f"{self.name} was extremely weak to the {atk_type} attack! {damage} damage taken! HP left: {self.hp}")

            else:  # If no weaknesses or resistances are identified, resort to default damage.'
                print(f"{self.name} takes {damage} damage!")

        elif self.race == "Human" and atk_type == "VMP":
            damage = max(5, self.attack + random.randint(-3, 3)) * 1.5
            print(
                f"{self.name} takes {damage} damage! Due to being a Vampire, {self.name} heals {damage // 2} HP! HP left: {self.hp}")
            print(
                f"{self.name} was hurt more than normal due to the {atk_type} attack! {damage} damage taken! HP left: {self.hp}")

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
    def __init__(self, race, name, combat_style, max_hp, hp, attack, spattack, defense, spdefense, max_energy, energy,
                 energy_regen, moves, leg_resistances, leg_actions, leg_moves,
                 sprite_path, x, y):
        super().__init__(race, name, combat_style, max_hp, hp, attack, spattack, defense, spdefense, max_energy, energy,
                         energy_regen,
                         moves, sprite_path, x, y)

        # Unique Boss Characteristics
        self.leg_resistances = leg_resistances
        self.leg_actions = leg_actions
        self.leg_moves = leg_moves

    # Unique Boss Functions
    def leg_move(self, move_index, enemy, race):
        """Use a Legendary Action if enough uses are available."""
        move = self.leg_moves[move_index]
        if self.energy >= move["energy_cost"] and self.leg_actions >= move["leg_cost"]:
            self.energy -= move["energy_cost"]  # Reduce energy
            self.leg_actions -= move["leg_cost"]  # Reduce legendary actions

            # Search for weaknesses/strengths
            if self.combat_style == "Hamon" and race == "Vampire":
                damage = int(max(5, self.attack + move["damage"] + random.randint(-3, 3)) * 3)
            elif self.combat_style == "Vampirism" and race != "Hamon User" or "Angel":
                damage = int(max(5, self.attack + move["damage"] + random.randint(-3, 3)) * 1.5)
                self.recieve_healing(damage // 2)
                print(f"{self.name} healed {damage // 2} HP due to being a Vampire!")
            elif self.race == "Cambion" and race != "Angel":
                damage = int(max((5, self.attack + move["damage"] + random.randint(-3, 3)) * 2) + 5)
            else:
                damage = int(max(5, self.attack + move["damage"] + random.randint(-3, 3)))
            enemy.take_damage(damage, move["type"])
            return move["name"], damage
        else:
            return "Not enough energy!", 0  # Not enough energy warning


class MagicalBeing(Character):
    def __init__(self, name, race, combat_style, magic_level, max_hp, hp, attack, spattack, defense, spdefense,
                 max_energy, energy, energy_regen, moves, sprite_path, x, y):
        self.magic_level = magic_level
        super().__init__(race, name, combat_style, max_hp, hp, attack, spattack, defense, spdefense, max_energy, energy,
                         energy_regen, moves, sprite_path, x, y)

    def attack_target(self, enemy, race):
        if race != "Cambion":
            damage = int(max(5, self.attack + random.randint(-3, 3)) * 1.25 + self.magic_level // 2)
        else:
            damage = 1
        enemy.take_damage(damage, "MAG")
        return damage  # Return damage dealt
