import Calculator as Cal

class Player():

    def __init__(self, name, cash, num, display=False):

        self.display = display
        self.name = name
        self.cash = cash
        self.num = num
        self.hand = []
        self.on_table = 1       # on = 1, fold = 0, all in = -1
        self.bet = 0
        self.raised = False

    def deal(self, cards):

        self.hand = cards

    def action(self, GM, bet_level, mandatory=0):       # calling machine

        if mandatory > 0:
            print('[' + self.name + ']', '<< blind: ', mandatory)
            self.cash = max(self.cash - mandatory, 0)
            self.bet += mandatory
            return self.bet - bet_level, mandatory

        self.bet, last_bet = self.getaction(bet_level, GM)
        self.cash -= max(0, self.bet) - last_bet

        self.showaction(bet_level)
        return max(0, self.bet) - bet_level, max(0, self.bet) - last_bet

    def getaction(self, bet_level, GM):     # call or fold, don't all in

        if bet_level - self.bet < self.cash:
            return bet_level, self.bet

        self.on_table = 0
        return self.bet, self.bet

    def showaction(self, bet_level):

        print('[' + self.name + ']', '<<', end=' ')
        if self.cash == 0:
            print('ALL IN ', self.bet)
        elif self.bet < bet_level:
            print('FOLD')
        elif self.bet == bet_level == 0:
            print('check')
        elif self.bet == bet_level:
            print('call')
        else:
            print('raise to ', self.bet)

    def showon(self):

        print('[' + self.name + ']', end=' ')
        if self.on_table == -1:
            print('ALL IN')
        elif self.on_table == 0:
            print('FOLD')
        else:
            print('ON')

class HumanPlayer(Player):      # ask before action

    def getaction(self, bet_level, GM):

        last_bet = self.bet
        print('[' + self.name + ']', end=' ')
        print('bet level:', bet_level, end=', ')
        print('your last bet:', last_bet)

        while 1:        # A for ALL IN, F for FOLD, C for CALL

            print('[' + self.name + ']', '>>', end=' ')
            op = input('bet (raise to): ').strip().upper()
            amount = -2
            if op.isdigit():
                amount = int(eval(op))
            if op == 'A' or amount - last_bet == self.cash:
                self.bet += self.cash
                self.on_table = -1
                break
            elif op == 'F' or amount == -1:
                self.bet = -1
                self.on_table = 0
                break
            elif amount > bet_level and self.raised:
                print("U can\'t raise again.")
            elif amount > bet_level and amount - last_bet > self.cash:
                print("U have only ", self.cash, " left")
            elif (op == 'C' or amount == bet_level) and bet_level - last_bet > self.cash:
                print("U have only ", self.cash, " left")
            elif amount >= bet_level:
                self.bet = amount
                break
            elif op == 'C' or amount == bet_level:
                self.bet = bet_level
                break
            else:
                print("Invalid bet. ")

        self.raised = self.raised or self.bet > bet_level
        return self.bet, last_bet

class CardSharp(Player):        # know the result

    def getresult(self, GM):

        com = GM.community_cards
        if len(com) < 5:
            com = com + GM.deck[-1 * (5 - len(com)):]
        hands, numbers = [], []
        for player in GM.players:
            if player.on_table != 0:
                hands.append(player.hand)
                numbers.append(player.num)
        winners = Cal.compare(hands, com)
        for winner in winners:
            if numbers[winner] == self.num:
                return True
        return False

    def getaction(self, bet_level, GM):

        last_bet = self.bet
        if self.getresult(GM):       # call if win
            return bet_level, last_bet

        self.on_table = 0
        return self.bet, last_bet

class Probabilist(Player):      # Calculate the exact p_win

    def getprob(self, com, GM, removed=[]):

        self_score = Cal.score(self.hand, com)
        self_type = 8 - self_score // 16 ** 5
        if self.display:
            print(self_type, end='')
        n_win, n_total = 0, 0
        n_deck = len(GM.deck)

        for i in range(n_deck):
            if i in removed:
                continue
            for j in range(n_deck):
                if j in removed or j == i:
                    continue
                n_total += 1
                if self_score >= Cal.score([GM.deck[i], GM.deck[j]], com, cutoff=self_type):     # tie is win
                    n_win += 1

        return n_win * 1.0 / n_total

    def makedecision(self, p_win, bet_level, GM):

        n_player = len(GM.players)      # ignore folders
        p_win = p_win ** n_player
        E_win = p_win * GM.pot
        E_lose = (1 - p_win) * bet_level
        
        if E_win > E_lose and bet_level - self.bet < self.cash:      # call or fold
            return bet_level

        self.on_table = 0
        return self.bet

    def getaction(self, bet_level, GM):

        last_bet = self.bet
        com = GM.community_cards

        if len(com) == 0:      # just call before flop
            return bet_level, self.bet

        print('[' + self.name + ']', 'Calculating...', end=' ')

        if len(com) == 3:
            p_win = 0
            n_deck = len(GM.deck)
            for i in range(n_deck):
                if self.display and i % 5 == 0:
                    print('\n<' + str(i), end = '> ')
                for j in range(i + 1, n_deck):
                    p_win += self.getprob(com + [GM.deck[i], GM.deck[j]], GM, [i, j])
            p_win /= 0.5 * n_deck * (n_deck - 1)

        if len(com) == 4:
            p_win = 0
            n_deck = len(GM.deck)
            for i in range(n_deck):
                p_win += self.getprob(com + [GM.deck[i]], GM, [i])
            p_win /= n_deck

        if len(com) == 5:
            p_win = self.getprob(com, GM)

        print('\n[' + self.name + ']', 'p_win:', round(p_win, 3))
        self.bet = self.makedecision(p_win, bet_level, GM)
        return self.bet, last_bet

class Estimator(Probabilist):       # Estimate p_win

    def getprob(self, com, GM, removed=[]):

        self_type, _ = Cal.check(self.hand, com)
        if self.display:
            print(Cal.t2i[self_type], end='')
        return 1 - 0.01 * Cal.prob_sum[Cal.t2i[self_type]]