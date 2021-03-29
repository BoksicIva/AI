import sys
from decimal import Decimal
from pathlib import Path



def heuristic(path2):
    hueristic_values = {}
    with open(path2, encoding='utf-8') as file:
        # lines = file.read().splitlines()
        for line in file:
            if not line.startswith('#'):
                x = line.split()
                hueristic_values[x[0][:len(x[0])-1]] = x[1]
    return hueristic_values


def transition(path1,heuristics):
    transitions = {}
    cities = {}
    counter = 0
    with open(path1, encoding='utf-8') as file:
        for line in file:
            if not line.startswith('#'):
                if counter == 0:
                    start = line.strip('\n')
                    counter = counter + 1
                elif counter == 1:
                    counter = counter + 1
                    end = line.strip('\n').split(',')
                else:
                    counter = counter + 1
                    cities = []
                    x = line.strip('\n').split()
                    state = x[0][:len(x[0]) - 1]
                    for i in range(1, len(x)):
                        city = {}
                        city_and_cost = x[i].split(',')
                        city["city"]=city_and_cost[0]
                        city["cost"] = city_and_cost[1]
                        city["path"]=''
                        city["total_cost"]=0
                        city["h_value"]=heuristics[city_and_cost[0]]
                        cities.append(city)
                    cities = sorted(cities, key=lambda k: k['city'])
                    transitions[state] = cities
    return start, end, transitions


def bfs(s0, suc, goal):
    open = [{'city': s0, 'cost': 0, 'path': s0, 'total_cost': 0}]
    visited = []
    while open:
        n = open.pop(0)
        while True:
            if n["city"] in visited:
                n = open.pop(0)
            else:
                break
        print(n["city"]+ "  "+str(n["total_cost"]))
        visited.append(n["city"])
        visited = list(dict.fromkeys(visited))
        if n['city'] in goal:
            return n,visited
        expand = suc[n['city']]
        for state in expand:
            if state["city"] not in visited:
                state["path"] = n["path"] + " => " + state["city"]
                state["total_cost"] = n["total_cost"] + int(state["cost"])
                open.append(state)
    return False


def ucs(s0, suc, goal):
    open = [{'city': s0, 'cost': 0, 'path': s0, 'total_cost': 0}]
    visited=[]
    while open:
        n = open.pop(0)
        while True:
            if n["city"] in visited:
                n=open.pop(0)
            else:
                break
        visited.append(n["city"])
        visited = list(dict.fromkeys(visited))
        if n['city'] in goal:
            return n,visited
        expand = suc[n['city']]
        for state in expand:
            if state["city"] not in visited:
                state["path"] = n["path"] + " => " + state["city"]
                state["total_cost"] = n["total_cost"] + float(state["cost"])
                open.append(state)
        open = sorted(open, key=lambda x: float(x['total_cost']))
        open=[dict(t) for t in {tuple(sorted(d.items())) for d in open}]
        open = sorted(open, key=lambda x: (Decimal(x['total_cost']),x["city"]))
    return False

def astar(s0,suc,goal,h):
    open = [{'city': s0, 'cost': 0, 'path': s0, 'total_cost': 0}]
    closed = []
    visited = []
    while open:
        n = open.pop(0)
        while True:
            if n["city"] in closed:
                n = open.pop(0)
            else:
                break
        closed.append(n)
        if n['city'] in goal:
            return n, closed
        expand = suc[n['city']]
        for state in expand:
            v,o=-1,-1
            for i in range(0,len(closed)):
                if closed[i]["city"] == state["city"]:
                    v=i
            for i in range(0, len(open)):
                if open[i]["city"] == state["city"]:
                    o=i
            if v>=0 and closed:
                if float(closed[v]["total_cost"]) < float(n["total_cost"])+float(state["cost"]):
                    continue
                else:
                    closed.insert(v,state)
                    closed.pop(v+1)
            if o>=0 and open:
                if float(open[o]["total_cost"]) < float(n["total_cost"])+float(state["cost"]):
                    continue
                else:
                    open.insert(o,state)
                    open.pop(o+1)
            if state["city"] not in visited:
                state["path"] = n["path"] + " => " + state["city"]
                state["total_cost"] = float(n["total_cost"]) + float(state["cost"])
                open.append(state)
        open = sorted(open, key=lambda x: (float(x['total_cost'])+float(x["h_value"])))
        open = [dict(t) for t in {tuple(sorted(d.items())) for d in open}]
        open = sorted(open, key=lambda x: ((float(x['total_cost'])+float(x["h_value"])), x["city"]))
        closed = [dict(t) for t in {tuple(sorted(d.items())) for d in closed}]
        visited.append(n["city"])
        visited = list(dict.fromkeys(visited))
    return False

def astar2(s0,suc,goal,h,heuristic_path):
    print("# HEURISTIC-OPTIMISTIC "+Path(heuristic_path).name)
    open = [{'city': s0, 'cost': 0, 'path': s0, 'total_cost': 0, 'h_value':0}]
    closed = []
    visited = []
    while len(closed) < len(suc):
        n = open.pop(0)
        while True:
            if n["city"] in closed:
                n = open.pop(0)
            else:
                break
        closed.append(n)
        expand = suc[n['city']]
        for state in expand:
            v,o=-1,-1
            for i in range(0,len(closed)):
                if closed[i]["city"] == state["city"]:
                    v=i
            for i in range(0, len(open)):
                if open[i]["city"] == state["city"]:
                    o=i
            if v >=0 and closed:
                if float(closed[v]["total_cost"]) < float(n["total_cost"])+float(state["cost"]):
                    continue
                else:
                    closed.insert(v,state)
                    closed.pop(v+1)

            if o>=0 and open:
                if float(open[o]["total_cost"]) < float(n["total_cost"])+float(state["cost"]):
                    continue
                else:
                    open.insert(o,state)
                    open.pop(o+1)
            if state["city"] not in visited:
                state["path"] = n["path"] + " => " + state["city"]
                state["total_cost"] = float(n["total_cost"]) + float(state["cost"])
                open.append(state)
        open = sorted(open, key=lambda x: (float(x['total_cost'])+float(x["h_value"])))
        open = [dict(t) for t in {tuple(sorted(d.items())) for d in open}]
        open = sorted(open, key=lambda x: ((float(x['total_cost'])+float(x["h_value"])), x["city"]))
        closed = [dict(t) for t in {tuple(sorted(d.items())) for d in closed}]
        visited.append(n["city"])
        visited = list(dict.fromkeys(visited))
    return closed

def optimistic(end,transitions,heuristic_values,heuristic_path):
    print("# HEURISTIC-OPTIMISTIC " + Path(heuristic_path).name)
    n,visited=astar(end,transitions,end,heuristic_values)
    visited = sorted(visited, key=lambda x: x["city"])
    conclusion = ""
    for item in visited:
        condition = ("OK" if float(item["h_value"]) <= float(item["total_cost"]) else "ERR")
        print("[CONDITION]: [" + condition + "] h(" + item["city"] + ") <= h*: " + str(
            float(item["h_value"])) + " <= " + str(float(item["total_cost"])))
        if condition == "ERR":
            conclusion = "not"
    print("[CONCLUSION]: Heuristic is " + conclusion + " optimistic.")

def consistent(heuristic_path,transitions,heuristic_values):
    print("# HEURISTIC-CONSISTENT " + Path(heuristic_path).name)
    for city in transitions:
        for neighbour_city in transitions[city]:
            condition = ("OK" if float(heuristic_values[city]) <= float(neighbour_city["h_value"])+float(neighbour_city["cost"]) else "ERR")
            print("[CONDITION]: ["+condition+"] h("+city+") <= h("+neighbour_city["city"]+") + c: "+str(float(heuristic_values[city]))+" <= "+str(float(neighbour_city["h_value"]))+" + "+str(float(neighbour_city["cost"])))
            if condition == "ERR":
                conclusion = "not"
    print("[CONCLUSION]: Heuristic is " + conclusion + " consistent.")


def main():
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
        elif sys.argv[x] == "--check-optimistic":
            optimistic = True
        elif sys.argv[x] == "--check-consistent":
            consistent = True
    heuristic_values = heuristic(heuristic_path)
    start, end, transitions = transition(path,heuristic_values)
    #print(heuristic_values)
    # print(start)
    # print(end)
    #print(transitions)
    #n,visited=astar(start,transitions,end,heuristic_values)
    #visited = astar2(end[0], transitions, end, heuristic_values,heuristic_path)


    # if n != False:
    #     print("[FOUND_SOLUTION]: yes")
    #     print("[STATES_VISITED]: "+str(len(visited)))
    #     print("[PATH_LENGTH]: "+str(len(n["path"].split("=>"))))
    #     print("[TOTAL_COST]: "+str(n["total_cost"]))
    #     print("[PATH]: "+n["path"])
    # else:
    #     print("[FOUND_SOLUTION]: no")




main()
