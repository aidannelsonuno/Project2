class WordleInfo:
    '''
    A class that contains data used for the wordle helper
    '''
    def __init__(self) -> None:
        '''
        Initializes data groups (green, yellow, and black)
        Green data is represented as a list of characters, letters in this list belong in that index in the answer
        Yellow data is a dictionary of letter/position pairs (char/list), where the letter is in the answer but not in any
            of the indexes in the position list
        Black data is a list of characters where none of the letters in the list are in the answer
        '''
        self.green = ['_', '_', '_', '_', '_']
        self.yellow = {}
        self.black = []

    def check_against_info(self, word: str) -> bool:
        '''
        Checks a candidate word against known information to determine if it can be the answer
        Returns True if the candidate word is a possible answer, and False if it is not
        :param word: The word being checked against known information
        :return: Result of whether the input word can be the answer (True/False)
        '''
        for letter in self.black:
            # Checks if there is a letter in the word that does not exist in the answer
            # Variable n counts how many times the black letter has already been accounted for
            n = 0
            for i in self.green:
                if i == letter:
                    n += 1
            if letter in self.yellow:
                n += len(self.yellow[letter])
            # If there are more of that letter than accounted for, the word cannot be the answer
            if word.count(letter) > n:
                return False
        for i, letter in enumerate(self.green):
            # Checks if the known positions within the word are matched correctly
            if letter != '_' and letter != word[i]:
                return False
        for key, [y_duplicity, y_indices] in self.yellow.items():
            for i in y_indices:
                # Checks if a letter in the checked word is in an incorrect position
                if word[i] == key:
                    return False
            if word.count(key) < y_duplicity + ''.join(self.green).count(key):
                # Checks if a known letter in the answer exists in the checked word enough times
                return False
        return True
    
    def process_input_info(self, word: str, colors: str) -> None:
        '''
        Takes a guess and the colors the wordle program used for it and sorts it into usable data
        This data is stored in the instance variables self.green, self.yellow and self.black
        :param word: The user's guess
        :param colors: The colors given by the Wordle program
        '''
        if len(word) != len(colors):
            raise ValueError("ValueError: Word and colors must be of the same length")
        dupe_info = {}
        for letter in self.yellow:
            dupe_info.update({letter: 0})
        for i, letter in enumerate(word):
            if colors[i] == 'G':
                self.green[i] = letter
                if letter in self.yellow:
                    self.yellow[letter][0] -= 1
            elif colors[i] == 'Y':
                if letter in self.yellow:
                    self.yellow[letter][1].append(i)
                    dupe_info[letter] += 1
                else:
                    self.yellow.update({letter: [0, [i]]})
                    dupe_info.update({letter: 1})
            elif letter not in self.black:
                self.black.append(letter)
        for letter, n in dupe_info.items():
            self.yellow[letter][0] = max(n, self.yellow[letter][0])
        for letter, val in self.yellow.copy().items():
            if val[0] == 0:
                del self.yellow[letter]

    def get_possible_words(self, all_words: list) -> list:
        '''
        Takes a list of all possibilities for the answer and reduces it based on the known information
        :param all_words: A list of all words that are known to be answer candidates
        :return: An updated list of all answer candidates based on known information from guesses
        '''
        possible_words = []        
        for word in all_words:
            if self.check_against_info(word):
                possible_words.append(word)
        return possible_words
