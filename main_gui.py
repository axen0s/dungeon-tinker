import tkinter as tk
from tkinter import ttk
from typing import TypeVar, Type

from gen.base_dungeon_gen import BaseDungeonGenerator
from gen.cellular_automata_dungeon import CADungeonGen

base_dungeon_type = TypeVar('base_dungeon_type', bound=BaseDungeonGenerator)
dungeon_gens: dict[str, Type[base_dungeon_type]] = {"Cellular Automata": CADungeonGen}

root = tk.Tk()
root.geometry("500x500")

seed_var = tk.IntVar()
seed_label = tk.Label(root, text="Seed")
seed_label.grid(row=0, column=0)
seed_entry = tk.Entry(root, textvariable=seed_var)
seed_entry.grid(row=0, column=1)

width_var = tk.IntVar()
width_label = tk.Label(root, text="Width")
width_label.grid(row=0, column=2)
width_entry = tk.Entry(root, textvariable=width_var)
width_entry.grid(row=0, column=3)

height_var = tk.IntVar()
height_label = tk.Label(root, text="Height")
height_label.grid(row=0, column=4)
height_entry = tk.Entry(root, textvariable=height_var)
height_entry.grid(row=0, column=5)

tk.Label(root, text="Generation Algorithm").grid(row=1, column=0)
text_dungeon_type = tk.StringVar()
combo_dungeon_type = ttk.Combobox(root, values=list(dungeon_gens.keys()), textvariable=text_dungeon_type)
combo_dungeon_type.bind('<<ComboboxSelected>>', func=lambda event: gen_selected(event))
combo_dungeon_type.grid(row=1, column=1)


# combo_dungeon_type.current(0)


# label_selected = tk.Label(root, text="Select Dungeon Type")
# label_selected.grid(row=0, column=1)

def do_gen(dungeon_object: CADungeonGen, textvars: dict[str, tk.Variable]):
    real_kwargs = {}
    for textvar in textvars:
        real_kwargs[textvar] = textvars[textvar].get()
    # dungeon = dungeon_module(height_var.get(), width_var.get())
    dungeon_object.generate(seed_var.get(), kwargs=real_kwargs)

    dungeon_display = tk.Text(root, wrap="word")
    dungeon_display.grid()
    dungeon_display.configure(font=("Courier New", 12))
    for row in dungeon_object.get_dungeon_lines():
        dungeon_display.insert("1.0", row + "\n")
    dungeon_display.configure(state="disabled")

    def clear():
        del_button.destroy()
        dungeon_display.destroy()

    del_button = tk.Button(root, text="Clear", command=lambda: clear())
    del_button.grid()


def gen_selected(event):
    textvars = {}
    dungeon_gen = dungeon_gens[text_dungeon_type.get()]

    current_row = 2
    current_col = 0
    for req_arg in dungeon_gen.dungeon_kwargs:
        tk.Label(root, text=req_arg[0]).grid(row=current_row, column=current_col)
        current_col += 1
        if req_arg[1] == str:
            textvars[req_arg[0]] = tk.StringVar()
        elif req_arg[1] == int:
            textvars[req_arg[0]] = tk.IntVar()
        elif req_arg[1] == float:
            textvars[req_arg[0]] = tk.DoubleVar()
        tk.Entry(root, textvariable=textvars[req_arg[0]]).grid(row=current_row, column=current_col)
        current_row += 1
        current_col = 0
    tk.Button(root, text="Generate",
              command=lambda: do_gen(dungeon_gen(height_var.get(), width_var.get()), textvars)).grid(row=current_row,
                                                                                                     column=current_col)


root.mainloop()
