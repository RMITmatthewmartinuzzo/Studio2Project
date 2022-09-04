from mcpi.minecraft import Minecraft
from mcpi.minecraft import Block
from mcpi.minecraft import Vec3
from building import Building
from village import Village

if __name__ == "__main__":
    #create minecraft connection
    mc = Minecraft.create()
    
    startingPosition = mc.player.getTilePos()
    
    # village = Village(startingPosition)
    
    building = Building(startingPosition, "pos x", mc)