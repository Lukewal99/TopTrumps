# Imports
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_text
import random
import math

# Database of cards, listing features of each card
database = ([1414,2329,16],[650,1738,3.3],[-220,1.6,99],[579,2200,5.3],[321,8650,24],[115,2070,1.3],[-102,2.9,18],[1538,7874,1.9],[4489,2260,1.2],[64,862,190],[1085,8960,4.7],[962,10500,310],[842,1550,20])

winsTracker = []

# Initial training data
features=[[579,2200,5.3],[321,8650,24],[64,862,190],[1085,8960,4.7],[1085,8960,4.7]]
outcomes=[0,1,2,0,1]

# Functions
def turnDecider(player,playerHand,gameCount):
    if gameCount <= 10:
        print("Player Card: " + str(database[playerHand[0]]), end=" / ") 
    if player == "P":
        statChoice = humanTurn()
    elif player == "E":
        statChoice = easyAITurn()
    elif player == "H":
        statChoice = hardAITurn(features, outcomes, playerHand)
    return statChoice

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

def hardAITurn(features, outcomes, playerHand):
    # Train the AI based on the features and outcomes we have so far
    global clf
    clf = trainAI(features, outcomes)

    feature0 = database[playerHand[0]][0]  # Feature 0 from top card in playersHand
    feature1 = database[playerHand[0]][1]
    feature2 = database[playerHand[0]][2]
    #! ToDo part 2 - remove Choice from features and make Choice the Outcome
    return clf.predict([[feature0, feature1, feature2]])[0]



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
        
        turn = random.randint(1,2)
        turnCount = 0

        # Create & Shuffle the deck
        deck = []
        for cardRef in range(len(database)):
            deck.append(cardRef)
        random.shuffle(deck)

        # Split deck into two hands
        playerOneHand = []
        playerTwoHand = []
        #!TODO Improve code logic!
        for cardPointer in range(0,len(deck)-1,2):
            playerOneHand.append(deck[cardPointer])
            if cardPointer < len(deck):
                playerTwoHand.append(deck[cardPointer+1])

        if gameCount <= 10:
            print("Player One Hand: " + str(playerOneHand))
            print("Player Two Hand: " + str(playerTwoHand))

        # Take turns until one player has no cards left in their hand
        while (len(playerOneHand)>0 and len(playerTwoHand)>0):
            if gameCount <= 10:
                print("Game " + str(gameNumber + 1), end=" / ")  # Print a more natural game number
                print("Turn  " + str(turnCount + 1), end=" / ")  # Print a more natural turn number
            turnCount+=1

            # Choose statistic, ie melting point
            if turn == 1:
                statChoice = turnDecider(playerOne, playerOneHand, gameCount)
            
            elif turn == 2:
                statChoice = turnDecider(playerTwo, playerTwoHand, gameCount)

            if gameCount <= 10:
                print("Stat " + str(statChoice) + " Chosen", end=" / ")
                print("P1 Stat: " + str(database[playerOneHand[0]][statChoice]) + " / P2 Stat: " + str(database[playerTwoHand[0]][statChoice]), end=" / ")


            # If Player 1 wins the hand  
            if database[playerOneHand[0]][statChoice] > database[playerTwoHand[0]][statChoice]:
                # Append the features from top card in player 1's hand and choice to the features training data
                features.append([database[playerOneHand[0]][0], database[playerOneHand[0]][1], database[playerOneHand[0]][2]])
                # Append a win for those features and choice to the outcome training data
                outcomes.append(statChoice)

                # Declare Winner - Pop cards from top of hand and place at bottom of winners hand
                playerOneHand.append(playerOneHand.pop(0))
                playerOneHand.append(playerTwoHand.pop(0))
                turn = 1

                if gameCount <= 10:
                    print("Player One Wins")

            # If Player 2 wins the hand
            elif database[playerOneHand[0]][statChoice] < database[playerTwoHand[0]][statChoice]:
                # Append the features from top card in player 2's hand and choice to the features training data
                features.append([database[playerTwoHand[0]][0], database[playerTwoHand[0]][1], database[playerTwoHand[0]][2]])
                # Append a loss for those features and choice to the outcome training data
                outcomes.append(statChoice)

                # Declare Winner - Pop cards from top of hand and place at bottom of winners hand
                playerTwoHand.append(playerOneHand.pop(0))
                playerTwoHand.append(playerTwoHand.pop(0))
                turn = 2

                if gameCount <= 10:
                    print("Player Two Wins")


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
            winsTracker.append(1)
        else:
            print("Player Two Wins The Game!", end=" / ")
            playerTwoWins += 1
            winsTracker.append(2)

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
    
    winTrackerDecider = input("Do you want to tack win progression? (Y/N) ")
    if winTrackerDecider == "Y":

        playerOneTenthWins = 0
        playerTwoTenthWins = 0 
        playerOneWinsInTenths = []
        playerTwoWinsInTenths = []

        winIterableLength = math.floor(len(winsTracker)/10)
        for tenthIterable in range (0,9):
            for winTrackerIterable in range(0,winIterableLength):
                if len(winsTracker) >= (winTrackerIterable + 10*tenthIterable):
                    if winsTracker[(winTrackerIterable + 10*tenthIterable)] == 1:
                        playerOneTenthWins += 1
                    else:
                        playerTwoTenthWins += 1
            playerOneWinsInTenths.append(playerOneTenthWins)
            playerTwoWinsInTenths.append(playerTwoTenthWins)
            playerOneTenthWins = 0
            playerTwoTenthWins = 0

        print("Player One won X times in each tenth: ", end="")
        print(playerOneWinsInTenths)
        print("Player Two won X times in each tenth: ", end = "")
        print(playerTwoWinsInTenths) 

    if playerOne == "H" or playerTwo == "H":
        # Export decission tree
        print()
        print(export_text(clf, feature_names=["Feature Zero", "Feature One", "Feature Two"], decimals=1, show_weights=True))


if __name__ == "__main__":
    main()
