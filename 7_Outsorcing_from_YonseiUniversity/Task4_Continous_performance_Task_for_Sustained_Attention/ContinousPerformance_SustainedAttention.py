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
nPractice=4
restInterval=40
restTime=30
termiValue=0.8
maxTermiValue=8

# Repetition of Main Experiment
nBlocks=45

# Presenting Times (units: second)
fixationT=1
targetT=0.15
maxResT=3
tailTPrac=1
tailTMain=0.1

# Experimental Variables
colorMatchList=[0,1]
shapeMatchList=[0,1]

# Instruction Images
nInstruction=14
instructionList=range(nInstruction)
instructionHorzRatio=0.7

# Background Screen
backgroundColor=[-1,-1,-1]
screenNum=0

# Fixation Cross
fixationCrossSize=2 # units: cm
fixationCrossThickness=0.2 # units: cm
fixationCorssColor=[1,1,1]

# Target & Distractor Shape & Color
targetStimShape=2 # 0: square, 1: triangle, 2: circle, 3: hexagon
targetStimColor=[1/2,-1/2,-1/2] # dark red
distractorColor1=[-1/2,-1/2,1/2] # dark blue
distractorColor2=[1/2,1/2,-1/2] # dark yellow

# Mask
maskFlipLowestDuration=1#1 # units=second
maskFlipHighestDuration=5#5 # units=second
maskFlipInterval=1 # units=frame

# Square
squareSize=2 # units: cm

# Triangle
triangleSideLen=2 # units: cm

# Circle
circleDiameter=2 # units: cm

# Hexagon
hexaSize=2 # units: cm

#===============================================
# Setup of Pop Up Window=======================
#===============================================
expName='CPT' # practice response to clockwise & counterclockwise
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
dataFile.write('Participant_Number\t' 'Initials_of_Name\t' 'Gender\t' 'Age\t' 'SerialIdx\t' 'BlockIdx\t' 'TrialIdx\t' 'ColorMatch\t' 'ShapeMatch\t' 'Response\t' 'CorrectOrNot\t' 'ResponseTime\t' 'PracticeTrials\t' 'PracticeAccuracy\n')

#===============================================
# Make a Matrix for Experimental Design=========
#===============================================
# Main Experiment

expTrials = []; curSerialIdx=0; 
for curBlockIdx in range(nBlocks):
    curTrialIdx=0; blockTrials=[];
    for curColorMatch in colorMatchList:
        for curShapeMatch in shapeMatchList:
            curSerialIdx+=1; curTrialIdx+=1;
            trial = [sbjIdx] + [intialIdx] + [genderIdx] + [ageIdx] + [curSerialIdx+1] + [curBlockIdx+1] + [curTrialIdx+1] + [curColorMatch] + [curShapeMatch]
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
colorMatchLoc = 7
shapeMatchLoc = 8

serialIdx=0
for curBlock in range(nBlocks):
    trialIdx=0
    for curColorMatch in colorMatchList:
        for curShapeMatch in shapeMatchList:
            serialIdx+=1
            trialIdx+=1
            
            expTrials[curBlock][trialIdx-1][serialIdxLoc]=serialIdx
            expTrials[curBlock][trialIdx-1][trialIdxLoc]=trialIdx
    
nTotalTrials=len(colorMatchList)*len(shapeMatchList)
nRuns=nBlocks*nTotalTrials

# Practice Trials
practiceColorMatchList=[0,1]
practiceShapeMatchList=[0,1]

practiceColorMatchLoc=0
practiceShapeMatchLoc=1

nPracticeBlocks=int(ceil(nPractice/(len(practiceColorMatchList)*len(practiceShapeMatchList))))

practiceExpTrials = [];
for curBlockIdx in range(nPracticeBlocks):
    blockTrials=[];
    for curpracticeColorMatch in practiceColorMatchList:
        for practiceShapeMatch in practiceShapeMatchList:
            practiceTrial = [curpracticeColorMatch] + [practiceShapeMatch]
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
    
# Experimental Stimulus; Square
squareSize=cm2pix(squareSize)
outerSquareCoordi = squareSize/2
outerSquareVert = [[-outerSquareCoordi, outerSquareCoordi],[outerSquareCoordi,outerSquareCoordi],[outerSquareCoordi,-outerSquareCoordi],[-outerSquareCoordi,-outerSquareCoordi]]

squareStim = visual.ShapeStim(win,
    vertices = outerSquareVert,
    lineWidth = 0, fillColor=0, closeShape=True, ori=0)

# Experimental Stimulus; Triangle
triangleSideLen=cm2pix(triangleSideLen)
outerTriangleSideLen=triangleSideLen
outerTriangleHeight=(sqrt(3)/2)*triangleSideLen
outerTriangleInradius=outerTriangleHeight/3

outerTriangleVert=[[0,outerTriangleHeight-outerTriangleInradius],[-outerTriangleSideLen/2, -outerTriangleInradius], [outerTriangleSideLen/2,-outerTriangleInradius]]

triangleStim = visual.ShapeStim(win,
    vertices = outerTriangleVert,
    lineWidth = 0, fillColor=0, closeShape=True, ori=0, units='pix')
    
# Experimental Stimulus; Circle
circleDiameter=cm2pix(circleDiameter)

outerCircleRadius=circleDiameter/2
outerCircleStim = visual.Circle(win=win,
    pos=[0, 0],
    radius=outerCircleRadius, edges=1024,
    lineWidth=2, # pixel unit
    lineColor=0,
    fillColor=None)
outerCicleVert=outerCircleStim.vertices
circleStimVert = outerCicleVert

# Experimental Stimulus; Hexagon
hexaSize=cm2pix(hexaSize)
hexaCoordi=hexaSize/2
hexaMiddleCoordi=[hexaCoordi*cos(radians(60)), hexaCoordi*sin(radians(60))]

outerHexaVert=[[hexaMiddleCoordi[0],hexaMiddleCoordi[1]], [hexaCoordi,0], [hexaMiddleCoordi[0],-hexaMiddleCoordi[1]], [-hexaMiddleCoordi[0],-hexaMiddleCoordi[1]], [-hexaCoordi,0], [-hexaMiddleCoordi[0],hexaMiddleCoordi[1]]]

hexagonStim = visual.ShapeStim(win,
    vertices = outerHexaVert,
    lineWidth = 0, fillColor=0, closeShape=True, ori=0, units='pix')

# Temporary Stimulus
temStim= visual.ShapeStim(win,
    vertices = outerHexaVert,
    lineWidth = 0, fillColor=0, closeShape=True, ori=0, units='pix')

# Color & Shape Pool
totalStimColorPool=[targetStimColor,distractorColor1,distractorColor2] # dark red, dark blue, dark yellow

stimVertPool = [circleStimVert, outerSquareVert, outerTriangleVert, outerHexaVert] # square, triangle, circle, hexagon
circleLoc=0; squareLoc=1; triangleLoc=2; hexagonLoc=3;
stimColorPool = totalStimColorPool # red, blue, yellow
redLoc=0; blueLoc=1; yellowLoc=2;

# Target Colors & Shapes
if targetStimShape==0:
    targetStimShape=outerSquareVert
elif targetStimShape==1:
    targetStimShape=outerTriangleVert
elif targetStimShape==2:
    targetStimShape=outerCicleVert
elif targetStimShape==3:
    targetStimShape=outerHexaVert

# Distractor Colors & Shapes
distractorStimShapePool=[circleStimVert, outerSquareVert, outerTriangleVert, outerHexaVert]
distractorStimShapePool.remove(targetStimShape)

distractorStimColorPool=[targetStimColor,distractorColor1,distractorColor2] # dark red, dark blue, dark yellow
distractorStimColorPool.remove(targetStimColor)
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
                
                targetIdx=0
                
                if curTrial==-1:
                        
                    if practiceExpTrials[practiceTrial][practiceColorMatchLoc]==1 and practiceExpTrials[practiceTrial][practiceShapeMatchLoc]==1:
                        temStim.fillColor = targetStimColor
                        temStim.vertices = targetStimShape
                        targetIdx=1
                        
                    if practiceExpTrials[practiceTrial][practiceColorMatchLoc]==1 and practiceExpTrials[practiceTrial][practiceShapeMatchLoc]==0:
                        random.seed()
                        random.shuffle(distractorStimShapePool)
                        
                        temStim.fillColor = targetStimColor
                        temStim.vertices = distractorStimShapePool[0]
                        
                    if practiceExpTrials[practiceTrial][practiceColorMatchLoc]==0 and practiceExpTrials[practiceTrial][practiceShapeMatchLoc]==1:
                        random.seed()
                        random.shuffle(distractorStimColorPool)
                        
                        temStim.fillColor = distractorStimColorPool[0]
                        temStim.vertices = targetStimShape
                        
                    if practiceExpTrials[practiceTrial][practiceColorMatchLoc]==0 and practiceExpTrials[practiceTrial][practiceShapeMatchLoc]==0:
                        random.seed()
                        random.shuffle(distractorStimShapePool)
                        
                        random.seed()
                        random.shuffle(distractorStimColorPool)
                        
                        temStim.fillColor = distractorStimColorPool[0]
                        temStim.vertices = distractorStimShapePool[0]
                        
                    
                else:
                    
                    if expTrials[curBlock][curTrial][colorMatchLoc]==1 and expTrials[curBlock][curTrial][shapeMatchLoc]==1:
                        temStim.fillColor = targetStimColor
                        temStim.vertices = targetStimShape
                        targetIdx=1
                        
                    if expTrials[curBlock][curTrial][colorMatchLoc]==1 and expTrials[curBlock][curTrial][shapeMatchLoc]==0:
                        random.seed()
                        random.shuffle(distractorStimShapePool)
                        
                        temStim.fillColor = targetStimColor
                        temStim.vertices = distractorStimShapePool[0]
                        
                    if expTrials[curBlock][curTrial][colorMatchLoc]==0 and expTrials[curBlock][curTrial][shapeMatchLoc]==1:
                        random.seed()
                        random.shuffle(distractorStimColorPool)
                        
                        temStim.fillColor = distractorStimColorPool[0]
                        temStim.vertices = targetStimShape
                        
                    if expTrials[curBlock][curTrial][colorMatchLoc]==0 and expTrials[curBlock][curTrial][shapeMatchLoc]==0:
                        random.seed()
                        random.shuffle(distractorStimShapePool)
                        
                        random.seed()
                        random.shuffle(distractorStimColorPool)
                        
                        temStim.fillColor = distractorStimColorPool[0]
                        temStim.vertices = distractorStimShapePool[0]
                
                temStim.draw()
                drawnT=True
                
        win.flip()
        
        # Draw Target Stimuli
        event.clearEvents()
        startTarget=globalClock.getTime(); response=-1; drawnT=False;
        while globalClock.getTime() - startTarget <= targetT - MsPerFrame:
            if event.getKeys(keyList=['escape']):
                core.quit()
            
            if drawnT == False and curTrial==-1:
                
                # Instruction 14
                instructionIdx=13
                instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
                instructions[instructionIdx].draw()
                
                drawnT = True
            
            if event.getKeys(keyList=['z']):
                response=0
                responseTime=globalClock.getTime()-startTarget
                
            if event.getKeys(keyList=['slash']):
                response=1
                responseTime=globalClock.getTime()-startTarget
        
        win.flip()
        
        # Draw Response Screen
        startRes=globalClock.getTime();
        while (globalClock.getTime() - startRes <= maxResT) and (response==-1):
            
            if event.getKeys(keyList=['escape']):
                core.quit()
                
            if event.getKeys(keyList=['z']):
                response=0
                responseTime=globalClock.getTime()-startTarget
                
            if event.getKeys(keyList=['slash']):
                response=1
                responseTime=globalClock.getTime()-startTarget
                
        if response==-1:
            responseTime=globalClock.getTime()-startTarget
            # ITI & Wirting Responses
            win.flip()
        
        # ITI & Wirting Responses
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
                if (targetIdx == 1 and response == 1) or (targetIdx == 0 and response == 0):
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
        
        # Draw Mask
        startTarget=globalClock.getTime(); pressedRes=False; response=-1;
        
        maskT=range(int(maskFlipLowestDuration*10),int((maskFlipHighestDuration*10)+1))
        maskT=[maskT/10 for maskT in maskT ]
        random.seed()
        random.shuffle(maskT)
        maskT=maskT[0]
        
        nMaskFlip=-1
        while (globalClock.getTime() - startTarget <= maskT):
            if event.getKeys(keyList=['escape']):
                core.quit()
                
            nMaskFlip+=1
            flipT=returnNumber(nMaskFlip,maskFlipInterval+1)
            
            if flipT==0:
                random.seed()
                random.shuffle(stimVertPool)
                
                random.seed()
                random.shuffle(stimColorPool)
                
            temStim.fillColor = stimColorPool[0]
            temStim.vertices = stimVertPool[0]
            
            temStim.draw()
            win.flip()
        
        # Rest Between Blocks
        if not curTrial==-1:
            if returnNumber(expTrials[curBlock][curTrial][serialIdxLoc],restInterval)==0:
                
                event.clearEvents()
                startBlock=globalClock.getTime(); pressed=False; response=-1;
                while (globalClock.getTime() - startBlock <= restTime) and (pressed==False):
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