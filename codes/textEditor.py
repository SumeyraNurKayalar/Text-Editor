import sys
from tkinter import *
from tkinter import filedialog, ttk, colorchooser 
from tkinter.font import Font

# Ana pencereyi oluştur
root = Tk()
root.title("I DID SOMETHING!!")
root.geometry("900x600")

# Varsayılan font
default_font = Font(family="Arial", size=12)

# Metin kutusu
text = Text(root, wrap="word", font=default_font, undo=True)
text.grid(row=0, column=0, columnspan=12, sticky="nsew", padx=10, pady=10)

# Kaydetme fonksiyonu
def saveas():
    t = text.get("1.0", "end-1c")
    savelocation = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if savelocation:
        with open(savelocation, "w") as file:
            file.write(t)

# Biçimlendirme fonksiyonları
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
        current_font.config(size=int(size))  # Boyutu tam sayı olarak ayarla
        text.configure(font=current_font)
    except ValueError:
        # Geçersiz giriş yapılırsa bir şey yapma
        pass


# Hizalama fonksiyonları
def align_text(justify):
    # Önce tüm eski hizalamaları kaldır
    for align in ["left", "center", "right"]:
        text.tag_remove(align, "1.0", "end")

    # Yeni hizalamayı ekle
    text.tag_configure(justify, justify=justify)
    text.tag_add(justify, "1.0", "end")

# Renk değiştirme fonksiyonları
def change_text_color():
    color = colorchooser.askcolor()[1]
    if color:
        text.config(fg=color)

def change_bg_color():
    color = colorchooser.askcolor()[1]
    if color:
        text.config(bg=color)

# Undo ve Redo fonksiyonları
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

# Kelime ve karakter sayısı
def update_word_count(event=None):
    content = text.get("1.0", "end-1c").strip()
    word_count = len(content.split()) if content else 0
    char_count = len(content)
    status_label.config(text=f"Words: {word_count} | Characters: {char_count}")

# Stil ve Tema Ayarları
style = ttk.Style()
style.theme_use("clam")  # "clam", "alt", "default" gibi temalar
style.configure("TButton", font=("Arial", 10), padding=5)
style.configure("TMenubutton", font=("Arial", 10))
style.configure("TSpinbox", font=("Arial", 10))
style.configure("TLabel", font=("Arial", 10))

# Üst düğme çubuğu
button_frame = ttk.Frame(root)
button_frame.grid(row=1, column=0, columnspan=12, sticky="ew", padx=10, pady=5)

# Düğmeler
ttk.Button(button_frame, text="Save", command=saveas, width=10).grid(row=0, column=0, padx=5)
ttk.Button(button_frame, text="Bold", command=toggle_bold, width=10).grid(row=0, column=1, padx=5)
ttk.Button(button_frame, text="Italic", command=toggle_italic, width=10).grid(row=0, column=2, padx=5)
ttk.Button(button_frame, text="Text Color", command=change_text_color, width=10).grid(row=0, column=3, padx=5)
ttk.Button(button_frame, text="BG Color", command=change_bg_color, width=10).grid(row=0, column=4, padx=5)
ttk.Button(button_frame, text="Undo", command=undo_text, width=10).grid(row=0, column=5, padx=5)
ttk.Button(button_frame, text="Redo", command=redo_text, width=10).grid(row=0, column=6, padx=5)

# Yazı tipi seçici
font_selector = ttk.Combobox(button_frame, values=["Arial", "Courier", "Helvetica", "Times New Roman", "Verdana", "Comic Sans MS"])
font_selector.set("Arial")  # Varsayılan yazı tipi
font_selector.grid(row=0, column=7, padx=5)
font_selector.bind("<<ComboboxSelected>>", lambda e: change_font(font_selector.get()))

# Yazı boyutu seçici
font_size_selector = ttk.Spinbox(button_frame, from_=8, to=72, width=5)
font_size_selector.set(12)
font_size_selector.grid(row=0, column=8, padx=5)
font_size_selector.config(command=lambda: change_font_size(font_size_selector.get()))
font_size_selector.bind("<Return>", lambda e: change_font_size(font_size_selector.get()))  # Enter tuşuyla
font_size_selector.bind("<FocusOut>", lambda e: change_font_size(font_size_selector.get()))  # Odak kaybında
font_size_selector.bind("<<Increment>>", lambda e: change_font_size(font_size_selector.get()))  # Yukarı ok
font_size_selector.bind("<<Decrement>>", lambda e: change_font_size(font_size_selector.get()))  # Aşağı ok



# Hizalama düğmeleri
ttk.Button(button_frame, text="Left", command=lambda: align_text("left"), width=10).grid(row=0, column=9, padx=5)
ttk.Button(button_frame, text="Center", command=lambda: align_text("center"), width=10).grid(row=0, column=10, padx=5)
ttk.Button(button_frame, text="Right", command=lambda: align_text("right"), width=10).grid(row=0, column=11, padx=5)

# Her sütunun eşit genişlikte olmasını sağla
for col in range(12):  # 12 sütun olduğu için
    button_frame.grid_columnconfigure(col, weight=1)

# Kelime ve karakter sayısı
status_label = ttk.Label(root, text="Words: 0 | Characters: 0", anchor="e")
status_label.grid(row=2, column=0, columnspan=12, sticky="ew", padx=10, pady=5)

# Dinamik boyutlandırma
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Metin kutusu değiştikçe kelime ve karakter sayısını güncelle
text.bind("<KeyRelease>", update_word_count)

# Ana döngüyü başlat
root.mainloop()
