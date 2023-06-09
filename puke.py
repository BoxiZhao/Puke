from GM import GameManager as GM

if __name__ == '__main__':

	info_list = [{'name': 'boxi', 'cash': 500, 'type': 'human'},
					{'name': 'lonely', 'cash': 500, 'type': 'calling_machine'},
					{'name': 'cj', 'cash': 500, 'type': 'calling_machine'},
					{'name': 'gls', 'cash': 500, 'type': 'calling_machine'}]

	gm = GM()
	gm.LOAD(len(info_list), info_list)

	while 1:
		gm.INIT()
		gm.PLAY()