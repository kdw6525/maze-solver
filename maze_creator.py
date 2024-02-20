# 
# maze_creator.py
# 
# Generates a maze
# ADD GRID DATA FOR EASY PRINTING!!! AND NEIGHBOR CHECKING!!!!

import random

# random.seed(10)

def get_char(directions):
    n = 0 in directions
    e = 1 in directions
    s = 2 in directions
    w = 3 in directions

    if n and s:
        if e and w:
            return '\u254B'
        elif e and not w:
            return '\u2523'
        elif not e and w:
            return '\u252B'
        else:
            return '\u2503'
    if n and not s:
        if e and w:
            return '\u253B'
        elif e and not w:
            return '\u2517'
        elif not e and w:
            return '\u251B'
        else:
            return '\u2503'
    if not n and s:
        if e and w:
            return '\u2533'
        elif e and not w:
            return '\u250F'
        elif not e and w:
            return '\u2513'
        else:
            return '\u2503'
    else:   
        return '\u2501'

def get_move(row, col, direction):
    # returns new_row, new_col, new_direction
    
    r = random.random()
    if r < .5:
        # go straight
        if direction == 0:
            return row - 1, col, direction
        elif direction == 1:
            return row, col + 1, direction
        elif direction == 2:
            return row + 1, col, direction
        else:
            return row, col - 1, direction
    else:
        # turn left
        if direction == 0:
            return row, col - 1, 3
        elif direction == 1:
            return row - 1, col, 0
        elif direction == 2:
            return row, col + 1, 1
        else:
            return row + 1, col, 2
    
def print_grid_nice(grid):
    # print the grid nicely :)
    s = '|'
    for row in grid:
        for val in row:
            if val == -1:
                s += '   '
            else:
                s += f'{val:2} '
        s += '|\n|'
    s += '|'
    print(s)
    return

def print_grid_lines(grid, connections):
    # print the grid with the line characters
    s = ''
    for row in grid:
        for val in row:
            if val == -1:
                s += ' '
            else:
                s += get_char(connections[val])
        s += '\n'
    print(s)
    return

def write_maze(connections, file='generated1.txt'):
    file = open(file, 'w')
    s = ''
    for key, val in connections.items():
        s += f'{key}'
        for node, direction in val.items():
            s += f' {node} {direction}'
        s += '\n'
    s = s[:len(s)-1]
    s += ' g'

    file.write(s)
    file.close()
    return

def generate_maze():
    # generate 2D array for printing, max of 10x10, row 0 and 11 are for start and end 
    # generate maze 1D array, aka the array needed for solving.
    # 
    # start a bit to the right of the middle of row 11 and work upwards 

    grid = [[-1 for i in range(10)] for x in range(12)]

    # bottom bound to stay above
    bottom = len(grid) - 1
    right = len(grid[0]) - 1

    # starting state conditions
    connections = {0:{0:1}, 1:{0:2, 2:0}, 2:{2:1}}
    direction = 0

    row = len(grid) - 3
    col = len(grid[0]) - 3

    grid[row][col] = 2
    grid[row+1][col] = 1
    grid[row+2][col] = 0

    cur_node = 2
    num_nodes = 3
    finished = False
    while not finished:
        # check if on edge case
        if direction == 1 and col >= right:
            row -= 1
            direction = 0
        elif direction == 2 and row >= bottom:
            col += 1
            direction = 1
        elif direction == 3 and col <= 0:
            row += 1
            direction = 2
        else: 
            row, col, direction = get_move(row, col, direction)

        prev_node = cur_node
        cur_node = grid[row][col]
        if cur_node == -1:
            cur_node = num_nodes
            connections[cur_node] = dict()
            num_nodes += 1
            grid[row][col] = cur_node
        
        connections[prev_node][direction] = cur_node
        connections[cur_node][(direction+2) % 4] = prev_node

        print(f'{str(row)} {str(col)} {str(direction)}')
        if row == 0:
            finished = True

    print_grid_nice(grid)
    print(connections)
    print_grid_lines(grid, connections)
    write_maze(connections, file='generated8.txt')
    return 

def main():
    generate_maze()
    return

if __name__ == '__main__':
    main()
