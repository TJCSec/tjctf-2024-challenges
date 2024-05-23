"""
https://github.com/flavioeverardo/gauss_jordan_elimination/blob/master/tester.py
https://github.com/flavioeverardo/gauss_jordan_elimination/blob/master/tester.py
https://github.com/flavioeverardo/gauss_jordan_elimination/blob/master/tester.py

This module contains all the methods to perform Gauss Jordan Elimination. 

Functions:
For pre process
columns_state_to_matrix -- Transform the state of columns to a single matrix including the parity column
xor_columns             -- Perform xor operation of a single column to the parity column

For GJE
perform_gauss_jordan_elimination -- Entire GJE process
swap -- Sub module for GJE to swap rows
xor  -- Sub module for GJE to xor rows

check_sat      -- Check satisfiability after performing GJE
deduced_clause -- Obtain implications after GJE
"""

import numpy as np

def print_matrix(m):
    for i in range(len(m)):
        print(m[i])
    print()
    
def swap(m, r1, r2):
    """ Swap rows in forward elimination"""
    temp  = m[r1]
    m[r1] = m[r2]
    m[r2] = temp
    return m

def xor(m, i, j):
    """ XOR rows during GJE"""
    for e in range(len(m[0])):
        m[j][e] ^= m[i][e]
    return m

def xor_columns(col, parity):
    """ XOR a column with the parity values from the state  """
    result = []
    for i in range(len(col)):
        result.append(col[i] ^ parity[i])
    return result

def columns_state_to_matrix(state):
    """ Transform the state of columns to a single matrix including the parity column """
    m = []
    lits = []
    for key, values in state.items():
        if key != "parity":
            m.append(values)
            lits.append(key)
    m += [state["parity"]]
    m = np.array(m).T.tolist()
    return m, lits

def remove_rows_zeros(m):
    matrix = []
    for row in m:
        if sum(row) > 0:
            matrix.append(row)
    return matrix

def check_sat(m):
    """ Check the matrix satisfiability wrt the augmented (parity) column  """
    conflict = False
    matrix = np.array(m)

    ## If only augmented column remains
    if len(matrix[0]) == 1:
        for i in range(len(matrix)):
            if matrix[i,0] == 1:
                conflict = True
                break
    else:
        ## Check if exist empty odd which means UNSAT i.e. a conflict
        for row in matrix[::-1]:
            if row[-1] == 1 and np.sum(row[:-1]) == 0:
                ## UNSAT
                conflict = True                        
                break 
    return conflict


def deduce_clause(m, lits):
    """ If no conflict, deduce the implications after GJE """
    clause = []

    #Pre work... Remove rows with all zeros
    mm = remove_rows_zeros(m)
    matrix = np.array(mm)

    ## If empty matrix, means there are no implications
    if matrix.size > 0:
        ## If matrix is square
        if len(matrix) >= (len(matrix[0])-1):                 
            for i in range(len(lits)):
                if matrix[i,-1] == 1:
                    clause.append( lits[i])
                else:
                    clause.append(-lits[i])
        else: ## Rectangular matrix
            for row in matrix:
                if np.sum(row[:-1]) == 1:
                    index = np.where(row[:-1] == 1)[0][0]
                    if row[-1] == 1:
                        clause.append( lits[index])
                    else:
                        clause.append(-lits[index])
    return clause


def perform_gauss_jordan_elimination(m, show):
    """ Perform GJE using swap and xor operations """
    if show:
        print("Initial State")
        print_matrix(m)

    if show:
        print("Forward Elimination")
    dimension = len(m)
    #if len(m) > len(m[0]):
    #    dimension = len(m[0])
    if show:
        print("len(m)", len(m), "len(m[0])", len(m[0]), "dimension", dimension)

    ## "Forward Elimination"
    r = 0
    right_most_col = 0
    lowest_row = 0
    for c in range(len(m[0])-1):
        _swap = False
        _xor  = False
        if show:
            print("r", r, "c", c, "value", m[r][c])
        for j in range(r+1, dimension):
            if m[r][c] == 0 and m[j][c] == 1:
                if show:
                    print("Swapping", m[r], "and", m[j])
                m = swap(m,r,j)
                _swap = True
                if show:
                    print_matrix(m)

            if m[r][c] == 1:
                _xor = True
                if m[j][c] == 1:
                    if show:
                        print("XOR Row", r, m[r], "into Row", j, m[j])
                    m = xor(m,r,j)
                    if show:
                         print_matrix(m)

        if m[r][c] == 1:
            right_most_col = c
            lowest_row = r
        if show:
            print("_swap", _swap, "_xor", _xor)
        if _swap or _xor:
            r+=1

    if show:
        print("")
        print("Right Most Column", right_most_col, "lowest row", lowest_row)
        print("Row Echelon Form")
        print_matrix(m)

    if show:
        print("")
        print("Backward Substitution")

    ## "Backward Substitution"
    #r = len(m)-1
    #if len(m)> len(m[0]):
    r = lowest_row
    for c in range(right_most_col, 0, -1):
        _xor  = False
        if show:
            print("r", r, "c,", c, "value", m[r][c])
        for j in range(r-1, -1, -1):
            if m[r][c] == 1 and m[j][c] == 1:
                _xor  = True
                if show:
                    print("XOR Row", r, m[r], "into Row", j, m[j])
                m = xor(m,r,j)
                if show:
                    print_matrix(m)

        if show:
            print("_xor", _xor)
        if m[r][c-1] == 0:
            r-=1

    if show:
        print("")
        print("Result")
        print_matrix(m)


    return m
