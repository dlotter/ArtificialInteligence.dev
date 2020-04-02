"""
Skeleton code for Project 1 of Columbia University's AI EdX course (8-puzzle).
Python 3
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


# Function that Writes to output.txt
# Students need to change the method to have the corresponding parameters
def writeOutput(start_time, state=False):
    '''
    path_to_goal: ['Up', 'Left', 'Left']

    cost_of_path: 3

    nodes_expanded: 10

    search_depth: 3

    max_search_depth: 4

    running_time: 0.00188088

    max_ram_usage: 0.07812500
    '''
    
    current, peak = tracemalloc.get_traced_memory()

    tracemalloc.stop()
    
    if state:
        print(f'path_to_goal:  {calculate_path(state)}\n',
            f'cost_of_path: {calculate_total_cost(state)} \n',
            'nodes_expanded: {} \n',
            'search_depth: {} \n',
            'max_search_depth: {} \n',       
            f'max_running_time: {time.time() - start_time} \n',
            f"max_ram_usage: {peak / 10**6}"
                )
    else:
        print('Failure')


def bfs_search(initial_state):
    """BFS search"""

    start_time = time.time()

    tracemalloc.start()

    frontier = Q.Queue()
    frontier.put(initial_state)
    explored = set()

    while not frontier.empty():
        state = frontier.get()
        explored.add(state)

        if test_goal(state.config):
            
            return writeOutput(start_time, state)

        for neighbor in state.expand():
            if neighbor not in explored.union(frontier.queue):
                frontier.put(neighbor)

    return writeOutput(start_time)


def dfs_search(initial_state):
    """DFS search"""

    ### STUDENT CODE GOES HERE ###
    pass


def A_star_search(initial_state):
    """A * search"""

    ### STUDENT CODE GOES HERE ###
    pass


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    return state.cost


def calculate_path(state, actions=False):
    
    if not actions:
        actions = []

    if state.action != "Initial":
        actions.append(state.action)
        calculate_path(state.parent, actions)
    
    return actions[::-1]


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
