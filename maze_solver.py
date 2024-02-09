# maze_solver.py
#
# solves No right turns! maze using bfs, dfs and a modified search algorithm
# 
# python maze_solver.py maze 
#

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
        v = data[0]
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

def make_path(parents, v):
    # make a path out of parent dictionary
    if v not in parents:
        return [v]
    else:
        return make_path(parents, parents[v]) + [v]

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

def modified_search():
    return

def main():
    file = open('maze1.txt')
    maze = read_maze(file)

    bfs_path = bfs(maze)
    print(bfs_path)
    dfs_path = dfs(maze)
    print(dfs_path)
    
    return


if __name__ == '__main__':
    main()
