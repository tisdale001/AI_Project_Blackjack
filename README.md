# AI_Project_Blackjack

AI Project: Blackjack

This was a project for Foundations of Artificial Intelligence, written in Python. We created a blackjack simulation (completely coded by me) that could be played by various ‘computer players’ using different AI methods: expectimax, Monte Carlo, and Q-learning algorithms. For my part, I coded the Blackjack simulation and the Q-learning AI player. We ran thousands of simulations and compared the results (number of wins) of each AI player with an ‘optimal’ player based on accepted/known strategies of Blackjack.

The screenshot below shows what the blackjack simulation looks like if played as a 1-player game.

![blackjack_1](https://user-images.githubusercontent.com/53150782/194774384-9fe0defd-8653-4288-8aab-85c554e23764.PNG)

The screenshot below shows what the tables for different hands look like. The tables are arranged in rows and columns that compare what your total is and what the dealer hand shows (for more information, see rules of blackjack). For instance, the columns in the hard hand table are for hand totals from 21 down to 4, and the rows represent the dealer card showing (2 - 11). 'S' tells you to stay, 'H' tells you to hit, 'D' tells you to double down, 'Y' tells you you should, yes, split the pairs, and 'N' tells you that you should not split. After tens of thousands of simulations, this is the results for Q-learning as applied to blackjack.

![blackjack_2](https://user-images.githubusercontent.com/53150782/194774490-f4af6a50-caa9-486e-8aad-39868a62fcce.PNG)
