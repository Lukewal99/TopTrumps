# Imports
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_text
from keras.models import Sequential
from keras.layers import Dense
import random
import math

# Constants
PLAYER_1 = 1
PLAYER_2 = 2

TOP_CARD = 0

NUM_FEATURES = 3

# Database of cards, listing features of each card
database = ([1414,2329,16],[650,1738,3.3],[-220,1.6,99],[579,2200,5.3],[321,8650,24],[115,2070,1.3],[-102,2.9,18],[1538,7874,1.9],[4489,2260,1.2],[64,862,190],[1085,8960,4.7],[962,10500,310],[842,1550,20])

winsTracker = []
firstRun = True

# Functions
def turnDecider(player, playerHand, features, outcomes):
    if player == "P":
        statChoice = humanTurn()
    elif player == "E":
        statChoice = easyAITurn()
    elif player == "H":
        statChoice = hardAITurn(features, outcomes, playerHand)
    elif player == "X":
        statChoice = extremeAITurn(playerHand)
    return statChoice

def generateTrainingData():
    features = []
    outcomes = []
    # Generate training data
    for _ in range(1, 100):
        # Select two random cards
        randomCardPointerOne = random.randint(0, len(database)-1)
        randomCardPointerTwo = random.randint(0, len(database)-1)
        # Which are not the same
        while randomCardPointerTwo == randomCardPointerOne:
            randomCardPointerTwo = random.randint(0, len(database)-1)
        # Select a random feature
        randomChoice = random.randint(0,2)
        # FIGHT
        # If card One wins - append it to training data
        if database[randomCardPointerOne][randomChoice] > database[randomCardPointerTwo][randomChoice]:
            features.append(database[randomCardPointerOne])
            outcomes.append(randomChoice)
        # If card Two wins - append it to training data
        elif database[randomCardPointerOne][randomChoice] < database[randomCardPointerTwo][randomChoice]:
            features.append(database[randomCardPointerTwo])
            outcomes.append(randomChoice)
    return features, outcomes

def trainHardAI(features, outcomes):
    clf = DecisionTreeClassifier()
    # TODO part 3 - Can we improve results by preprocessing data?
    # https://scikit-learn.org/stable/modules/preprocessing.html
    clf.fit(features, outcomes)
    return clf

def humanTurn():
    statChoice = int(input("0, 1 or 2 / "))
    return statChoice

def easyAITurn():
    return random.randint(0, NUM_FEATURES - 1)

def hardAITurn(features, outcomes, playerHand):
    # Train the AI based on the features and outcomes we have so far
    clf = trainHardAI(features, outcomes)

    feature0 = database[playerHand[TOP_CARD]][0]  # Feature 0 from top card in playersHand
    feature1 = database[playerHand[TOP_CARD]][1]
    feature2 = database[playerHand[TOP_CARD]][2]
    
    return clf.predict([[feature0, feature1, feature2]])[0]

def extremeAITurn(playerHand):
    # Generate prediction
    # predictions = (model.predict([database[playerHand[TOP_CARD]]]) > 0.5).astype("int32")
    predictions = model.predict_classes([database[playerHand[TOP_CARD]]])
    # np.argmax(model.predict([database[playerHand[TOP_CARD]]]), axis=-1)
    return predictions[0][0]



def main():
    # Generate training data
    features, outcomes = generateTrainingData()

    playerOneType = input("Player 1 Type - Human(P); Easy(E), Hard(H) or Extreme Robot(X) ")
    playerTwoType = input("Player 2 Type - Human(P); Easy(E), Hard(H) or Extreme Robot(X) ")

    if playerOneType == "X" or playerTwoType == "X":
        # Neural Network setup
        print("\nTrain extremeAINeural Network")
        global model
        model = Sequential()
        model.add(Dense(12, input_dim=3, activation='relu'))
        model.add(Dense(6, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
        #model.add(Dense(1, activation='softmax'))
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.fit(features, outcomes, epochs=50, batch_size=32, verbose=2)
        print("extremeAI Trained\n")

    # Variable to keep track of some statistics
    playerOneWins = 0  # Number of wins by player 1
    playerTwoWins = 0  # Number of wins by player 2
    greatestTurns = 0  # Largest number of turns across all games
    totalTurns = 0  # Total number of turns taken across all games

    numberOfGames = int(input("How many games would you like to play "))
    print()

    # Game Loop
    for gameNumber in range(numberOfGames):
        
        # Which player will go first?
        player = random.randint(PLAYER_1,PLAYER_2)
        turnNumber = 0

        # Create & Shuffle the "deck" of pointers to "database"
        deck = []
        for cardRef in range(len(database)):
            deck.append(cardRef)
        random.shuffle(deck)

        # Split the "deck" of pointers into "playerOneHand" and "playerTwoHand"
        # "playerOneHand" and "playerTwoHand" are lists of pointers to "database"
        playerOneHand = []
        playerTwoHand = []
        for cardPointer in range(0,len(deck)-1,2):
            playerOneHand.append(deck[cardPointer])
            if cardPointer < len(deck):
                playerTwoHand.append(deck[cardPointer+1])

        if numberOfGames <= 10:
            print("P1 Hand: " + str(playerOneHand))
            print("P2 Hand: " + str(playerTwoHand))

        # Take turns until one player has no cards left in their hand
        while (len(playerOneHand) > 0 and len(playerTwoHand) > 0) and (turnNumber < 100):
            if numberOfGames <= 10:
                print("Game " + str(gameNumber + 1), end=" / ")  # Print a more natural game number
                print("Turn  " + str(turnNumber + 1), end=" / ")  # Print a more natural turn number
                print("P1 Card: " + str(database[playerOneHand[TOP_CARD]]), end=" / ")
                print("P2 Card: " + str(database[playerTwoHand[TOP_CARD]]), end=" / ") 
           # else:
            #    print(player, end="")

            turnNumber+=1

            # Choose statistic, ie melting point
            if player == PLAYER_1:
                statChoice = turnDecider(playerOneType, playerOneHand, features, outcomes)
            
            elif player == PLAYER_2:
                statChoice = turnDecider(playerTwoType, playerTwoHand, features, outcomes)

            if numberOfGames <= 10:
                print("Stat " + str(statChoice) + " Chosen", end=" / ")
                print("P1 Stat: " + str(database[playerOneHand[TOP_CARD]][statChoice]) + " / P2 Stat: " + str(database[playerTwoHand[TOP_CARD]][statChoice]), end=" / ")

            # If Player 1 wins the hand  
            if database[playerOneHand[TOP_CARD]][statChoice] > database[playerTwoHand[TOP_CARD]][statChoice]:
                # Append the features from top card in player 1's hand and choice to the features training data
                features.append(database[playerOneHand[TOP_CARD]])
                # Append a win for those features and choice to the outcome training data
                outcomes.append(statChoice)

                # Declare Winner - Pop cards from top of hand and place at bottom of winners hand
                playerOneHand.append(playerOneHand.pop(TOP_CARD))
                playerOneHand.append(playerTwoHand.pop(TOP_CARD))
                player = PLAYER_1

                if numberOfGames <= 10:
                    print("Player One Wins")

            # If Player 2 wins the hand
            elif database[playerOneHand[TOP_CARD]][statChoice] < database[playerTwoHand[TOP_CARD]][statChoice]:
                # Append the features from top card in player 2's hand and choice to the features training data
                features.append(database[playerTwoHand[TOP_CARD]])
                # Append a loss for those features and choice to the outcome training data
                outcomes.append(statChoice)

                # Declare Winner - Pop cards from top of hand and place at bottom of winners hand
                playerTwoHand.append(playerOneHand.pop(TOP_CARD))
                playerTwoHand.append(playerTwoHand.pop(TOP_CARD))
                player = PLAYER_2

                if numberOfGames <= 10:
                    print("Player Two Wins")


            # If the Hand Draws
            else:
                playerOneHand.append(playerOneHand.pop(TOP_CARD))
                playerTwoHand.append(playerTwoHand.pop(TOP_CARD))

        # One player has no cards left and wins the Game, unless it was called off after too many turns
        print("\nGame " + str(gameNumber + 1), end=" / ") 
        if (len(playerOneHand) > len(playerTwoHand)):
            print("Player One wins the Game", end=" / ")
            playerOneWins += 1
            winsTracker.append(PLAYER_1)
        else:
            print("Player Two wins the Game", end=" / ")
            playerTwoWins += 1
            winsTracker.append(PLAYER_2)

        # Record highest turnCount across all games
        if turnNumber > greatestTurns:
            greatestTurns = turnNumber

        # Record totalTurns to enable average turns to be calculated across all games
        totalTurns += turnNumber

        print("in " + str(turnNumber) + " turns ")

    print("\nPlayer One (%s) won %d time(s) - %.0f%%" %(playerOneType, playerOneWins, (100 * (playerOneWins/numberOfGames))))
    print("Player Two (%s) won %d time(s) - %.0f%%" %(playerTwoType, playerTwoWins, (100 * (playerTwoWins/numberOfGames))))
    print("Average turns taken %.1f, max turns taken %d." %(totalTurns / numberOfGames, greatestTurns))
    
    if numberOfGames > 10:
        # How many wins does each player have in each tenth number of games
        playerOneTenthWins = 0
        playerTwoTenthWins = 0 
        playerOneWinsInTenths = []
        playerTwoWinsInTenths = []

        # Calculate how many games in each tenth (winIterableLength)
        # Note, this code ignores the final len(winsTracker) modulus 10 games (the remainder)
        winIterableLength = math.floor(len(winsTracker) / 10)

        # Iterate through tenths
        for tenthIterable in range(0, 10):
            # Iterate through winIterableLength games in each tenth
            for winTrackerIterable in range(0, winIterableLength):
                # If playerOne wins, count it as such
                if winsTracker[(winTrackerIterable + (winIterableLength * tenthIterable))] == 1:
                    playerOneTenthWins += 1
                else:
                    playerTwoTenthWins += 1
            # Append result to result list and reset TenthWins counts before looping through next tenth
            playerOneWinsInTenths.append(playerOneTenthWins)
            playerTwoWinsInTenths.append(playerTwoTenthWins)
            playerOneTenthWins = 0
            playerTwoTenthWins = 0

        print("Player One won X times in each tenth: ", end="")
        print(playerOneWinsInTenths)
        print("Player Two won X times in each tenth: ", end = "")
        print(playerTwoWinsInTenths)


    if playerOneType == "H" or playerTwoType == "H":
        # Export decission tree
        print()
        #print(export_text(clf, feature_names=["Feature Zero", "Feature One", "Feature Two"], decimals=1, show_weights=True))


if __name__ == "__main__":
    main()
