import json

SAVE_FILE = "data/save.json"


def load_data():
    with open(SAVE_FILE, "r") as file:
        return json.load(file)


def save_data(data):
    with open(SAVE_FILE, "w") as file:
        json.dump(data, file, indent=4)


def get_xp():
    data = load_data()
    return data["xp"]


def add_xp(amount):
    data = load_data()
    data["xp"] += amount
    save_data(data)


def get_theme():
    data = load_data()
    return data["theme"]


def set_theme(theme):
    data = load_data()
    data["theme"] = theme
    save_data(data)

#test

if __name__ == "__main__":
    print(get_xp())

    add_xp(20)

    print(get_xp())

def set_theme(theme):

    data = load_data()

    data["theme"] = theme

    save_data(data)


def get_theme():

    data = load_data()

    return data["theme"]

def update_stats(result):

    data = load_data()

    data["games_played"] += 1


    if result == "win":

        data["wins"] += 1
        data["current_streak"] += 1


        if data["current_streak"] > data["best_streak"]:
            data["best_streak"] = data["current_streak"]


    elif result == "loss":

        data["losses"] += 1
        data["current_streak"] = 0


    save_data(data) 

def reset_progress():

    data = {
        "xp": 0,
        "themes_owned": ["Default"],
        "theme": "Default",
        "games_played": 0,
        "wins": 0,
        "losses": 0,
        "current_streak": 0,
        "best_streak": 0
    }

    save_data(data)