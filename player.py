from card import *
import random


class Player:
    players_won = 0

    skip_players = 0

    plus_cards = 0

    reverse = False
    reverse_left = 0  # how many players more to skip, to effectively reverse direction

    def __init__(self, name, player_names, stack):
        self.cards = []
        for _ in range(7):
            self.take_random_card()

        self.name = name
        self.players = player_names
        self.stack = stack

        self.cards_layed = 0
        self.pass_amount = 0

        self.done = False

    def __str__(self):
        return f'{self.cards}'

    def lay_card(self, card_index):
        end_turn = False
        is_plus_card = False

        self.cards_layed += 1

        if self.cards[card_index].value == SKIP:
            Player.skip_players += 1
            end_turn = True
        elif self.cards[card_index].value == REVERSE:
            if len(self.players) > 2:  # hvis der kun er to personer fungere reverse som skip
                if Player.reverse:
                    Player.reverse = False
                    Player.reverse_left = 0
                else:
                    Player.reverse = True
                    Player.reverse_left = len(self.players) - 1
            else:
                Player.skip_players += 1

            end_turn = True
        elif type(self.cards[card_index].value) == str:
            if self.cards[card_index].value.startswith('+'):
                Player.plus_cards += int(self.cards[card_index].value[1:])
                is_plus_card = True

        if self.cards[card_index].color == CHOICE:
            while True:
                color = input('Choose color >')
                if color == RED or color == GREEN or color == BLUE or color == YELLOW:
                    self.cards[card_index].color = color
                    break
                else:
                    print('Please try again')
            if is_plus_card:  # hvis det er et choice +kort skal næste tage kort op uanset hvad, og må ikke lægge noget selv
                Player.skip_players += 1
            end_turn = True

        self.stack.append(self.cards[card_index])
        self.cards.pop(card_index)

        if end_turn:
            return True

        if self.cards:
            print(f'\n{display_cards(self.stack[-1])}\n')

    def take_random_card(self):
        choice = random.randint(1, 108)
        if choice <= 76:
            self.cards.append(Card(color=random.choice((RED, GREEN, BLUE, YELLOW)), value=random.randint(0, 9)))
        elif 77 <= choice <= 100:
            self.cards.append(
                Card(color=random.choice((RED, GREEN, BLUE, YELLOW)), value=random.choice((PLUS(2), REVERSE, SKIP))))
        else:
            self.cards.append(Card(color=CHOICE, value=random.choice((PLUS(4), None))))

    def check_card(self, card_index):
        if self.cards_layed == 0:
            if self.cards[card_index].color == self.stack[-1].color or (
                    self.cards[card_index].color == CHOICE and Player.plus_cards == 0) or self.cards[card_index].value == self.stack[-1].value:
                return True
            return False
        else:
            if self.cards[card_index].value == self.stack[-1].value:
                return True
            return False

    def take_turn(self):
        self.pass_amount = 0
        self.cards_layed = 0

        skipped = False

        if Player.skip_players > 0:
            Player.skip_players -= 1
            print('You have been skipped\n')
            cards_to_pick_up = Player.plus_cards
            while Player.plus_cards > 0:  # hvis spilleren skal skippes + der er plus_kort, skal personen tage kortene op, da det kun kan ske hvis der blev lagt en choice +kort ned
                Player.plus_cards -= 1
                self.take_random_card()
            print(f'You picked up {cards_to_pick_up} cards\n{display_cards(self.cards)}') if cards_to_pick_up > 0 else print('')
            skipped = True

        if len(self.players) - 1 <= Player.players_won:
            print('You lost :(')
            skipped = True
            self.done = True
            return False

        while not skipped:
            end_turn = False

            print(display_cards(self.cards))
            print(f'Plus cards: {Player.plus_cards}')
            command = input('>')
            if command.isdigit():
                command = int(command)
                if command < len(self.cards):
                    if self.check_card(command):
                        if self.lay_card(
                                command):  # Returner true hvis man ikke må ligge mere efter at have lagt kort, ved skip, reverse, change color og plus 4
                            end_turn = True  # Slutter turen
                    else:
                        print('You can\'t use that card')
            elif command == 'pass':
                if self.pass_turn():  # hvis man har passet tre gange, har lagt kort, eller samlet +kort op, returner den true, og turen stoppes
                    print(display_cards(self.cards))
                    end_turn = True
            elif command == 'end':
                while not self.pass_turn():
                    pass
                print(display_cards(self.cards))
                end_turn = True
            elif command == 'quit':
                self.done = True
                end_turn = True

            if not self.cards:
                Player.players_won += 1
                print(f'You finished in {Player.players_won}th place!')
                self.done = True
                break

            if end_turn:
                break
        return True

    def pass_turn(self):  # returner true hvis man kan end turen
        if self.cards_layed == 0:
            if self.pass_amount < 3:
                if Player.plus_cards > 0:
                    while Player.plus_cards > 0:
                        Player.plus_cards -= 1
                        self.take_random_card()
                    return True
                else:
                    self.take_random_card()
                    self.pass_amount += 1
            else:
                return True
        else:
            return True

