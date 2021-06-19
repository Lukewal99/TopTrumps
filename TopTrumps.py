#Imports
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_text
import random

#Database of cards, listing features of each card
database = [[1414,329],[650,1738],[220,1.6],[842,1550],[579,2200],[321,8650]]

#Initial training Data
features=[[579,2200,0],[579,2200,1],[321,8650,0],[321,8650,1]]
outcomes=[1,0,0,1]

#Functions
def trainAI(features, outcomes):
    clf = DecisionTreeClassifier()
    clf.fit(features, outcomes)
    return clf

def humanTurn():
    statChoice = int(input("0 or 1 / "))
    return statChoice

def easyAITurn():
    return random.randint(0,1)

def hardAITurn(turn,features, outcomes):
    clf = trainAI(features, outcomes)
    if turn == "playerOne":
        feature1 = database[playerOneHand[0]][0]
        feature2 = database[playerOneHand[0]][1]
        if clf.predict([[feature1, feature2, 0]]) == 1:
            return(0)
        else:
            return(1)
    else:
        feature1 = database[playerTwoHand[0]][0]
        feature2 = database[playerTwoHand[0]][1]
        if clf.predict([[feature1, feature2, 0]]) == 1:
            return(0)
        else:
            return(1)


playerOne = input("Human Player (P), Easy Robot(E) or Hard Robot(H) ")
playerTwo = input("Human Player (P), Easy Robot(E) or Hard Robot(H) ")

playerOneWins = 0
playerTwoWins = 0
greatestTurns = 0
totalTurns = 0

gameCount = int(input("How many games would you like to play? "))
print()

#Game Loop
for i in range(1,gameCount+1):
    turn = "playerOne"
    turnsCount = 0

    #shuffle the deck
    deck = []
    for j in range(0,len(database)):
        deck.append(j)
    random.shuffle(deck)

    #Split deck into two hands
    playerOneHand = deck[:len(deck)//2]
    playerTwoHand = deck[len(deck)//2:]

    print("Player One Hand: " + str(playerOneHand))
    print("Player Two Hand: " + str(playerTwoHand))

    while (len(playerOneHand)>0 and len(playerTwoHand)>0):
        print("Game " + str(i), end=" / ")
        turnsCount+=1

        #Choose statistic, ie melting point
        if turn == "playerOne":
            print("Player One Card: " + str(database[playerOneHand[0]]), end=" / ") 
            if playerOne == "P":
                statChoice = humanTurn()
            elif playerOne == "E":
                statChoice = easyAITurn()
            elif playerOne == "H":
                statChoice = hardAITurn(turn,features, outcomes)
        

        if turn == "playerTwo":
            print("Player Two Card: " + str(database[playerTwoHand[0]]), end=" / ")
            if playerTwo == "P":
                statChoice = humanTurn()
            elif playerTwo == "E":
                statChoice = easyAITurn()
            elif playerTwo == "H":
                statChoice = hardAITurn(turn,features, outcomes)



        print("Statistic " + str(statChoice) + " Chosen", end=" / ")
        print("P1 Stat: " + str(database[playerOneHand[0]][statChoice]) + " / P2 Stat: " + str(database[playerTwoHand[0]][statChoice]), end=" / ")

        #If Player 1 Wins the Hand               
        if database[playerOneHand[0]][statChoice] > database[playerTwoHand[0]][statChoice]:
            #Add to training Data
            #Player 1
            placeholderCardOne = [0,0]
            placeholderCardOne[0] = database[playerOneHand[0]][0]
            placeholderCardOne[1] = database[playerOneHand[0]][1]
            placeholderCardOne.append(statChoice)
            features.append(placeholderCardOne)
            outcomes.append(1)
            #Player 2
            placeholderCardTwo = [0,0]
            placeholderCardTwo[0] = database[playerTwoHand[0]][0]
            placeholderCardTwo[1] = database[playerTwoHand[0]][1]
            placeholderCardTwo.append(statChoice)
            features.append(placeholderCardTwo)
            outcomes.append(0)

            #Declare Winner
            playerOneHand.append(playerOneHand.pop(0))
            playerOneHand.append(playerTwoHand.pop(0))
            turn = "playerOne"
            print("Player One Wins")

            

        #If Player 2 Wins the hand
        elif database[playerOneHand[0]][statChoice] < database[playerTwoHand[0]][statChoice]:
            #Add to training Data
            #Player 1
            placeholderCardOne = [0,0]
            placeholderCardOne[0] = database[playerOneHand[0]][0]
            placeholderCardOne[1] = database[playerOneHand[0]][1]
            placeholderCardOne.append(statChoice)
            features.append(placeholderCardOne)
            outcomes.append(0)
            #Player 2
            placeholderCardTwo = [0,0]
            placeholderCardTwo[0] = database[playerTwoHand[0]][0]
            placeholderCardTwo[1] = database[playerTwoHand[0]][1]
            placeholderCardTwo.append(statChoice)
            features.append(placeholderCardTwo)
            outcomes.append(1)

            #Declare Winner
            playerTwoHand.append(playerOneHand.pop(0))
            playerTwoHand.append(playerTwoHand.pop(0))
            turn = "playerTwo"
            print("Player Two Wins")

        #If the Hand Draws
        else:
            playerOneHand.append(playerOneHand.pop(0))
            playerTwoHand.append(playerTwoHand.pop(0))





    #Win the Game
    if (len(playerOneHand)>0):
        print("Player One Wins The Game!", end=" / ")
        playerOneWins += 1
    else:
        print("Player Two Wins The Game!", end=" / ")
        playerTwoWins += 1

    if turnsCount > greatestTurns:
        greatestTurns = turnsCount

    totalTurns+=turnsCount

    print("In " + str(turnsCount) + " Turns ")
    print()

print("\nPlayer One (%s) won %d time(s) - %.0f%%" %(playerOne, playerOneWins, (100*(playerOneWins/gameCount))))
print("Player Two (%s) won %d time(s) - %.0f%%" %(playerTwo, playerTwoWins, (100*(playerTwoWins/gameCount))))
print("Average turns taken %.1f, max turns taken %d." %(totalTurns/gameCount,greatestTurns))
