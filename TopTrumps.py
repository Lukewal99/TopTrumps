# Imports
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_text
import random

# Database of cards, listing features of each card
# TODO Change 'database' to a Tuple, why?
# TODO Extend deck database and code to cover 3 choices
database = [[1414,329],[650,1738],[220,1.6],[842,1550],[579,2200],[321,8650]]

# Initial training data
features=[[579,2200,0],[579,2200,1],[321,8650,0],[321,8650,1]]
outcomes=[1,0,0,1]

# Functions
def trainAI(features, outcomes):
    clf = DecisionTreeClassifier()
    # TODO part 3 - Can we improve results by preprocessing data?
    # https://scikit-learn.org/stable/modules/preprocessing.html
    clf.fit(features, outcomes)
    return clf

def humanTurn():
    statChoice = int(input("0 or 1 / "))
    return statChoice

def easyAITurn():
    return random.randint(0,1)

# ToDo Remove the code duplication in this function by removing 'turn'
def hardAITurn(turn, features, outcomes, playerOneHand, playerTwoHand):
    # Train the AI based on the features and outcomes we have so far
    global clf
    clf = trainAI(features, outcomes)

    if turn == "playerOne":
        feature0 = database[playerOneHand[0]][0]  # Feature 0 from top card in playersHand
        feature1 = database[playerOneHand[0]][1]
        # ToDo part 2 - remove Choice from features and make Choice the Outcome
        if clf.predict([[feature0, feature1, 0]]) == 1:
            return(0)  # Choose feature 0
        else:
            return(1)  # Choose feature 1
    else:
        feature0 = database[playerTwoHand[0]][0]
        feature1 = database[playerTwoHand[0]][1]
        if clf.predict([[feature0, feature1, 0]]) == 1:
            return(0)
        else:
            return(1)


def main():
    playerOne = input("Human Player (P), Easy Robot(E) or Hard Robot(H) ")
    playerTwo = input("Human Player (P), Easy Robot(E) or Hard Robot(H) ")

    # Variable to keep track of some statistics
    playerOneWins = 0  # Number of wins by player 1
    playerTwoWins = 0  # Number of wins by player 2
    greatestTurns = 0  # Largest number of turns across all games
    totalTurns = 0  # Total number of turns taken across all games

    gameCount = int(input("How many games would you like to play? "))
    print()

    # Game Loop
    for gameNumber in range(gameCount):
        
        # TODO Randomise which player goes first
        turn = "playerOne"
        turnCount = 0

        # Create & Shuffle the deck
        deck = []
        for cardRef in range(len(database)):
            deck.append(cardRef)
        random.shuffle(deck)

        # Split deck into two hands
        # TODO Deal the cards - one each until no cards left
        playerOneHand = deck[:len(deck)//2]
        playerTwoHand = deck[len(deck)//2:]

        #print("Player One Hand: " + str(playerOneHand))
        #print("Player Two Hand: " + str(playerTwoHand))

        # Take turns until one player has no cards left in their hand
        while (len(playerOneHand)>0 and len(playerTwoHand)>0):
            #print("Game " + str(gameNumber + 1), end=" / ")  # Print a more natural game number
            #print("Turn  " + str(turnCount + 1), end=" / ")  # Print a more natural turn number
            turnCount+=1

            # Choose statistic, ie melting point
            # TODO If you create a function chooseStatistic can you remove the repeating of this section?
            if turn == "playerOne":
                #print("Player One Card: " + str(database[playerOneHand[0]]), end=" / ") 
                if playerOne == "P":
                    statChoice = humanTurn()
                elif playerOne == "E":
                    statChoice = easyAITurn()
                elif playerOne == "H":
                    statChoice = hardAITurn(turn, features, outcomes, playerOneHand, playerTwoHand)
            
            if turn == "playerTwo":
                #print("Player Two Card: " + str(database[playerTwoHand[0]]), end=" / ")
                if playerTwo == "P":
                    statChoice = humanTurn()
                elif playerTwo == "E":
                    statChoice = easyAITurn()
                elif playerTwo == "H":
                    statChoice = hardAITurn(turn, features, outcomes, playerOneHand, playerTwoHand)

            #print("Stat " + str(statChoice) + " Chosen", end=" / ")
            #print("P1 Stat: " + str(database[playerOneHand[0]][statChoice]) + " / P2 Stat: " + str(database[playerTwoHand[0]][statChoice]), end=" / ")

            # If Player 1 wins the hand  
            if database[playerOneHand[0]][statChoice] > database[playerTwoHand[0]][statChoice]:
                # Append the features from top card in player 1's hand and choice to the features training data
                features.append([database[playerOneHand[0]][0], database[playerOneHand[0]][1], statChoice])
                # Append a win for those features and choice to the outcome training data
                outcomes.append(1)

                # Append the features from top card in player 2's hand and choice to the features training data
                features.append([database[playerTwoHand[0]][0], database[playerTwoHand[0]][1], statChoice])
                # Append a loss for those features and choice to the outcome training data
                outcomes.append(0)

                # Declare Winner - Pop cards from top of hand and place at bottom of winners hand
                playerOneHand.append(playerOneHand.pop(0))
                playerOneHand.append(playerTwoHand.pop(0))
                turn = "playerOne"
                #print("Player One Wins")

            # If Player 2 wins the hand
            # TODO 
            elif database[playerOneHand[0]][statChoice] < database[playerTwoHand[0]][statChoice]:
                # Append the features from top card in player 1's hand and choice to the features training data
                features.append([database[playerOneHand[0]][0], database[playerOneHand[0]][1], statChoice])
                # Append a win for those features and choice to the outcome training data
                outcomes.append(0)

                # Append the features from top card in player 2's hand and choice to the features training data
                features.append([database[playerTwoHand[0]][0], database[playerTwoHand[0]][1], statChoice])
                # Append a loss for those features and choice to the outcome training data
                outcomes.append(1)

                # Declare Winner - Pop cards from top of hand and place at bottom of winners hand
                playerTwoHand.append(playerOneHand.pop(0))
                playerTwoHand.append(playerTwoHand.pop(0))
                turn = "playerTwo"
                #print("Player Two Wins")


            # If the Hand Draws
            else:
                playerOneHand.append(playerOneHand.pop(0))
                playerTwoHand.append(playerTwoHand.pop(0))

        # One player has no cards left
        # Win the Game
        print("Game " + str(gameNumber + 1), end=" / ") 
        if (len(playerOneHand) > 0):
            print("Player One Wins The Game!", end=" / ")
            playerOneWins += 1
        else:
            print("Player Two Wins The Game!", end=" / ")
            playerTwoWins += 1

        # Record highest turnCount across all games
        if turnCount > greatestTurns:
            greatestTurns = turnCount

        # Record totalTurns to enable average turns to be calculated across all games
        totalTurns += turnCount

        print("In " + str(turnCount) + " Turns ")
        print()

    print("\nPlayer One (%s) won %d time(s) - %.0f%%" %(playerOne, playerOneWins, (100*(playerOneWins/gameCount))))
    print("Player Two (%s) won %d time(s) - %.0f%%" %(playerTwo, playerTwoWins, (100*(playerTwoWins/gameCount))))
    print("Average turns taken %.1f, max turns taken %d." %(totalTurns/gameCount,greatestTurns))
    #TODO How can we show change in win rates over many games?

    # Export decission tree
    print()
    print(export_text(clf, feature_names=["Feature Zero", "Feature One", "Choice"], decimals=1, show_weights=True))


if __name__ == "__main__":
    main()
