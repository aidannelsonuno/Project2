import random
import wordlemodule as wmod

def main():
    print("Welcome to Wordle! Type 'q' as any prompt to exit the game.")
    file = "allfivewords.txt"
    all_words = wmod.get_all_words(file)
    debug_mode, wants_help = wmod.settings_setup()
    if wants_help:
        info = wmod.WordleInfo()
    answer = wmod.select_answer(all_words)
    if debug_mode:
        print(f"DEBUG MODE: answer is {answer}")
    for i in range(1, 7):
        if wants_help == 'Q':
            print("Goodbye!")
            break
        print(f"Guess {i}-", end=' ')
        guess = wmod.get_input_play(all_words)
        if guess == 'Q':
            print("Goodbye!")
            break
        elif guess == answer:
            print(f"You got it in {i} guesses! The answer is {answer}.")
            break
        colors = wmod.check_against_answer(guess, answer)
        print(f"The results of your guess {guess}: {colors}")
        if wants_help:
            wmod.process_input_info(guess, colors, info)
            wmod.print_possibilities(wmod.get_possible_words(all_words, info))
        print()
        if i == 5:
            print(f"You ran out of guesses! The answer was {answer}.")


if __name__ == "__main__":
    main()