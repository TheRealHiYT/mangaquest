import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import json
import os


class CharacterCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Character Creator")

        self.character_data = {
            "race": "",
            "name": "",
            "combat_style": "",
            "max_hp": 100,
            "hp": 100,
            "attack": 10,
            "spattack": 10,
            "defense": 5,
            "spdefense": 5,
            "max_energy": 50,
            "energy": 50,
            "energy_regen": 5,
            "moves": [],
            "sprite_path": "",
            "x": 100,
            "y": 100
        }

        self.create_widgets()

    def create_widgets(self):
        """Create input fields for character attributes"""

        # Name, Race, Combat Style
        tk.Label(self.root, text="Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Race:").grid(row=1, column=0)
        self.race_entry = tk.Entry(self.root)
        self.race_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Combat Style:").grid(row=2, column=0)
        self.combat_style_entry = tk.Entry(self.root)
        self.combat_style_entry.grid(row=2, column=1)

        # Stats
        self.create_stat_input("Max HP:", "max_hp", 3)
        self.create_stat_input("Attack:", "attack", 4)
        self.create_stat_input("Sp. Attack:", "spattack", 5)
        self.create_stat_input("Defense:", "defense", 6)
        self.create_stat_input("Sp. Defense:", "spdefense", 7)
        self.create_stat_input("Max Energy:", "max_energy", 8)
        self.create_stat_input("Energy Regen:", "energy_regen", 9)

        # Moves Section
        tk.Label(self.root, text="Moves:").grid(row=10, column=0, columnspan=2)
        self.moves_listbox = tk.Listbox(self.root, height=4, width=40)
        self.moves_listbox.grid(row=11, column=0, columnspan=2)

        tk.Button(self.root, text="Add Move", command=self.add_move).grid(row=12, column=0)
        tk.Button(self.root, text="Remove Move", command=self.remove_move).grid(row=12, column=1)

        # Sprite Selection
        tk.Button(self.root, text="Select Sprite", command=self.select_sprite).grid(row=13, column=0, columnspan=2)
        self.sprite_label = tk.Label(self.root, text="No sprite selected")
        self.sprite_label.grid(row=14, column=0, columnspan=2)

        # Save Button
        tk.Button(self.root, text="Save Character", command=self.save_character).grid(row=15, column=0, columnspan=2)

    def create_stat_input(self, label, key, row):
        """Helper function to create stat input fields"""
        tk.Label(self.root, text=label).grid(row=row, column=0)
        entry = tk.Entry(self.root)
        entry.grid(row=row, column=1)
        setattr(self, f"{key}_entry", entry)

    def add_move(self):
        """Add a move to the character's moveset"""
        move_name = tk.simpledialog.askstring("Move Name", "Enter move name:")
        if move_name:
            move_damage = tk.simpledialog.askinteger("Move Damage", "Enter move damage:")
            move_cost = tk.simpledialog.askinteger("Energy Cost", "Enter move energy cost:")
            move_type = tk.simpledialog.askstring("Move Type", "Enter move damage type:")
            if move_damage is not None and move_cost is not None:
                move = {"name": move_name, "damage": move_damage, "energy_cost": move_cost, "type": move_type}
                self.character_data["moves"].append(move)
                self.moves_listbox.insert(tk.END, f"{move_name} (Dmg: {move_damage}, Cost: {move_cost}, Type: {move_type})")

    def remove_move(self):
        """Remove selected move from list"""
        selected = self.moves_listbox.curselection()
        if selected:
            index = selected[0]
            del self.character_data["moves"][index]
            self.moves_listbox.delete(index)

    def select_sprite(self):
        """Select a sprite image file"""
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.character_data["sprite_path"] = file_path
            self.sprite_label.config(text=os.path.basename(file_path))

    def save_character(self):
        """Save character data to JSON file"""
        self.character_data["name"] = self.name_entry.get()
        self.character_data["race"] = self.race_entry.get()
        self.character_data["combat_style"] = self.combat_style_entry.get()

        # Update numeric stats
        for key in ["max_hp", "attack", "spattack", "defense", "spdefense", "max_energy", "energy_regen"]:
            try:
                self.character_data[key] = int(getattr(self, f"{key}_entry").get())
                if self.character_data[key] == "max_energy":
                    self.character_data["energy"] = int(getattr(self, f"{key}_entry").get())
                elif self.character_data[key] == "max_hp":
                    self.character_data["hp"] = int(getattr(self, f"{key}_entry").get())
            except ValueError:
                messagebox.showerror("Input Error", f"Invalid value for {key}. Please enter a number.")
                return

        # Save to JSON file
        file_name = f"{self.character_data['name']}.json"
        with open(file_name, "w") as f:
            json.dump(self.character_data, f, indent=4)

        messagebox.showinfo("Success", f"Character saved as {file_name}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CharacterCreator(root)
    root.mainloop()
