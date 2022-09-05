# border_size determines the size of the border, a border_size of 10 gives a 10x10 fence
def draw_border(mc, border_size):
    player_x, player_y, player_z = mc.player.getTilePos()
    border_size = 10
    border_width = player_z + border_size
    border_depth = player_x + border_size
    for x in range(player_x, border_depth):
        mc.setBlock(x, mc.getHeight(x, player_z), player_z, 1)
        mc.setBlock(x, mc.getHeight(x, player_z), player_z + border_size, 1)
    for z in range(player_z, border_width + 1):
        mc.setBlock(player_x, mc.getHeight(player_x, z), z, 1)
        mc.setBlock(player_x + border_size, mc.getHeight(player_x, z), z, 1)

# An alternative implementation that is currently not working
# def draw_border(mc):
#     player_x, player_y, player_z = mc.player.getTilePos()
#     border_width = border_depth = 5
#     top_left = (player_x + border_width,
#                 mc.getHeight(player_x + border_width, player_z + border_depth),
#                 player_z + border_depth)
#     bottom_right = (player_x - border_width,
#                     mc.getHeight(player_x - border_width, player_z - border_depth),
#                     player_z - border_depth)
#     print(top_left, bottom_right)
#     for i in range(border_width):
#         mc.setBlock(player_x + i, mc.getHeight(player_x, player_z), player_z + border_depth)
