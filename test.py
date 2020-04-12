def calculate_manhattan_dist(idx, value, n):

    """calculate the manhattan distance of a tile"""

    initial_row = idx // n

    initial_col = idx % n

    goal_row = value // n
    
    goal_col = value % n

    return abs(initial_row - goal_row) + abs(initial_col - goal_col)


array = (7,2,4,5,0,6,8,3,1)

cost = 0
for i, item in enumerate(array):
    if item != 0:
        cost += calculate_manhattan_dist(i, item, 3)
        print(i, calculate_manhattan_dist(i, item,3))
print(cost)