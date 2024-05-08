import random

class WordleInfo:
    def __init__(self):
        self.green = ['_', '_', '_', '_', '_']
        self.yellow = {}
        self.black = []


def check_against_answer(guess, answer):
    if len(guess) != len(answer):
        raise ValueError("ValueError: Guess and answer must be the same length")
    colors = ''
    for i, letter in enumerate(guess):
        duplicity = answer.count(letter)
        if letter == answer[i]:
            colors += 'G'
        elif duplicity >= guess.count(letter) + colors.count(letter):
            colors += 'Y'
        else:
            colors += 'X'
    return colors


def check_against_info(word, info):
    # Checks a candidate word against known information to determine if it can be the answer
    # Used in wordlecheat.py
    for letter in info.black:
        # Checks if there is a letter in the word that does not exist in the answer
        # Variable n counts how many times the black letter has already been accounted for
        n = 0
        for i in info.green:
            if i == letter:
                n += 1
        if letter in info.yellow:
            n += len(info.yellow[letter])
        # If there are more of that letter than accounted for, the word cannot be the answer
        if word.count(letter) > n:
            return False
    for i, letter in enumerate(info.green):
        # Checks if the known positions within the word are matched correctly
        if letter != '_' and letter != word[i]:
            return False
    for key, [y_duplicity, y_indices] in info.yellow.items():
        for i in y_indices:
            # Checks if a letter in the checked word is in an incorrect position
            if word[i] == key:
                return False
        if word.count(key) < y_duplicity + ''.join(info.green).count(key):
            # Checks if a known letter in the answer exists in the checked word enough times
            return False
    return True


def get_all_words(file):
    all_words = []
    with open(file, 'r') as f:
        for line in f.readlines():
            for word in line.strip().split():
                all_words.append(word)
    return all_words


def get_input_cheater(n=5):
    # Accepts any 5-letter input for word (even if it is not a word in the dictionary)
    # Invalid input will prompt the user for input again
    while True:
        word = input("Enter your guess (or type 'q' to quit):  ").strip().upper()
        # Accepts any 5-letter input for colors
        # Although the program prompts the user to give an 'x' for black letters from the guess,
        #    it will assume any letter besides 'y' or 'g' is a black letter 
        if word == 'Q':
            return word, ''
        print("Enter the color that corresponds with each letter from your guess (or type 'q' to quit)")
        colors = input("   black (x), yellow (y), or green (g):  ").strip().upper()
        if colors == 'Q':
            return colors, ''
        if len(word) != n or len(word) != len(colors):
            print(f"Invalid input, word and color info must each be {n} letters.")
            continue
        elif not word.isalpha() or not colors.isalpha():
            print("Invalid input, only letters may be used in your word and colors.")
            continue
        return word, colors


def get_input_play(all_words, n=5):
    # Accepts any 5-letter input for word (must be a word present in allfivewords.txt)
    # Invalid input will prompt the user for input again
    while True:
        word = input("Enter your guess (or type 'q' to quit):  ").strip().upper()
        if word == 'Q':
            return word
        if len(word) != n:
            print(f"Invalid input, your guess must be {n} letters.")
            continue
        elif not word.isalpha():
            print("Invalid input, only letters may be used in your word.")
            continue
        if word in all_words:
            return word
        print("Invalid input, word does not exist (not found in chosen database).")


def get_possible_words(all_words, info):
    possible_words = []        
    for word in all_words:
        if check_against_info(word, info):
            possible_words.append(word)
    return possible_words


def print_possibilities(all_words):
    if len(all_words) == 0:
        print("No words were found that meet the information you entered.")
        print("Consider double checking inputs for errors and trying again.")
    else:
        print("The word could be one of the following:")
    i = 1
    for word in all_words:
        print(word, end='')
        if i % 15 == 0:
            print()
        else:
            print("  ", end='')
        i += 1
    print()


def print_word_info(info):
    print()
    print(f"Letters in known positions are {''.join(info.green)}.")
    for letter, [y_duplicity, y_indices] in info.yellow.items():
        print(f"Letter {letter} is in the word {y_duplicity} times but not in these positions:", end=' ')
        for i in y_indices:
            print(i + 1, end=' ')
        print()
    print(f"Letters {', '.join(info.black)} have no more instances in the word.")


def process_input_info(word, colors, info):
    if len(word) != len(colors):
        raise ValueError("ValueError: Word and colors must be of the same length")
    dupe_info = {}
    for letter in info.yellow:
        dupe_info.update({letter: 0})
    for i, letter in enumerate(word):
        if colors[i] == 'G':
            info.green[i] = letter
            if letter in info.yellow:
                info.yellow[letter][0] -= 1
        elif colors[i] == 'Y':
            if letter in info.yellow:
                info.yellow[letter][1].append(i)
                dupe_info[letter] += 1
            else:
                info.yellow.update({letter: [0, [i]]})
                dupe_info.update({letter: 1})
        elif letter not in info.black:
            info.black.append(letter)
    for letter, n in dupe_info.items():
        info.yellow[letter][0] = max(n, info.yellow[letter][0])
    for letter, val in info.yellow.copy().items():
        if val[0] == 0:
            del info.yellow[letter]


def select_answer(all_words):
    return all_words[random.randint(0, len(all_words) - 1)]


def settings_setup():
    debug_mode = wants_help = ''
    while debug_mode not in ['Y', 'N']:
        debug_mode = input("Would you like to enable debug mode? (y/n): ").strip().upper()
        if debug_mode == 'Q':
            return 'Q', 'Q'
        elif debug_mode not in ['Y', 'N']:
            print(f"{debug_mode} is not a valid option. Please enter y or n: ")
    while wants_help not in ['Y', 'N']:
        wants_help = input("Would you like to use the Wordle helper for this game? (y/n): ").strip().upper()
        if wants_help == 'Q':
            return 'Q', 'Q'
        elif wants_help not in ['Y', 'N']:
            print(f"{wants_help} is not a valid option. Please enter y or n: ")
    debug_mode = True if debug_mode == 'Y' else False
    wants_help = True if wants_help == 'Y' else False
    return debug_mode, wants_help


def wordlemodule_info():
    with open("wordlemodinfo.txt", 'r') as file:
        lines = file.readlines()
        print("Welcome to the wordlemodule module!")
        response = ''
        while response != 'q':
            print("Enter the number of one of these functions to learn about it, or q to quit")
            print(lines[0])
            response = input().strip().lower()
            if response == 'q':
                break
            i = int(response) if response.isdecimal() else -1
            if i < 1 or i > 12 :
                print("Input not recognized as a valid number (1-12), please try again.")
            else:
                print(lines[i])
                response = input("Press enter to continue... ")
    print("Goodbye!")


if __name__ == "__main__":
    wordlemodule_info()