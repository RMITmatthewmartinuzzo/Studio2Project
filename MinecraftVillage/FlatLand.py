from mcpi.minecraft import Minecraft
from mcpi.minecraft import Block
from mcpi.minecraft import Vec3


class FlatLand:
    # will store land co-ordinates
    flat_land = set()

    # will mark when a block has been visited
    seen_blocks = set()
    # determines if a region is flat
    FLATNESS_CONST = 100
    MIN_AREA = 25

    def __init__(self, mCon, world_map):
        self.mCon = mCon

        # input a 2d array world_map of heights
        self.world_map = world_map

    def find_flat_land(self):
        for row in range(len(self.world_map)):
            for column in range(len(self.world_map[row])):
                if (row, column) not in self.seen_blocks:
                    new_land = []
                    self.flat_land_helper(row, column, new_land, self.FLATNESS_CONST)
                    if len(new_land) >= self.MIN_AREA:
                        self.flat_land.add(new_land)

    # recursive function to help find flat land with depth first search
    def flat_land_helper(self, row, column, new_land, current_flatness):
        if current_flatness <= 0:
            return
        # we want to store current co-ordinates in new_land
        new_land.append((row, column))
        # mark current block as seen
        self.seen_blocks.add((row, column))
        current_height = self.world_map[row][column]

        # check if we can go down
        if current_height == self.world_map[row + 1][column] and (
        row + 1, column) not in self.seen_blocks and row + 1 < len(self.world_map):
            self.flat_land_helper(row + 1, column, new_land, current_flatness)
        else:
            current_flatness = current_flatness - abs(current_height - self.world_map[row + 1][column])

        # check if we can go up
        if current_height == self.world_map[row - 1][column] and (
        row - 1, column) not in self.seen_blocks and row - 1 > 0:
            self.flat_land_helper(row - 1, column, new_land, current_flatness)
        else:
            current_flatness = current_flatness - abs(current_height - self.world_map[row - 1][column])

        # check if we can go right
        if current_height == self.world_map[row][column + 1] and (
        row, column + 1) not in self.seen_blocks and column + 1 < len(self.world_map[row]):
            self.flat_land_helper(row, column + 1, new_land, current_flatness)
        else:
            current_flatness = current_flatness - abs(current_height - self.world_map[row][column + 1])

        # check if we can go left
        if current_height == self.world_map[row][column - 1] and (
        row, column - 1) not in self.seen_blocks and column - 1 > 0:
            self.flat_land_helper(row, column - 1, new_land, current_flatness)
        else:
            current_flatness = current_flatness - abs(current_height - self.world_map[row][column - 1])

# issues...
# dont think current_flatness is working
