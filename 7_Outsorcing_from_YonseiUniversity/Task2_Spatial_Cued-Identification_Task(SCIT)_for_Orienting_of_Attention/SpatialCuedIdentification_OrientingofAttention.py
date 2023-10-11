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
restInterval=60
restTime=30
termiValue=0.8
maxTermiValue=16

# Repetition of Main Experiment
nBlocks=20

# Presenting Times (units: second)
fixationT=1
cueT=0.1
ITI=0.1
targetT=0.1
maxResT=3
tailTPrac=1
tailTMain=0.1

# Experimental Variables
cueLocationList=[0,1] # 0: left / 1: right
targetTypeList=[0,1] # 0: circle / 1: triangle
targetLocationList=[0,1] # 0: left / 1: right

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
fixationCorssColor=[1,1,1] # units: cm

# Rectagular
squareSize=[2.9,2.2]
squareThickness=0.2 # units: cm
addedThickness=0.2 # units: cm
squareLocationFromCenter=5.2 # units: cm
squareColor=[1,1,1]

# Triangle
triangleSideLen=0.7 # units: cm
triangleThickness=0.2 # units: cm
triangleColor=[1,1,1]

# Circle
circleDiameter=0.7 # units: cm
circleThickness=0.2 # units: cm
circleColor=[1,1,1]

#===============================================
# Setup of Pop Up Window=======================
#===============================================
expName='SCIT' # practice response to clockwise & counterclockwise
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
dataFile.write('Participant_Number\t' 'Initials_of_Name\t' 'Gender\t' 'Age\t' 'SerialIdx\t' 'BlockIdx\t' 'TrialIdx\t' 'Cue_Location\t' 'Target_Type\t' 'Target_Location\t' 'Response\t' 'CorrectOrNot\t' 'ResponseTime\t' 'PracticeTrials\t' 'PracticeAccuracy\n')

#===============================================
# Make a Matrix for Experimental Design=========
#===============================================
# Main Experiment

expTrials = []; curSerialIdx=0; 
for curBlockIdx in range(nBlocks):
    curTrialIdx=0; blockTrials=[];
    for curCueLocation in cueLocationList:
        for curTargetType in targetTypeList:
            for curTargetLocation in targetLocationList:
                curSerialIdx+=1; curTrialIdx+=1;
                trial = [sbjIdx] + [intialIdx] + [genderIdx] + [ageIdx] + [curSerialIdx+1] + [curBlockIdx+1] + [curTrialIdx+1] + [curCueLocation] + [curTargetType] + [curTargetLocation]
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
cueLocationLoc = 7
targetTypeLoc = 8
targetLocationLoc = 9

serialIdx=0
for curBlock in range(nBlocks):
    trialIdx=0
    for curCueLocation in cueLocationList:
        for curTargetType in targetTypeList:
            for curTargetLocation in targetLocationList:
                serialIdx+=1
                trialIdx+=1
                
                expTrials[curBlock][trialIdx-1][serialIdxLoc]=serialIdx
                expTrials[curBlock][trialIdx-1][trialIdxLoc]=trialIdx
    
nTotalTrials=len(cueLocationList)*len(targetTypeList)*len(targetLocationList)
nRuns=nBlocks*nTotalTrials

# Practice Trials
practiceCueLocationList=[0,1]
practiceTargetTypeList=[0,1]
practiceTargetLocationList=[0,1]

practiceCueLocationLoc=0
practiceTargetTypeLoc=1
practiceTargetLocationLoc=2

nPracticeBlocks=int(ceil(nPractice/(len(practiceCueLocationList)*len(practiceTargetTypeList)*len(practiceTargetLocationList))))

practiceExpTrials = [];
for curBlockIdx in range(nPracticeBlocks):
    blockTrials=[];
    for practiceCueLocation in practiceCueLocationList:
        for practiceTargetType in practiceTargetTypeList:
            for practiceTargetLocation in practiceTargetLocationList:
                practiceTrial = [practiceCueLocation] + [practiceTargetType] + [practiceTargetLocation]
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
    
# Experimental Stimulus; Rectangular
# background rectagular
squareSize=[cm2pix(squareSize[0]),cm2pix(squareSize[1])]
squareThickness=cm2pix(squareThickness)
outerSquareCoordi = [squareSize[0]/2,squareSize[1]/2]
outerSquareVert = [[-outerSquareCoordi[0], outerSquareCoordi[1]],[outerSquareCoordi[0],outerSquareCoordi[1]],[outerSquareCoordi[0],-outerSquareCoordi[1]],[-outerSquareCoordi[0],-outerSquareCoordi[1]]]

innerSquareCoordi = [outerSquareCoordi[0] - squareThickness,outerSquareCoordi[1] - squareThickness]
innerSquareVert = [[-innerSquareCoordi[0], innerSquareCoordi[1]],[innerSquareCoordi[0],innerSquareCoordi[1]],[innerSquareCoordi[0],-innerSquareCoordi[1]],[-innerSquareCoordi[0],-innerSquareCoordi[1]]]

squareStim = visual.ShapeStim(win,
    vertices = [outerSquareVert, innerSquareVert],
    lineWidth = 0, fillColor=squareColor, closeShape=True, ori=0, units='pix')

# cue rectagular
addedThickness=cm2pix(addedThickness)
outerSquareCoordi = [(squareSize[0]/2)+(addedThickness),(squareSize[1]/2)+(addedThickness)]
outerSquareVert = [[-outerSquareCoordi[0], outerSquareCoordi[1]],[outerSquareCoordi[0],outerSquareCoordi[1]],[outerSquareCoordi[0],-outerSquareCoordi[1]],[-outerSquareCoordi[0],-outerSquareCoordi[1]]]

innerSquareCoordi = [outerSquareCoordi[0] - (squareThickness+(addedThickness/2)),outerSquareCoordi[1] - (squareThickness+(addedThickness/2))]
innerSquareVert = [[-innerSquareCoordi[0], innerSquareCoordi[1]],[innerSquareCoordi[0],innerSquareCoordi[1]],[innerSquareCoordi[0],-innerSquareCoordi[1]],[-innerSquareCoordi[0],-innerSquareCoordi[1]]]

cueSquareStim = visual.ShapeStim(win,
    vertices = [outerSquareVert, innerSquareVert],
    lineWidth = 0, fillColor=squareColor, closeShape=True, ori=0, units='pix')

# Experimental Stimulus; Triangle
triangleSideLen=cm2pix(triangleSideLen)
triangleThickness=cm2pix(triangleThickness)

outerTriangleSideLen=triangleSideLen
outerTriangleHeight=(sqrt(3)/2)*triangleSideLen
outerTriangleInradius=outerTriangleHeight/3

outerTriangleVert=[[0,outerTriangleHeight-outerTriangleInradius],[-outerTriangleSideLen/2, -outerTriangleInradius], [outerTriangleSideLen/2,-outerTriangleInradius]]

innerTriangleInradius=outerTriangleInradius-(triangleThickness/2)
innerTriangleHeight=innerTriangleInradius*3
innerTriangleSideLen=(2/sqrt(3))*innerTriangleHeight

innerTriangleVert=[[0,innerTriangleHeight-innerTriangleInradius],[-innerTriangleSideLen/2, -innerTriangleInradius], [innerTriangleSideLen/2,-innerTriangleInradius]]

triangleStim = visual.ShapeStim(win,
    vertices = [outerTriangleVert,innerTriangleVert],
    lineWidth = 0, fillColor=triangleColor, closeShape=True, ori=0, units='pix')
    
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


#=================================================================================================
#=================================================================================================
# Start Experiment================================================================================
#=================================================================================================
#=================================================================================================

stimPosList=[[-cm2pix(squareLocationFromCenter),0],[cm2pix(squareLocationFromCenter),0]]

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
                    
        # Draw Cross & Rectangulars
        fixationCross.draw()
        squareStim.pos=stimPosList[0]
        squareStim.draw()
        squareStim.pos=stimPosList[1]
        squareStim.draw()
        win.flip()
        
        startT=globalClock.getTime(); drawnT=False;
        while globalClock.getTime() - startT <= fixationT - MsPerFrame:
            if event.getKeys(keyList=['escape']):
                core.quit()
            
            if drawnT==False:
                
                fixationCross.draw()
                squareStim.pos=stimPosList[0]
                squareStim.draw()
                squareStim.pos=stimPosList[1]
                squareStim.draw()
                
                if curTrial==-1:
                    cueSquareStim.pos=stimPosList[practiceExpTrials[practiceTrial][practiceCueLocationLoc]]
                    cueSquareStim.draw()
                else:
                    cueSquareStim.pos=stimPosList[expTrials[curBlock][curTrial][cueLocationLoc]] # Loaction of Cue Lectagular
                    cueSquareStim.draw()
                drawnT=True
                
        win.flip()
        
        # Draw Cue Rectangular
        startTCue=globalClock.getTime(); drawnCue=False;
        while globalClock.getTime() - startTCue <= cueT - MsPerFrame:
            if event.getKeys(keyList=['escape']):
                core.quit()
            
            if drawnCue==False:
                
                fixationCross.draw()
                squareStim.pos=stimPosList[0]
                squareStim.draw()
                squareStim.pos=stimPosList[1]
                squareStim.draw()
                
                drawnCue=True
        
        win.flip()
        
        # ITI
        startITI=globalClock.getTime(); drawnITI=False; targetTypeIdx=-1;
        while globalClock.getTime() - startITI <= ITI - MsPerFrame:
            if event.getKeys(keyList=['escape']):
                core.quit()
            
            if drawnITI==False:
                
                fixationCross.draw()
                squareStim.pos=stimPosList[0]
                squareStim.draw()
                squareStim.pos=stimPosList[1]
                squareStim.draw()
                
                if curTrial==-1:
                    targetTypeIdx=practiceExpTrials[practiceTrial][practiceTargetTypeLoc] 
                    targetLocationIdx=practiceExpTrials[practiceTrial][practiceTargetLocationLoc]
                    
                else:
                    targetTypeIdx=expTrials[curBlock][curTrial][targetTypeLoc] 
                    targetLocationIdx=expTrials[curBlock][curTrial][targetLocationLoc]
                    
                if targetTypeIdx==0:
                    circleStim.pos=stimPosList[targetLocationIdx]
                    circleStim.draw()
                if targetTypeIdx==1:
                    triangleStim.pos=stimPosList[targetLocationIdx]
                    triangleStim.draw()
                
                drawnITI=True
        
        win.flip()
        
        # Draw Stimuli
        event.clearEvents()
        startTarget=globalClock.getTime(); response=-1;
        while globalClock.getTime() - startITI <= targetT - MsPerFrame:
            if event.getKeys(keyList=['escape']):
                core.quit()
            
            if drawnITI==False:
                
                # Instruction 14
                instructionIdx=13
                instructions[instructionIdx].size=[win.size[0]*instructionHorzRatio, win.size[0]*instructionHorzRatio*(instructionSizes[instructionIdx][1]/instructionSizes[instructionIdx][0])]
                instructions[instructionIdx].draw()
                
                drawnITI=True
                
            if event.getKeys(keyList=['z']):
                response=0
                responseTime=globalClock.getTime()-startTarget
                
            if event.getKeys(keyList=['slash']):
                response=1
                responseTime=globalClock.getTime()-startTarget
                
        win.flip()
        
        startRes=globalClock.getTime();
        # Draw Response Instruction
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
                if (targetTypeIdx == 0 and response == 0) or (targetTypeIdx ==1 and response == 1):
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