# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 12:48:10 2019

CURRENT ISSUES:
    - will only cast one spell per turn, would need nested where loops to cast 
      more than one until we run out of lands
    - still need to write functions to cast the various spells in the deck
    
@author: fxsmith
"""

import random
from collections import Counter
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

Hand = []
InPlay = []
Graveyard = []
Deck = []
Turn = 0

winningTurn = []

def cardDraw(n):
    global Deck
    global Hand
    Hand += Deck[0:n]
    Deck = Deck[n:]

def scry(n):
    global Deck
    top = []
    bottom = []
    scryCards = Deck[0:n]
    for card in scryCards:
        if card[0] == "Land":
            if len([x for x in InPlay if x[0]=="Land"]) < 6:
                top.append(card)
            else:
                bottom.append(card)
        elif card[1] not in [x[1] for x in Hand]:
            top.append(card)
        else:
            bottom.append(card)
    Deck = Deck[n:]
    Deck += bottom
    Deck = top + Deck

def surveil(n):
    global Deck
    global Graveyard
    top = []
    bottom = []
    scryCards = Deck[0:n]
    for card in scryCards:
        if card[0] == "Land":
            if len([x for x in InPlay if x[0]=="Land"]) < 6:
                top.append(card)
            else:
                bottom.append(card)
        elif card[1] not in [x[1] for x in Hand]:
            top.append(card)
        else:
            bottom.append(card)
    Deck = Deck[n:]
    Graveyard += bottom
    Deck = top + Deck

def castAnticipate():
    global Deck
    global Hand
    lookAt = 0
    keep = []
    bottom = []
    scryCards = Deck[0:3]
    Deck = Deck[3:]
    while len(keep) < 1:
        if scryCards[lookAt][0] == "Land":
            if len([x for x in InPlay if x[0]=="Land"]) < 6:
                keep.append(scryCards[lookAt])
                lookAt += 1
            elif lookAt >= 2:
                keep.append(scryCards[lookAt])
            else:
                bottom.append(scryCards[lookAt])
                lookAt += 1
        elif scryCards[lookAt][1] not in [x[1] for x in Hand]:
            keep.append(scryCards[lookAt])
            lookAt += 1
        elif lookAt >= 2:
            keep.append(scryCards[lookAt])
        else:
            bottom.append(scryCards[lookAt])
            lookAt += 1
    if lookAt < 2:
        bottom += scryCards[lookAt:]
    Deck += bottom
    Hand += keep
            
def initializeDeck():
    global Deck
    global Hand
    global InPlay
    global Graveyard
    global Turn
    Hand = []
    InPlay = []
    Graveyard = []
    Turn = 0
    Deck = []
    Deck += [("Opt", 1)]*4
    Deck += [("Anticipate", 2)]*4
    Deck += [("Blink of an Eye", 2)]*4
    Deck += [("Disperse", 2)]*2
    Deck += [("Secrets of the Golden City", 3)]*4
    Deck += [("Chemister's Insight", 4)]*4
    Deck += [("Precognitive Perception", 5)]*4
    Deck += [("Atemsis", 6)]*4
    Deck += [("Discovery/Dispersal", 7)]*4
    Deck += [("Vilis",8)]*2
    Deck += [("Land",0)]*24
    
def drawOpener():
    global Deck
    global Hand
    random.shuffle(Deck)
    openingHand = Deck[0:7]
    Deck = Deck[7:]
    while len([x for x in openingHand if x[0]=="Land"]) <= 1:
        Deck = Deck + openingHand
        random.shuffle(Deck)
        openingHand = Deck[0:7]
        Deck = Deck[7:]
    while len([x for x in openingHand if x[0]=="Land"]) >= 6:
        Deck = Deck + openingHand
        random.shuffle(Deck)
        openingHand = Deck[0:7]
        Deck = Deck[7:]
    Hand = openingHand
    Hand.sort(key=lambda x: x[1])

def takeTurn():
    global Deck
    global Hand
    global InPlay
    global Turn
    
    while "Atemsis" not in [x[0] for x in InPlay] or len(set([x[1] for x in Hand])) < 6:
            
        Turn += 1
        print("TURN: " + str(Turn))
        try:
            Hand.append(Deck[0])
            Deck.pop(0)
        except:
            return 1000
            break
        Hand.sort(key=lambda x: x[1])
        
        if Hand[0][0] == "Land":
            if len([x for x in InPlay if x[0]=="Land"]) < 6:
                InPlay.append(Hand[0])
                Hand.pop(0)
        
        availableLands = [x for x in InPlay if x[0]=="Land"]
        
        castableSpells = [x for x in Hand if x[0]!="Land" and x[1] <= len(availableLands)]
        while len(castableSpells) > 0:
            if "Atemsis" in [x[0] for x in InPlay] and len(set([x[1] for x in Hand])) > 5:
                break
            print("Lands in play and untapped: " + str(len(availableLands)))
            if "Atemsis" in [x[0] for x in castableSpells] and "Atemsis" not in [x[0] for x in InPlay]:
                preferredSpell = ("Atemsis", 6)
            else:
                castableSpells.sort(key=lambda x: x[1], reverse=True)
                checkCMCs = Counter(castableSpells)
                preferredSpell = checkCMCs.most_common(1)[0][0]
        
            print("Casting " + preferredSpell[0])
            Hand.remove(preferredSpell)
            availableLands = availableLands[preferredSpell[1]:]
            
            if preferredSpell[0] == "Atemsis":
                InPlay.append(preferredSpell)
            
            if preferredSpell[0] == "Opt":
                Graveyard.append(preferredSpell)
                scry(1)
                cardDraw(1)
            
            if preferredSpell[0] == "Anticipate":
                Graveyard.append(preferredSpell)
                castAnticipate()
            
            if preferredSpell[0] == "Blink of an Eye":
                Graveyard.append(preferredSpell)
            
            if preferredSpell[0] == "Disperse":
                Graveyard.append(preferredSpell)
            
            if preferredSpell[0] == "Secrets of the Golden City":
                Graveyard.append(preferredSpell)
                if len(InPlay) >= 10:
                    cardDraw(3)
                else:
                    cardDraw(2)
            
            if preferredSpell[0] == "Chemister's Insight":
                Graveyard.append(preferredSpell)
                cardDraw(2)
                # No added Jump-Start at the moment, consider this later
            
            if preferredSpell[0] == "Precognitive Perception":
                Graveyard.append(preferredSpell)
                scry(3)
                cardDraw(3)
            
            if preferredSpell[0] == "Discovery/Dispersal":
                Graveyard.append(preferredSpell)
                surveil(2)
                cardDraw(1)
            
            if preferredSpell[0] == "Vilis":
                InPlay.append(preferredSpell)            
    
            castableSpells = [x for x in Hand if x[0]!="Land" and x[1] <= len(availableLands)]

    return(Turn)
             
while len(winningTurn) < 5000:
    initializeDeck()
    drawOpener()
    result = takeTurn()
    winningTurn.append(result + 1)

winningTurn = np.array(winningTurn)
winTAvg = np.mean(winningTurn)
winTStd = np.std(winningTurn)
winTMin = np.min(winningTurn)
winTMax = np.max(winningTurn)
winTMed = np.median(winningTurn)
winTMode = stats.mode(winningTurn)


bins = np.linspace(1,30,30)
plt.hist(winningTurn, bins)

