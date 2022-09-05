from mcpi.minecraft import Minecraft
from mcpi.minecraft import Block
from random import randint
from building import Building


def create_torch(location):
    mc = Minecraft.create()
    mc.setBlock(location, 1)
    pass


class Torch:
    def __init__(self, location):
        create_torch(location)


class Lantern:
    def __init__(self, location):
        self.create_lantern(location)

    def create_lantern(self, location):
        mc = Minecraft.create()
        mc.setBlock(location, 1)
        pass
