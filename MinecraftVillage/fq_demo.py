from mcpi import minecraft
from fast_query import *

mc = minecraft.Minecraft.create()

px, py, pz = mc.player.getTilePos()
sz = 25

test_cuboid = Cuboid((px - sz, px + sz + 1), (0,1), (pz - sz, pz + sz + 1))
hm = fq_heights(test_cuboid)
fq_draw_heights(hm, test_cuboid.x_range, test_cuboid.z_range)