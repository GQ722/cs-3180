from itertools import islice
import os
import random
import re
import string


class Board(object):
    """
    A Boggle board, outputtable to stdout. Randomly chooses consonants and
    vowels according to a certain board size, then outputs them.

    @author Kevin Porter
    """
    def computer_move(self):
        board_letters = ''.join(self.board_letters)
        board_letters.replace('Q', 'QU')
        # Below there be magic (compares board letters to words in dictionary)
        valid = re.compile('[' + board_letters + ']{4,}$', re.I).match
        words = set(word for word in self.dictionary if valid(word))
        score = 0
        score_dict = {}
        for word in words:
            word_score = self.score_word(word)
            score += word_score
            score_dict[word] = word_score
        return score_dict, score

    def display_board(self):
        for i in range(0, self.board_height):
            print(self.block_separator + (self.long_separator *
                                          self.board_width))
            output_str = ''
            for letter in islice(self.board_letters, i * self.board_width,
                                 i * self.board_width + 5):
                if letter == 'Q':
                    letter = 'Qu'
                output_str = output_str + self.block_separator + ' ' + letter
                if len(letter) < 2:
                    output_str = output_str + ' '
            output_str = output_str + self.block_separator
            print(output_str)
            if i == self.board_height - 1:
                print(self.block_separator + (self.long_separator *
                                              self.board_width))

    def gen_board(self):
        VOWELS = ['A', 'E', 'I', 'O', 'U']
        CONSONANTS = []
        for letter in string.ascii_uppercase:
            if letter not in VOWELS:
                CONSONANTS.append(letter)
        min_vowels = 7
        max_vowels = 13  # not inclusive
        vowel_count = random.randrange(min_vowels, max_vowels)
        consonant_count = self.board_size - vowel_count

        vowel_list = []
        while len(vowel_list) < vowel_count:
            vowel_list.append(random.choice(VOWELS))

        consonant_list = []
        while len(consonant_list) < consonant_count:
            consonant_list.append(random.choice(CONSONANTS))

        board_list = vowel_list + consonant_list
        random.shuffle(board_list)
        return board_list

    def is_word(self, word):
        is_word = False
        if word in self.dictionary:
            is_word = True
        '''
        Shouldn't be necessary?
        if word.endswith('S') and word - 'S' in self.dictionary:
            is_word = True
        if word.endswith('ES') and word - 'ES' in self.dictionary:
            is_word = True
        '''
        return is_word

    def is_legal(self, word):
        is_legal = False
        to_compare = word.replace('QU', 'Q')
        to_compare = list(to_compare)
        if (set(to_compare) & set(self.board_letters) ==
                set(to_compare)):
            is_legal = True
        return is_legal

    def play(self):
        self.display_board()
        player_words, player_score = self.player_move()
        computer_words, computer_score = self.computer_move()
        print('Player\'s words: ')
        for k, v in player_words.iteritems():
            print str(v).ljust(5), k.ljust(25)
        print('Player\'s total score: ' + str(player_score))
        print('Computer\'s words: ')
        for k, v in computer_words.iteritems():
            print str(v).ljust(5), k.ljust(25)
        print('Computer\'s total score: ' + str(computer_score))
        if player_score > computer_score:
            print('Player wins!')
        elif computer_score > player_score:
            print('Computer wins!')
        else:
            print('Tie! You both lose.')

    def player_move(self):
        user_input = raw_input('Enter as many distinct words from the board ' +
                               'as possible, separated by spaces: ')
        words = user_input.split(' ')
        score = 0
        score_dict = {}
        for word in words:
            word = word.upper()
            if self.is_word(word) and self.is_legal(word):
                word_score = self.score_word(word)
                score += word_score
                score_dict[word] = word_score
        return score_dict, score

    @staticmethod
    def score_word(word):
        score = 0
        if len(word) == 4:
            score = 1
        elif len(word) == 5:
            score = 2
        elif len(word) == 6:
            score = 3
        elif len(word) == 7:
            score = 5
        elif len(word) > 7:
            score = 11
        return score

    def __init__(self):
        self.board_width = 5
        self.board_height = 5
        self.board_size = self.board_width * self.board_height
        self.long_separator = '---|'
        self.block_separator = '|'

        self.board_letters = self.gen_board()
        self.dictionary = []
        with open('linuxwords.txt', 'r') as f:
            for line in f:
                for word in line.split():
                    self.dictionary.append(word.upper())

if not os.path.isfile('linuxwords.txt'):
    print('ERROR: Download and place linuxwords.txt in this script\'s ' +
          'directory.')
    quit()

board = Board()
board.play()
