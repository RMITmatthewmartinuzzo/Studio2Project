# border_size determines the size of the border, a border_size of 10 gives a 10x10 fence
def draw_border(mc, x, y, z, border_size):
    start_x, end_x = x - border_size, x + border_size
    start_z, end_z = z - border_size, z + border_size
    for x in range(start_x, end_x):
        mc.setBlock(x, mc.getHeight(x, z), z + border_size, 1)
        mc.setBlock(x, mc.getHeight(x, z), z - border_size, 1)
        mc.setBlock(x, mc.getHeight(x, z) + 1, z + border_size, 85)
        mc.setBlock(x, mc.getHeight(x, z) + 1, z - border_size, 85)
    for z in range(start_z + 1, end_z):
        mc.setBlock(x, mc.getHeight(x, z), z, 1)
        mc.setBlock(x - (border_size * 2), mc.getHeight(x, z), z, 1)
        mc.setBlock(x, mc.getHeight(x, z) + 1, z, 85)
        mc.setBlock(x - (border_size * 2), mc.getHeight(x, z) + 1, z, 85)

# An alternative implementation that is currently not working

# def draw_border(mc):
#     x, y, z = mc.player.getTilePos()
#     border_width = border_depth = 5
#     top_left = (x + border_width,
#                 mc.getHeight(x + border_width, z + border_depth),
#                 z + border_depth)
#     bottom_right = (x - border_width,
#                     mc.getHeight(x - border_width, z - border_depth),
#                     z - border_depth)
#     print(top_left, bottom_right)
#     for i in range(border_width):
#         mc.setBlock(x + i, mc.getHeight(x, z), z + border_depth)
