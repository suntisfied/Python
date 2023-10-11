from __future__ import division #so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, misc, logging, gui, monitors
from numpy import *
import os #handy system and path functions
import math
from PIL import Image # Get the size(demension) of an image

def returnNumber(inputNumber, returnUnit):
    return inputNumber - (floor(inputNumber/returnUnit)*returnUnit)
def isOdd(inputNumber):
    return ceil(float(inputNumber)/2-floor(float(inputNumber)/2))

# value setting=============
nBlocks=1
associationTypeList=[0,1] # 0: words, 1: non-words
wordList=range(10) # number of words
primingWordList=wordList # number of priming words
targetWordList=wordList # number of target words

instructionList=range(7) # number of instruction images

imgSizeX=20 # actual visual angle: 60% (blank space)
imgSize=[imgSizeX, imgSizeX*(606/921)] # (606/921): word images' size ratio
instructionSizeX=[40,30]
fixationSizeX=5

durationForInstruction=1.4
durationForPriming=0.5
durationForBlank=0.5
durationForTarget=2

# pop up for subject number~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
expName='serial_words_presentation' # practice on only vertical gratings
expInfo={'group':'00', 'participant':'00'}
dlg=gui.DlgFromDict(dictionary=expInfo,title=expName)
if dlg.OK==False: core.quit() #user pressed cancel
expInfo['date']=data.getDateStr()#add a simple timestamp
expInfo['expName']=expName

sbjIdx = int(expInfo['participant']);

# experimental design=======================================================================================================================
expTrials = []; thisSerial=0;
for thisBlock in range(nBlocks):
    thisTrial=0; blockTrials=[];
    for thisCondi in range(len(associationTypeList)):
        for thisWord in range(len(wordList)):
            thisSerial+=1; thisTrial+=1;
            trial = [sbjIdx] + [thisSerial+1] + [thisBlock+1] + [thisTrial+1] + [thisWord+1] + [thisWord+1] + [thisCondi+1]
            blockTrials.append(trial)
    random.seed()
    random.shuffle(blockTrials)
    expTrials.append(blockTrials)

sbjIdx=0
serialLoc=1
blockLoc=2
trialLoc=3
primingWordLoc=4
targetWordLoc=5
condiLoc=6

nTotalTrials=len(associationTypeList)*len(wordList)

serialIdx=0
for thisBlock in range(nBlocks):
    for thisCondi in range(len(associationTypeList)):
        for thisWord in range(len(wordList)):
            serialIdx+=1
            expTrials[thisBlock][serialIdx-1][serialLoc]=serialIdx

# open window===============================================================================================================================
win = visual.Window(screen = 0, color = 1, fullscr = True, monitor='testMonitor', units='deg')
globalClock = core.Clock()
win.setMouseVisible(False)
# ===========================================================================================================================================
# prepare word images========================================================================================================================
# ===========================================================================================================================================
# text stimulus (available only for english)
textStim=visual.TextStim(win,
    text='defualt, you can change the text by code text.text',
    height=30, pos=[0,0], color=[-1,-1,-1], font='Arial', colorSpace='rgb', ori=0, wrapWidth=None, opacity=1, depth=0.0, units='pix')

# images of word stimuli
associationTypePaths=['/word_stimuli/practice/words/practice_word','/word_stimuli/practice/nonWords/practice_nonWord']

associationTypes=[]; startingLoadingNumber=0; endingLoadingNumber=len(associationTypePaths)*len(wordList);
for thisAssoci in range(len(associationTypePaths)):
    words=[]
    for thisWords in range(len(wordList)):
        if thisWords < 9:
            stimName = os.getcwd() + associationTypePaths[thisAssoci] + '_' + '0' + str(thisWords+1) + '.png'
        else:
            stimName = os.getcwd() + associationTypePaths[thisAssoci] + '_' + str(thisWords+1) + '.png'
        thisStimWords = visual.ImageStim(win, image=stimName, mask = 'none',
                size=imgSize,#will be the size of the original image in pixels
                units='deg', interpolate=True,
                autoLog=False)
        
        # calculate how far loading proceeds
        startingLoadingNumber+=1
        loadingPercent=int(round((startingLoadingNumber/endingLoadingNumber)*100))
        
        textStim.height=40
        if startingLoadingNumber==endingLoadingNumber:
            textStim.text='Now Loading  ' + '100' + '%'
        else:   
            textStim.text='Now Loading  ' + str(loadingPercent) + '%'
        
        textStim.draw()
        win.flip()
        
        words.append(thisStimWords)
    associationTypes.append(words)

# images of instruction
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

instructions[1].size=[instructionSizeX[0], instructionSizeX[0]*(instructionSizes[1][1]/instructionSizes[1][0])]
instructions[1].draw()
win.flip()
event.waitKeys(keyList=['return'])

# ====================================================================================================================================
# experiment start ===================================================================================================================
# ====================================================================================================================================
thisTrial=-1
for thisBlock in range(nBlocks):
    for thisAssoci in range(len(associationTypePaths)):
        for thisWords in range(len(wordList)):
            thisTrial+=1
            
            associationTypeIdx = expTrials[thisBlock][thisTrial][condiLoc]-1
            wordNumberIdx = expTrials[thisBlock][thisTrial][primingWordLoc]-1
            
            instructions[0].size=[fixationSizeX, fixationSizeX*(instructionSizes[0][1]/instructionSizes[0][0])]
            instructions[0].draw()
            win.flip()
            
            itiTargetOnset = globalClock.getTime()
            drawnT = False
            while globalClock.getTime() - itiTargetOnset <= durationForInstruction: # duration for presenting instruction
                if drawnT == False:
                    drawnT == True
            
            associationTypes[0][wordNumberIdx].draw()
            win.flip()
            
            itiTargetOnset = globalClock.getTime()
            drawnT = False
            while globalClock.getTime() - itiTargetOnset <= durationForPriming: # duration for presenting priming word
                if drawnT == False:
                    drawnT == True
            
            win.flip()
            
            itiTargetOnset = globalClock.getTime()
            drawnT = False
            while globalClock.getTime() - itiTargetOnset <= durationForBlank: # duration for presenting black screen
                if drawnT == False:
                    drawnT == True
            
            associationTypes[associationTypeIdx][int(returnNumber(wordNumberIdx+1, len(wordList)))].draw()
            win.flip()
            
            responseStartingTime = globalClock.getTime()
            drawnT = False; responsePressed = False;
            event.clearEvents()
            while globalClock.getTime() - responseStartingTime <= durationForTarget and drawnT == False: # duration for presenting target word
                
                # get response
                if event.getKeys('left'):
                    response=0
                    responsePressed=True
                    
                elif event.getKeys('right'):
                    response=1
                    responsePressed=True
                    
                # record the response
                if responsePressed==True:
                    
                    # determine whether response was corret
                    correctOrNot = 0
                    if (associationTypeIdx == 1 and response == 0) or (associationTypeIdx ==0 and response == 1):
                        correctOrNot = 1
                    core.wait(0.5)
                    if correctOrNot == 1:
                        instructions[3].size=[fixationSizeX, fixationSizeX*(instructionSizes[3][1]/instructionSizes[3][0])]
                        instructions[3].draw()
                        win.flip()
                        
                    elif correctOrNot == 0:
                        instructions[4].size=[fixationSizeX, fixationSizeX*(instructionSizes[4][1]/instructionSizes[4][0])]
                        instructions[4].draw()
                        win.flip()
                        
                    core.wait(0.5)
                    
                    drawnT=True

instructions[2].size=[instructionSizeX[1], instructionSizeX[1]*(instructionSizes[2][1]/instructionSizes[2][0])]
instructions[2].draw()
win.flip()
event.waitKeys(keyList=['escape'])
win.setMouseVisible(True)
core.quit()