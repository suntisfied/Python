#========================
# Load Libraries=========
#========================
from __future__ import division #so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, misc, logging, gui, monitors
from psychopy.hardware.emulator import launchScan
from PIL import Image # Get the size(demension) of an image
from numpy import *
from math import *
import os #handy system and path functions

#========================
# Define Functions=======
#========================
def returnNumber(inputNumber, returnUnit):
    return int(inputNumber - (floor(inputNumber/returnUnit)*returnUnit))
def isOdd(inputNumber):
    return int(ceil(float(inputNumber)/2-floor(float(inputNumber)/2)))
def isEven(inputNumber):
    return int(1-ceil(float(inputNumber)/2-floor(float(inputNumber)/2)))

#======================
# Parameters===========
#======================
# Monitor Size
crossInchOfMonitor=13.3
mesuredMonitorHorizontalSize=29.8
monHz=60

# Practice Trials
nPractice=4
restInterval=40
restTime=30
termiValue=0.8
maxTermiValue=8

# Repetition of Main Experiment
nBlocks=20

# Presenting Times (units: second)
fixationT=1
targetT=0.15
maxResT=3
tailTPrac=1
tailTMain=0.1

# Experimental Variables
instructionTypeList=[0,1]
arrowDirectionList=[0,1] # 0: downward / 1: upward
arrowLocationList=[0,1] # 0: below / 1: up

# Instruction Images
nInstruction=20
instructionList=range(nInstruction)
instructionHorzRatio=0.7

# Background Screen
backgroundColor=[-1,-1,-1]
screenNum=0

# Fixation Cross
fixationCrossSize=2 # units: cm
fixationCrossThickness=0.2 # units: cm
fixationCorssColor=[1,1,1]

# Arrow
arrowLen=1.7
arrowTriangleHeight=0.6 # units: cm
arrowThickness=0.2 # units: cm
arrowLocationFromCenter=3.2 # units: cm
arrowColor=[1,1,1]

#===============================================
# Setup of Pop Up Window=======================
#===============================================
expName='LDST' # practice response to clockwise & counterclockwise
expInfo={'Initials_of_Name':'','Gender':'','Age':'','Participant_Number':''}
dlg=gui.DlgFromDict(dictionary=expInfo,title=expName)
if dlg.OK==False: core.quit() #user pressed cancel
expInfo['Date']=data.getDateStr()#add a simple timestamp
expInfo['ExpName']=expName

if expInfo['Initials_of_Name'] == '':
    intialIdx=-1
else:
    intialIdx=expInfo['Initials_of_Name'];

if expInfo['Gender'] == '':
    genderIdx=-1
else:
    genderIdx=int(expInfo['Gender']);

if expInfo['Age'] == '':
    ageIdx=-1
else:
    ageIdx=int(expInfo['Age']);

if expInfo['Participant_Number'] == '':
    sbjIdx=-1
else:
    sbjIdx=int(expInfo['Participant_Number']);

#==========================================================
# Open Text File for Writing Data==========================
#==========================================================
if not os.path.isdir('Data'):
    os.makedirs('Data') #if this fails (e.g. permissions) we will get error
fileName='Data' + os.path.sep + '%s_%s_%s_%s' %(expName, 'Participant', expInfo['Participant_Number'], expInfo['Date'])

# open data file & write the tilt of values
dataFile = open(fileName+'.txt', 'w')
dataFile.write('Participant_Number\t' 'Initials_of_Name\t' 'Gender\t' 'Age\t' 'SerialIdx\t' 'BlockIdx\t' 'TrialIdx\t' 'Instruction_Type\t' 'Arrow_Direction\t' 'Arrow_Location\t' 'Response\t' 'CorrectOrNot\t' 'ResponseTime\t' 'PracticeTrials\t' 'PracticeAccuracy\n')

#===============================================
# Make a Matrix for Experimental Design=========
#===============================================
# Main Experiment

expTrials = []; curSerialIdx=0; 
for curBlockIdx in range(nBlocks):
    curTrialIdx=0; blockTrials=[];
    for curInstructionType in instructionTypeList:
        for curArrowDirection in arrowDirectionList:
            for curArrowLocation in arrowLocationList:
                curSerialIdx+=1; curTrialIdx+=1;
                trial = [sbjIdx] + [intialIdx] + [genderIdx] + [ageIdx] + [curSerialIdx+1] + [curBlockIdx+1] + [curTrialIdx+1] + [curInstructionType] + [curArrowDirection] + [curArrowLocation]
                blockTrials.append(trial)
    random.seed()
    random.shuffle(blockTrials)
    expTrials.append(blockTrials)

sbjIdxLoc = 0
intialIdxLoc = 1
genderIdxLoc = 2
ageIdxLoc = 3
serialIdxLoc= 4
blockIdxLoc = 5
trialIdxLoc = 6
intructionTypeLoc = 7
arrowDirectionLoc = 8
arrowLocationLoc = 9

nTotalTrials=len(arrowDirectionList)*len(arrowLocationList)*len(instructionTypeList)
nRuns=nBlocks*nTotalTrials

serialIdx=0
for curBlock in range(nBlocks):
    trialIdx=0
    for curInstructionType in instructionTypeList:
        for curArrowDirection in arrowDirectionList:
            for curArrowLocation in arrowLocationList:
                serialIdx+=1
                trialIdx+=1
                
                expTrials[curBlock][trialIdx-1][serialIdxLoc]=serialIdx
                expTrials[curBlock][trialIdx-1][trialIdxLoc]=trialIdx
                if serialIdx <= nRuns/2:
                    expTrials[curBlock][trialIdx-1][intructionTypeLoc]=isEven(sbjIdx)
                else:
                    expTrials[curBlock][trialIdx-1][intructionTypeLoc]=isOdd(sbjIdx)
                    
# Practice Trials
practiceArrowDirectionList=[0,1]
practiceArrowLocationList=[0,1]

practiceArrowDirectionLoc=0
practiceArrowLocationLoc=1

nPracticeBlocks=int(ceil(nPractice/(len(practiceArrowDirectionList)*len(practiceArrowLocationList))))

practiceExpTrials = [];
for curBlockIdx in range(nPracticeBlocks):
    blockTrials=[];
    for curpracticeArrowDirection in practiceArrowDirectionList:
        for practiceArrowLocation in practiceArrowLocationList:
            practiceTrial = [curpracticeArrowDirection] + [practiceArrowLocation]
            blockTrials.append(practiceTrial)
    random.seed()
    random.shuffle(blockTrials)
    practiceExpTrials = practiceExpTrials + blockTrials
    
random.seed()
random.shuffle(practiceExpTrials)

#======================
# Open a Window========
#======================

# Open Window
win = visual.Window(color = backgroundColor, fullscr = True, monitor='default', screen = screenNum, units='pix')
win.mouseVisible=False
# Actual Measure by Flip Test (takes some times)
#MsPerFrame = win.getMsPerFrame(nFrames=monHz)
#MsPerFrame = MsPerFrame[0]/1000
# Theoretical Calculation
MsPerFrame=1/monHz

crossCmOfmonitor=crossInchOfMonitor*2.54 # convert inch to cm
monitorHorizontalSize=sqrt((win.size[0]**2/(win.size[0]**2+win.size[1]**2))*crossCmOfmonitor**2) # induced by the Pythagorean theorem
monitorHorizontalSize=mesuredMonitorHorizontalSize # actually measured size
def cm2pix(inputCm):
    return int(round(inputCm*(win.size[0]/monitorHorizontalSize)))

#==============================
# Load Instruction Images======
#==============================
instructions=[]; instructionSizes=[];
for curInstr in range(len(instructionList)):
    instructionName = os.getcwd() + '/Instruction_Images/Instruction' + str(curInstr+1) + '.png'
    img = Image.open(instructionName)
    instructionSizes.append(img.size)
    curInstructions = visual.ImageStim(win, image=instructionName, mask = 'none',
                size=[5,5],#will be the size of the original image in pixels
                units='pix', interpolate=True,
                autoLog=False)
    instructions.append(curInstructions)

#===================
# Make Stimuli======
#===================
# Fixation Cross
fixationCrossSize=cm2pix(fixationCrossSize)
fixationCrossThickness=cm2pix(fixationCrossThickness)

fixationVert = [(0,-fixationCrossSize/2),(0,fixationCrossSize/2),(0,0),(fixationCrossSize/2,0),(-fixationCrossSize/2,0)]
fixationCross = visual.ShapeStim(win,vertices=fixationVert,lineWidth=fixationCrossThickness, lineColor=fixationCorssColor, closeShape=False, ori=0)
    
# Experimental Stimulus; Arrow
arrowLen=cm2pix(arrowLen)
arrowTriangleHeight=cm2pix(arrowTriangleHeight)
arrowThickness=cm2pix(arrowThickness)

arrowTriangleSideLen=(2/sqrt(3))*arrowTriangleHeight

arrowVert=[[-(arrowThickness/2),-arrowLen/2],
            [(arrowThickness/2),-arrowLen/2],
            [arrowThickness/2,(arrowLen/2)-arrowTriangleHeight],
            [(arrowTriangleSideLen/2),(arrowLen/2)-arrowTriangleHeight],
            [0,arrowLen/2],
            [-(arrowTriangleSideLen/2),(arrowLen/2)-arrowTriangleHeight],
            [-(arrowThickness/2),(arrowLen/2)-arrowTriangleHeight]]

arrowStim = visual.ShapeStim(win,
    vertices = arrowVert,
    lineWidth = 0, fillColor=arrowColor, closeShape=True, ori=0)

#=================================================================================================
#=================================================================================================
# Start Experiment================================================================================
#=================================================================================================
#=================================================================================================

stimPosList=[[0,-cm2pix(arrowLocationFromCenter)],[0,cm2pix(arrowLocationFromCenter)]]

loopSerialNum=-1; practiceTrial=-1; practiceSerial=-1;

correctOrNotSerialPool=[]; practiceD=True
globalClock = core.Clock()
for curBlock in range(nBlocks):
    
    # Reset Values according to Experimental Versions
    if (curBlock == 0) or (curBlock == ceil(nBlocks/2)):
        loopSerialNum=-1
        practiceSerial=-1
        correctOrNotTrialPool=[]
        correctOrNotSerialPool=[]
        practiceD=True
        
    curTrial=-1
    while curTrial < (nTotalTrials-1):
        
        loopSerialNum+=1
        
        # Determine Whether Practice & Main
        if (practiceD == False) or (loopSerialNum > maxTermiValue-1) or (nPractice==0):
            curTrial+=1
            nPracInExp=practiceSerial+1 # practiceTrial: reset by every nPractice // loopSerialNum: reset by whole exptrials
            accPracInExp=mean(correctOrNotSerialPool)
        
        # for Practice Trials
        if curTrial==-1:
            practiceTrial+=1
            practiceSerial+=1
            
            if returnNumber(loopSerialNum, nPractice)==0:
                practiceTrial=0
                correctOrNotTrialPool=[]
                
                # Shuffle Practice Trials at Each Practice Blocks
                random.seed()
                random.shuffle(practiceExpTrials)
        
        # Determine Whether to Proceed or Quit the Practice
        if (practiceD == True) and (practiceSerial>0) and (practiceTrial==0):
            # Instruction 11
            instructionIdx=10
            instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
            instructions[instructionIdx].draw()
            win.flip()
            # Proceed after Key Press
            event.clearEvents()
            pressedDefault=False
            while pressedDefault==False:
                if event.getKeys(keyList=['escape']):
                    core.quit()
                if event.getKeys(keyList=['space']):
                    pressedDefault=True
                    
        # Instructions for Practice Trials
        if (practiceD == True) and (practiceTrial==0):
            
            # Instruction 1
            if not nPractice==0:
                
                instructionIdx=0
                instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
                instructions[instructionIdx].draw()
                win.flip()
                # Proceed after Key Press
                event.clearEvents()
                pressedDefault=False
                while pressedDefault==False:
                    if event.getKeys(keyList=['escape']):
                        core.quit()
                    if event.getKeys(keyList=['space']):
                        pressedDefault=True
                
            # Instruction 2
            instructionIdx=1
            instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
            instructions[instructionIdx].draw()
            win.flip()
            # Proceed after Key Press
            event.clearEvents()
            pressedDefault=False
            while pressedDefault==False:
                if event.getKeys(keyList=['escape']):
                    core.quit()
                if event.getKeys(keyList=['space']):
                    pressedDefault=True
                    
            # Instruction 3
            instructionIdx=2
            instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
            instructions[instructionIdx].draw()
            win.flip()
            # Proceed after Key Press
            event.clearEvents()
            pressedDefault=False
            while pressedDefault==False:
                if event.getKeys(keyList=['escape']):
                    core.quit()
                if event.getKeys(keyList=['space']):
                    pressedDefault=True
            
            if (expTrials[curBlock][0][intructionTypeLoc]==0):
                # Instruction 4
                instructionIdx=3
                instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
                instructions[instructionIdx].draw()
                win.flip()
                # Proceed after Key Press
                event.clearEvents()
                pressedDefault=False
                while pressedDefault==False:
                    if event.getKeys(keyList=['escape']):
                        core.quit()
                    if event.getKeys(keyList=['space']):
                        pressedDefault=True
                
                # Instruction 5
                instructionIdx=4
                instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
                instructions[instructionIdx].draw()
                win.flip()
                # Proceed after Key Press
                event.clearEvents()
                pressedDefault=False
                while pressedDefault==False:
                    if event.getKeys(keyList=['escape']):
                        core.quit()
                    if event.getKeys(keyList=['space']):
                        pressedDefault=True
                
            
            if (expTrials[curBlock][0][intructionTypeLoc]==1):
                
                # Instruction 7
                instructionIdx=6
                instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
                instructions[instructionIdx].draw()
                win.flip()
                # Proceed after Key Press
                event.clearEvents()
                pressedDefault=False
                while pressedDefault==False:
                    if event.getKeys(keyList=['escape']):
                        core.quit()
                    if event.getKeys(keyList=['space']):
                        pressedDefault=True
                
                # Instruction 8
                instructionIdx=7
                instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
                instructions[instructionIdx].draw()
                win.flip()
                # Proceed after Key Press
                event.clearEvents()
                pressedDefault=False
                while pressedDefault==False:
                    if event.getKeys(keyList=['escape']):
                        core.quit()
                    if event.getKeys(keyList=['space']):
                        pressedDefault=True
                
            # Instruction 9
            instructionIdx=8
            instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
            instructions[instructionIdx].draw()
            win.flip()
            # Proceed after Key Press
            event.clearEvents()
            pressedDefault=False
            while pressedDefault==False:
                if event.getKeys(keyList=['escape']):
                    core.quit()
                if event.getKeys(keyList=['space']):
                    pressedDefault=True
            
            # Instruction 10
            if not nPractice==0:
                instructionIdx=9
                instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
                instructions[instructionIdx].draw()
                win.flip()
                # Proceed after Key Press
                event.clearEvents()
                pressedDefault=False
                while pressedDefault==False:
                    if event.getKeys(keyList=['escape']):
                        core.quit()
                    if event.getKeys(keyList=['space']):
                        pressedDefault=True
            
            
        # Instruction for Starting Main Exp
        if (curBlock==0 and curTrial==0) or (curBlock==ceil(nBlocks/2) and curTrial==0):
            # Instruction 12
            instructionIdx=11
            instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
            instructions[instructionIdx].draw()
            win.flip()
            # Proceed after Key Press
            event.clearEvents()
            pressedDefault=False
            while pressedDefault==False:
                if event.getKeys(keyList=['escape']):
                    core.quit()
                if event.getKeys(keyList=['space']):
                    pressedDefault=True
            
        # Draw Cross
        fixationCross.draw()
        win.flip()
        
        startT=globalClock.getTime(); drawnT=False;
        while globalClock.getTime() - startT <= fixationT - MsPerFrame:
            if event.getKeys(keyList=['escape']):
                core.quit()
            
            if drawnT==False:
                
                if curTrial==-1:
                    arrowStim.ori=(practiceExpTrials[practiceTrial][practiceArrowDirectionLoc]-1)*180
                    arrowStim.pos=stimPosList[practiceExpTrials[practiceTrial][practiceArrowLocationLoc]]
                    
                    arrowStim.draw()
                        
                else:
                    arrowStim.ori=(expTrials[curBlock][curTrial][arrowDirectionLoc]-1)*180
                    arrowStim.pos=stimPosList[expTrials[curBlock][curTrial][arrowLocationLoc]] # Loaction of Cue Lectagular
                    
                    arrowStim.draw()
                drawnT=True
                
        win.flip()
        
        # Draw Stimuli: arrow
        event.clearEvents()
        startTarget=globalClock.getTime(); response=-1; drawnCue=False;
        while globalClock.getTime() - startTarget <= targetT - MsPerFrame:
            if event.getKeys(keyList=['escape']):
                core.quit()
            
            if drawnCue==False:
                if curTrial==-1:
                    if (expTrials[curBlock][0][intructionTypeLoc]==0):
                        # Instruction 19
                        instructionIdx=18
                        instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
                        instructions[instructionIdx].draw()
                        
                    if (expTrials[curBlock][0][intructionTypeLoc]==1):
                        # Instruction 20
                        instructionIdx=19
                        instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
                        instructions[instructionIdx].draw()
                drawnCue=True
            
            if event.getKeys(keyList=['down']):
                response=0
                responseTime=globalClock.getTime()-startTarget
                
            if event.getKeys(keyList=['up']):
                response=1
                responseTime=globalClock.getTime()-startTarget
        
        win.flip()
        
        # Draw Response Scene
        startRes=globalClock.getTime();
        while (globalClock.getTime() - startRes <= maxResT) and (response==-1):
            if event.getKeys(keyList=['escape']):
                core.quit()
                
            if event.getKeys(keyList=['down']):
                response=0
                responseTime=globalClock.getTime()-startTarget
                
            if event.getKeys(keyList=['up']):
                response=1
                responseTime=globalClock.getTime()-startTarget
                
        if response==-1:
            responseTime=globalClock.getTime()-startTarget
            # ITI & Wirting Responses
            win.flip()
        
        if curTrial == -1:
            tailT = tailTPrac
        else:
            tailT = tailTMain
        
        startWritten=globalClock.getTime(); writtenRes=False;
        while (globalClock.getTime() - startWritten <= tailT):
            if event.getKeys(keyList=['escape']):
                core.quit()
            if writtenRes==False:
                # determine whether response was corret
                correctOrNot = 0
                
                if expTrials[curBlock][curTrial][intructionTypeLoc] == 0:
                    
                    if curTrial == -1:
                        targetIdx=practiceExpTrials[practiceTrial][practiceArrowLocationLoc]
                    else:
                        targetIdx=expTrials[curBlock][curTrial][arrowLocationLoc]
                    
                    if (targetIdx == 0 and response == 0) or (targetIdx ==1 and response == 1):
                        correctOrNot = 1
                    
                if expTrials[curBlock][curTrial][intructionTypeLoc] == 1:
                    
                    if curTrial == -1:
                        targetIdx=practiceExpTrials[practiceTrial][practiceArrowDirectionLoc]
                    else:
                        targetIdx=expTrials[curBlock][curTrial][arrowDirectionLoc]
                        
                    if (targetIdx == 0 and response == 0) or (targetIdx ==1 and response == 1):
                        correctOrNot = 1
                
                # for Practice Trials
                if curTrial==-1:
                    correctOrNotTrialPool.append(correctOrNot)
                    correctOrNotSerialPool.append(correctOrNot)
                
                if not curTrial == -1:
                    # write response to .txt
                    line = expTrials[curBlock][curTrial] + [response] + [correctOrNot] + [responseTime] + [nPracInExp] + [accPracInExp]
                    line = '\t'.join(str(i) for i in line)
                    line += '\n'
                    dataFile.write(line)
                    dataFile.flush()
                    os.fsync(dataFile)
                    
                if curTrial == -1:
                    if not response == -1:
                        if correctOrNot == 1:
                            # Instruction 14
                            instructionIdx=13
                            instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
                            instructions[instructionIdx].draw()
                        elif correctOrNot == 0:
                            # Instruction 15
                            instructionIdx=14
                            instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
                            instructions[instructionIdx].draw()
                    if response == -1:
                        # Instruction 16
                        instructionIdx=15
                        instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
                        instructions[instructionIdx].draw()
                    win.flip()
                writtenRes=True
        
        # Rest Between Blocks
        if not curTrial==-1:
            if returnNumber(expTrials[curBlock][curTrial][serialIdxLoc],restInterval)==0:
                
                event.clearEvents()
                startBlock=globalClock.getTime(); pressed=False; response=-1;
                while (globalClock.getTime() - startBlock <= restTime) and (pressed==False):
                    if event.getKeys(keyList=['escape']):
                        core.quit()
                    
                    # Instruction 17
                    instructionIdx=16
                    instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
                    instructions[instructionIdx].draw()
                    win.flip()
                    
                    if event.getKeys(keyList=['space']):
                        pressed=True
                
                event.clearEvents()
                # Instruction 18
                instructionIdx=17
                instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
                instructions[instructionIdx].draw()
                win.flip()
                # Proceed after Key Press
                event.clearEvents()
                pressedDefault=False
                while pressedDefault==False:
                    if event.getKeys(keyList=['escape']):
                        core.quit()
                    if event.getKeys(keyList=['space']):
                        pressedDefault=True
                        
        # Determine Whether pratice trials are terminated
        if not nPractice==0:
            if (returnNumber(practiceTrial, nPractice)==(nPractice-1)) and (len(correctOrNotTrialPool)>0):
                if (mean(correctOrNotTrialPool)>termiValue):
                    practiceD=False

# Instruction 13
instructionIdx=12
instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
instructions[instructionIdx].draw()
win.flip()
# Proceed after Key Press
event.clearEvents()
pressedDefault=False
while pressedDefault==False:
    if event.getKeys(keyList=['escape']):
        core.quit()
    if event.getKeys(keyList=['space']):
        pressedDefault=True