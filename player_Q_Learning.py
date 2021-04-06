#player_Q_Learning.py

class playerQLearning():

    def __init__(self):
        self.hardHandTable = self.getHardHandTable()
        self.softHandTable = self.getSoftHandTable()
        self.pairsTable = self.getPairsTable()
        self.betAmount = 10
        self.GAMMA = 0.9
        self.ALPHA = 0.9

    def hitStayOrDoubleDown(self, playerCardList, dealerUpCard):
        """
        Return: H, S, or D
        """
        total = 0
        aceCount = 0
        for card in playerCardList:
            total += card.getValue()
            if card.isAce():
                aceCount += 1
        while aceCount > 0:
            if total > 21:
                total -= 10
                aceCount -= 1
            else:
                aceCount -= 1
        # check if soft hand and check proper table
        if aceCount > 0:
            maxQValue = - float('inf')
            index = 0
            for i in range(3):
                qValue = self.softHandTable[total - 12][dealerUpCard.getValue()
                                                        - 2][i]
                if qValue > maxQValue:
                    maxQValue = qValue
                    index = i
            if index == 0:
                return 'H'
            elif index == 1:
                return 'S'
            elif index == 2:
                return 'D'
            
        else:
            # Hard hand
            maxQValue = - float('inf')
            index = 0
            for i in range(3):
                qValue = self.hardHandTable[total - 4][dealerUpCard.getValue()
                                                       - 2][i]
                if qValue > maxQValue:
                    maxQValue = qValue
                    index = i
            if index == 0:
                return 'H'
            elif index == 1:
                return 'S'
            elif index == 2:
                return 'D'
            
        return 'S'

    def doSplit(self, card1, card2, dealerUpCard):
        """
        Return: Boolean, True for yes, False for no
        """
        if card1.getName() != card2.getName():
            return False
        maxQValue = - float('inf')
        index = 0
        for i in range(2):
            qValue = self.pairsTable[card1.getValue() - 2][dealerUpCard.getValue()
                                                           - 2][i]
            if qValue > maxQValue:
                maxQValue = qValue
                index = i
        if index == 0:
            return False
        elif index == 1:
            return True

    def betAmount(self):
        """
        Returns: int
        """
        return self.betAmount

    def helperMethod(self, playerCardList, dealerUpCard):
        """
        Recursive, handles multiple 'Hits', also handles the 'No Split' scenario
        Returns: Void
        """
        if len(playerCardList) == 2:
            #check for 'no split'
            if playerCardList[0].getName() == playerCardList[1].getName():
                #'No split'
                oldQValue = self.pairsTable[playerCardList[0].getValue() - 2][
                    dealerUpCard.getValue() - 2][0]
                if playerCardList[0].isAce() and playerCardList[1].isAce():
                    # soft hand, total = 12
                    maxQValue = - float('inf')
                    for j in range(3):
                        if self.softHandTable[12 - 12][dealerUpCard.getValue() - 2][j] > maxQValue:
                            maxQValue = self.softHandTable[12 - 12][
                                dealerUpCard.getValue() - 2][j]
                        
                    estimatedQValue = maxQValue
                        
                else:
                    #total hand, hardHandTable
                    totalHand = playerCardList[0].getValue() + playerCardList[1].getValue()
                    maxQValue = - float('inf')
                    for j in range(3):
                        if self.hardHandTable[totalHand - 4][dealerUpCard.getValue() - 2][j] > maxQValue:
                            maxQValue = self.hardHandTable[totalHand - 4][
                                dealerUpCard.getValue() - 2][j]
                    estimatedQValue = maxQValue
                    
                newQValue = oldQValue + self.ALPHA * (self.GAMMA * estimatedQValue - oldQValue)
                return
            else:
                #2 cards left: do nothing
                return
        else:
            #Hit
            totalHand = 0
            aceCount = 0
            for card in playerCardList:
                totalHand += card.getValue()
                if card.isAce():
                    aceCount += 1
            while aceCount > 0:
                if totalHand > 21:
                    totalHand -= 10
                    aceCount -= 1
                else:
                    aceCount -= 1
            dealtCard = playerCardList.pop()
            totalOrigHand = 0
            aceCount2 = 0
            for card in playerCardList:
                totalOrigHand += card.getValue()
                if card.isAce():
                    aceCount2 += 1
            while aceCount2 > 0:
                if totalOrigHand > 21:
                    totalOrigHand -= 10
                    aceCount2 -= 1
                else:
                    aceCount2 -= 1
            #get estimatedQValue from totalHand and aceCount
            if aceCount > 0:
                #soft hand
                maxQValue = - float('inf')
                for j in range(3):
                    if self.softHandTable[totalHand - 12][
                        dealerUpCard.getValue() - 2][j] > maxQValue:
                        maxQValue = self.softHandTable[totalHand - 12][
                            dealerUpCard.getValue() - 2][j]
                estimatedQValue = maxQValue
            else:
                #hard hand
                maxQValue = - float('inf')
                for j in range(3):
                    if self.hardHandTable[totalHand - 4][
                        dealerUpCard.getValue() - 2][j] > maxQValue:
                        maxQValue = self.hardHandTable[totalHand - 4][
                            dealerUpCard.getValue() - 2][j]
                estimatedQValue = maxQValue
            #get newQValue and apply to table
            if aceCount2 > 0:
                #soft hand
                oldQValue = self.softHandTable[totalOrigHand - 12][
                    dealerUpCard.getValue() - 2][0]
                newQValue = oldQValue + self.ALPHA * (self.GAMMA * estimatedQValue - oldQValue)
                self.softHandTable[totalOrigHand - 12][
                    dealerUpCard.getValue() - 2][0] = newQValue
                self.helperMethod(playerCardList, dealerUpCard)
            else:
                #hard hand
                oldQValue = self.hardHandTable[totalOrigHand - 4][
                    dealerUpCard.getValue() - 2][0]
                newQValue = oldQValue + self.ALPHA * (self.GAMMA * estimatedQValue - oldQValue)
                self.hardHandTable[totalOrigHand - 4][
                    dealerUpCard.getValue() - 2][0] = newQValue
                self.helperMethod(playerCardList, dealerUpCard)
        return

    def endOfHand(self, playerHandNestedList, dealerHandList):
        """
        Calculates all Q-values for hand and saves results in permanent tables.
        Return: Void
        """
        split = False
        if len(playerHandNestedList) > 1:
            split = True
        dealerTotal = 0
        aceCountDealer = 0
        for card in dealerHandList:
            dealerTotal += card.getValue()
            if card.isAce():
                aceCountDealer += 1
        while aceCountDealer > 0:
            if dealerTotal > 21:
                dealerTotal -= 10
                aceCountDealer -= 1
            else:
                aceCountDealer -= 1

        for hand in playerHandNestedList:
            betAmount = hand.pop()
            doubleDown = False
            if betAmount == 2 * self.betAmount:
                doubleDown = True
            totalHand = 0
            aceCount = 0
            for card in hand:
                totalHand += card.getValue()
                if card.isAce():
                    aceCount += 1
            tempAceCount = aceCount
            while tempAceCount > 0:
                if totalHand > 21:
                    totalHand -= 10
                    tempAceCount -= 1
                    aceCount -= 1
                else:
                    tempAceCount -= 1
            #get estimatedQValue from hand
            if totalHand >= 21:
                estimatedQValue = 0.0
            else:
                if aceCount > 0:
                    #soft hand table
                    maxQValue = - float('inf')
                    for j in range(3):
                        if self.softHandTable[totalHand - 12][
                                dealerUpCard.getValue() - 2][j] > maxQValue:
                            maxQValue = self.softHandTable[totalHand - 12][
                                dealerUpCard.getValue() - 2][j]
                    estimatedQValue = maxQValue
                else:
                    #hard hand table
                    maxQValue = - float('inf')
                    for j in range(3):
                        if self.hardHandTable[totalHand - 4][
                            dealerUpCard.getValue() - 2][j] > maxQValue:
                            maxQValue = self.hardHandTable[totalHand - 4][
                                dealerUpCard.getValue() - 2][j]
                    estimatedQValue = maxQValue

            if len(hand) > 2:
                # total original(smaller) hand
                dealtCard = hand.pop()
                totalOrigHand = 0
                aceCount2 = 0
                for card in hand:
                    totalOrigHand += card.getValue()
                    if card.isAce():
                        aceCount2 += 1
                tempAceCount2 = aceCount2
                while tempAceCount2 > 0:
                    if totalOrigHand > 21:
                        totalOrigHand -= 10
                        tempAceCount2 -= 1
                        aceCount2 -= 1
                    else:
                        tempAceCount2 -= 1
                # all possibilities of hand total and doubleDown
                if totalHand > 21:
                    if dealerTotal > 21:
                        #push, hit or doubleDown with reward 0
                        if doubleDown:
                            if aceCount2 > 0:
                                #soft hand
                                oldQValue = self.softHandTable[totalOrigHand
                                            - 12][dealerHandList[1].getValue()
                                            - 2][2]
                                newQValue = oldQValue + self.ALPHA * (0
                                            + self.GAMMA * estimatedQValue - oldQValue)
                                self.softHandTable[totalOrigHand
                                        - 12][dealerHandList[1].getValue()
                                        - 2][2] = newQValue
                                self.helperMethod(hand, dealerHandList[1])
                            else:
                                #hard hand
                                oldQValue = self.hardHandTable[totalOrigHand
                                            - 4][dealerHandList[1].getValue()
                                            - 2][2]
                                newQValue = oldQValue + self.ALPHA * (0
                                                    + self.GAMMA * estimatedQValue - oldQValue)
                                self.hardHandTable[totalOrigHand - 4][
                                    dealerHandList[1].getValue() - 2][2]
                                self.helperMethod(hand, dealerHandList[1])
                        else:
                            # Hit
                            if aceCount2 > 0:
                                #soft hand
                                oldQValue = self.softHandTable[totalOrigHand
                                            - 12][dealerHandList[1].getValue()
                                            - 2][0]
                                newQValue = oldQValue + self.ALPHA * (0
                                                    + self.GAMMA * estimatedQValue - oldQValue)
                                self.softHandTable[totalOrigHand - 12][
                                    dealerHandList[1].getValue() - 2][0] = newQValue
                                self.helperMethod(hand, dealerHandList[1])
                            else:
                                #hard hand
                                oldQValue = self.hardHandTable[totalOrigHand
                                                - 4][dealerHandList[1].getValue()
                                                - 2][0]
                                newQValue = oldQValue + self.ALPHA * (0
                                                    + self.GAMMA * estimatedQValue - oldQValue)
                                self.hardHandTable[totalOrigHand - 4][
                                    dealerHandList[1].getValue() - 2][0] = newQValue
                                self.helperMethod(hand, dealerHandList[1])
                    else:
                        #lose, hit or doubleDown with negative reward
                        if doubleDown:
                            if aceCount2 > 0:
                                #soft hand
                                oldQValue = self.softHandTable[totalOrigHand
                                                - 12][dealerHandList[1].getValue()
                                                - 2][2]
                                newQValue = oldQValue + self.ALPHA * (- betAmount
                                                + self.GAMMA * estimatedQValue - oldQValue)
                                self.softHandTable[totalOrigHand - 12][
                                    dealerHandList[1].getValue() - 2][2] = newQValue
                                self.helperMethod(hand, dealerHandList[1])
                            else:
                                #hard hand
                                oldQValue = self.hardHandTable[totalOrigHand
                                                - 4][dealerHandList[1].getValue()
                                                - 2][2]
                                newQValue = oldQValue + self.ALPHA * (- betAmount
                                                + self.GAMMA * estimatedQValue - oldQValue)
                                self.hardHandTable[totalOrigHand - 4][
                                    dealerHandList[1].getValue() - 2][2] = newQValue
                                self.helperMethod(hand, dealerHandList[1])
                        else:
                            #Hit
                            if aceCount2 > 0:
                                #soft hand
                                oldQValue = self.softHandTable[totalOrigHand
                                                - 12][dealerHandList[1].getValue()
                                                - 2][0]
                                newQValue = oldQValue + self.ALPHA * (- betAmount
                                                + self.GAMMA * estimatedQValue - oldQValue)
                                self.softHandTable[totalOrigHand - 12][
                                    dealerHandList[1].getValue() - 2][0] = newQValue
                                self.helperMethod(hand, dealerHandList[1])
                            else:
                                #hard hand
                                oldQValue = self.hardHandTable[totalOrigHand
                                                - 4][dealerHandList[1].getValue()
                                                - 2][0]
                                newQValue = oldQValue + self.ALPHA * (- betAmount
                                                + self.GAMMA * estimatedQValue - oldQValue)
                                self.hardHandTable[totalOrigHand - 4][
                                    dealerHandList[1].getValue() - 2][0] = newQValue
                                self.helperMethod(hand, dealerHandList[1])

                elif totalHand == 21:
                    if dealerTotal == 21:
                        #Push
                        if doubleDown:
                            #DoubleDown
                            if aceCount2 > 0:
                                #soft hand
                                oldQValue = self.softHandTable[totalOrigHand
                                                - 12][dealerHandList[1].getValue()
                                                - 2][2]
                                newQValue = oldQValue + self.ALPHA * (self.GAMMA * estimatedQValue
                                                                      - oldQValue)
                                self.softHandTable[totalOrigHand - 12][
                                    dealerHandList[1].getValue() - 2][2] = newQValue
                                self.helperMethod(hand, dealerHandList[1])
                            else:
                                #hard hand
                                oldQValue = self.hardHandTable[totalOrigHand
                                                - 4][dealerHandList[1].getValue()
                                                - 2][2]
                                newQValue = oldQValue + self.ALPHA * (self.GAMMA * estimatedQValue
                                                                      - oldQValue)
                                self.hardHandTable[totalOrigHand - 4][
                                    dealerHandList[1].getValue() - 2][2] = newQValue
                                self.helperMethod(hand, dealerHandList[1])
                        else:
                            #Hit
                            if aceCount2 > 0:
                                #soft hand
                                oldQValue = self.softHandTable[totalOrigHand
                                                - 12][dealerHandList[1].getValue()
                                                - 2][0]
                                newQValue = oldQValue + self.ALPHA * (self.GAMMA * estimatedQValue
                                                                      - oldQValue)
                                self.softHandTable[totalOrigHand - 12][
                                    dealerHandList[1].getValue() - 2][0] = newQValue
                                self.helperMethod(hand, dealerHandList[1])
                            else:
                                #hard hand
                                oldQValue = self.hardHandTable[totalOrigHand
                                                - 4][dealerHandList[1].getValue()
                                                - 2][0]
                                newQValue = oldQValue + self.ALPHA * (self.GAMMA * estimatedQValue
                                                                      - oldQValue)
                                self.hardHandTable[totalOrigHand - 4][
                                    dealerHandList[1].getValue() - 2][0] = newQValue
                                self.helperMethod(hand, dealerHandList[1])
                    else:
                        #Win
                        if doubleDown:
                            #DoubleDown
                            if aceCount2 > 0:
                                #soft hand
                                oldQValue = self.softHandTable[totalOrigHand
                                                - 12][dealerHandList[1].getValue()
                                                - 2][2]
                                newQValue = oldQValue + self.ALPHA * (betAmount
                                                        + self.GAMMA * estimatedQValue - oldQValue)
                                self.softHandTable[totalOrigHand - 12][
                                    dealerHandList[1].getValue() - 2][2] = newQValue
                                self.helperMethod(hand, dealerHandList[1])
                            else:
                                #hard hand
                                oldQValue = self.hardHandTable[totalOrigHand
                                                - 4][dealerHandList[1].getValue()
                                                - 2][2]
                                newQValue = oldQValue + self.ALPHA * (betAmount
                                                    + self.GAMMA * estimatedQValue - oldQValue)
                                self.hardHandTable[totalOrigHand - 4][
                                    dealerHandList[1].getValue() - 2][2] = newQValue
                                self.helperMethod(hand, dealerHandList[1])
                        else:
                            #Hit
                            if aceCount2 > 0:
                                #soft hand
                                oldQValue = self.softHandTable[totalOrigHand
                                                - 12][dealerHandList[1].getValue()
                                                -2][0]
                                newQValue = oldQValue + self.ALPHA * (betAmount
                                                        + self.GAMMA * estimatedQValue - oldQValue)
                                self.softHandTable[totalOrigHand - 12][
                                    dealerHandList[1].getValue() - 2][0] = newQValue
                                self.helperMethod(hand, dealerHandList[1])
                            else:
                                #hard hand
                                oldQValue = self.hardHandTable[totalOrigHand
                                                - 4][dealerHandList[1].getValue()
                                                - 2][0]
                                newQValue = oldQValue + self.ALPHA * (betAmount
                                                    + self.GAMMA * estimatedQValue - oldQValue)
                                self.hardHandTable[totalOrigHand - 4][
                                    dealerHandList[1].getValue() - 2][0] = newQValue
                                self.helperMethod(hand, dealerHandList[1])

                elif totalHand < 21:
                    #Stay
                    if dealerTotal > 21 or dealerTotal < totalHand:
                        #Win
                        if doubleDown:
                            #doubleDown, use totalOrigHand and aceCount2
                            if aceCount2 > 0:
                                #soft hand
                                oldQValue = self.softHandTable[totalOrigHand
                                                - 12][dealerHandList[1].getValue()
                                                - 2][2]
                                if aceCount > 0:
                                    #soft hand table
                                    maxIndex = 0
                                    maxQValue = - float('inf')
                                    for j in range(3):
                                        if self.softHandTable[totalHand - 12][
                                            dealerHandList[1].getValue() - 2][j] > maxQValue:
                                            maxQValue = self.softHandTable[totalHand - 12][
                                                dealerHandList[1].getValue() - 2][j]
                                            maxIndex = j
                                    estimateQValue = self.softHandTable[totalHand - 12][
                                        dealerHandList[1].getValue() - 2][maxIndex]
                                else:
                                    #hard hand table
                                    maxIndex = 0
                                    maxQValue = - float('inf')
                                    for j in range(3):
                                        if self.hardHandTable[totalHand - 4][
                                            dealerHandList[1].getValue() - 2][j] > maxQValue:
                                            maxQValue = self.hardHandTable[totalHand - 4][
                                                dealerHandList[1].getValue() - 2][j]
                                            maxIndex = j
                                    estimateQValue = self.hardHandTable[totalHand - 4][
                                        dealerHandList[1].getValue() - 2][maxIndex]
                                newQValue = oldQValue + self.ALPHA * (betAmount
                                                + self.GAMMA * estimateQValue - oldQValue)
                                self.softHandTable[totalOrigHand - 12][
                                    dealerHandList[1].getValue() - 2][2] = newQValue
                                self.helperMethod(hand, dealerHandList[1])
                            else:
                                #hard hand
                                oldQValue = self.hardHandTable[totalOrigHand - 4][
                                    dealerHandList[1].getValue() - 2][2]
                                if aceCount > 0:
                                    #soft hand table
                                    maxIndex = 0
                                    maxQValue = - float('inf')
                                    for j in range(3):
                                        if self.softHandTable[totalHand - 12][
                                            dealerHandList[1].getValue() - 2][j] > maxQValue:
                                            maxQValue = self.softHandTable[totalHand - 12][
                                                dealerHandList[1].getValue() - 2][j]
                                            maxIndex = j
                                    estimatedQValue = self.softHandTable[totalHand - 12][
                                        dealerHandList[1].getValue() - 2][maxIndex]
                                else:
                                    #hard hand table
                                    maxIndex = 0
                                    maxQValue = - float('inf')
                                    for j in range(3):
                                        if self.hardHandTable[totalHand - 4][
                                            dealerHandList[1].getValue() - 2][j] > maxQValue:
                                            maxQValue = self.hardHandTable[totalHand - 4][
                                                dealerHandList[1].getValue() - 2][j]
                                            maxIndex = j
                                    estimatedQValue = self.hardHandTable[totalHand - 4][
                                        dealerHandList[1].getValue() - 2][maxIndex]
                                newQValue = oldQValue + self.ALPHA * (betAmount
                                                + self.GAMMA * estimatedQValue - oldQValue)
                                self.hardHandTable[totalOrigHand - 4][
                                    dealerHandList[1].getValue() - 2][2] = newQValue
                                self.helperMethod(hand, dealerHandList[1])
                        else:
                            #Stay, use totalHand and aceCount
                            if aceCount > 0:
                                #soft hand
                                oldQValue = self.softHandTable[totalHand - 12][
                                    dealerHandList[1].getValue() - 2][1]
                                newQValue = oldQValue + self.ALPHA * (betAmount
                                                        + self.GAMMA * estimatedQValue - oldQValue)
                                self.softHandTable[totalHand - 12][
                                    dealerHandList[1].getValue() - 2][1] = newQValue
                                self.helperMethod(hand, dealerHandList[1])
                            else:
                                #hard hand
                                oldQValue = self.hardHandTable[totalHand - 4][
                                    dealerHandList[1].getValue() - 2][1]
                                newQValue = oldQValue + self.ALPHA * (betAmount
                                                        + self.GAMMA * estimatedQValue - oldQValue)
                                self.hardHandTable[totalHand - 4][
                                    dealerHandList[1].getValue() - 2][1] = newQValue
                                self.helperMethod(hand, dealerHandList[1])
                    
                    elif dealerTotal > totalHand:
                        #Lose
                        if doubleDown:
                            #DoubleDown with negative reward
                            if aceCount2 > 0:
                                #soft hand
                                oldQValue = self.softHandTable[totalOrigHand - 12][
                                    dealerHandList[1].getValue() - 2][2]
                                newQValue = oldQValue + self.ALPHA * (- betAmount
                                                    + self.GAMMA * estimatedQValue - oldQValue)
                                self.softHandTable[totalOrigHand - 12][
                                    dealerHandList[1].getValue() - 2][2] = newQValue
                                self.helperMethod(hand, dealerHandList[1])
                            else:
                                #hard hand
                                oldQValue = self.hardHandTable[totalOrigHand - 4][
                                    dealerHandList[1].getValue() - 2][2]
                                newQValue = oldQValue + self.ALPHA * (- betAmount
                                                        + self.GAMMA * estimatedQValue - oldQValue)
                                self.hardHandTable[totalOrigHand - 4][
                                    dealerHandList[1].getValue() - 2][2] = newQValue
                                self.helperMethod(hand, dealerHandList[1])
                        else:
                            #Stay with negative reward
                            if aceCount > 0:
                                #soft hand
                                oldQValue = self.softHandTable[totalHand - 12][
                                    dealerHandList[1].getValue() - 2][1]
                                newQValue = oldQValue + self.ALPHA * (- betAmount
                                                    + self.GAMMA * estimatedQValue - oldQValue)
                                self.softHandTable[totalHand - 12][
                                    dealerHandList[1].getValue() - 2][1] = newQValue
                                self.helperMethod(hand, dealerHandList[1])
                            else:
                                #hard hand
                                oldQValue = self.hardHandTable[totalHand - 4][
                                    dealerHandList[1].getValue() - 2][1]
                                newQValue = oldQValue + self.ALPHA * (- betAmount
                                                + self.GAMMA * estimatedQValue - oldQValue)
                                self.hardHandTable[totalHand - 4][
                                    dealerHandList[1].getValue() - 2][1] = newQValue
                                self.helperMethod(hand, dealerHandList[1])
                    
            else:
                # Hand is 2 cards, STAY
                if dealerTotal > 21 or dealerTotal < totalHand:
                    #Win
                    if aceCount > 0:
                        #soft hand
                        oldQValue = self.softHandTable[totalHand - 12][
                            dealerHandList[1].getValue() - 2][1]
                        newQValue = oldQValue + self.ALPHA * (betAmount
                                                    + self.GAMMA * estimatedQValue - oldQValue)
                        self.softHandTable[totalHand - 12][
                            dealerHandList[1].getValue() - 2][1] = newQValue
                    else:
                        #hard hand
                        oldQValue = self.hardHandTable[totalHand - 4][
                            dealerHandList[1].getValue() - 2][1]
                        newQValue = oldQValue + self.ALPHA * (betAmount
                                            + self.GAMMA * estimatedQValue - oldQValue)
                        self.hardHandTable[totalHand - 4][
                            dealerHandList[1].getValue() - 2][1] = newQValue
                elif dealerTotal == totalHand:
                    #Push
                    if aceCount > 0:
                        #soft hand
                        oldQValue = self.softHandTable[totalHand - 12][
                            dealerHandList[1].getValue() - 2][1]
                        newQValue = oldQValue + self.ALPHA * (self.GAMMA * estimatedQValue
                                                              - oldQValue)
                        self.softHandTable[totalHand - 12][
                            dealerHandList[1].getValue() - 2][1] = newQValue
                    else:
                        #hard hand
                        oldQValue = self.hardHandTable[totalHand - 4][
                            dealerHandList[1].getValue() - 2][1]
                        newQValue = oldQValue + self.ALPHA * (self.GAMMA * estimatedQValue
                                                              - oldQValue)
                        self.hardHandTable[totalHand - 4][
                            dealerHandList[1].getValue() - 2][1] = newQValue
                elif dealerTotal > totalHand:
                    #Lose
                    if aceCount > 0:
                        #soft hand
                        oldQValue = self.softHandTable[totalHand - 12][
                            dealerHandList[1].getValue() - 2][1]
                        newQValue = oldQValue + self.ALPHA * (- betAmount
                                                + self.GAMMA * estimatedQValue - oldQValue)
                        self.softHandTable[totalHand - 12][
                            dealerHandList[1].getValue() - 2][1] = newQValue
                    else:
                        #hard hand
                        oldQValue = self.hardHandTable[totalHand - 4][
                            dealerHandList[1].getValue() - 2][1]
                        newQValue = oldQValue + self.ALPHA * (- betAmount
                                            + self.GAMMA * estimatedQValue - oldQValue)
                        self.hardHandTable[totalHand - 4][
                            dealerHandList[1].getValue() - 2][1] = newQValue

        # deal with split
        if split == True:
            hand1 = playerHandNestedList[0]
            hand2 = playerHandNestedList[1]
            totalHand1 = 0
            aceCount1 = 0
            for card in hand1:
                totalHand1 += card.getValue()
                if card.isAce():
                    aceCount1 += 1
            tempAceCount1 = aceCount1
            while tempAceCount1 > 0:
                if totalHand1 > 21:
                    totalHand1 -= 10
                    tempAceCount1 -= 1
                    aceCount1 -= 1
                else:
                    tempAceCount1 -= 1
            totalHand2 = 0
            aceCount2 = 0
            for card in hand2:
                totalHand2 += card.getValue()
                if card.isAce():
                    aceCount2 += 1
            tempAceCount2 = aceCount2
            while tempAceCount2 > 0:
                if totalHand2 > 21:
                    totalHand2 -= 10
                    tempAceCount2 -= 1
                    aceCount2 -= 1
                else:
                    tempAceCount2 -= 1
            
            # find estimatedQValue1 for hand1
            if aceCount1 > 0:
                #soft hand
                maxQValue = - float('inf')
                index1 = 0
                for j in range(3):
                    if self.softHandTable[totalHand1 - 12][
                        dealerHandList[1].getValue() - 2][j] > maxQValue:
                        maxQValue = self.softHandTable[totalHand1 - 12][
                            dealerHandList[1].getValue() - 2][j]
                        index1 = j
                estimatedQValue1 = self.softHandTable[totalHand1 -  12][
                    dealerHandList[1].getValue() - 2][index1]
            else:
                #hard hand
                maxQValue = - float('inf')
                index1 = 0
                for j in range(3):
                    if self.hardHandTable[totalHand1 - 4][
                        dealerHandList[1].getValue() - 2][j] > maxQValue:
                        maxQValue = self.hardHandTable[totalHand1 - 4][
                            dealerHandList[1].getValue() - 2][j]
                        index1 = j
                estimatedQValue1 = self.hardHandTable[totalHand1 -  4][
                    dealerHandList[1].getValue() - 2][index1]
            # find estimatedQValue2 for hand2
            if aceCount2 > 0:
                #soft hand
                maxQValue = - float('inf')
                index2 = 0
                for j in range(3):
                    if self.softHandTable[totalHand2 - 12][
                        dealerHandList[1].getValue() - 2][j] > maxQValue:
                        maxQValue = self.softHandTable[totalHand2 - 12][
                            dealerHandList[1].getValue() - 2][j]
                        index2 = j
                estimatedQValue2 = self.softHandTable[totalHand2 -  12][
                    dealerHandList[1].getValue() - 2][index2]
            else:
                #hard hand
                maxQValue = - float('inf')
                index2 = 0
                for j in range(3):
                    if self.hardHandTable[totalHand2 - 4][
                        dealerHandList[1].getValue() - 2][j] > maxQValue:
                        maxQValue = self.hardHandTable[totalHand2 - 4][
                            dealerHandList[1].getValue() - 2][j]
                        index2 = j
                estimatedQValue2 = self.hardHandTable[totalHand2 -  4][
                    dealerHandList[1].getValue() - 2][index2]
            # update newQValue for pairs table
            avgEstimatedQValue = (estimatedQValue1 + estimatedQValue2) / 2
            oldQValue = self.pairsTable[hand1[0].getValue() - 2][
                dealerHandList[1].getValue() - 2][1]
            newQValue = oldQValue + self.ALPHA * (self.GAMMA * avgEstimatedQValue
                                                  - oldQValue)
            self.pairsTable[hand1[0].getValue() - 2][
                dealerHandList[1].getValue() - 2][1] = newQValue

        self.saveHardHandTable()
        self.saveSoftHandTable()
        self.savePairsTable()
        return

    def makeHardHandTable(self):
        """
        Rows: possible totals from 5 to 20
        Columns: Dealer UpCard 2 to 10 to A
        """
        hardHandTable = []
        for i in range(17):
            hardHandTable.append([])
            for j in range(10):
                hardHandTable[i].append([])
                for k in range(3):
                    hardHandTable[i][j].append(float(0))
        #print(hardHandTable)
        return hardHandTable

    def makeSoftHandTable(self):
        """
        Rows: Ace plus number: 2 to 9
        Columns: Dealer UpCard 2 to 10 to A
        """
        softHandTable = []
        for i in range(9):
            softHandTable.append([])
            for j in range(10):
                softHandTable[i].append([])
                for k in range(3):
                    softHandTable[i][j].append(float(0))
        #print(softHandTable)
        return softHandTable

    def makePairsTable(self):
        """
        Rows: pairs: 2 to 10 to A
        Columns: Dealer UpCard 2 to 10 to A
        """
        pairsTable = []
        for i in range(10):
            pairsTable.append([])
            for j in range(10):
                pairsTable[i].append([])
                for k in range(2):
                    pairsTable[i][j].append(float(0))
        #print(pairsTable)
        return pairsTable

    def getHardHandTable(self):
        """
        If previous table cannot be found, then create a new one.
        """
        hardHandTable = []
        newString = ''
        index = 0
        try:
            with open('hardhandtable.txt', 'r') as filehandle:
                filecontents = filehandle.readlines()
                for line in filecontents:
                    current_place = line[:-1]
                    newString += current_place + ','
            
            newList = newString.split(',')
            
            for i in range(17):
                hardHandTable.append([])
                for j in range(10):
                    hardHandTable[i].append([])
                    for k in range(3):
                        hardHandTable[i][j].append(float(newList[index]))
                        index += 1
                    
        except:
            print("Cannot find Hard Hand Table.")
            hardHandTable = self.makeHardHandTable()
        
        #print(hardHandTable)
        return hardHandTable

    def getSoftHandTable(self):
        """
        If previous table cannot be found, then create a new one.
        """
        softHandTable = []
        newString = ''
        index = 0
        try:
            with open('softhandtable.txt', 'r') as filehandle:
                filecontents = filehandle.readlines()
                for line in filecontents:
                    current_place = line[:-1]
                    newString += current_place + ','

            newList = newString.split(',')

            for i in range(9):
                softHandTable.append([])
                for j in range(10):
                    softHandTable[i].append([])
                    for k in range(3):
                        softHandTable[i][j].append(float(newList[index]))
                        index += 1
        except:
            print("Cannot find Soft Hand Table.")
            softHandTable = self.makeSoftHandTable()
        
        #print(softHandTable)
        return softHandTable

    def getPairsTable(self):
        """
        If previous table cannot be found, then create a new one.
        """
        pairsTable = []
        newString = ''
        index = 0
        try:
            with open('pairstable.txt', 'r') as filehandle:
                filecontents = filehandle.readlines()
                for line in filecontents:
                    current_place = line[:-1]
                    newString += current_place + ','

            newList = newString.split(',')

            for i in range(10):
                pairsTable.append([])
                for j in range(10):
                    pairsTable[i].append([])
                    for k in range(3):
                        pairsTable[i][j].append(float(newList[index]))
                        index += 1
        except:
            print("Cannot find Pairs Table.")
            pairsTable = self.makePairsTable()
        
        #print(pairsTable)
        return pairsTable

    def saveHardHandTable(self):
        """
        Saves hardHandTable to .txt file
        """
        newList = []
        for i in range(17):
            for j in range(10):
                for k in range(3):
                    newList.append(self.hardHandTable[i][j][k])
        try:
            with open('hardhandtable.txt', 'w') as filehandle:
                filehandle.writelines("%s\n" % place for place in newList)
                filehandle.close()
        except:
            print("Could not save data to Hard Hand Table.")
        return

    def saveSoftHandTable(self):
        """
        Saves softHandTable to .txt file
        """
        newList = []
        for i in range(9):
            for j in range(10):
                for k in range(3):
                    newList.append(self.softHandTable[i][j][k])
        try:
            with open('softhandtable.txt', 'w') as filehandle:
                filehandle.writelines("%s\n" % place for place in newList)
                filehandle.close()
        except:
            print("Could not save data to Soft Hand Table.")
        return

    def savePairsTable(self):
        """
        Saves pairsTable to .txt file
        """
        newList = []
        for i in range(10):
            for j in range(10):
                for k in range(2):
                    newList.append(self.pairsTable[i][j][k])
        try:
            with open('pairstable.txt', 'w') as filehandle:
                filehandle.writelines("%s\n" % place for place in newList)
                filehandle.close()
        except:
            print("Could not save data to Pairs Table.")
        return

##def main():
##    player = playerQLearning()
##
##
##
##main()
