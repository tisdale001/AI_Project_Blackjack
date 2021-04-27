"""
Class that implements and optimal playing agent. This agent
is based of black jack basic strategy.
"""


class OptimalAgent:

    def __init__(self):
        self.betAmount = 10
        self.split_count = 0

    def hitStayOrDoubleDown(self, playerCardList, dealerUpCard):
        agents_total_hand = self.agent_total_hand(playerCardList)
        dealers_up_card = dealerUpCard.getValue()

        # if players hand is hand total
        if not self.contains_ace(playerCardList):

            if agents_total_hand <= 8:
                return 'H'
            if agents_total_hand == 9:
                if dealers_up_card in [1, 2, 7, 8, 9, 10, 11]:
                    return 'H'
                return 'D'
            if agents_total_hand == 10 or 11:
                if dealers_up_card in [1, 10, 11]:
                    return 'H'
                return 'D'
            if agents_total_hand == 12:
                if dealers_up_card in [4, 5, 6]:
                    return 'S'
                return 'H'
            if agents_total_hand in [13, 14, 15, 16]:
                if dealers_up_card in [1, 2, 3, 4, 5, 6]:
                    return 'S'
                return 'H'
            if agents_total_hand >= 17:
                return 'S'
        else:
            # player's hand is soft total
            if agents_total_hand in [13, 14]:
                if dealers_up_card in [5, 6]:
                    return 'D'
                return 'H'
            if agents_total_hand in [15, 16]:
                if dealers_up_card in [4, 5, 6]:
                    return 'D'
                return 'H'
            if agents_total_hand == 17:
                if dealers_up_card in [3, 4, 5, 6]:
                    return 'D'
                return 'H'
            if agents_total_hand == 18:
                if dealers_up_card in [3, 4, 5, 6]:
                    return 'D'
                if dealers_up_card in [2, 7, 8]:
                    return 'S'
                return 'H'
            if agents_total_hand >= 19:
                return 'S'

    def doSplit(self, card1, card2, dealerUpCard):

        total_hand = card1.getValue() + card2.getValue()
        dealers_up_card = dealerUpCard.getValue()

        if total_hand in [4, 6]:
            if dealers_up_card in [8, 9, 10, 11]:
                return False
            self.split_count += 1
            return True
        if total_hand == 8:
            if dealers_up_card in [5, 6]:
                self.split_count += 1
                return True
            return False
        if total_hand == 10:
            return False
        if total_hand == 12:
            if dealers_up_card in [7, 8, 9, 10, 11]:
                return False
            self.split_count += 1
            return True
        if total_hand == 14:
            if dealers_up_card in [8, 9, 10, 11]:
                return False
            self.split_count += 1
            return True
        if total_hand == 16:
            if dealers_up_card in [10, 11]:
                return False
            self.split_count += 1
            return True
        if total_hand == 18:
            if dealers_up_card in [7, 10, 11]:
                self.split_count += 1
                return True
            return False
        if total_hand == 20:
            return False
        if total_hand == 2 or 22:
            if dealers_up_card == 11:
                return False
            self.split_count += 1
            return True

    def get_split_count(self):
        return self.split_count

    def contains_ace(self, player_card_list):

        for card in player_card_list:
            if card.isAce():
                return True

        return False

    def agent_total_hand(self, player_card_list):
        total = 0
        for card in player_card_list:
            total += card.getValue()

        return total

    def betAmount(self):
        return self.betAmount

    def endOfHand(self, playerHandNestedList, dealerHandList):
        print('End of Hand')
        return
