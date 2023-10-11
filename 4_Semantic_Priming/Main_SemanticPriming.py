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
associationTypeList=[0,1,2,3] # 0: hi-imagery words pairs, 1: low-imagery, 2: no-imagery, 3: non-words
wordList=range(20) # number of words
#wordList=range(3) # number of words
primingWordList=wordList # number of priming words
targetWordList=wordList # number of target words

instructionList=range(7) # number of instruction images

imgSizeX=20
imgSize=[imgSizeX, imgSizeX*(606/921)] # (606/921): word images' size ratio / size on file: 1594, 1048 / size without blank: 943, 435
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

if not os.path.isdir('data'):
    os.makedirs('data') #if this fails (e.g. permissions) we will get error
fileName='data' + os.path.sep + '%s_%s_%s_%s' %(expName, expInfo['group'], expInfo['participant'], expInfo['date'])

groupIdx = int(expInfo['group']);
sbjIdx = int(expInfo['participant']);
# ====================================================================================================================================================================
# open text file for writing data==================================================================================================================================================
# ====================================================================================================================================================================
dataFile = open(fileName+'.txt', 'w')
dataFile.write('group\t' 'sbj\t' 'serial\t' 'BlockIdx\t' 'TrialIdx\t' 'PrimingWordNumber(1-20)\t' 'TargetWordNumber(1-20)\t' 'AssociationTypeIdx(1:high-association, 2:low-association, 3:non-association, 4:non-word)\t' 'Response(0:left-nonWord, 1:right-word)\t' 'CorrectOrNot(0:wrong, 1:correct)\t' 'ReseponseTime(unit:second)\n')


# experimental design=======================================================================================================================
expTrials = []; thisSerial=0;
for thisBlock in range(nBlocks):
    thisTrial=0; blockTrials=[];
    for thisCondi in range(len(associationTypeList)):
        for thisWord in range(len(wordList)):
            thisSerial+=1; thisTrial+=1;
            trial = [groupIdx] + [sbjIdx] + [thisSerial+1] + [thisBlock+1] + [thisTrial+1] + [thisWord+1] + [thisWord+1] + [thisCondi+1]
            blockTrials.append(trial)
    random.seed()
    random.shuffle(blockTrials)
    expTrials.append(blockTrials)

groupIdx = 0
sbjIdx = 1
serialLoc = 2
blockLoc = 3
trialLoc = 4
primingWordLoc = 5
targetWordLoc = 6
condiLoc = 7

nTotalTrials=len(associationTypeList)*len(wordList)

serialIdx=0
for thisBlock in range(nBlocks):
    trialIdx=0
    for thisCondi in range(len(associationTypeList)):
        for thisWord in range(len(wordList)):
            serialIdx+=1
            trialIdx+=1
            expTrials[thisBlock][serialIdx-1][serialLoc]=serialIdx
            expTrials[thisBlock][serialIdx-1][trialLoc]=trialIdx

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
associationTypePaths=['/word_stimuli/hi_association','/word_stimuli/low_association','/word_stimuli/non_association','/word_stimuli/non_word']
presentingTypePaths=['/priming_words/', '/target_words/']
wordNameList_associ=['hi_association_', 'low_association_', 'non_association_', 'non_']
wordNameList_presenting=['priming', 'target']

associationTypes=[]; startingLoadingNumber=0; endingLoadingNumber=len(associationTypePaths)*len(presentingTypePaths)*len(wordList);
for thisAssoci in range(len(associationTypePaths)):
    presentingTypes=[]
    for thisPresenting in range(len(presentingTypePaths)):
        words=[]
        for thisWords in range(len(wordList)):
            if thisWords < 9:
                stimName = os.getcwd() + associationTypePaths[thisAssoci] + presentingTypePaths[thisPresenting] + wordNameList_associ[thisAssoci] + wordNameList_presenting[thisPresenting] + '_word' + '_' + '0' + str(thisWords+1) + '.png'
            else:
                stimName = os.getcwd() + associationTypePaths[thisAssoci] + presentingTypePaths[thisPresenting] + wordNameList_associ[thisAssoci] + wordNameList_presenting[thisPresenting] + '_word' + '_' + str(thisWords+1) + '.png'
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
        presentingTypes.append(words)
    associationTypes.append(presentingTypes)

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
            
            associationTypes[associationTypeIdx][0][wordNumberIdx].draw()
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
            
            associationTypes[associationTypeIdx][1][wordNumberIdx].draw()
            win.flip()
            
            responseStartingTime = globalClock.getTime()
            responsePressed = False; responseTime = durationForTarget;
            responseTime=2; response=-1; correctOrNot = -1; # defualt response value without acutal response
            event.clearEvents()
            while globalClock.getTime() - responseStartingTime <= durationForTarget and responsePressed == False: # duration for presenting target word
                
                # get response
                if event.getKeys('left'):
                    response=0
                    responseTime = globalClock.getTime() - responseStartingTime
                    responsePressed=True
                    
                elif event.getKeys('right'):
                    response=1
                    responseTime = globalClock.getTime() - responseStartingTime
                    responsePressed=True
            
            # record the response
            responseRecordingStartingTime = globalClock.getTime(); record=False;
            while globalClock.getTime() - responseRecordingStartingTime <= 0.5:
                
                if record == False:
                    # determine whether response was corret
                    correctOrNot = 0
                    if (associationTypeIdx == 3 and response == 0) or (associationTypeIdx < 3 and response == 1):
                        correctOrNot = 1
                    elif response==-1:
                        correctOrNot=-1
                    
                    # write response to .txt
                    line = expTrials[thisBlock][thisTrial] + [response] + [correctOrNot] + [responseTime]
                    line = '\t'.join(str(i) for i in line)
                    line += '\n'
                    dataFile.write(line)
                    dataFile.flush()
                    os.fsync(dataFile)
                    
                    drawnT=True # terminate target word scene after response
                    core.wait(0.5)
                    record=True

instructions[2].size=[instructionSizeX[1], instructionSizeX[1]*(instructionSizes[2][1]/instructionSizes[2][0])]
instructions[2].draw()
win.flip()
event.waitKeys(keyList=['escape'])
win.setMouseVisible(True)
core.quit()