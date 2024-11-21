import sys
from tkinter import *
from tkinter import filedialog, ttk, colorchooser 
from tkinter.font import Font

root = Tk()
root.title("I DID SOMETHING!!")
root.geometry("900x600")

default_font = Font(family="Arial", size=12)

text = Text(root, wrap="word", font=default_font, undo=True)
text.grid(row=0, column=0, columnspan=12, sticky="nsew", padx=10, pady=10)

def saveas():
    t = text.get("1.0", "end-1c")
    savelocation = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if savelocation:
        with open(savelocation, "w") as file:
            file.write(t)

def toggle_bold():
    current_font = Font(font=text["font"])
    current_font.config(weight="bold" if current_font.actual()["weight"] == "normal" else "normal")
    text.configure(font=current_font)

def toggle_italic():
    current_font = Font(font=text["font"])
    current_font.config(slant="italic" if current_font.actual()["slant"] == "roman" else "roman")
    text.configure(font=current_font)

def change_font(font_name):
    current_font = Font(font=text["font"])
    current_font.config(family=font_name)
    text.configure(font=current_font)

def change_font_size(size):
    try:
        current_font = Font(font=text["font"])
        current_font.config(size=int(size)) 
        text.configure(font=current_font)
    except ValueError:
        pass

def align_text(justify):
    for align in ["left", "center", "right"]:
        text.tag_remove(align, "1.0", "end")

    text.tag_configure(justify, justify=justify)
    text.tag_add(justify, "1.0", "end")

def change_text_color():
    color = colorchooser.askcolor()[1]
    if color:
        text.config(fg=color)

def change_bg_color():
    color = colorchooser.askcolor()[1]
    if color:
        text.config(bg=color)

def undo_text():
    try:
        text.edit_undo()
    except TclError:
        pass

def redo_text():
    try:
        text.edit_redo()
    except TclError:
        pass

def update_word_count(event=None):
    content = text.get("1.0", "end-1c").strip()
    word_count = len(content.split()) if content else 0
    char_count = len(content)
    status_label.config(text=f"Words: {word_count} | Characters: {char_count}")

style = ttk.Style()
style.theme_use("clam")  
style.configure("TButton", font=("Arial", 10), padding=5)
style.configure("TMenubutton", font=("Arial", 10))
style.configure("TSpinbox", font=("Arial", 10))
style.configure("TLabel", font=("Arial", 10))

button_frame = ttk.Frame(root)
button_frame.grid(row=1, column=0, columnspan=12, sticky="ew", padx=10, pady=5)

ttk.Button(button_frame, text="Save", command=saveas, width=10).grid(row=0, column=0, padx=5)
ttk.Button(button_frame, text="Bold", command=toggle_bold, width=10).grid(row=0, column=1, padx=5)
ttk.Button(button_frame, text="Italic", command=toggle_italic, width=10).grid(row=0, column=2, padx=5)
ttk.Button(button_frame, text="Text Color", command=change_text_color, width=10).grid(row=0, column=3, padx=5)
ttk.Button(button_frame, text="BG Color", command=change_bg_color, width=10).grid(row=0, column=4, padx=5)
ttk.Button(button_frame, text="Undo", command=undo_text, width=10).grid(row=0, column=5, padx=5)
ttk.Button(button_frame, text="Redo", command=redo_text, width=10).grid(row=0, column=6, padx=5)

font_selector = ttk.Combobox(button_frame, values=["Arial", "Courier", "Helvetica", "Times New Roman", "Verdana", "Comic Sans MS"])
font_selector.set("Arial") 
font_selector.grid(row=0, column=7, padx=5)
font_selector.bind("<<ComboboxSelected>>", lambda e: change_font(font_selector.get()))

font_size_selector = ttk.Spinbox(button_frame, from_=8, to=72, width=5)
font_size_selector.set(12)
font_size_selector.grid(row=0, column=8, padx=5)
font_size_selector.config(command=lambda: change_font_size(font_size_selector.get()))
font_size_selector.bind("<Return>", lambda e: change_font_size(font_size_selector.get()))  # Enter tuşuyla
font_size_selector.bind("<FocusOut>", lambda e: change_font_size(font_size_selector.get()))  # Odak kaybında
font_size_selector.bind("<<Increment>>", lambda e: change_font_size(font_size_selector.get()))  # Yukarı ok
font_size_selector.bind("<<Decrement>>", lambda e: change_font_size(font_size_selector.get()))  # Aşağı ok

ttk.Button(button_frame, text="Left", command=lambda: align_text("left"), width=10).grid(row=0, column=9, padx=5)
ttk.Button(button_frame, text="Center", command=lambda: align_text("center"), width=10).grid(row=0, column=10, padx=5)
ttk.Button(button_frame, text="Right", command=lambda: align_text("right"), width=10).grid(row=0, column=11, padx=5)

for col in range(12): 
    button_frame.grid_columnconfigure(col, weight=1)

status_label = ttk.Label(root, text="Words: 0 | Characters: 0", anchor="e")
status_label.grid(row=2, column=0, columnspan=12, sticky="ew", padx=10, pady=5)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

text.bind("<KeyRelease>", update_word_count)

root.mainloop()
