import numpy as np
from functools import cmp_to_key as c2k

suits = ['h', 's', 'd', 'c']	   # 9829 ♥ 9824 ♠ 9830 ♦ 9827 ♣
s2i = {'h': 0, 's': 1, 'd': 2, 'c': 3}
suits2name = {'h': 'hearts', 's': 'spades', 'd': 'diamonds', 'c': 'clubs'}
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
ranks2name = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 'jack', 'Q': 'queen',  'K': 'king', 'A': 'ace'}
r2i = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
cards_type = ['Straight Flush', 'Four of a Kind', 'Full House', 'Flush', 'Straight', 'Three of a Kind', 'Two pairs', 'One pair', 'High card']  # 9 Types
t2i = {'Straight Flush': 0, 'Four of a Kind': 1, 'Full House': 2, 'Flush': 3, 'Straight': 4, 'Three of a Kind': 5, 'Two pairs': 6, 'One pair': 7, 'High card': 8}  # 9 Types
deal_list = [-3, -1, -1]

def cmp(a, b):		# a b are cards, < -1, == 0, > 1

	if r2i[a[0]] < r2i[b[0]]:
		return -1
	if r2i[a[0]] > r2i[b[0]]:
		return 1
	if s2i[a[1]] < s2i[b[1]]:
		return -1
	if s2i[a[1]] > s2i[b[1]]:
		return 1
	return 0

def anynum(arr, arr_count, num):

	return any(arr_count[i] == num for i in arr)

def c2i(card):

	return (r2i[card[0]] - 2) * 4 + s2i[card[1]]

def putmajor(n, arr_set, cards_arr, arr_choose, start_pos=0):

	for arr in arr_set:
		if cards_arr.count(arr) == n and arr != arr_choose[0]:
			arr_choose[start_pos : start_pos + n] = [arr] * n		# continue to find the biggest
	return arr_choose

def putminor(n, arr_set, cards_arr, arr_choose):

	tp = 0
	for i in range(len(cards_arr)):
		if cards_arr[-i - 1] != arr_choose[0] and tp < n:
			arr_choose[5 - n + tp] = cards_arr[-i - 1]
			tp += 1
	return arr_choose

def check(hand, community_cards, cutoff=0):

	is_type = [False, False, False, False, False, False, False, False, True]  # at least High card
	cards = hand + community_cards
	cards.sort(key=c2k(cmp))
	cards_suit = [card[1] for card in cards]
	suit_count = [cards_suit.count(suit) for suit in suits]
	cards_rank = [r2i[card[0]] for card in cards]
	rank_set = np.array(list(set(cards_rank)))
	rank_choose = [[0] * 5] * 9
	rank_count = [cards_rank.count(i) for i in range(16)]

	if any(suit_count[i] > 4 for i in range(4)):  # Flush 3
		is_type[3] = True
		if cutoff > 3:
			return cards_type[3], rank_choose[3]
		for suit in suits:
			if cards_suit.count(suit) > 4:
				rank_choose[3] = [r2i[card[0]] for card in cards if card[1] == suit][-5:][::-1]
				break

	rank_set_plus = rank_set.copy()
	if rank_set[-1] == r2i['A']:  # Straight 4
		rank_set_plus = np.insert(rank_set, 0, 1)  # add Ace as 1 for straight A2345
	for i in range(len(rank_set_plus) - 4):
		if rank_set_plus[i] == rank_set_plus[i + 1] - 1 == rank_set_plus[i + 2] - 2 == rank_set_plus[i + 3] - 3 == rank_set_plus[i + 4] - 4:
			is_type[4] = True
			if cutoff > 4:
				return cards_type[4], rank_choose[4]
			rank_choose[4] = list(range(rank_set_plus[i], rank_set_plus[i] + 5))		# continue to find the biggest

	if is_type[4] and is_type[3]:  # Straight Flush 0
		for i in range(3):
			st = [i]
			for j in range(i + 1, len(cards)):
				if cards[j][1] == cards[i][1] and r2i[cards[j][0]] == r2i[cards[st[-1]][0]] + 1:
					st.append(j)
			if len(st) > 4:
				is_type[0] = True
				rank_choose[0] = list(range(r2i[cards[i][0]], r2i[cards[i][0]] + 5))
			elif len(st) == 4 and cards[i][0] == '2' and 'A' + cards[i][1] in cards:
				is_type[0] = True
				rank_choose[0] = list(range(1, 6))
			if is_type[0] and cutoff > 0:
				return cards_type[0], rank_choose[0]

	if anynum(cards_rank, rank_count, 4):  # Four of a Kind 1
		is_type[1] = True
		if cutoff > 1:
			return cards_type[1], rank_choose[1]
		rank_choose[1] = putmajor(4, rank_set, cards_rank, rank_choose[4])

	elif anynum(cards_rank, rank_count, 3) and anynum(cards_rank, rank_count, 2):  # Full House 2
		is_type[2] = True
		if cutoff > 2:
			return cards_type[2], rank_choose[2]
		rank_choose[2] = putmajor(3, rank_set, cards_rank, rank_choose[2])
		rank_choose[2] = putmajor(2, rank_set, cards_rank, rank_choose[2], start_pos=3)
	
	elif anynum(cards_rank, rank_count, 3):  # Three of a Kind 5
		is_type[5] = True
		if cutoff > 5:
			return cards_type[5], rank_choose[5]
		rank_choose[5] = putmajor(3, rank_set, cards_rank, rank_choose[5])
		rank_choose[5] = putminor(2, rank_set, cards_rank, rank_choose[5])

	elif sum(rank_count[rank] == 2 for rank in rank_set) > 1:  # Two pairs 6
		is_type[6] = True
		if cutoff > 6:
			return cards_type[6], rank_choose[6]
		tp = 0
		for i in range(len(rank_set)):		# caution for 3 pairs
			if cards_rank.count(rank_set[-i - 1]) == 2 and tp < 4:
				rank_choose[6][tp : tp + 2] = [rank_set[-i - 1]] * 2
				tp += 2
		for rank in rank_set:
			if rank != rank_choose[6][0] and rank != rank_choose[6][2]:
				rank_choose[6][4] = rank

	elif anynum(cards_rank, rank_count, 2):  # One pair 7
		is_type[7] = True
		if cutoff > 7:
			return cards_type[7], rank_choose[7]
		rank_choose[7] = putmajor(2, rank_set, cards_rank, rank_choose[7])
		rank_choose[7] = putminor(3, rank_set, cards_rank, rank_choose[7])

	for i in range(8):
		if is_type[i] > 0:
			return cards_type[i], rank_choose[i]

	is_type[8] = True		# High card 8
	rank_choose[8] = putminor(5, rank_set, cards_rank, rank_choose[8])
	return cards_type[8], rank_choose[8]

def score(hand, community_cards, cutoff=0):

	card_type, rank_choose = check(hand, community_cards, cutoff)
	hash_score = 8 - t2i[card_type]
	for i in range(5):
		hash_score *= 16
		hash_score += rank_choose[i]

	return hash_score

def compare(hands, community_cards):	 # return the indice(s) of biggest number(s)

	num = []
	for hand in hands:
		num.append(score(hand, community_cards))
	winner = np.argmax(num)

	return [index for (index, value) in enumerate(num) if value == num[winner]]

if __name__ == '__main__':

	test_mat = [[['5s', '6h'], ['7s', '8s', 'Tc', 'Jd', 'As']],
	[['5s', '6h'], ['7s', '8s', 'Tc', 'Jd', 'Ts']],
	[['5s', '7h'], ['7s', '8s', 'Tc', 'Jd', 'Ts']],
	[['5s', 'Th'], ['7s', '8s', 'Tc', 'Jd', 'Ts']],
	[['5s', '6h'], ['4s', '3s', '2c', 'Jd', 'As']],
	[['Qs', '6h'], ['4s', '3s', '2s', 'Js', 'As']],
	[['5s', 'Th'], ['Js', '8s', 'Tc', 'Jd', 'Ts']],
	[['Td', 'Th'], ['Js', '8s', 'Tc', 'Jd', 'Ts']],
	[['5s', '6h'], ['4s', '3s', '2s', 'Jd', 'As']],
	[['5s'], ['4s', '3s', '2s', 'As']]]

	for test_hand, test_com in test_mat:
		print(check(test_hand, test_com), score(test_hand, test_com))
		# print(8 - score(test_hand, test_com) // 16 **5)