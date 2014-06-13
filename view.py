# This is the view.  Includes the PygameView class, which uses pygame to draw
# the game, as well as helper classes.

from events import *
from model import *

import pygame
from pygame.locals import *

BLACK = 0, 0, 0
WHITE = 255, 255, 255
TRANSPARENT = 0, 0, 0, 0
NAVY_BLUE = 0, 0, 128
DARK_GREEN = 0, 100, 0
FIREBRICK_RED = 178, 34, 34

#------------------------------------------------------------------------------
class PygameView:
    """..."""
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener( self )

        pygame.init()
        self.window = pygame.display.set_mode( (529,529) )
        pygame.display.set_caption( 'Color Game ' )
        self.background = pygame.Surface( self.window.get_size() )
        self.background.fill( WHITE )
        self.window.blit( self.background, (0,0) )
        pygame.display.flip()

        self.backSprites = pygame.sprite.RenderUpdates()
        self.frontSprites = pygame.sprite.RenderUpdates()
        
        self.colliders = []

    #----------------------------------------------------------------------
    def ShowMap(self, gameMap):
        # clear the screen first
        self.background.fill( BLACK )
        self.window.blit( self.background, (0,0) )
        pygame.display.flip()

        # use this squareRect as a cursor and go through the
        # columns and rows and assign the rect
        # positions of the SectorSprites
        squareRect = pygame.Rect( (-41,10, 50,50 ) )

        column = 0
        for sector in gameMap.sectors:
            if column < 10:
                squareRect = squareRect.move( 51,0 )
            else:
                column = 0
                squareRect = squareRect.move( -(51*9), 51 )
            column += 1
            newSprite = SectorSprite( sector, self.backSprites )
            newSprite.rect = squareRect
            newSprite = None
            
    #----------------------------------------------------------------------
    def ShowCharactor(self, charactor):

        if isinstance( charactor, Essence ):
            charactorSprite = EssenceSprite( charactor, self.frontSprites )
        elif isinstance( charactor, Element ):
            charactorSprite = ElementSprite( charactor, self.frontSprites )
        elif isinstance( charactor, Soul ):
            charactorSprite = SoulSprite( charactor, self.frontSprites )
        else:
            charactorSprite = CharactorSprite( charactor, self.frontSprites )

        sector = charactor.sector
        sectorSprite = self.GetSectorSprite( sector )
        charactorSprite.rect.center = sectorSprite.rect.center

    #----------------------------------------------------------------------
    def MoveCharactor(self, charactor):
        charactorSprite = self.GetCharactorSprite( charactor )
        sector = charactor.sector
        sectorSprite = self.GetSectorSprite( sector )
        charactorSprite.moveTo = sectorSprite.rect.center

    #----------------------------------------------------------------------
    def GetCharactorSprite(self, charactor):
        for char in self.frontSprites:
            if hasattr(char, "charactor") and char.charactor == charactor:
                return char
        return None
    
    #----------------------------------------------------------------------
    def GetSectorSprite(self, sector):
        for sect in self.backSprites:
            if hasattr(sect, "sector") and sect.sector == sector:
                return sect

    #----------------------------------------------------------------------
    def DetectCollisions(self, charactor):
        charactorSprite = self.GetCharactorSprite( charactor )

        self.colliders = pygame.sprite.spritecollide( charactorSprite, self.frontSprites, False )
        
        if len(self.colliders) == 2:
            ev = CharactorCollisionEvent(self.colliders)
            self.evManager.Post( ev )
            self.frontSprites.remove(self.colliders)

    #----------------------------------------------------------------------
    def Notify(self, event):
        if isinstance( event, TickEvent ):
            #Draw Everything
            self.backSprites.clear( self.window, self.background )
            self.frontSprites.clear( self.window, self.background )

            self.backSprites.update()
            self.frontSprites.update()

            dirtyRects1 = self.backSprites.draw( self.window )
            dirtyRects2 = self.frontSprites.draw( self.window )

            dirtyRects = dirtyRects1 + dirtyRects2
            pygame.display.update( dirtyRects )

        elif isinstance( event, MapBuiltEvent ):
            gameMap = event.map
            self.ShowMap( gameMap )

        elif isinstance( event, CharactorPlaceEvent ):
            self.ShowCharactor( event.charactor )

        elif isinstance( event, CharactorMoveEvent ):
            self.MoveCharactor( event.charactor )
            self.DetectCollisions(event.charactor)



#------------------------------------------------------------------------------
class SectorSprite(pygame.sprite.Sprite):
    """..."""
    def __init__(self, sector, group = None ):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface( (50,50) )
        self.image.fill( WHITE )
        
        self.sector = sector


#------------------------------------------------------------------------------
class CharactorSprite(pygame.sprite.Sprite):
    """..."""
    def __init__(self, charactor, group = None ):
        pygame.sprite.Sprite.__init__(self, group)

        self.charactor = charactor
        self.moveTo = None
            
    #----------------------------------------------------------------------
    def update(self):
        if self.moveTo:
            self.rect.center = self.moveTo
            self.moveTo = None

#------------------------------------------------------------------------------
class SoulSprite(CharactorSprite):
    def __init__(self, charactor, group = None ):
        CharactorSprite.__init__(self, charactor, group)
        
        charactorSurf = pygame.Surface( (20,20) )
        charactorSurf = charactorSurf.convert_alpha()
        charactorSurf.fill( TRANSPARENT )

        self.image = charactorSurf
        self.rect  = charactorSurf.get_rect()
        pygame.draw.circle( charactorSurf, BLACK, (10,10), 10, 2 )

    #----------------------------------------------------------------------
    def update(self):
        if self.moveTo:
            self.rect.center = self.moveTo
            self.moveTo = None
            
        for j in range(1,11):
            if self.charactor.colorCount[0] % 5 == j:
                pygame.draw.circle( self.image, RED, (10,10), j%5*2, 0 )
            elif self.charactor.colorCount[1] % 5 == j:
                pygame.draw.circle( self.image, BLUE, (10,10), j%5*2, 0 )
            elif self.charactor.colorCount[2] % 5 == j:
                pygame.draw.circle( self.image, GREEN, (10,10), j%5*2, 0 )
                
        if self.charactor.colorCount[0] == 5:
            self.image = pygame.image.load('fire_core.png').convert_alpha()
        #elif self.charactor.colorCount[1] == 5:
        #    self.image = pygame.image.load('water_core.png').convert_alpha()
        #elif self.charactor.colorCount[2] == 5:    
        #    self.image = pygame.image.load('nature_core.png').convert_alpha()
        
#------------------------------------------------------------------------------
class EssenceSprite(SoulSprite):
    """..."""
    def __init__(self, charactor, group = None ):
        SoulSprite.__init__(self, charactor, group)
        pygame.draw.circle( self.image, charactor.color, (10,10), 7, 0 )

        
#------------------------------------------------------------------------------
class ElementSprite(CharactorSprite):
    """..."""
    def __init__(self, charactor, group = None ):
        CharactorSprite.__init__(self, charactor, group )
        self.image = pygame.Surface( (50,50) )
        self.image.fill( charactor.color )
        self.rect = self.image.get_rect()

    #----------------------------------------------------------------------
    def update(self):
        if self.moveTo:
            self.rect.center = self.moveTo
            self.moveTo = None
            
        for j in range(1,11):
            if self.charactor.colorCount[0] % 5 == j:
               pygame.draw.circle( self.image, FIREBRICK_RED, (25,25), j%5*2, 0 )
            elif self.charactor.colorCount[1] % 5 == j:
               pygame.draw.circle( self.image, NAVY_BLUE, (25,25), j%5*2, 0 )
            elif self.charactor.colorCount[2] % 5 == j:
                pygame.draw.circle( self.image, DARK_GREEN, (25,25), j%5*2, 0 )
                
        #if self.charactor.colorCount[0] == 5:            
        #    self.image = pygame.image.load('fire_core.png').convert_alpha()
        #elif self.charactor.colorCount[1] == 5:
        #    self.image = pygame.image.load('water_core.png').convert_alpha()
        #elif self.charactor.colorCount[2] == 5:    
        #    self.image = pygame.image.load('nature_core.png').convert_alpha()      

if __name__ == "__main__":
	print("wasn't expecting that")
