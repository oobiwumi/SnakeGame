# SnakeOOP - A Snake Game
# Olufemi Obiwumi

# IMPORTS
import pygame
import random
import constants as c
import PathFind


# main ################################################################################################################
def main():
    # set up grid and snake
    grid = Grid(c.GRID_SIZE_X, c.GRID_SIZE_Y)
    snake = Snake(grid.grd)

    # set up window
    pygame.init()
    window_size_x = c.TILE_SIZE * grid.size_x + 2
    window_size_y = c.TILE_SIZE * grid.size_y + 2
    window = pygame.display.set_mode((window_size_x, window_size_y))
    pygame.display.set_caption("Snake|  Score = 0")

    # run game loop
    clock = pygame.time.Clock()
    tick_count = 0
    run = True
    while run:
        # manage ticks
        clock.tick(30)
        if tick_count >= c.MOVE_INTERVAL:
            tick_count = 0
        tick_count += 1

        # check for game exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # move snake
        snake.change_direction()
        if tick_count % c.MOVE_INTERVAL == 0:
            game_over_check(snake.check_collision(grid))
            snake.move(grid.grd)
            grid.update(snake.snk)
        pygame.display.set_caption("Snake|  Score =" + str(len(snake.snk)*5-5))
        draw(window, window_size_x, window_size_y, grid.grd)


# draw - draws the grid on the window ---------------------------------------------------------------------------------
def draw(win, win_size_x, win_size_y, grd):
    win.fill((0, 0, 0))
    # draw snake and apple
    for i, _ in enumerate(grd):
        for j, _ in enumerate(grd[i]):
            if grd[i][j] == 1:
                pygame.draw.rect(win, (255, 0, 0), (i * c.TILE_SIZE, j * c.TILE_SIZE, c.TILE_SIZE, c.TILE_SIZE))
            if grd[i][j] == 2:
                pygame.draw.rect(win, (0, 255, 0), (i * c.TILE_SIZE, j * c.TILE_SIZE, c.TILE_SIZE, c.TILE_SIZE))

    # draw tile dividing lines
    # horizontal lines
    place = 0
    for line in range(0, win_size_y, c.TILE_SIZE):
        pygame.draw.line(win, (255, 255, 255), (0, c.TILE_SIZE * place), (win_size_x, c.TILE_SIZE * place), 2)
        place += 1
    place = 0
    # vertical lines
    for line in range(0, win_size_x, c.TILE_SIZE):
        pygame.draw.line(win, (255, 255, 255), (c.TILE_SIZE * place, 0), (c.TILE_SIZE * place, win_size_y), 2)
        place += 1
    pygame.display.update()


# game_over_check - checks if the game has been lost ------------------------------------------------------------------
def game_over_check(collision_type):
    # if there has been no collision, return
    if collision_type == 0:
        return 0
    if collision_type == 1:
        print("\n\nYou hit the wall!!")
    if collision_type == 2:
        print("\n\nYou hit your tail!!")
    print("Game Over :(")
    pygame.quit()
    exit(0)


# print_grid - prints the grid ----------------------------------------------------------------------------------------
def print_grid(grd):
    for row in grd:
        print(row)
    print("\n")


# Class Grid - The grid that the game is placed on ####################################################################
class Grid:
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        # grd is a 2d array that holds the positions of the snake and apple
        self.grd = [[0 for _ in range(self.size_y)] for _ in range(self.size_x)]
        self.apple_position = [random.randint(0, self.size_x-1), random.randint(0, self.size_y-1)]

    # update - updates the positions of the snake and apple on the grid -----------------------------------------------
    def update(self, snk):
        # reset grid
        self.grd = [[0 for _ in range(self.size_y)] for _ in range(self.size_x)]
        # place apple (represented by a 2)
        self.grd[self.apple_position[0]][self.apple_position[1]] = 2
        # place snake (represented by 1s)
        for [x, y] in snk:
            self.grd[x][y] = 1

    # new_apple - creates a new apple ---------------------------------------------------------------------------------
    def new_apple(self, snk):
        self.grd[self.apple_position[0]][self.apple_position[1]] = 0
        good_place = False
        while not good_place:
            self.apple_position = [random.randint(0, self.size_x - 1), random.randint(0, self.size_y - 1)]
            if self.apple_position not in snk:
                good_place = True
                self.grd[self.apple_position[0]][self.apple_position[1]] = 2


# Class Snake - The snake that the player controls ####################################################################
class Snake:
    def __init__(self, grd):
        grid_size_x = len(grd)
        grid_size_y = len(grd[0])
        # snk is an array of the positions of each snake link (treated as a queue)
        self.snk = [[int(grid_size_x/2), int(grid_size_y/2)]]
        # directions_dict is used to transform written directions into values to be applied to snk
        self.directions_dict = {"UP": [0, -1], "RIGHT": [1, 0], "DOWN": [0, 1], "LEFT": [-1, 0]}
        self.direction = "RIGHT"
        self.direction_changed = False  # True if the direction has been changed since the last movement
        self.grow = False  # True if an apple has been eaten
        self.auto = False  # Press the Space key to have the snake move itself
        self.path = []  # used with auto; stores the best path to the apple

    # change_direction - takes in arrow-key input to change the direction of the snake --------------------------------
    def change_direction(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.auto = True
        if not self.auto:
            if keys[pygame.K_LEFT] and not self.direction == "RIGHT" and not self.direction_changed:
                self.direction = "LEFT"
                self.direction_changed = True
            if keys[pygame.K_RIGHT] and not self.direction == "LEFT" and not self.direction_changed:
                self.direction = "RIGHT"
                self.direction_changed = True
            if keys[pygame.K_UP] and not self.direction == "DOWN" and not self.direction_changed:
                self.direction = "UP"
                self.direction_changed = True
            if keys[pygame.K_DOWN] and not self.direction == "UP" and not self.direction_changed:
                self.direction = "DOWN"
                self.direction_changed = True
        else:
            self.auto_change_direction()

    # move - moves the snake in the correct direction -----------------------------------------------------------------
    def move(self, grd):
        head_pos = self.snk[0]
        converted_direction = self.directions_dict[self.direction]
        # if grow is False, remove the snake tail
        if not self.grow:
            self.snk.pop()
        # add a new link in the correct direction
        self.snk.insert(0, [head_pos[0] + converted_direction[0], head_pos[1] + converted_direction[1]])
        self.direction_changed = False
        self.grow = False
        self.path = self.get_path(grd)

    # check_collision - checks if the snake collides with a wall or its tail, or eats an apple ------------------------
    def check_collision(self, grid):
        head_pos = self.snk[0]
        converted_direction = self.directions_dict[self.direction]
        # new_head_pos is where the head is about to go
        new_head_pos = [head_pos[0] + converted_direction[0], head_pos[1] + converted_direction[1]]

        if not new_head_pos[0] in range(grid.size_x) or not new_head_pos[1] in range(grid.size_y):
            return 1
        if new_head_pos in self.snk:
            return 2
        if new_head_pos == grid.apple_position:
            self.grow = True
            grid.new_apple(self.snk)
        return 0

    # get_path - gets the best path to the apple ----------------------------------------------------------------------
    def get_path(self, grd):
        def copy_grid():
            new_grd = []
            for row in grd:
                new_grd.append(row.copy())
            return new_grd
        grd_for_path = copy_grid()
        head_pos = self.snk[0]
        path = PathFind.find_path(grd_for_path, [[head_pos]])
        return path

    # auto_change_direction - used with auto; keeps the snake on the path ---------------------------------------------
    def auto_change_direction(self):
        head_pos = self.snk[0]
        up = [head_pos[0], head_pos[1]-1]
        down = [head_pos[0], head_pos[1]+1]
        left = [head_pos[0]-1, head_pos[1]]
        right = [head_pos[0]+1, head_pos[1]]
        # finds which direction the snake is has to go to stay on the path
        if self.path:
            if up == self.path[1]:
                self.direction = "UP"
            if down == self.path[1]:
                self.direction = "DOWN"
            if left == self.path[1]:
                self.direction = "LEFT"
            if right == self.path[1]:
                self.direction = "RIGHT"
        else:
            # if there is no path to the apple, the snake just avoids dying
            if up not in self.snk and up[1] >= 0:
                self.direction = "UP"
            elif down not in self.snk and down[1] < c.GRID_SIZE_Y:
                self.direction = "DOWN"
            elif left not in self.snk and left[0] >= 0:
                self.direction = "LEFT"
            elif right not in self.snk and right[0] < c.GRID_SIZE_X:
                self.direction = "RIGHT"


#######################################################################################################################
if __name__ == "__main__":
    main()
