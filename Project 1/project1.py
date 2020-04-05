"""
Skeleton code for Project 1 of Columbia University's AI EdX course (8-puzzle).
Python 3

EXAMPLE CODE: 
    USE python3 -m cProfile -s tottime driver.py <puzzle initial state> for checking speed results
    
    python3 project1.py bfs 1,2,5,3,4,0,6,7,8
    python3 project1.py dfs 1,2,5,3,4,0,6,7,8
    python3 project1.py bfs 3,1,2,0,4,5,6,7,8
    python3 project1.py dfs 3,1,2,0,4,5,6,7,8
    python3 project1.py bfs 1,2,5,3,4,0,6,7,8
    python3 project1.py dfs 1,2,5,3,4,0,6,7,8


    EXAMPLES OF OUTPUTS:
        python3 project1.py dfs 6,1,8,4,0,2,7,3,5

            path_to_goal: ['Up', 'Left', 'Down', ... , 'Up', 'Left', 'Up', 'Left']
            cost_of_path: 46142
            nodes_expanded: 51015
            search_depth: 46142
            max_search_depth: 46142

        python3 project1.py bfs 6,1,8,4,0,2,7,3,5

            path_to_goal: ['Down', 'Right', 'Up', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Up', 'Left', 'Up', 'Right', 'Right', 'Down', 'Down', 'Left', 'Left', 'Up', 'Up']
            cost_of_path: 20
            nodes_expanded: 54094
            search_depth: 20
            max_search_depth: 21

        python3 project1.py dfs 8,6,4,2,1,3,5,7,0

            path_to_goal: ['Up', 'Up', 'Left', ..., , 'Up', 'Up', 'Left']
            cost_of_path: 9612
            nodes_expanded: 9869
            search_depth: 9612
            max_search_depth: 9612


        python3 project1.py bfs 8,6,4,2,1,3,5,7,0

            path_to_goal: ['Left', 'Up', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Up', 'Right', 'Right', 'Up', 'Left', 'Left', 'Down', 'Right', 'Right', 'Up', 'Left', 'Down', 'Down', 'Right', 'Up', 'Left', 'Up', 'Left']
            cost_of_path: 26
            nodes_expanded: 166786
            search_depth: 26
            max_search_depth: 27
"""

import queue as Q

import tracemalloc

import time

import sys

import math


#### SKELETON CODE ####
# The Class that Represents the Puzzle
class PuzzleState(object):
    """docstring for PuzzleState"""
                   
                # config=begin_state  n=size
                # begin_state = (1,2,3,0,4,5,6,7,8)
    def __init__(self, config, n, parent=None, action="Initial", cost=0):

        if n*n != len(config) or n < 2:

            raise Exception("the length of config is not correct!")
        
        self.config = config

        self.n = n

        self.parent = parent

        self.cost = cost

        self.action = action

        self.dimension = n

        self.children = []

        for i, item in enumerate(self.config):
            
            if item == 0:

                self.blank_row = i // self.n

                self.blank_col = i % self.n

                break

    def display(self):

        for i in range(self.n):

            line = []

            offset = i * self.n

            for j in range(self.n):

                line.append(self.config[offset + j])

            print(line)

    def move_left(self):

        if self.blank_col == 0:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index - 1

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):

        if self.blank_col == self.n - 1:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index + 1

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):

        if self.blank_row == 0:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index - self.n

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):

        if self.blank_row == self.n - 1:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index + self.n

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    def expand(self):
        """expand the node"""

        # add child nodes in order of UDLR

        if len(self.children) == 0:

            up_child = self.move_up()

            if up_child is not None:

                self.children.append(up_child)

            down_child = self.move_down()

            if down_child is not None:

                self.children.append(down_child)

            left_child = self.move_left()

            if left_child is not None:

                self.children.append(left_child)

            right_child = self.move_right()

            if right_child is not None:

                self.children.append(right_child)

        return self.children


class Frontier():
    def __init__(self, initial_state, stack = False, queue = False):
        self.stack = stack
        self.queue = queue
        self.frontier = [initial_state]
        self.config_frontier = set()
        self.config_frontier.add(initial_state.config)
    
    def pop(self):
        removed = self.frontier.pop() if self.stack else self.frontier.pop(0)
        self.config_frontier.remove(removed.config)
        return removed
    
    def append(self, state):
        self.frontier.append(state)
        self.config_frontier.add(state.config)


    def empty(self):
        return True if not self.frontier else False


# Function that Writes to output.txt
# Students need to change the method to have the corresponding parameters
def writeOutput(start_time, nodes_expanded, max_search_depth, state=False):
    '''
    Example output:
        path_to_goal: ['Up', 'Left', 'Left']
        cost_of_path: 3
        nodes_expanded: 10
        search_depth: 3
        max_search_depth: 4
        running_time: 0.00188088
        max_ram_usage: 0.07812500
    '''
    
    peak = tracemalloc.get_traced_memory()[1]

    tracemalloc.stop()
    
    if state:
        print(f'path_to_goal:  {calculate_path(state)}\n',
            f'cost_of_path: {calculate_total_cost(state)} \n',
            f'nodes_expanded: {nodes_expanded - 1} \n',
            f'search_depth: {calculate_total_cost(state)} \n',
            f'max_search_depth: {max_search_depth} \n',       
            f'max_running_time: {time.time() - start_time} \n',
            f"max_ram_usage: {peak / 10**6} \n"
                )
    else:
        print('Failure')


def bfs_search(initial_state):
    """BFS search"""

    start_time = time.time()
    tracemalloc.start()
    nodes_expanded = 0
    max_search_depth = 0

    frontier = Frontier(initial_state)
    explored = set()

    while not frontier.empty():
        state = frontier.pop()
        explored.add(state.config)
        nodes_expanded += 1
        
        if max_search_depth < state.cost:
            max_search_depth = state.cost

        if test_goal(state.config):
            return writeOutput(start_time, nodes_expanded, max_search_depth, state)

        for neighbor in state.expand():
            if neighbor.config not in explored and neighbor.config not in frontier.config_frontier:
                frontier.append(neighbor)

    return writeOutput(start_time, nodes_expanded, max_search_depth)


def dfs_search(initial_state):
    """DFS search"""

    start_time = time.time()
    tracemalloc.start()
    nodes_expanded = 0
    max_search_depth = 0

    frontier = Frontier(initial_state, stack=True)
    explored = set()
    
    while not frontier.empty():
        state = frontier.pop()
        explored.add(state.config)
        nodes_expanded += 1
        
        if max_search_depth < state.cost:
            max_search_depth = state.cost

        if test_goal(state.config):
            return writeOutput(start_time, nodes_expanded, max_search_depth, state)

        for neighbor in state.expand()[::-1]:
            if neighbor.config not in explored and neighbor.config not in frontier.config_frontier:
                frontier.append(neighbor)

    return writeOutput(start_time, nodes_expanded, max_search_depth)


def A_star_search(initial_state):
    """A * search"""

    ### STUDENT CODE GOES HERE ###
    pass


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    return state.cost


def calculate_path(state):
    path = []
    while state.action != "Initial":
        path.append(state.action)
        state = state.parent
    
    return path[::-1]


def test_goal(puzzle_state):
    """test the state is the goal state or not"""

    if puzzle_state == (0, 1, 2, 3, 4, 5, 6, 7, 8):
        return True

# Main Function that reads in Input and Runs corresponding Algorithm
def main():

    sm = sys.argv[1].lower()

    begin_state = sys.argv[2].split(",")

    begin_state = tuple(map(int, begin_state)) # (1,2,5,3,4,0,6,7,8)

    size = int(math.sqrt(len(begin_state))) # 3

    hard_state = PuzzleState(begin_state, size)

    if sm == "bfs":

        bfs_search(hard_state)

    elif sm == "dfs":

        dfs_search(hard_state)

    elif sm == "ast":

        A_star_search(hard_state)

    else:

        print("Enter valid command arguments !")


if __name__ == '__main__':

    main()
