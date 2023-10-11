#==============================
# Load The Libraries===========
#==============================
from __future__ import division #so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, misc, logging, gui, monitors
from numpy import *
import os #handy system and path functions
import math
from PIL import Image # Get the size(demension) of an image

#======================================
# Default Hand Made Function===========
#======================================
def returnNumber(inputNumber, returnUnit):
    return inputNumber - (floor(inputNumber/returnUnit)*returnUnit)
def isOdd(inputNumber):
    return ceil(float(inputNumber)/2-floor(float(inputNumber)/2))
    

#======================
# Parameters===========
#======================

# experimental conditions
attentionToFirstTargetList = [0, 1];
numberOfSeondDistractorIntervalList = [1, 3, 5];
soaList = [0.05, 0.1, 0.2];

# instructions
instructionList=range(12); # number of instructions
instructionSizeX=[30, 10]; # width of instructions

# Presenting Duration
durationForFixation = 1.5
durationForLetters = 0.1

# Number Of Stimuli
nCharacterTargets = 2;
nNumberDistractors = [7, 3, 6];

letterSize = 100;

# Fixation Cross
fixationCrossLength = 100;
fixationCrossWidth = 10;
fixationCrossColor = [-1, -1, -1];

# Number Of Repetitoin
nBlocks = 5;

# Stimuli Pool
characterPool = [['A','a'], ['B','b'], ['C','c'], ['D','d'], ['E','e'], ['F','f'], ['G','g'], ['H','h'], ['I','i'], ['J','j'], ['K','k'], ['L','l'], ['M','m'], ['N','n'], ['O','o'], ['P','p'], ['Q','q'], ['R','r'], ['S','s'], ['T','t'], ['U','u'], ['V','v'], ['W','w'], ['X','x'], ['Y','y'], ['Z','z']];
characterPool = [['A','a'], ['B','b'], ['C','c'], ['D','d'], ['E','e'], ['F','f'], ['G','g'], ['H','h'], ['J','j'], ['K','k'], ['L','l'], ['M','m'], ['N','n'], ['P','p'], ['Q','q'], ['R','r'], ['S','s'], ['T','t'], ['U','u'], ['V','v'], ['W','w'], ['X','x'], ['Y','y'], ['Z','z']];
numberpool = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
numberpool = ['2', '3', '4', '5', '6', '7', '8', '9']

#===============================================
# Setup For Pop Up Window=======================
#===============================================
expName='Second_Class_Practice' # practice on only vertical gratings
expInfo={'group':'00', 'participant':'00'}
dlg=gui.DlgFromDict(dictionary=expInfo,title=expName)
if dlg.OK==False: core.quit() #user pressed cancel
expInfo['date']=data.getDateStr()#add a simple timestamp
expInfo['expName']=expName

if not os.path.isdir('data'):
    os.makedirs('data') #if this fails (e.g. permissions) we will get error
fileName='data' + os.path.sep + '%s_%s_%s_%s' %(expName, expInfo['group'], expInfo['participant'], expInfo['date'])

groupIdx = int(expInfo['group']);
sbjIdx = int(expInfo['participant']);

# ====================================================================================================================================================================
# open text file for writing data==================================================================================================================================================
# ====================================================================================================================================================================
dataFile = open(fileName+'.txt', 'w')
dataFile.write('group\t' 'sbj\t' 'serial\t' 'BlockIdx\t' 'TrialIdx\t' 'AttentionToFirstTarget\t' 'NumberOfSecondDistractorInterval\t' 'SOAList\t' 'NumberOfFirstDistractorInterval\t' 'NumberOfThirdDistractorInterval\t' 'FirstTarget\t' 'SecondTarget\t' 'ResponseToFirstTarget\t' 'ResponseToSecondTarget\t' 'CorrectOrNotInFirst\t' 'CorrectOrNotSeond\t' 'ResponseTimeToFirst\t' 'ResponseTimeToSecond\n')

#====================================================================
# Experimental Design================================================
#====================================================================
expTrials = []; thisSerial=0;
for thisBlock in range(nBlocks):
    thisTrial=0; blockTrials=[];
    for thisAttentionToFirstTarget in attentionToFirstTargetList:
        for thisNumberOfSeondDistractorInterval in numberOfSeondDistractorIntervalList:
            for thisSoa in soaList:
                thisSerial+=1; thisTrial+=1;
                trial = [groupIdx] + [sbjIdx] + [thisSerial+1] + [thisBlock+1] + [thisTrial+1] + [thisAttentionToFirstTarget] + [thisNumberOfSeondDistractorInterval] + [thisSoa]
                blockTrials.append(trial)
    random.seed()
    random.shuffle(blockTrials)
    expTrials.append(blockTrials)

groupIdx = 0
sbjIdx = 1
serialLoc = 2
blockLoc = 3
trialLoc = 4
attentionToFirstTargetLoc = 5
numberOfSeondDistractorIntervalLoc = 6
soaLoc = 7

nTotalTrials=len(attentionToFirstTargetList)*len(numberOfSeondDistractorIntervalList)*len(soaList);

serialIdx=0
for thisBlock in range(nBlocks):
    trialIdx=0
    for thisAttentionToFirstTarget in range(len(attentionToFirstTargetList)):
        for thisNumberOfSeondDistractorInterval in range(len(numberOfSeondDistractorIntervalList)):
            for thisSoa in range(len(soaList)):
                serialIdx+=1
                trialIdx+=1
                expTrials[thisBlock][trialIdx-1][serialLoc]=serialIdx
                expTrials[thisBlock][trialIdx-1][trialLoc]=trialIdx
    
#====================================================================
# Get Monitor Information============================================
#====================================================================
whichScreen = 2;
whichScreen = 0;
backgroundColor = [0, 0, 0];
win = visual.Window(screen = whichScreen, color = backgroundColor, fullscr = True, monitor='testMonitor', units='deg')
globalClock = core.Clock()
#win.setMouseVisible(False)

#=======================
# Stimuli Ready=========
#=======================

#============================
# Text Stimuli Ready=========
#============================


#==============================
# Fixation Cross Ready=========
#==============================
fixationCrossVert = [[0, fixationCrossLength/2], [0, 0], [fixationCrossLength/2, 0], [0, 0], [0, -fixationCrossLength/2], [0, 0], [-fixationCrossLength/2, 0]]
fixationCross = visual.ShapeStim(win, vertices=fixationCrossVert, closeShape=False, lineWidth=fixationCrossWidth, lineColor=fixationCrossColor, units='pix', fillColorSpace='rgb')

#==================================
# Instruction Images Ready=========
#==================================
instructions=[]; instructionSizes=[];
for thisInstr in range(len(instructionList)):
    instructionName = os.getcwd() + '/instruction/instruction' + str(thisInstr) + '.png'
    img = Image.open(instructionName)
    instructionSizes.append(img.size)
    thisInstructions = visual.ImageStim(win, image=instructionName, mask = 'none',
                size=[5,5],#will be the size of the original image in pixels
                units='deg', interpolate=True,
                autoLog=False)
    instructions.append(thisInstructions)

#=============================================
# Simple Rectagnular Background===============
#=============================================
backgroundRectVert = [[-win.size[0]/2, -win.size[1]/2], [-win.size[0]/2, +win.size[1]/2], [+win.size[0]/2, +win.size[1]/2], [+win.size[0]/2, -win.size[1]/2]]
backgroundRect = visual.ShapeStim(win, vertices=backgroundRectVert, lineWidth=0, fillColor=backgroundColor, units='pix', fillColorSpace='rgb')

textStim=visual.TextStim(win,
                    text='defualt, you can change the text by code text.text',
                    height=letterSize, pos=[0,0], color=[-1,-1,-1], font='Arial', colorSpace='rgb', ori=0, wrapWidth=None, opacity=1, depth=0.0, units='pix')

#===============================================
# Draw First Instruction Before Experiment======
#===============================================
numberOfInstruction=1
instructions[numberOfInstruction].size=[instructionSizeX[0], instructionSizeX[0]*(instructionSizes[numberOfInstruction][1]/instructionSizes[numberOfInstruction][0])]
instructions[numberOfInstruction].draw()
win.flip()
event.waitKeys(keyList = ['space'])
event.clearEvents()
#=========================================================================================================================================================================================================================================
#=========================================================================================================================================================================================================================================
# Experiment Starts!====================================================s==================================================================================================================================================================
#=========================================================================================================================================================================================================================================
#=========================================================================================================================================================================================================================================
for thisBlock in range(nBlocks):
    for thisTrial in range(nTotalTrials):
        #==================================================================
        # adjust parameters according to experimental condtions============
        #==================================================================
        ignoreOrNot = expTrials[thisBlock][thisTrial][attentionToFirstTargetLoc] # ignore first target or not
#        print ignoreOrNot
        nNumberDistractors[1] = expTrials[thisBlock][thisTrial][numberOfSeondDistractorIntervalLoc] # Number of Lag
        durationForLetters = expTrials[thisBlock][thisTrial][soaLoc] # SOA
        
        #===================================================
        # Draw Experimental Instruction Between Trials======
        #===================================================
        if ignoreOrNot in [0]:
            numberOfInstruction=2
        elif ignoreOrNot in [1]:
            numberOfInstruction=3
        instructions[numberOfInstruction].size=[instructionSizeX[0], instructionSizeX[0]*(instructionSizes[numberOfInstruction][1]/instructionSizes[numberOfInstruction][0])]
        instructions[numberOfInstruction].draw()
        win.flip()
        event.waitKeys(keyList = ['space'])
        event.clearEvents()
        
        #==========================
        # Draw Fixation Cross======
        #==========================
        fixationCross.draw()
        win.flip()
        
        #=========================================================================
        # Ready for Exerimental Conditions During Presenting Fixation Cross=======
        #=========================================================================
        itiTargetOnset = globalClock.getTime()
        drawnT = False
        while globalClock.getTime() - itiTargetOnset <= durationForFixation: # duration for presenting instruction
            if drawnT == False:
                
                # randomly select number of distractor (numbers) in each intervals
                random.seed();
                numberOfFirstInterval = random.randint(3,10);
                numberOfLastInterval = (nNumberDistractors[0] + nNumberDistractors[2]) - numberOfFirstInterval;
                
                nNumberDistractors = [numberOfFirstInterval, nNumberDistractors[1], numberOfLastInterval]
                
                # write response to .txt
                line = expTrials[thisBlock][thisTrial] + [numberOfFirstInterval] + [numberOfLastInterval]
                line = '\t'.join(str(i) for i in line)
                line += '\t'
                dataFile.write(line)
                dataFile.flush()
                os.fsync(dataFile)
                
                # Generate Character Targets List / Format: [1st Target, 2nd Target, ...]
                characterTargets = []; random.seed(); random.shuffle(characterPool);
                for thisCharacter in range(nCharacterTargets):
                    textStim=visual.TextStim(win,
                        text='defualt, you can change the text by code text.text',
                        height=letterSize, pos=[0,0], color=[-1,-1,-1], font='Arial', colorSpace='rgb', ori=0, wrapWidth=None, opacity=1, depth=0.0, units='pix')
                    textStim.text = characterPool[thisCharacter][0]
                    characterTargets.append(textStim)
                
                # Generate Number Distractors List / Format: [[1st interval], [2nd interval], [3rd interval], ...]
                numberDistractors = [];
                for thisNumberGroup in range(len(nNumberDistractors)):
                    random.seed(); random.shuffle(numberpool);
                    tmpNumberDistractors = [];
                    for thisNumber in range(nNumberDistractors[thisNumberGroup]):
                        textStim=visual.TextStim(win,
                            text='defualt, you can change the text by code text.text',
                            height=letterSize, pos=[0,0], color=[-1,-1,-1], font='Arial', colorSpace='rgb', ori=0, wrapWidth=None, opacity=1, depth=0.0, units='pix')
                        whichNumberDistractor = random.randint(0,8);
                        textStim.text = numberpool[whichNumberDistractor]
                        tmpNumberDistractors.append(textStim)
                    numberDistractors.append(tmpNumberDistractors)
                
                # Combine Character Targets & Number Distractors
                expStim = []; thisNumberDistractor = 0; thisCharacterTarget = 0;
                for thisInterval in range(len(numberDistractors) + len(characterTargets)):
                    if returnNumber(thisInterval, 2) == 0: # even
                        expStim = expStim + numberDistractors[thisNumberDistractor]
                        thisNumberDistractor += 1;
                    elif returnNumber(thisInterval, 2) == 1: # odd
                        expStim.append(characterTargets[thisCharacterTarget])
                        thisCharacterTarget += 1;
                        
                # write response to .txt
                line = characterPool[0][0] + '\t' + characterPool[1][0]
                line += '\t'
                dataFile.write(line)
                dataFile.flush()
                os.fsync(dataFile)
                        
                drawnT = True
        
        #========================================
        # Draw Stimuli sequentially==============
        #========================================
        for thisLetter in range(len(expStim)):
            expStim[thisLetter].draw()
            win.flip()
            
            itiTargetOnset = globalClock.getTime()
            drawnT = False
            while globalClock.getTime() - itiTargetOnset <= durationForLetters: # duration between stimuli
                if drawnT == False:
                    drawnT == True
        backgroundRect.draw()
        win.flip()
        
        #========================
        # Get Responses==========
        #========================
        durationForResponse=1;
        
        itiTargetOnset = globalClock.getTime();
#        ResponseToFirst = ['TimeOVer'];
        ResponseTimeForSecond = durationForResponse;
#        while globalClock.getTime() - itiTargetOnset <= durationForResponse: # duration between stimuli
        if ignoreOrNot in [0]:
            # Response To First Letter
            backgroundRect.draw()
            numberOfInstruction=4
            instructions[numberOfInstruction].size=[instructionSizeX[0], instructionSizeX[0]*(instructionSizes[numberOfInstruction][1]/instructionSizes[numberOfInstruction][0])]
            instructions[numberOfInstruction].draw()
            win.flip()
            
            ResponseToFirst = [''];
            ResponseTimeForFirstOnset = globalClock.getTime()
            while ResponseToFirst[0] == '':
                ResponseToFirst = event.waitKeys()
#                print(ResponseToFirst)
            ResponseTimeForFirstOffset = globalClock.getTime()
            ResponseTimeForFirst = ResponseTimeForFirstOffset - ResponseTimeForFirstOnset;
        else:
            ResponseToFirst=['null']
            ResponseTimeForFirst=-1
        
        itiTargetOnset = globalClock.getTime()
#        ResponseToFirst = ['TimeOVer'];
        ResponseTimeForSecond = durationForResponse;
#        while globalClock.getTime() - itiTargetOnset <= durationForResponse: # duration between stimuli
        # Response To Second Letter
        backgroundRect.draw()
        numberOfInstruction=5
        instructions[numberOfInstruction].size=[instructionSizeX[0], instructionSizeX[0]*(instructionSizes[numberOfInstruction][1]/instructionSizes[numberOfInstruction][0])]
        instructions[numberOfInstruction].draw()
        win.flip()
        
        ResponseToSecond = [''];
        ResponseTimeForSecondOnset = globalClock.getTime()
        while ResponseToSecond[0] == '':
            ResponseToSecond = event.waitKeys()
#            print(ResponseToSecond)
        ResponseTimeForSecondOffset = globalClock.getTime()
        ResponseTimeForSecond = ResponseTimeForSecondOffset - ResponseTimeForSecondOnset;
        
        #==========================================================
        # Draw Result of Responses Whether Correct Or Not==========
        #==========================================================
        if (ignoreOrNot in [0]) and (ResponseToFirst[0] == characterPool[0][1]) and (ResponseToSecond[0] == characterPool[1][1]):
            numberOfInstruction=6; # number of instruction
            correctOrNotInFrist=1; #
            correctOrNotInSecond=1;
            
        elif (ignoreOrNot in [0]) and (ResponseToFirst[0] == characterPool[0][1]) and (ResponseToSecond[0] != characterPool[1][1]):
            numberOfInstruction=7; # number of instruction
            correctOrNotInFrist=1; #
            correctOrNotInSecond=0;
            
        elif (ignoreOrNot in [0]) and (ResponseToFirst[0] != characterPool[0][1]) and (ResponseToSecond[0] == characterPool[1][1]):
            numberOfInstruction=8; # number of instruction
            correctOrNotInFrist=0; #
            correctOrNotInSecond=1;
            
        elif (ignoreOrNot in [0]) and (ResponseToFirst[0] != characterPool[0][1]) and (ResponseToSecond[0] != characterPool[1][1]):
            numberOfInstruction=9; # number of instruction
            correctOrNotInFrist=0; #
            correctOrNotInSecond=0;
            
        elif (ignoreOrNot in [1]) and (ResponseToSecond[0] == characterPool[1][1]):
            numberOfInstruction=10; # number of instruction
            correctOrNotInFrist=-1; #
            correctOrNotInSecond=1;
            
        elif (ignoreOrNot in [1]) and (ResponseToSecond[0] != characterPool[1][1]):
            numberOfInstruction=11; # number of instruction
            correctOrNotInFrist=-1; #
            correctOrNotInSecond=0;
        
        
#        # Get The Response To First Letter
#        if ignoreOrNot in [0]:
#            if ResponseToFirst[0] == characterPool[0][1]: # [location][capital or small letter]
#                numberOfInstruction=6
#                correctOrNotInFrist = 1
#            else:
#                numberOfInstruction=7
#                correctOrNotInFrist = 0
#            print 'Answer First:', characterPool[0]
#        else:
#            correctOrNotInFrist = -1
#        
#        # Get The Response To Second Letter
#        if ResponseToSecond[0] == characterPool[1][1]:
#            numberOfInstruction=6
#            correctOrNotInSecond = 1
#        else:
#            numberOfInstruction=7
#            correctOrNotInSecond = 0
#        print 'Answer Second:', characterPool[1]
        
        # Drawing Result of Whether Correct Or Not
#        print numberOfInstruction
#        instructions[numberOfInstruction].size=[instructionSizeX[1], instructionSizeX[1]*(instructionSizes[numberOfInstruction][1]/instructionSizes[numberOfInstruction][0])]
#        instructions[numberOfInstruction].draw()
        win.flip()
        
        #=====================
        # Record Responses====
        #=====================
        # write response to .txt
        tmpLine = ResponseToFirst[0] + '\t' + ResponseToSecond[0] + '\t'
        line = [correctOrNotInFrist] + [correctOrNotInSecond] + [ResponseTimeForFirst] + [ResponseTimeForSecond]
        line = '\t'.join(str(i) for i in line)
        line = tmpLine + line
        line += '\n'
        dataFile.write(line)
        dataFile.flush()
        os.fsync(dataFile)
        
        core.wait(1)
        
numberOfInstruction=0
instructions[numberOfInstruction].size=[instructionSizeX[0], instructionSizeX[0]*(instructionSizes[numberOfInstruction][1]/instructionSizes[numberOfInstruction][0])]
instructions[numberOfInstruction].draw()
win.flip()
event.waitKeys(keyList = ['escape'])
event.clearEvents()
core.quit()