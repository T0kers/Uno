from colorama import Fore
from colorama import Style

RED = 'red'
GREEN = 'green'
BLUE = 'blue'
YELLOW = 'yellow'
CHOICE = 'choice'

colors = {
    RED: Fore.LIGHTRED_EX,
    GREEN: Fore.LIGHTGREEN_EX,
    BLUE: Fore.LIGHTBLUE_EX,
    YELLOW: Fore.LIGHTYELLOW_EX,
    CHOICE: Fore.RESET
          }


# For fx +2 or +4 cards
def PLUS(number):
    return f'+{number}'


SKIP = 'skip'
REVERSE = 'rev'


class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __repr__(self):
        return f'{self.color} {self.value}'


def color_text(text, color):
    return f'{colors[color]}{text}{Style.RESET_ALL}'


def display_cards(cards):
    line_1 = ''
    line_2 = ''
    line_3 = ''
    line_4 = ''

    if type(cards) != list:
        cards = [cards]
    for card in cards:
        card_space = '  '

        line_1 += color_text(' ___ ', card.color) + card_space

        try:
            card_line_2 = f'|{card.color[0:3]}|' + card_space
        except TypeError:
            card_line_2 = '|###|' + card_space

        line_2 += color_text(card_line_2, card.color)

        if type(card.value) == int:
            card_line_3 = f'| {card.value} |'
        elif card.value == SKIP:
            card_line_3 = '| Ø |'
        elif card.value == REVERSE:
            card_line_3 = '|< >|'
        elif card.value == PLUS(2):
            card_line_3 = '|+2 |'
        elif card.value == PLUS(4):
            card_line_3 = '|+4 |'
        elif card.value is None and card.color == CHOICE:
            card_line_3 = '| C |'
        else:
            if card.value is None:
                value = '###'
            else:
                value = f'{card.value}' + '   '
            card_line_3 = f'|{value[0:3]}|'
        line_3 += color_text(card_line_3, card.color) + card_space

        line_4 += color_text('|___|', card.color) + card_space
    return f'{line_1}\n{line_2}\n{line_3}\n{line_4}'


#  ___
# |   |
# | 4 |
# |___|

#  ___
# |   |
# | 7 |
# |___|

#  ___
# |   |
# | Ø |
# |___|

#  ___
# |   |
# |< >|
# |___|

#  ___
# |   |
# |+2 |
# |___|

#  ___
# |   |
# |+4 |
# |___|

#  ___
# |   |
# | C |
# |___|

#  ___
# |   |
# | # |
# |___|
