from PyQt6.QtWidgets import *
from gui import *
from wordleinfo import WordleInfo
import random


class Logic(QMainWindow, Ui_main_window):
    '''
    A class containing the logic that drives the wordle game.
    '''
    def __init__(self) -> None:
        '''
        Initializes the GUI object and variables related to the functionality of GUI widgets.
        '''
        super().__init__()
        self.setupUi(self)

        self.all_words = self.get_all_words()

        self.gameplay_group = self.make_gameplay_group()
        self.letter_array = self.make_letter_array()
        self.appearing_group = self.make_appearing_group()
        self.startup_group = self.make_startup_group()
        self.guess_label_group = self.make_guess_title_list()
        self.helper_info = WordleInfo()

        self.exit_button.clicked.connect(self.close)
        self.return_button.clicked.connect(self.enter_startup_mode)
        self.start_button.clicked.connect(self.enter_gameplay_mode)
        self.guess_button.clicked.connect(self.take_guess)

        self.enter_startup_mode()


    def check_against_answer(self, guess: str) -> None:
        '''
        Checks a user's guess against the answer to correctly color the letters for user's information.
        :param guess: Five-letter word guessed by the user.
        '''
        if len(guess) != len(self.answer):
            raise ValueError("ValueError: Guess and answer must be the same length")
        colors = ['X', 'X', 'X', 'X', 'X']
        guess_counts = {}
        answer_counts = {}
        for i, letter in enumerate(guess): # Records all instances of green placement (correct letter and placement)
            green_round = False
            self.letter_array[self.guesses_made][i].setText(guess[i])
            if letter == self.answer[i]:
                colors[i] = 'G'
                self.letter_array[self.guesses_made][i].setStyleSheet("color: green;")
                green_round = True
            else:
                self.letter_array[self.guesses_made][i].setStyleSheet("color: gray;")
            if letter in guess_counts: # Counts of letters in guess and answer give information used in yellow placement
                guess_counts[letter] += 1
            else:
                guess_counts.update({letter: 1})
            if not green_round:
                if self.answer[i] in answer_counts:
                    answer_counts[self.answer[i]] += 1
                else:
                    answer_counts.update({self.answer[i]: 1})
        for i, letter in enumerate(guess): # Records all instances of yellow placement (correct letter but incorrect placement)
            if letter in guess_counts and letter in answer_counts and not colors[i] == 'G':
                colors[i] = 'Y'
                self.letter_array[self.guesses_made][i].setStyleSheet("color: yellow;")
                guess_counts[letter] -= 1 # Counts must be recorded for yellow placement in case of duplicate letters
                answer_counts[letter] -= 1
                if guess_counts[letter] <= 0:
                    del guess_counts[letter]
                if answer_counts[letter] <= 0:
                    del answer_counts[letter]
        if self.checkBox_helper_toggle.isChecked():
            self.helper_info.process_input_info(guess, colors)


    def enter_gameplay_mode(self) -> None:
        '''
        Hides widgets for the setup menu, shows widgets for gameplay and initializes new game data
        '''
        for widget in self.startup_group:
            widget.setVisible(False)
        for widget in self.gameplay_group:
            widget.setVisible(True)
        if self.checkBox_helper_toggle.isChecked:
            self.all_possibilities.setVisible(True)
        self.initialize_gamestate()


    def enter_startup_mode(self) -> None:
        '''
        Hides widgets for the game, shows widgets for the startup menu and updates statistic displays
        '''
        with open("Project2/stats_data.txt", 'r') as file:
            data = file.readline().split()
            self.label_games_played.setText(data[0])
            self.label_stats_1g.setText(data[1])
            self.label_stats_2g.setText(data[2])
            self.label_stats_3g.setText(data[3])
            self.label_stats_4g.setText(data[4])
            self.label_stats_5g.setText(data[5])
            self.label_stats_6g.setText(data[6])
        for widget in self.startup_group:
            widget.setVisible(True)
        for widget in self.gameplay_group:
            widget.setVisible(False)
        for widget in self.appearing_group:
            widget.setVisible(False)


    def get_all_words(self, curated=False) -> list:
        '''
        Reads words from a file of words separated by whitespace and makes them a list
        Words can come from all_five_words.txt, a file of all 5-letter English words, or previous_wordle_answers.txt,
        a file of previous answers from the official Wordle game, depending on the users choice (curation)
        :param curated: Determines which file to use (False uses all_five_words.txt, True uses previous_wordle_answers.txt)
        :return: A list of all possible answers at the beginning of the game based on the desired set of words
        '''
        all_words = []
        if curated:
            filename = "Project2/previous_wordle_answers.txt"
        else:
            filename = "Project2/all_five_words.txt"
        with open(filename, 'r') as f:
            for line in f.readlines():
                for word in line.strip().split():
                    all_words.append(word)
        return all_words
    

    def initialize_gamestate(self) -> None:
        '''
        Sets up the data needed to play the game
        '''
        self.remaining_words = self.get_all_words()
        self.word_list = self.get_all_words(self.checkBox_curation_toggle.isChecked())
        self.answer = self.all_words[random.randint(0, len(self.all_words) - 1)]
        self.label_answer.setText(self.answer)
        self.helper_info = WordleInfo()
        self.all_possibilities.setText('')
        self.guesses_made = 0


    def make_appearing_group(self) -> list:
        '''
        Groups all widgets that appear during gameplay but do not start revealed
        These widgets are grouped in order to easily perform operations on several of them simultaneously
        :return: A list of all widgets that appear during gameplay
        '''
        appearing_group = [self.label_previous_title, self.label_answer_title, self.label_answer]
        appearing_group += [self.label_guess_1_title, self.label_guess_2_title, self.label_guess_3_title]
        appearing_group += [self.label_guess_4_title, self.label_guess_5_title, self.label_guess_6_title]
        appearing_group += [self.label_congrats_answer, self.label_congrats_guesses, self.all_possibilities]
        for guess in self.letter_array:
            for letter in guess:
                appearing_group.append(letter)
        return appearing_group


    def make_gameplay_group(self) -> list:
        '''
        Groups all widgets that are always visible during gameplay
        These widgets are grouped in order to easily perform operations on several of them simultaneously
        :return: A list of all widgets that are always visible during gameplay
        '''
        return [self.label_guess_title, self.entry_guess, self.guess_button, self.label_error_display, self.return_button]
    

    def make_guess_title_list(self) -> list:
        '''
        Groups the labels for each of the guess numbers (ex: Guess 1)
        These items are grouped in order to select a title to reveal without hard coding each title individually
        :return: A list of all guessing titles that appear during gameplay
        '''
        title_list = [self.label_guess_1_title, self.label_guess_2_title, self.label_guess_3_title]
        title_list += [self.label_guess_4_title, self.label_guess_5_title, self.label_guess_6_title]
        return title_list


    def make_letter_array(self) -> list:
        '''
        Groups all elements that represent letters of a user guess
        These items are grouped in order to edit each item's letter and color without hard coding each item
        :return: An array of label widgets where each row is a guessed word and each column is a letter in that word
        '''
        group1 = [self.g1c1, self.g1c2, self.g1c3, self.g1c4, self.g1c5]
        group2 = [self.g2c1, self.g2c2, self.g2c3, self.g2c4, self.g2c5]
        group3 = [self.g3c1, self.g3c2, self.g3c3, self.g3c4, self.g3c5]
        group4 = [self.g4c1, self.g4c2, self.g4c3, self.g4c4, self.g4c5]
        group5 = [self.g5c1, self.g5c2, self.g5c3, self.g5c4, self.g5c5]
        group6 = [self.g6c1, self.g6c2, self.g6c3, self.g6c4, self.g6c5]
        return [group1, group2, group3, group4, group5, group6]
    

    def make_startup_group(self) -> list:
        '''
        Groups all widgets that are always visible during the setup phase
        These widgets are grouped in order to easily perform operations on several of them simultaneously
        :return: A list of all widgets that appear during the setup phase
        '''
        startup_group = [self.label_welcome, self.label_settings, self.start_button, self.checkBox_helper_toggle]
        startup_group += [self.checkBox_curation_toggle, self.label_stats_title, self.label_games_played_title, self.label_games_played]
        startup_group += [self.label_stats_1g_title, self.label_stats_1g, self.label_stats_2g_title, self.label_stats_2g]
        startup_group += [self.label_stats_3g_title, self.label_stats_3g, self.label_stats_4g_title, self.label_stats_4g]
        startup_group += [self.label_stats_5g_title, self.label_stats_5g, self.label_stats_6g_title, self.label_stats_6g]
        return startup_group


    def take_guess(self) -> None:
        '''
        Takes the user's guess and performs actions on it to progress the game
        Prompts for a new answer if the guess is not a 5-letter English word found in the dictionary
        Uses guess to generate data which it displays using color-coded letters
        Ends the gameplay loop if the answer is guessed or the maximum of 6 guesses is reached
        This is the main driver of gameplay progress
        '''
        if self.guesses_made < 6:
            guess = self.entry_guess.text().strip().upper()
            if not guess.isalpha():
                self.label_error_display.setText("Guesses must only contain letters.")
            elif len(guess) != 5:
                self.label_error_display.setText("Guesses must be 5 letters long.")
            elif guess not in self.all_words:
                self.label_error_display.setText(f"{guess.title()} is not an English word.")
            else:
                self.label_error_display.setText('')
                self.check_against_answer(guess)
                self.label_previous_title.setVisible(True)
                self.guess_label_group[self.guesses_made].setVisible(True)
                for letter in self.letter_array[self.guesses_made]:
                    letter.setVisible(True)
                if self.checkBox_helper_toggle.isChecked():
                    self.remaining_words = self.helper_info.get_possible_words(self.remaining_words)
                    self.all_possibilities.setText(f"Possible words:\n{'  '.join(self.remaining_words)}")
                self.entry_guess.setText('')
                self.guesses_made += 1
                if guess == self.answer or self.guesses_made == 6:
                    self.label_answer_title.setVisible(True)
                    self.label_answer.setVisible(True)
                    self.all_possibilities.setText('')
                    self.all_possibilities.setVisible(False)
                    self.label_congrats_answer.setText(f"The answer was {self.answer}")
                    if guess == self.answer:
                        self.label_congrats_guesses.setText(f"You got it in {self.guesses_made} guesses!")
                    else:
                        self.label_congrats_guesses.setText(f"Better luck next time!")
                    self.label_congrats_answer.setVisible(True)
                    self.label_congrats_guesses.setVisible(True)
                    with open("Project2/stats_data.txt", "r+") as file: # This file is 7 numbers separated by spaces
                        stats = file.readline().split()
                        stats[0] = str(int(stats[0]) + 1)
                        stats[self.guesses_made] = str(int(stats[self.guesses_made]) + 1)
                        file.seek(0)
                        file.write(' '.join(stats))