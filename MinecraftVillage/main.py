from mcpi.minecraft import Minecraft
from mcpi.minecraft import Vec3
from building import Building
import village
import decoration

if __name__ == "__main__":
    # create minecraft connection
    mc = Minecraft.create()

    player_pos = mc.player.getTilePos()
    otherPosition = Vec3(player_pos.x + 10, player_pos.y, player_pos.z + 10)
    
    testHouse = Building(player_pos.x, otherPosition.x, player_pos.z, otherPosition.z, player_pos.y, mc)

    # fountain = decoration.Fountain(mc, *player_pos)
