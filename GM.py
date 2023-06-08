import random
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from Player import Player

class GameManager:

    def __init__(self):

        self.suits = ['h', 's', 'd', 'c']       # 9829 ♥ 9824 ♠ 9830 ♦ 9827 ♣
        self.suits2name = {'h': 'hearts', 's': 'spades', 'd': 'diamonds', 'c': 'clubs'}
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        self.ranks2name = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 'jack', 'Q': 'queen',  'K': 'king', 'A': 'ace'}
        self.deal_list = [-3, -4, -5]

        self.players = []
        self.name_list = []
        self.deck = []
        self.community_cards = []
        self.state = 0

    def START(self):

        name_list = ['boxi', 'lonely']
        cash_list = [50, 50]
        self.loadplayers(name_list, cash_list)
        self.name_list = name_list

        for suit in self.suits:
            for rank in self.ranks:
                self.deck.append(f'{rank}{suit}')
        random.shuffle(self.deck)

        for player in self.players:
            player.deal(self.deck[-2:])
            self.deck = self.deck[:-2]

        while 1:

            op = input("Continue[y] or Chek one's hand[name]: ").strip()

            if self.state == 3 and op == 'y':
                self.showresult()
                self.state = 0

            elif op == 'y':
                self.community_cards = self.deck[self.deal_list[self.state]:]
                self.showcards(self.community_cards, 'Community cards: ')
                self.state += 1

            elif op in name_list:
                player = self.players[self.name_list.index(op)]
                self.showcards(op + '\'s hand', player.hand)

            else:
                print("U r isolated.")

    def loadplayers(self, name_list, cash_list):

        for i in range(len(name_list)):
            player = Player(name_list[i], cash_list[i], i)
            self.players.append(player)

    def findimg(self, card):

        card_name = str(self.ranks2name.get(card[1])) + '_of_' + self.suits2name.get(card[0])
        return './png/' + card_name + '.png', './png/face.png'

    def showresult(self):

        print('----- Result -----')
        print('Community cards:', self.community_cards)
        for player in self.players:
            print(player.name, '\'s hand: ', player.hand, ' ', self.check(player.hand))
        print('------------------')

    def showcards(self, cards, title):

        """
        fig = plt.figure(figsize=(10,5))
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
        """
        print(title, cards)

    def anynum(self, arr, num, bigger=0):

        if bigger > 0:
            return any(arr.count(i) > num for i in arr)
        return any(arr.count(i) == num for i in arr)

    def check(self, hands):

        r2i = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        cards_type = ['Straight Flush', 'Four of a Kind', 'Full House', 'Flush', 'Straight', 'Three of a Kind', 'Two pairs', 'One pair', 'High card']       # 9 Types

        is_type = [0, 0, 0, 0, 0, 0, 0, 0, 1]
        cards = hands + self.community_cards
        cards.sort(key=lambda card: self.ranks.index(card[0]))
        cards_suit = [card[1] for card in cards]
        cards_rank = [r2i[card[0]] for card in cards]

        is_type[3] = self.anynum(cards_suit, 4, bigger=1)        # Flush 3

        rank_set = np.array(list(set(cards_rank)))        # Straight 4
        if rank_set[-1] == r2i['A']:
            np.insert(rank_set, 0, 1)        # add Ace as 1 for straight A2345
        if len(rank_set) > 4:
            for i in range(4):
                rank_set = rank_set[1:] - rank_set[:-1]        # only straights remain 0
            is_type[4] = np.any(rank_set == 0)

        if is_type[4] and is_type[3]:        # Straight Flush 0
            for i in range(3):
                st = [i]
                for j in range(i + 1, len(cards_rank)):
                    if cards[j][1] == cards[i][1] and r2i[cards[j][0]] == r2i[cards[st[-1]][0]] + 1:
                        st.append(j)
                is_type[0] = is_type[0] or len(st) > 4

        is_type[1] = self.anynum(cards_rank, 4)        # Four of a Kind 1

        is_type[2] = self.anynum(cards_rank, 3) and self.anynum(cards_rank, 2)        # Full House 2

        is_type[5] = self.anynum(cards_rank, 3)        # Three of a Kind 5

        is_type[6] = sum(cards_rank.count(rank) == 2 for rank in cards_rank) > 3        # Two pairs 6

        is_type[7] = self.anynum(cards_rank, 2)        # One pair 7

        for i in range(9):
            if is_type[i] > 0:
                return cards_type[i]
