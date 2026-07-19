import customtkinter as ctk

ctk.set_appearance_mode("Dark")   
ctk.set_default_color_theme("blue")  

app = ctk.CTk()

app.title("khit!")
app.geometry("800x800")
app.resizable(False, False)

title = ctk.CTkLabel(app, text="khit!", font=("Arial", 24))
title.pack(pady=30)

tagline = ctk.CTkLabel(app, text="Think, Guess, & Remember.", font=("Arial", 14))
tagline.pack(pady=10)

playbutton = ctk.CTkButton(app, text="Play", font=("Arial", 18), command=lambda: print("Play button clicked"))
playbutton.pack(pady=20)

themesButton = ctk.CTkButton(app, text="Themes", font=("Arial", 18), command=lambda: print("Themes button clicked"))
themesButton.pack(pady=20)

settingsButton = ctk.CTkButton(app, text="Settings", font=("Arial", 18), command=lambda: print("Settings button clicked"))
settingsButton.pack(pady=20)

exitButton = ctk.CTkButton(app, text="Exit", font=("Arial", 18), command=app.destroy)
exitButton.pack(pady=20)

from ui import KhitApp

app = KhitApp()

app.mainloop()