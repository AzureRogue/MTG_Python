# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 09:41:17 2018

@author: AzureRogue
"""

import random
import numpy as np
import matplotlib.pyplot as plt

# Create deck distributions based on cards from the popular UB midrange 
# decks (replaced 1x Gearhulk with Belzenlok). Simply coding cards by CMC and 
# L for lands.

# Decklist: https://www.mtggoldfish.com/deck/988603#paper

Hand = []

def initializeDeck():
    global Deck
    Deck = [0, 0, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5, 5, 5, 6, 5, 5, 1,
            1, 1, 1, 2, 3, 4, 4, 4, 4, 8, 8, "B"]
        
    Deck += ["L"]*26
    
def fixedStart():
    global Deck
    global Hand
    Deck = [0, 0, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5, 5, 5, 6, 5, 5, 1,
            1, 1, 1, 2, 3, 4, 4, 4, 4, 8, 8]
    Deck += ["L"]*20
    
    Hand = ["L", "L", "L", "L", "L", "L", "B"]
    random.shuffle(Deck)
    

def drawOpener():
    global Deck
    global Hand
    random.shuffle(Deck)
    openingHand = Deck[0:7]
    Deck = Deck[7:]
    numLands = sum(1 for i in openingHand if i == "L")
    if numLands <= 1:
        Deck = Deck + openingHand
        random.shuffle(Deck)
        openingHand = Deck[0:6]
        Deck = Deck[6:]
    if numLands >= 6:
        Deck = Deck + openingHand
        random.shuffle(Deck)
        openingHand = Deck[0:6]
        Deck = Deck[6:]
    Hand = openingHand

def onPlay():
    global Deck
    global Hand
    Turn = 1
    while "B" not in Hand:
        Turn += 1
        Hand.append(Deck[0])
        Deck.pop(0)
    while sum(1 for i in Hand if i == "L") < 6:
        Turn += 1
        Hand.append(Deck[0])
        Deck.pop(0)
    while Turn < 6:
        Turn += 1
        Hand.append(Deck[0])
        Deck.pop(0)
    return Turn

def onDraw():
    global Deck
    global Hand
    Turn = 1
    Hand.append(Deck[0])
    Deck.pop(0)
    while "B" not in Hand:
        Turn += 1
        Hand.append(Deck[0])
        Deck.pop(0)
    while sum(1 for i in Hand if i == "L") < 6:
        Turn += 1
        Hand.append(Deck[0])
        Deck.pop(0)
    while Turn < 6:
        Turn += 1
        Hand.append(Deck[0])
        Deck.pop(0)
    return Turn

def demonDad():
    Damage = 0
    endit = 0
    while endit == 0:
        if len(Deck) == 0:
            break
        if Deck[0] == "L":
            Deck.pop(0)
        elif Deck[0] < 4:
            Hand.append(Deck[0])
            Deck.pop(0)
            Damage += 1
            endit = 1
        elif Deck[0] >= 4:
            Hand.append(Deck[0])
            Deck.pop(0)
            Damage += 1
    return Damage

results = []

while len(results) < 1000:
    fixedStart()
    Turn = onPlay()
    Damage = demonDad()
    results.append([Turn, Damage, "Play"])
while len(results) < 2000:
    fixedStart()
    Turn = onDraw()
    Damage = demonDad()
    results.append([Turn, Damage, "Draw"])

playDamage = [x[1] for x in results if x[2]=="Play"]
playDmg = np.array(playDamage)
playDmgAvg= np.mean(playDmg)
playDmgStd = np.std(playDmg)
playDmgMin = np.min(playDmg)
playDmgMax = np.max(playDmg)
playDmgMed = np.median(playDmg)

drawDamage = [x[1] for x in results if x[2]=="Draw"]
drawDmg = np.array(drawDamage)
drawDmgAvg= np.mean(drawDmg)
drawDmgStd = np.std(drawDmg)
drawDmgMin = np.min(drawDmg)
drawDmgMax = np.max(drawDmg)
drawDmgMed = np.median(drawDmg)

bins = np.linspace(1,10,10)
plt.hist([playDmg, drawDmg], bins, label=['Play', 'Draw'])
plt.legend(loc="upper right")

"""
while len(results) < 1000:
    initializeDeck()
    drawOpener()
    Turn = onPlay()
    Damage = demonDad()
    results.append([Turn, Damage, "Play"])
while len(results) < 2000:
    initializeDeck()
    drawOpener()
    Turn = onDraw()
    Damage = demonDad()
    results.append([Turn, Damage, "Draw"])
"""