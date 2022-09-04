from mcpi.minecraft import Minecraft
from mcpi.minecraft import Block
from random import randint

class Building():
    #startingLocation is a tuple of x, y, z
    #direction is either pos/neg x/z
    #mCon is minecraft connection
    def __init__(self, startingLocation, direction, mCon):
        self.mCon = mCon
        
        # self.map = []
        self.startingLocation = startingLocation
        self.direction = direction
        self.height = mCon.getHeight(startingLocation.x, startingLocation.z)
        
        #build Building
        self.build()
    
    def build(self):
        buildingWidth, buildingLength, roomHeight = randint(10, 15), randint(10, 15), randint(3, 5)
        # do i want a map of my building? lets start with no map...
        print(buildingLength, buildingWidth)
        #build to the roof
        for y in range(roomHeight):
            #build front and back walls
            blockObj = Block(1, 0)
            for x in range(buildingWidth):
                self.mCon.setBlock(self.startingLocation.x + x, self.startingLocation.y + y, self.startingLocation.z, blockObj)
                self.mCon.setBlock(self.startingLocation.x + x, self.startingLocation.y + y, self.startingLocation.z + buildingLength - 1, blockObj)
            
            #build side walls    
            for z in range(1, buildingLength - 1):
                self.mCon.setBlock(self.startingLocation.x, self.startingLocation.y + y, self.startingLocation.z + z, blockObj)
                self.mCon.setBlock(self.startingLocation.x + buildingWidth - 1, self.startingLocation.y + y, self.startingLocation.z + z, blockObj)
        
        def buildRooms():
            pass