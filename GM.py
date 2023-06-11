import random
import numpy as np
import time
import matplotlib.pyplot as plt
from PIL import Image

from Player import Player, HumanPlayer, Probabilist, CardSharp, Estimator
import Calculator as Cal

class GameManager:

    def __init__(self, blind=[5,10], mode='slow_play', disp=False):

        self.blind = blind
        self.mode = mode
        self.default_player_type = 'calling_machine'        # default(calling_machine) / human / card_sharp / probabilist / estimator
        self.disp = disp

        self.players = []
        self.name_list = []
        self.deck = []
        self.community_cards = []
        self.state = 0
        self.pot = 0

    def LOAD(self, n_player, info_list=[], p_disp=False):

        self.players = []
        self.name_list = []

        if self.mode == 'slow_play':
            print("[GM] Loading players", end='')
            for i in range(3):
                print('.', end='')
                time.sleep(0.3)
            print()

        for i in range(n_player):

            player_type = self.default_player_type
            if i < len(info_list):
                name = info_list[i]['name']
                cash = info_list[i]['cash']
                player_type = info_list[i]['type']
            else:
                print("[GM] >> Registration for Player No." + str(i))
                name = input('name: ').strip()
                cash = int(input('cash: ').strip())
                player_type = input('player type: ').strip().lower()
            if player_type == 'human':
                player = HumanPlayer(name, cash, i)
            elif player_type == 'card_sharp':
                player = CardSharp(name, cash, i)
            elif player_type == 'probabilist':
                player = Probabilist(name, cash, i, display=p_disp)
            elif player_type == 'estimator':
                player = Estimator(name, cash, i, display=p_disp)
            else:
                player = Player(name, cash, i)

            self.players.append(player)
            self.name_list.append(name)
            print('[' + name + '] successfully registered as', player_type.upper())

            if self.mode == 'slow_play':
                time.sleep(0.3)

    def INIT(self):

        self.deck = []
        self.community_cards = []
        self.state = 0
        self.pot = 0

        if self.mode == 'slow_play':
            print("[GM] Shuffling", end='')
            for i in range(3):
                print('.', end='')
                time.sleep(0.3)
            print()

        random.seed(time.time())
        for suit in Cal.suits:
            for rank in Cal.ranks:
                self.deck.append(f'{rank}{suit}')
        random.shuffle(self.deck)

        for player in self.players:
            player.on_table = 1
            player.deal(self.deck[-2:])
            self.deck = self.deck[:-2]

    def PLAY(self):

        op = input("[GM] >> Continue[c] or Chek one's hand[name]: ").strip()

        if self.state == 3 and op == 'c':
            self.showresult()
            self.state = 0
            return

        elif op == 'c':
            if self.state == 0:
                self.polling()
            self.community_cards += self.deck[Cal.deal_list[self.state]:]     # 0: -3, 1: -1, 2: -1
            self.deck = self.deck[:Cal.deal_list[self.state]]
            self.showcards('Community cards:', self.community_cards)
            self.state += 1
            self.polling()
 
        elif op in self.name_list:
            player = self.players[self.name_list.index(op)]
            self.showcards(op + '\'s hand:', player.hand)
            print(op + '\'s cash:', player.cash)

        else:
            print("U r isolated.")

        self.PLAY()

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
                    bet_raise, bet_add = player.action(self, bet_level, mandatory=self.blind[0])
                elif self.state == 0 and bet_level == 5:
                    bet_raise, bet_add = player.action(self, bet_level, mandatory=self.blind[1])
                elif player.on_table == 1 and (player.bet != bet_level or bet_level == 0):        # not fold nor all in
                    bet_raise, bet_add = player.action(self, bet_level)
                elif (player.bet != bet_level or bet_level == 0):
                    player.showon()

                self.pot += max(0, bet_add)
                if bet_raise > 0:
                    bet_level += bet_raise
                    ready = False

    def showresult(self):

        print('----- Result -----')
        print('Community cards:', self.community_cards)
        hands, numbers = [], []
        for player in self.players:
            if player.on_table == 0:
                continue
            print(player.name, '\'s hand: ', player.hand, Cal.check(player.hand, self.community_cards)[0])
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
            print(player.name, '\'s cash:', player.cash)
        print('------------------')

    def findimg(self, card):

        card_name = str(Cal.r2n[card[0]]) + '_of_' + Cal.s2n[card[1]]
        return './png/' + card_name + '.png', './png/face.png'

    def showcards(self, title, cards):

        print(title, end=' ')
        for card in cards:
            print(card, end=' ')
        print()

        if not self.disp:
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
