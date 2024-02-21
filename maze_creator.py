# -*- coding: utf-8 -*-
# maze_creator.py
# 
# Generates a maze
# ADD GRID DATA FOR EASY PRINTING!!! AND NEIGHBOR CHECKING!!!!

import random
import sys

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
    s = ''
    for row in grid:
        for val in row:
            if val == -1:
                s += '   |'
            else:
                s += f'{val:3}|'
        s += '\n'
    print(s)
    return s

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
    return s

def read_maze(file):
    # read file into graph like structure
    # index is vertex, value is edges (edges is an array of tuples)
    # tuples are (neighbor, direction)
    # neighbors are the index and direction is 0, 1, 2, and 3
    #                                         (N, E, S, and W)
    # the state of the solver is the current vertex, direction facing
    # direction is represented as an int so we can define valid directions as
    # d, going straight, or (d + 3) % 4, talking a left turn
    #

    lines = file.readlines()
    maze = []
    connections = {}
    for line in lines:
        data = line.strip().split(' ')
        v = int(data[0])
        g = data[-1] == 'g' 
        edges = data[1:len(data)-1] if g else data[1:]
        edge_dict = {}
        for i in range(0, len(edges), 2):
            edge_dict[int(edges[i+1])] = int(edges[i])
        connections[v] = edge_dict
        maze.append((v, edge_dict, g))
    return maze, connections

def read_grid(file):

    lines = file.readlines()
    grid = []
    for line in lines:
        vals = line.split('|')
        # remove \n val
        vals = vals[:len(vals)-1]

        row = []
        for val in vals:
            if val == '   ':
                row.append(-1)
            else:
                row.append(int(val))
        grid.append(row)
    return grid

def write_maze(connections, file='generated1.txt'):
    file = open(file, 'w')
    s = ''
    for key, val in connections.items():
        s += f'{key}'
        for node, direction in val.items():
            s += f' {direction} {node}'
        s += '\n'
    s = s[:len(s)-1]
    s += ' g'

    file.write(s)
    file.close()
    return

def write_file(s, file):
    file = open(file, 'w')
    file.write(s)
    file.close()
    return

def generate_maze():
    # generate 2D array for printing, max of 10x10, row 0 and 11 are for start and end 
    # generate maze 1D array, aka the array needed for solving.
    # 
    # start a bit to the right of the middle of row 11 and work upwards 

    # edit in code to adjust maze size
    rows = 21
    columns = 20

    grid = [[-1 for i in range(columns)] for x in range(rows)]

    # bottom bound to stay above
    bottom = len(grid) - 2
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

        if row == 0:
            finished = True

    return grid, connections

def make_path(parents, v):
    # make a path out of parent dictionary
    if v not in parents:
        return [v[0]]
    else:
        return make_path(parents, parents[v]) + [v[0]]

def get_moves(v, dir):
    # v: vertex
    # dir: direction
    # only check 2 directions to go
    # that is matching direction and (dir + 3) % 4
    moves = []
    # straight?
    if dir in v[1]:
        # (index, direction)
        moves.append((v[1][dir], dir))

    # left turn?
    if (dir+3)%4 in v[1]:
        # (index, direction)
        moves.append((v[1][(dir+3)%4], (dir+3)%4))

    return moves

def maze_scorer(maze, pos=0):
    # just using bfs because I don't know how using my modified search will work here.
    # maze: array containing the maze structure, a list containing vetecies and their edges
    # pos: starting index in the maze
    #
    # perform a bfs search
    # 

    # pos pointing north, initial conditions
    dir = 0
    state = (pos, dir)
    q = [state]

    # create sets
    parents = {}
    visited_state = set()
    visited_state.add(state)
    end_or_loop = 0
    num_visited = 0
    path = []

    while q:
        # (index, direction)
        state = q.pop(0)
        dir = state[1]

        # vertext details
        # index, edges, goal?
        v = maze[state[0]]
        goal = v[2]
        
        if goal:
            if num_visited == 0:
                num_visited = len(visited_state)
            path.append(make_path(parents, state))
        moves = get_moves(v, dir)
        if moves:
            for move in moves:
                if move not in visited_state:
                    q.append(move)
                    visited_state.add(move)
                    parents[move] = state
        else:
            end_or_loop += 1
    
    # scoring mumbo jumbo!!! 
    # Honestly, this type of maze is incredibly easy to solve since there are only 1 or 2 branching paths per intersection
    # So I'm going to measure fun instead of difficulty
    # I want to consider:
    # 1. number of states visited (this includes possible moves at the end, so this will consider the # of branches) before first path found
    # 2. number of states along path
    # 3. number of nodes in maze (probably scaled down considering the lenghth of path) 
    # 4. number of dead ends/loops, essentially equivalent in this maze. If you get to a spot that's been visited already it's a loop (If I've made good edits)
    # maybe I should multiply some of these stats together? and add other stats together?
    
    # scale this depending on how big the first path found was, there should be at least one path found, if there wasn't thats an issue lol
    # I'm gonna subtract this from the score because more nodes = tedious or clutter
    num_nodes_stat = len(maze) / (len(maze) // len(path[0]))

    score = len(visited_state) + len(path) - num_nodes_stat - (end_or_loop // 2) 

    return path, score

def main():
    print(sys.argv)
    if len(sys.argv) == 1:
        print('give command plz')
        exit()
    elif sys.argv[1] == 'create':
        num = sys.argv[2]
        print(num)
        grid, connections = generate_maze()
        str_grid = print_grid_nice(grid)
        write_maze(connections, file=f'generated{num}.txt')
        write_file(str_grid, file=f'grid{num}.txt')
        line_grid = print_grid_lines(grid, connections)

        f = open(f'generated{num}.txt')
        maze, bleh = read_maze(f)
        f.close()

        path, score = maze_scorer(maze)
        print(path)
        print(score)
        # print(connections)
    elif sys.argv[1] == 'score':
        num = sys.argv[2]

        f = open(f'generated{num}.txt')
        maze, connections = read_maze(f)
        f.close()
        
        f = open(f'grid{num}.txt')
        grid = read_grid(f)
        f.close()

        str_grid = print_grid_nice(grid)
        line_grid = print_grid_lines(grid, connections)

        path, score = maze_scorer(maze)
        print(path)
        print(score)
    return

if __name__ == '__main__':
    main()
