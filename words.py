import random

def load_words(filename):
    with open(f"data/{filename}", "r") as file:
        words = file.read().splitlines()

    return words


def get_random_word(length):

    if length == 3:
        filename = "threeLetters.txt"

    elif length == 4:
        filename = "fourLetters.txt"

    elif length == 5:
        filename = "fiveLetters.txt"

    else:
        return None

    words = load_words(filename)

    return random.choice(words)

if __name__ == "__main__":
    print("3 Letters:", get_random_word(3))
    print("4 Letters:", get_random_word(4))
    print("5 Letters:", get_random_word(5))