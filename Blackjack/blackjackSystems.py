import math
import time
import random
import os
import json
from itertools import combinations

sourceFileDir = os.path.dirname(os.path.abspath(__file__))

suits = ['H','C','D','S']

class Player:
    def __init__(self):
        self.hand = [[[], None , None, False]] #Cards, Value, Bet, Stand
        self.balance = 1000

class Ai(Player):
    def __init__(self):
        super().__init__()
        self.difficulty = 'Medium'

class Dealer(Player):
    def __init__(self):
        super().__init__()
        self.difficulty = 'Medium'
        self.revealed = False

class GameController:
    def __init__(self):
        self.mdn = False
        self.setupState = "menu"
        self.gameState = "betting"
        self.numplayers = 0
        self.players = []
        self.deck = None
        self.newDeck = []
        self.blitDeck = [[],0]
        self.activeHand = False
        self.activeHandIndex = None
        self.payout = False


def makeDeck():
    newDeck = []
    for i in open(sourceFileDir + '/deck.txt', 'r'):
        i = i.rstrip()
        line = i.split(' ')
        for suit in suits:
            for j in line:
                newDeck.append(j+suit)
    return newDeck

def shuffleDeck(list):
    random.shuffle(list)

def dealCard(player, spechand):
    player.hand[spechand][0].append(gameInfo.deck[0])
    gameInfo.deck.pop(0)

def hit(player, hand):
    dealCard(player, hand)

def stand(player, hand):
    player.hand[hand][3] = True
    gameInfo.activeHand = False

def split(player,specificHand,card): #player, player.hand[hand][0], player.hand[hand][2]
    if player.hand[specificHand][2] > player.balance:
        bet = player.balance
    else:
        bet = player.hand[specificHand][2]
    player.balance = player.balance - bet
    player.hand.append([[card], None, bet, False])
    player.hand[specificHand][0].pop(0)
    dealCard(player,specificHand)
    dealCard(player,specificHand+1)

def doubleDown(player, hand):
    if player.hand[hand][2] > player.balance:
        bet = player.balance
    else:
        bet = player.hand[hand][2]
    player.balance = player.balance - bet
    player.hand[hand][2] = player.hand[hand][2] + bet
    dealCard(player,hand)
    stand(player,hand)

def checkHandVal(hand):
    val = [0]
    aceIndex = []
    for index in range(len(hand)):
        if 'A' in hand[index]:
            aceIndex.append(index)
    for card in hand:
        try:
            val[0] = val[0] + int(card[0])
            if int(card[0]) == 1:
                val[0] = val[0] + 9
        except:
            if card[0] != 'A':
                val[0] = val[0] + 10
            else:
                val[0] = val[0] + 1
    for i in range(len(aceIndex)):
        if val[0] + 10*(i+1) <= 21:
            val.append(val[0] + 10*(i+1))
    return val

gameInfo = GameController()

'''
deck = makeDeck()
shuffleDeck(deck)


players = []

for i in range(4):
    players.append(Player())

players.append(Dealer())


for player in players:
    for i in range(2):
        dealCard(player)

hit(players[0])


print(deck)

for player in players:
    print(player.hand)
    print(checkHandVal(player.hand[0][0]))
print(checkHandVal(['1S','1C','2C','AC']))
print("POG")'''