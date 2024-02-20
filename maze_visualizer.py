# -*- coding: utf-8 -*-
# using box characters!
# https://www.w3schools.com/charsets/ref_utf_box.asp
# 
# maze_visualizer.py
# 
# a function to print out the maze in a readable format :)
#
#
# BUG: EDGES THAT TRAVERSE MORE THAN 2 IN A DIRECTION ARE A PROBLEM
# TODO FIX: ADD GRID DATA INTO THE MAZE STRUCTURE

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
    for line in lines:
        data = line.strip().split(' ')
        v = int(data[0])
        g = data[-1] == 'g' 
        edges = data[1:len(data)-1] if g else data[1:]
        edge_dict = {}
        for i in range(0, len(edges), 2):
            edge_dict[int(edges[i+1])] = int(edges[i])

        maze.append((v, edge_dict, g))
    return maze

def add_left(matrix):
    return [[' '] + row for row in matrix]

def add_right(matrix):
    return [row + [' '] for row in matrix]

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
        return '\u2500'

def get_char_neighbors(state, x, y):
    # get the character to put into matrix and the next neighbors
    directions = set()
    neighbors = []
    for direction, neighbor in state[1].items():
        directions.add(direction)
        if direction == 0:
            neighbors.append((neighbor, (x, y-1)))
        elif direction == 1:
            neighbors.append((neighbor, (x+1, y)))
        elif direction == 2:
            neighbors.append((neighbor, (x, y+1)))
        else:
            neighbors.append((neighbor, (x-1, y)))

    return get_char(directions), neighbors
    # return str(state[0]), neighbors

def get_matrix(maze):
    # (hardest part of the function)
    # start with the end node and work backwards, end node is the goal
    
    # start with 1x1 matrix
    matrix = [[' ']]
    left = 0
    right = 0
    bottom = 0

    # perform bfs backwards to visit all nodes/intersections
    visited = set()
    q = [(maze[-1], (0,0))]
    while q:
        node, cords = q.pop(0)
        visited.add(node[0])
        x = cords[0]
        y = cords[1]

        if x < left:
            matrix = add_left(matrix)
            left -= 1
        elif x > right:
            matrix = add_right(matrix)
            right += 1

        if y > bottom:
            matrix.append([' '] * ((right - left) + 1))
            bottom += 1

        char, neighbors = get_char_neighbors(node, x, y)
        matrix[y][x - left] = char

        print(neighbors)
        for neighbor in neighbors:
            if neighbor[0] not in visited:
                q.append((maze[neighbor[0]], neighbor[1]))

    return matrix

def show_maze():
    # steps:
    # 1. put nodes into a n x m matrix
    # 2. check blank spots for if between
    # 3. put a s below start and an g above goal

    
    
    return



def main():
    file = open('maze1.txt')
    maze = read_maze(file)

    matrix = get_matrix(maze)
    s = ''
    for row in matrix:
        
        for val in row:
            s += val
        s += '\n'
        print(row)
    print(s)

    print(get_char_neighbors(maze[4], x=0, y=4))
    return

if __name__ == '__main__':
    main()