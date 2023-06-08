class Player():

    def __init__(self, name, cash, num):
        self.name = name
        self.cash = cash
        self.num = num
        self.hand = []
        self.state = 'on'       # on, fold, all

    def deal(self, cards):
        self.hand = cards

    def bet(self, amount):
        self.cash -= amount
        return amount