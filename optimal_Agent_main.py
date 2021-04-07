from blackjack_game import *
from OptimalAgent import *


def main():
    game = blackJack(1000, 1000000, OptimalAgent())
    print('Number of wins ' + str(game.number_of_wins))
    print('Number of loses ' + str(game.number_of_loses))
    print('Number of draws ' + str(game.number_of_draws))
    print('Number of blackjacks ' + str(game.number_of_blackjacks))
    print('Number of splits ' + str(game.player.split_count))


main()
