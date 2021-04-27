#blackjack_qlearning_main.py

from player_Q_Learning import *
from player_1_blackjack import *
from blackjack_game import *

def main():
    game = blackJack(1000000, 10000000, playerQLearning())

    print('Number of wins ' + str(game.number_of_wins))
    print('Number of loses ' + str(game.number_of_loses))
    print('Number of draws ' + str(game.number_of_draws))
    print('Number of blackjacks ' + str(game.number_of_blackjacks))
    print('Number of splits ' + str(game.player.split_count))

    # print('pairsTable')
    # print(game.player.pairsTable)
    # print('softHandTable')
    # print(game.player.softHandTable)
    # print('hardHandTable')
    # print(game.player.hardHandTable)


    
main()
