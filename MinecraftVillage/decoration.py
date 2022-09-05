from mcpi.minecraft import Minecraft
from mcpi.minecraft import Block
from random import randint
from building import Building


def create_torch(location):
    mc = Minecraft.create()
    mc.setBlock(location, 1)
