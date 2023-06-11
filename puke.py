from GM import GameManager as GM

info_list = [{'name': 'boxi', 'cash': 500, 'type': 'human'},
				{'name': 'cj', 'cash': 500, 'type': 'calling_machine'},
				{'name': 'lonely', 'cash': 500, 'type': 'card_sharp'},
				# {'name': 'gls', 'cash': 500, 'type': 'probabilist'},
				{'name': 'lazy_gls', 'cash': 500, 'type': 'estimator'}]

def START(gm):

	op = input("[GM] >> Enter [y] to start: ").strip().upper()
	if op == 'Y':
		gm.INIT()
		gm.PLAY()

	START(gm)

if __name__ == '__main__':

	print('[GM] << Welcome to PEACH & PLUM Casino.')

	gm = GM(blind=[5,10], mode='slow_play', disp=False)
	gm.LOAD(len(info_list) + 0, info_list, p_disp=False)

	START(gm)