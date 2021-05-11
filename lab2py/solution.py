import sys


def read_clause():
    clauses = []
    with open(sys.argv[2], encoding='utf-8') as file:
        for line in file:
            if not line.startswith('#'):
                clause = line.strip('\n').lower().split(' v ')
                clause_dict = {}
                for literal in clause:
                    if literal.startswith("~"):
                        clause_dict[literal] = False
                    else:
                        clause_dict[literal] = True
                clauses.append(clause_dict)
    return clauses


def read_recipe():
    clauses = []
    operators = []
    with open(sys.argv[3], encoding='utf-8') as file:
        for line in file:
            if not line.startswith('#'):
                operator = line.strip('\n')[-1]
                line = line.replace(operator, '')
                line = line[0:-2]
                clause = line.strip('\n').lower().split(' v ')
                clause_dict = {}
                operators.append(operator)
                for literal in clause:
                    if literal.startswith("~"):
                        clause_dict[literal] = False
                    else:
                        clause_dict[literal] = True
                clauses.append(clause_dict)
    return clauses, operators


def resolve_goal(goal):
    new_goal = []
    for key in goal.keys():
        dict = {}
        if goal[key] == False:
            newkey = key[1:]
        else:
            newkey = "~" + key
        dict[newkey] = not goal[key]
        new_goal.append(dict)
    return new_goal


def print_clause(clause, bool=True):
    string = ""
    i = 0
    for literal in clause.keys():
        if i != 0:
            string += " v "
        if bool == True:
            string += literal
        else:
            if clause[literal] == True:
                string += "~" + literal
            else:
                string += literal[1:]
        i += 1
    return string


def not_tautology(resolved):
    for literal1 in resolved.keys():
        for literal2 in resolved.keys():
            if resolved[literal1] != resolved[literal2] and (literal2 + "~" == literal1 or literal2 == literal1 + "~"):
                return False
    return True


def delete_strategy(clauses1, clauses2, duplicated1, duplicated2, index):
    for i in range(0, len(clauses1)):
        for j in range(0, len(clauses2)):
            if clauses1 == clauses2 and index == 0:
                if i != j and clauses1[i].items() <= clauses2[j].items():
                    duplicated1[j + 1] = j + 1
                if not not_tautology(clauses1[i]):
                    duplicated1[i + 1] = i + 1
            elif clauses1 == clauses2 and index != 0:
                if i != j and clauses1[i].items() <= clauses2[j].items():
                    duplicated1[j + index + 1] = j + index + 1
                if not not_tautology(clauses1[i]):
                    duplicated2[i + index + 1] = i + index + 1
            else:
                if clauses1[i].items() < clauses2[j].items():
                    duplicated2[j + index + 1] = j + index + 1
                if clauses1[i].items() >= clauses2[j].items():
                    duplicated1[i + 1] = i + 1


def select_clauses(clauses, clauses1, clauses2, duplicated1, duplicated2, i):
    pairs = []
    numbers1 = []
    numbers2 = []
    j = 0
    for clause1 in clauses1:
        i += 1
        for literal in clause1.keys():
            j = 0
            for clause2 in clauses2:
                j += 1
                if i not in duplicated1 and j + len(clauses) not in duplicated2:
                    if clause1 != clause2:
                        if clause1[literal] == False:
                            find_literal = literal[1:]
                        else:
                            find_literal = "~" + literal
                        if find_literal in clause2:
                            if clause1[literal] != clause2[find_literal]:
                                return_clause = dict((i, clause1[i]) for i in clause1 if i != literal)
                                return_new_clause = dict((i, clause2[i]) for i in clause2 if i != find_literal)
                                result = {}
                                if return_clause:
                                    result.update(return_clause)
                                if return_new_clause:
                                    result.update(return_new_clause)
                                if result not in pairs:
                                    pairs.append(result)
                                    numbers1.append(i)
                                    numbers2.append(j + len(clauses))

    return pairs, numbers1, numbers2


def refutation_resolution(clauses, goal, duplicated1, duplicated2):
    new = goal
    new_numbers1 = []
    new_numbers2 = []
    for i in range(0, len(goal)):
        new_numbers1.append(0)
        new_numbers2.append(0)
    while True:
        delete_strategy(clauses, new, duplicated1, duplicated2, 0)
        delete_strategy(new, new, duplicated2, duplicated2, len(clauses))

        pairs1, numbers11, numbers21 = select_clauses(clauses, clauses, new, duplicated1, duplicated2, 0)
        pairs2, numbers12, numbers22 = select_clauses(clauses, new, new, duplicated2, duplicated2, len(clauses))

        pairs = pairs1 + pairs2
        numbers1 = numbers11 + numbers12
        numbers2 = numbers21 + numbers22

        newNew = []
        i = 0;
        for pair in pairs:
            if pair not in new and not_tautology(pair) and pair not in clauses:
                newNew.append(pair)
                new_numbers1.append(numbers1.__getitem__(i))
                new_numbers2.append(numbers2.__getitem__(i))
            if not pair:
                new.append(pair)
                return True, new, new_numbers1, new_numbers2
            i += 1

        if all(item in newNew for item in new) or len(newNew) == 0:
            return False, False, False, False
        new = new + newNew


def print_resolved(clauses, resolvents, numbers1, numbers2, goal):
    nilNumbers1 = {}
    nilNumbers2 = {}
    first1 = numbers1[len(numbers1) - 1]
    first2 = numbers2[len(numbers2) - 1]
    nilNumbers1[first1] = first1
    nilNumbers2[first2] = first2

    stack = []
    stack.append(first2)
    if first1 > len(clauses):
        stack.append(first1)
    while len(stack) != 0:
        pop = stack.pop()
        first1 = numbers1[pop - len(clauses) - 1]
        first2 = numbers2[pop - len(clauses) - 1]
        if first1 > len(clauses):
            stack.append(first1)
            nilNumbers2[first1] = first1
        else:
            nilNumbers1[first1] = first1
        if first2 != 0:
            stack.append(first2)
        nilNumbers2[first2] = first2

    i = 1
    for clause in clauses:
        if i in nilNumbers1:
            string = str(i) + ". "
            string += print_clause(clause)
            print(string)
        i += 1
    for clause in resolvents:
        if i - len(goal) - 1 == len(clauses):
            print("============")
        if i in nilNumbers1 or i in nilNumbers2 or not clause:
            string = str(i) + ". "
            if not clause:
                string += "NIL"
            else:
                string += print_clause(clause)
            if i > len(clauses) + len(goal):
                string += " (" + str(numbers1[i - len(clauses) - 1]) + "," + str(numbers2[i - len(clauses) - 1]) + ")"
            print(string)
        i += 1
    print("============")
    print("[CONCLUSION]: " + print_clause(goal) + " is true")


def cooking():
    goal_clauses, operators = read_recipe()
    clauses = read_clause()
    for i in range(0, len(operators)):
        print("User's command: " + print_clause(goal_clauses[i]) + " " + operators[i])
        if operators[i] == '?':
            duplcated = {}
            duplicated_goal = {}
            goal = resolve_goal(goal_clauses[i])
            delete_strategy(clauses, clauses, duplcated, duplcated, 0)
            bool, resolvents, numbers1, numbers2 = refutation_resolution(clauses, goal, duplcated, duplicated_goal)
            if bool == True:
                print_resolved(clauses, resolvents, numbers1, numbers2, goal_clauses[i])
            else:
                print("[CONCLUSION]: " + print_clause(goal[0], False) + " is unknown")
        if operators[i] == '+':
            print("Added " + print_clause(goal_clauses[i]))
            clauses.append(goal_clauses[i])
        if operators[i] == '-':
            print("removed " + print_clause(goal_clauses[i]))
            clauses.remove(goal_clauses[i])
        print("\n\n")


if sys.argv[1] == "resolution":
    clauses = read_clause()
    duplcated_start = {}
    duplicated_goal = {}
    real_goal = clauses.pop(len(clauses) - 1)
    goal = resolve_goal(real_goal)
    delete_strategy(clauses, clauses, duplcated_start, duplcated_start, 0)

    bool, resolvents, numbers1, numbers2 = refutation_resolution(clauses, goal, duplcated_start, duplicated_goal)
    if bool == True:
        print_resolved(clauses, resolvents, numbers1, numbers2, real_goal)
    else:
        print("[CONCLUSION]: " + print_clause(real_goal) + " is unknown")
else:
    cooking()
