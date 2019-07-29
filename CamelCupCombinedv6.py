# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 00:13:22 2019

@author: Connor
"""

from tkinter import *
from tkinter.ttk import *
import random
from random import randint
from functools import partial
from tkinter import messagebox
from tkinter import Menu
import webbrowser
import numpy as np
import operator
import json
import copy
import time
from functools import wraps
import pickle

root = Tk()
 
root.title("Camel Up")
 
root.geometry('950x310')

global blue
global green
global yellow
global orange
global white
global camels
global color
global dier
global camelcolor
global pturn
global p15
global p25
global p1score
global p2score
global fivetile
global camelwinner
global camelloser
global p1winner
global p2winner
global p1loser
global p2loser
global run
global runtype
global start_time
global gamecheck
global endrun
global hlayer1
global hlayer2
global hlayer3
global stepsize
global flatchoicescount
global camellist

'''Variables that can be adjusted'''
'''How often values are printed during bulk runs of training'''
gamecheck = 2500
'''Stopping point for gathering inputs and deep learning'''
endrun = 50000
'''Percent of change to values after training'''
stepsize = .9

'''Variables that should not be adjsuted'''
'''hlayers are the hidden layer sizes'''
hlayer1 = 90
hlayer2 = 90
hlayer3 = 90
run = 0
runtype = 0      
start_time = time.monotonic()
inputdictionary = {}
rolldictionary = {}
btiledictionary = {}
gtiledictionary = {}
ytiledictionary = {}
otiledictionary = {}
wtiledictionary = {}
winnerdictionary = {}
loserdictionary = {}
flatchoicescount = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

'''File with weights and bias for the neural network'''
with open('CamelCupNNweightsbiasv2.pickle','rb') as handle:
    wandb = pickle.load(handle)

'''Balanced inputs files from previous "Find Inputs" run'''
with open('rollrandomdictionary2.json') as g:
    rollranswer = json.load(g)
with open('btilerandomdictionary2.json') as g:
    btileranswer = json.load(g)
with open('gtilerandomdictionary2.json') as g:
    gtileranswer = json.load(g)
with open('ytilerandomdictionary2.json') as g:
    ytileranswer = json.load(g)
with open('otilerandomdictionary2.json') as g:
    otileranswer = json.load(g)
with open('wtilerandomdictionary2.json') as g:
    wtileranswer = json.load(g)
with open('winnerrandomdictionary2.json') as g:
    winnerranswer = json.load(g)
with open('loserrandomdictionary2.json') as g:
    loserranswer = json.load(g)

'''Menu for rules and new game'''
def openrules():
    webbrowser.open_new(r"https://www.fgbradleys.com/rules/rules2/CamelUp-rules.pdf")

menu = Menu(root)
new_item = Menu(menu)
new_item.add_command(label = 'Rules', command=openrules)
menu.add_cascade(label='File',menu=new_item)
new_item.add_command(label = 'New Game', command=restart)
root.config(menu=menu)

'''Create classes for each camel'''
class camel:
    def __init__(self,color,rollstatus,space,cunder,cabove):
        self.color = color
        self.rollstatus = "rolled"
        self.space = 0
        self.cunder = []
        self.cabove = []
    
    '''allow for change for rollstatus,space,cunder'''
    def change_rollstatus(self, crolled):
        self.rollstatus = crolled
    
    def change_space(self,cspace):
        self.space = cspace
    
    def change_under(self,ccunder):
        self.cunder = ccunder
        
    def change_above(self,ccabove):
        self.cabove = ccabove

class bettingtiles:
    def __init__(self,values):
        self.values = values
        self.betcolors = ['blue','green','yellow','orange','white']
    
    def removebettile(self,chosentile):
        self.betcolors.remove(chosentile)
    
    def fulltiles(self):
        self.betcolors = ['blue','green','yellow','orange','white']

'''Initiaialze classes'''

'''Classes for camels'''
blue = camel('blue','unrolled',0,[],[])
green = camel('green','unrolled',0,[],[])
yellow = camel('yellow','unrolled',0,[],[])
orange = camel('orange','unrolled',0,[],[])
white = camel('white','unrolled',0,[],[])

'''Classes for the bettingtiles'''
fivers = bettingtiles(5)
threes = bettingtiles(3)
twos = bettingtiles(2)

'''list of camels for rolling'''
camels = [blue,green,yellow,orange,white]
'''list of camels (unchanging)'''
camellist = [blue,green,yellow,orange,white]

'''Dropdown to select camel for 5,3,2 point bet'''
fivetile = Combobox(root)
fivetile['values']= (fivers.betcolors)
fivetile.grid(column=0,row=3)

threetile = Combobox(root)
threetile['values']= (threes.betcolors)
threetile.grid(column=0,row=5)

twotile = Combobox(root)
twotile['values']= (twos.betcolors)
twotile.grid(column=0,row=7)

'''Dropdown to select overall winner/loser'''
owinner = Combobox(root)
camelwinner = ['blue','green','yellow','orange','white']
owinner['values']= (camelwinner)
owinner.grid(column=0,row=9)

oloser = Combobox(root)
camelloser = ['blue','green','yellow','orange','white']
oloser['values']= (camelloser)
oloser.grid(column=0,row=11)

rolltitle = Label(root, text='Roll')
rolltitle.grid(column=2,row=0)
rollcolor = Label(root, text='Camel Roll')
rollcolor.grid(column=3,row=0)
camelsleft = Label(root, text='Camels Left')
camelsleft.grid(column=4,row=0, columnspan = 4)
turn = Label(root, text='Turn')
turn.grid(column=1,row=0)
cleft = Label(root, text = 'blue, green, yellow, orange, white')
cleft.grid(column=4,row=1,columnspan = 4)

'''Headers'''
loclabel = Label(root, text = "Camel")
loclabel.grid(column=1,row=3)
spacelabel = Label(root, text = "Current Space")
spacelabel.grid(column=2,row=3)
camelsbelow = Label(root, text ="Camels Beneath")
camelsbelow.grid(column=3,row=3,columnspan = 2)

'''Player Hands/Scores'''
playerone = Label(root, text = "Player 1")
playerone.grid(column=6,row=2)
playertwo = Label(root, text = "Player 2")
playertwo.grid(column=7,row=2)
currentscore = Label(root, text = "Score")
currentscore.grid(column=5,row=3)
fivebet = Label(root, text = "Five Place Bets")
fivebet.grid(column=5,row=4)
threebet = Label(root, text = "Three Place Bets")
threebet.grid(column=5,row=5)
twobet = Label(root, text = "Two Place Bets")
twobet.grid(column=5,row=6)
overallwinner = Label(root, text = "Overall Winner")
overallwinner.grid(column=5, row=7)
overallloser = Label(root, text = "Overall Loser")
overallloser.grid(column=5, row=8)

'''Changing Labels for hands/scores'''
p1score = 3
playeronescore = Label(root, text = '3')
playeronescore.grid(column=6,row=3)
p2score = 3
playertwoscore = Label(root, text = '3')
playertwoscore.grid(column=7,row=3) 
player15 = Message(root, text = '',width=150)
player15.grid(column=6,row=4)
player25 = Message(root, text = '',width=150)
player25.grid(column=7,row=4)
player13 = Label(root, text = '')
player13.grid(column=6,row=5)
player23 = Label(root, text = '')
player23.grid(column=7,row=5)
player12 = Label(root, text = '')
player12.grid(column=6,row=6)
player22 = Label(root, text = '')
player22.grid(column=7,row=6)
player1owinner = Label(root,text = '')
player1owinner.grid(column=6,row=7)
player2owinner = Label(root,text = '')
player2owinner.grid(column=7,row=7)
player1oloser = Label(root,text = '')
player1oloser.grid(column=6,row=8)
player2oloser = Label(root,text = '')
player2oloser.grid(column=7,row=8)

'''Betting Tiles'''
p15 = []
p25 = []
p13 = []
p23 = []
p12 = []
p22 = []
p1winner = ''
p1loser = ''
p2winner = ''
p2loser = ''
p1wmod = 0
p2wmod = 0
p1lmod = 0
p2lmod = 0

greenc = Label(root, text = "Green")
greenc.grid(column=1,row=4)
gspace = StringVar()
greenloc = Label(root, textvariable = gspace)
greenloc.grid(column=2, row=4)
bluec = Label(root, text = "Blue")
bluec.grid(column=1,row=5)
bspace = StringVar()
blueloc = Label(root, textvariable = bspace)
blueloc.grid(column=2, row=5)
yellowc = Label(root, text = "Yellow")
yellowc.grid(column=1,row=6)
yspace = StringVar()
yellowloc = Label(root, textvariable=yspace)
yellowloc.grid(column=2, row=6)
orangec = Label(root, text = "Orange")
orangec.grid(column=1,row=7)
ospace = StringVar()
orangeloc = Label(root, textvariable=ospace)
orangeloc.grid(column=2, row=7)
whitec = Label(root, text = "White")
whitec.grid(column=1,row=8)
wspace = StringVar()
whiteloc = Label(root, textvariable=wspace)
whiteloc.grid(column=2, row=8)

'''Camels Beneath Section'''
gcb = Message(root, text = ' ', width=150)
gcb.grid(column=3,row=4,columnspan =2)
bcb = Label(root, text = ' ')
bcb.grid(column=3,row=5,columnspan =2)
ycb = Label(root, text = ' ')
ycb.grid(column=3,row=6,columnspan =2)
ocb = Label(root, text = ' ')
ocb.grid(column=3,row=7,columnspan =2)
wcb = Label(root, text = ' ')
wcb.grid(column=3,row=8,columnspan =2)

dier = StringVar()
rollresult = Label(root, textvariable=dier)
rollresult.grid(column=2, row=1)
camelcolor = StringVar()
colorresult = Label(root, textvariable=camelcolor)
colorresult.grid(column=3,row=1)
pturn = StringVar()
playerturn = Label(root, textvariable=str(pturn))
playerturn.grid(column=1,row=1)
pturn.set('Player 1')

def sigmoid(x):
    return 1/(1+np.exp(-x))

def newactivation(dweight,dbias,prevact):
    newactw = dweight * prevact
    newactb = dbias + newactw
    newactivation = sigmoid(newactb)
    return newactivation

'''Finds the choice from current weights and biases'''
def newneuronmatrix(inputs, paction, pdec, available):
    inputm = np.matrix(inputs)
    inputmatrix = np.transpose(inputm)
    
    activation1 = newactivation(wandb["wmat1"],wandb["bmat1"],inputmatrix)
    activation2 = newactivation(wandb["wmat2"],wandb["bmat2"],activation1)
    activation3 = newactivation(wandb["wmat3"],wandb["bmat3"],activation2)
    activation4 = newactivation(wandb["wmat4"],wandb["bmat4"],activation3)
    
    finalactivation = activation4
    choicemax = np.minimum(finalactivation,available)
    outputlist = choicemax.tolist()
    aichoice = outputlist.index(max(outputlist))
    
    flatchoices = ['roll','btile', 'gtile', 'ytile', 'otile', 'wtile', 'wblue', 'wgreen','wyellow','worange','wwhite',\
                 'lblue', 'lgreen','lyellow','lorange','lwhite']
    
    aiplayerselection = flatchoices[aichoice]
    formatchoice = activation4[aichoice].item()
    aiformatchoice = round(formatchoice*100,3)
    aiplayermsg = ("AI is {}% positive of this answer.".format(aiformatchoice))
    aimessagechoice(aiplayermsg,aiplayerselection)

'''camelcheck is used for troubleshooting issues'''
def camelcheck():
    global camellist
    print("BLUE CAMEL")
    print("space {}  Under {}  Above {}".format(blue.space,blue.cunder,blue.cabove))
    print("")
    print("GREEN CAMEL")
    print("space {}  Under {}  Above {}".format(green.space,green.cunder,green.cabove))
    print("")
    print("YELLOW CAMEL")
    print("space {}  Under {}  Above {}".format(yellow.space,yellow.cunder,yellow.cabove))
    print("")
    print("ORANGE CAMEL")
    print("space {}  Under {}  Above {}".format(orange.space,orange.cunder,orange.cabove))
    print("")
    print("WHITE CAMEL")
    print("space {}  Under {}  Above {}".format(white.space,white.cunder,white.cabove))
    print("")
    print("END CAMEL CHECK")
    print("")

def camelcolorleft():
    global camellist
    remainingcamels = []
    for c in camellist:
        if c.rollstatus == "unrolled":
            remainingcamels.append(c.color)
    return remainingcamels

def camelclassleft():
    global camellist
    remainingcamels = []
    for c in camellist:
        if c.rollstatus == "unrolled":
            remainingcamels.append(c)
    return remainingcamels

def playerscoring(player, scoreadjustment, currentscore):
    global p1score
    global p2score
    if player == 1:
        adjscore = scoreadjustment + currentscore
        playeronescore.configure(text = str(adjscore))
        p1score = adjscore
    else:
        adjscore = scoreadjustment + currentscore
        playertwoscore.configure(text = str(adjscore))
        p2score = adjscore

'''choicesrun is based of the flatchoicescount from the "findinputs" run'''
def choosescenario(choiceofinputs,choicesrun,choiceofflat):
    randscenario = random.randint(0,choicesrun)
    return choiceofinputs["{}{}".format(choiceofflat,randscenario)]

def getranddictionary():
    global run
    rcw4 = np.zeros(shape=(16,hlayer3))
    rcw3 = np.zeros(shape=(hlayer3,hlayer2))
    rcw2 = np.zeros(shape=(hlayer2,hlayer1))
    rcw1 = np.zeros(shape=(hlayer1,32))
    rcb4 = np.zeros(shape=(16,1))
    rcb3 = np.zeros(shape=(hlayer3,1))
    rcb2 = np.zeros(shape=(hlayer2,1))
    rcb1 = np.zeros(shape=(hlayer1,1))
    summatrixcost = 0
    flatchoices = ['roll','btile', 'gtile', 'ytile', 'otile', 'wtile',\
                  'wblue', 'wgreen','wyellow','worange','wwhite',\
                 'lblue', 'lgreen','lyellow','lorange','lwhite']
    '''learniter is the batch size for training'''
    learniter = 20
    for i in range(learniter):
        choseninput = random.randint(0,15)
        if choseninput == 0:
            randinfo = choosescenario(rollranswer,90000,'roll')
        elif choseninput == 1:
            randinfo = choosescenario(btileranswer,15500,'btile')
        elif choseninput == 2:
            randinfo = choosescenario(gtileranswer,15500,'gtile')
        elif choseninput == 3:
            randinfo = choosescenario(ytileranswer,15500,'ytile')
        elif choseninput == 4:
            randinfo = choosescenario(otileranswer,15500,'otile')
        elif choseninput == 5:
            randinfo = choosescenario(wtileranswer,15500,'wtile')
        elif choseninput < 11:
            randinfo = choosescenario(winnerranswer,350,flatchoices[choseninput])
        else:
            randinfo = choosescenario(loserranswer,780,flatchoices[choseninput])
        
        inputm = np.matrix(randinfo)
        inputmatrix = np.transpose(inputm)
        
        activation1 = newactivation(wandb["wmat1"],wandb["bmat1"],inputmatrix)
        
        activation2 = newactivation(wandb["wmat2"],wandb["bmat2"],activation1)
        
        activation3 = newactivation(wandb["wmat3"],wandb["bmat3"],activation2)
        
        activation4 = newactivation(wandb["wmat4"],wandb["bmat4"],activation3)
        
        '''Takes the Activations and backpropagates'''
        
        '''Creates zero matrix with the right answer as one'''
        choicematrixadj = np.zeros(shape=(16,1))
        choicematrix = choicematrixadj + .01
        choicematrix[choseninput] = [.99]
        '''Takes answers and subtracts 1 or 0 to find the cost derivative'''
        newitem = activation4 - choicematrix
        cmatrix = np.transpose(newitem)
        matrixcost = cmatrix * newitem
        '''Calcs the derivative of the sigmoid'''
        dsigmoid4 = np.multiply(activation4, 1 - activation4)
        '''Multiply the derivative of the sigmoid function by the cost by the previous layer neuron'''
        cdicttemp = np.multiply(dsigmoid4,newitem*2)
        cbias4 = cdicttemp
        cwmat4 = cdicttemp * np.transpose(activation3)
        '''Calculates the changeactivation for previous layer'''
        cact3 = np.transpose(wandb["wmat4"]) * cdicttemp
        
        dsigmoid3 = np.multiply(activation3,1-activation3)
        cdicttemp = np.multiply(dsigmoid3,cact3)
        cbias3 = cdicttemp
        cwmat3 = cdicttemp * np.transpose(activation2)
        cact2 = np.transpose(wandb["wmat3"]) * cdicttemp
        
        dsigmoid2 = np.multiply(activation2,1-activation2)
        cdicttemp = np.multiply(dsigmoid2,cact2)
        cbias2 = cdicttemp
        cwmat2 = cdicttemp * np.transpose(activation1)
        cact1 = np.transpose(wandb["wmat2"]) * cdicttemp
        
        dsigmoid1 = np.multiply(activation1,1-activation1)
        cdicttemp = np.multiply(dsigmoid1,cact1)
        cbias1 = cdicttemp
        cwmat1 = cdicttemp * inputm
        
        summatrixcost = matrixcost + summatrixcost
    
        rcw4 = rcw4 + cwmat4
        rcw3 = rcw3 + cwmat3
        rcw2 = rcw2 + cwmat2
        rcw1 = rcw1 + cwmat1
        
        rcb4 = rcb4 + cbias4
        rcb3 = rcb3 + cbias3
        rcb2 = rcb2 + cbias2
        rcb1 = rcb1 + cbias1
    
    adjustwb("wmat4",rcw4,learniter)
    adjustwb("wmat3",rcw3,learniter)
    adjustwb("wmat2",rcw2,learniter)
    adjustwb("wmat1",rcw1,learniter)
    adjustwb("bmat4",rcb4,learniter)
    adjustwb("bmat3",rcb3,learniter)
    adjustwb("bmat2",rcb2,learniter)
    adjustwb("bmat1",rcb1,learniter)
    learnitercost = summatrixcost/learniter
    return learnitercost

def adjustwb(weightorbias,adjustment,adjrunningcount):
    global stepsize
    global momentum
    wandb[weightorbias] = wandb[weightorbias] - (adjustment/adjrunningcount*stepsize)

'''Saves inputs to dictionary'''
def saveinputs(finalchoices,finalchoicescount,inputaction,inputaiinfo,actiondictionary):
    k = 0
    for i in finalchoices:
        j = finalchoicescount[k]
        if inputaction == i:
            actiondictionary["{}{}".format(inputaction,finalchoicescount[k])] = inputaiinfo
            flatchoicescount[k]  = j + 1
        k = k + 1

'''Takes the dictionaries from "saveinputs" and saves them to a file'''
def saveinputstofile(inputdictionaryname, savefilename):
    with open('{}randomdictionary2.json'.format(savefilename), 'w') as d:
        json.dump(inputdictionaryname, d)

global saverandomscheck
saverandomscheck = 0
'''Handles the random inputs and handles making the AI player 2 choices'''
def balanceinputs(action):
    global camellist
    global flatchoicescount
    global runtype
    global saverandomscheck
    global endrun
    aiblue5 = -1
    aiblue3 = -1
    aiblue2 = -1
    aigreen5 = -1
    aigreen3 = -1
    aigreen2 = -1
    aiyellow5 = -1
    aiyellow3 = -1
    aiyellow2 = -1
    aiorange5 = -1
    aiorange3 = -1
    aiorange2 = -1
    aiwhite5 = -1
    aiwhite3 = -1
    aiwhite2 = -1
        
    if blue.rollstatus == 'rolled':
        aiblue = 1
    else:
        aiblue = -1
    if green.rollstatus == 'rolled':
        aigreen = 1
    else:
        aigreen = -1
    if yellow.rollstatus == 'rolled':
        aiyellow = 1
    else:
        aiyellow = -1
    if orange.rollstatus == 'rolled':
        aiorange = 1
    else:
        aiorange = -1
    if white.rollstatus == 'rolled':
        aiwhite = 1
    else:
        aiwhite = -1
    
    if 'blue' in fivers.betcolors:
        aiblue5 = 1
    if 'blue' in threes.betcolors:
        aiblue3 = 1
    if 'blue' in twos.betcolors:
        aiblue2 = 1
    if 'green' in fivers.betcolors:
        aigreen5 = 1
    if 'green' in threes.betcolors:
        aigreen3 = 1
    if 'green' in twos.betcolors:
        aigreen2 = 1
    if 'yellow' in fivers.betcolors:
        aiyellow5 = 1
    if 'yellow' in threes.betcolors:
        aiyellow3 = 1
    if 'yellow' in twos.betcolors:
        aiyellow2 = 1
    if 'orange' in fivers.betcolors:
        aiorange5 = 1
    if 'orange' in threes.betcolors:
        aiorange3 = 1
    if 'orange' in twos.betcolors:
        aiorange2 = 1
    if 'white' in fivers.betcolors:
        aiwhite5 = 1
    if 'white' in threes.betcolors:
        aiwhite3 = 1
    if 'white' in twos.betcolors:
        aiwhite2 = 1
        
    if pturn.get() == "Player 1":
        if p1winner != '':
            winnertile = 1
        else:
            winnertile = -1
    elif p2winner != '':
        winnertile = 1
    else:
        winnertile = -1
    
    if pturn.get() == "Player 1":
        if p1loser != '':
            losertile = 1
        else:
            losertile = -1
    elif p2loser != '':
        losertile = 1
    else:
        losertile = -1
    
    '''aiinfo are the inputs normalized'''
    aiinfo = [(aiblue+1)/2, (aiblue5+1)/2, (aiblue3+1)/2, (aiblue2+1)/2, (blue.space-1)/17,\
              (len(blue.cabove))/4,\
              (aigreen+1)/2, (aigreen5+1)/2, (aigreen3+1)/2, (aigreen2+1)/2, (green.space-1)/17,\
              (len(green.cabove))/4,\
              (aiyellow+1)/2, (aiyellow5+1)/2, (aiyellow3+1)/2, (aiyellow2+1)/2, (yellow.space-1)/17,\
              (len(yellow.cabove))/4,\
              (aiorange+1)/2, (aiorange5+1)/2, (aiorange3+1)/2, (aiorange2+1)/2, (orange.space-1)/17,\
              (len(orange.cabove))/4,\
              (aiwhite+1)/2, (aiwhite5+1)/2, (aiwhite3+1)/2, (aiwhite2+1)/2, (white.space-1)/17,\
              (len(white.cabove))/4,\
              (winnertile+1)/2, (losertile+1)/2]
    
    flatchoices = ['roll','btile', 'gtile', 'ytile', 'otile', 'wtile', 'wblue', 'wgreen','wyellow','worange','wwhite',\
                 'lblue', 'lgreen','lyellow','lorange','lwhite']
    
    decision = flatchoices.index(action)
    '''Takes the input during "findinputs" and saves it off. The minsavepoint is the minimum number of examples for the least occuring example.'''
    minsavepoint = 351
    if runtype != 0:
        if min(flatchoicescount) < minsavepoint:
            if decision < 6:
                if action == 'roll' and flatchoicescount[0] < 150000:
                    saveinputs(flatchoices,flatchoicescount,action,aiinfo,rolldictionary)
                elif action == 'btile':
                    saveinputs(flatchoices,flatchoicescount,action,aiinfo,btiledictionary)
                elif action == 'gtile':
                    saveinputs(flatchoices,flatchoicescount,action,aiinfo,gtiledictionary)
                elif action == 'ytile':
                    saveinputs(flatchoices,flatchoicescount,action,aiinfo,ytiledictionary)
                elif action == 'otile':
                    saveinputs(flatchoices,flatchoicescount,action,aiinfo,otiledictionary)
                else:
                    saveinputs(flatchoices,flatchoicescount,action,aiinfo,wtiledictionary)
            elif decision < 11:
                saveinputs(flatchoices,flatchoicescount,action,aiinfo, winnerdictionary)
            else:
                saveinputs(flatchoices,flatchoicescount,action,aiinfo, loserdictionary)
        elif saverandomscheck == 0:
            saveinputstofile(rolldictionary, 'roll')
            saveinputstofile(btiledictionary, 'btile')
            saveinputstofile(gtiledictionary, 'gtile')
            saveinputstofile(ytiledictionary, 'ytile')
            saveinputstofile(otiledictionary, 'otile')
            saveinputstofile(wtiledictionary, 'wtile')
            saveinputstofile(winnerdictionary, 'winner')
            saveinputstofile(loserdictionary, 'loser')
            saverandomscheck = 1
            print("PRINTING FLATCHOICESCOUNT")
            print(flatchoicescount)
            print("")
            print("All Done")
            '''Makes it so the program stops running once files are saved'''
            run = endrun + 1
        
    '''Removes unavailable choices for the AI'''
    if runtype == 0 and pturn.get() == "Player 2":
        aichoices = np.ones((16,1))
        if aiinfo[3] == 0:
            aichoices[1] = 0
        if aiinfo[9] == 0:
            aichoices[2] = 0
        if aiinfo[15] == 0:
            aichoices[3] = 0
        if aiinfo[21] == 0:
            aichoices[4] = 0
        if aiinfo[27] == 0:
            aichoices[5] = 0
        '''Checks if it is Player1's turn'''
        if winnertile == 1:
            aichoices[6] = 0
            aichoices[7] = 0
            aichoices[8] = 0
            aichoices[9] = 0
            aichoices[10] = 0
        if losertile == 1:
            aichoices[11] = 0
            aichoices[12] = 0
            aichoices[13] = 0
            aichoices[14] = 0
            aichoices[15] = 0
        newneuronmatrix(aiinfo, action, decision, aichoices)

'''AI choice'''
def aimessagechoice(activationmsg,activationchoice):
    aimsgcon.set(activationmsg)
    aimsgchoice.set(activationchoice)

'''This runs through a number of sceanrios to find the probabilistic right choice to have the nn train on'''
def tilepredict(tileprecamels,tpreblue,tpregreen,tpreyellow,tpreorange,tprewhite):
    global runtype
    if blue.space == 0:
        needstart = ['start','']
        return needstart
    tileplist = []
    tilepdictionary = {}
    tilepredictcolors = ['blue','green','yellow','orange','white']
    wlorder = [tpreblue, tpregreen, tpreyellow, tpreorange, tprewhite]
    wlorder.sort(key=lambda x: (x.space,-len(x.cabove)))
    loserleader = wlorder[0].space
    almostloser = wlorder[1].space
    winnerleader = wlorder[4].space
    almostleader = wlorder[3].space
    if winnerleader > 10:
        if winnerleader - almostleader > 3:
            if pturn.get() == 'Player 1':
                if p1winner == '':
                    camelthatwon = wlorder[4].color
                    thewinner = ['owinner','one',camelthatwon]
                    if runtype != 0:
                        return thewinner
                    else:
                        print(camelthatwon)
            else:
                if p2winner == '':
                    camelthatwon = wlorder[4].color
                    thewinner = ['owinner','two',camelthatwon]
                    if runtype != 0:
                        return thewinner
                    else:
                        print(camelthatwon)
    elif winnerleader > 15:
        if winnerleader - almostleader > 2:
            if pturn.get() == 'Player 1':
                if p1winner == '':
                    camelthatwon = wlorder[4].color
                    thewinner = ['owinner','one',camelthatwon]
                    if runtype != 0:
                        return thewinner
                    else:
                        print(camelthatwon)
            else:
                if p2winner == '':
                    camelthatwon = wlorder[4].color
                    thewinner = ['owinner','two',camelthatwon]
                    if runtype != 0:
                        return thewinner
                    else:
                        print(camelthatwon)
    if almostloser > loserleader + 3:
        if pturn.get() == 'Player 1':
            if p1loser == '':
                camelthatlost = wlorder[0].color
                theloser = ['oloser','one',camelthatlost]
                if runtype != 0:
                    return theloser
                else:
                    print(camelthatlost)
        else:
            if p2loser == '':
                camelthatlost = wlorder[0].color
                theloser = ['oloser','two',camelthatlost]
                if runtype != 0:
                    return theloser
                else:
                    print(camelthatlost)
    attempts = 25
    for y in range(attempts):
        tilepcamels = copy.deepcopy(tileprecamels)
        tilepblue = copy.deepcopy(tpreblue)
        tilepgreen = copy.deepcopy(tpregreen)
        tilepyellow = copy.deepcopy(tpreyellow)
        tileporange = copy.deepcopy(tpreorange)
        tilepwhite = copy.deepcopy(tprewhite)
        tileprefcamellist = [tilepblue, tilepgreen, tilepyellow, tileporange, tilepwhite]
        tilepredictrepeat = len(tilepcamels)
        
        camelsremain = []
        camels = []
        for c in tileprefcamellist:
            if c.rollstatus == "unrolled":
                camelsremain.append(c.color)
                camels.append(c)
                
        tilepredictrepeat = len(camels)
                
        for x in range(tilepredictrepeat):
            choice = random.choice(camels)
            camels.remove(choice)
            camelsremain.remove(choice.color)
            choice.change_rollstatus("rolled")
            colorchoice = choice.color
            spacechoice = choice.space
            cunderchoice = choice.cunder
            cabovechoice = choice.cabove
            roll = randint(1,3)
            
            finalspace = (choice.space + roll)
            
            '''Creates a list of the camels that will be placed underneath the moving camels'''
            tempunderlist = []
            tempsingleabove = [colorchoice]
            for c in tileprefcamellist:
                if c != choice:
                    if c.color in cunderchoice:
                        c.change_above([x for x in c.cabove if x not in cabovechoice])
                        c.change_above([x for x in c.cabove if x not in tempsingleabove])
                    elif c.space == finalspace:
                        c.cabove.append(choice.color)
                        c.cabove.extend(cabovechoice)
                        tempunderlist.append(c.color)
                    elif c.color in cabovechoice:
                        c.change_under([x for x in c.cunder if x not in cunderchoice])
                        c.change_space(c.space + roll)
            choice.change_space(roll + choice.space)
                        
            choice.change_under(tempunderlist)
            for c in tileprefcamellist:
                if c.color in cabovechoice:
                    c.cunder.extend(tempunderlist)
            
        spacelist = [tilepblue.space, tilepgreen.space, tilepyellow.space, tileporange.space, tilepwhite.space]
        spacelist.sort()
        leadspace = spacelist[-1]
        
        for c in tileprefcamellist:
            if c.space == leadspace and c.cabove == []:
                leadcamel = c.color
                tileplist.append(leadcamel)
    for g in tilepredictcolors:
        problead = tileplist.count(g)/attempts
        if g in fivers.betcolors:
            predictvalue = problead * 5 - (1-problead)
            tilepdictionary[g] = [predictvalue,'five',g]
        elif g in threes.betcolors:
            predictvalue = problead * 3 - (1-problead)
            tilepdictionary[g] = [predictvalue,'three',g]
        elif g in twos.betcolors:
            predictvalue = problead * 2 - (1-problead)
            tilepdictionary[g] = [predictvalue,'two',g]
    tprelist = tilepdictionary[max(tilepdictionary.items(), key = operator.itemgetter(1))[0]]
    if tprelist[0] > 1.2:
        if tprelist[1] == 'five':
            tiletobet = tprelist[2]
            bettingtile = ['bettile','five',tiletobet]
            if runtype != 0:
                return bettingtile
            else:
                print(tiletobet)
        elif tprelist[1] == 'three':
            tiletobet = tprelist[2]
            bettingtile = ['bettile','three',tiletobet]
            if runtype != 0:
                return bettingtile
            else:
                print(tiletobet)
        elif tprelist[1] == 'two':
            tiletobet = tprelist[2]
            bettingtile = ['bettile','two',tiletobet]
            if runtype != 0:
                return bettingtile
            else:
                print(tiletobet)
    else:
        rolling = ['roll','']
        if runtype != 0:
            return rolling
        else:
            print("roll")

'''Resets all values to beginning values'''
def restart():
    global camels
    global p1score
    global p2score
    global camelsleft
    global p1winner
    global p2winner
    global p1loser
    global p2loser
    global p1wmod
    global p2wmod
    global p1lmod
    global p2lmod
    reset()
    pturn.set('Player 1')
    gspace.set(0)
    bspace.set(0)
    yspace.set(0)
    ospace.set(0)
    wspace.set(0)
    gcb.configure(text = str(''))
    bcb.configure(text = str(''))
    ycb.configure(text = str(''))
    ocb.configure(text = str(''))
    wcb.configure(text = str(''))
    green.change_space(0)
    blue.change_space(0)
    yellow.change_space(0)
    orange.change_space(0)
    white.change_space(0)
    green.change_under([])
    blue.change_under([])
    yellow.change_under([])
    orange.change_under([])
    white.change_under([])
    green.change_above([])
    blue.change_above([])
    yellow.change_above([])
    orange.change_above([])
    white.change_above([])
    camels = [blue,green,yellow,orange,white]
    p1score = 3
    p2score = 3
    playeronescore.configure(text = str(p1score))
    playertwoscore.configure(text = str(p2score))
    camelsremain = ['blue','green','yellow','orange','white']
    cleft.configure(text = str(camelsremain))
    player1owinner.configure(text = str(''))
    player2owinner.configure(text = str(''))
    player1oloser.configure(text = str(''))
    player2oloser.configure(text = str(''))
    p1winner = ''
    p2winner = ''
    p1loser = ''
    p2loser = ''
    p1wmod = 0
    p2wmod = 0
    p1lmod = 0
    p2lmod = 0
    aimessagechoice("","")
    camelcolor.set("")
    dier.set("")

'''Resets player hands and refills camels left'''
def reset():
    global camellist
    global p1score
    global p2score
    fivers.fulltiles()
    fivetile['values'] = (fivers.betcolors)
    threes.fulltiles()
    threetile['values'] = (threes.betcolors)
    twos.fulltiles()
    twotile['values'] = (twos.betcolors)        
    p15.clear()
    player15.configure(text = str(p15))
    p25.clear()
    player25.configure(text = str(p25))
    p13.clear()
    player13.configure(text = str(p13))
    p23.clear()
    player23.configure(text = str(p23))
    p12.clear()
    player12.configure(text = str(p12))
    p22.clear()
    player22.configure(text = str(p22))
    blue.change_rollstatus("unrolled")
    for c in camellist:
        c.change_rollstatus("unrolled")

'''Starts the game. Rolls each dice once and puts camels in starting postions'''
def start():
    global camels
    global camellist
    global p1score
    global p2score
    
    for x in range(5):
        choice = random.choice(camels)
        camels.remove(choice)
        roll = randint(1,3)
        colorchoice = choice.color
        
        for c in camellist:
            if c.space == roll:
                c.cabove.append(choice.color)
                choice.cunder.append(c.color)
                
        choice.change_space(roll)
    
    spacelist = [bspace, gspace, yspace, ospace, wspace]
    spacelistlabel = [bcb, gcb, ycb, ocb, wcb]
    camellist = [blue,green,yellow,orange,white]
    for c, s, l in zip(camellist,spacelist,spacelistlabel):
        s.set(c.space)
        l.configure(text = c.cunder)
        c.change_rollstatus("unrolled")
    if runtype == 0:
        root.mainloop()

'''Function for rolling the dice'''
def rolldice():
    global camellist
    global p1score
    global p2score
    global spacelist
    global spacelistlabel
    global runtype
    global run
    
    camels = camelclassleft()
    camelsremain = camelcolorleft()
    
    if runtype == 1:
        balanceinputs('roll')
    
    choice = random.choice(camels)
    camels.remove(choice)
    camelsremain.remove(choice.color)
    choice.change_rollstatus("rolled")
    colorchoice = choice.color
    spacechoice = choice.space
    cunderchoice = choice.cunder
    cabovechoice = choice.cabove
    roll = randint(1,3)
    
    finalspace = (choice.space + roll)
    
    '''Creates a list of the camels that will be placed underneath the moving camels'''
    tempunderlist = []
    tempsingleabove = [colorchoice]
    for c in camellist:
        if c != choice:
            if c.color in cunderchoice:
                c.change_above([x for x in c.cabove if x not in cabovechoice])
                c.change_above([x for x in c.cabove if x not in tempsingleabove])
            elif c.space == finalspace:
                c.cabove.append(choice.color)
                c.cabove.extend(cabovechoice)
                tempunderlist.append(c.color)
            elif c.color in cabovechoice:
                c.change_under([x for x in c.cunder if x not in cunderchoice])
                c.change_space(c.space + roll)
    choice.change_space(roll + choice.space)
                
    '''Changes the chosen camel's underneath camels to new under list'''
    choice.change_under(tempunderlist)
    for c in camellist:
        if c.color in cabovechoice:
            c.cunder.extend(tempunderlist)
            
    '''Prints the die roll and camel color to othe gui'''        
    dier.set(roll)
    camelcolor.set(colorchoice)
    
    spacelist = [bspace, gspace, yspace, ospace, wspace]
    spacelistlabel = [bcb, gcb, ycb, ocb, wcb]
    camellist = [blue,green,yellow,orange,white]
    for c, s, l in zip(camellist,spacelist,spacelistlabel):
        s.set(c.space)
        l.configure(text = c.cunder)
    
    '''Changes the player turn'''    
    if pturn.get() == 'Player 1':
        playerscoring(1,1,p1score)
        pturn.set('Player 2')
    else:
        playerscoring(2,1,p2score)
        pturn.set('Player 1')
        
    spacelist = [blue.space,green.space,yellow.space,orange.space,white.space]
    spacelist.sort()
    leadspace = spacelist[-1]
    secondspace = spacelist[-2]
    lastspace = spacelist[0]
    '''Checks for the End of a Round and finds position of camels'''
    if 'unrolled' not in [blue.rollstatus,green.rollstatus,yellow.rollstatus,orange.rollstatus,white.rollstatus] or leadspace > 16:
        for c in camellist:
            if c.space == leadspace:
                if c.cabove == []:
                    leadcamel = c.color
                elif len(c.cabove) == 1:
                    secondcamel = c.color 
            elif c.space == secondspace and c.cabove ==[]:
                secondcamel = c.color
            if c.space == lastspace and c.cunder == []:
                lastcamel = c.color
        ''' End of Round Scoring'''
        '''Gives points for second place camels'''
        ponescore=p1score+((p15.count(secondcamel)+p13.count(secondcamel)+p12.count(secondcamel))*2)
        p1score = ponescore
        ptwoscore=p2score+((p25.count(secondcamel)+p23.count(secondcamel)+p22.count(secondcamel))*2)
        p2score = ptwoscore
        '''Gives points for the betting tiles (1st place)'''    
        if leadcamel in p15:
            playerscoring(1, 6-len(p15), p1score)
        if leadcamel in p13:
            playerscoring(1, 4-len(p13), p1score)
        if leadcamel in p12:
            playerscoring(1, 3-len(p12), p1score)
        if leadcamel in p25:
            playerscoring(2, 6-len(p25), p2score)
        if leadcamel in p23:
            playerscoring(2, 4-len(p23), p2score)
        if leadcamel in p22:
            playerscoring(2, 3-len(p22), p2score)
        '''Places the tiles back'''
        reset()
        '''End of Game'''
        if leadspace > 16:
            '''Gives points for overall winnner and overall loser betting tiles'''
            if p1winner != '':
                if leadcamel == p1winner:
                    playerscoring(1, 8 - p1wmod, p1score)
                else:
                    playerscoring(1, -1, p1score)
            if p1loser != '':
                if lastcamel == p1loser:
                    playerscoring(1, 8 - p1lmod, p1score)
                else:
                    playerscoring(1, -1, p1score)
            if p2winner != '':
                if leadcamel == p2winner:
                    playerscoring(2, 8 - p2wmod, p2score)
                else:
                    playerscoring(2, -1, p2score)
            if p2loser != '':
                if lastcamel == p2loser:
                    playerscoring(2, 8 - p2lmod, p2score)
                else:
                    playerscoring(2, -1, p2score)
            if p1score > p2score:
                winner = ("Player 1 wins {n} to {s}".format(n=p1score,s=p2score))
            else:
                winner = ("Player 2 wins {n} to {s}".format(n=p2score,s=p1score))
            if runtype == 1:
                run = run + 1
                if run%(gamecheck/10) == 0:
                    print(run)
            if runtype == 0:
                messagebox.showinfo("Final Score",winner)
            restart()
        else:
            camelsremain = ['blue','green','yellow','orange','white']
    cleft.configure(text = str(camelsremain))
    if runtype == 0:
        balanceinputs('roll')
        root.mainloop()

'''Handles bets for the round to round betting'''
def bettile(remaintilenumber, tilenum, p1, player1, p2, player2):
    global runtype
    chosencamel = tilenum.get()
    tilechoice = chosencamel[0] + 'tile'
    if runtype == 1:
        balanceinputs(tilechoice)
    if pturn.get() == 'Player 1':
        p1.append(chosencamel)
        remaintilenumber.removebettile(chosencamel)
        player1.configure(text = str(p1))
        tilenum['values']= (remaintilenumber.betcolors)
        pturn.set('Player 2')
    else:
        p2.append(chosencamel)
        remaintilenumber.removebettile(chosencamel)
        player2.configure(text = str(p2))
        tilenum['values']= (remaintilenumber.betcolors)
        pturn.set('Player 1')
    if remaintilenumber:
        tilenum.current(0)
    if runtype == 0:
        balanceinputs(tilechoice)
        root.mainloop()
    
'''Handles bets for overall winner of the race'''   
def rwinner(overallcamelwinner):
    global camels
    global p1winner
    global p2winner
    global p1wmod
    global p2wmod
    global runtype
    selectedcamel = overallcamelwinner.get()
    tilechoice = 'w' + selectedcamel
    if runtype == 1:
        balanceinputs(tilechoice)
    if pturn.get() == 'Player 1':
        if p1winner == '':
            player1owinner.configure(text = str(selectedcamel))
            p1winner = selectedcamel
            pturn.set('Player 2')
            owinner['values']=(camelwinner)
            if p2winner == p1winner:
                p1wmod = 3
    else:
        if p2winner == '':
            player2owinner.configure(text = str(selectedcamel))
            p2winner = selectedcamel
            pturn.set('Player 1')
            owinner['values']=(camelwinner)
            if p1winner == p2winner:
                p2wmod = 3
    if runtype == 0:
        balanceinputs(tilechoice)
        root.mainloop()

'''Handles bets for overall loser of the race'''       
def rloser(overallcamelloser):
    global camels
    global p1loser
    global p2loser
    global p1lmod
    global p2lmod
    global runtype
    selectedcamel = overallcamelloser.get()
    tilechoice = 'l' + selectedcamel
    if runtype == 1:
        balanceinputs(tilechoice)
    if pturn.get() == 'Player 1':
        if p1loser == '':
            player1oloser.configure(text = str(selectedcamel))
            p1loser = selectedcamel
            pturn.set('Player 2')
            oloser['values']=(camelloser)
            if p2loser != '':
                p1lmod = 3
    else:
        if p2loser == '':
            player2oloser.configure(text = str(selectedcamel))
            p2loser = selectedcamel
            pturn.set('Player 1')
            oloser['values']=(camelloser)
            if p1loser != '':
                p2lmod = 3
    if runtype == 0:
        balanceinputs(tilechoice)
        root.mainloop()

'''deeplearn trains off the inputs from "find inputs" '''
def deeplearn():
    global camellist
    global run
    global runtype
    print("Deep Learn running")
    run = 0
    runtype = 2
    fmavg = 0
    lastgcheckavg = 0
    for x in range(985000500):
        if run < (endrun+1):
            avgmcost = getranddictionary()
            fmavg = fmavg + avgmcost
            lastgcheckavg = lastgcheckavg  + avgmcost
            if run%gamecheck == 0 and run > 0:
                print(fmavg/run)
                formatlastgcheckavg = lastgcheckavg[0].item()
                print("Avg cost since last gamecheck is {}".format(formatlastgcheckavg/gamecheck))
                lastgcheckavg = 0
            run = run + 1
            if run%gamecheck == 0:
                print("Run {}".format(run))
        else:
            with open('CamelCupNNweightsbiasv3.pickle', 'wb') as handle:
                    pickle.dump(wandb, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print("")
            end_time = time.monotonic()
            print(end_time - start_time)
            print('done')
            break

'''findinputs ensures that a wide range of inputs are found to feed into the neural network.'''
def findinputs():
    global camellist
    global fivetile
    global threetile
    global twotile
    global oloser
    global owinner
    global run
    global runtype
    runtype = 1
    run = 0
    for x in range(985000500):
        if run < (endrun+1):
            nextchoice = tilepredict(camellist,blue,green,yellow,orange,white)
            if nextchoice[0] == 'start':
                start()
            elif nextchoice[0] == 'roll':
                rolldice()
            elif nextchoice[0] == 'owinner':
                owinner.set(nextchoice[2])
                rwinner(owinner)
            elif nextchoice[0] == 'oloser':
                oloser.set(nextchoice[2])
                rloser(oloser)
            elif nextchoice[0] == 'bettile':
                if nextchoice[1] == 'five':
                    fivetile.set(nextchoice[2])
                    bettile(fivers, fivetile, p15, player15, p25, player25)
                elif nextchoice[1] == 'three':
                    threetile.set(nextchoice[2])
                    bettile(threes, threetile, p13, player13, p23, player23)
                elif nextchoice[1] == 'two':
                    twotile.set(nextchoice[2])
                    bettile(twos, twotile, p12, player12, p22, player22)
        else:
            print('done')
            break        

'''Start Button'''
startbtn = Button(root,text="Start", command=start,width=22)
startbtn.grid(column=0,row=0)

'''Roll Dice Command'''
rollbtn = Button(root, text="Roll", command=rolldice,width=22) 
rollbtn.grid(column=0, row=1)

'''Deep Learn'''
dlearnbtn = Button(root,text="Deep Learn",command=deeplearn,width=15)
dlearnbtn.grid(column=9,row=1)

'''Find Inputs'''
findinputsbtn = Button(root,text="Find Inputs",command=findinputs,width=15)
findinputsbtn.grid(column=9,row=2)

'''Predicts Tile using probiblity during a game'''
pchoicebtn = Button(root,text="Predict Choice",command= lambda: tilepredict(camellist,blue,green,yellow,orange,white),width=15)
pchoicebtn.grid(column=9,row=0)

'''Buttons for bets on the round'''
tile5btn = Button(root, text="5 point", command= lambda: bettile(fivers, fivetile, p15, player15, p25, player25),width=22)
tile5btn.grid(column=0,row=2)
tile3btn = Button(root, text="3 point", command= lambda: bettile(threes, threetile, p13, player13, p23, player23),width=22)
tile3btn.grid(column=0,row=4)
tile2btn = Button(root, text="2 point", command= lambda: bettile(twos, twotile, p12, player12, p22, player22),width=22)
tile2btn.grid(column=0,row=6)

'''Buttons for race winner/loser'''
racewinner = Button(root, text="Overall Winner", command= lambda: rwinner(owinner),width=22)
racewinner.grid(column=0,row=8)
raceloser = Button(root, text="Overall Loser", command= lambda: rloser(oloser),width=22)
raceloser.grid(column=0,row=10)
          
'''Button for Restart'''
restartbtn = Button(root, text="Restart", command=restart,width=22)
restartbtn.grid(column=0,row=12)

'''AI Header'''
aiheader = Message(root, text="AI Decision:",width=100)
aiheader.grid(column=5, row=9, columnspan=4)

'''AI confidence message'''
global aimsgcon
aimsgcon = StringVar()
aimsgcon.set("")
aiconfidence = Message(root, textvariable=aimsgcon,width=400)
aiconfidence.grid(column=5, row=11, columnspan=4)

'''AI selection message'''
global aimsgchoice
aimsgchoice = StringVar()
aimsgchoice.set("")
aiselection = Message(root, textvariable=aimsgchoice,width=400)
aiselection.grid(column=5, row=10, columnspan=4)

'''Formatting for printing to the GUI'''
root.grid_columnconfigure(1, minsize=75)
root.grid_columnconfigure(2, minsize=75)
root.grid_columnconfigure(3, minsize=150)
root.grid_columnconfigure(4, minsize=75)
root.grid_columnconfigure(6, minsize=120)
root.grid_columnconfigure(7, minsize=120)
root.mainloop()