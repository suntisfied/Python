from __future__ import division #so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, misc, logging, gui
from psychopy.constants import * #things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, pre-pend 'np.'
from numpy import *
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os #handy system and path functions
import math
from psychopy.hardware.emulator import launchScan
import random

win = visual.Window(allowGUI=False, colorSpace= "rgb255", color = 130, fullscr = True, screen = 0, monitor='testMonitor', units='deg')
#win = visual.Window(allowGUI=False, colorSpace= "rgb255", color = 130, fullscr = True, screen = 1, monitor='testMonitor', units='deg')

#win.flip()
#core.quit()

sbjIdx = 0;


sbj=0; runIdx=1; trialIdx=2; targetType=3; setSize=4; tLoc=5; 

robot = 0; uncanny = 1; human = 2; notarget=3;
present=0; absent=1

targetTypeList = [robot] + [uncanny] + [human] + [notarget]
setSizeList = [3,6,12]
tLocList = range(12)

nTrial = len(targetTypeList)*len(setSizeList)*len(tLocList)
nRun = 1
nRep = 1
nCond = 6

initRunIdx=0
initTrialIdx=0

radi = 10
ImgSize=(3,3)

trialExp = np.empty((nRun,nRep,nTrial,nCond),int)

for thisBlock in range(nRun):
    trialBlock = np.empty((0,nCond),int)
    for thisRep in range(nRep):
        for curTargetType in targetTypeList:
            for curSetSize in setSizeList:
                for curTloc in tLocList:
                    trial = [sbjIdx] + [initRunIdx] + [initTrialIdx] + [curTargetType] + [curSetSize] + [curTloc]
                    trialBlock=np.vstack((trialBlock,trial))
    np.random.seed()
    np.random.shuffle(trialBlock)
    trialExp[thisBlock,thisRep,:,:]=trialBlock

for thisRun in range(nRun):
    for thisRep in range(nRep):
        for thisTrial in range(nTrial):
            trialExp[thisRun,thisRep,thisTrial,trialIdx]=thisTrial+1
            trialExp[thisRun,thisRep,thisTrial,runIdx]=thisRun+1
            

notargetExp=np.empty((nRun,nRep,nTrial,1),int)

for thisRun in range(nRun):
    notargetBlock=np.empty((0,1),int)
    for thisRep in range(nRep):
        for thisno in range(nTrial):
            notargetTrial=math.floor(thisno/(nTrial/3))
            notargetBlock=np.vstack((notargetBlock,notargetTrial))
    np.random.seed()
    np.random.shuffle(notargetBlock)
    notargetExp[thisRun,thisRep,:,:]=notargetBlock

#print trialExp, np.shape(trialExp)
#core.quit() 

#fixation
sizeFixation = 0.7
fixation = visual.ShapeStim(win, 
    vertices=((0, -sizeFixation), (0, sizeFixation), (0,0), (-sizeFixation,0), (sizeFixation, 0)),
    lineWidth=7,
    closeShape=False,
    lineColor='white'
) # cross shape fixation


#def polarToRect(angleList,radius):
#        """Accepts a list of angles and a radius.  Outputs the x,y positions for the angles"""
#	coords=np.empty((0,2))
#	for curAngle in angleList:
#		radAngle = (float(curAngle)*2.0*pi)/360.0
#		xCoord = round(float(radius)*cos(radAngle),0)
#		yCoord = round(float(radius)*sin(radAngle),0)
#		coords=np.vstack((coords, [xCoord,yCoord]))
#	return coords   
def polarToRect(angleList,radius):
        """Accepts a list of angles and a radius.  Outputs the x,y positions for the angles"""
	coords=[]
	for curAngle in angleList:
		radAngle = (float(curAngle)*2.0*pi)/360.0
		xCoord = round(float(radius)*cos(radAngle),0)
		yCoord = round(float(radius)*sin(radAngle),0)
		coords.append([xCoord,yCoord])
	return coords
angle = 360/16
angles=[]
#for i in range(1,17):
#    angles.append(angle*i)
#coords = polarToRect(angles, 6)
coords = polarToRect([angle, angle*2, angle*3, angle*4, angle*5, angle*6, angle*7, angle*8, angle*9, angle*10, angle*11, angle*12, angle*13, angle*14, angle*15, angle*16], radi)

#print coords, i
#core.quit()

# eliminate vertical, horizontal
#stimuliCoords=np
stimuliCoords = np.array([[coords[0], coords[1], coords[2]], [coords[4], coords[5], coords[6]], [coords[8], coords[9], coords[10]], [coords[12], coords[13], coords[14]]])
#stimuliCoords = np.matrix('coords[0], coords[1], coords[2]; coords[4], coords[5], coords[6]; coords[8], coords[9], coords[10]; coords[12], coords[13], coords[14]')

def randomButNot (lst, item, k):
    randItemList = random.sample(lst, k)
    if item in randItemList:
        go = True
        while go:
            randItemList = random.sample(lst, k)
            if not item in randItemList:
                return randItemList
    else:
        return randItemList

keyList = ['slash', 'z', 'escape']

#text ready
loadingText=visual.TextStim(win, ori=0, name='instrText',
    text='Now loading... please wait',
    font='Arial',
    pos=[0, 0], height=1,wrapWidth=None,
    color=[1, 1, 1], colorSpace='rgb', opacity=1,
    depth=0.0)

readyText=visual.TextStim(win, ori=0, name='instrText',
    text='If you are feeling well and ready,\n\npress space bar to continue',
    font='Arial',
    pos=[0, 0], height=1,wrapWidth=None,
    color=[1, 1, 1], colorSpace='rgb', opacity=1,
    depth=0.0)
    
okText=visual.TextStim(win, ori=0, name='okText',
    text='Alright!!\nThe experiment will start soon',
    font='Arial',
    pos=[0, 0], height=1,wrapWidth=None,
    color=[1, 1, 1], colorSpace='rgb', opacity=1,
    depth=0.0)    
    
probeText=visual.TextStim(win, ori=0, name='probeText',
    text='present or absent?',
    font='Arial',
    pos=[0, 0], height=1,wrapWidth=None,
    color=[1, 1, 1], colorSpace='rgb', opacity=1,
    depth=0.0)        

feedbackTextwrong=visual.TextStim(win, ori=0, name='feedText',
    text='incorrect!',
    font='Arial',
    pos=[0, 0], height=2,wrapWidth=None,
    color=[1, 1, 1], colorSpace='rgb', opacity=1,
    depth=0.0)
    
feedbackTextright=visual.TextStim(win, ori=0, name='feedText',
    text='correct!',
    font='Arial',
    pos=[0, 0], height=2,wrapWidth=None,
    color=[1, 1, 1], colorSpace='rgb', opacity=1,
    depth=0.0)
    
finishText=visual.TextStim(win, ori=0, name='instrText',
    text='This session is finished.\nPlease see the next experiment',
    font='Arial',
    pos=[0, 0], height=1,wrapWidth=None,
    color=[1, 1, 1], colorSpace='rgb', opacity=1,
    depth=0.0)

allfinishText=visual.TextStim(win, ori=0, name='instrText',
    text='This experiment is finished.\nThank you.',
    font='Arial',
    pos=[0, 0], height=1,wrapWidth=None,
    color=[1, 1, 1], colorSpace='rgb', opacity=1,
    depth=0.0)

instructionText=visual.TextStim(win, ori=0, name='instrText',
    text='One image is presented frist.\n\nIn next pageSearch the image \n\nz key=absent, / key=present',
    font='Arial',
    pos=[0, 0], height=1,wrapWidth=None,
    color=[1, 1, 1], colorSpace='rgb', opacity=1,
    depth=0.0)


loadingText.draw()
win.flip()


#stimuli ready!!

distractorPath = os.getcwd() + '/img_prac/distractors/'
tRobotPath = os.getcwd() + '/img_prac/targets/robot/'
tUncannyPath = os.getcwd() + '/img_prac/targets/uncanny/'
tHumanPath = os.getcwd() + '/img_prac/targets/human/'
instructioinPath = os.getcwd() + '/instruction_text_image/'

tRobot=0; tUncanny=1; tHuman=2;
distImgs=np.empty((0,1))
targetImgs=np.empty((0,3))

for thisImg in range(1,13):
    distImgName = distractorPath + 'D' + str(thisImg) + '.jpg'
    tRobotImgName = tRobotPath + 'R' + str(thisImg) + '.jpg'
    tUncannyImgName = tUncannyPath + 'U' + str(thisImg) + '.jpg'
    tHumanImgName = tHumanPath + 'H' + str(thisImg) + '.jpg'
    
    distImg = visual.ImageStim(win, image=distImgName, pos=(0, 0), mask = 'none',
        size=ImgSize,#will be the size of the original image in pixels
        units='deg', interpolate=True,
        autoLog=False)
    robotImg = visual.ImageStim(win, image=tRobotImgName, pos=(0, 0), mask = 'none',
        size=ImgSize,#will be the size of the original image in pixels
        units='deg', interpolate=True,
        autoLog=False)
    uncannyImg = visual.ImageStim(win, image=tUncannyImgName, pos=(0, 0), mask = 'none',
        size=ImgSize,#will be the size of the original image in pixels
        units='deg', interpolate=True,
        autoLog=False)
    humanImg = visual.ImageStim(win, image=tHumanImgName, pos=(0, 0), mask = 'none',
        size=ImgSize,#will be the size of the original image in pixels
        units='deg', interpolate=True,
        autoLog=False)
        
    distImgs=np.vstack((distImgs,distImg))
    targetImg=[robotImg,uncannyImg,humanImg]
    targetImgs=np.vstack((targetImgs,targetImg))

ImgName_instr_search = instructioinPath + 'instruction_search.png'
ImgName_instr_rating = instructioinPath + 'instruction_rating.png'

instruction_search = visual.ImageStim(win, image=ImgName_instr_search, pos=(0, 0), mask = 'none',
        size=[14.98, 13],#will be the size of the original image in pixels
        units='deg', interpolate=True,
        autoLog=False)
instruction_rating = visual.ImageStim(win, image=ImgName_instr_rating, pos=(0, 0), mask = 'none',
        size=[20.80, 13],#will be the size of the original image in pixels
        units='deg', interpolate=True,
        autoLog=False)

#print targetImgs
#targetImgs[1,0].draw()
#win.flip()
#core.wait(1)
#core.quit()

#print distImgs
#
#for thisItem in range(12):
#    distImgs[thisItem,0].setPos(stimuliCoords[thisItem])
#    distImgs[thisItem,0].draw()
#    
#
#win.flip()
#core.wait(5)
#
#core.quit()

instruction_search.draw()
win.flip()
event.waitKeys('space')

globalClock = core.Clock()     
for thisRun in range(nRun):

    readytxt='If you are feeling well and ready,\n\npress space bar to continue'
    readytxt=readytxt + '\n\nsession ' + str(thisRun+1) + '/6'
    readyText=visual.TextStim(win, ori=0, name='instrText',
    text=readytxt,
    font='Arial',
    pos=[0, 0], height=1,wrapWidth=None,
    color=[1, 1, 1], colorSpace='rgb', opacity=1,
    depth=0.0)
    #ready screen 
    readyText.draw()
    win.flip()
    
    event.waitKeys(keyList = ['space']) #remove max wait for behavioral experiment
    okText.draw()
    win.flip()
    event.waitKeys(maxWait = 1, keyList=['g']) #for scan, remove maxWait
    #vol = launchScan(win, MR_settings, simResponses=None, mode = 'Test', globalClock=globalClock, instr = 'Select Scan or Test, press enter')
    fixation.draw()
    win.flip()
    core.wait(0.5)
    
    for thisTrial in range(nTrial):
        
        tIdx = random.sample(range(12), 1)[0]
        np.random.shuffle(distImgs)
        
        if trialExp[thisRun, 0, thisTrial, targetType] == robot:
            targetImgs[tIdx,tRobot].setPos([0,0])
            targetImgs[tIdx,tRobot].draw()
        elif trialExp[thisRun, 0, thisTrial, targetType] == uncanny:
            targetImgs[tIdx,tUncanny].setPos([0,0])
            targetImgs[tIdx,tUncanny].draw()
        elif trialExp[thisRun, 0, thisTrial, targetType] == human:
            targetImgs[tIdx,tHuman].setPos([0,0])
            targetImgs[tIdx,tHuman].draw()
        elif trialExp[thisRun, 0, thisTrial, targetType] == notarget:
            thisNotarget=notargetExp[thisRun, 0, thisTrial, 0]
            targetImgs[tIdx,thisNotarget].setPos([0,0])
            targetImgs[tIdx,thisNotarget].draw()
        win.flip()
        
        itiTargetOnset = globalClock.getTime()
        drawnT = False
        while globalClock.getTime() - itiTargetOnset <= 0.3: # target presentation time
            if drawnT == False:
                drawnT == True
        fixation.draw()
        win.flip()
        
        targetOnset = globalClock.getTime()
        drawn = False
        while globalClock.getTime() - targetOnset <= 0.15:
            if drawn == False:
                if trialExp[thisRun, 0, thisTrial, setSize] == 3:
                    drawn = True
                    
                    tTypeIdx = int(trialExp[thisRun, 0, thisTrial, targetType])
                    tLocIdx = int(trialExp[thisRun, 0, thisTrial, tLoc])
                    dPosIdx = int(math.floor(tLocIdx/3))
                    tsetLosIdx = int(tLocIdx - (3*dPosIdx))
                    
                    for thisImg in range(3):
                        distImgs[thisImg,0].setPos(stimuliCoords[dPosIdx,thisImg])
                        distImgs[thisImg,0].draw()
                    
                    if tTypeIdx != notarget:
                       targetImgs[tIdx,tTypeIdx].setPos(stimuliCoords[dPosIdx,tsetLosIdx])
                       targetImgs[tIdx,tTypeIdx].draw()
                    
                elif trialExp[thisRun, 0, thisTrial, setSize] == 6:
                    drawn = True
                    
                    tTypeIdx = trialExp[thisRun, 0, thisTrial, targetType]
                    tLocIdx = trialExp[thisRun, 0, thisTrial, tLoc]
                    dPosIdx1 = int(math.floor(tLocIdx/3))
                    dPosIdx2 = int(abs(2-dPosIdx1))
                    tsetLosIdx = tLocIdx - (3*dPosIdx1)
                    
                    for thisImg in range(3):
                        distImgs[thisImg,0].setPos(stimuliCoords[dPosIdx1,thisImg])
                        distImgs[thisImg+3,0].setPos(stimuliCoords[dPosIdx2,thisImg])
                        distImgs[thisImg,0].draw()
                        distImgs[thisImg+3,0].draw()
                    if tTypeIdx != notarget:
                       targetImgs[tIdx,tTypeIdx].setPos(stimuliCoords[dPosIdx1,tsetLosIdx])
                       targetImgs[tIdx,tTypeIdx].draw()
                        
                elif trialExp[thisRun, 0, thisTrial, setSize] == 12:
                    drawn = True
                    
                    tTypeIdx = trialExp[thisRun, 0, thisTrial, targetType]
                    tLocIdx = trialExp[thisRun, 0, thisTrial, tLoc]
                    dPosIdx = int(math.floor(tLocIdx/3))
                    tsetLosIdx = tLocIdx - (3*dPosIdx)
                    
                    for thisImg in range(12):
                        dPosIdxRow = math.floor(thisImg/3)
                        dPosIdxCol = thisImg - (3*dPosIdxRow)
                        
                        distImgs[thisImg,0].setPos(stimuliCoords[dPosIdxRow,dPosIdxCol])
                        distImgs[thisImg,0].draw()
                    if tTypeIdx != notarget:
                       targetImgs[tIdx,tTypeIdx].setPos(stimuliCoords[dPosIdx,tsetLosIdx])
                       targetImgs[tIdx,tTypeIdx].draw()
            fixation.draw()
        win.flip()
        

        searchOnset = globalClock.getTime()
        
        respTargetClock = core.Clock()
        respTargetClock.reset()
        
        tAccR = 0
        tResR = 0
        tRtR = 0
        
        event.clearEvents()
        thisKey = event.waitKeys(keyList = keyList)
        if (thisKey[0] == keyList[present]) or (thisKey[0] == keyList[absent]):
            tRtR = respTargetClock.getTime()
        if thisKey[0] == keyList[present]:
            tResR = present
        elif thisKey[0] == keyList[absent]:
            tResR = absent
        elif thisKey[0] in ['escape']: 
            core.quit()
        
        if (trialExp[thisRun,0,thisTrial,targetType] != 3 and tResR == absent) or (trialExp[thisRun,0,thisTrial,targetType] == 3 and tResR == present):
            tAccR = 1
            
        if tAccR ==1:
            feedbackTextright.draw()
            win.flip()
        else:
            feedbackTextwrong.draw()
            win.flip()
        core.wait(0.5)
        
#        instruction_rating.draw()
#        win.flip()
#        event.waitKeys('space')
        
#        if thisTrial ==0 or thisTrial ==2 or thisTrial ==4:
#            keypad = ['num_0','num_1', 'num_2','num_3','num_4','num_5','num_6','num_7','num_8','num_9']
#            keypad = ['0','1', '2','3','4','5','6','7','8','9']
#            ratingScale = visual.RatingScale(win, choices = ['0','1','2','3','4','5','6','7', '8', '9'], respKeys  = keypad, acceptKeys ='space',
#            scale='0=extremly slow, ................. 9=extremly fast')
#            instr_rating_txt = "How confident are you fast for searching?"
#            instr_rating = visual.TextStim(win, text=instr_rating_txt, height=.08, units='norm')
#        while ratingScale.noResponse:
#            instr_rating.draw()
#            ratingScale.draw()
#            win.flip()
        

allfinishText.draw()
win.flip()
event.waitKeys(keyList = ['escape'])
core.quit()








