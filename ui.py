import customtkinter as ctk
from PIL import Image
from words import get_random_word
from game import check_guess
from save import add_xp
from save import get_xp
from save import load_data
from save import save_data
from themes import THEMES
from save import load_data
from save import set_theme, get_theme, update_stats, reset_progress


class KhitApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.theme = THEMES[get_theme()]
        self.configure(
            fg_color=self.theme["bg"])

        self.title("khit!")
        self.geometry("800x800")
        self.resizable(False, False)
        self.current_word = ""
        self.word_length = 0

        self.current_row = 0
        self.current_col = 0
        self.guess = ""

        self.game_active = False

        #keyb detection
        self.bind("<Key>", self.key_pressed)

        # screens
        self.main_menu = self.create_MainMenu()
        self.game_mode = self.create_GameMode()
        self.game_screen = self.create_GameScreen()
        self.themes_screen = self.create_ThemesScreen()
        self.settings_screen = self.create_SettingsScreen()

        # main menu 
        self.show_frame(self.main_menu)

    def key_pressed(self, event):

        # Stop i
        if not self.game_active:
            return

        key = event.keysym.lower()

        # erase
        if key == "backspace":

            if self.current_col > 0:

                self.current_col -= 1

                self.board[self.current_row][self.current_col].configure(
                    text=""
                )

                self.guess = self.guess[:-1]

        # ENTER
        elif key == "return":
            if self.current_col == self.word_length:

                # Check the guess
                result = check_guess(
                    self.current_word,
                    self.guess
                )

                # Color the tiles
                self.animate_tiles(self.current_row, result)

                # WIN
                if self.guess == self.current_word:

                    self.game_active = False

                    update_stats("win")

                    self.settings_screen.destroy()
                    self.settings_screen = self.create_SettingsScreen()

                    if self.word_length == 3:
                        reward = 20

                    elif self.word_length == 4:
                        reward = 35

                    else:
                        reward = 50

                    add_xp(reward)
                    current_xp = get_xp()
                    self.refresh_xp()

                    self.status_label.configure(
                    text=f"🎉 YOU WIN!\n\n+{reward} XP\nCurrent XP: {current_xp}",
                    text_color=self.theme["text"]
                    )

                    #para maclick play button
                    self.play_again_button.configure(state="normal")

                    self.play_again_button.pack(pady=10)
                    

                    self.update_idletasks()

                    return

                # Move to next row
                self.current_row += 1

                # GAME OVER
                if self.current_row >= 6:

                    self.game_active = False

                    update_stats("loss")
                    self.settings_screen.destroy()
                    self.settings_screen = self.create_SettingsScreen()

                    self.status_label.configure(
                        text=f"❌ GAME OVER!\nThe word was: {self.current_word.upper()}",
                        text_color="#E74C3C"
                    )

                    self.play_again_button.configure(state="normal")

                    self.play_again_button.pack(pady=15)
                    self.update_idletasks()
                    return

                # Reset for next guess
                self.current_col = 0
                self.guess = ""


        elif len(event.char) == 1 and event.char.isalpha():

            if self.current_col < self.word_length:

                self.board[self.current_row][self.current_col].configure(
                    text=event.char.upper()
                )

                self.guess += event.char.lower()

                self.current_col += 1

    def start_game(self, length):

        self.word_length = length
        self.current_word = get_random_word(length)

        self.current_row = 0
        self.current_col = 0
        self.guess = ""

        self.game_active = True

        #for hint
        self.hint_used = False

        print("Answer:", self.current_word)

        # Destroy the old game screen
        self.game_screen.destroy()

        self.game_screen = self.create_GameScreen()

        self.hint_button.configure(state="normal")

        self.show_frame(self.game_screen)

    def refresh_theme(self):
        self.theme = THEMES[get_theme()]

    # ----- image helpers -----

    def add_background(self, frame, size=(800, 800)):
        """Places a full-frame background image behind a screen's widgets."""

        bg_path = self.theme["bg_image"]
        pil_image = Image.open(bg_path)

        bg_image = ctk.CTkImage(
            light_image=pil_image,
            dark_image=pil_image,
            size=size
        )

        bg_label = ctk.CTkLabel(frame, image=bg_image, text="")
        bg_label.image = bg_image  # keep a reference so it isn't garbage collected

        # place first so widgets packed/gridded afterwards render on top of it
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        return bg_label

    def add_logo(self, parent, size=(240, 100), **pack_opts):
        """Creates a logo image label (replaces the old 'khit!' text title)."""

        logo_path = self.theme["logo_image"]
        pil_image = Image.open(logo_path)

        logo_image = ctk.CTkImage(
            light_image=pil_image,
            dark_image=pil_image,
            size=size
        )

        logo_label = ctk.CTkLabel(parent, image=logo_image, text="")
        logo_label.image = logo_image  # keep a reference so it isn't garbage collected

        logo_label.pack(**pack_opts)

        return logo_label

#MAINMENU
    def create_MainMenu(self):

        frame = ctk.CTkFrame(
            self,
            fg_color=self.theme["bg"]
        )

        self.add_background(frame)

        self.add_logo(frame, pady=(50, 50))

        tagline = ctk.CTkLabel(
            frame,
            text="Think, Guess, & Unlock!",
            text_color=self.theme["text"],
            font=("Arial", 14)
        )
        tagline.pack(pady=10)

        self.xp_label = ctk.CTkLabel(
            frame,
            text=f"Current XP: {get_xp()}",
            font=("Arial", 16),
            text_color=self.theme["text"]
        )
        self.xp_label.pack(pady=10)

        playButton = ctk.CTkButton(
            frame,
            fg_color=self.theme["button"],
            hover_color=self.theme["hover"],
            text_color=self.theme["button-text"],
            text="Play",
            command=lambda: self.show_frame(self.game_mode)
        )
        playButton.pack(pady=20)

        themesButton = ctk.CTkButton(
            frame,
            fg_color=self.theme["button"],
            hover_color=self.theme["hover"],
            text_color=self.theme["button-text"],
            text="Themes",
            command=lambda: self.show_frame(self.themes_screen)
        )
        themesButton.pack(pady=20)

        settingsButton = ctk.CTkButton(
            frame,
            fg_color=self.theme["button"],
            hover_color=self.theme["hover"],
            text_color=self.theme["button-text"],
            text="Settings",
            command=lambda: self.show_frame(self.settings_screen)
        )
        settingsButton.pack(pady=20)

        exitButton = ctk.CTkButton(
            frame,
            fg_color=self.theme["button"],
            hover_color=self.theme["hover"],
            text_color=self.theme["button-text"],
            text="Exit",
            command=self.destroy
        )
        exitButton.pack(pady=20)

        return frame

    # game mode

    def create_GameMode(self):
        
        frame = ctk.CTkFrame(
            self,
            fg_color=self.theme["bg"]
        )

        self.add_background(frame)

        ctk.CTkLabel(
            frame,
            text="Choose Game Mode",
            font=("Arial", 28, "bold"),
            text_color=self.theme["text"]
        ).pack(pady=(40,40))

        ctk.CTkButton(
            frame,
            fg_color=self.theme["button"],
            text="3 Letters",
            hover_color=self.theme["hover"],
            text_color=self.theme["button-text"],
            command=lambda: self.start_game(3)
        ).pack(pady=20)

        ctk.CTkButton(
            frame,
            fg_color=self.theme["button"],
            text="4 Letters",
            hover_color=self.theme["hover"],
            text_color=self.theme["button-text"],
            command=lambda: self.start_game(4)
        ).pack(pady=20)

        ctk.CTkButton(
            frame,
            fg_color=self.theme["button"],
            text="5 Letters",
            hover_color=self.theme["hover"],
            text_color=self.theme["button-text"],
            command=lambda: self.start_game(5)
        ).pack(pady=20)


        ctk.CTkButton(
            frame,
            fg_color=self.theme["button"],
            text="Back",
            hover_color=self.theme["hover"],
            text_color=self.theme["button-text"],
            command=lambda: self.show_frame(self.main_menu)
        ).pack(pady=30)

        return frame

    # gamescreen

    def create_GameScreen(self):
        frame = ctk.CTkFrame(
            self,
            fg_color=self.theme["bg"]
        )

        self.add_background(frame)

        self.add_logo(frame, size=(180, 75), pady=(20, 10))

        # Container for the board
        board_frame = ctk.CTkFrame(frame, fg_color="transparent")
        board_frame.pack(pady=20)

        # Store all the boxes
        self.board = []

        # Create 6 rows
        for row in range(6):

            row_boxes = []

            # Create boxes depending on the word length
            for col in range(self.word_length):

                box = ctk.CTkLabel(
                    board_frame,
                    text="",
                    text_color=self.theme["text"],
                    width=70,
                    height=70,
                    anchor="center",
                    corner_radius=8,
                    border_width=2,
                    border_color="gray",
                    font=("Arial", 24, "bold")
                )

                box.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5
                )

                row_boxes.append(box)

            self.board.append(row_boxes)

        #win or lose

        self.status_label = ctk.CTkLabel(
            frame,
            text="",
            font=("Arial", 20, "bold"),
            text_color=self.theme["text"]
        )
        self.status_label.pack(pady=10)

        # -------------------------
        # BUTTON CONTAINER
        # -------------------------

        button_frame = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )
        button_frame.pack(pady=20)


        # hint

        self.hint_button = ctk.CTkButton(
            button_frame,
            text="Hint (-10 XP)",
            hover_color=self.theme["hover"],
            fg_color=self.theme["button"],
            text_color=self.theme["button-text"],
            command=self.use_hint
        )
        self.hint_button.pack(side="left", padx=5)

        #
        # PLAY AGAIN BUTTON
        self.play_again_button = ctk.CTkButton(
            button_frame,
            text="Play Again",
            hover_color=self.theme["hover"],
            fg_color=self.theme["button"],
            text_color=self.theme["button-text"],
            command=self.play_again
        )

        # Hide until the game ends
        self.play_again_button.pack(side="left", padx=5)
        self.play_again_button.pack_forget()

        # BACK
        backButton = ctk.CTkButton(
            button_frame,
            text="Back to Menu",hover_color=self.theme["hover"],
            fg_color=self.theme["button"],
            text_color=self.theme["button-text"],
            command=lambda: self.show_frame(self.main_menu)
        )
        backButton.pack(side="left", padx=5)

        return frame
    
    def refresh_xp(self):
        self.xp_label.configure(
            text=f"Current XP: {get_xp()}"
        )
    
    def play_again(self):
        print("PLAY AGAIN ")
        self.start_game(self.word_length)

    #reset progress

    def reset_game_progress(self):

        reset_progress()

        self.refresh_theme()

        self.main_menu.destroy()
        self.game_mode.destroy()
        self.game_screen.destroy()
        self.themes_screen.destroy()
        self.settings_screen.destroy()

        self.main_menu = self.create_MainMenu()
        self.game_mode = self.create_GameMode()
        self.game_screen = self.create_GameScreen()
        self.themes_screen = self.create_ThemesScreen()
        self.settings_screen = self.create_SettingsScreen()

        self.show_frame(self.settings_screen)

    #confirmation 4 reset
    def confirm_reset(self):

        window = ctk.CTkToplevel(self)
        window.title("Reset Progress")
        window.geometry("350x180")
        window.resizable(False, False)

        ctk.CTkLabel(
            window,
            text="Reset all progress?\n\nThis cannot be undone.",
            font=("Arial",16)
        ).pack(pady=20)

        button_frame = ctk.CTkFrame(window, fg_color="transparent")
        button_frame.pack(pady=10)

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=window.destroy
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            button_frame,
            text="Reset",
            fg_color="#C0392B",
            hover_color="#A93226",
            command=lambda: (
                window.destroy(),
                self.reset_game_progress()
            )
        ).pack(side="left", padx=10)

    # themes

    def create_ThemesScreen(self):

        frame = ctk.CTkFrame(
            self,
            fg_color=self.theme["bg"]
        )

        self.add_background(frame)

        data = load_data()
        owned = data["themes_owned"]
        current_theme = get_theme()

        ctk.CTkLabel(
            frame,
            text="🎨 Theme Shop",
            font=("Arial", 28, "bold"),
            text_color=self.theme["text"]
        ).pack(pady=(40,40))

        self.xp_label = ctk.CTkLabel(
            frame,
            text=f"Current XP: {data['xp']}",
            font=("Arial",18,"bold"),
            text_color=self.theme["text"]
        )
        self.xp_label.pack(pady=(0,15))

        self.theme_message = ctk.CTkLabel(
            frame,
            text="",
            font=("Arial",15),
            text_color=self.theme["text"]
        )
        self.theme_message.pack()

        # themes rows
        for theme_name, info in THEMES.items():

            card = ctk.CTkFrame(
                frame,
                corner_radius=12,
                fg_color=self.theme["button"]
            )

            card.pack(fill="x", padx=25, pady=8)

            # Preview square
            preview = ctk.CTkFrame(
                card,
                width=35,
                height=35,
                corner_radius=8,
                fg_color=info["button"]
            )
            preview.pack(side="left", padx=15, pady=12)

            # Theme name
            ctk.CTkLabel(
                card,
                text=theme_name,
                font=("Arial",18,"bold"),
                text_color=self.theme["text"]
            ).pack(side="left")

            # Right button
            if theme_name == current_theme:

                btn = ctk.CTkButton(
                    card,
                    text="Applied ✓",
                    width=120,
                    state="disabled"
                )

            elif theme_name in owned:

                btn = ctk.CTkButton(
                    card,
                    text="Apply",
                    width=120,
                    fg_color=self.theme["button"],
                    hover_color="#2563EB",
                    command=lambda t=theme_name: self.apply_theme(t)
                )

            else:

                btn = ctk.CTkButton(
                    card,
                    text=f"Buy • {info['price']} XP",
                    width=120,
                    fg_color="#16A34A",
                    hover_color="#15803D",
                    command=lambda t=theme_name: self.buy_theme(t)
                )

            btn.pack(side="right", padx=15)

        ctk.CTkButton(
            frame,
            text="Back",
            fg_color=self.theme["button"],
            hover_color=self.theme["hover"],
            text_color=self.theme["button-text"],
            command=lambda: self.show_frame(self.main_menu)
        ).pack(pady=25)

        return frame
    
    def buy_theme(self, theme_name):
        data = load_data()

        # Already owned
        if theme_name in data["themes_owned"]:
            return

        price = THEMES[theme_name]["price"]

        # Not enough XP
        if data["xp"] < price:

            self.status_label.configure(
                text="Not enough XP!",
                text_color="red"
            )

            return

        # Deduct XP
        data["xp"] -= price

        # Unlock theme
        data["themes_owned"].append(theme_name)

        # Save
        save_data(data)

        self.theme_message.configure(
            text=f"🎉 {theme_name} unlocked!",
            text_color=self.theme["text"]
        )

        self.after(1000, self.refresh_theme_screen)

        # Refresh the Themes screen
        self.main_menu.destroy()
        self.main_menu = self.create_MainMenu()

        self.themes_screen.destroy()
        self.themes_screen = self.create_ThemesScreen()

        self.show_frame(self.themes_screen)

    def refresh_theme_screen(self):

        self.main_menu.destroy()
        self.main_menu = self.create_MainMenu()

        self.themes_screen.destroy()
        self.themes_screen = self.create_ThemesScreen()

        self.show_frame(self.themes_screen)

    def apply_theme(self, theme_name):

        data = load_data()

        if theme_name not in data["themes_owned"]:
            return

        # Save selected theme
        set_theme(theme_name)

        # Reload theme
        self.refresh_theme()

        # Destroy old screens
        self.main_menu.destroy()
        self.game_mode.destroy()
        self.game_screen.destroy()
        self.themes_screen.destroy()
        self.settings_screen.destroy()

        # Recreate screens using the new colors
        self.main_menu = self.create_MainMenu()
        self.game_mode = self.create_GameMode()
        self.game_screen = self.create_GameScreen()
        self.themes_screen = self.create_ThemesScreen()
        self.settings_screen = self.create_SettingsScreen()

        # Show main menu
        self.show_frame(self.main_menu)

        print(f"{theme_name} Applied!")

    # settings

    def create_SettingsScreen(self):

        frame = ctk.CTkFrame(
            self,
            fg_color=self.theme["bg"]
        )

        self.add_background(frame)

        ctk.CTkLabel(
            frame,
            text="Settings",
            text_color=self.theme["text"],
            font=("Arial", 30)
        ).pack(pady=30)

        data = load_data()

        games = data["games_played"]

        if games == 0:
            win_rate = 0
        else:
            win_rate = round((data["wins"] / games) * 100)

        stats = f"""
        XP: {data["xp"]}

        Games Played: {data["games_played"]}
        Wins: {data["wins"]}
        Losses: {data["losses"]}

        Win Rate: {win_rate}%

        Current Streak: {data["current_streak"]}
        Best Streak: {data["best_streak"]}
        """

        ctk.CTkLabel(
            frame,
            text=stats,
            justify="left",
            font=("Arial", 16),
            text_color=self.theme["text"]
        ).pack(pady=10)

        ctk.CTkButton(
        frame,
        text="Reset Progress",
        fg_color="#C0392B",
        hover_color="#A93226",
        command=self.confirm_reset).pack(pady=(20,10))

        ctk.CTkButton(
            frame,
            fg_color=self.theme["button"],
            text="Back", hover_color=self.theme["hover"],
            text_color=self.theme["button-text"],
            command=lambda: self.show_frame(self.main_menu)
        ).pack()

        return frame
    
    
    def animate_tiles(self, row, result):

        for col in range(self.word_length):

            def update_tile(c=col):

                color = result[c]

                if color == "green":
                    tile = self.theme["correct"]

                elif color == "yellow":
                    tile = self.theme["present"]

                else:
                    tile = self.theme["wrong"]

                self.board[row][c].configure(
                    fg_color=tile,
                    border_color=tile,
                    text_color=self.theme["text"]
                )

            self.after(col * 150, update_tile)


    #hints
    def use_hint(self):

        if self.hint_used:
            return

        data = load_data()

        if data["xp"] < 10:

            self.status_label.configure(
                text="Not enough XP!",
                text_color="red"
            )

            return

        # Spend XP
        data["xp"] -= 10
        save_data(data)

        self.hint_used = True

        self.hint_button.configure(state="disabled")

        # Reveal a random unrevealed letter
        import random

        hidden = []

        for i in range(self.word_length):

            if self.board[self.current_row][i].cget("text") == "":
                hidden.append(i)

        if not hidden:
            return

        index = random.choice(hidden)

        letter = self.current_word[index].upper()

        self.board[self.current_row][index].configure(
            text=letter
        )

        self.guess += letter.lower()

        self.current_col += 1

        self.status_label.configure(
            text="-10 XP",
            text_color="gold"
        )

    # show

    def show_frame(self, frame):

        self.main_menu.pack_forget()
        self.game_mode.pack_forget()
        self.game_screen.pack_forget()
        self.themes_screen.pack_forget()
        self.settings_screen.pack_forget()

        frame.pack(fill="both", expand=True)
