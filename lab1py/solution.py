import sys
from queue import PriorityQueue
import collections
import numpy as np


class Node:
    def __init__(self, name, path, total_cost, h_value, neighbours):
        self.name = name
        self.path = path
        self.total_cost = total_cost
        self.h_value = h_value
        self.neighbours = neighbours

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return f'Node(name={self.name}, cost={self.total_cost})'


class Transition:
    def __init__(self, node, cost, total_cost, path):
        self.node = node
        self.cost = cost
        self.total_cost = total_cost
        self.path = path

    def __lt__(self, other):
        return self.node.name < other.node.name


def heuristic(path2):
    heuristic_values = {}
    with open(path2, encoding='utf-8') as file:
        # lines = file.read().splitlines()
        for line in file:
            if not line.startswith('#'):
                x = line.split()
                heuristic_values[x[0][:len(x[0]) - 1]] = x[1]
    return heuristic_values


def transition(path1, heuristics):
    transitions = {}
    counter = 0
    with open(path1, encoding="UTF-8") as file:
        for line in file:

            if not line.startswith('#'):

                if counter == 0:
                    start = line.strip('\n')
                    counter = counter + 1

                elif counter == 1:
                    counter = counter + 1
                    end = line.strip('\n').split(' ')
                    counter = counter + 1

                else:
                    x = line.strip('\n').split()
                    state = x[0][:len(x[0]) - 1]
                    cities = []

                    for i in range(1, len(x)):
                        name_and_cost = x[i].split(',')

                        node_exists = transitions.get(name_and_cost[0], False)
                        if not node_exists:
                            nextNode = Node(name_and_cost[0], name_and_cost[0], 0, 0, [])
                            if heuristics:
                                nextNode.h_value = heuristics[name_and_cost[0]]
                            new_transition = Transition(nextNode, name_and_cost[1], 0, name_and_cost[0])
                            transitions[name_and_cost[0]] = nextNode
                        else:
                            new_transition = Transition(node_exists, name_and_cost[1], 0, name_and_cost[0])

                        cities.append(new_transition)

                    cities = sorted(cities)

                    main_node = transitions.get(state, False)
                    if main_node:
                        main_node.neighbours = cities
                    else:

                        main_node = Node(state, state, 0, 0, cities)
                        if heuristics:
                            main_node.h_value = heuristics[state]
                    transitions[state] = main_node
                    if state == start:
                        start_node = main_node
    end_dict = {}
    for city in end:
        end_dict[city] = city
    return start_node, end_dict, transitions


def bfs(s0, goal):
    open = []
    open.append(s0)
    visited = {}

    while len(open) != 0:
        n = open.pop(0)

        visited[n.name] = n.name

        if n.name in goal:
            return n, visited

        expand = n.neighbours
        for trans in expand:
            if trans.node.name not in visited:
                trans.node.path = n.path + " => " + trans.node.name
                trans.node.total_cost = n.total_cost + int(trans.cost)
                open.append(trans.node)

    return False, False


def ucs(s0, goal):
    open = PriorityQueue()
    open.put((0, s0, s0.name))
    visited = {}
    while open.qsize() != 0:
        all = open.get()
        n = all[1]
        n.total_cost = all[0]
        n.path = all[2]

        while True:
            if open and visited and n.name in visited:
                all = open.get()
                n = all[1]
                n.total_cost = all[0]
                n.path = all[2]
            else:
                break
        visited[n.name] = n.name

        if n.name in goal:
            return n, visited

        expand = n.neighbours

        for trans in expand:
            if trans.node.name not in visited:
                trans.path = n.path + " => " + trans.node.name
                trans.total_cost = n.total_cost + int(trans.cost)
                open.put((trans.total_cost, trans.node, trans.path))
    return False, False


def astar(s0, goal):
    open = PriorityQueue()
    open.put((0, s0, s0.name, 0))
    open_dict = {}
    open_dict[s0.name] = s0.name
    visited = {}
    while open.qsize() != 0:
        all = open.get()
        n = all[1]
        n.total_cost = float(all[3])
        n.path = all[2]
        while True:
            if open and visited and n.name in visited:
                all = open.get()
                n = all[1]
                n.total_cost = float(all[3])
                n.path = all[2]
            else:
                break
        visited[n.name] = n.name
        if n.name in goal:
            return n, visited
        expand = n.neighbours
        for trans in expand:
            if trans.node.name not in visited:
                trans.path = n.path + " => " + trans.node.name
                trans.total_cost = n.total_cost + int(trans.cost)
                open.put((float(trans.total_cost) + float(trans.node.h_value), trans.node, trans.path,
                          float(trans.total_cost)))
                open_dict[trans.node.name] = trans.node.name
    return False, False


def optimistic_f(end, transitions, heuristic_path):
    print("# HEURISTIC-OPTIMISTIC " + heuristic_path)
    conclusion = ""
    for state in transitions:
        n, visited = ucs(transitions[state], end)
        condition = ("OK" if float(transitions[state].h_value) <= float(n.total_cost) else "ERR")
        print("[CONDITION]: [" + condition + "] h(" + transitions[state].name + ") <= h*: " + str(
            float(transitions[state].h_value)) + " <= " + str(float(n.total_cost)))
        if condition == "ERR":
            conclusion = " not"
    print("[CONCLUSION]: Heuristic is" + conclusion + " optimistic.")


def consistent_f(heuristic_path, transitions, heuristic_values):
    print("# HEURISTIC-CONSISTENT " + heuristic_path)
    conclusion = ""
    for state in transitions:
        for neighbor in sorted(transitions[state].neighbours):
            condition = (
                "OK" if float(heuristic_values[transitions[state].name]) <= float(neighbor.node.h_value) + float(
                    neighbor.cost) else "ERR")
            print("[CONDITION]: [" + condition + "] h(" + transitions[
                state].name + ") <= h(" + neighbor.node.name + ") + c: " + str(
                float(heuristic_values[transitions[state].name])) + " <= " + str(
                float(neighbor.node.h_value)) + " + " + str(
                float(neighbor.cost)))
            if condition == "ERR":
                conclusion = " not"
    print("[CONCLUSION]: Heuristic is" + conclusion + " consistent.")

def dijkstra(source, transitions, distance):
    queue = PriorityQueue()

    # for key in transitions:
    #     for neighbor in transitions[key].neighbours:
    #         newTransition = Transition(transitions[key],neighbor.cost,0,'')
    #         if neighbor.node.neighbours and transitions[key].name != neighbor.node.name:
    #             neighbor.node.neighbours.append(newTransition)
    #         else:
    #             new = [newTransition]
    #             neighbor.node.neighbours=new

    if not distance:
        for state in transitions:
            distance[transitions[state].name] = np.inf
            if transitions[state].name == source:
                distance[source] = 0
            queue.put((distance[transitions[state].name], transitions[state]))

    else:
        for key in distance:
            queue.put((float(distance[key]),transitions[key]))

    while queue.qsize() != 0:
        n = queue.get()[1]
        if  len(n.neighbours) != 0:
            expand = n.neighbours

            for neighbour in expand:
                new_distance = float(distance[n.name]) + float(neighbour.cost)
                if new_distance < distance[neighbour.node.name]:
                    distance[neighbour.node.name] = new_distance

    return distance

def optimistic_f2(end, transitions, heuristic_path):
    print("# HEURISTIC-OPTIMISTIC " + heuristic_path)
    conclusion = ""
    distance = {}
    for state in end:
        distance = dijkstra(state, transitions, distance)

    for state in transitions:
        condition = ("OK" if float(transitions[state].h_value) <= float(distance[transitions[state].name]) else "ERR")
        print("[CONDITION]: [" + condition + "] h(" + transitions[state].name + ") <= h*: " + str(
            float(transitions[state].h_value)) + " <= " + str(float(distance[transitions[state].name])))
        if condition == "ERR":
            conclusion = " not"
    print("[CONCLUSION]: Heuristic is" + conclusion + " optimistic.")


def algorithm_output(n, visited):
    if n:
        print("[FOUND_SOLUTION]: yes")
        print("[STATES_VISITED]: " + str(len(visited)))  # str(visited.qsize()))
        print("[PATH_LENGTH]: " + str(len(n.path.split("=>"))))
        print("[TOTAL_COST]: " + str(float(n.total_cost)))
        print("[PATH]: " + n.path)
    else:
        print("[FOUND_SOLUTION]: no")


def main():
    heuristic_values = {}
    optimistic, consistent = False, False
    algorithm = ""
    path = ''
    heuristic_path = ''
    for x in range(1, len(sys.argv)):
        if sys.argv[x] == "--alg":
            x = x + 1
            algorithm = sys.argv[x]
        elif sys.argv[x] == "--ss":
            x = x + 1
            path = sys.argv[x]
        elif sys.argv[x] == '--h':
            x = x + 1
            heuristic_path = sys.argv[x]
            heuristic_values = heuristic(heuristic_path)
        elif sys.argv[x] == "--check-optimistic":
            optimistic = True
        elif sys.argv[x] == "--check-consistent":
            consistent = True

    start, end, transitions = transition(path, heuristic_values)
    transitions = collections.OrderedDict(sorted(transitions.items()))
    n, visited = False, False
    if algorithm:
        if algorithm == "astar":
            print("# A-STAR " + heuristic_path)
            n, visited = astar(start, end)
        if algorithm == "bfs":
            print("# BFS")
            n, visited = bfs(start, end)
        if algorithm == "ucs":
            print("# UCS")
            n, visited = ucs(start, end)
        algorithm_output(n, visited)

    if optimistic:
        optimistic_f(end, transitions, heuristic_path)

    if consistent:
        consistent_f(heuristic_path, transitions, heuristic_values)


main()
