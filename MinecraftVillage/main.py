from mcpi.minecraft import Minecraft
from building import Building
from village import Village
from decoration import Torch

if __name__ == "__main__":
    # create minecraft connection
    mc = Minecraft.create()

    starting_position = mc.player.getTilePos()

    # village = Village(starting_position)

    building = Building(starting_position, "pos x", mc)
