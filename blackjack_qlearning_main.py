#blackjack_qlearning_main.py

from player_Q_Learning import *
from player_1_blackjack import *
from blackjack_game import *

def main():
    game = blackJack(500, 1000000, playerQLearning())

    print('pairsTable')
    print(game.player.pairsTable)
    print('softHandTable')
    print(game.player.softHandTable)
    print('hardHandTable')
    print(game.player.hardHandTable)
    
main()
