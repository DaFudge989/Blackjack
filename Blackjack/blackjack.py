import pygame
from pygame.locals import *
import math
import time
import random
import os
import json
from blackjackSystems import *

sourceFileDir = os.path.dirname(os.path.abspath(__file__))

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
dark_green = (0,160,0)
light_green = (0,200,0)
red = (255,0,0)
light_red = (200,0,0)
blue = (0,0,255)
ehh = (255,255,0)
purple = (255,0,255)
light_grey = (220,220,220)
lighter_grey = (190,190,190)
grey = (150,150,150)
turqoise = (0,220,220)
dark_turqoise = (0, 148, 148)
orange = (230,121,44)
dark_orange = (163,87,33)
pink = (219, 13, 219)
dark_pink = (148, 7, 148)
rose = (219, 0, 80)
dark_rose = (145, 0, 53)
yellow = (255, 238, 0)

pygame.init()


gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Blackjack')
clock = pygame.time.Clock()

images = {}

for card in makeDeck():
    images[card] = pygame.image.load(sourceFileDir + "/cards/" + card + ".png")
images["Back"] = pygame.image.load(sourceFileDir + "/cards/" + "Back" + ".png")

def displayText(text, x, y, center=False, font=pygame.font.SysFont("futura",15)):
    textSurface = font.render(text, True, blue)
    textRect = textSurface.get_rect()
    #print(text, textRect)
    if center == True:
        textRect.center = (x, y)
    else:
        textRect = (x, y)
    gameDisplay.blit(textSurface, textRect)

def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

def button(msg,x,y,w,h,ic,ac,action,aoh,test=None,test2=None,test3=None):
    mouse = pygame.mouse.get_pos()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if aoh == True:
            action()
        if gameInfo.mdn == True and action != None:
            if test != None:
                if test3 != None:
                    gameInfo.mdn = False
                    action(test,test2,test3)
                elif test2 != None:
                    gameInfo.mdn = False
                    action(test,test2)
                else:
                    gameInfo.mdn = False
                    action(test)
            else:
                gameInfo.mdn = False
                action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    displayText(msg, x+(w/2), y+(h/2), True, pygame.font.SysFont("futura",15))

def plusOne():
    if gameInfo.numplayers < 4:
        gameInfo.numplayers = gameInfo.numplayers + 1

def minusOne():
    if gameInfo.numplayers > 0:
        gameInfo.numplayers = gameInfo.numplayers - 1

def increaseDifficulty(number):
    try:
        if gameInfo.players[number+1].difficulty == "Medium":
            gameInfo.players[number+1].difficulty = "Hard"
        elif gameInfo.players[number+1].difficulty == "Easy":
            gameInfo.players[number+1].difficulty = "Medium"
    except:
        if dealer.difficulty == "Medium":
            dealer.difficulty = "Hard"
        elif dealer.difficulty == "Easy":
            dealer.difficulty = "Medium"

def decreaseDifficulty(number):
    try:
        if gameInfo.players[number+1].difficulty == "Hard":
            gameInfo.players[number+1].difficulty = "Medium"
        elif gameInfo.players[number+1].difficulty == "Medium":
            gameInfo.players[number+1].difficulty = "Easy"
    except:
        if dealer.difficulty == "Hard":
            dealer.difficulty = "Medium"
        elif dealer.difficulty == "Medium":
            dealer.difficulty = "Easy"

def changeBet(difference):
    if gameInfo.players[0].hand[0][2] == None:
        gameInfo.players[0].hand[0][2] = 0
    if difference+gameInfo.players[0].hand[0][2] < 0:
        gameInfo.players[0].hand[0][2] = 0
    elif difference+gameInfo.players[0].hand[0][2] <= gameInfo.players[0].balance:
        gameInfo.players[0].hand[0][2] = gameInfo.players[0].hand[0][2] + difference
    elif difference+gameInfo.players[0].hand[0][2] > gameInfo.players[0].balance:
        gameInfo.players[0].hand[0][2] = gameInfo.players[0].balance

def decisionMaking(player):
    if checkHandVal(player.hand[0][0])[0] >= 21:
        player.hand[0][3] = True
    if player.hand[0][3] == False:
        if player.difficulty == 'Easy':
            dealCard(player,0)
        elif player.difficulty == 'Medium':
            if checkHandVal(player.hand[0][0])[-1] <= 17:
                dealCard(player,0)
            else:
                stand(player,0)
        elif player.difficulty == 'Hard':
            if checkHandVal(player.hand[0][0])[-1] <= 15:
                dealCard(player,0)
            else:
                stand(player,0)

def finishAction():
    if gameInfo.setupState == "menu":
        gameInfo.setupState = "numOfPlayers"
    elif gameInfo.setupState == "numOfPlayers":
        for i in range(gameInfo.numplayers):
            gameInfo.players.append(Ai())
        gameInfo.setupState = "playerSettings"
    elif gameInfo.setupState == "playerSettings":
        gameInfo.setupState = "game"
    elif gameInfo.setupState == "game":
        if gameInfo.gameState == "betting":
            gameInfo.players[0].balance = gameInfo.players[0].balance - gameInfo.players[0].hand[0][2]
            for player in gameInfo.players:
                for i in range(2):
                    dealCard(player, 0)
            for i in range(2):
                dealCard(dealer, 0)
            gameInfo.gameState = "playing"
        elif gameInfo.gameState == "playing":
            gameInfo.gameState = "finish"
        elif gameInfo.gameState == "finish":
            if gameInfo.players[0].balance == 0:
                gameInfo.setupState = "lose"
            for each in range(len(gameInfo.players)):
                gameInfo.players[each].hand = [[[], None , None, False]]
            dealer.hand =  [[[], None , None, False]]
            gameInfo.deck = makeDeck()
            shuffleDeck(gameInfo.deck)
            gameInfo.payout = False
            gameInfo.gameState = "betting"

def main_menu():
    i = 1
    for card in gameInfo.blitDeck[0]:
        i = i+1
        x = 368 + 300*math.cos((i+gameInfo.blitDeck[1])*(math.pi/180))
        y = 276 + 300*math.sin((i+gameInfo.blitDeck[1]*2)*(math.pi/180))
        gameDisplay.blit(images[card], (x,y))

    if len(gameInfo.newDeck) > 0 and len(gameInfo.blitDeck[0]) < 360:    
        gameInfo.blitDeck[0].append(gameInfo.newDeck[0])
        gameInfo.newDeck.pop(0)
    
    elif len(gameInfo.blitDeck[0]) < 360:
        gameInfo.newDeck = makeDeck()
        gameInfo.blitDeck[0].append(gameInfo.newDeck[0])
        gameInfo.newDeck.pop(0)
    
    gameInfo.blitDeck[1] = gameInfo.blitDeck[1] + 1

    displayText("Welcome To Blackjack",400,250, True, font=pygame.font.SysFont("futura", 30))
    button("Start Game", 350, 300, 100, 50, green, dark_green, finishAction, False)

def numOfPlayers():
    button("+1 Player", 280, 250, 100, 50, orange, dark_orange, plusOne, False)
    button("-1 Player", 420, 250, 100, 50, orange, dark_orange, minusOne, False)
    displayText("Number of Players: " + str(gameInfo.numplayers),400, 200, True)
    button("Done", 350, 400, 100, 50, green, dark_green, finishAction, False)

def playerSettings():
    for number in range(gameInfo.numplayers):
        button(">", 300, 250+((number-1)*100), 30, 30, orange, dark_orange, increaseDifficulty, False, number)
        button("<", 270, 250+((number-1)*100), 30, 30, orange, dark_orange, decreaseDifficulty, False, number)
        displayText("Player "+str(number+1)+": "+gameInfo.players[number+1].difficulty, 300,240+((number-1)*100),True)
    displayText("Dealer: " + str(dealer.difficulty), 520, 190, True)
    button("<", 520, 200, 30, 30, orange, dark_orange,decreaseDifficulty, False, "dealer")
    button(">", 550, 200, 30, 30, orange, dark_orange,increaseDifficulty, False, "dealer")
    button("Done", 500, 400, 100, 50, green, dark_green, finishAction, False)

def game_loop():
    while True:
        for event in pygame.event.get():
            #print(event.type)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                gameInfo.mdn = True
            if event.type == pygame.MOUSEBUTTONUP:
                gameInfo.mdn = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pass
                if event.key == pygame.K_RIGHT:
                    pass
                if event.key == pygame.K_UP:
                    #dealCard(gameInfo.players[0], 0)
                    pass
                if event.key == pygame.K_DOWN:
                    pass
                if event.key == pygame.K_SPACE:
                    pass
        gameDisplay.fill(grey)
        
        if gameInfo.setupState == "menu":
            main_menu()
        
        elif gameInfo.setupState == "numOfPlayers":
            numOfPlayers()

        elif gameInfo.setupState == "playerSettings":
            playerSettings()

        elif gameInfo.setupState == "game":
            i = -1
            for player in range(gameInfo.numplayers):
                i = i + 1
                j = 0
                displayText("Player " + str(i+1),100+i*200,40,True)
                displayText("Value: " + ', '.join([str(i) for i in checkHandVal(gameInfo.players[player+1].hand[0][0])]),100+i*200,139,True)
                displayText("Chips: " + str(gameInfo.players[player+1].balance),100+i*200,154,True)
                displayText("Bet: " + ', '.join([str(i[2]) for i in gameInfo.players[player+1].hand]),100+i*200,169,True)
                for card in gameInfo.players[player+1].hand[0][0]:
                    gameDisplay.blit(images[card], (55+15*j+i*200,60))
                    j = j + 1
            
            displayText("Dealer", 650, 250, True)
            if dealer.revealed == True:
                displayText("Value: " + ', '.join([str(i) for i in checkHandVal(dealer.hand[0][0])]), 650, 349, True)
                j = 0
                for count in range(len(dealer.hand[0][0])):
                    gameDisplay.blit(images[dealer.hand[0][0][count]], (620+15*j,270))
                    j = j + 1        
            else:
                displayText("Value: ?", 650, 349, True)
                if len(dealer.hand[0][0]) > 0:
                    gameDisplay.blit(images["Back"], (605,270))
                j = 0
                for count in range(len(dealer.hand[0][0])-1):
                    gameDisplay.blit(images[dealer.hand[0][0][count+1]], (620+15*j,270))
                    j = j + 1

            displayText("Chips: " + str(gameInfo.players[0].balance),100,574,True)
            for row in range(len(gameInfo.players[0].hand)):
                j = 1
                displayText("Value: " + ', '.join([str(i) for i in checkHandVal(gameInfo.players[0].hand[row][0])]), 325, 545-row*120, True)
                displayText("Bet: " + str(gameInfo.players[0].hand[row][2]), 325, 559-row*120, True)
                for card in gameInfo.players[0].hand[row][0]:
                    j = j + 1
                    gameDisplay.blit(images[card], (280+15*j,465-row*120))


            if gameInfo.gameState == "betting":
                try:
                    if gameInfo.players[1].hand[0][2] == None:
                        for i in range(gameInfo.numplayers):
                            bet = 0
                            if gameInfo.players[i+1].difficulty == 'Easy':
                                bet = random.randint(1,50)
                            elif gameInfo.players[i+1].difficulty == 'Medium':
                                bet = random.randint(51,99)
                            elif gameInfo.players[i+1].difficulty == 'Hard':
                                bet = random.randint(100,200)
                            if bet > gameInfo.players[i+1].balance:
                                gameInfo.players[i+1].hand[0][2] = gameInfo.players[i+1].balance
                                gameInfo.players[i+1].balance = 0
                            else:
                                gameInfo.players[i+1].hand[0][2] = bet
                                gameInfo.players[i+1].balance = gameInfo.players[i+1].balance - bet
                except:
                    pass

                displayText("Your Bet: " + str(gameInfo.players[0].hand[0][2]),300,300,True)
                button("+1",300,315,40,30,orange,dark_orange,changeBet,False,1)
                button("+10",300,345,40,30,orange,dark_orange,changeBet,False,10)
                button("+100",300,375,40,30,orange,dark_orange,changeBet,False,100)
                button("-1",260,315,40,30,orange,dark_orange,changeBet,False,-1)
                button("-10",260,345,40,30,orange,dark_orange,changeBet,False,-10)
                button("-100",260,375,40,30,orange,dark_orange,changeBet,False,-100)

                if gameInfo.players[0].hand[0][2] != None:  
                    button("Done", 420, 335, 100, 50, green, dark_green, finishAction, False)


            elif gameInfo.gameState == "playing":
                for hand in range(len(gameInfo.players[0].hand)):
                    if gameInfo.activeHand == False:
                        gameInfo.activeHandIndex = hand
                    if gameInfo.activeHand == True and gameInfo.activeHandIndex != hand:
                        continue
                    pygame.draw.rect(gameDisplay, yellow, [270, 450-gameInfo.activeHandIndex*120, 170, 130], 3)
                    if checkHandVal(gameInfo.players[0].hand[hand][0])[0] >= 21:
                        gameInfo.players[0].hand[hand][3] = True
                        gameInfo.activeHand = False
                    if gameInfo.players[0].hand[hand][3] == False:
                        gameInfo.activeHand = True
                        button("Hit", 50, 500, 100, 50, pink, dark_pink, hit, False, gameInfo.players[0],hand)
                        button("Stand", 50, 440, 100, 50, green, dark_green, stand, False, gameInfo.players[0],hand)
                    if len(gameInfo.players[0].hand[hand][0]) == 2 and gameInfo.players[0].hand[hand][0][0][0] == gameInfo.players[0].hand[hand][0][1][0]:
                        button("Split", 50, 380, 100, 50, turqoise, dark_turqoise, split, False, gameInfo.players[0],hand,gameInfo.players[0].hand[hand][0][0])
                    if len(gameInfo.players[0].hand[hand][0]) == 2:
                        button("Double Down", 50, 320, 100, 50, rose, dark_rose, doubleDown, False, gameInfo.players[0], hand)
                
                for each in range(gameInfo.numplayers):
                    decisionMaking(gameInfo.players[each+1])


                if gameInfo.players[0].hand[-1][3] == True:
                    finishAction()

            elif gameInfo.gameState == "finish":
                decisionMaking(dealer)
                dealer.revealed = True

                if gameInfo.payout == False:
                    gameInfo.payout = True
                    for each in gameInfo.players:
                        for hand in each.hand:
                            if len(hand[0]) == 2 and checkHandVal(hand[0])[-1] == 21:
                                each.balance = each.balance + int(hand[2]*2.5)
                                continue
                            if checkHandVal(hand[0])[-1] > checkHandVal(dealer.hand[0][0])[-1] and checkHandVal(hand[0])[-1] < 22 or checkHandVal(hand[0])[-1] < 22 and checkHandVal(dealer.hand[0][0])[-1] > 21:
                                each.balance = each.balance + int(hand[2]*2)

                button("Done", 420, 335, 100, 50, green, dark_green, finishAction, False)

        elif gameInfo.setupState == "lose":
            displayText("You Lost All Your Chips",400,250,True,font=pygame.font.SysFont("futura", 30))

        button("Quit", 690,540, 100, 50, red, light_red, quit, False)


        pygame.display.update()
        clock.tick(60)

gameInfo.deck = makeDeck()
gameInfo.newDeck = makeDeck()
shuffleDeck(gameInfo.deck)

players = []

gameInfo.players.append(Player())

dealer = Dealer()



game_loop()
pygame.quit()
quit()