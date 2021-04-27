class ExpectimaxAgent:
    def __init__(self):
        self.betAmount = 10
        self.split_count = 0

    def hitStayOrDoubleDown(self, playerCardList, dealerUpCard):
        agents_total_hand = self.agent_total_hand(playerCardList)
        dealers_up_card = dealerUpCard.getValue()

        if playerCardList[0].isAce() and playerCardList[1].isAce():
            return 'S'

        # Always assume face card for flip card.
        dealers_up_card += 10

        if dealers_up_card < 17:
            dealers_up_card += 5

        # while dealers_up_card < 17:
        #     dealers_up_card += 6

        var = self.expecti_max(True, agents_total_hand, dealers_up_card, False, self.betAmount)
        #print("Expectimax chooses " + str(var[1]))
        return var[1]

        # print("EXPECTI RETURN " + str(var[1]))
        # print("EXPECTI score " + str(var[0]))

    def expecti_max(self, is_first, current_hand_val, dealers_up_card_val, leaf_node, weight):

        if leaf_node or current_hand_val > 21:
            if current_hand_val > 21:
                print("Player bust")
                return [-weight]
            elif dealers_up_card_val > 21:
                print("Dealer bust")
                return [weight]
            elif dealers_up_card_val > current_hand_val:
                print("Dealer win")
                return [-weight]
            elif dealers_up_card_val < current_hand_val:
                print("Player win")
                return [weight]
            else:
                print("else")
                return [weight]

        if is_first:
            return self.max_value(current_hand_val, dealers_up_card_val, weight)
        else:
            return self.exp_val(current_hand_val, dealers_up_card_val, weight)

    def max_value(self, current_hand_val, dealers_up_card_val, weights):
        max_value = [-1000000]

        for action in ['H', 'S', 'D']:
            child_state = self.generateSuccessors(current_hand_val, action, weights)
            value = self.expecti_max(False, child_state[0], dealers_up_card_val, child_state[1], child_state[2])
            # print("Value" + str(value))
            # print(action + " = " + str(value))

            if value[0] >= max_value[0]:
                max_value = [value[0], action]

        # print("Maximizer " + str(max_value))
        return max_value

    def exp_val(self, current_hand_val, dealers_up_card_val, weight):

        weights = [0]
        print("Current hand val" + str(current_hand_val))
        for action in ['H', 'S']:
            child_state = self.generateSuccessors(current_hand_val, action, weight)
            value = self.expecti_max(False, child_state[0], dealers_up_card_val, child_state[1], child_state[2])
            # print("NODE " + str(float(value[0] * (1 / 2))))
            weights[0] += float(value[0] * (1 / 2))

        # print("Weights" + str(weights))
        return weights

    def generateSuccessors(self, current_hand_val, action, weights):
        if action == 'S':
            return [current_hand_val, True, weights]
        elif action == 'H':
            child_hand = current_hand_val + 10
            return [child_hand, False, weights]
        else:
            child_hand = current_hand_val + 10
            return [child_hand, True, weights * 2]

    def agent_total_hand(self, player_card_list):
        total = 0
        for card in player_card_list:
            total += card.getValue()

        return total

    def betAmount(self):
        return self.betAmount

    def doSplit(self, card1, card2, dealerUpCard):
        return False

    def endOfHand(self, playerHandNestedList, dealerHandList):
        print('End of Hand')
        return
