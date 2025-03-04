from tkinter import Tk, Label, Entry, IntVar, StringVar
from tkinter.ttk import Combobox, Button
from assets.structure.characters import Character
import pygame

pygame.init()
WIDTH, HEIGHT = 1000, 800
pygame.display.set_mode((WIDTH, HEIGHT))
character = Character
moves = list()


def finalize_character():
    """ When user has entered all states, they press the 'create_character' button, which writes the character to fighters.json
    :return: A new character in '*/assets/structure/fighters.json'
    """

    try:
        finished_character = character(race=race_var.get(), name=char_var.get(), combat_style=style_var.get(),
                                       max_hp=hp_var.get(), hp=hp_var.get(),
                                       attack=attack_var.get(), spattack=spattack_var.get(), defense=defense_var.get(),
                                       spdefense=spdefense_var.get(),
                                       max_energy=energy_var.get(), energy=energy_var.get(),
                                       energy_regen=regen_var.get(), moves=moves, x=-50, y=300,
                                       sprite_path=sprite_var.get())

        with open('assets/structure/fighters.txt', mode='a') as file:
            file.write(f'"{char_var.get()}": \u007b \n{finished_character.race}, \n{finished_character.name}, \n'
                       f'{finished_character.combat_style}, \n{finished_character.maxhp}, \n{finished_character.hp}, '
                       f'\n{finished_character.attack}, \n{finished_character.spattack}, \n{finished_character.defense}, \n'
                       f'{finished_character.spdefense}, \n{finished_character.max_energy}, \n{finished_character.energy}, \n'
                       f'{finished_character.energy_regen}, \n{finished_character.moves}, \n-50, \n300, \n{finished_character.sprite}')
    except Exception as e:
        print(f"An error occurred: {e}")


def write_moves():
    """ Asks user to input the number of spells, input the words of the spell, and then write to file.
    :return:
    """
    global character
    global moves
    # user inputs each spell, then they are appended to a list
    for x in range(4):
        move_name = input("Whisper the name of a technique: ")
        move_damage = int(input("Whisper the damage of the technique: "))
        move_cost = int(input("Whiser the cost of the technique: "))
        move_type = input("Whisper the damage type of the technique (MAG, PHY, HAM, RAD): ")

        moves.append({"name": move_name, "damage": move_damage, "energy_cost": move_cost, "type": move_type})


# ---Window Setup---
window = Tk()
window.minsize(500, 900)

# ---Data Field Setup---
char_label = Label(window, text="Character's Name:")
char_label.grid(row=0, column=0, padx=5, pady=5)

char_var = StringVar(value="Anonymous Fighter")
char_entry = Entry(window, textvariable=char_var)
char_entry.grid(row=0, column=1, padx=5, pady=5)

race_label = Label(window, text="Character's Species:")
race_label.grid(row=1, column=0, padx=5, pady=5)

race_list = ["Human", "Vampire", "Cambion"]
race_var = StringVar(value="Human")

race_dropdown = Combobox(window, values=race_list, textvariable=race_var, state="readonly")
race_dropdown.grid(row=1, column=1, padx=5, pady=5)

style_label = Label(window, text="Character's Combat Style:")
style_label.grid(row=2, column=0, padx=5, pady=5)

style_list = ["PHY", "MAG", "HAM", "RAD"]
style_var = StringVar(value="PHY")

style_dropdown = Combobox(window, values=style_list, textvariable=style_var)
style_dropdown.grid(row=2, column=1, padx=5, pady=5)

hp_var = IntVar(value=100)
hp_label = Label(window, text="Character's HP:")
hp_label.grid(row=3, column=0, padx=5, pady=5)

hp_entry = Entry(window, textvariable=hp_var)
hp_entry.grid(row=3, column=1, padx=5, pady=5)

attack_var = IntVar(value=20)
attack_label = Label(window, text="Character's Attack:")
attack_label.grid(row=4, column=0, padx=5, pady=5)

attack_entry = Entry(window, textvariable=attack_var)
attack_entry.grid(row=4, column=1, padx=5, pady=5)

spattack_var = IntVar(value=20)
spattack_label = Label(window, text="Character's Special Attack:")
spattack_label.grid(row=5, column=0, padx=5, pady=5)

spattack_entry = Entry(window, textvariable=spattack_var)
spattack_entry.grid(row=5, column=1, padx=5, pady=5)

defense_var = IntVar(value=25)
defense_label = Label(window, text="Character's Defense:")
defense_label.grid(row=6, column=0, padx=5, pady=5)

defense_entry = Entry(window, textvariable=defense_var)
defense_entry.grid(row=6, column=1, padx=5, pady=5)

spdefense_var = IntVar(value=25)
spdefense_label = Label(window, text="Character's Special Defense:")
spdefense_label.grid(row=7, column=0, padx=5, pady=5)

spdefense_entry = Entry(window, textvariable=spdefense_var)
spdefense_entry.grid(row=7, column=1, padx=5, pady=5)

energy_var = IntVar(value=50)
energy_label = Label(window, text="Character's Energy:")
energy_label.grid(row=8, column=0, padx=5, pady=5)

energy_entry = Entry(window, textvariable=energy_var)
energy_entry.grid(row=8, column=1, padx=5, pady=5)

regen_var = IntVar(value=5)
regen_label = Label(window, text="Character's Energy Regen:")
regen_label.grid(row=9, column=0, padx=5, pady=5)

regen_entry = Entry(window, textvariable=regen_var)
regen_entry.grid(row=9, column=1, padx=5, pady=5)

moves_button = Button(window, text="Create Techniques", command=write_moves)
moves_button.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

sprite_var = StringVar(value="C:/")
sprite_label = Label(window, text="Sprite File Path:")
sprite_label.grid(row=11, column=0, padx=5, pady=5)

sprite_entry = Entry(window, textvariable=sprite_var)
sprite_entry.grid(row=11, column=1, padx=5, pady=5)

create_character = Button(window, text="Create Character", command=finalize_character)
create_character.grid(row=12, column=0, columnspan=2, padx=5, pady=5)

window.mainloop()
