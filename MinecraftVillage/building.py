from mcpi.minecraft import Minecraft
from mcpi.minecraft import Block
from mcpi.minecraft import Vec3
from random import randint


class Building:
    # building input is going to be two co-ordinates
    # building should store one co-ordinate (location of front door)

    def __init__(self, x1, x2, z1, z2, height, mc):
        self.mc = mc

        self.x1 = x1
        self.x2 = x2
        self.z1 = z1
        self.z2 = z2
        self.height = height

        # build Building
        self.build()

    def build(self):
        pass
    
    
    def recurssive_build(self, x1, x2, z1, z2, height):
        pass
        

        # # recursive function to split rooms into smaller rooms
        # def build_rooms(building_width, building_length, room_height, starting_location):

        #     # blockDoor = Block(64)
        #     # self.mc.setBlock(starting_location.x + 1, starting_location.y, starting_location.z, blockDoor)
        #     # self.mc.setBlock(starting_location.x + 1, starting_location.y + 1, starting_location.z, blockDoor)

        #     area = building_width * building_length
        #     area_randomizer = randint(0, 100)
        #     # splitting stops upon an area of 9 or less, or if the randomizer is less than 10
        #     if area <= 9 or area_randomizer < 10:
        #         return
        #     # choose either room to be divided in x or y direction
        #     direction = 1
        #     # this is in the x direction
        #     if direction == 1:
        #         # choose a random point to split the room
        #         split = randint(1, building_width - 1)
        #         block_obj = Block(1, 0)
        #         for y in range(room_height):
        #             for z in range(1, building_length - 1):
        #                 self.mc.setBlock(starting_location.x + split, starting_location.y + y,
        #                                     starting_location.z + z, block_obj)
        #         left_location = Vec3(starting_location.x + 1, starting_location.y, starting_location.z)
        #         right_location = Vec3(starting_location.x + split + 1, starting_location.y, starting_location.z)

        #         build_rooms(split, building_length, room_height, left_location)
        #         build_rooms(building_width - split, building_length, room_height, right_location)
        #     # else do it in the z direction
        #     else:
        #         pass

        # # width is in the x direction, length is in the z direction
        # building_width, building_length, room_height = randint(50, 55), randint(50, 55), randint(3, 5)
        # # do I want a map of my building? let's start with no map...
        # print(building_length, building_width)
        # # build to the roof
        # for y in range(room_height):
        #     # build front and back walls
        #     block_obj = Block(1, 0)
        #     for x in range(building_width):
        #         self.mc.setBlock(self.startingLocation.x + x, self.startingLocation.y + y, self.startingLocation.z,
        #                             block_obj)
        #         self.mc.setBlock(self.startingLocation.x + x, self.startingLocation.y + y,
        #                             self.startingLocation.z + building_length - 1, block_obj)

        #     # build side walls
        #     for z in range(1, building_length - 1):
        #         self.mc.setBlock(self.startingLocation.x, self.startingLocation.y + y, self.startingLocation.z + z,
        #                             block_obj)
        #         self.mc.setBlock(self.startingLocation.x + building_width - 1, self.startingLocation.y + y,
        #                             self.startingLocation.z + z, block_obj)

        # build_rooms(building_width, building_length, room_height, self.startingLocation)
