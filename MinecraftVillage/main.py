from mcpi.minecraft import Minecraft
from building import Building
import village

if __name__ == "__main__":
    # create minecraft connection
    mc = Minecraft.create()

    starting_position = mc.player.getTilePos()

    village.create_village(mc, 10)

    # building = Building(starting_position, "pos x", mc)
