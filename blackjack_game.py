#blackjack_game.py
from player_1_blackjack import player1BlackJack
import random

class card():
    
    def __init__(self, nameString, value):
        self.name = nameString
        self.value = value
        
    def getName(self):
        return self.name

    def getValue(self):
        return self.value

    def isAce(self):
        if self.value == 11:
            return True

class deckOfCards():
    """
    Creates shuffled decks plus one extra shuffled deck for black jack.
    """
    def __init__(self, numberOfDecks):
        self.numberOfDecks = numberOfDecks
        self.cardList = self.shuffle()
        
    def shuffle(self):
        finalDeck = []
        #add extra deck for overage
        unshuffledExtra = []
        for i in range(4):
            unshuffledExtra.append(card('2', 2))
            unshuffledExtra.append(card('3', 3))
            unshuffledExtra.append(card('4', 4))
            unshuffledExtra.append(card('5', 5))
            unshuffledExtra.append(card('6', 6))
            unshuffledExtra.append(card('7', 7))
            unshuffledExtra.append(card('8', 8))
            unshuffledExtra.append(card('9', 9))
            unshuffledExtra.append(card('10', 10))
            unshuffledExtra.append(card('J', 10))
            unshuffledExtra.append(card('Q', 10))
            unshuffledExtra.append(card('K', 10))
            unshuffledExtra.append(card('A', 11))
        while unshuffledExtra:
            index = random.randint(0, len(unshuffledExtra) - 1)
            finalDeck.append(unshuffledExtra[index])
            unshuffledExtra.pop(index)
            
        unshuffledDeck = []
        #create unshuffled deck
        for i in range(self.numberOfDecks):
            for j in range(4):
                unshuffledDeck.append(card('2', 2))
                unshuffledDeck.append(card('3', 3))
                unshuffledDeck.append(card('4', 4))
                unshuffledDeck.append(card('5', 5))
                unshuffledDeck.append(card('6', 6))
                unshuffledDeck.append(card('7', 7))
                unshuffledDeck.append(card('8', 8))
                unshuffledDeck.append(card('9', 9))
                unshuffledDeck.append(card('10', 10))
                unshuffledDeck.append(card('J', 10))
                unshuffledDeck.append(card('Q', 10))
                unshuffledDeck.append(card('K', 10))
                unshuffledDeck.append(card('A', 11))
        #shuffle deck
        while unshuffledDeck:
            index = random.randint(0, len(unshuffledDeck) - 1)
            finalDeck.append(unshuffledDeck[index])
            unshuffledDeck.pop(index)
##        # stack deck for testing
##        for i in range(6):
##            finalDeck.append(card('2', 2))
##        finalDeck.append(card('A', 11))
##        finalDeck.append(card('J', 10))
##        finalDeck.append(card('2', 2))
##        finalDeck.append(card('2', 2))
            
        return finalDeck

    def dealCard(self):
        topCard = None
        try:
            topCard = self.cardList.pop()
        except:
            print("Error: Card deck is empty.")
        return topCard

    def numCardsLeft(self):
        return len(self.cardList)

class blackJack():
    
    def __init__(self, numHands, startMoney, player = player1BlackJack()):
        self.deck = deckOfCards(1)
        self.dealerUpCard = None
        self.dealerHoleCard = None
        self.dealerDealtCards = []
        self.playerHandList = []
        self.numHands = numHands
        self.player = player
        self.money = startMoney
        self.betAmount = 0
        self.playBlackJack()
        
    def playHand(self, card1, card2, dealerUpCard):
        """
        Returns card list including bet amount at end of list.
        """
        playerCardList = [card1, card2]
        total = self.totalPlayerHand(playerCardList)
        betAmount = self.betAmount
        #self.drawHand(playerCardList, dealerUpCard)
        while total < 21:
            x = self.player.hitStayOrDoubleDown(playerCardList, dealerUpCard)
            if x.upper() == 'H':
                playerCardList.append(self.deck.dealCard())
                total = self.totalPlayerHand(playerCardList)
                self.drawHand(playerCardList, dealerUpCard)
            elif x.upper() == 'S':
                break
            elif x.upper() == 'D':
                betAmount = 2 * self.betAmount
                playerCardList.append(self.deck.dealCard())
                self.drawHand(playerCardList, dealerUpCard)
                break
            elif x.upper() == 'Q':
                # Is this how to quit game?
                exit()

        playerCardList.append(betAmount)
        return playerCardList

    def split(self, card1, card2, dealerUpCard):
        """
        Returns card lists including bet amount at end of each list.
        """
        playerHandList = []
        hand1 = [card1, self.deck.dealCard()]
        hand2 = [card2, self.deck.dealCard()]
        # play hand1
        self.drawHand(hand1, self.dealerUpCard)
        if hand1[0].getName() == hand1[1].getName():
            if self.player.doSplit(hand1[0], hand1[1], self.dealerUpCard):
                # recursive function call
                handList = self.split(hand1[0], hand1[1], self.dealerUpCard)
                for newCardList in handList:
                    playerHandList.append(newCardList)
            else:
                cardList = self.playHand(hand1[0], hand1[1], self.dealerUpCard)
                playerHandList.append(cardList)
        else:
            cardList = self.playHand(hand1[0], hand1[1], self.dealerUpCard)
            playerHandList.append(cardList)
        
        # play hand2
        self.drawHand(hand2, self.dealerUpCard)
        if hand2[0].getName() == hand2[1].getName():
            if self.player.doSplit(hand2[0], hand2[1], self.dealerUpCard):
                # recursive function call
                handList = self.split(hand2[0], hand2[1], self.dealerUpCard)
                for newCardList in handList:
                    playerHandList.append(newCardList)
            else:
                cardList = self.playHand(hand2[0], hand2[1], self.dealerUpCard)
                playerHandList.append(cardList)
        else:
            cardList = self.playHand(hand2[0], hand2[1], self.dealerUpCard)
            playerHandList.append(cardList)
            
        return playerHandList

    def drawHand(self, playerCardList, dealerUpCard):
        """
        Draws game state with Dealer's hole card face-down.
        """
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        moneyStr = '                    Money: ' + str(self.money)
        print(moneyStr)
        print('Dealer')
        dealerStr = '% ' + dealerUpCard.getName()
        print(dealerStr)
        print()
        print('Player')
        playerStr = ''
        for card in playerCardList:
            playerStr += card.getName() + ' '
        print(playerStr)
        totalStr = str(self.totalPlayerHand(playerCardList))
        print(totalStr)
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        return

    def showDealerHand(self, playerHandNestedList):
        """
        Draws game state including dealer's hand face-up.
        """
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        moneyStr = '                    Money: ' + str(self.money)
        print(moneyStr)
        print('Dealer')
        dealerStr = ''
        dealerHandList = [self.dealerHoleCard, self.dealerUpCard]
        if self.dealerDealtCards:
            for card in self.dealerDealtCards:
                dealerHandList.append(card)
        for card in dealerHandList:
            dealerStr += card.getName() + ' '
        print(dealerStr)
        dealerTotal = self.totalDealerHand()
        print(str(dealerTotal))
        print()
        print('Player')
        playerStr = ''
        for playerHand in playerHandNestedList:
            for i in range(len(playerHand)):
                if i == len(playerHand) - 1:
                    betAmount = playerHand[i]
                else:
                    playerStr += str(playerHand[i].getName()) + ' '
            playerStr += '      '
        print(playerStr)
        playerTotalStr = ''
        #cardList = []
        for playerHand in playerHandNestedList:
            cardList = []
            for i in range(len(playerHand)):
                if i == len(playerHand) - 1:
                    nothing = True
                else:
                    cardList.append(playerHand[i])
            playerTotalStr += str(self.totalPlayerHand(cardList))
            for j in range(len(cardList) - 1):
                playerTotalStr += '  '
            playerTotalStr += '       '
        print(playerTotalStr)
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        return

    def playDealer(self, playerHandNestedList):
        """
        Plays dealer's turn.
        Returns: dealerHandList
        """
        self.showDealerHand(playerHandNestedList)
        dealerHand = [self.dealerHoleCard, self.dealerUpCard]
        while self.totalDealerHand() <= 17:
            aceCount = 0
            for card in dealerHand:
                if card.isAce():
                    aceCount += 1
            if self.totalDealerHand() == 17 and aceCount == 1:
                # Hit on soft 17
                newCard = self.deck.dealCard()
                self.dealerDealtCards.append(newCard)
                dealerHand.append(newCard)
                self.showDealerHand(playerHandNestedList)
            elif self.totalDealerHand() == 17:
                # stay on hard 17
                break
            else:
                # Hit on total < 17
                newCard = self.deck.dealCard()
                self.dealerDealtCards.append(newCard)
                dealerHand.append(newCard)
                self.showDealerHand(playerHandNestedList)

        if self.totalDealerHand() > 21:
            print('Dealer bust!')
        return dealerHand

    def totalDealerHand(self):
        """
        Returns: int, a total of dealer's hand
        """
        dealerHand = [self.dealerHoleCard, self.dealerUpCard]
        if self.dealerDealtCards:
            for card in self.dealerDealtCards:
                dealerHand.append(card)
        total = 0
        aceCount = 0
        for card in dealerHand:
            total += card.getValue()
            if card.isAce():
                aceCount += 1
        while aceCount > 0:
            if total > 21:
                total -= 10
                aceCount -= 1
            else:
                aceCount -= 1
                
        return total

    def totalPlayerHand(self, playerCardList):
        """
        Input: List of cards (no betAmount)
        Returns: int, a total of player's hand
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
                
        return total

    def playBlackJack(self):
        for i in range(self.numHands):
            if self.deck.numCardsLeft() <= 52:
                print('Shuffling....')
                self.deck = deckOfCards(1)
            #print('Place bet....')
            self.betAmount = self.player.betAmount
            while self.betAmount > self.money:
                print('You cannot bet more money than you have.')
                self.betAmount = player.betAmount()
            self.dealerHoleCard = self.deck.dealCard()
            self.dealerUpCard = self.deck.dealCard()
            card1 = self.deck.dealCard()
            card2 = self.deck.dealCard()
            playerCardList = [card1, card2]
            self.drawHand(playerCardList, self.dealerUpCard)
            # check for dealer blackjack
            if self.dealerUpCard.getValue() + self.dealerHoleCard.getValue() == 21:
                if card1.getValue() + card2.getValue() == 21:
                    self.showDealerHand([[card1, card2, self.betAmount]])
                    print('Push.')
                    self.dealerDealtCards = []
                    self.playerHandList = [] 
                else:
                    self.money -= self.betAmount
                    self.showDealerHand([[card1, card2, self.betAmount]])
                    print('Dealer has Blackjack.')
                    self.dealerDealtCards = []
                    self.playerHandList = [] 
            # check player blackjack
            elif card1.getValue() + card2.getValue() == 21:
                self.money += self.betAmount
                self.showDealerHand([[card1, card2, self.betAmount]])
                print('Player has Blackjack!')
                self.dealerDealtCards = []
                self.playerHandList = []
            else:
                # play hand
                if card1.getName() == card2.getName():
                    #print('Split cards?')
                    if self.player.doSplit(card1, card2, self.dealerUpCard):
                        self.playerHandList = self.split(card1, card2, self.dealerUpCard)
                    else:
                        self.playerHandList = [ self.playHand(card1, card2, self.dealerUpCard) ]
                else:
                    self.playerHandList = [ self.playHand(card1, card2, self.dealerUpCard) ]
                    
                # evaluate hands and award bets
                dealerHandList = self.playDealer(self.playerHandList)
                dealerHandTotal = self.totalDealerHand()
                for hand in self.playerHandList:
                    totalBet = 0
                    totalHand = 0
                    aceCount = 0
                    for j in range(len(hand)):
                        if j == len(hand) - 1:
                            totalBet = hand[j]
                        else:
                            totalHand += hand[j].getValue()
                            if hand[j].isAce():
                                aceCount += 1
                    while aceCount != 0:
                        if totalHand > 21:
                            totalHand -= 10
                            aceCount -= 1
                        else:
                            aceCount -= 1

                    # all possible outcomes of bust or comparison of totals
                    if dealerHandTotal > 21:
                        if totalHand > 21:
                            # Push
                            push = True
                        else:
                            # Win
                            self.money += totalBet
                    else:
                        if totalHand > 21:
                            #Bust--Lose
                            self.money -= totalBet
                        elif totalHand == dealerHandTotal:
                            #Push
                            push = True
                        elif totalHand < dealerHandTotal:
                            #Lose
                            self.money -= totalBet
                        elif totalHand > dealerHandTotal:
                            #Win
                            self.money += totalBet

                # Hand is over
                self.showDealerHand(self.playerHandList)
                self.player.endOfHand(self.playerHandList, dealerHandList)
                self.dealerDealtCards = []
                self.playerHandList = []      
            
        return

