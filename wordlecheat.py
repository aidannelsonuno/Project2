# This program will take an input of an incomplete wordle word, along with banned letters
# Then it will compare the information against a list of all 5-letter words to find possibilities
import wordlemodule as wmod

def main():
    # Initializing variables
    file = "allfivewords.txt"
    info = wmod.WordleInfo()
    all_words = wmod.get_all_words(file)
    # Loops 6 times (6 rounds in wordle)
    for i in range(6):
        # Word and colors in the form of 5-character strings of letters
        # More info in function get_input
        word, colors = wmod.get_input_cheater()
        if word == 'Q':
            print("Goodbye!")
            break
        elif colors == 'GGGGG':
            print("You got it! Good job")
            break
        wmod.process_input_info(word, colors, info)
        wmod.print_word_info(info)
        wmod.print_possibilities(wmod.get_possible_words(all_words, info))


if __name__ == "__main__":
    main()