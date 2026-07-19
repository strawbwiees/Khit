def check_guess(guess, answer):

    result = []

    for i in range(len(guess)):

        if guess[i] == answer[i]:
            result.append("correct")

        elif guess[i] in answer:
            result.append("present")

        else:
            result.append("wrong")

    return result

def check_guess(answer, guess):

    result = []

    for i in range(len(guess)):

        if guess[i] == answer[i]:
            result.append("green")

        elif guess[i] in answer:
            result.append("yellow")

        else:
            result.append("gray")

    return result