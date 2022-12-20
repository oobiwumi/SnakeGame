# Grid is a 2d list. On this list, a 0 is an open space, a 1 is a closed space, and 2 is the goal

# Paths begins as [[[starting position]]]. it grows to hold the paths to all spaces reachable within a number of
# moves equal to the number of times find_path has been run. when the goal is found, it returns the path that
# reached it

# find_path - finds the path from the points ----------------------------------------------------------------------
def find_path(grid, paths):
    new_paths = []  # a list of all the paths to replace paths
    for path in paths:
        # up, down, left, and right hold the values you would add to the current position to go in that direction
        up = [0, -1]
        down = [0, 1]
        left = [-1, 0]
        right = [1, 0]
        for direction in [up, down, left, right]:
            # direction_position is the new position when a direction is applied
            direction_position = [path[-1][0] + direction[0], path[-1][1] + direction[1]]
            # direction_val is a given by check_new_pos; 0 = valid direction, 1 = invalid direction, 2 = end reached
            direction_val = check_new_pos(grid, direction_position)
            if direction_val != 1:
                new_paths.append(path + [direction_position])
                if direction_val == 2:
                    # if the end is reached, return the path
                    return new_paths[-1]
                # set the explored tile as blocked
                grid[direction_position[0]][direction_position[1]] = 1
    # if there is no possible path, return []
    if not new_paths:
        return []
    # recurse with the new paths
    return find_path(grid, new_paths)


# check_new_pos - checks if a position in the grid is open or the goal ------------------------------------------------
def check_new_pos(grid, pos):
    # return 0 = valid direction, 1 = invalid direction, 2 = end reached
    grid_size_x = len(grid)
    grid_size_y = len(grid[0])

    if pos[0] not in range(grid_size_x) or pos[1] not in range(grid_size_y):
        return 1

    return grid[pos[0]][pos[1]]
