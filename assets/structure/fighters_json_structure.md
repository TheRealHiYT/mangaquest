###So you want to learn the character structure? Alright, first, let's look at the file.

<p style="color:green">fighters.json</p>

```json
{
  "Alice Allstar": {
    "race": "Human",
    "name": "Alice Allstar",
    "attack_type": "Hamon",
    "max_hp": 450,
    "hp": 450,
    "attack": 70,
    "spattack": 125,
    "defense": 55,
    "spdefense": 45,
    "max_energy": 60,
    "energy": 60,
    "energy_regen": 10,
    "moves": [
        {
            "name": "Scarf Trip",
            "damage": 15,
            "energy_cost": 5
        },
        {
            "name": "Scarf Blade",
            "damage": 25,
            "energy_cost": 15
        },
        {
            "name": "Hamon Wrap",
            "damage": 35,
            "energy_cost": 25
        }
    ],
    "sprite": "assets/sprites/hero_blank.png"
  }
}
```

###Now that we've looked at the file, let's look at how to create a new character.

#### Note: This is in plain text.

```text
  "Alice Allstar: {      # Defines Character and opens the attribute list
    "race": "Human",     # Defines the character's species
    "name": "Alice Allstar",      # Defines the character's name
    "attack_type": "Hamon",       # Defines what the character attacks with. Used for weaknesses.
    "max_hp": 450,                  # Sets the maximum health points of a character.
    "hp": 450,                      # Defines the current health points of a character. Cannot be edited during runtime.
    "attack": 70,                   # Measures how well a character can use their brawn. Used for physical attacks.
    "spattack": 125,                # Measures a character's strength with non-physical attacks (ex. burning someone via body heat).
    "defense": 55,                  # Gauges how well a character can defend against physical blows.
    "spdefense": 45,                # Gauges how well a character can defend against non-physical attacks, such as being frozen.
    "max_energy": 60,               # Describes the amount of moves a character can throw out before getting tired. 
    "energy": 60,                   # Defines the current energy of a character. Drained by the energy cost of moves.
    "energy_regen": 10,             # Measures how fast a character regains their energy. Increases energy by this after every turn.
    "moves": [                      # Movelist
        {
            "name": "Scarf Trip",   # Name of the move
            "damage": 15,           # The damage the move does
            "energy_cost": 5        # Energy cost of the move
        },
        {
            "name": "Scarf Blade",  # Name of the move
            "damage": 25,           # The damage the move does
            "energy_cost": 15       # Energy cost of the move
        },
        {
            "name": "Hamon Wrap",   # Name of the move
            "damage": 35,           # The damage the move does
            "energy_cost": 25       # Energy cost of the move
        }
    ],
    "sprite": "assets/sprites/hero_blank.png"   # Sprite path of the character
  }
```

###Let's take a closer look at how the stats work.
- "Alice Allstar": {
  - This determines how the character is referenced **in the program's calculations**, but not much else.
- "race": *string*
  - This is the character's species, options include: **"Human"**, **"Vampire"**, or **"Cambion"**
- "name": *string*
  - This determines how the character is called inside the game and during character selection.
- "attack_type": *string*
  - This is the character's combat style, and is where all their techniques come from.
- "max_hp": *integer*
  - This is the character's **total** health points, and determines how many hits they can take before dying.
- "hp": *integer*
  - This is the character's **current** health points. This is used if a character is wounded.
- "attack": *integer*
  - When a character uses **physical** attacks, this is the stat they use.
- "spattack": *integer*
  - When a character uses **supernatural** attacks, this is the stat they use.
- "defense": *integer*
  - When a character is hit by a **physical** attack, this is used for damage resistance.
- "spdefense": *integer*
  - When a character is hit by a **supernatural** attack, this is used for damage resistance.
- "max_energy": *integer*
  - This is the character's **total** energy, determines how long they can use techniques.
- "energy": *integer*
  - This is the character's **current** energy, determines how long they can continue to use techniques.
- "energy_regen": *integer*
  - This is how much energy the character **regenerates** every turn, determines how quickly they recover.
- "moves": *list* of *dicts*
  - This is the **techniques** the character can perform, determines the character's signature attacks.
- "sprite": *file path string*
  - This is the **image** of the character, used in character display.