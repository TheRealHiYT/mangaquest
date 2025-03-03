from tkinter import Tk, Label, Button, Entry, IntVar, StringVar, filedialog
from tkinter.ttk import Combobox
import json


def write_moves_to_file(filename: str):
    """ Asks user to input the number of spells, input the words of the spell, and then write to file.
    :param filename:
    :return:
    """
    # user inputs each spell, then they are appended to a list
    moves = list()
    for x in range(1):
        move_name = input("Whisper the name of a technique: ")
        move_damage = int(input("Whisper the damage of the technique: "))
        move_cost = int(input("Whiser the cost of the technique: "))
        move_type = input("Whisper the damage type of the technique (MAG, PHY, HAM, RAD): ")

        moves.append({"name": move_name, "damage": move_damage, "energy_cost": move_cost, "type": move_type})
    # write spells to the file
    with open(filename, 'a') as file:
        for move in moves:
            json.dump(move, fp=file, indent=4)


def read_spells_from_file(filename: str):
    """ Reads the user's spellbook from filename
    :param filename:
    :return:
    """
    with open(filename, 'r') as file:
        # Reads the file, seperating each line into a list
        spells = [line.strip() for line in file.readlines()]
        # Tells the user what to expect from the following lines
        print("Spells in your spellbook:\n\n")
        # Prints each spell in the list (spells) in order
        for spell in spells:
            print(spell)

        int_spells = [len(spell) for spell in spells]
        # Tells the user the numerical length of their spellbook
        print(f"There are {len(spells)} spells in your spellbook.\n")
        # Tells the user that the following are only extra details,
        # and they are not needed to understand the spellbook
        print("Some extra details of your spellbook:")
        # Flavoring spell names as incantations in order to fit the setting
        print(f"Characters in your longest incantation (spell name): {len(max(spells))}")
        print(f"Your incantations (spell names) have an average length of {sum(int_spells)/len(spells)}")


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
spdefense_label.grid(row=6, column=0, padx=5, pady=5)


spdefense_entry = Entry(window, textvariable=spdefense_var)
spdefense_entry.grid(row=6, column=1, padx=5, pady=5)


energy_var = IntVar(value=50)
energy_label = Label(window, text="Character's Energy:")
energy_label.grid(row=7, column=0, padx=5, pady=5)


energy_entry = Entry(window, textvariable=energy_var)
energy_entry.grid(row=7, column=1, padx=5, pady=5)


regen_var = IntVar(value=5)
regen_label = Label(window, text="Character's Energy Regen:")
regen_label.grid(row=8, column=0, padx=5, pady=5)


regen_entry = Entry(window, textvariable=regen_var)
regen_entry.grid(row=8, column=1, padx=5, pady=5)


moves_label = Label(window, text="Character's Techniques:")
moves_label.grid(row=9, column=0, padx=5, pady=5)


moves_button = Button(window, command=write_moves_to_file)
