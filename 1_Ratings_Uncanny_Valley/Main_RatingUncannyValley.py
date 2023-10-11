from __future__ import division #so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, misc, logging, gui
from psychopy.constants import * #things like STARTED, FINISHED
import psychopy
import numpy as np  # whole numpy lib is available, pre-pend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os #handy system and path functions
from math import *
import random
from psychopy.hardware.emulator import launchScan
import time
from decimal import Decimal
from StringIO import StringIO
import struct
from PIL import Image # Get the size(demension) of an image
import Tkinter as tk # text widget library
#import pyglet

from collections import deque
import time

from psychopy.iohub.client import ioHubDeviceView, ioEvent, DeviceRPC
from psychopy.iohub.devices import DeviceEvent
from psychopy.iohub.devices.keyboard import KeyboardInputEvent
from psychopy.iohub.constants import EventConstants, KeyboardConstants
from psychopy.core import getTime
from psychopy.visual.window import Window

#ptrfdP = (c_double*100000)()

#set up some fonts. If a list is provided, the first font found will be used.
sans = ['Gill Sans MT', 'Arial','Helvetica','Verdana'] #use the first font found on this list

white=(255, 255, 255)
black=(0, 0, 0)
gray=(50, 50, 50)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)

expName='Rating'
expInfo={'participant':'00'}
dlg=gui.DlgFromDict(dictionary=expInfo,title=expName)
if dlg.OK==False: core.quit() #user pressed cancel
expInfo['date']=data.getDateStr()#add a simple timestamp
expInfo['expName']=expName

if not os.path.isdir('data'):
    os.makedirs('data') #if this fails (e.g. permissions) we will get error


sbjIdx = int(expInfo['participant'])
issbjIdx = ceil((sbjIdx/2) - floor(sbjIdx/2))

#-----------Value Control-----------------------
screenNum=0;

#ntRA=3; ntRD=3; ntRR=3; ntHA=3; ntHD=3; ntHR=5;
ntRA=114; ntRD=86; ntRR=70; ntHA=96; ntHD=106; ntHR=82;

#------switch image stumulus according to subject number--------------------------------------------------------------------
if np.ceil(sbjIdx/2-floor(sbjIdx/2))!=0:
    nRA=[0,floor(ntRA/2), floor(ntRA/2)+1,ntRA+1];
    nRD=[0,floor(ntRD/2), floor(ntRD/2)+1,ntRD+1];
    nRR=[0,floor(ntRR/2), floor(ntRR/2)+1,ntRR+1];
    nHA=[0,floor(ntHA/2), floor(ntHA/2)+1,ntHA+1];
    nHD=[0,floor(ntHD/2), floor(ntHD/2)+1,ntHD+1];
    nHR=[0,floor(ntHR/2), floor(ntHR/2)+1,ntHR+1];
else:
    nRA=[floor(ntRA/2)+1,ntRA+1, 0,floor(ntRA/2)];
    nRD=[floor(ntRD/2)+1,ntRD+1, 0,floor(ntRD/2)];
    nRR=[floor(ntRR/2)+1,ntRR+1, 0,floor(ntRR/2)];
    nHA=[floor(ntHA/2)+1,ntHA+1, 0,floor(ntHA/2)];
    nHD=[floor(ntHD/2)+1,ntHD+1, 0,floor(ntHD/2)];
    nHR=[floor(ntHR/2)+1,ntHR+1, 0,floor(ntHR/2)];
#---------------------------------------------------------------------------------------------------------------------------
#print nRA, nRD, nRR, nHA, nHD, nHR, 'if=',np.ceil(sbjIdx/2-floor(sbjIdx/2))
imgSizeX=300
imgSizeY=400

disImgX=imgSizeX+100
disImgY=imgSizeY+20

disTextX=40

ratingTextSize=30
blurtextcolor=180

TextRectlinecolor=200; TextRectfillcolor=70
TextRectwidth=70; TextRectheight=50;

insttextSize1=[1400,1400/2.783]
insttextSize2=[1400,1400/2.235]
headtextSize1=[1000,1000/11.8]
headtextSize2=[1000,1000/9.5]
#------------------------------------------------

win = visual.Window(allowGUI=False, colorSpace= "rgb255", color = 130, fullscr = True, screen = screenNum, monitor='testMonitor', units='pix')
#win = visual.Window(allowGUI=False, colorSpace= "rgb255", color = 130, fullscr = True, screen = 1, monitor='testMonitor', units='deg')

loadingText=visual.TextStim(win,
    text='Now loading... please wait',
    height=30, pos=[0,0], color=white, font='Arial', colorSpace='rgb255', ori=0, wrapWidth=None, opacity=1, depth=0.0)

loadingPercentText=visual.TextStim(win,
    text='',
    height=30, pos=[0,-100], color=white, font='Arial', colorSpace='rgb255', ori=0, wrapWidth=None, opacity=1, depth=0.0)

loadingCompleteText=visual.TextStim(win,
    text='Done',
    height=30, pos=[0,100], color=white, font='Arial', colorSpace='rgb255', ori=0, wrapWidth=None, opacity=1, depth=0.0)

responseText=visual.TextStim(win,
    text='',
    height=ratingTextSize, pos=[0,0], color=white, font='Arial', colorSpace='rgb255', ori=0, wrapWidth=None, opacity=1, depth=0.0)
    
    
instruct1=visual.TextStim(win,
    text='Please rating the pictures according to how you feel familiary when you look at from 1(certainly not) to 100(certainly do) if you ready enter key',
    height=ratingTextSize, pos=[0,0], color=white, font='Arial', colorSpace='rgb255', ori=0, wrapWidth=None, opacity=1, depth=0.0)
    
instruct2=visual.TextStim(win,
    text='Please rating the pictures according to how you think the picture has human likeness from 1(certainly not) to 100(certainly do) if you ready enter key',
    height=ratingTextSize, pos=[0,0], color=white, font='Arial', colorSpace='rgb255', ori=0, wrapWidth=None, opacity=1, depth=0.0)
    
endText=visual.TextStim(win,
    text='Thank you! All processes are over',
    height=50, pos=[0,0], color=white, font='Arial', colorSpace='rgb255', ori=0, wrapWidth=None, opacity=1, depth=0.0)
    
TextRect=visual.Rect(win,
                    pos=[0,0],
                    width=TextRectwidth, height=TextRectheight,
                    lineWidth=5, lineColor=TextRectlinecolor, fillColor=TextRectfillcolor, lineColorSpace='rgb255',  fillColorSpace='rgb255')

if issbjIdx==0:
    textpath = os.getcwd() + '/TextImages_hor/'
    fileName1='data' + os.path.sep + '%s_%s_%s' %(expInfo['participant'], 'Horrifying', expInfo['date'])
elif issbjIdx==1:
    textpath = os.getcwd() + '/TextImages_fam/'
    fileName1='data' + os.path.sep + '%s_%s_%s' %(expInfo['participant'], 'Familiarity', expInfo['date'])

issbjIdx2=sbjIdx-floor((sbjIdx-0.1)/4)*4
if sbjIdx<=38:
    if issbjIdx==1:
        textpath = os.getcwd() + '/TextImages_hor/'
        fileName1='data' + os.path.sep + '%s_%s_%s' %(expInfo['participant'], 'Horrifying', expInfo['date'])
    elif issbjIdx==0:
        textpath = os.getcwd() + '/TextImages_fam/'
        fileName1='data' + os.path.sep + '%s_%s_%s' %(expInfo['participant'], 'Familiarity', expInfo['date'])
elif sbjIdx>38:
    if issbjIdx2>2:
        textpath = os.getcwd() + '/TextImages_hor/'
        fileName1='data' + os.path.sep + '%s_%s_%s' %(expInfo['participant'], 'Horrifying', expInfo['date'])
    elif issbjIdx2<=2:
        textpath = os.getcwd() + '/TextImages_fam/'
        fileName1='data' + os.path.sep + '%s_%s_%s' %(expInfo['participant'], 'Familiarity', expInfo['date'])
    
instF = visual.ImageStim(win, image=textpath+'inst_familarity'+'.png',  pos=(0, 0), mask = 'none',
                size=(insttextSize1[0],insttextSize1[1]),
                interpolate=True,
                autoLog=False)
                
instH = visual.ImageStim(win, image=textpath+'inst_humanlikeness'+'.png',  pos=(0, 0), mask = 'none',
                size=(insttextSize2[0],insttextSize2[1]),
                interpolate=True,
                autoLog=False)
                
                
headF = visual.ImageStim(win, image=textpath+'familarity'+'.png',  pos=(0, 0), mask = 'none',
                size=(headtextSize1[0],headtextSize1[1]),
                interpolate=True,
                autoLog=False)
                
headH = visual.ImageStim(win, image=textpath+'humanlikeness'+'.png',  pos=(0, 0), mask = 'none',
                size=(headtextSize2[0],headtextSize2[1]),
                interpolate=True,
                autoLog=False)
                

RApath = os.getcwd() + '/Images/Robot-like/Animation/'
RDpath = os.getcwd() + '/Images/Robot-like/Doll/'
RRpath = os.getcwd() + '/Images/Robot-like/Robot/'
HApath = os.getcwd() + '/Images/Human-like/Animation/'
HDpath = os.getcwd() + '/Images/Human-like/Doll/'
HRpath = os.getcwd() + '/Images/Human-like/Robot/'

path=[RApath,RDpath,RRpath,HApath,HDpath,HRpath]
imageRangeName=['RA','RD','RR','HA','HD','HR']
nImgA=[nRA,nRD,nRR,nHA,nHD,nHR]

RA=0; RD=1; RR=2; HA=3; HD=4; HR=5;

keysLocation = [['1', 'num_1'], ['2', 'num_2'], ['3', 'num_3'], ['4', 'num_4'],]


for thisBlock in range(0,3,2):
    
    if thisBlock==0:
        instF.draw()
#        if issbjIdx==1:
#            fileName1='data' + os.path.sep + '%s_%s_%s' %(expInfo['participant'], 'Familiarity', expInfo['date'])
#        elif issbjIdx==0:
#            fileName1='data' + os.path.sep + '%s_%s_%s' %(expInfo['participant'], 'Horrifying', expInfo['date'])
        dataFile1 = open(fileName1+'.txt', 'w')
        dataFile1.write('subj\t' 'trialNum\t' 'imageType\t' 'imageNum\t' 'imageSizeH\t' 'imageSizeV\t' 'res\n') # write the datafile ## \t->space the amount of tab
    else:
        instH.draw()
        fileName2='data' + os.path.sep + '%s_%s_%s' %(expInfo['participant'], 'Human_Likeness', expInfo['date'])
        dataFile2 = open(fileName2+'.txt', 'w')
        dataFile2.write('subj\t' 'trialNum\t' 'imageType\t' 'imageNum\t' 'imageSizeH\t' 'imageSizeV\t' 'res\n')
    win.flip()
        
    event.waitKeys(keyList = ['return'])
    
    # image loading
    nImgs=0
    for this in range(len(nImgA)):
        nImgs=nImgs+(int(nImgA[this][thisBlock+1])-int(nImgA[this][thisBlock]))
#    print 'nImgs=',nImgs, nImgA[this][thisBlock+1],nImgA[this][thisBlock]
    loadingText.draw()
    win.flip()
    
    nimage=0; nsubj=1; ntrialNum=2; nimageType=3; nimageNum=4; nimageSizeH=5; nimageSizeV=6; nres=7;
    trialExp=[]; trialNum=0; thisImgPercent=0; tiralNum=0; subj=0; res=0
    for thisRange in range(len(nImgA)):
        if nImgA[thisRange][thisBlock]==0:#numbering of image
            imageNum=nImgA[thisRange][thisBlock]
        else:
            imageNum=nImgA[thisRange][thisBlock]-1

        imageType=imageRangeName[thisRange]
        for thisImg in range(int(nImgA[thisRange][thisBlock]),int(nImgA[thisRange][thisBlock+1])):
            trialNum=trialNum+1
            imageNum=imageNum+1
            
            if nImgA[thisRange][thisBlock]==0:
                strImg = thisImg+1
            else:
                strImg = thisImg
                if strImg>nImgA[thisRange][thisBlock+1]:
                    strImg = thisImg-1
                    
#            print 'strImg=',strImg
            imgName = path[thisRange] + imageRangeName[thisRange] + str(strImg) + '.png'
            im = Image.open(imgName)
            
            if im.size[1]>imgSizeY or im.size[0]>imgSizeX:
                temImg = visual.ImageStim(win, image=imgName,  pos=(0, 0), mask = 'none',
                size=(imgSizeX,imgSizeY),
                interpolate=True,
                autoLog=False)
            else:
                temImg = visual.ImageStim(win, image=imgName,  pos=(0, 0), mask = 'none',
                interpolate=True,
                autoLog=False)
                
            imageSizeH=im.size[0]
            imageSizeV=im.size[1]
            image=temImg
            
            trial=[image] + [sbjIdx] + [trialNum] + [imageType] + [imageNum] + [imageSizeH] + [imageSizeV] + [res]
    
            thisImgPercent=thisImgPercent+1
            thisPercent=(thisImgPercent/nImgs)*100
            thisPercent=np.floor(thisPercent)
            loadingPercentText.setText(thisPercent)
            loadingText.draw()
            loadingPercentText.draw()
            win.flip()
    
            trialExp.append(trial)
            for key in event.getKeys():
                if key in ['escape']:
                    core.quit()
#    print len(trialExp), trialExp
    
    random.seed()
    random.shuffle(trialExp)
    
    loadingCompleteText.draw()
    win.flip()
    
    imagePos=[
        [-disImgX,disImgY/2],
        [0,disImgY/2],
        [disImgX,disImgY/2],
        [-disImgX,-disImgY/2],
        [0,-disImgY/2],
        [disImgX,-disImgY/2]
        ]
        
    
    # research start
    for thisStart in range(0, nImgs, 6):
#        print 'thisStart=',thisStart
        
        if thisStart/6==floor(nImgs/6):
            rimg=nImgs-thisStart
        else:
            rimg = 6
#            print 'rimg=', rimg
        
        # Text Position Setting
        responseTextPosArray=[]; horz=0; vert=1;
        # get each image size
        for thistextpos in range(rimg):
#            print 'thistextpos=',thistextpos
            if trialExp[thisStart+thistextpos][nimageSizeV]>imgSizeX or trialExp[thisStart+thistextpos][nimageSizeH]>imgSizeY:
                imageSizeH=imgSizeX
                imageSizeV=imgSizeY
            else:
                imageSizeH=trialExp[thisStart+thistextpos][nimageSizeH]
                imageSizeV=trialExp[thisStart+thistextpos][nimageSizeV]
            # text position setting according to each image size
            if thistextpos<3:
                responseTextPos=[imagePos[thistextpos][0]+(imageSizeH/2)+disTextX, imagePos[thistextpos][1]-(imageSizeV/2.5)]
            else:
                responseTextPos=[imagePos[thistextpos][0]+(imageSizeH/2)+disTextX, imagePos[thistextpos][1]+(imageSizeV/2.5)]
            
            responseTextPosArray.append(responseTextPos)
        
        # first draw face images and textboxes
        # draw face image
        TextRect.setLineColor(TextRectlinecolor)
        TextRect.setFillColor(TextRectfillcolor)
        for thisImg in range(rimg):
            trialExp[thisStart+thisImg][nimage].setPos(imagePos[thisImg])
            trialExp[thisStart+thisImg][nimage].draw()
            TextRect.setPos(responseTextPosArray[thisImg])
            TextRect.draw()
        TextRect.setPos(responseTextPosArray[0])
        TextRect.setLineColor(white)
        TextRect.setFillColor(black)
        TextRect.draw()
#        if thisBlock ==0:
#            headF.setPos([0,470])
#            headF.draw()
#        else:
#            headH.setPos([0,470])
#            headH.draw()
        win.flip()
        
        responseList=[]; responseTextPosList=[];
        CurrentRes=0; boxRes=1;
        response='';
        event.clearEvents()
        while CurrentRes<=rimg-1:
            TextRect.setLineColor(TextRectlinecolor)
            TextRect.setFillColor(TextRectfillcolor)
#            core.wait(0.1)
            for key in event.waitKeys():
                # set for using numeric keypad
                #-----------------------------------------------------------------------------------------
                keypad=['num_0','num_1', 'num_2','num_3','num_4','num_5','num_6','num_7','num_8','num_9']
                for i in range(10):
                    if key==keypad[i]:
                        key=str(i)
                #-----------------------------------------------------------------------------------------
#                print 'key=',key
#                key=pyglet.window.key.symbol_string(key).lower()

                # Only accept numeric input
                Keytype=np.core.defchararray.isnumeric(unicode(key))
                responsetype=np.core.defchararray.isnumeric(unicode(response))

                # Key Responses start
                if key in ['escape']:
                    win.close()
                    core.quit()
    
                elif Keytype==True:
                    for thisImg in range(rimg):
                        trialExp[thisStart+thisImg][nimage].setPos(imagePos[thisImg])
                        trialExp[thisStart+thisImg][nimage].draw()
                        TextRect.setPos(responseTextPosArray[thisImg])
                        TextRect.draw()
                        
                    for thisRes in range(len(responseList)):
                        responseText.setText(responseList[thisRes])
                        responseText.setColor(blurtextcolor)
                        responseText.setPos(responseTextPosList[thisRes])
                        responseText.draw()
                        
                    responseText.setColor(white)
                    responseText.setPos(responseTextPosArray[CurrentRes])
                    
                    TextRect.setPos(responseTextPosArray[CurrentRes])
                    TextRect.setLineColor(white)
                    TextRect.setFillColor(black)
                    TextRect.draw()
    
                    if response=='' or int(response) in range(1,10) or (int(response)==10 and int(key)==0):
                        response=response+key
                    responseText.setText(response)
                    responseText.draw()

#                    if thisBlock ==0:
#                        headF.setPos([0,470])
#                        headF.draw()
#                    else:
#                        headH.setPos([0,470])
#                        headH.draw()
#                    core.wait(0.1)
                    win.flip()
#                    print 'key=',key
                    
                elif key in ['return'] and responsetype==True:
                    Res = trialExp[thisStart+CurrentRes][1:nres]
                    Res.append(int(response))
                    
                    line = '\t'.join(str(i) for i in Res)
                    line += '\n'
                    
                    if thisBlock==0:
                        dataFile1.write(line)
                        dataFile1.flush()
                        os.fsync(dataFile1)
                    else:
                        dataFile2.write(line)
                        dataFile2.flush()
                        os.fsync(dataFile2)
                    
                    CurrentRes=CurrentRes+1
                    
                    responseList.append(response)
                    responseTextPosList.append(responseTextPosArray[CurrentRes-1])
                    response=''
                    
                    for thisImg in range(rimg):
                        trialExp[thisStart+thisImg][nimage].setPos(imagePos[thisImg])
                        trialExp[thisStart+thisImg][nimage].draw()
                        TextRect.setPos(responseTextPosArray[thisImg])
                        TextRect.draw()
                    if CurrentRes>rimg-1:
                        TextRect.setPos(responseTextPosArray[CurrentRes-1])
                    else:
                        TextRect.setPos(responseTextPosArray[CurrentRes])
                    
                    TextRect.setLineColor(white)
                    TextRect.setFillColor(black)
                    TextRect.draw()
                        
                    for thisRes in range(len(responseList)):
                        responseText.setText(responseList[thisRes])
                        responseText.setColor(blurtextcolor)
                        responseText.setPos(responseTextPosList[thisRes])
                        responseText.draw()
#                    if thisBlock ==0:
#                        headF.setPos([0,470])
#                        headF.draw()
#                    else:
#                        headH.setPos([0,470])
#                        headH.draw()
#                    core.wait(0.1)
                    win.flip()
                    core.wait(0.1)
                    
                elif key in ['delete','backspace']:
                    response = response[:-1] #delete last character
                    
                    for thisImg in range(rimg):
                        trialExp[thisStart+thisImg][nimage].setPos(imagePos[thisImg])
                        trialExp[thisStart+thisImg][nimage].draw()
                        TextRect.setPos(responseTextPosArray[thisImg])
                        TextRect.draw()
                    TextRect.setPos(responseTextPosArray[CurrentRes])
                    TextRect.setLineColor(white)
                    TextRect.setFillColor(black)
                    TextRect.draw()
                        
                    for thisRes in range(len(responseList)):
                        responseText.setText(responseList[thisRes])
                        responseText.setColor(blurtextcolor)
                        responseText.setPos(responseTextPosList[thisRes])
                        responseText.draw()
                    
                    responseText.setPos(responseTextPosArray[CurrentRes])
                    responseText.setColor(white)
                    responseText.setText(response)
                    responseText.draw()
#                    if thisBlock ==0:
#                        headF.setPos([0,470])
#                        headF.draw()
#                    else:
#                        headH.setPos([0,470])
#                        headH.draw()
#                    core.wait(0.1)
                    win.flip()
                    core.wait(0.1)
                    event.waitKeys(maxWait=-1) # wait until all keys are released
                    event.clearEvents()
                    
                event.waitKeys(maxWait=-1) # wait until all keys are released
                event.clearEvents()
            

endText.draw()
win.flip()
event.waitKeys(keyList = ['escape'])

core.quit()
