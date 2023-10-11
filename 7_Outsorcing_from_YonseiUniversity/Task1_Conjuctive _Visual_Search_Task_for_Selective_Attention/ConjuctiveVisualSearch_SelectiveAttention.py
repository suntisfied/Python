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

#======================
# Parameters===========
#======================
# Monitor Size
crossInchOfMonitor=13.3
mesuredMonitorHorizontalSize=29.8
monHz=60

# Practice Trials
nPractice=8
restInterval=40
restTime=30
termiValue=0.8
maxTermiValue=16

# Repetition of Main Experiment
nBlocks=20

# Presenting Times (units: second)
fixationT=1
tailTPrac=1
tailTMain=0.1

# Experimental Variables
setSizeList=[4,8,16,32]
targetList=[0,1] # 0: absent, 1: present

# Instruction Images
nInstruction=13
instructionList=range(nInstruction)
instructionHorzRatio=0.7

# Background Screen
backgroundColor=[-1,-1,-1] # black
screenNum=0

# Fixation Cross
fixationCrossSize=2 # units: cm
fixationCrossThickness=0.2 # units: cm
fixationCorssColor=[1,1,1] # white

# Target & Distractor
targetColor=[-1,-1,1] # blue
targetShape=1 # 0: circle / 1: square
distractorColor=[1,-1,-1] # red

# Square
squareSize=0.8 # units: cm
squareThickness=0.1 # units: cm

# Circle
circleDiameter=0.8 # units: cm
circleThickness=0.1 # units: cm

# Stimuli Matrix
matrixSize=[9.5,8] # horizontal, vertical

#===============================================
# Setup of Pop Up Window=======================
#===============================================
expName='CVST' # practice response to clockwise & counterclockwise
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
dataFile.write('Participant_Number\t' 'Initials_of_Name\t' 'Gender\t' 'Age\t' 'SerialIdx\t' 'BlockIdx\t' 'TrialIdx\t' 'Target_Presence\t' 'SetSize\t' 'Response\t' 'CorrectOrNot\t' 'ResponseTime\t' 'PracticeTrials\t' 'PracticeAccuracy\n')

#===============================================
# Make a Matrix for Experimental Design=========
#===============================================
# Main Experiment

expTrials = []; curSerialIdx=0; 
for curBlockIdx in range(nBlocks):
    curTrialIdx=0; blockTrials=[];
    for curTarget in targetList:
        for curSetSize in setSizeList:
            curSerialIdx+=1; curTrialIdx+=1;
            trial = [sbjIdx] + [intialIdx] + [genderIdx] + [ageIdx] + [curSerialIdx+1] + [curBlockIdx+1] + [curTrialIdx+1] + [curTarget] + [curSetSize]
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
targetLoc = 7
setSizeLoc = 8

serialIdx=0
for curBlock in range(nBlocks):
    trialIdx=0
    for curTarget in range(len(targetList)):
        for curSetSize in range(len(setSizeList)):
            serialIdx+=1
            trialIdx+=1
            
            expTrials[curBlock][trialIdx-1][serialIdxLoc]=serialIdx
            expTrials[curBlock][trialIdx-1][trialIdxLoc]=trialIdx

nTotalTrials=len(setSizeList)*len(targetList)
nRuns=nBlocks*nTotalTrials

# Practice Trials
practiceSetSizeList=[4,8,16,32]
practiceTargetList=[0,1]

practiceTargetLoc=0
practiceSetSizeLoc=1

nPracticeBlocks=int(ceil(nPractice/(len(practiceSetSizeList)*len(practiceTargetList))))

practiceExpTrials = [];
for curBlockIdx in range(nPracticeBlocks):
    blockTrials=[];
    for practiceSetSize in practiceSetSizeList:
        for practiceTarget in practiceTargetList:
            practiceTrial = [practiceTarget] + [practiceSetSize]
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
squareColor=[-1,-1,1] # blue
circleColor=[1,-1,-1] # red

# Fixation Cross
fixationCrossSize=cm2pix(fixationCrossSize)
fixationCrossThickness=cm2pix(fixationCrossThickness)
fixationVert = [(0,-fixationCrossSize/2),(0,fixationCrossSize/2),(0,0),(fixationCrossSize/2,0),(-fixationCrossSize/2,0)]
fixationCross = visual.ShapeStim(win,vertices=fixationVert,lineWidth=fixationCrossThickness, lineColor=fixationCorssColor, closeShape=False, ori=0)
    
# Experimental Stimulus; Square
squareSize=cm2pix(squareSize)
squareThickness=cm2pix(squareThickness)
outerSquareCoordi = squareSize/2
outerSquareVert = [[-outerSquareCoordi, outerSquareCoordi],[outerSquareCoordi,outerSquareCoordi],[outerSquareCoordi,-outerSquareCoordi],[-outerSquareCoordi,-outerSquareCoordi]]

innerSquareCoordi = outerSquareCoordi - (squareThickness/2)
innerSquareVert = [[-innerSquareCoordi, innerSquareCoordi],[innerSquareCoordi,innerSquareCoordi],[innerSquareCoordi,-innerSquareCoordi],[-innerSquareCoordi,-innerSquareCoordi]]

squareStim = visual.ShapeStim(win,
    vertices = [outerSquareVert, innerSquareVert],
    lineWidth = 0, fillColor=squareColor, closeShape=True, ori=0)
    
# Experimental Stimulus; Circle
circleDiameter=cm2pix(circleDiameter)
circleThickness=cm2pix(circleThickness)

outerCircleRadius=circleDiameter/2
outerCircleStim = visual.Circle(win=win,
    pos=[0, 0],
    radius=outerCircleRadius, edges=1024,
    lineWidth=2, # pixel unit
    lineColor=circleColor,
    fillColor=None)
outerCicleVert=outerCircleStim.vertices

innerCircleRadius=(circleDiameter-circleThickness)/2
innerCircleStim=visual.Circle(win=win,
    pos=[0, 0],
    radius=innerCircleRadius, edges=1024,
    lineWidth=2, # pixel unit
    lineColor=circleColor,
    fillColor=None)
innerCircleVert=innerCircleStim.vertices

circleStim=visual.ShapeStim(win,
    vertices = [outerCicleVert, innerCircleVert],
    lineWidth = 0, fillColor=circleColor, closeShape=True, ori=0)

# Sitmuli Positions in the Matrix
matrixSize=[cm2pix(matrixSize[0]), cm2pix(matrixSize[1])]
matrixElementSize=[7,6]
gapSize=[(matrixSize[0]-(matrixElementSize[0]*squareSize))/(matrixElementSize[0]-1), (matrixSize[1]-(matrixElementSize[1]*squareSize))/(matrixElementSize[1]-1)]

stimPoses=[]
for curMatrixVert in range(matrixElementSize[1]):
    curY=(curMatrixVert*squareSize) + (curMatrixVert*gapSize[1]) + (0.5*squareSize)
    for curMatrixHorz in range(matrixElementSize[0]):
        curX=(curMatrixHorz*squareSize) + (curMatrixHorz*gapSize[0]) + (0.5*squareSize)
        curPos=[curX-(matrixSize[0]/2),curY-(matrixSize[1]/2)]
        stimPoses.append(curPos)

#=================================================================================================
#=================================================================================================
# Start Experiment================================================================================
#=================================================================================================
#=================================================================================================

loopSerialNum=-1; practiceTrial=-1; practiceSerial=-1;

correctOrNotSerialPool=[]; practiceD=True
globalClock = core.Clock()
for curBlock in range(nBlocks):
    
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
            # Instruction 6
            instructionIdx=5
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
            if not nPractice==0:
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
                    
        # Instruction for Starting Main Exp
        if curBlock==0 and curTrial==0:
            # Instruction 7
            instructionIdx=6
            instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
            instructions[instructionIdx].draw()
            win.flip()
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
        
        event.clearEvents()
        startT=globalClock.getTime(); drawnT=False;
        while globalClock.getTime() - startT <= fixationT - MsPerFrame:
            if event.getKeys(keyList=['escape']):
                core.quit()
            
            if drawnT==False:
                
                if curTrial==-1:
                    nStim=practiceExpTrials[practiceTrial][practiceSetSizeLoc]
                else:
                    nStim=expTrials[curBlock][curTrial][setSizeLoc] # number of setSize
                    
                
                random.seed()
                random.shuffle(stimPoses) # Randomly Shuffle the positions of stimuli
                
                # Target
                if curTrial==-1:
                    targetPresence=practiceExpTrials[practiceTrial][practiceTargetLoc]
                else:
                    targetPresence=expTrials[curBlock][curTrial][targetLoc]
                
                targetOn=0
                if targetPresence==1:
                    
                    if targetShape==1:
                        squareStim.fillColor=targetColor
                        squareStim.pos=stimPoses[0]
                        squareStim.draw()
                    if targetShape==0:
                        circleStim.fillColor=targetColor
                        circleStim.pos=stimPoses[0]
                        circleStim.draw()
                    
#                    stimPoses.remove(stimPoses[0])
                    nStim=nStim-1
                    targetOn=1
                    
                # Distractors
                nStimList=[floor(nStim/3), round(nStim/3), ceil(nStim/3)]
                random.seed()
                random.shuffle(nStimList)
                
                if targetShape==1:
                    for curNStim in range(targetOn, targetOn+int(nStimList[0])):
                        squareStim.fillColor=distractorColor
                        squareStim.pos=stimPoses[curNStim]
                        squareStim.draw()
                        
                    for curNStim in range(targetOn + int(nStimList[0]), targetOn+int(nStimList[0])+int(nStimList[1])):
                        circleStim.fillColor=distractorColor
                        circleStim.pos=stimPoses[curNStim]
                        circleStim.draw()
                        
                    for curNStim in range(targetOn + int(nStimList[0])+int(nStimList[1]), targetOn+int(nStimList[0])+int(nStimList[1])+int(nStimList[2])):
                        circleStim.fillColor=targetColor
                        circleStim.pos=stimPoses[curNStim]
                        circleStim.draw()
                    
                if targetShape==0:
                    for curNStim in range(targetOn, targetOn+int(nStimList[0])):
                        circleStim.fillColor=distractorColor
                        circleStim.pos=stimPoses[curNStim]
                        circleStim.draw()
                        
                    for curNStim in range(targetOn + int(nStimList[0]), targetOn+int(nStimList[0])+int(nStimList[1])):
                        squareStim.fillColor=distractorColor
                        squareStim.pos=stimPoses[curNStim]
                        squareStim.draw()
                        
                    for curNStim in range(targetOn + int(nStimList[0])+int(nStimList[1]), targetOn+int(nStimList[0])+int(nStimList[1])+int(nStimList[2])):
                        squareStim.fillColor=targetColor
                        squareStim.pos=stimPoses[curNStim]
                        squareStim.draw()
                        
                drawnT=True
        win.flip()
        
        event.clearEvents()
        # Draw Stimuli
        startT=globalClock.getTime(); pressedRes=False; response=-1;
        while (globalClock.getTime() - startT <= 3) and (pressedRes==False):
            if event.getKeys(keyList=['escape']):
                core.quit()
                
            if event.getKeys(keyList=['z']):
                response=0
                pressedRes=True
            if event.getKeys(keyList=['slash']):
                response=1
                pressedRes=True
                
        responseTime=globalClock.getTime()-startT
        
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
                if (targetPresence == 0 and response == 0) or (targetPresence ==1 and response == 1):
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
                            # Instruction 9
                            instructionIdx=8
                            instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
                            instructions[instructionIdx].draw()
                        elif correctOrNot == 0:
                            # Instruction 10
                            instructionIdx=9
                            instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
                            instructions[instructionIdx].draw()
                    if response == -1:
                        # Instruction 11
                        instructionIdx=10
                        instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
                        instructions[instructionIdx].draw()
                    win.flip()
                writtenRes=True
        
        # Rest Between Blocks
        if not curTrial==-1:
            if returnNumber(expTrials[curBlock][curTrial][serialIdxLoc],restInterval)==0:
                
                event.clearEvents()
                startT=globalClock.getTime(); pressed=False; response=-1;
                while (globalClock.getTime() - startT <= restTime) and (pressed==False):
                    if event.getKeys(keyList=['escape']):
                        core.quit()
                        
                    # Instruction 12
                    instructionIdx=11
                    instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
                    instructions[instructionIdx].draw()
                    win.flip()
                    
                    if event.getKeys(keyList=['space']):
                        pressed=True
                
                event.clearEvents()
                # Instruction 13
                instructionIdx=12
                instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
                instructions[instructionIdx].draw()
                win.flip()
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

# Instruction 8
instructionIdx=7
instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
instructions[instructionIdx].draw()
win.flip()
pressedDefault=False
while pressedDefault==False:
    if event.getKeys(keyList=['escape']):
        core.quit()