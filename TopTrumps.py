
import random
database = [[1414,329],[650,1738],[220,1.6],[842,1550]]

playerOne = input("Human Player (P), Easy Robot(E) or Hard Robot(H) ")
playerTwo = input("Human Player (P), Easy Robot(E) or Hard Robot(H) ")

gameCount = int(input("How many games would you like to play? "))
print()

#Game Loop
for i in range(1,gameCount+1):
    turn = "playerOne"
    turnsCount = 0

    #shuffle the deck
    deck = [0,1,2,3]
    random.shuffle(deck)

    #Split deck into two hands
    playerOneHand = deck[:len(deck)//2]
    playerTwoHand = deck[len(deck)//2:]

    print("Player One Hand: " + str(playerOneHand))
    print("Player Two Hand: " + str(playerTwoHand))

    while (len(playerOneHand)>0 and len(playerTwoHand)>0):
        print("Game " + str(i), end=" / ")
        turnsCount+=1

        #Choose statistic ie melting point
        if turn == "playerOne":
            print("Player One Card: " + str(database[playerOneHand[0]]), end=" / ") 
            if playerOne == "P":
                statChoice = int(input("0 or 1 / "))
            elif playerOne == "E":
                statChoice = random.randint(0,1)
            elif playerOne == "H":
                statChoice = random.randint(0,1)
        

        if turn == "playerTwo":
            print("Player Two Card: " + str(database[playerTwoHand[0]]), end=" / ")
            if playerTwo == "P":
                statChoice = int(input("0 or 1 / "))
            elif playerTwo == "E":
                statChoice = random.randint(0,1)
            elif playerTwo == "H":
                statChoice = random.randint(0,1)



        print("Statistic " + str(statChoice) + " Chosen", end=" / ")
        print("P1 Stat: " + str(database[playerOneHand[0]][statChoice]) + " / P2 Stat: " + str(database[playerTwoHand[0]][statChoice]), end=" / ")

        #If Player 1 Win
        if database[playerOneHand[0]][statChoice] > database[playerTwoHand[0]][statChoice]:

            playerOneHand.append(playerOneHand.pop(0))
            playerOneHand.append(playerTwoHand.pop(0))
            turn = "playerOne"
            print("Player One Wins")

        #If Player 2 Win
        elif database[playerOneHand[0]][statChoice] < database[playerTwoHand[0]][statChoice]:
            playerTwoHand.append(playerOneHand.pop(0))
            playerTwoHand.append(playerTwoHand.pop(0))
            turn = "playerTwo"
            print("Player Two Wins")

        #If Draw
        else:
            playerOneHand.append(playerOneHand.pop(0))
            playerTwoHand.append(playerTwoHand.pop(0))


    
    if (len(playerOneHand)>0):
        print("Player One Wins The Game!", end=" / ")
    else:
        print("Player Two Wins The Game!", end=" / ")

    print("In " + str(turnsCount) + " Turns ")
    print()
