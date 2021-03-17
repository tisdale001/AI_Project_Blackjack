#player_1_blackjack.py

class player1BlackJack():

    def hitStayOrDoubleDown(self, playerCardList, dealerUpCard):
        x = input('(H)it, (S)tay, or (D)oubleDown?')
        if x.upper() == 'H':
            return 'H'
        elif x.upper() == 'S':
            return 'S'
        elif x.upper() == 'D':
            return 'D'
        elif x.upper() == 'Q':
            return 'Q'
        else:
            return self.hitStayOrDoubleDown(playerCardList, dealerUpCard)

    def doSplit(self, card1, card2, dealerUpCard):
        """
        Return True for split, False for no split.
        """
        x = input('Split cards? (Y)es or (N)o')
        if x.upper() == 'Y':
            return True
        elif x.upper() == 'N':
            return False
        elif x.upper() == 'Q':
            exit()
        else:
            return self.doSplit(card1, card2, dealerUpCard)

    def betAmount(self):
        """
        Returns integer.
        """
        x = input('Enter bet amount.')
        try:
            y = int(x)
        except:
            y = self.betAmount()
        return y

    def endOfHand(self, playerHandNestedList, dealerHandList):
        input('Press ENTER')
        return
