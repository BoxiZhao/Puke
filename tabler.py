import Calculator as Cal
import itertools
from functools import cmp_to_key as c2k

deck = []
for suit in Cal.suits:
	for rank in Cal.ranks:
		deck.append(f'{rank}{suit}')

for hand in itertools.combinations(['As', 'Ah'], 2):

	f = open('./table/' + hand[0] + hand[1] + '.txt', 'w')
	table = [[[0] * 52] * 52] * 52
	hand = list(hand)
	hand.sort(key=c2k(Cal.cmp))
	remove = [hand]

	trail_count = 0

	for com012 in itertools.combinations(deck, 3):

		com012 = list(com012)
		com012.sort(key=c2k(Cal.cmp))

		if len(hand) + len(com012) != len(set(hand + com012)):
			continue
		n_win, n_total = 0, 0
		remove.extend(com012)

		for com3 in deck:
			if com3 in remove:
				continue
			remove.append(com3)
			for com4 in deck:
				if com4 in remove:
					continue
				com = com012 + [com3] + [com4]
				self_score = Cal.score(hand, com)
				self_type = 8 - self_score // 16 ** 5
				remove.append(com4)

				for op0 in deck:
					if op0 in remove:
						continue
					remove.append(op0)
					for op1 in deck:
						if op1 in remove:
							continue
						n_total += 1
						if self_score >= Cal.score([op0, op1], com, cutoff=self_type):	 # tie is win
							n_win += 1

					remove.pop()
				remove.pop()
			remove.pop()
		remove = remove[:-3]

		p_win = round(n_win * 1.0 / n_total, 3)
		for i in range(3):
			f.write(str(Cal.c2i(com012[i])) + ' ')
		f.write(str(p_win) + '\n')

		trail_count += 1
		print(trail_count,'/ 22100 Completed.')

	f.close()
