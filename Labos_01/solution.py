import sys
from decimal import Decimal
from pathlib import Path
from queue import PriorityQueue
from collections import OrderedDict
import time


class Node:
    def __init__(self, name, path, total_cost, h_value, neigbours):
        self.name = name
        self.path = path
        self.total_cost = total_cost
        self.h_value = h_value
        self.neigbours = neigbours

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


class Timer:
    def __init__(self):
        self.counter = 0
        self.sumTime = 0.0

    def startF(self):
        self.start = time.time()
        self.counter += 1

    def endF(self):
        self.end = time.time()
        self.sumTime = self.sumTime + self.end - self.start

    def sumAllTime(self):
        print(self.sumTime)


def heuristic(path2):
    hueristic_values = {}
    with open(path2, encoding='utf-8') as file:
        # lines = file.read().splitlines()
        for line in file:
            if not line.startswith('#'):
                x = line.split()
                hueristic_values[x[0][:len(x[0]) - 1]] = x[1]
    return hueristic_values


def transition(path1, heuristics):
    transitions = {}
    counter = 0
    lista = []
    timer2 = Timer()
    timer = Timer()
    timer.startF()
    timer3 = Timer()
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

                        nodeExists = transitions.get(name_and_cost[0], False)
                        timer2.startF()
                        if nodeExists == False:
                            nextNode = Node(name_and_cost[0], name_and_cost[0], 0, 0, [])
                            if heuristics:
                                nextNode.h_value = heuristics[name_and_cost[0]]
                            newTransition = Transition(nextNode, name_and_cost[1],0,name_and_cost[0])
                            transitions[name_and_cost[0]] =nextNode
                        else:
                            newTransition = Transition(nodeExists, name_and_cost[1],0,name_and_cost[0])

                        cities.append(newTransition)
                        timer2.endF()

                    timer3.startF()
                    cities = sorted(cities) ## provjeri suta koliko se vrti
                    timer3.endF()

                    mainNode = transitions.get(state, False)
                    if mainNode:
                        mainNode.neigbours = cities
                    else:

                        mainNode = Node(state, state, 0, 0, cities)
                        if heuristics:
                            mainNode.h_value = heuristics[state]
                    transitions[state] = mainNode
                    if state == start:
                        startNode = mainNode

    timer.endF()
    timer2.sumAllTime()
    timer.sumAllTime()
    timer3.sumAllTime()
    end_dict = {}
    for city in end:
        end_dict[city] = city
    return startNode, end_dict, transitions



def bfs(s0, suc, goal):
    open = []
    open.append(s0)
    visited = {}
    counter = 1

    while len(open) != 0:
        n = open.pop(0)

        visited[n.name] = n.name

        if n.name in goal:
            return n, visited

        expand = n.neigbours
        for trans in expand:
            if trans.node.name not in visited:
                trans.node.path = n.path + " => " + trans.node.name
                trans.node.total_cost = n.total_cost + int(trans.cost)
                open.append(trans.node)
        counter += 1

    return False, False


def ucs(s0, suc, goal):
    open = PriorityQueue()
    open.put((0, s0, s0.name))
    visited= {}
    while open:
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

        expand = n.neigbours

        for trans in expand:
            if trans.node.name not in visited:
                trans.path = n.path + " => " + trans.node.name
                trans.total_cost = n.total_cost + int(trans.cost)
                open.put((trans.total_cost, trans.node, trans.path))

    return False, False


def astar(s0, suc, goal, h):
    open = PriorityQueue()
    open.put((0, s0, s0.name, 0))
    open_dict={}
    open_dict[s0.name]=s0.name
    visited = {}
    while open:
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
        expand = n.neigbours
        for trans in expand:
            if trans.node.name not in visited:
                trans.path = n.path + " => " + trans.node.name
                trans.total_cost = n.total_cost + int(trans.cost)
                open.put((float(trans.total_cost) + float(trans.node.h_value), trans.node, trans.path,
                          float(trans.total_cost)))
                open_dict[trans.node.name]=trans.node.name
    return False, False


def optimistic_f(end, transitions, heuristic_path):
    print("# HEURISTIC-OPTIMISTIC " + heuristic_path)
    conclusion = ""
    for state in transitions:
        n, visited = ucs(state, transitions, end)
        condition = ("OK" if float(state.h_value) <= float(n.total_cost) else "ERR")
        print("[CONDITION]: [" + condition + "] h(" + state.name + ") <= h*: " + str(
            float(state.h_value)) + " <= " + str(float(n.total_cost)))
        if condition == "ERR":
            conclusion = " not"
    print("[CONCLUSION]: Heuristic is" + conclusion + " optimistic.")


def consistent_f(heuristic_path, transitions, heuristic_values):
    print("# HEURISTIC-CONSISTENT " + heuristic_path)
    conclusion = ""
    for state in transitions:
        for neigbor in sorted(state.neigbours):
            condition = ("OK" if float(heuristic_values[state.name]) <= float(neigbor.h_value) + float(
                neigbor.cost) else "ERR")
            print("[CONDITION]: [" + condition + "] h(" + state.name + ") <= h(" + neigbor.name + ") + c: " + str(
                float(heuristic_values[state.name])) + " <= " + str(float(neigbor.h_value)) + " + " + str(
                float(neigbor.cost)))
            if condition == "ERR":
                conclusion = " not"
    print("[CONCLUSION]: Heuristic is" + conclusion + " consistent.")


def algoritam_output(n, visited):
    if n != False:
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
    algoritam = ""
    for x in range(1, len(sys.argv)):
        if sys.argv[x] == "--alg":
            x = x + 1;
            algoritam = sys.argv[x]
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
    transitions = sorted(transitions)
    n, visited = False, False
    if algoritam:
        if algoritam == "astar":
            print("# A-STAR " + heuristic_path)
            n, visited = astar(start, transitions, end, heuristic_values)
        if algoritam == "bfs":
            print("# BFS")
            n, visited = bfs(start, transitions, end)
        if algoritam == "ucs":
            print("# UCS")
            n, visited = ucs(start, transitions, end)
        algoritam_output(n, visited)

    if optimistic:
        optimistic_f(end, transitions, heuristic_path)

    if consistent:
        consistent_f(heuristic_path, transitions, heuristic_values)
main()
