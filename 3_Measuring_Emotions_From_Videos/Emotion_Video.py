from __future__ import division #so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, misc, logging, gui, monitors
from psychopy.constants import * #things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, pre-pend 'np.'
import copy # for copying variable
import os #handy system and path functions
import math
import random
import time
def returnNumber(inputNumber, returnUnit):
    return inputNumber - (np.floor(inputNumber/returnUnit)*returnUnit)

# pop ups for participant's information=====================
expName='EmotionMovie'
expInfo={'participant':'000', 'Age':'00', 'BirthDate':'000000', 'Gender':'0'}
dlg=gui.DlgFromDict(dictionary=expInfo,title=expName)
if dlg.OK==False: core.quit() #user pressed cancel
expInfo['date']=data.getDateStr(format='%Y_%b_%d_%H%M%S')#add a simple timestamp %'%Y_%b_%d_%H%M%S'
expInfo['expName']=expName

if not os.path.isdir('Data'):
    os.makedirs('Data') #if this fails (e.g. permissions) we will get error
fileName='Data' + os.path.sep + '%s_%s_%s' %(expName, expInfo['participant'], expInfo['date'])
# pop ups for participant's information--------------------

# variable settings=====================
sbjIdx = int(expInfo['participant']);
ageIdx = int(expInfo['Age'])
genderIdx = int(expInfo['Gender'])
BirthDateIdx = int(expInfo['BirthDate'])

neuMovieList=[1,2]
exMovieList=[3,4]
nMovieElements=2
nMoviePools=2
nMovies=nMovieElements*nMoviePools
nTrial=nMovies+1
movieIdx=5
# variable settings--------------------

# shuffle each movie lists
np.random.seed()
random.shuffle(neuMovieList)
random.shuffle(exMovieList)

# combine each randomized lists
movieListPool=[neuMovieList]+[exMovieList]

# make movie list by intersection design
movieList=[]
for thisMovie in range(nMovieElements):
    for thisMoviePool in range(nMoviePools):
        tmpMovieNum=movieListPool[thisMoviePool][thisMovie] # choose one movie number for intersection design
        movieList.append(tmpMovieNum)

movieList=[0]+movieList

# make arrary of experimetal design
expTrials = []; thisSerial=0; 
for thisDeginTrial in range(nTrial):
    trial = [sbjIdx] + [ageIdx] + [BirthDateIdx] + [genderIdx] + [thisDeginTrial+1] + [movieList[thisDeginTrial]]
    expTrials.append(trial)

# load video stime=================================================
videoNames = ['N1.wmv', 'N2.wmv', 'ex1.wmv', 'ex2.avi']

videoPaths=[];
for thisVideoPath in range(len(videoNames)):
    tmpVideoPath = os.getcwd() + '/MovieStim/' + videoNames[thisVideoPath]
    videoPaths.append(tmpVideoPath)
# load video stime-------------------------------------------------

# open window
win = visual.Window(colorSpace= "rgb255", color = [255, 255, 255], fullscr = True, units='deg')
win.setMouseVisible(False) # hide cursur while running

nInstr=12
InstructionPath = os.getcwd() + '/Instructions/'
instructions = []
for thisInstr in range(1, nInstr+1):
    subInstrImgName = InstructionPath + 'Instruction' + str(thisInstr) + '.png'
    subInstrImg=visual.ImageStim(win, image=subInstrImgName, pos=(0,0), mask = 'none', units='pix', interpolate=True)
    instructions.append(subInstrImg)

# Create your movie stim.
movies=[]
for thisMovie in range(len(videoPaths)):
    tmpMovie = visual.MovieStim2(win, videoPaths[thisMovie],
        size=win.size[0],
        # pos specifies the /center/ of the movie stim location
        pos=[0, 0],
        flipVert=False, flipHoriz=False, loop=False)
    movies.append(tmpMovie)

# create a RatingScale object:
#ratingScale = visual.RatingScale(win, choices=['bad', 'normal', 'good'])
movieStimOrder= "".join(str(i) for i in movieList)
# open text file
dataFile = open(fileName + '__' + movieStimOrder + '.txt', 'w')
dataFile.write('sbj\t' 'age\t' 'BirthDate\t' 'gender\t' 'TrialIdx\t' 'MovieIdx\t' 'startTime\t' 'endTime\n')

# experiment start!!!======================================================================
for thisTrial in range(len(expTrials)):
    
    if thisTrial==0:
        instructions[0].draw()
        win.flip()
        event.waitKeys(keyList = ['space'])
        
        # get time stamp of rest screen
        lineBeforeInst = '\t'.join(str(i) for i in expTrials[thisTrial]) + '\t'
        lineBeforeInst += data.getDateStr(format='%H%M%S') + '\t'
        
        dataFile.write(lineBeforeInst)
        dataFile.flush()
        os.fsync(dataFile)
        
        instructions[1].draw()
        win.flip()
        core.wait(360)
#        core.wait(1)
        
        # get time stamp of ending the rest screen
        lineAfterInst = data.getDateStr(format='%H%M%S') + '\n'
        
        dataFile.write(lineAfterInst)
        dataFile.flush()
        os.fsync(dataFile)
        
        instructions[2].draw()
        win.flip()
        event.waitKeys(keyList = ['space'])
        
        instructions[3].draw()
        win.flip()
        event.waitKeys(keyList = ['space'])
        
    
    if thisTrial>0:
        # get time stamp of starting the movie
        lineBeforeMovie = '\t'.join(str(i) for i in expTrials[thisTrial]) + '\t'
        lineBeforeMovie += data.getDateStr(format='%H%M%S') + '\t'
        
        dataFile.write(lineBeforeMovie)
        dataFile.flush()
        os.fsync(dataFile)
        
        # Start the movie stim by preparing it to play
#        mov=movies[expTrials[thisTrial][movieIdx]-1]
#        print movieList, movieList[thisTrial], expTrials[thisTrial][movieIdx]-1, thisTrial
        while mov.status != visual.FINISHED:
#        clock=core.Clock()
#        while clock.getTime()<1:
            mov.draw()
            win.flip()
            time.sleep(0.001)
            
            # Check for action keys.....
            for key in event.getKeys():
                if key in ['escape', 'q']:
                    win.close()
                    core.quit()
        
        # get time stamp of ending the movie
        lineAfterMovie = data.getDateStr(format='%H%M%S') + '\n'
        
        dataFile.write(lineAfterMovie)
        dataFile.flush()
        os.fsync(dataFile)
        
        instructions[(thisTrial*2)+2].draw()
        win.flip()
        event.waitKeys(keyList = ['space'])
        
        instructions[(thisTrial*2)+3].draw()
        win.flip()
        event.waitKeys(keyList = ['space'])
# experiment end!!!------------------------------------------------------------------------

instructions[11].draw()
win.flip()
event.waitKeys(keyList = ['escape'])