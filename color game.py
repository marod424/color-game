# Color Game with MVC (Model, View, Controller) and Mediator (Event Manager) Paradigms

from events import *
from model import *
from view import *
from controller import *

def Debug( msg ):
    print(msg)


#------------------------------------------------------------------------------
class EventManager:
    """this object is responsible for coordinating most communication
    between the Model, View, and Controller."""
    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()

    #----------------------------------------------------------------------
    def RegisterListener( self, listener ):
        self.listeners[ listener ] = 1

    #----------------------------------------------------------------------
    def UnregisterListener( self, listener ):
        if listener in self.listeners:
            del self.listeners[ listener ]

    #----------------------------------------------------------------------
    def Post( self, event ):
        if not ( isinstance(event, (TickEvent, CharactorMoveEvent, GameClockEvent, CharactorMoveRequest)) ):
            Debug( "     Message: " + event.name )
        for listener in self.listeners:
            listener.Notify( event )


#------------------------------------------------------------------------------
def main():
    """..."""
    evManager = EventManager()

    keybd = KeyboardController( evManager )
    spinner = CPUSpinnerController( evManager )
    pygameView = PygameView( evManager )
    game = Game( evManager )

    spinner.Run()

if __name__ == "__main__":
    main()
