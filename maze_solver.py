# maze_solver.py
#
# solves No right turns! maze using bfs, dfs and a modified search algorithm
# 
# python maze_solver.py maze 
#

import re

def read_maze(file):
    # read file into graph like structure
    # index is vertex, value is edges (edges is an array of tuples)
    # tuples are (neighbor, direction)
    # neighbors are the index and direction is 0, 1, 2, and 3
    #                                         (N, E, S, and W)

    lines = file.readlines()
    maze = []
    for line in lines:
        data = re.match('(-?[0-9]*) ([\(-?[0-9]*,[0-4]\)(,\(-?[0-9]*,[0-4]\))*])( g)?', line)
        v, e, g = data[1], data[2], data[4]
        print(v)
        maze.append((e, g))

    
    return 

def dfs():
    return

def bfs():
    return

def modified_search():
    return

def main():
    file = open('maze1.txt')
    read_maze(file)
    return


if __name__ == '__main__':
    main()
