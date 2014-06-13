# This is the game model.  It includes the game class, the charactor class, and the map class, as well as any
# subclasses.

from events import *
from utils import *
from random import randint, choice

DIRECTION_UP = 0
DIRECTION_DOWN = 1
DIRECTION_LEFT = 2
DIRECTION_RIGHT = 3

BLACK = 0, 0, 0
RED = 255, 0, 0
BLUE = 0, 0, 255
GREEN = 0, 255, 0

#------------------------------------------------------------------------------
class Game:
    """..."""

    STATE_PREPARING = 0
    STATE_RUNNING = 1
    STATE_PAUSED = 2

    GAME_CLOCK = 0
    ELEMENT_COUNT = 0
    
    #----------------------------------------------------------------------
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener( self )

        self.Reset()

    #----------------------------------------------------------------------
    def Reset(self):
        self.state = Game.STATE_PREPARING

        self.essences = []
        self.elements = []
        for i in range(20):
            self.essences.append( RandomEssence( self.evManager ) )
            if i % 2 == 1:
                self.elements.append( Element( self.evManager ) )
        self.charactors = [ Soul(self.evManager), self.essences, self.elements ]
        
        self.map = Map( self.evManager )

    #----------------------------------------------------------------------
    def Start(self):
        self.map.Build()
        self.state = Game.STATE_RUNNING
        ev = GameStartedEvent( self )
        self.evManager.Post( ev )

    #----------------------------------------------------------------------
    def Notify(self, event):
        if isinstance( event, TickEvent ):
            if self.state == Game.STATE_PREPARING:
                self.Start()
                
            elif self.state == Game.STATE_RUNNING:

                self.GAME_CLOCK += 1
                if self.GAME_CLOCK == 100:
                    ev = GameClockEvent( self )
                    self.evManager.Post( ev  )
                    self.GAME_CLOCK = 0
                    
                
            elif self.state == Game.STATE_PAUSED:
                return
                

        elif isinstance( event, CharactorCollisionEvent ):
            ClassifyCollisions(self, event.name, event.colliders )

        elif isinstance( event, TogglePauseRequest ):
            if event.pause:
                self.state = Game.STATE_PAUSED
            else: 
                self.state = Game.STATE_RUNNING


#------------------------------------------------------------------------------
class Charactor:
    """..."""

    STATE_INACTIVE = 0
    STATE_ACTIVE = 1
    STATE_TRANSFORMED = 2

    RED_COUNT = 0
    BLUE_COUNT = 0
    GREEN_COUNT = 0

    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener( self )

        self.sector = None
        self.color = BLACK
        self.colorCount = [ Charactor.RED_COUNT, Charactor.BLUE_COUNT, Charactor.GREEN_COUNT ]
        self.state = Charactor.STATE_INACTIVE
        
    #----------------------------------------------------------------------
    def __str__(self):
        return 'Charactor'

    #----------------------------------------------------------------------
    def Move(self, direction):
        if self.state == Charactor.STATE_INACTIVE:
            return

        if self.sector.MovePossible( direction ):
            newSector = self.sector.neighbors[direction]
            self.sector = newSector
            ev = CharactorMoveEvent( self )
            self.evManager.Post( ev )

    #----------------------------------------------------------------------
    def Place(self, sector, color, colorCount):
        self.sector = sector
        self.color = color
        self.colorCount = colorCount
        self.state = Charactor.STATE_ACTIVE
        ev = CharactorPlaceEvent( self )
        self.evManager.Post( ev )
        
    #----------------------------------------------------------------------
    def Absorb(self, color):
        self.Place( self.sector, self.color, self.colorCount  )
    
    #----------------------------------------------------------------------
    def Transform(self):
        self.state = Charactor.STATE_TRANSFORMED
        del self

    #----------------------------------------------------------------------
    def Replace(self):
        self.state = Charactor.STATE_INACTIVE
        del self

    #----------------------------------------------------------------------
    def BuildCore(self, color):
        
        if color == RED and self.BLUE_COUNT == 0:
            if self.GREEN_COUNT > 0:
                self.GREEN_COUNT -= 1
            else:
                self.RED_COUNT += 1
                
        elif color == BLUE and self.GREEN_COUNT == 0:
            if self.RED_COUNT > 0:
                self.RED_COUNT -= 1
            else:
                self.BLUE_COUNT += 1
                
        elif color == GREEN and self.RED_COUNT == 0:
            if self.BLUE_COUNT > 0:
                self.BLUE_COUNT -= 1
            else:
                self.GREEN_COUNT += 1

        self.colorCount = [ self.RED_COUNT, self.BLUE_COUNT, self.GREEN_COUNT ]
        print(self.colorCount)
    
    #----------------------------------------------------------------------   
    def Notify(self, event):
        return


#------------------------------------------------------------------------------
class Soul(Charactor):
    """..."""
    
    def __init__(self, evManager):
        Charactor.__init__(self, evManager)

    #----------------------------------------------------------------------
    def __str__(self):
        return 'Soul'

    #----------------------------------------------------------------------
    def Absorb(self, color):
        self.BuildCore(color)
        self.Place( self.sector, color, self.colorCount )

    #----------------------------------------------------------------------
    def Notify(self, event):
        if isinstance( event, GameStartedEvent ):
            gameMap = event.game.map
            self.Place( gameMap.sectors[choice(gameMap.map_center)], self.color, self.colorCount )

        elif isinstance( event, CharactorMoveRequest ):
            self.Move( event.direction )

    
#------------------------------------------------------------------------------
class Essence(Charactor):
    """..."""

    WILL_PLACE = 0
    
    def __init__(self, evManager):
        Charactor.__init__(self, evManager) 

    #----------------------------------------------------------------------
    def __str__(self):
        return 'Essence'
    
    #----------------------------------------------------------------------
    def Notify(self, event):
        if isinstance( event, GameClockEvent ):
            
            self.WILL_PLACE = randint(1, len(event.game.essences) )
            
            if self.state == Charactor.STATE_INACTIVE and self.WILL_PLACE == 1: 
                gameMap = event.game.map
                self.Place( gameMap.sectors[choice(gameMap.map_border)], self.color, self.colorCount )
                
            elif self.state == Charactor.STATE_ACTIVE:
                direction = randint(0, 3)
                self.Move( direction )
                

#------------------------------------------------------------------------------
class RedEssence(Essence):
    """..."""
    def __init__(self, evManager):
        Essence.__init__(self, evManager)
        self.color = RED

    #----------------------------------------------------------------------
    def __str__(self):
        return 'Red Essence'

    
#------------------------------------------------------------------------------
class BlueEssence(Essence):
    """..."""
    def __init__(self, evManager):
        Essence.__init__(self, evManager)
        self.color = BLUE

    #----------------------------------------------------------------------
    def __str__(self):
        return 'Blue Essence'
    

#------------------------------------------------------------------------------
class GreenEssence(Essence):
    """..."""
    def __init__(self, evManager):
        Essence.__init__(self, evManager)
        self.color = GREEN

    #----------------------------------------------------------------------
    def __str__(self):
        return 'Green Essence'


#------------------------------------------------------------------------------
class RandomEssence(Essence):
    """..."""
    def __init__(self, evManager):
        Essence.__init__(self, evManager)
        self.color = choice([RED, BLUE, GREEN])

    #----------------------------------------------------------------------
    def __str__(self):
        if self.color == RED:
            return 'Red Essence'
        elif self.color == BLUE:
            return 'Blue Essence'
        elif self.color == GREEN:
            return 'Green Essence'
        
              
#------------------------------------------------------------------------------
class Element( Charactor ):
    """..."""
    
    def __init__(self, evManager):
        Charactor.__init__(self, evManager)
        
    #----------------------------------------------------------------------
    def __str__(self):
        if self.color == RED:
            return 'Red Element'
        elif self.color == BLUE:
            return 'Blue Element'
        elif self.color == GREEN:
            return 'Green Element'
        return 'Element'

    #----------------------------------------------------------------------
    def Absorb(self, color):
        self.BuildCore(color)
        self.Place( self.sector, self.color, self.colorCount )


#------------------------------------------------------------------------------
class Map:
    """..."""

    STATE_PREPARING = 0
    STATE_BUILT = 1

    map_center = [44, 45, 54, 55]
    map_border = [0,1,2,3,4,5,6,7,8,9,10,19,20,29,30,39,40,49,50,59,60,69,70,79,80,89,90,91,92,93,94,95,96,97,98,99]
    
    #----------------------------------------------------------------------
    def __init__(self, evManager):
        self.evManager = evManager

        self.state = Map.STATE_PREPARING

        self.sectors = []

    #----------------------------------------------------------------------
    def Build(self):
        for i in range(100):
            self.sectors.append( Sector() )
        for i in range(100):
            if i > 9:
                self.sectors[i].neighbors[DIRECTION_UP] = self.sectors[i-10]
            if i < 90:
                self.sectors[i].neighbors[DIRECTION_DOWN] = self.sectors[i+10]
            if i % 10 != 0:
                self.sectors[i].neighbors[DIRECTION_LEFT] = self.sectors[i-1]
            if i % 10 != 9:
                self.sectors[i].neighbors[DIRECTION_RIGHT] = self.sectors[i+1]

        self.state = Map.STATE_BUILT

        ev = MapBuiltEvent( self )
        self.evManager.Post( ev )

#------------------------------------------------------------------------------
class Sector:
    """..."""
    def __init__(self):

        self.neighbors = list(range(4))

        self.neighbors[DIRECTION_UP] = None
        self.neighbors[DIRECTION_DOWN] = None
        self.neighbors[DIRECTION_LEFT] = None
        self.neighbors[DIRECTION_RIGHT] = None

    #----------------------------------------------------------------------
    def MovePossible(self, direction):
        if self.neighbors[direction]:
            return 1


if __name__ == "__main__":
	print("wasn't expecting that")
