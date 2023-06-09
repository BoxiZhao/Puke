import random
import numpy as np
import time
import matplotlib.pyplot as plt
from PIL import Image

from Player import Player, HumanPlayer
import Calculator as Cal

class GameManager:

    def __init__(self):

        self.blind = [5, 10]
        self.mode = 'slow_play'
        self.default_player_type = 'calling_machine'        # human or not
        self.disp = False

        self.players = []
        self.name_list = []
        self.deck = []
        self.community_cards = []
        self.state = 0
        self.pot = 0

    def LOAD(self,  n_player, info_list=[]):

        self.players = []
        self.name_list = []

        for i in range(n_player):
            player_type = self.default_player_type
            if i < len(info_list):
                name = info_list[i]['name']
                cash = info_list[i]['cash']
                player_type = info_list[i]['type']
            else:
                name = input('name: ').strip()
                cash = int(input('cash: ').strip())
            if player_type == 'human':
                player = HumanPlayer(name, cash, i)
            else:
                player = Player(name, cash, i)
            self.players.append(player)
            self.name_list.append(name)

    def INIT(self):

        self.deck = []
        self.community_cards = []
        self.state = 0
        self.pot = 0

        if self.mode == 'slow_play':
            print("[GM] << Shuffling", end=' ')
            for i in range(3):
                print('.', end=' ')
                time.sleep(0.3)
            print()

        for suit in Cal.suits:
            for rank in Cal.ranks:
                self.deck.append(f'{rank}{suit}')
        random.shuffle(self.deck)

        for player in self.players:
            player.deal(self.deck[-2:])
            self.deck = self.deck[:-2]

    def PLAY(self):

        while 1:

            op = input("[GM] >> Continue[c] or Chek one's hand[name]: ").strip()

            if self.state == 3 and op == 'c':
                self.showresult()
                self.state = 0
                return

            elif op == 'c':
                if self.state == 0:
                    self.polling()
                self.community_cards = self.deck[-3 - self.state:]
                self.showcards('Community cards: ', self.community_cards)
                self.state += 1
                self.polling()

            elif op in self.name_list:
                player = self.players[self.name_list.index(op)]
                self.showcards(op + '\'s hand: ', player.hand)
                print(op + '\'s cash: ', player.cash)

            else:
                print("U r isolated.")

    def polling(self):

        print("---- Poll ", self.state, " ----")

        bet_level = 0
        ready = False

        for player in self.players:
            player.bet = 0
            player.raised = False

        while not ready:
            ready = True

            for player in self.players:

                bet_add, bet_raise = 0, 0
                if self.mode == 'slow_play':
                    time.sleep(0.3)

                if self.state == 0 and bet_level == 0:
                    bet_raise, bet_add = player.action(bet_level, mandatory=self.blind[0])
                elif self.state == 0 and bet_level == 5:
                    bet_raise, bet_add = player.action(bet_level, mandatory=self.blind[1])
                elif player.on_table == 1 and (player.bet != bet_level or bet_level == 0):        # not fold nor all in
                    bet_raise, bet_add = player.action(bet_level)

                self.pot += bet_add
                if bet_raise > 0:
                    bet_level += bet_raise
                    ready = False

    def findimg(self, card):

        card_name = str(Cal.ranks2name.get(card[1])) + '_of_' + Cal.suits2name.get(card[0])
        return './png/' + card_name + '.png', './png/face.png'

    def showresult(self):

        print('----- Result -----')
        print('Community cards:', self.community_cards)
        hands, numbers = [], []
        for player in self.players:
            if player.on_table == 0:
                continue
            print(player.name, '\'s hand: ', player.hand, ' ', Cal.check(player.hand, self.community_cards))
            hands.append(player.hand)
            numbers.append(player.num)
        winners = Cal.compare(hands, self.community_cards)
        income = self.pot / len(winners)
        print("Winner:", end=' ')
        for winner in winners:
            self.players[numbers[winner]].cash += income
            print(self.players[numbers[winner]].name, end=' ')
        print('+', income, end=' ')
        if len(winners) > 1:
            print('(each)', end=' ')
        print()
        print('------------------')
        for player in self.players:
            print(player.name, '\'s cash: ', player.cash)
        print('------------------')

    def showcards(self, title, cards):

        if not self.disp:
            print(title, cards)
            return

        fig = plt.figure(figsize=(10, 5))
        fig.canvas.manager.set_window_title(title)
        fig.patch.set_facecolor('green')
        i = 0
        for card in cards:
            i = i + 1
            card_fc, card_bk = self.findimg(card)
            plt.subplot(1, 5, i)
            plt.imshow(Image.open(card_bk))
            plt.imshow(Image.open(card_fc))
            plt.axis('off')
        plt.show()
