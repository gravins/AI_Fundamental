from itertools import combinations
from time import time
import numpy as np
import copy

def AC3(csp, neighbor):
    """
    This AC3 function implements the algorithm show in Figure 6.3 pag 209 of the AIMA book

    :param csp: dict{X: list of variables,
                     D: dictionary {variable: [domain]},
                     C: dictionary {(node_i, node_j): list of constraints}
    :param neighbor: dict {var: [neighbor]}
    :return: a (bool, arc consistent domain(if exist)) with false if an inconsistency is found and true otherwise
    """
    queue = []
    for x in neighbor.keys():
        if len(neighbor[x]) > 0:
            for y in neighbor[x]:
                queue.append((x, y))

    counts = []
    count_for = 0
    while len(queue) != 0:
        arc = queue.pop(0)
        res, csp_new, c = revise(csp, arc[0], arc[1])
        csp = csp_new
        if res:
            if len(csp["D"][arc[0]]) == 0:
                counts.append(c)
                print("AC3 require ", len(counts), " while steps. In average each of those require ", np.average(counts), " steps. The total of basic operations is ", np.sum(counts)) #len(counts)*np.sum(counts)+count_for)
                return False, csp["D"]
            for Xk in neighbor[arc[0]]:
                count_for += 1
                if Xk != arc[1]:
                    queue.append((Xk, arc[0]))
        counts.append(max(c,count_for))
    print("AC3 require ", len(counts), " while steps. In average each of those require ", np.average(counts), " steps. The total of basic operations is ", np.sum(counts))#len(counts)*np.sum(counts))+count_for)
    return True, csp["D"]


def revise(csp, Xi, Xj):
    """
    This function try to revise the domain
    :param csp: list(X,D,C) where X is a list of variables, D is a dictionary {variable: [domain]},
                and C is a list of constraints
    :param Xi: node i
    :param Xj: node j
    :return: a (bool, csp) with true iff we revise the domain of Xi
    """
    count = 0
    revised = False
    if (Xi, Xj) in csp["C"].keys():
        for Vi in csp["D"][Xi]:
            satisfy = False
            for Vj in csp["D"][Xj]:
                count += 1
                if (Vi, Vj) in csp["C"][(Xi, Xj)]:
                    satisfy = True
                    break
            if not satisfy:
                csp["D"][Xi].remove(Vi)
                revised = True

    return revised, csp, count



def AC4(csp):
    """
    This AC4 function implements the algorithm show in Section 4.2 chapter 4 pag 87
    of Edward Tsang's book (Foundations of Constraint Satisfaction)

    :param csp: dict{X: list of variables,
                     D: dictionary {variable: [domain]},
                     C: dictionary {(node_i, node_j): list of constraints}
    :return: a (bool, arc consistent domain(if exist)) with false if an inconsistency is found and true otherwise
    """
    # Construction and initialization of support sets (support and counter)
    support = {}
    for x in csp["X"]:
        for val in csp["D"][x]:
            support[(x, val)] = []

    # deletion_stream mantain all <variable-value>, where value has been removed
    # from domain of variable , but the effect of the removal has not yet been propagated
    deletion_stream = []
    counter = {}
    count = 0
    for (Xi, Xj) in csp["C"].keys():
        for Vi in csp["D"][Xi]:
            tot = 0
            for Vj in csp["D"][Xj]:
                count += 1
                if (Vi, Vj) in csp["C"][(Xi, Xj)]:
                    tot += 1
                    support[(Xj, Vj)].append((Xi, Vi))
            if tot == 0:
                csp["D"][Xi].remove(Vi)
                deletion_stream.append((Xi, Vi))
                if len(csp["D"][Xi]) == 0:
                    print("AC4 require ", count, " steps")
                    return False, csp["D"]
            else:
                counter[(Xi, Xj, Vi)] = tot

    # Propagation of removed values
    count2 = 0
    while len(deletion_stream) != 0:
        (xi, vi) = deletion_stream.pop(0)
        for (xj, vj) in support[(xi, vi)]:
            count2 += 1
            counter[(xj, xi, vj)] -= 1
            if counter[(xj, xi, vj)] == 0 and vj in csp["D"][xj]:
                csp["D"][xj].remove(vj)
                deletion_stream.append((xj, vj))
                if len(csp["D"][xj]) == 0:
                    print("AC4 require ", max(count,count2), " steps")
                    return False, csp["D"]

    print("AC4 require ", max(count,count2), " steps")
    return True, csp["D"]




if __name__ == "__main__":
    # CSP problem for coloring the map of Australia with a fix "wa" state
    print("*** Example coloring Australia state ***\n")
    neighbors = {"wa": ["nt", "sa"], "nt": ["wa", "sa","q"], "sa": ["nt", "wa","q","nsw","v"], "q": ["nt", "sa", "nsw"], "nsw": ["q", "sa", "v"], "v": ["nsw", "sa"]}

    X = ["wa", "nt", "sa", "q", "nsw", "v"]
    D = {}
    for el in X:
        if el == "wa":
            D[el] = ["R"]
        else:
            D[el] = ["R", "G", "B"]
    constr = [(x, y) for x in ["R", "G", "B"] for y in ["R", "G", "B"] if x != y]
    C = {}
    for state in neighbors.keys():
        for neighbor_state in neighbors[state]:
            C[(state, neighbor_state)] = constr

    # Run AC3
    start = time()
    consistency, value = AC3(copy.deepcopy({"X": X, "D": D, "C": C}), neighbors)
    s = time() - start
    if consistency:
        print("AC3 -> Exist consistent solution: ", value)
    else:
        print("AC3 -> No consistent solution!")
    print("solution retrieved in: %.4g s" % s)
    print("\n")

    # Run AC4
    start = time()
    consistency, value = AC4(copy.deepcopy({"X": X, "D": D, "C": C}))
    s = time() - start
    if consistency:
        print("AC4 -> Exist consistent solution: ", value)
    else:
        print("AC4 -> No consistent solution!")
    print("solution retrieved in: %.4g s" % s)
    print("\n")

    ############################################################################
    # Arc consistent CSP problem for sudoku
    print("\n*** Example sudoku ***\n")
    X = [chr(r)+str(c) for r in range(ord("a"), ord("i")+1) for c in range(1,10)]
    D = {}
    for x in X:
        D[x] = [k for k in range(10)]

    D['a1'] = [2]
    D['b1'] = [4]
    D['c3'] = [3]
    D['a6'] = [5]
    D['a9'] = [8]
    D['e6'] = [6]
    D['f3'] = [1]
    D['f6'] = [9]
    D['h1'] = [7]
    D['i6'] = [1]

    C = {}
    # Add constraints regarding rows
    for r in range(ord("a"), ord("i")+1):
        for c1 in range(1,10):
            for c2 in range(c1+1,10):
                C[(chr(r)+str(c1), chr(r)+str(c2))] = [(x, y) for x in range(1,10) for y in range(1,10) if x != y]
    # Add constraints regarding columns
    for c in range(1,10):
        for r1 in range(ord("a"), ord("i")+1):
            for r2 in range(r1+1, ord("i")+1):
                C[(chr(r1)+str(c), chr(r2)+str(c))] = [(x, y) for x in range(1,10) for y in range(1,10) if x != y]

    # Add constraints regarding 3x3 box
    for b in range(1,3):
        for b2 in range(1,3):
            for r1 in range(3*b + ord("a"), 3*b + ord("c")+1):
                for c1 in range(b2 + 1, 3*b2 + 4):
                    for r2 in range(r1 + 1, 3*b + ord("c")+1):
                        for c2 in range(3*b2 + 1, 3*b2 + 4):
                            if c1 != c2:
                                C[(chr(r1)+str(c1), chr(r2)+str(c2))] = [(x, y) for x in range(1,10) for y in range(1,10) if x != y]

    neighbors = {}
    for el in X:
        for (xi,xj) in C.keys():
            if el == xi:
                if el in neighbors.keys():
                    neighbors[el].append(xj)
                else:
                    neighbors[el] = [xj]
    # Run AC3
    start = time()
    consistency, value = AC3(copy.deepcopy({"X": X, "D": D, "C": C}), neighbors)
    s = time() - start
    if consistency:
        print("AC3 -> Exist consistent solution: ", value)
    else:
        print("AC3 -> No consistent solution!")
    print("solution retrieved in: %.4g s" % s)
    print("\n")

    # Run AC4
    start = time()
    consistency, value = AC4(copy.deepcopy({"X": X, "D": D, "C": C}))
    s = time() - start
    if consistency:
        print("AC4 -> Exist consistent solution: ", value)
    else:
        print("AC4 -> No consistent solution!")
    print("solution retrieved in: %.4g s" % s)

    ############################################################################
    # NO arc consistent CSP problem for sudoku
    print("\n*** No arc consistent example sudoku ***\n")
    D['g1'] = [2]
    # Run AC3
    start = time()
    consistency, value = AC3(copy.deepcopy({"X": X, "D": D, "C": C}), neighbors)
    s = time() - start
    if consistency:
        print("AC3 -> Exist consistent solution: ", value)
    else:
        print("AC3 -> No consistent solution!")
    print("solution retrieved in: %.4g s" % s)
    print("\n")

    # Run AC4
    start = time()
    consistency, value = AC4(copy.deepcopy({"X": X, "D": D, "C": C}))
    s = time() - start
    if consistency:
        print("AC4 -> Exist consistent solution: ", value)
    else:
        print("AC4 -> No consistent solution!")
    print("solution retrieved in: %.4g s" % s)
