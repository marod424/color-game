# Utils: utility functions that don't inherently belong in the model,
# view, or controller.

#----------------------------------------------------------------------
def ClassifyCollisions(game, name, colliders):

    # Note: Collision name --> "colliders[0] - colliders[1] - ... - colliders[N] Collision"
    #       where N equals len(colliders)-1

    
    # ----- Essence - Essence Collisions -----
    if (name == "Red Essence - Red Essence Collision" or name == "Blue Essence - Blue Essence Collision" or
        name == "Green Essence - Green Essence Collision"):

        game.charactors[2][game.ELEMENT_COUNT].Place(colliders[0].charactor.sector, colliders[0].charactor.color,
                                                     colliders[0].charactor.colorCount)
        game.ELEMENT_COUNT += 1
        
        colliders[0].charactor.Transform()
        colliders[1].charactor.Transform()
        
    elif (name == "Red Essence - Blue Essence Collision" or name == "Green Essence - Red Essence Collision"
          or name == "Blue Essence - Green Essence Collision"):

        colliders[0].charactor.Replace()
        colliders[1].charactor.Absorb( colliders[0].charactor.color )

    elif (name == "Blue Essence - Red Essence Collision" or name == "Red Essence - Green Essence Collision"
          or name == "Green Essence - Blue Essence Collision"):

        colliders[0].charactor.Absorb( colliders[1].charactor.color )
        colliders[1].charactor.Replace()
        
    # ----- Soul - Essence Collisions -----
    elif (name == "Soul - Red Essence Collision" or name == "Soul - Blue Essence Collision" or
          name == "Soul - Green Essence Collision"):

        colliders[0].charactor.Absorb( colliders[1].charactor.color )
        colliders[1].charactor.Replace()

    elif (name == "Red Essence - Soul Collision" or name == "Green Essence - Soul Collision" or
          name == "Blue Essence - Soul Collision"):

        colliders[0].charactor.Replace()
        colliders[1].charactor.Absorb( colliders[0].charactor.color )

    # ----- Soul - Element Collisions -----
    elif (name == "Soul - Red Element Collision" or name == "Soul - Blue Element Collision" or
          name == "Soul - Green Element Collision" or name == "Red Element - Soul Collision" or
          name == "Blue Element - Soul Collision" or name == "Green Element - Soul Collision"):

        colliders[0].charactor.Absorb(  colliders[1].charactor.color )
        colliders[1].charactor.Absorb(  colliders[0].charactor.color )
        
    # ----- Essence - Element Collisions -----
    elif (name == "Red Element - Red Essence Collision" or name == "Blue Element - Blue Essence Collision"
          or name == "Green Element - Green Essence Collision" or name == "Red Element - Green Essence Collision"
          or name == "Blue Element - Red Essence Collision" or name == "Green Element - Blue Essence Collision"
          or name == "Red Element - Blue Essence Collision" or name == "Blue Element - Green Essence Collision"
          or name == "Green Element - Red Essence Collision"):

        colliders[0].charactor.Absorb( colliders[1].charactor.color )
        colliders[1].charactor.Replace()

    elif (name == "Red Essence - Red Element Collision" or name == "Blue Essence - Blue Element Collision"
          or name == "Green Essence - Green Element Collision" or name == "Green Essence - Red Element Collision"
          or name == "Red Essence - Blue Element Collision" or name == "Blue Essence - Green Element Collision"
          or name == "Blue Essence - Red Element Collision" or name == "Green Essence - Blue Element Collision"
          or name == "Red Essence - Green Element Collision"):

        colliders[0].charactor.Replace()
        colliders[1].charactor.Absorb( colliders[0].charactor.color )
        
    else:
        print("Unknown Collision: " + name)
        
            
if __name__ == "__main__":
	print("wasn't expecting that")
