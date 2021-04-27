from blackjack_game import *
from expectimax_agent import *


def main():
    game = blackJack(10000, 10000000, ExpectimaxAgent())
    print('Number of wins ' + str(game.number_of_wins))
    print('Number of loses ' + str(game.number_of_loses))
    print('Number of draws ' + str(game.number_of_draws))
    print('Number of blackjacks ' + str(game.number_of_blackjacks))
    print('Number of splits ' + str(game.player.split_count))


main()
