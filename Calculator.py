import numpy as np

suits = ['h', 's', 'd', 'c']       # 9829 ♥ 9824 ♠ 9830 ♦ 9827 ♣
suits2name = {'h': 'hearts', 's': 'spades', 'd': 'diamonds', 'c': 'clubs'}
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
ranks2name = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 'jack', 'Q': 'queen',  'K': 'king', 'A': 'ace'}
r2i = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
cards_type = ['Straight Flush', 'Four of a Kind', 'Full House', 'Flush', 'Straight', 'Three of a Kind', 'Two pairs', 'One pair', 'High card']  # 9 Types
t2i = {'Straight Flush': 0, 'Four of a Kind': 1, 'Full House': 2, 'Flush': 3, 'Straight': 4, 'Three of a Kind': 5, 'Two pairs': 6, 'One pair': 7, 'High card': 8}  # 9 Types

def anynum(arr, num, bigger=0):

    if bigger > 0:
        return any(arr.count(i) > num for i in arr)
    return any(arr.count(i) == num for i in arr)

def check(hand, community_cards):



    is_type = [False, False, False, False, False, False, False, False, True]  # at least High card
    cards = hand + community_cards
    cards.sort(key=lambda card: ranks.index(card[0]))
    cards_suit = [card[1] for card in cards]
    cards_rank = [r2i[card[0]] for card in cards]

    is_type[3] = anynum(cards_suit, 4, bigger=1)  # Flush 3

    rank_set = np.array(list(set(cards_rank)))  # Straight 4
    if rank_set[-1] == r2i['A']:
        np.insert(rank_set, 0, 1)  # add Ace as 1 for straight A2345
    if len(rank_set) > 4:
        is_type[4] = True
        for i in range(4):
            rank_set = rank_set[1:] - rank_set[:-1]
            is_type[4] = is_type[4] and (i < 1 or np.any(rank_set == 0))  # only straights always have 0 after 1 cycle

    if is_type[4] and is_type[3]:  # Straight Flush 0
        for i in range(3):
            st = [i]
            for j in range(i + 1, len(cards_rank)):
                if cards[j][1] == cards[i][1] and r2i[cards[j][0]] == r2i[cards[st[-1]][0]] + 1:
                    st.append(j)
            is_type[0] = is_type[0] or len(st) > 4

    is_type[1] = anynum(cards_rank, 4)  # Four of a Kind 1

    is_type[2] = anynum(cards_rank, 3) and anynum(cards_rank, 2)  # Full House 2

    is_type[5] = anynum(cards_rank, 3)  # Three of a Kind 5

    is_type[6] = sum(cards_rank.count(rank) == 2 for rank in cards_rank) > 3  # Two pairs 6

    is_type[7] = anynum(cards_rank, 2)  # One pair 7

    for i in range(9):
        if is_type[i] > 0:
            return cards_type[i]

def compare(hands, community_cards):     # return the indice(s) of biggest number(s)

    num = []
    for hand in hands:
        num.append(t2i[check(hand, community_cards)])
    winner = np.argmin(num)

    return [index for (index, value) in enumerate(num) if value == num[winner]]
