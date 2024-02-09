# maze_solver.py
#
# solves No right turns! maze using bfs, dfs and a modified search algorithm
# 
# python maze_solver.py maze 
#
# the expected maze input format is a graph adjacency list
# with the additional requirements of a direction
# for example in maze1.txt, vertex 0 is connected to vertex 4 by an edge going north (aka 0)
# maze1.txt is also the example given in the Imagine RIT link
#

import sys

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

def get_backwards_moves(v, dir):
    # v: vertex
    # dir: direction
    # only check 2 directions to go
    # that is matching direction (backwards) and (dir + 1) % 4 (right turn)
    moves = []
    # straight?
    inverted_dir = (dir+2)%4
    if inverted_dir in v[1]:
        # (index, inverted_direction)
        moves.append((v[1][inverted_dir], dir))

    if (dir-1)%4 in v[1]:
        # (index, direction)
        moves.append((v[1][(dir-1)%4], (dir+1)%4))
    return moves

def make_path(parents, v):
    # make a path out of parent dictionary
    if v not in parents:
        return [v[0]]
    else:
        return make_path(parents, parents[v]) + [v[0]]

def bfs(maze, pos=0):
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

    while q:
        # (index, direction)
        state = q.pop(0)
        dir = state[1]
        visited_state.add(state)

        # vertext details
        # index, edges, goal?
        v = maze[state[0]]
        goal = v[2]
        
        if goal:
            return make_path(parents, state)
        moves = get_moves(v, dir)
        
        for move in moves:
            if move not in visited_state:
                q.append(move)
                parents[move] = state
        
    return False

def dfs(maze, pos=0):
    # maze: array containing the maze structure, a list containing vetecies and their edges
    # pos: starting index in the maze
    #
    # perform a dfs search
    # 

    # pos pointing north
    dir = 0
    state = (pos, dir)
    stack = [state]

    # create sets
    parents = {}
    visited_state = set()
    visited_state.add(state)

    while stack:
        # (index, direction)
        state = stack.pop()
        dir = state[1]
        visited_state.add(state)

        # vertext details
        # index, edges, goal?
        v = maze[state[0]]
        goal = v[2]

        if goal:
            return make_path(parents, state)
        moves = get_moves(v, dir)
        
        for move in moves:
            if move not in visited_state:
                stack.append(move)
                parents[move] = state
    return False

def modified_search(maze, goal, pos=0):
    # maze: array containing the maze structure, a list containing vetecies and their edges
    # pos: starting index in the maze
    #
    #
    # Do a simultanious backward search, forward uses bfs and backwards uses dfs
    # foward will use bfs, because I think there will be lengthier branches going forward
    # backward will use dfs, because I think there will be short branches going backwards
    #
    # Do a forward step, then do a backward step.
    # They work on different visited sets and parent dictionarys
    # 
    # Annoying quirk of my implementation, when joining the forward path and backward path the
    # the method of path printing is different, it still works though. 

    # pos pointing north
    fwd_dir = 0
    fwd_state = (pos, fwd_dir)
    fwd_q = [fwd_state]

    # assuming looking north at end of maze
    bck_dir = 0
    bck_state = (goal, bck_dir)
    bck_stack = [bck_state]

    # create sets
    fwd_parents = {}
    fwd_visited_state = set()
    fwd_visited_state.add(fwd_state)

    bck_parents = {}
    bck_visited_state = set()
    bck_visited_state.add(bck_state)

    while fwd_q or bck_stack:
        # While both forward and back has no steps to take

        # if forward q isn't empty
        if fwd_q:
            # FORWARD STEP
            # (index, direction)
            fwd_state = fwd_q.pop(0)
            fwd_dir = fwd_state[1]
            fwd_visited_state.add(fwd_state)
            # print(f'fw:{str(fwd_state)}')
            
            # vertext details
            # index, edges, goal?
            v = maze[fwd_state[0]]
            
            if fwd_state in bck_visited_state:
                return make_path(fwd_parents, fwd_parents[fwd_state]) + make_path(bck_parents, fwd_state)[::-1]
            fwd_moves = get_moves(v, fwd_dir)

            for move in fwd_moves:
                if move not in fwd_visited_state:
                    fwd_q.append(move)
                    fwd_parents[move] = fwd_state
        
        # if backward stack isn't empty
        if bck_stack:
            # BACKWARD STEP
            # (index, direction)
            bck_state = bck_stack.pop()
            bck_dir = bck_state[1]
            bck_visited_state.add(bck_state)
            # print(f'bk: {str(bck_state)}')

            #  vertex details
            # index, edges, goal?
            v = maze[bck_state[0]]

            if bck_state in fwd_visited_state:
                return make_path(fwd_parents, bck_state) + make_path(bck_parents, bck_parents[bck_state])[::-1]
            bck_moves = get_backwards_moves(v, bck_dir)

            for move in bck_moves:
                if move not in bck_visited_state:
                    bck_stack.append(move)
                    bck_parents[move] = bck_state

    return False

def main():
    # pass maze file through argv
    # format explaination is in top file comment
    if len(sys.argv) == 2:
        file = open(sys.argv[1])
    else:
        file = open('maze1.txt')

    maze = read_maze(file)
    goal = maze[-1][0]

    bfs_path = bfs(maze)
    print(f'BFS Solution: {str(bfs_path)}')
    dfs_path = dfs(maze)
    print(f'DFS Solution: {str(dfs_path)}')
    ms_path = modified_search(maze, goal)
    # When the path says swap, it means that the method for reading the path has changed. It's a quirk, but it still finds the solution.
    print(f'Modified Search Solution: {str(ms_path)}')
    
    return


if __name__ == '__main__':
    main()
