from mcpi.minecraft import Minecraft
from building import Building
import village
import decoration

if __name__ == "__main__":
    # create minecraft connection
    mc = Minecraft.create()

    player_pos = mc.player.getTilePos()

    # fountain = decoration.Fountain(mc, *player_pos)
    village.draw_border(mc, *player_pos, 2)

