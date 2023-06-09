class Player():

    def __init__(self, name, cash, num):
        self.name = name
        self.cash = cash
        self.num = num
        self.hand = []
        self.on_table = 1       # on = 1, fold = 0, all in = -1
        self.bet = 0
        self.raised = False

    def deal(self, cards):
        self.hand = cards

    def action(self, bet_level, mandatory=0):       # CallingMachine

        if mandatory > 0:
            print('[' + self.name + ']', '<< blind: ', mandatory)
            self.cash = max(self.cash - mandatory, 0)
            self.bet += mandatory
            return self.bet - bet_level, mandatory

        self.bet, last_bet = self.getaction(bet_level)
        self.cash -= self.bet - last_bet

        self.showaction(bet_level)
        return self.bet - bet_level, self.bet - last_bet

    def getaction(self, bet_level):
        return bet_level, self.bet

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

class HumanPlayer(Player):

    def getaction(self, bet_level):

        last_bet = self.bet
        print('[' + self.name + ']', '<<', end=' ')
        print('bet level: ', bet_level, end=', ')
        print('your last bet: ', last_bet)

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
