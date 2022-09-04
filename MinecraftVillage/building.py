from mcpi.minecraft import Minecraft
from mcpi.minecraft import Block
from mcpi.minecraft import Vec3
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
        #recursive function to split rooms into smaller rooms
        def buildRooms(buildingWidth, buildingLength, roomHeight, startingLocation):
            
            # blockDoor = Block(64)
            # self.mCon.setBlock(startingLocation.x + 1, startingLocation.y, startingLocation.z, blockDoor)
            # self.mCon.setBlock(startingLocation.x + 1, startingLocation.y + 1, startingLocation.z, blockDoor)
            
            area = buildingWidth * buildingLength
            areaRandomizer = randint(0, 100)
            #splitting stops upon an area of 9 or less, or if the randomizer is less than 10
            if area <= 9 or areaRandomizer < 10:
                return
            #choose either room to be divided in x or y direction
            direction = 1
            #this is in the x direction
            if direction == 1:
                #choose a random point to split the room
                split = randint(1, buildingWidth - 1)
                blockObj = Block(1, 0)
                for y in range(roomHeight):
                    for z in range(1, buildingLength - 1):
                        self.mCon.setBlock(startingLocation.x + split, startingLocation.y + y, startingLocation.z + z, blockObj)
                leftLocation = Vec3(startingLocation.x + 1, startingLocation.y, startingLocation.z)
                rightLocation = Vec3(startingLocation.x + split + 1, startingLocation.y, startingLocation.z)
                
                buildRooms(split, buildingLength, roomHeight, leftLocation)
                buildRooms(buildingWidth - split, buildingLength, roomHeight, rightLocation)
            #else do it in the z direction
            else:
                pass
        
        
        #width is in the x direction, length is in the z direction
        buildingWidth, buildingLength, roomHeight = randint(50, 55), randint(50, 55), randint(3, 5)
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

        buildRooms(buildingWidth, buildingLength, roomHeight, self.startingLocation)