#
# ENSICAEN
# École Nationale Supérieure d'Ingénieurs de Caen
# 6 Boulevard Maréchal Juin
# F-14050 Caen Cedex France
#
# Artificial Intelligence 2I1AE1
#

#
# @file agents.py
#
# @author Régis Clouard.
#

from __future__ import print_function
import random
import copy
import sys
import utils

class Agent:
    """
    The base class for various flavors of the agent.
    This an implementation of the Strategy design pattern.
    """
    isLearningAgent = False

    def init( self, gridSize ):
        raise Exception("Invalid Agent class, init() not implemented")

    def think( self, percept, action, score, isTraining = False ):
        raise Exception("Invalid Agent class, think() not implemented")

def pause( text):
    if sys.version_info.major >= 3:
        input(text)
    else:
        raw_input(text)

class DummyAgent( Agent ):
    """
    An example of simple Wumpus hunter brain: acts randomly...
    """

    def init( self, gridSize ):
        pass

    def think( self, percept, action, score, isTraining = False ):
        return random.choice(['shoot', 'grab', 'left', 'right', 'forward', 'forward'])


class HumanAgent( Agent ):
    """
    Game version using keyboard to control the agent
    """
 
    def init( self, gridSize ):
        self.state = State(gridSize)
        self.isStarted = False

    def think( self, percept, action, score ):
        """
        Returns the best action regarding the current state of the game.
        Available actions are ['left', 'right', 'forward', 'shoot', 'grab', 'climb'].
        """
        if not self.isStarted:
            self.isStarted = True
            return GRAB
        else:
            self.state.updateStateFromPercepts(percept, score)
            self.state.printWorld()
            key = input("Choose action (l, r, f, s, g, c) ? ")
            if key=='r': action = RIGHT
            elif key=='f': action = FORWARD
            elif key=='c': action = CLIMB
            elif key=='s': action = SHOOT
            elif key=='g': action = GRAB
            else: action = LEFT
            self.state.updateStateFromAction(action)
            return action

#######
####### Exercise: Rational Agent
#######
class RationalAgent( Agent ):
    """
    Your smartest Wumpus hunter brain.
    """ 

    def avoid_wall(self, i):
        if self.avoiding_wall in [0, 1]:
            action = RIGHT
        return action

    def turn_around_monster(self, i): 
        if i == 4:
            action = RIGHT
        elif i == 3:
            action = RIGHT
        elif i == 2: 
            action = FORWARD
        elif i == 1:
            action = LEFT
        elif i == 0:
            action = FORWARD
        elif i == -1:
            action = LEFT
        elif i == -2:
            action = LEFT
        return action

    def turn_around_pit(self, i): 
        if self.directional == 1:
            if i == 4:
                action = RIGHT
            elif i == 3:
                action = RIGHT
            elif i == 2: 
                action = FORWARD
            elif i == 1:
                action = LEFT
            elif i == 0:
                action = FORWARD
            elif i == -1:
                action = LEFT
        elif self.directional == 3:
            if i == 4:
                action = LEFT
            elif i == 3:
                action = LEFT
            elif i == 2: 
                action = FORWARD
            elif i == 1:
                action = RIGHT
            elif i == 0:
                action = FORWARD
            elif i == -1:
                action = RIGHT
        return action
    
    def skip_pit(self, i):
        if i == 7:
            action = RIGHT
        elif i == 6:
            action = FORWARD
        elif i == 5:
            action = LEFT
        elif i == 4:
            action = FORWARD
        elif i == 3:
            action = FORWARD
        elif i == 2:
            action = LEFT
        elif i == 1:
            action = FORWARD
        elif i == 0:
            action = RIGHT
            self.skipping = "pitJustSkipped"
        return action
    
    def figuring_out_the_pit(self, percept):
        if percept.breeze:
            if self.directional == 1:
                self.state.setCell(self.state.posx + 1, self.state.posy, PIT)
            elif self.directional == 3:
                self.state.setCell(self.state.posx - 1, self.state.posy, PIT)
                print('pit added')
                self.skipping = ''
            return 'THIS'
        else:
            if self.directional == 1:
                self.state.setCell(self.state.posx + 2, self.state.posy - 1, PIT)
            elif self.directional == 3:
                self.state.setCell(self.state.posx - 2, self.state.posy + 1, PIT)
            return 'OTHER'
    
    def figuring_out_the_monster(self, percept):
        if percept.stench:
            return 'THIS'
        else:
            return 'OTHER'
   
    def go_back(self, i):
        if self.directional == 1:
            if i == 4:
                action = LEFT
            elif i == 3:
                action = LEFT
            elif i == 2: 
                action = FORWARD
            elif i == 1:
                action = RIGHT
            elif i == 0:
                action = FORWARD
        elif self.directional == 3:
            if i == 4:
                action = RIGHT
            elif i == 3:
                action = RIGHT
            elif i == 2: 
                action = FORWARD
            elif i == 1:
                action = LEFT
            elif i == 0:
                action = FORWARD
        return action
    
    def avoid_wall(self, i):
        if i == 1:
            action = RIGHT
        elif i == 0:
            action = FORWARD
        elif i == -1:
            action = RIGHT
            self.wall_avoided = True
            if self.directional == 1:
                self.directional = 3
            elif self.directional == 3:
                self.directional = 1
        return action
    
    def init( self, gridSize ):
        self.state = State(gridSize)
        self.turning_around = -2
        self.going_back = -1
        self.skipping_pit = -1
        self.avoiding_wall = -2
        self.directional = 1
        self.wall_avoided = False
        self.fighting = -3
        self.skipping = ""
        self.kill = "Dontshoot"
        " *** YOUR CODE HERE ***"
        
    def isNextToWall(self):
        return (self.state.posx == self.state.size - 2 or self.state.posy == self.state.size - 2) and (self.wall_avoided == False)
    
    def think( self, percept, action, score ):
        """
        Returns the best action regarding the current state of the game.
        Available actions are ['left', 'right', 'forward', 'shoot', 'grab', 'climb'].
        """
        " *** YOUR CODE HERE ***"
        self.state.updateStateFromPercepts(percept, score)
      
        if self.turning_around > -2 :
            action = self.turn_around_pit(self.turning_around)
            self.turning_around = self.turning_around - 1
            if self.turning_around == -2:
                self.figuring_out_the_pit(percept)
                self.going_back = 4
                action = ''
            self.state.updateStateFromAction(action)
            return action

        if self.going_back > -1:
            action = self.go_back(self.going_back)
            self.going_back = self.going_back - 1
            self.state.updateStateFromAction(action)
            if(self.going_back == -1) and self.state.getCell(self.state.posx + 1, self.state.posy) == PIT:
                self.skipping_pit = 7
            
            return action
        
        if self.skipping_pit > -1 :
            action = self.skip_pit(self.skipping_pit)
            self.skipping_pit = self.skipping_pit -1
            self.state.updateStateFromAction(action)
            return action

        if self.avoiding_wall > -2:
            action = self.avoid_wall(self.avoiding_wall)
            self.avoiding_wall = self.avoiding_wall - 1
            self.state.updateStateFromAction(action)
            return action
        
        if self.fighting > -3 :
            action = self.turn_around_monster(self.fighting)
            self.fighting = self.fighting - 1
            if self.fighting == -3:
                if self.figuring_out_the_monster(percept) == 'THIS':
                    action = SHOOT
                    self.kill = "KILLED"
                else:
                    action = ''
                    self.kill = "KILL"
                self.going_back = 3
            self.state.updateStateFromAction(action)
            return action

        if percept.breeze and self.skipping != "pitJustSkipped" and not self.state.canGoForward():
            self.turning_around = 4
            action = ''
        elif percept.stench:
            if self.kill == "KILL":
                action = SHOOT
            else:
                if self.kill != "KILLED":
                    self.fighting = 4
                    action = ''
        elif self.isNextToWall() :
            self.avoiding_wall = 1
            action = ''
        else:
            action = FORWARD
            self.skipping = ''
            self.wall_avoided = False
        self.state.updateStateFromAction(action)

        return action


#######
####### Exercise: Learning Agent
#######
class LearningAgent( Agent ):
    """
    Your smartest Wumpus hunter brain.
    """
    isLearningAgent = True
    
    def init( self, gridSize ):

        self.state = State(gridSize)
        " *** YOUR CODE HERE ***"

    def think( self, percept, action, score, isTraining ):
        """
        Returns the best action regarding the current state of the game.
        Available actions are ['left', 'right', 'forward', 'shoot', 'grab', 'climb'].
        """
        " *** YOUR CODE HERE ***"

#######
####### Exercise: Environment
#######

WALL='#'
UNKNOWN='?'
WUMPUSP='w'
WUMPUS='W'
PITP='p'
PIT='P'
WUMPUSPITP='x'
SAFE=' '
VISITED='.'
GOLD='G'

RIGHT  ='right'
LEFT = 'left'
FORWARD = 'forward'
CLIMB = 'climb'
SHOOT = 'shoot'
GRAB = 'grab'

DIRECTION_TABLE = [(0, -1), (1, 0), (0, 1), (-1, 0)] # North, East, South, West

class State():
    def __init__( self, gridSize ):
        self.size = gridSize
        self.worldmap = [[((y in [0, gridSize - 1] or  x in [0, gridSize - 1]) and WALL) or UNKNOWN
                          for x in range(gridSize) ] for y in range(gridSize)]
        self.direction = 1
        self.posx = 1
        self.posy = 1
        self.action = 'left'
        self.setCell(self.posx, self.posy, self.agentAvatar())
        self.wumpusIsKilled = False
        self.goldIsGrabbed = False
        self.wumpusLocation = None
        self.arrowInventory = 1
        self.score = 0
        " *** YOUR CODE HERE ***"

    def printWorld( self ):
        """
        For debugging purpose.
        """
        for y in range(self.size):
            for x in range(self.size):
                print(self.getCell(x, y) + " ", end=' ')
            print()

    def getCell( self, x, y ):
        return self.worldmap[x][y]

    def setCell( self, x, y, value ):
        self.worldmap[x][y] = value

    def getCellNeighbors( self, x, y ):
        return [(x + dx, y + dy) for (dx,dy) in DIRECTION_TABLE]
    
    def getForwardPosition( self, x, y, direction ):
        (dx, dy) = DIRECTION_TABLE[direction]
        return (x + dx, y + dy)

    def fromDirectionToAction( self, direction ):
        if direction == self.direction:
            return FORWARD
        elif direction == (self.direction + 1) % 4:
            return RIGHT
        elif direction == (self.direction + 2) % 4:
            return RIGHT
        else:
            return LEFT

    def canGoForward(self):
        x1, y1 = self.getForwardPosition(self.posx, self.posy, self.direction)
        square = self.getCell(x1, y1)
        return square == VISITED

    def isGoal(self):
        return (self.posx, self.posy) == (1,1) and self.arrowInventory == 0 and self.goldIsGrabbed

    def updateStateFromPercepts( self, percept, score ):
        """
        Updates the current environment with regards to the percept information.
        """
        self.score = score;

        # Update neighbours
        self.setCell(self.posx, self.posy, VISITED)

        # Update location of Pits and Wumpus
        for (x, y) in self.getCellNeighbors(self.posx, self.posy):
            square = self.getCell(x, y)
            if square == WALL or square == VISITED or square == SAFE or square == WUMPUS or square == PIT:
                continue
            if percept.stench and percept.breeze:
                if square == UNKNOWN:
                    if self.wumpusLocation == None:
                        self.setCell(x,y, WUMPUSPITP)
                    else:
                        self.setCell(x,y, PITP)
            elif percept.stench and not percept.breeze:
                if square == UNKNOWN or square == WUMPUSPITP:
                    if  self.wumpusLocation == None:
                        self.setCell(x, y, WUMPUSP)
                    else:
                        self.setCell(x, y, SAFE)
                elif square == PITP:
                    self.setCell(x, y, SAFE)
            elif not percept.stench and percept.breeze:
                if square == UNKNOWN  or square == WUMPUSPITP:
                    self.setCell(x, y, PITP)
                elif square == WUMPUSP:
                    self.setCell(x, y, SAFE)
            else:
                self.setCell(x, y, SAFE)

        # Gold
        if percept.glitter:
            self.setCell(self.posx, self.posy, GOLD)

        # Wumpus killed
        if percept.scream:
            self.wumpusIsKilled = True
            # Remove WUMPUS from all squares
            for (x, y) in self.getCellNeighbors(self.posx, self.posy):
                square = self.getCell(x, y)
                if square == WUMPUSP or square == WUMPUS:
                    self.setCell(x, y, SAFE)
                elif square == WUMPUSPITP:
                    self.setCell(x, y, PITP)

        # Confirm Wumpus or Pit
        for y in range(self.size):
            for x in range(self.size):
                if self.getCell(x, y) == VISITED:
                    # Count the number WUMPUSP in neighborhood
                    wumpusCount = 0
                    for (px, py) in self.getCellNeighbors(x, y):
                        if self.getCell(px, py) in [WUMPUSP, WUMPUSPITP]:
                            wumpusCount += 1
                    if wumpusCount == 1: # Confirm WUMPUSP as WUMPUS and discard other WUMPUSP
                        for (px, py) in self.getCellNeighbors(x, y):
                            if self.getCell(px, py) in [WUMPUSP, WUMPUSPITP]:
                                self.setCell(px, py, WUMPUS)
                                self.wumpusLocation = (px, py)
                                for y1 in range(self.size):
                                    for x1 in range(self.size):
                                        if self.getCell(x1, y1) == WUMPUSP:
                                            self.setCell(x1, y1, SAFE)
                                        if self.getCell(x1, y1) == WUMPUSPITP:
                                            self.setCell(x1, y1, PITP)
                                break;
                    # Count the number of PITP in neighborhood
                    pitCount = 0
                    for (px, py) in self.getCellNeighbors(x, y):
                        if self.getCell(px, py) in [PIT, PITP, WUMPUSPITP]:
                            pitCount += 1
                    if pitCount == 1:
                        for (px, py) in self.getCellNeighbors(x, y):
                            if self.getCell(px, py) in [PIT, PITP, WUMPUSPITP]:
                                self.setCell(px, py, PIT)
                                break;
        return self
    
    def updateStateFromAction( self, action ):
        self.action = action
        if self.action == GRAB:
            self.goldIsGrabbed = True
            self.setCell(self.posx, self.posy, VISITED)
        elif self.action == LEFT:
            self.direction = (self.direction + 3) % 4
        elif self.action == RIGHT:
            self.direction = (self.direction + 1) % 4
        elif self.action == FORWARD:
            self.setCell(self.posx, self.posy, VISITED)
            self.posx, self.posy = self.getForwardPosition(self.posx, self.posy, self.direction)
        self.setCell(self.posx, self.posy, self.agentAvatar())

    def agentAvatar( self ):
        if self.direction == 0:
            return "^"
        elif self.direction == 1:
            return ">"
        elif self.direction == 2:
            return "v"
        else:
            return "<"

    def getWumpusPlace( self ):
        return self.wumpusLocation

    def isShootingPositionFor( self, x, y ):
        if self.direction == 0 and self.posx == x and self.posy > y:
            return True
        if self.direction == 1 and self.posy == y and self.posx < x:
            return True
        if self.direction == 2 and self.posx == x and self.posy < y:
            return True
        if self.direction == 3 and self.posy == y and self.posx > x:
            return True
        return False
