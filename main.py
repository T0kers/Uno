import random
from card import *
from player import Player


class Uno:
    players = []

    def __init__(self, player_names, starting_cards=7, pass_amount=3, rev_becomes_skip=True, choice_plus_interchangeable=False):
        self.stack = [Card(color=random.choice((RED, GREEN, BLUE, YELLOW)), value=random.randint(0, 9))]

        for name in player_names:
            Uno.players.append(Player(name, player_names, self.stack))

    def play(self):
        end_game = False
        while True:
            for player in self.players:

                skipped = False

                Player.reverse_left -= 1
                if Player.reverse_left > 0:
                    skipped = True
                else:
                    if Player.reverse:
                        Player.reverse_left = len(self.players) - 1

                if not skipped and not player.done:
                    print(f'\n{display_cards(self.stack[-1])}\n')
                    print(player.name)
                    if player.take_turn():
                        pass
                    else:
                        print('\nGame finished!')
                        end_game = True
                        break
            if end_game:
                break


def main():
    names = ['Player1', 'Player2', 'Player3']
    game = Uno(names)
    game.play()


if __name__ == '__main__':
    main()

# normal cards
# color = red, green, blue, yellow
# value = int 1-9

# +2
# color = same as normal
# value = '+2'

# skip
# color = same as normal
# value = 'skip'

# uno reverse
# color = same as normal
# value = 'rev'