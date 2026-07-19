# khit!

> Think, Guess, & Unlock!

khit! is a Wordle-inspired word puzzle game built with Python. Players can challenge themselves by guessing hidden words, earn XP through gameplay, and customize their experience by unlocking different color themes.

The game name **khit!** comes from the Thai word **"คิด (khit)"**, meaning *to think*, representing the game's focus on logic, guessing, and problem-solving.

---

## 🎮 Features

### 📝 Word Puzzle Gameplay
- Choose between different word lengths:
  - 3-letter words
  - 4-letter words
  - 5-letter words
- Word guessing system inspired by Wordle
- Color-based feedback:
  - 🟩 Correct letter and position
  - 🟨 Correct letter but wrong position
  - ⬜ Incorrect letter

---

### 🏠 Main Menu
Navigate through different sections:
- Play Game
- Theme Shop
- Settings
- Exit

---

### ⭐ XP Reward System
- Players earn XP by completing games.
- XP can be used to unlock color themes.

---

### 🎨 Theme Shop
Customize the game's appearance by purchasing color themes using XP.

Current available themes:
- Default
- Nightnight
- Leafie
- Pinku
- Cyber

Themes modify the game's visual design, including:
- Background colors
- Buttons
- Game tiles

---

### ⚙️ Settings & Player Statistics

khit! includes a settings menu where players can view their game progress and manage their saved data.

- **Statistics Tracking**
  - View total games played
  - Track wins and losses
  - View win rate percentage
  - Monitor best streak
  - Check total XP earned

- **Reset Progress**
  - Allows players to reset their saved progress
  - Clears XP, unlocked themes, and statistics
  - Restarts the game experience from the beginning

---

## 🛠️ Built With

- Python
- CustomTkinter (GUI)
- JSON (Save System)

---

## 📂 Project Structure
```
Khit/
│
├── main.py
├── game.py
├── ui.py
├── words.py
├── themes.py
├── save.py
│
├── data/
│   ├── threeLetters.txt
│   ├── fourLetters.txt
│   ├── fiveLetters.txt
│   └── save.json
│
├── assets/
│   ├── icons/
│   ├── images/
│   ├── fonts/
│
├── README.md
├── Screenshots
├── LICENSE
└── .gitignore
```

