#========================
# Load Libraries=========
#========================
from __future__ import division #so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, misc, logging, gui, monitors
from psychopy.visual import filters
from psychopy.constants import * #things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, pre-pend 'np.'
import copy
from numpy import *
from psychopy.iohub import launchHubServer
import os #handy system and path functions
import math
from psychopy.hardware.emulator import launchScan
import random
import time
from decimal import Decimal
from StringIO import StringIO
from PIL import Image # Get the size(demension) of an image
def returnNumber(inputNumber, returnUnit):
    return inputNumber - (np.floor(inputNumber/returnUnit)*returnUnit)
def isOdd(inputNumber):
    return np.ceil(float(inputNumber)/2-floor(float(inputNumber)/2))

#=================================================
# Ready For Keyboard Response=====================
#=================================================
io = launchHubServer()
keyboard = io.devices.keyboard

#==============================================
#==============================================
# Experiment Version===========================
#==============================================
#==============================================
expVersion = 3 # 0: practice, 1: measuring orienation bias, 2: measuring tilt illusion during binocular rivalry, 3: measuring tilt illusion during interocular grouping
targetPresentationType=0 # 0: two stimuli, different, 1: two stimuli, same, 2: one stimulus, 3: one stimulus without rivalry


#==============================================
# Common Parameters============================
#==============================================
screenNum=1;
backgroundColor=[127.5, 127.5, 127.5];
nInstr=4; # number of instrument scenes

sameORdifferentOrientationList=[1] # among gratings, 0: same-no rivalry, 1: same-rivalry, 2: different-no rivalry, 3: different-rivalry
stimSizeList=[100];#[120];
stimTypeList=[0];
targetGratingOrientatioinChangeList=[-2, -1, -0.5, 0, 0.5, 1, 2]; # orientation variation of target grating
sizeRatioValue=1.7 # size differences among gratings (standard: middle, +-middlesize/sizeRatioValue)

fixationWidth=5; fixationLength=30; fixDist=70; fixationLengthCen=30; # fixation cross setting

lineOris=[0,90] # fixation line setting
lineSizes=[fixationWidth+5,fixationLength*2] # fixation line setting

# target grating default orientations
gratingOrientationSmallL=90
gratingOrientationSmallR=0

mixedEdgeSize=8 # size of gray border between small target grating and middle surround
movingUnit=0.5 # unit when moving fixation & grating
NmatchingLetina=6 # number of matching scenes
frameForAppear=50 # appear or disappear speed calculated by frame

#=====================================================================
# Exp 0. Practice Responses to Clockwise & Counterclockwise===========
#=====================================================================
if expVersion==0:
    whichEyeList=[0, 1]; # 0: left, 1: right / target
    whichEyeFixationList=[0, 1] # 0: direct / 1: switched before 2017.10.20 17:00~
    whichEyeFixationList=[0, 1, 2, 3] # 
    effectDirectionList=[1]; # 0: small orientation difference with adjacent stim, 1: big orientation difference with adjacent stim
    stimOrientationDifferenceList=[60]; # 45+-60/2 & 240/2
    
#    targetGratingOrientatioinChangeList=[-6 -3, -1.5, 1.5, 3, 6];
#    targetGratingOrientatioinChangeList=[-12, -9, -6,-3];
#    targetGratingOrientatioinChangeList=[-6, -3, 3, 6];
    targetGratingOrientatioinChangeList=[-0.5,0.5];
#    targetGratingOrientatioinChangeList=[-0.3,0.3];
#    targetGratingOrientatioinChangeList=[-0.5, -0.3, 0.3, 0.5];
#    targetGratingOrientatioinChangeList=[0];
    
    nBlocks=2; # before 2017.10.17 ~
    nBlocks=2; # from 2017.10.17 ~
    resTime=10;
#    resTime=1000;
#    resTime=1;
    restBetwBlock=60 # before 2017.10.17 ~
    restBetwBlock=2 # from 2017.10.17 ~
    restSeqInterval = 4
    
#===============================================
# Exp 2a. Measuring Orientation Bias============
#===============================================
elif expVersion==1: 
    whichEyeList=[0,1]; # 0: left, 1: right / target
    whichEyeFixationList=[0, 1] # 0: direct / 1: switched before 2017.10.20 17:00~
    whichEyeFixationList=[0, 1, 2, 3]
    effectDirectionList=[1]; # 0: small orientation difference with adjacent stim, 1: big orientation difference with adjacent stim
    stimOrientationDifferenceList=[60]; # 45+-60/2 & 240/2
    
    nBlocks=3; # before 2017.10.17 ~
    nBlocks=5; # from 2017.10.17 ~
    nBlocks=2; # from 2017.10.20 17:00~
    resTime=10;
    restBetwBlock=60 # before 2017.10.17 ~
    restBetwBlock=20 # from 2017.10.17 ~
    restSeqInterval=20 # from 2017.10.17 ~
    
#=======================================================================
# Exp 2b. Measuring Tilt Illusion During Binocular Rivlary==============
#=======================================================================
elif expVersion==2:
    whichEyeList=[0,1]; # 0: left, 1: right / target
    whichEyeFixationList=[0, 1] # 0: direct / 1: switched before 2017.10.20 17:00~
    whichEyeFixationList=[0, 1, 2, 3]
    effectDirectionList=[0,1]; # 0: small orientation difference with adjacent stim, 1: big orientation difference with adjacent stim
#    effectDirectionList=[1]; # 0: small orientation difference with adjacent stim, 1: big orientation difference with adjacent stim
    stimOrientationDifferenceList=[60,120]; # 45+-60/2 & 240/2
    
    nBlocks=2;
    nBlocks=1; # from 2017.10.20 17:00~
    resTime=10;
    restBetwBlock=60 # before 2017.10.17 ~
    restBetwBlock=20 # from 2017.10.17 ~
    restSeqInterval=20 # from 2017.10.17 ~
    
#=========================================================================
# Exp 3. Measuring Tilt Illusion During Interocular Grouping==============
#=========================================================================
elif expVersion==3:
    sameORdifferentOrientationList=[3] # among gratings, 0: same-no rivalry, 1: same-rivalry, 2: different-no rivalry, 3: different-rivalry
    whichEyeList=[0,1]; # 0: left, 1: right / target
    whichEyeFixationList=[0, 1] # 0: direct / 1: switched before 2017.10.20 17:00~
    whichEyeFixationList=[0, 1, 2, 3]
    effectDirectionList=[0,1]; # 0: small orientation difference with adjacent stim, 1: big orientation difference with adjacent stim
#    effectDirectionList=[1]; # 0: small orientation difference with adjacent stim, 1: big orientation difference with adjacent stim
    stimOrientationDifferenceList=[60,120]; # 45+-60/2 & 240/2
    
    nBlocks=2;
    nBlocks=1; # from 2017.10.20 17:00~
    resTime=10;
    restBetwBlock=60 # before 2017.10.17 ~
    restBetwBlock=20 # from 2017.10.17 ~
    restSeqInterval=20 # from 2017.10.17 ~

#============================================================
# adjust parameters for screen capture of stimuli============
#============================================================
#sameORdifferentOrientationList=[3]
#whichEyeList=[0,1]; # 0: left, 1: right / target
#targetGratingOrientatioinChangeList=[-0.5,0.5];
#effectDirectionList=[0,1]
#whichEyeFixationList=[0,1,2,3]
#stimOrientationDifferenceList=[60,120]
#resTime=3

#=======================================================================
# Adjust The Parameters For Applying Types Of Presenting Stimuli========
#=======================================================================
pixelsForPushTheRightOusideOfMonitor=0
indexForLocateTheLeftToCenter=1
if targetPresentationType==0:
    targetGratingOrinetationList=[-1]
elif targetPresentationType==1:
    targetGratingOrinetationList=[gratingOrientationSmallL, gratingOrientationSmallR]
    whichEyeList=[0]
elif targetPresentationType==2:
    targetGratingOrinetationList=[gratingOrientationSmallL, gratingOrientationSmallR]
elif targetPresentationType==3:
    targetGratingOrinetationList=[-1]
    indexForLocateTheLeftToCenter=0
    pixelsForPushTheRightOusideOfMonitor=100000

indexForLocateTheLeftToCenter
pixelsForPushTheRightOusideOfMonitor

drawAllTarget=True
if targetPresentationType==2:
    drawAllTarget=False

#==============================================
# Records Of Parameters In Past Experiments====
#==============================================
# in experiment 13th of sep, 19:00
# nblocks=3
# restTime=10

#===============================================
# Setup For Pop Up Window=======================
#===============================================
# exp 1a & 1b: measuring orientation bias & tilt illusion without binocular rivalry
if expVersion==0:
    expName='exp0_orientation_bias_practice' # practice response to clockwise & counterclockwise
elif expVersion==1:
    expName='exp2a_orientation_bias' # measuring orientation bias
elif expVersion==2:
    expName='exp2b_tilt_illusion' # measuring tilt illusion during binocular rivalry
elif expVersion==3:
    expName='exp3_tilt_illusion' # measuring tilt illusion during binocular rivalry

expInfo={'participant':'00'}
dlg=gui.DlgFromDict(dictionary=expInfo,title=expName)
if dlg.OK==False: core.quit() #user pressed cancel
expInfo['date']=data.getDateStr()#add a simple timestamp
expInfo['expName']=expName

#==========================================================
# Open Text File For Writing Data==========================
#==========================================================
if not os.path.isdir('data'):
    os.makedirs('data') #if this fails (e.g. permissions) we will get error
# determine detail name according to experiment version
if expVersion==1:
    detailName = '_forChecingOrientationBias_duringBR'
elif expVersion==2:
    detailName = '_during_binocular_rivalry'
elif expVersion==3:
    detailName = '_during_interocular_grouping'
elif expVersion==0:
    detailName = '_practice'
fileName='data' + os.path.sep + '%s_%s_%s' %(expName, expInfo['participant'], expInfo['date']) + detailName
# open data file & write the tilt of values
dataFileTilt = open(fileName+'.txt', 'w')
if expVersion==3:
    dataFileTilt.write('sbj\t' 'serial\t' 'BlockIdx\t' 'TrialIdx\t' 'whichEye\t' 'WichEyeFixation\t' 'targetGratingOrientatioin\t' 'targetGratingOrientatioinChange\t' 'effectDirection\t' 'midoutSameOri\t' 'stimSize\t' 'stimOrientationDifference\t' 'tiltResVert\t' 'tiltResHorz\t' 'resVertList\t' 'resHorzList\t' 'resList\t' 'perceiveGroupingVert\t' 'perceiveGroupingHorz\n')
else:
    dataFileTilt.write('sbj\t' 'serial\t' 'BlockIdx\t' 'TrialIdx\t' 'whichEye\t' 'WichEyeFixation\t' 'targetGratingOrientatioin\t' 'targetGratingOrientatioinChange\t' 'effectDirection\t' 'midoutSameOri\t' 'stimSize\t' 'stimOrientationDifference\t' 'tiltResVert\t' 'tiltResHorz\t' 'resVertList\t' 'resHorzList\t' 'resList\n')

sbjIdx = int(expInfo['participant']);
print 'Subject Number='+str(sbjIdx)
#===========================================
#===========================================
# Set Parameters For Stimuli================
#===========================================
#===========================================

#======================
# Grating==============
#======================
arraySize=int(1024/4)
custumGrating = np.zeros([arraySize,arraySize,3]) #the f indicates we want floats 
custumGratingMixed = np.zeros([arraySize,arraySize,3]) #the f indicates we want floats 

custumGratingType='sin'
custumGratingFilterCycle=(filters.makeGrating(gratType=custumGratingType, res=arraySize, cycles=1, phase=0, contr=1)/7)
custumGratingFilterColorDifference=0.5255/2

#================================
# Background Patterned Patch=====
#================================
fieldsize=[np.max(stimSizeList)+(np.max(stimSizeList)/2)+50, np.max(stimSizeList)+(np.max(stimSizeList)/2)+50];
Npatches=[30, 30]#[100, 100] # [The number according to Width, Height]

patchElementTex='sqr'
patchElementMask='sqr'
patchElementtexRes=48
patchFieldPos=[0,0]
patchFieldShape='sqr'

patchSize=[fieldsize[0]/Npatches[0], fieldsize[1]/Npatches[1]] # [The number according to Width, Height]
patchLocUnit=[patchSize[0], patchSize[1]] # [The unit according to Width, Height]

#=======================================
# Gratings Locateion====================
#=======================================
#starting_loc=1300; # iMac
#starting_loc=900; # 144 Hz monitor
starting_loc=400;
#starting_loc=450;
gratingPoses=[[-starting_loc, 0], [starting_loc, 0]]
gratingPoses=[[-starting_loc*indexForLocateTheLeftToCenter, 0], [starting_loc+pixelsForPushTheRightOusideOfMonitor, 0]]

#if targetPresentationType==3:
#    gratingPoses=[[0, 0], [10000, 0]]

#======================================
# Gratings Size========================
#======================================
#gratingSizeBig=300
#gratingSizeMiddle=150
#gratingSizeSmall=50
gratingSizeBig=150
gratingSizeMiddle=100
gratingSizeSmall=50

#======================================
# Gratings Orientation=================
#======================================
#gratingOrientationBigL=45
#gratingOrientationBigR=135
gratingOrientationBigL=70#-10 #95 #120
gratingOrientationBigR=20#-10 #5 #170
#gratingOrientationBigL=120
#gratingOrientationBigR=170
#gratingOrientationMiddleL=0 #160
#gratingOrientationMiddleR=90 #110
gratingOrientationMiddleL=gratingOrientationBigR#+10
gratingOrientationMiddleR=gratingOrientationBigL#+10
#gratingOrientationSmallL=90
#gratingOrientationSmallR=0
gratingOrientationSmallL_default=gratingOrientationSmallL
gratingOrientationSmallR_default=gratingOrientationSmallR

gratingOrientations=[[gratingOrientationBigL,gratingOrientationMiddleL,gratingOrientationSmallL],[gratingOrientationBigR,gratingOrientationMiddleL,gratingOrientationSmallR]]

#=======================================================================
# Gratings Spatial Frequency, Constrast, Opacity========================
#=======================================================================
spatialfrequencyValue = 13.
spatialfrequencyValueBigL = spatialfrequencyValue#6.
spatialfrequencyValueBigR = spatialfrequencyValue#10.
spatialfrequencyValueMiddleL = spatialfrequencyValueBigR
spatialfrequencyValueMiddleR = spatialfrequencyValueBigL
spatialfrequencyValueSmallL = spatialfrequencyValueBigL
spatialfrequencyValueSmallR = spatialfrequencyValueBigR
contrastValue = 1# 0.7
opacityValue = 1
#overlapsValue = 1
additionalLinesWidth=10

#=========================================================
# Fixation Grating========================================
#=========================================================
#fixationGratingSize=gratingSizeBig
#fixationGratingSizeL=50
#fixationGratingSizeR=100
#fixationGratingSizeOrientation=0
fixationGratingSizeL=30
fixationGratingSizeR=60
fixationGratingSizeOrientation=0

#=======================================================
# Gratings Color========================================
#=======================================================
custumGrating[:,:,0] = custumGratingFilterCycle + custumGratingFilterColorDifference
custumGrating[:,:,1] = -custumGratingFilterCycle + custumGratingFilterColorDifference
custumGrating[:,:,2] = -1

custumGratingMixed[:,:,0] = custumGratingFilterCycle + custumGratingFilterColorDifference
custumGratingMixed[:,:,1] = custumGratingFilterCycle + custumGratingFilterColorDifference
custumGratingMixed[:,:,2] = -1

custumGratingFixationGratingL = np.zeros([arraySize,arraySize,3]) #the f indicates we want floats 

custumGratingFixationGratingL[:,:,0] = custumGratingFilterCycle + custumGratingFilterColorDifference
custumGratingFixationGratingL[:,:,1] = -custumGratingFilterCycle + custumGratingFilterColorDifference
custumGratingFixationGratingL[:,:,2] = -1

custumGratingFixationGratingR = np.zeros([arraySize,arraySize,3]) #the f indicates we want floats 

custumGratingFixationGratingR[:,:,0] = custumGratingFilterCycle + custumGratingFilterColorDifference/2
custumGratingFixationGratingR[:,:,1] = -1
custumGratingFixationGratingR[:,:,2] = -custumGratingFilterCycle + custumGratingFilterColorDifference/2

#=========================================
# Gratings Mask===========================
#=========================================
#maskType='circle'
#maskType='gauss'
maskType='raisedCos'
maskParamsValue={'fringeWidth':0.05}

#===========================================
# FixationCross=============================
#===========================================
#fixationColor='green';
#fixationWidth=6; fixationLength=10; fixDist=100;
#fixationColor=[((+((1/5)+0.5255)/1) + (-((1/5)-0.5255)/1)) / 2, ((+((1/5)+0.5255)/1) + (-((1/5)-0.5255)/1)) / 2, -1];
fixationColor=[-1,-1,-1] # black
fixationCenPoses=[[-starting_loc,0], [starting_loc,0]]
fixationCenPoses=[[-starting_loc*indexForLocateTheLeftToCenter,0], [starting_loc*indexForLocateTheLeftToCenter,0]]
indexForLocateTheLeftToCenter
pixelsForPushTheRightOusideOfMonitor
#if targetPresentationType==3:
#    fixationCenPoses=[[0, 0], [0, 0]]
fixationCrossOrientationL=180; fixationCrossOrientationR=0;

#=======================================================
# Fixation Circle=======================================
#=======================================================
fixationCircleSize=3#7#3
#fixationCircleColor=[-1,-1,-1]
fixationCircleColor=[1,1,1]

#====================================================================
# Experimental Design================================================
#====================================================================
expTrials = []; thisSerial=0; 
for thisBlock in range(nBlocks):
    thisTrial=0; blockTrials=[];
    for thisWhichEye in whichEyeList:
        for thisWichEyeFixation in whichEyeFixationList:
            for targetGratingOrinetation in targetGratingOrinetationList:
                for thisTargetGratingOrientatioinChange in targetGratingOrientatioinChangeList:
                    for thisEffectDirection in effectDirectionList:
                        for thisStimSize in stimSizeList:
                            for thisStimOrientationDifference in stimOrientationDifferenceList:
                                for thisSameORdifferentOrientation in sameORdifferentOrientationList:
                                    thisSerial+=1; thisTrial+=1;
                                    trial = [sbjIdx] + [thisSerial] + [thisBlock] + [thisTrial] + [thisWhichEye] + [thisWichEyeFixation] + [targetGratingOrinetation] + [thisTargetGratingOrientatioinChange] + [thisEffectDirection] + [thisSameORdifferentOrientation] + [thisStimSize] + [thisStimOrientationDifference]
                                    blockTrials.append(trial)
    np.random.seed()
    np.random.shuffle(blockTrials)
    expTrials.append(blockTrials)

sbjIdx=0
serialLoc=1
blockLoc=2
trialLoc=3
whichEyeLoc=4
whichEyeFixationLoc=5
targetGratingOrientationLoc=6
targetGratingOrientatioinChangeLoc=7
effectDirectionLoc=8
sameORdifferentOrientationLoc=9
stimSizeLoc=10
stimOrientationDifferenceLoc=11

nTotalTrials=len(whichEyeList)*len(whichEyeFixationList)*len(targetGratingOrinetationList)*len(targetGratingOrientatioinChangeList)*len(effectDirectionList)*len(stimTypeList)*len(stimSizeList)*len(stimOrientationDifferenceList) * len(sameORdifferentOrientationList)
print 'Total Number Of Sequences='+str(nTotalTrials*nBlocks)

thisSerial=0;
for thisBlock in range(nBlocks):
    for thisTrial in range(nTotalTrials):
        thisSerial+=1;
        expTrials[thisBlock][thisTrial][serialLoc]=thisSerial
        expTrials[thisBlock][thisTrial][blockLoc]=thisBlock+1
        expTrials[thisBlock][thisTrial][trialLoc]=thisTrial+1

#====================================================================
# Get Monitor Information============================================
#====================================================================
monSize=[1920,1080]
mon = monitors.Monitor('customSetting')#fetch the most recent calib for this monitor
mon.setDistance(114) #further away than normal?
mon.setSizePix(monSize)
mon.setWidth(50)

if screenNum == 0:
#    win = visual.Window(allowGUI=True, colorSpace= "rgb255", color = backgroundColor, fullscr = True, screen = screenNum, monitor='Main', units='deg', multiSample=False, numSamples=64, useRetina=True)
    win = visual.Window(allowGUI=True, colorSpace= "rgb255", color = backgroundColor, fullscr = True, screen = screenNum, monitor='Main', units='deg',waitBlanking=False)
    
elif screenNum == 1:
#    win = visual.Window(allowGUI=True, colorSpace= "rgb255", color = backgroundColor, fullscr = True, screen = screenNum, monitor='Extended', units='deg', waitBlanking=True, multiSample=False, numSamples=64, useRetina=True)
    win = visual.Window(allowGUI=False, colorSpace= "rgb255", color = backgroundColor, fullscr = True, screen = screenNum, monitor='default', units='deg', waitBlanking=False)
MsPerFrame = win.getMsPerFrame(nFrames=120)
MsPerFrame = MsPerFrame[0]/1000

#====================================================================
#====================================================================
# Stimuli Ready======================================================
#====================================================================
#====================================================================

#====================================================================
# Text Stimuli=======================================================
#====================================================================
textStim=visual.TextStim(win,
    text='defualt, you can change the text by code text.text',
    height=30, pos=[0,0], color=[-1,-1,-1], font='Arial', colorSpace='rgb', ori=0, wrapWidth=None, opacity=1, depth=0.0, units='pix')

#====================================================================
# Gratings===========================================================
#====================================================================
gratingStimLS_mixed = visual.GratingStim(
    win=win,
    units = "pix",
    size = [gratingSizeSmall+10, gratingSizeSmall+10],
    tex = 'sin',
#    tex = custumGrating,
#    tex = custumGratingMixed,
    
    mask = maskType,
#    sf = spatialfrequencyValueBigL / gratingSizeBig, # SpatialFrequency
    sf = 0, # SpatialFrequency
    ori = gratingOrientationBigL, # orientation
    contrast = 1,
    phase = 0,
    maskParams = maskParamsValue,
    opacity = opacityValue,
    colorSpace = 'rgb',
    color=[0,0,0],
    interpolate=True,
    pos = gratingPoses[0])
    
gratingStimRS_mixed = visual.GratingStim(
    win=win,
    units = "pix",
    size = [gratingSizeSmall+10, gratingSizeSmall+10],
    tex = 'sin',
#    tex = custumGrating,
#    tex = custumGratingMixed,
    
    mask = maskType,
#    sf = spatialfrequencyValueBigL / gratingSizeBig, # SpatialFrequency
    sf = 0, # SpatialFrequency
    ori = gratingOrientationBigL, # orientation
    contrast = 1,
    phase = 0,
    maskParams = maskParamsValue,
    opacity = opacityValue,
    colorSpace = 'rgb',
    color=[0,0,0],
    interpolate=True,
    pos = gratingPoses[1])
    

gratingStimLB = visual.GratingStim(
    win=win,
    units = "pix",
    size = [gratingSizeBig, gratingSizeBig],
    tex = 'sin',
#    tex = custumGrating,
#    tex = custumGratingMixed,
    
    mask = maskType,
#    sf = spatialfrequencyValueBigL / gratingSizeBig, # SpatialFrequency
    sf = 0, # SpatialFrequency
    ori = gratingOrientationBigL, # orientation
    contrast = contrastValue,
    phase = 0,
    maskParams = maskParamsValue,
    opacity = opacityValue,
    #    colorSpace = 'rgb255',
    #    color='green',
    interpolate=True,
    pos = gratingPoses[0])

gratingStimLM = visual.GratingStim(
    win=win,
    units = "pix",
    size = [gratingSizeMiddle, gratingSizeMiddle],
    tex = 'sin',
#    tex = custumGrating,
    mask = maskType,
    sf = spatialfrequencyValueMiddleL / gratingSizeMiddle, # SpatialFrequency
    ori = gratingOrientationMiddleL, # orientation
    contrast = contrastValue,
    phase = 0,
    maskParams = maskParamsValue,
    opacity = opacityValue,
    #    colorSpace = 'rgb255',
    #    color='green',
    interpolate=True,
    pos = gratingPoses[0])

gratingStimLS = visual.GratingStim(
    win=win,
    units = "pix",
    size = [gratingSizeSmall, gratingSizeSmall],
#    tex = 'sqr',
    tex = 'sin',
#    tex = custumGrating,
    mask = maskType,
    sf = spatialfrequencyValue / gratingSizeSmall, # SpatialFrequency
    ori = gratingOrientationSmallL, # orientation
    contrast = contrastValue,
    phase = 0,
    maskParams = maskParamsValue,
    opacity = opacityValue,
    #    colorSpace = 'rgb255',
    #    color='green',
    interpolate=True,
    pos = gratingPoses[0])
    
gratingStimRB = visual.GratingStim(
    win=win,
    units = "pix",
    size = [gratingSizeBig, gratingSizeBig],
    tex = 'sin',
#    tex = custumGrating,
#    tex = custumGratingMixed,
    mask = maskType,
    sf = spatialfrequencyValueBigR / gratingSizeBig, # SpatialFrequency
#    sf=0,
    ori = gratingOrientationBigR, # orientation
    contrast = contrastValue,
    phase = 0,
    maskParams = maskParamsValue,
    opacity = opacityValue,
    #    colorSpace = 'rgb255',
    #    color='green',
    interpolate=True,
    pos = gratingPoses[1])

gratingStimRM = visual.GratingStim(
    win=win,
    units = "pix",
    size = [gratingSizeMiddle, gratingSizeMiddle],
    tex = 'sin',
#    tex = custumGrating,
    mask = maskType,
    sf = spatialfrequencyValueMiddleR / gratingSizeMiddle, # SpatialFrequency
    ori = gratingOrientationMiddleR, # orientation
    contrast = contrastValue,
    phase = 0,
    maskParams = maskParamsValue,
    opacity = opacityValue,
    #    colorSpace = 'rgb255',
    #    color='green',
    interpolate=True,
    pos = gratingPoses[1])

gratingStimRS = visual.GratingStim(
    win=win,
    units = "pix",
    size = [gratingSizeSmall, gratingSizeSmall],
#    tex = 'sqr',
    tex = 'sin',
#    tex = custumGrating,
    mask = maskType,
    sf = spatialfrequencyValue / gratingSizeSmall, # SpatialFrequency
    ori = gratingOrientationSmallR, # orientation
    contrast = contrastValue,
    phase = 0,
    maskParams = maskParamsValue,
    opacity = opacityValue,
    #    colorSpace = 'rgb255',
    #    color='green',
    interpolate=True,
    pos = gratingPoses[1])
gratingStims=[[gratingStimLB, gratingStimLM, gratingStimLS_mixed, gratingStimLS],[gratingStimRB, gratingStimRM, gratingStimRS_mixed, gratingStimRS]]

#gratingStimRB.ori = 0
#gratingStimRB.draw()
#win.flip()
#event.waitKeys()
#core.quit()

#=============================================
# Lines Between Gratings (For Flipping Exp)===
#=============================================
vertices=[]
radius=gratingSizeBig/2
sf=spatialfrequencyValue
nElements=sf*2
for thisnElements in range(int(nElements)):
    Xcoordinate=-radius+(radius/sf)*thisnElements; Ycoordinate=0;
    thisVertice=[Xcoordinate*np.cos(np.radians(gratingOrientationBigL)) + Ycoordinate*np.sin(np.radians(gratingOrientationBigL)),
        -Xcoordinate*np.sin(np.radians(gratingOrientationBigL)) + Ycoordinate*np.cos(np.radians(gratingOrientationBigL))] # equation of roation of axes
    vertices.append(thisVertice)

globForm = visual.ElementArrayStim(win,
    nElements=len(vertices), xys=vertices,
    sizes=[additionalLinesWidth,radius*4], oris=gratingOrientationBigL,
    elementTex='sqr',
    elementMask='sqr',
    colors=[((+((1/5)+0.5255)/1) + (-((1/5)-0.5255)/1)) / 2, ((+((1/5)+0.5255)/1) + (-((1/5)-0.5255)/1)) / 2, -1],
#    colors=[1, -1, -1],
    colorSpace='rgb',
    interpolate=True,
    sfs=0,
    units='pix')

globFormCounterDegree = visual.ElementArrayStim(win,
    nElements=len(vertices), xys=vertices,
    sizes=[additionalLinesWidth,radius*4], oris=180-gratingOrientationBigL,
    elementTex='sqr',
    elementMask='sqr',
    colors=[((+((1/5)+0.5255)/1) + (-((1/5)-0.5255)/1)) / 2, ((+((1/5)+0.5255)/1) + (-((1/5)-0.5255)/1)) / 2, -1],
#    colors=[1, -1, -1],
    colorSpace='rgb',
    interpolate=True,
    sfs=0,
    units='pix')

#====================================================================
# Background Patch Stimuli===========================================
#====================================================================
xys=[]; patchColors=[];
for thisPatchY in range(Npatches[1]):
    for thisPatchX in range(Npatches[0]):
#        patchColorR=(np.random.rand(1,1)[0][0]*2)-1; # -1 ~ 1 random number
        patchColorR=((np.around(np.random.rand(1,1)[0][0],decimals=0))*2)-1; # black & white
        patchColorG=patchColorR#(np.random.rand(1,1)[0][0]*2)-1;
        patchColorB=patchColorR#(np.random.rand(1,1)[0][0]*2)-1;
        patchColors.append([patchColorR, patchColorG, patchColorB])
        xys.append([-(fieldsize[0]/2)+(patchLocUnit[0]/2)+(patchLocUnit[0]*thisPatchX), -(fieldsize[1]/2)+(patchLocUnit[1]/2)+(patchLocUnit[1]*thisPatchY)])
        

if patchElementMask=='sqr':
#    isSqr=win.size[0]/win.size[1]
    isSqr=2
else:
    isSqr=1

patchGlobFormL = visual.ElementArrayStim(win,
    nElements=Npatches[0]*Npatches[1],
    sizes=[patchSize[0]*isSqr,patchSize[1]], 
    elementTex=patchElementTex, elementMask=patchElementMask,
    fieldPos=patchFieldPos, fieldShape=patchFieldShape,
    sfs=0, xys=xys, colors=patchColors, colorSpace='rgb', units='pix')
patchGlobFormR = visual.ElementArrayStim(win,
    nElements=Npatches[0]*Npatches[1],
    sizes=[patchSize[0]*isSqr,patchSize[1]], 
    elementTex=patchElementTex, elementMask=patchElementMask,
    fieldPos=patchFieldPos, fieldShape=patchFieldShape,
    sfs=0, xys=xys, colors=patchColors, colorSpace='rgb', units='pix')

#=============================================
# Fixation Cross==============================
#=============================================
fixationCrossOrientation=0

fixationCrossOrientation=0; fixationLength=50
def fixationCrossPos(fixationCenPosX, fixationCenPosY, fixationLength, fixationCrossOrientation):
    fixationCrossCoordinates=[];
    fixationCrossCoordinatesVertHorz=[[fixationCenPosX, fixationCenPosY+fixationLength],
#        [fixationCenPosX, fixationCenPosY-fixationLength],
        [fixationCenPosX, fixationCenPosY],
        [fixationCenPosX-fixationLength,fixationCenPosY],
        [fixationCenPosX+fixationLength, fixationCenPosY]]
    for thisCoodi in range(len(fixationCrossCoordinatesVertHorz)):
        XfixationCoodinateWithAngle = fixationCenPosX + ((fixationCrossCoordinatesVertHorz[thisCoodi][0]-fixationCenPosX)*np.cos(np.radians(fixationCrossOrientation))) - (fixationCrossCoordinatesVertHorz[thisCoodi][1]-fixationCenPosY)*np.sin(np.radians(fixationCrossOrientation))
        YfixationCoodinateWithAngle = fixationCenPosY + ((fixationCrossCoordinatesVertHorz[thisCoodi][0]-fixationCenPosX)*np.sin(np.radians(fixationCrossOrientation))) + (fixationCrossCoordinatesVertHorz[thisCoodi][1]-fixationCenPosY)*np.cos(np.radians(fixationCrossOrientation))
        fixationCrossCoordinates.append([XfixationCoodinateWithAngle, YfixationCoodinateWithAngle])
#    fixationCrossCoordinates[2]=[fixationCenPosX, fixationCenPosY]
    return fixationCrossCoordinates

fixationCross = visual.ShapeStim(win, vertices=fixationCrossPos(100,50,fixationLength, fixationCrossOrientation), lineWidth=fixationWidth, lineColor=fixationColor, units='pix', closeShape=False,
    ori=0,
    interpolate=True) # cross shape fixation

#=============================================
# Simple Rectagnular Background===============
#=============================================
backgroundRectVert = [[-win.size[0]/2, -win.size[1]/2], [-win.size[0]/2, +win.size[1]/2], [+win.size[0]/2, +win.size[1]/2], [+win.size[0]/2, -win.size[1]/2]]
backgroundRect = visual.ShapeStim(win, vertices=backgroundRectVert, lineWidth=0, fillColor=backgroundColor, units='pix', fillColorSpace='rgb255')

#====================================================================
# Fixation Circles===================================================
#====================================================================
fixationCircle = visual.Circle(win=win,
    pos=[0, 0],
    radius=fixationCircleSize, edges=10000,
    lineColor=fixationCircleColor,
    fillColor=fixationCircleColor,
    fillColorSpace='rgb',
    lineColorSpace='rgb',
    interpolate=True,
    units='pix')
fixationCircleL = visual.Circle(win=win,
    pos=[0, 0],
    radius=fixationCircleSize, edges=10000,
    lineColor=fixationCircleColor,
    fillColor=fixationCircleColor,
    fillColorSpace='rgb',
    lineColorSpace='rgb',
    interpolate=True,
    units='pix')
fixationCircleR = visual.Circle(win=win,
    pos=[0, 0],
    radius=fixationCircleSize, edges=10000,
    lineColor=fixationCircleColor,
    fillColor=fixationCircleColor,
    fillColorSpace='rgb',
    lineColorSpace='rgb',
    interpolate=True,
    units='pix')

#=============================================
# Instruction Images Ready====================
#=============================================
InstructionPath = os.getcwd() + '/Instruction/'
instructions = []
for thisInstr in range(1, nInstr+1):
    subInstrImgName = InstructionPath + 'Instruction' + str(thisInstr) + '.png'
    subInstrImg=visual.ImageStim(win, image=subInstrImgName, pos=(0,0), mask = 'none', units='pix', interpolate=True)
    instructions.append(subInstrImg)
instructions[1].setPos([0,300])


#=============================================
# Show Instruction Before The Experiment======
#=============================================
instructions[0].pos=gratingPoses[0]
instructions[0].draw()
instructions[0].pos=gratingPoses[1]
instructions[0].draw()
win.flip()
#event.waitKeys(['space'])
keyboard.waitForPresses(keys=[' '])
keyboard.waitForReleases(keys=[' '])

#=========================================================================================================================================================================================================================================
#=========================================================================================================================================================================================================================================
# Experiment Starts!======================================================================================================================================================================================================================
#=========================================================================================================================================================================================================================================
#=========================================================================================================================================================================================================================================


#==============================================================
# Defalt Parameters For Experiment Loop========================
#==============================================================
presentGratings=True; presentTargetGrating=0; presentFixation=0; presentCenFixation=1; flipGratings=0; flipNum=0; drawMiddle=True; presentLeftTarget=False; presentRighftTarget=False;
movingDirec=0; imageLorR=0; moveToXorY=0; movingDirec=0; imgKey=1; drawCross=True; switchGratingPos=0; adjustment=True; matchingLetina=0;
loopNumber = 0; resDuration=-1; resTilt=-1; drawBig=True; whichEyeFixationIdx=0;

#==========================================================================================
# Experimental Blocks & Instructions & Before-Trial Matching Task Start====================
#==========================================================================================
for curBlock in range(nBlocks):
    if curBlock==0: # instructions & matching scene
        loopList=list(repeat(0,NmatchingLetina)) + range(nTotalTrials)
    elif curBlock>0: # actual experimental trials
        loopList=range(nTotalTrials)
    
    #==========================================================================================
    # Experimental Trials & Instructions & Before-Trial Matching Task Start====================
    #==========================================================================================
    for curTrial in loopList: # total trials + loops for instructions & matching scene before actual trials
        
        resTiltVert=-1; resTiltHorz=-1; perceiveGrouping=-1;# default response recording without actual reponse
        matchingLetina+=1 # index for before-trial matching task
        
        
        if matchingLetina>NmatchingLetina:
            loopNumber+=1;
        elif matchingLetina==1:
            switchFixationPos=expTrials[curBlock][curTrial][whichEyeFixationLoc]
            switchGratingPos=expTrials[curBlock][curTrial][whichEyeLoc]
            loopNumber=1;
        else:
            loopNumber=1;
        
        #===================================
        # Show Instruction==================
        #===================================
        if loopNumber==2:
            instructions[2].pos=gratingPoses[0]
            instructions[2].draw()
            instructions[2].pos=gratingPoses[1]
            instructions[2].draw()
            win.flip()
#            event.waitKeys(['sapce'])
            keyboard.waitForPresses(keys=[' '])
            keyboard.waitForReleases(keys=[' '])
        
        #============================================================================
        # Set Parameters For Stimuli According To Experimental Conditions============
        #============================================================================
        if matchingLetina>NmatchingLetina:
            # whichEyeList
            switchGratingPos=expTrials[curBlock][curTrial][whichEyeLoc]
            
            # targetGratingOrientationList
            if targetPresentationType==0:
                gratingOrientationSmallL = gratingOrientationSmallL_default
                gratingOrientationSmallR = gratingOrientationSmallR_default
            elif targetPresentationType==1:
                gratingOrientationSmallL = expTrials[curBlock][curTrial][targetGratingOrientationLoc]
                gratingOrientationSmallR = expTrials[curBlock][curTrial][targetGratingOrientationLoc]
            elif targetPresentationType==2:
                gratingOrientationSmallL = expTrials[curBlock][curTrial][targetGratingOrientationLoc]
                gratingOrientationSmallR = expTrials[curBlock][curTrial][targetGratingOrientationLoc]
                
                drawAllTarget = False;
            # targetGratingOrientatioinChangeList
#            gratingOrientationSmallL=gratingOrientationSmallL_default
#            gratingOrientationSmallR=gratingOrientationSmallR_default
            gratingOrientationSmallL+=expTrials[curBlock][curTrial][targetGratingOrientatioinChangeLoc]
            gratingOrientationSmallR+=expTrials[curBlock][curTrial][targetGratingOrientatioinChangeLoc]
            
            # whichEyeFixationLoc
            whichEyeFixationIdx=expTrials[curBlock][curTrial][whichEyeFixationLoc]
            if whichEyeFixationIdx in [1, 3]:
                switchFixationPos=1;
            elif whichEyeFixationIdx in [0, 2]:
                switchFixationPos=0;
            
    #        if whichFixationPos==1:
    #            
    #            tmpfixationCenPoses=[fixationCenPoses[1], fixationCenPoses[0]]
    #            fixationCenPoses=tmpfixationCenPoses
                
            # stimSizeList
            gratingSizeMiddle=expTrials[curBlock][curTrial][stimSizeLoc]
            sizeRatio=gratingSizeMiddle/(sizeRatioValue) # 1.7
            gratingSizeBig=gratingSizeMiddle+(sizeRatio)
            gratingSizeSmall=gratingSizeMiddle-(sizeRatio)
    
            # stimOrientationDifferenceList
            gratingOrientationBigL= 45 + (expTrials[curBlock][curTrial][stimOrientationDifferenceLoc]/2) + (expTrials[curBlock][curTrial][targetGratingOrientatioinChangeLoc]) #70#-10 #95 #120
            gratingOrientationBigR= 45 - (expTrials[curBlock][curTrial][stimOrientationDifferenceLoc]/2) + (expTrials[curBlock][curTrial][targetGratingOrientatioinChangeLoc]) #20#-10 #5 #170
            gratingOrientationMiddleL=gratingOrientationBigR#+10
            gratingOrientationMiddleR=gratingOrientationBigL#+10
#            print 'gratingOrientationSmallL='+str(gratingOrientationSmallL), '/', 'gratingOrientationBigL='+str(gratingOrientationBigL), '/', 'BigL-SmallL='+str(gratingOrientationBigL-gratingOrientationSmallL), '//', 'gratingOrientationSmallR='+str(gratingOrientationSmallR), '/', 'gratingOrientationBigR='+str(gratingOrientationBigR), '/', 'BigR-SmallR='+str(gratingOrientationBigR-gratingOrientationSmallR),
            
            # effectDirectionList
            GratingOris = [[gratingOrientationBigL, gratingOrientationBigR], [gratingOrientationMiddleL, gratingOrientationMiddleR]]
            if expTrials[curBlock][curTrial][effectDirectionLoc] == 0:
                gratingOrientationBigL = GratingOris[0][0]
                gratingOrientationBigR = GratingOris[0][1]
                gratingOrientationMiddleL = GratingOris[1][0]
                gratingOrientationMiddleR = GratingOris[1][1]
                
    
            if expTrials[curBlock][curTrial][effectDirectionLoc] == 1:
                gratingOrientationBigL = GratingOris[1][0]
                gratingOrientationBigR = GratingOris[1][1]
                gratingOrientationMiddleL = GratingOris[0][0]
                gratingOrientationMiddleR = GratingOris[0][1]
                
            
            # sameORdifferentOrientationLoc
            if expTrials[curBlock][curTrial][sameORdifferentOrientationLoc]==0: # same-no rivalry
                gratingOrientationBigR=gratingOrientationBigL
                gratingOrientationMiddleL=gratingOrientationBigL
                gratingOrientationMiddleR=gratingOrientationBigR
            elif expTrials[curBlock][curTrial][sameORdifferentOrientationLoc]==1: # same-rivalry
                gratingOrientationMiddleL=gratingOrientationBigL
                gratingOrientationMiddleR=gratingOrientationBigR
                
            elif expTrials[curBlock][curTrial][sameORdifferentOrientationLoc]==2: # different-no rivalry
                gratingOrientationBigL=gratingOrientationBigR
                gratingOrientationMiddleL=gratingOrientationMiddleR
            elif expTrials[curBlock][curTrial][sameORdifferentOrientationLoc]==3: # different-rivalry
                gratingOrientationBigL=gratingOrientationMiddleR
                gratingOrientationBigR=gratingOrientationMiddleL
                
            gratingOrientations=[[gratingOrientationBigL,gratingOrientationMiddleL,gratingOrientationSmallL],[gratingOrientationBigR,gratingOrientationMiddleR,gratingOrientationSmallR]]
        
        #==================================================
        # Default Parameters For Showing Stimuli===========
        #==================================================
        adjustment=True; appearSlow=True; disappearSlow=False; disappearSlow2=False; adjustmentNumber=0; plusadjustmentNumber=True;
        resDurationActivation=False; restInfo=True;
         
        vertResList=[]
        horzResList=[]
        resList=[]
        
        drawRes=True
        
        feedback=False;
        if expVersion==0:
            feedback=True
            
        getSubjectPerception=False;
        if expVersion==3:
            getSubjectPerception=True
#            
#        drawnFixation=False
        recordResponseToTextFile = False;
        
        #==================================================
        # Show Stimuli=====================================
        #==================================================
        while adjustment==True:
#            # for stim & code sync check
#            if loopNumber>1:
#                text='trial='+str(expTrials[curBlock][curTrial][trialLoc])+'/StimType='+ str(expTrials[curBlock][curTrial][sameORdifferentOrientationLoc]) + '/whichEye=' + str(expTrials[curBlock][curTrial][whichEyeLoc]) + '/targetGratingOrientatioinChange=' + str(expTrials[curBlock][curTrial][targetGratingOrientatioinChangeLoc]) + '/effectDirection=' + str(expTrials[curBlock][curTrial][effectDirectionLoc]) + '/stimSize=' + str(expTrials[curBlock][curTrial][stimSizeLoc]) +'/stimOrientationDifference=' + str(expTrials[curBlock][curTrial][stimOrientationDifferenceLoc])
#                textStim.text=text
#                textStim.pos=(0,win.size[1]/2.2)
            
            if loopNumber==1:
                instructions[1].pos=[gratingPoses[0][0], gratingPoses[0][1]+(fieldsize[1]/2)+50]
                instructions[1].draw()
                instructions[1].pos=[gratingPoses[1][0], gratingPoses[1][1]+(fieldsize[1]/2)+50]
                instructions[1].draw()
                
            moving=False
            
            #===================================================
            # Refresh Parameters For Stimuli====================
            #===================================================
            gratingStimLS_mixed.pos=gratingPoses[0];
            gratingStimRS_mixed.pos=gratingPoses[1];
            gratingStimLS_mixed.size = gratingSizeSmall+mixedEdgeSize
            gratingStimRS_mixed.size = gratingSizeSmall+mixedEdgeSize
            
            gratingStimLB.pos=pos = gratingPoses[0];
            gratingStimLB.mask = maskType;
            gratingStimLB.sf = spatialfrequencyValueBigL / gratingSizeBig;
            if expVersion in [1, 0]:
                gratingStimLB.sf = 0;
            gratingStimLB.ori = gratingOrientationBigL;
            gratingStimLB.contrast = contrastValue;
            gratingStimLB.opacity = opacityValue;
            gratingStimLB.size = gratingSizeBig;
            
            gratingStimRB.pos=pos = gratingPoses[1];
            gratingStimRB.mask = maskType;
            gratingStimRB.sf = spatialfrequencyValueBigR / gratingSizeBig;
            if expVersion in [1, 0]:
                gratingStimRB.sf = 0;
            gratingStimRB.ori = gratingOrientationBigR;
            gratingStimRB.contrast = contrastValue;
            gratingStimRB.opacity = opacityValue;
            gratingStimRB.size = gratingSizeBig;
            
            gratingStimLM.pos=pos = gratingPoses[0];
            gratingStimLM.mask = maskType;
            gratingStimLM.sf = spatialfrequencyValueMiddleL / gratingSizeBig;
            gratingStimLM.ori = gratingOrientationMiddleL;
            gratingStimLM.contrast = contrastValue;
            gratingStimLM.opacity = opacityValue;
            gratingStimLM.size = gratingSizeMiddle;
            if expVersion in [1, 0]:
                gratingStimLM.sf = 0;
            
            gratingStimRM.pos=pos = gratingPoses[1];
            gratingStimRM.mask = maskType;
            gratingStimRM.sf = spatialfrequencyValueMiddleR / gratingSizeBig;
            gratingStimRM.ori = gratingOrientationMiddleR;
            gratingStimRM.contrast = contrastValue;
            gratingStimRM.opacity = opacityValue;
            gratingStimRM.size = gratingSizeMiddle;
            if expVersion in [1, 0]:
                gratingStimRM.sf = 0;
            
            gratingStimLS.pos=pos = gratingPoses[0];
            gratingStimLS.mask = maskType;
            gratingStimLS.sf = spatialfrequencyValueSmallL / gratingSizeBig;
            gratingStimLS.ori = gratingOrientationSmallL;
            gratingStimLS.contrast = contrastValue;
            gratingStimLS.opacity = opacityValue;
            gratingStimLS.size = gratingSizeSmall;
            
            gratingStimRS.pos=pos = gratingPoses[1];
            gratingStimRS.mask = maskType;
            gratingStimRS.sf = spatialfrequencyValueSmallR / gratingSizeBig;
            gratingStimRS.ori = gratingOrientationSmallR;
            gratingStimRS.contrast = contrastValue;
            gratingStimRS.opacity = opacityValue;
            gratingStimRS.size = gratingSizeSmall;
            
            spatialfrequencyValueBigL = spatialfrequencyValue#6.
            spatialfrequencyValueBigR = spatialfrequencyValue#10.
            spatialfrequencyValueMiddleL = spatialfrequencyValueBigR
            spatialfrequencyValueMiddleR = spatialfrequencyValueBigL
            
            gratingStims=[[gratingStimLB, gratingStimLM, gratingStimLS_mixed, gratingStimLS],[gratingStimRB, gratingStimRM, gratingStimRS_mixed, gratingStimRS]]
            
            #==================================================
            # Set The Keys For Response========================
            #==================================================
            pressedkeys=keyboard.state.keys() # keyboard.state: function -> check current keyboard state, needed of key press & .keys(): function -> get the key info of keyboard.state
            
            if pressedkeys in [['escape']]:
                print time
                win.close()
                core.quit()
                break
                
            elif set(pressedkeys) == set(['lshift', 'left']):
                imageLorR=0
                moveToXorY=0
                movingDirec=-1
                moving=True
            elif set(pressedkeys) == set(['lshift', 'right']):
                imageLorR=0
                moveToXorY=0
                movingDirec=+1
                moving=True
            elif set(pressedkeys) == set(['lshift', 'up']):
                imageLorR=0
                moveToXorY=1
                movingDirec=+1
                moving=True
            elif set(pressedkeys) == set(['lshift', 'down']):
                imageLorR=0
                moveToXorY=1
                movingDirec=-1
                moving=True
            elif set(pressedkeys) == set(['z', 'left']):
                imageLorR=1
                moveToXorY=0
                movingDirec=-movingUnit
                moving=True
            elif set(pressedkeys) == set(['z', 'right']):
                imageLorR=1
                moveToXorY=0
                movingDirec=+1
                moving=True
            elif set(pressedkeys) == set(['z', 'up']):
                imageLorR=1
                moveToXorY=1
                movingDirec=+1
                moving=True
            elif set(pressedkeys) == set(['z', 'down']):
                imageLorR=1
                moveToXorY=1
                movingDirec=-1
                moving=True
            
            #===================================================
            # Refreshing The Position of Stimuli================
            #===================================================
            # reflecting moving locations of fixation & gratings
            if (presentGratings==True and moving==True) or (isOdd(presentCenFixation)==1 and moving==True):
                gratingPoses[imageLorR][moveToXorY]+=(movingUnit*movingDirec)
            if isOdd(presentFixation)==1 and moving==True:
                fixationCenPoses[imageLorR][moveToXorY]+=(movingUnit*movingDirec)
            
            # refreshing locations of fixation & background patterns
            fixationCircleL.setPos(gratingPoses[0])
            fixationCircleR.setPos(gratingPoses[1])
            patchGlobFormL.setFieldPos(gratingPoses[0])
            patchGlobFormR.setFieldPos(gratingPoses[1])
            
            # reflecting switching info to fixation location
            fixationPosL=int(isOdd(switchFixationPos+0))
            fixationPosR=int(isOdd(switchFixationPos+1))
            
            additionalOri=0
            if whichEyeFixationIdx in [2, 3]:
                additionalOri=90
            
            fixationCrossOrientation=fixationCrossOrientationL+additionalOri
            fixationCrossCenL = visual.ShapeStim(win, vertices=fixationCrossPos(0,0,fixationLengthCen, fixationCrossOrientation), lineWidth=fixationWidth, lineColor=fixationColor, units='pix', closeShape=False,
                ori=0, interpolate=True) # cross shape fixation
            fixationCrossCenL.setPos(fixationCrossPos(fixationCenPoses[fixationPosL][0], fixationCenPoses[fixationPosL][1], fixationLengthCen, fixationCrossOrientation))
            
            fixationCrossOrientation=fixationCrossOrientationR+additionalOri
            fixationCrossCenR = visual.ShapeStim(win, vertices=fixationCrossPos(0,0,fixationLengthCen, fixationCrossOrientation), lineWidth=fixationWidth, lineColor=fixationColor, units='pix', closeShape=False,
                ori=0, interpolate=True) # cross shape fixation
            fixationCrossCenR.setPos(fixationCrossPos(fixationCenPoses[fixationPosR][0], fixationCenPoses[fixationPosR][1], fixationLengthCen, fixationCrossOrientation))
            
            #==============================================================================
            # Default Background Stimuli===================================================
            #==============================================================================
            # patterned background
            patchGlobFormL.draw()
            patchGlobFormR.draw()
            
            for LR in range(2): # left or right
                for BMS in range(4): # big, middle, gray circle, small
                    gratingStims[LR][BMS].contrast=0 # set contrast of gratings to zero for between-trials matching scene
                    gratingStims[LR][BMS].setPos(gratingPoses[int(isOdd(switchGratingPos+LR))]) # applying condition of switching position of stimuli
                    gratingStims[LR][BMS].draw()
            
            #===========================================
            # Show Before-Trials Matching Stimuli=======
            #===========================================
            if matchingLetina<=NmatchingLetina:
                        
                if matchingLetina==1:
                    distFromFix=lineSizes[1]/2
                    
                    swithIdx1=int(isOdd(switchFixationPos+1))
                    swithIdx2=int(isOdd(switchFixationPos+0))
                    
                    lineVerticesL=np.array([[fixationCenPoses[fixationPosL][0]+(distFromFix*swithIdx2),fixationCenPoses[fixationPosL][1]+(distFromFix*swithIdx1)]])
                    lineVerticesR=np.array([[fixationCenPoses[fixationPosR][0]-(distFromFix*swithIdx2),fixationCenPoses[fixationPosR][1]-(distFromFix*swithIdx1)]])
                    
                    linesL = visual.ElementArrayStim(win, xys=lineVerticesL, oris=lineOris[int(isOdd(switchFixationPos+0))], sizes=lineSizes, nElements=len(lineVerticesL), elementMask='sqr', sfs=0, colors=[-1, -1, -1], units='pix')
                    linesR = visual.ElementArrayStim(win, xys=lineVerticesR, oris=lineOris[int(isOdd(switchFixationPos+0))], sizes=lineSizes, nElements=len(lineVerticesR), elementMask='sqr', sfs=0, colors=[-1, -1, -1], units='pix')
                    
                    linesL.draw()
                    linesR.draw()
                    
                    fixationCircleL.draw()
                    fixationCircleR.draw()
                    
                    win.flip()
                    
                if matchingLetina==2:
                    distFromFix=lineSizes[1]/2
                    
                    swithIdx1=int(isOdd(switchFixationPos+1))
                    swithIdx2=int(isOdd(switchFixationPos+0))
                    
                    lineVerticesL=np.array([[fixationCenPoses[fixationPosL][0]+(distFromFix*swithIdx1),fixationCenPoses[fixationPosL][1]+(distFromFix*swithIdx2)]])
                    lineVerticesR=np.array([[fixationCenPoses[fixationPosR][0]-(distFromFix*swithIdx1),fixationCenPoses[fixationPosR][1]-(distFromFix*swithIdx2)]])
                    
                    linesL = visual.ElementArrayStim(win, xys=lineVerticesL, oris=lineOris[int(isOdd(switchFixationPos+0))], sizes=lineSizes, nElements=len(lineVerticesL), elementMask='sqr', sfs=0, colors=[-1, -1, -1], units='pix')
                    linesR = visual.ElementArrayStim(win, xys=lineVerticesR, oris=lineOris[int(isOdd(switchFixationPos+0))], sizes=lineSizes, nElements=len(lineVerticesR), elementMask='sqr', sfs=0, colors=[-1, -1, -1], units='pix')
                    
                    linesL.oris=lineOris[int(isOdd(switchFixationPos+1))]
                    linesR.oris=lineOris[int(isOdd(switchFixationPos+1))]
                    
                    linesL.draw()
                    linesR.draw()
                    
                    fixationCircleL.draw()
                    fixationCircleR.draw()
                    
                    win.flip()
                    
                if matchingLetina==3:
                    fixationCrossCenL.draw()
                    fixationCrossCenR.draw()
                    
                    switchFixationPosMatching=int(isOdd(switchFixationPos+1))
                    
                    fixationCircleL.draw()
                    fixationCircleR.draw()
                    
                    win.flip()
                
                if matchingLetina==4:
                    fixationPosL=int(isOdd(switchFixationPos+1))
                    fixationPosR=int(isOdd(switchFixationPos+0))
                    
                    fixationCrossOrientation=fixationCrossOrientationL
                    fixationCrossCenL = visual.ShapeStim(win, vertices=fixationCrossPos(0,0,fixationLengthCen, fixationCrossOrientation), lineWidth=fixationWidth, lineColor=fixationColor, units='pix', closeShape=False,
                        ori=0, interpolate=True) # cross shape fixation
                    fixationCrossCenL.setPos(fixationCrossPos(fixationCenPoses[fixationPosL][0], fixationCenPoses[fixationPosL][1], fixationLengthCen, fixationCrossOrientation))
                    
                    fixationCrossOrientation=fixationCrossOrientationR
                    fixationCrossCenR = visual.ShapeStim(win, vertices=fixationCrossPos(0,0,fixationLengthCen, fixationCrossOrientation), lineWidth=fixationWidth, lineColor=fixationColor, units='pix', closeShape=False,
                        ori=0, interpolate=True) # cross shape fixation
                    fixationCrossCenR.setPos(fixationCrossPos(fixationCenPoses[fixationPosR][0], fixationCenPoses[fixationPosR][1], fixationLengthCen, fixationCrossOrientation))
                    
                    fixationCrossCenL.draw()
                    fixationCrossCenR.draw()
                    
                    fixationCircleL.draw()
                    fixationCircleR.draw()
                    
                    win.flip()
                    
                if matchingLetina==5:
                    fixationPosL=int(isOdd(switchFixationPos+1))
                    fixationPosR=int(isOdd(switchFixationPos+0))
                    
                    fixationCrossOrientation=fixationCrossOrientationL+90;
                    fixationCrossCenL = visual.ShapeStim(win, vertices=fixationCrossPos(0,0,fixationLengthCen, fixationCrossOrientation), lineWidth=fixationWidth, lineColor=fixationColor, units='pix', closeShape=False,
                        ori=0, interpolate=True) # cross shape fixation
                    fixationCrossCenL.setPos(fixationCrossPos(fixationCenPoses[fixationPosL][0], fixationCenPoses[fixationPosL][1], fixationLengthCen, fixationCrossOrientation))
                    
                    fixationCrossOrientation=fixationCrossOrientationR+90;
                    fixationCrossCenR = visual.ShapeStim(win, vertices=fixationCrossPos(0,0,fixationLengthCen, fixationCrossOrientation), lineWidth=fixationWidth, lineColor=fixationColor, units='pix', closeShape=False,
                        ori=0, interpolate=True) # cross shape fixation
                    fixationCrossCenR.setPos(fixationCrossPos(fixationCenPoses[fixationPosR][0], fixationCenPoses[fixationPosR][1], fixationLengthCen, fixationCrossOrientation))
                    
                    fixationCrossCenL.draw()
                    fixationCrossCenR.draw()
                    
                    fixationCircleL.draw()
                    fixationCircleR.draw()
                    
                    win.flip()
                    
                if matchingLetina==6:
                    fixationPosL=int(isOdd(switchFixationPos+1))
                    fixationPosR=int(isOdd(switchFixationPos+0))
                    
                    fixationCrossOrientation=fixationCrossOrientationL+270;
                    fixationCrossCenL = visual.ShapeStim(win, vertices=fixationCrossPos(0,0,fixationLengthCen, fixationCrossOrientation), lineWidth=fixationWidth, lineColor=fixationColor, units='pix', closeShape=False,
                        ori=0, interpolate=True) # cross shape fixation
                    fixationCrossCenL.setPos(fixationCrossPos(fixationCenPoses[fixationPosL][0], fixationCenPoses[fixationPosL][1], fixationLengthCen, fixationCrossOrientation))
                    
                    fixationCrossOrientation=fixationCrossOrientationR+270;
                    fixationCrossCenR = visual.ShapeStim(win, vertices=fixationCrossPos(0,0,fixationLengthCen, fixationCrossOrientation), lineWidth=fixationWidth, lineColor=fixationColor, units='pix', closeShape=False,
                        ori=0, interpolate=True) # cross shape fixation
                    fixationCrossCenR.setPos(fixationCrossPos(fixationCenPoses[fixationPosR][0], fixationCenPoses[fixationPosR][1], fixationLengthCen, fixationCrossOrientation))
                    
                    fixationCrossCenL.draw()
                    fixationCrossCenR.draw()
                    
                    fixationCircleL.draw()
                    fixationCircleR.draw()
                    
                    win.flip()
                    
            if (expVersion==3) and (isOdd(adjustmentNumber)==0):
                drawnFixation=True
                    
            #======================================================
            # Show Appearing Main Stimuli==========================
            #======================================================
            if loopNumber>1 and appearSlow==True and isOdd(adjustmentNumber)==0:
                fixationCircleL.fillColor=[-1,-1,-1]
                fixationCircleL.lineColor=[-1,-1,-1]
                fixationCircleR.fillColor=[-1,-1,-1]
                fixationCircleR.lineColor=[-1,-1,-1]
#                    win.clearBuffer()
                for LR in range(2): # left or right
                    for BMS in range(4): # big, middle, small
                        gratingStims[LR][BMS].contrast=0
                for i in range(int(frameForAppear*contrastValue)):
                    patchGlobFormL.draw()
                    patchGlobFormR.draw()
                    for LR in range(2): # left or right
                        for BMS in range(4): # 0: big, 1: middle, 2: intercircle, 3: small
#                            textStim.draw() # for checking experimental condition sync
                            if expVersion in [1, 0]: # orientation bias or practice
                                if drawAllTarget==True:
                                    gratingStims[LR][2].contrast=((i+1)/frameForAppear)
                                    gratingStims[LR][3].contrast=((i+1)/frameForAppear)
                                    gratingStims[LR][BMS].draw()
                                elif drawAllTarget==False:
                                    gratingStims[LR][2].contrast=((i+1)/frameForAppear)
                                    gratingStims[LR][3].contrast=((i+1)/frameForAppear)
                                    gratingStims[LR][0].draw()
                                    gratingStims[LR][1].draw()
                                    gratingStims[LR][2].draw()
                                    gratingStims[switchFixationPos][3].draw()
                            elif expVersion in [2, 3]: # tilt illusion
                                gratingStims[LR][BMS].contrast=((i+1)/frameForAppear)
                                gratingStims[LR][BMS].draw()
                    fixationCircleL.draw()
                    fixationCircleR.draw()
                    win.flip()
                appearSlow=False
                disappearSlow=True
                fixationCircleL.fillColor=[1,1,1]
                fixationCircleL.lineColor=[1,1,1]
                fixationCircleR.fillColor=[1,1,1]
                fixationCircleR.lineColor=[1,1,1]
            #======================================================
            # Show Disappearing Main Stimuli=======================
            #======================================================
            elif loopNumber>1 and disappearSlow==True and isOdd(adjustmentNumber)==1:
                fixationCircleL.fillColor=[-1,-1,-1]
                fixationCircleL.lineColor=[-1,-1,-1]
                fixationCircleR.fillColor=[-1,-1,-1]
                fixationCircleR.lineColor=[-1,-1,-1]
                switchValue=expTrials[curBlock][curTrial][whichEyeLoc]
                
                fixationCrossCenL.opacity=0
                fixationCrossCenR.opacity=0
                for LR in range(2): # left or right
                    for BMS in [2]: # big, middle, small
                        gratingStims[LR][BMS].contrast=1
                for i in range(int(frameForAppear*contrastValue)):
                    patchGlobFormL.draw()
                    patchGlobFormR.draw()
                    for LR in range(2): # left or right
                        for BMS in range(4): # big, middle, small
                            gratingStims[LR][BMS].pos=gratingPoses[int(isOdd(LR+switchValue))]
#                            textStim.draw() # for checking experimental condition sync
                            if expVersion in [1, 0]: # orientation bias or practice
                                gratingStims[LR][2].contrast=((frameForAppear-i-1)/frameForAppear)
                                gratingStims[LR][3].contrast=((frameForAppear-i-1)/frameForAppear)
                                gratingStims[LR][BMS].draw()
                            elif expVersion in [2, 3]: # tilt illusion
                                gratingStims[LR][BMS].contrast=((frameForAppear-i-1)/frameForAppear)
                                gratingStims[LR][BMS].draw()
                        
                    fixationCrossCenL.opacity=((i+1)/frameForAppear)
                    fixationCrossCenR.opacity=((i+1)/frameForAppear)
                    fixationCrossCenL.draw()
                    fixationCrossCenR.draw()
                        
                    fixationCircleL.fillColor=[1,1,1]
                    fixationCircleL.lineColor=[1,1,1]
                    fixationCircleR.fillColor=[1,1,1]
                    fixationCircleR.lineColor=[1,1,1]
                    
                    fixationCircleL.draw()
                    fixationCircleR.draw()
                    
                    win.flip()
                    
                disappearSlow=False
                disappearSlow2=True
                
                if not expVersion in [0,3]:
                    print 'sequence='+str(expTrials[curBlock][curTrial][serialLoc])+'/'+str(nTotalTrials * nBlocks), '||', 'block='+str(expTrials[curBlock][curTrial][blockLoc]),'trial='+str(expTrials[curBlock][curTrial][trialLoc]),'||', 'oriChange='+str(expTrials[curBlock][curTrial][targetGratingOrientatioinChangeLoc]), '||','resTiltVert='+str(resTiltVert), 'resTiltHorz='+str(resTiltHorz), '||', 'whicheye='+str(expTrials[curBlock][curTrial][whichEyeLoc]), 'whichEyeFixation='+str(expTrials[curBlock][curTrial][whichEyeFixationLoc]), 'effectDirection='+str(expTrials[curBlock][curTrial][effectDirectionLoc])
            
            elif loopNumber>1 and isOdd(adjustmentNumber)==1 and disappearSlow==False and matchingLetina>NmatchingLetina:
                #======================================================
                # Show Result Of Responses When Practice Version=======
                #======================================================
                if feedback==True:
                    correctOrNotVert = 0
                    correctOrNotHorz = 0
                    curOriChange = expTrials[curBlock][curTrial][targetGratingOrientatioinChangeLoc]
                    
                    # calculate accuracy
                    if curOriChange < 0:
                        correctResVert=0
                        correctResHorz=2
                        
                        if resTiltVert==0:
                            correctOrNotVert = 1
                        if resTiltHorz==2:
                            correctOrNotHorz = 1
                        
                    if curOriChange > 0:
                        correctResVert=1
                        correctResHorz=3
                        
                        if resTiltVert==1:
                            correctOrNotVert = 1
                        if resTiltHorz==3:
                            correctOrNotHorz = 1
                    
                    textResVert='In Vetrical: Wrong!'
                    textResHorz='In Horizontal: Wrong!'
                    if correctOrNotVert ==1:
                        textResVert='In Vetrical: Correct!'
                    if correctOrNotHorz == 1:
                        textResHorz='In Horizontal: Correct!'
                    
                    backgroundRect.draw()
                    textStim.text=textResVert+'\n'+textResHorz
                    textStim.pos=gratingPoses[0]
                    textStim.draw()
                    textStim.pos=gratingPoses[1]
                    textStim.draw()
                    win.flip()
                    
                    core.wait(2)
                    feedback=False
                    
                    print 'sequence='+str(expTrials[curBlock][curTrial][serialLoc])+'/'+str(nTotalTrials * nBlocks), '||', 'block='+str(expTrials[curBlock][curTrial][blockLoc]),'trial='+str(expTrials[curBlock][curTrial][trialLoc]),'||', 'oriChange='+str(expTrials[curBlock][curTrial][targetGratingOrientatioinChangeLoc]), '||','resTiltVert='+str(resTiltVert)+'('+str(correctOrNotVert)+')', 'resTiltHorz='+str(resTiltHorz)+'('+str(correctOrNotHorz)+')', '||', 'correctResHorz='+str(correctResVert), 'correctResHorz='+str(correctResHorz), '||','whicheye='+str(expTrials[curBlock][curTrial][whichEyeLoc]), 'whichEyeFixation='+str(expTrials[curBlock][curTrial][whichEyeFixationLoc]), 'effectDirection='+str(expTrials[curBlock][curTrial][effectDirectionLoc])
                    
                #=======================================================
                # Asking Subjective Perception To Stimuli In Exp.3======
                #=======================================================
                if (expVersion==3) and (getSubjectPerception  == True):
                    
                    for i in range(2):
                    
                        core.wait(0.7)
                        
                        drawText=False; nframes=0; timeForText=0.5; framesForText=ceil(timeForText/MsPerFrame); drawInstru = False;
    #                    responseToPerception = null
                        while drawText == False:
                            nframes+=1
                            
                            backgroundRect.draw()
                            
                            pressedkeys=[]
                            if nframes >= framesForText:
                                pressedkeys=keyboard.state.keys()
                                
                                if drawInstru == True:
                                    if pressedkeys in [['z']]:
                                        if i == 0:
                                            perceiveGroupingVert = 1
                                        elif i ==1:
                                            perceiveGroupingHorz = 1
                                        
                                        textStim.text = askingText +'  Yes'
                                        drawText=True
                                    if pressedkeys in [['lshift']]:
                                        if i == 0:
                                            perceiveGroupingVert = 0
                                        elif i == 1:
                                            perceiveGroupingHorz = 0
                                        
                                        textStim.text = askingText + '  No'
                                        drawText=True
                                
                                if drawText==False:
                                    if i == 0:
                                        askingText='Did you respond\nin matched surround?\n(Vertical)'
                                        textStim.text=askingText
                                    if i == 1:
                                        askingText='Did you respond\nin matched surround?\n(Horizontal)'
                                        textStim.text=askingText
                                
                                if i == 0:
                                    if askingText=='Did you respond\nin matched surround?\n(Vertical)':
                                        drawInstru = True
                                if i == 1:
                                    if askingText=='Did you respond\nin matched surround?\n(Horizontal)':
                                        drawInstru = True
    #                            elif drawText==True:
    #                                textStim.text=responseToPerception
                                
                                textStim.height = 30
                                textStim.pos=[gratingPoses[0][0], gratingPoses[0][1]+(fieldsize[1]/2)+60]
                                textStim.draw()
                                textStim.pos=[gratingPoses[1][0], gratingPoses[1][1]+(fieldsize[1]/2)+60]
                                textStim.draw()
                            
                            fixationCircleL.fillColor=[-1,-1,-1]
                            fixationCircleL.lineColor=[-1,-1,-1]
                            fixationCircleR.fillColor=[-1,-1,-1]
                            fixationCircleR.lineColor=[-1,-1,-1]
                            
                            patchGlobFormL.draw()
                            patchGlobFormR.draw()
                            for LR in range(2): # left or right
                                for BMS in range(4): # big, middle, small
                                    gratingStims[LR][1].ori = gratingStims[LR][0].ori
                                    gratingStims[LR][BMS].contrast=0
                                    gratingStims[LR][BMS].draw()
                            fixationCircleL.draw()
                            fixationCircleR.draw()
                                    
                            win.flip()
                            
                            fixationCircleL.fillColor=[1,1,1]
                            fixationCircleL.lineColor=[1,1,1]
                            fixationCircleR.fillColor=[1,1,1]
                            fixationCircleR.lineColor=[1,1,1]
                            
                        core.wait(0.7)
                        
                        getSubjectPerception=False;
                        pressedkeys=[]; # reset space key response for next space key response
                    print 'sequence='+str(expTrials[curBlock][curTrial][serialLoc])+'/'+str(nTotalTrials * nBlocks), '||', 'block='+str(expTrials[curBlock][curTrial][blockLoc]),'trial='+str(expTrials[curBlock][curTrial][trialLoc]),'||', 'oriChange='+str(expTrials[curBlock][curTrial][targetGratingOrientatioinChangeLoc]), '||','resTiltVert='+str(resTiltVert), 'resTiltHorz='+str(resTiltHorz), '||', 'perceiveGroupingVert=', perceiveGroupingVert, 'perceiveGroupingHorz=', perceiveGroupingHorz, '||', 'whicheye='+str(expTrials[curBlock][curTrial][whichEyeLoc]), 'whichEyeFixation='+str(expTrials[curBlock][curTrial][whichEyeFixationLoc]), 'effectDirection='+str(expTrials[curBlock][curTrial][effectDirectionLoc])
#                    print 'sequence='+str(expTrials[curBlock][curTrial][serialLoc])+'/'+str(nTotalTrials * nBlocks), '||', 'vertResList=', vertResList
#                    print 'sequence='+str(expTrials[curBlock][curTrial][serialLoc])+'/'+str(nTotalTrials * nBlocks), '||', 'horzResList=', horzResList
                
                #============================================================
                # Show Instruction For Procedure & Resting Time==============
                #============================================================
                curSeq = expTrials[curBlock][curTrial][serialLoc];
                totalSeq = nTotalTrials * nBlocks;
                
#                print curSeq, totalSeq, int(returnNumber(curSeq-1, restSeqInterval)) + 1, restSeqInterval
                
                if (restInfo == True) and (int(returnNumber(curSeq-1, restSeqInterval)) + 1 == restSeqInterval):
                    backgroundRect.draw()
                    
                    textStim.pos=gratingPoses[0]
                    textStim.text='Rest for 20 seconds\n' + 'Progress: ' + str(int(floor((curSeq/totalSeq)*100))) + '%'
                    textStim.draw()
                    textStim.pos=gratingPoses[1]
                    textStim.draw()
                    win.flip()
                    core.wait(restBetwBlock)
                    
                    textStim.pos=gratingPoses[0]
                    textStim.text='Rest time is finished\nPress space'
                    textStim.draw()
                    textStim.pos=gratingPoses[1]
                    textStim.draw()
                    win.flip()
                    
                    keyboard.waitForPresses(keys=[' '])
                    keyboard.waitForReleases(keys=[' '])
                    
                    restInfo = False;
                    pressedkeys=[]; # reset space key response for next space key response
                
                #======================================================
                # Between-Trials Matching Scene========================
                #======================================================
                fixationCrossCenL.draw()
                fixationCrossCenR.draw()
                
                fixationCircleL.draw()
                fixationCircleR.draw()
                
                win.flip()
                
            #===============================================================================================
            # Refresh The Sitmuli Locations Acrroding To Locations of Between-Trials Matching Fixation======
            #===============================================================================================
            if targetPresentationType == 3:
                gratingPoses[0] = fixationCenPoses[0];
            else:
                gratingPoses=fixationCenPoses

            
            #===========================================================
            # Get Response During Set Time==============================
            #===========================================================
            if loopNumber>1 and disappearSlow==True and drawRes==True:
                resStartTime=core.Clock()
                resStartTime.reset()
                resStartTime.add(resTime)
                
                resList=[];
                horzResList=[];
                vertResList=[];
                resTiltVert=-1;
                resTiltHorz=-1;
                
                keyboard.getKeys(clear=True)
                # feature: clear every keyboard events
                # This code must be input before using function 'keyboard.~'.
                # This code is similar with the code 'event.clearEvents()'
                # This code is very very important function!!! I did mistake in getting responses because of absense of this code!
                # Without this code, 'keyboard.getPresses' or 'keyboard.getReleases' get every input, even before the loop set for getting responses such as keyboard input for moving stimuli not responses.
                # When the key for moving stimuli and for getting responses are same, the input key for moving stimuli are going to be recorded as responses.
                # The default option of 'clear' in function 'keyboard.getKeys' is 'True', so these two function work in same way;'keyboard.getKeys(clear=True)' & 'keyboard.getKeys()'.
                # The default options of 'keyboard.getPresses' & 'keyboard.getReleases' are also 'clear=True'.
                # That means that the problem above only occur when you get keyboard input by function 'keyboard.state.keys()' for multiple imput before using 'keyboard.getPresses' or 'keyboard.getReleases'.
                # In the problem above, I used 'keyboard.state.keys()' for moving stimuli with multiple keys (left shift & right or left or up or down) before getting responses with single keys. (right or left or up or down) The keys which were not input in responses loop were recoreded as responses.
                
                while resStartTime.getTime()<0: 
                    
                    if keyboard.getReleases(['up']):
                        resTiltHorz=2
                        resList.append(resTiltHorz)
                        horzResList.append(resTiltHorz)
                    if keyboard.getReleases(['down']):
                        resTiltHorz=3
                        resList.append(resTiltHorz)
                        horzResList.append(resTiltHorz)
                    if keyboard.getReleases(['left']):
                        resTiltVert=0
                        resList.append(resTiltVert)
                        vertResList.append(resTiltVert)
                    if keyboard.getReleases(['right']):
                        resTiltVert=1
                        resList.append(resTiltVert)
                        vertResList.append(resTiltVert)
                        
                    # checking whether response time is gone or not
                    if drawRes==True:
                        resDurationActivation=True
                        drawRes=False
            
            #==========================================================
            # Recording Response To Text================================
            #==========================================================
            if set(pressedkeys) == set([' ']) or resDurationActivation==True:
                adjustmentNumber+=1;
                
                if loopNumber>1 and disappearSlow2==True and isOdd(adjustmentNumber)==0:
                    adjustment=False
                
                if loopNumber>1 and isOdd(adjustmentNumber)==0 and disappearSlow==False:
                    
                    print 'sequence='+str(expTrials[curBlock][curTrial][serialLoc])+'/'+str(nTotalTrials * nBlocks), '||', 'vertResList=', vertResList
                    print 'sequence='+str(expTrials[curBlock][curTrial][serialLoc])+'/'+str(nTotalTrials * nBlocks), '||', 'horzResList=', horzResList
                    
                    # combinding elements of lists to one charater
                    vertResList=','.join(str(i) for i in vertResList)
                    horzResList=','.join(str(i) for i in horzResList)
                    resList=','.join(str(i) for i in resList)
                    
                    # transform the elements of lists to characters, combine & write to .txt
                    trialTilt = expTrials[curBlock][curTrial] + [resTiltVert] + [resTiltHorz]
                    lineTilt = '\t'.join(str(i) for i in trialTilt)
                    lineTilt = lineTilt + '\t' + vertResList + '\t' + horzResList + '\t' + resList
                    if expVersion in [3]:
                        lineTilt = lineTilt + '\t' + str(perceiveGroupingVert)
                        lineTilt = lineTilt + '\t' + str(perceiveGroupingHorz)
                    lineTilt += '\n'
                    dataFileTilt.write(lineTilt)
                    dataFileTilt.flush()
                    os.fsync(dataFileTilt)
                    
                    recordResponseToTextFile=True
                
                if loopNumber==1:
                    adjustment=False
                    
                if resDurationActivation==False:
                    keyboard.waitForReleases(keys=[' ']);
                    pressedkeys=[];
                
                resDurationActivation=False
                

#=========================================================================
# Instruction After Finishing All Experiment Procedure====================
#=========================================================================
instructions[3].pos=gratingPoses[0]
instructions[3].draw()
instructions[3].pos=gratingPoses[1]
instructions[3].draw()
win.flip(clearBuffer=True)
event.waitKeys(keyList = ['escape'])
win.close()
core.quit()