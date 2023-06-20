from turtle import Screen
import time
from snake import Snake
from food import Food
from scoreboard import Scoreboard
from queue import PriorityQueue

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("AI Snake Game")
screen.tracer(0)

snake = Snake()
food = Food()
scoreboard = Scoreboard()

# boundaries for new states generated
MIN_X = -300
MIN_Y = -280

MAX_X = 280
MAX_Y = 250

# orientations
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0

PIXEL_DISTANCE = 15  # the distance for checking if the snake is close to the food
DIRECTION = [-20, 20]  # helps compute new states coordinates


class Node:
    """This class represents a node object"""

    def __init__(self, current_state, parent, g_value, h_value, orientation):
        self.current_state = current_state
        self.parent = parent
        self.g_value = g_value
        self.h_value = h_value
        self.orientation = orientation

    def __hash__(self):
        return self.current_state.__hash__()

    def f_value(self):
        return int(self.g_value + self.h_value)

    def __lt__(self, other):
        return self.f_value() < other.f_value()


# This function calculates the estimated cost from a state to the food
def heuristic_cost(state):
    xcor, ycor = state
    return int(abs(xcor - food.xcor()) + abs(ycor - food.ycor()))


def goal_test(node_state):
    node_x = node_state[0]
    node_y = node_state[1]
    return food.distance(node_x, node_y) < PIXEL_DISTANCE


# This function generates a solution path leading to the food's location
def solution_path(n):
    movements_list = []

    while n.parent is not None:
        movements_list.append(n.orientation)
        n = n.parent
    movements_list.reverse()  # shows states in ascending order
    return movements_list


# This function generates the successor states of a node
def get_neighbouring_states(current_node):
    list_of_nodes = []
    curr_x = current_node.current_state[0]
    curr_y = current_node.current_state[1]

    if current_node.orientation != "up":
        new_state = (curr_x, curr_y + DIRECTION[0])
        if MIN_X <= new_state[0] <= MAX_X and MIN_Y <= new_state[1] <= MAX_Y:
            list_of_nodes.append(Node(new_state, current_node, food.distance((new_state[0],
                                                                              new_state[1])),
                                      heuristic_cost(new_state), "down"))

    if current_node.orientation != "down":
        new_state = (curr_x, curr_y + DIRECTION[1])
        if MIN_X < new_state[0] < MAX_X and MIN_Y < new_state[1] < MAX_Y:
            list_of_nodes.append(Node(new_state, current_node, food.distance((new_state[0], new_state[1])),
                                      heuristic_cost(new_state), "up"))

    if current_node.orientation != "left":
        new_state = (curr_x + DIRECTION[1], curr_y)
        if MIN_X < new_state[0] < MAX_X and MIN_Y < new_state[1] < MAX_Y:
            list_of_nodes.append(Node(new_state, current_node, food.distance((new_state[0], new_state[1])),
                                      heuristic_cost(new_state), "right"))

    if current_node.orientation != "right":
        new_state = (curr_x + DIRECTION[0], curr_y)
        if MIN_X < new_state[0] < MAX_X and MIN_Y < new_state[1] < MAX_Y:
            list_of_nodes.append(Node(new_state, current_node, food.distance((new_state[0], new_state[1])),
                                      heuristic_cost(new_state), "left"))

    return list_of_nodes


"""A function to implement the A* algorithm"""


def a_star_search(start_node):
    open_list = PriorityQueue()
    closed_list = set()

    # create corresponding map to compare positions
    positions_map_open_list = dict()
    positions_map_closed_list = dict()
    open_list.put(start_node)
    positions_map_open_list[start_node.current_state] = start_node

    while open_list.qsize() > 0:
        min_node = open_list.get()
        positions_map_open_list.pop(min_node.current_state)

        if goal_test(min_node.current_state):
            return solution_path(min_node)
        successor_nodes = get_neighbouring_states(min_node)

        for successor_node in successor_nodes:
            if goal_test(successor_node.current_state):
                return solution_path(successor_node)
            if successor_node.current_state in positions_map_closed_list:
                continue
            if successor_node.current_state not in positions_map_open_list and successor_node.current_state not in positions_map_closed_list:
                open_list.put(successor_node)
                positions_map_open_list[successor_node.current_state] = successor_node
            elif successor_node.current_state in positions_map_open_list:
                holder_node = positions_map_open_list.get(successor_node.current_state)
                holder_node_fvalue = holder_node.f_value()
                successor_node_fvalue = successor_node.f_value()
                if successor_node_fvalue < holder_node_fvalue:
                    open_list.put(successor_node)
                    open_list.queue.remove(holder_node)
                    positions_map_open_list.pop(holder_node.current_state)
                    positions_map_open_list[successor_node.current_state] = successor_node
        closed_list.add(min_node)
        positions_map_closed_list[min_node.current_state] = min_node
    return None


game_is_on = True

node = Node((0, 0), None, food.distance(0, 0), heuristic_cost((0, 0)), "right")  # starting node
orientation_path = a_star_search(node)  # path from A* algorithm
if orientation_path is None:
    print("open list became empty")
    exit(0)
orientation_path_length = len(orientation_path)

# displaying the start, goal and the directions taken to get to the goal
print(f"Start: {snake.head.pos()}")
print(f"Goal: {food.pos()}")
print(f"A* Path: {orientation_path}\n")

number_of_moves = 10
# for loop to move the snake according to path generated by A* algorithm
for turn in range(number_of_moves):

    for move in range(orientation_path_length):
        screen.update()
        time.sleep(0.1)

        if orientation_path[move] == "up":
            snake.move_up()
        elif orientation_path[move] == "down":
            snake.move_down()
        elif orientation_path[move] == "left":
            snake.move_left()
        elif orientation_path[move] == "right":
            snake.move_right()

        snake.move_snake()

        # checking for the snake hitting the screen boundary
        if snake.head.xcor() > MAX_X or snake.head.xcor() < MIN_X or snake.head.ycor() > MAX_Y or snake.head.ycor() < MIN_Y:
            scoreboard.reset()
            scoreboard.game_over()
            game_is_on = False
            exit(1)

    food.refresh()
    snake.extend()
    scoreboard.update_score()
    screen.update()
    time.sleep(0.1)

    # getting the coordinates for the snake's current position
    x = int(snake.head.xcor())
    y = int(snake.head.ycor())

    orientation = ""

    if snake.head.heading() == UP:
        orientation = "up"
    elif snake.head.heading() == DOWN:
        orientation = "down"
    elif snake.head.heading() == LEFT:
        orientation = "left"
    elif snake.head.heading() == RIGHT:
        orientation = "right"

    node = Node((x, y), None, food.distance(x, y), heuristic_cost((x, y)), orientation)
    orientation_path = a_star_search(node)

    if orientation_path is None:
        print("Open list became empty")
        exit(0)
    orientation_path_length = len(orientation_path)

    print(f"Start: {snake.head.pos()}")
    print(f"Goal: {food.pos()}")
    print(f"A* Path: {orientation_path}\n")


screen.exitonclick()
