from mcpi.minecraft import Minecraft
from mcpi.minecraft import Block
from random import randint
from building import Building


class Fountain:
    def __init__(self, mc, x, y, z):
        self.mc = mc
        self.x = x
        self.y = y
        self.z = z

        self.build()

    def build(self):
        # Stone
        for x in range(self.x - 3, self.x + 4):
            for z in range(self.z - 3, self.z + 4):
                if z == self.z - 3 or z == self.z + 3 or x == self.x - 3 or x == self.x + 3:
                    self.mc.setBlock(x, self.mc.getHeight(x, z), z, 0)
                else:
                    self.mc.setBlock(x, self.mc.getHeight(x, z) + 1, z, 1)
        for x in range(self.x - 1, self.x + 2):
            for z in range(self.z - 1, self.z + 2):
                self.mc.setBlock(x, self.mc.getHeight(x, z) + 1, z, 1)
                if (x == self.x - 1 or x == self.x + 1) and (z == self.z - 1 or z == self.z + 1):
                    self.mc.setBlock(x, self.mc.getHeight(x, z) + 1, z, 1)
        self.mc.setBlock(self.x, self.mc.getHeight(x, z) + 2, self.z, 1)
        # Flowing Water
        self.mc.setBlock(self.x, self.mc.getHeight(x, z) + 1, self.z, 8)

