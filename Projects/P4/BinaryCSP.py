# Hint: from collections import deque
from Interface import *


# = = = = = = = QUESTION 1  = = = = = = = #


def consistent(assignment, csp, var, value):
    """
    Checks if a value assigned to a variable is consistent with all binary constraints in a problem.
    Do not assign value to var.
    Only check if this value would be consistent or not.
    If the other variable for a constraint is not assigned,
    then the new value is consistent with the constraint.

    Args:
        assignment (Assignment): the partial assignment
        csp (ConstraintSatisfactionProblem): the problem definition
        var (string): the variable that would be assigned
        value (value): the value that would be assigned to the variable
    Returns:
        boolean
        True if the value would be consistent with all currently assigned values, False otherwise
    """
    # TODO: Question 1
    for bC in csp.binaryConstraints:
        if bC.affects(var):
            if assignment.isAssigned(bC.otherVariable(var)) and not bC.isSatisfied(value, assignment.assignedValues[bC.otherVariable(var)]):
                    return False
    return True
    raise_undefined_error()


def recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod):
    """
    Recursive backtracking algorithm.
    A new assignment should not be created.
    The assignment passed in should have its domains updated with inferences.
    In the case that a recursive call returns failure or a variable assignment is incorrect,
    the inferences made along the way should be reversed.
    See maintainArcConsistency and forwardChecking for the format of inferences.

    Examples of the functions to be passed in:
    orderValuesMethod: orderValues, leastConstrainingValuesHeuristic
    selectVariableMethod: chooseFirstVariable, minimumRemainingValuesHeuristic
    inferenceMethod: noInferences, maintainArcConsistency, forwardChecking

    Args:
        assignment (Assignment): a partial assignment to expand upon
        csp (ConstraintSatisfactionProblem): the problem definition
        orderValuesMethod (function<assignment, csp, variable> returns list<value>):
            a function to decide the next value to try
        selectVariableMethod (function<assignment, csp> returns variable):
            a function to decide which variable to assign next
        inferenceMethod (function<assignment, csp, variable, value> returns set<variable, value>):
            a function to specify what type of inferences to use
    Returns:
        Assignment
        A completed and consistent assignment. None if no solution exists.
    """
    # TODO: Question 1
    if assignment.isComplete():
        return assignment
    var = selectVariableMethod(assignment, csp)
    if var == None:
        return None
    inferences = set([])
    for value in orderValuesMethod(assignment, csp, var):
        if consistent(assignment, csp, var, value):
            assignment.assignedValues[var] = value
            inferences = inferenceMethod(assignment, csp, var, value)
            if inferences != None:
                result = recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod)
                if result != None:
                    return result
                for item in inferences:
                    assignment.varDomains[item[0]].add(item[1])
    assignment.assignedValues[var] = None
    return None
    raise_undefined_error()


def eliminateUnaryConstraints(assignment, csp):
    """
    Uses unary constraints to eleminate values from an assignment.

    Args:
        assignment (Assignment): a partial assignment to expand upon
        csp (ConstraintSatisfactionProblem): the problem definition
    Returns:
        Assignment
        An assignment with domains restricted by unary constraints. None if no solution exists.
    """
    domains = assignment.varDomains
    for var in domains:
        for constraint in (c for c in csp.unaryConstraints if c.affects(var)):
            for value in (v for v in list(domains[var]) if not constraint.isSatisfied(v)):
                domains[var].remove(value)
                # Failure due to invalid assignment
                if len(domains[var]) == 0:
                    return None
    return assignment


def chooseFirstVariable(assignment, csp):
    """
    Trivial method for choosing the next variable to assign.
    Uses no heuristics.
    """
    for var in csp.varDomains:
        if not assignment.isAssigned(var):
            return var


# = = = = = = = QUESTION 2  = = = = = = = #


def minimumRemainingValuesHeuristic(assignment, csp):
    """
    Selects the next variable to try to give a value to in an assignment.
    Uses minimum remaining values heuristic to pick a variable. Use degree heuristic for breaking ties.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
    Returns:
        the next variable to assign
    """
    nextVar = None
    domains = assignment.varDomains

    # TODO: Question 2
    unassigned = [var for var in assignment.varDomains if not assignment.isAssigned(var)]
    if len(unassigned) != 0:
        min = list(unassigned)[0]
        for var in unassigned:
            if var != min:
                r = len(assignment.varDomains[var])
                n = len(assignment.varDomains[min])
                if r < n:
                    min = var
                elif r == n:
                    if countConstraints(assignment, csp, var, unassigned) > countConstraints(assignment, csp, min, unassigned):
                        min = var
        return min
    else:
        return None
    raise_undefined_error()


def countConstraints(assignment, csp, var, unassigned):
    i = 0
    for bC in csp.binaryConstraints:
        if bC.affects(var) and (bC.otherVariable(var) in unassigned):
            i += 1
    return i


def orderValues(assignment, csp, var):
    """
    Trivial method for ordering values to assign.
    Uses no heuristics.
    """
    return list(assignment.varDomains[var])


# = = = = = = = QUESTION 3  = = = = = = = #


def leastConstrainingValuesHeuristic(assignment, csp, var):
    """
    Creates an ordered list of the remaining values left for a given variable.
    Values should be attempted in the order returned.
    The least constraining value should be at the front of the list.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
        var (string): the variable to be assigned the values
    Returns:
        list<values>
        a list of the possible values ordered by the least constraining value heuristic
    """
    # TODO: Question 3
    constraints = csp.binaryConstraints
    values = assignment.varDomains[var]
    pairs = []
    for value in values:
        count = 0
        for constraint in constraints:
            if constraint.affects(var):
                count += len([val for val in assignment.varDomains[constraint.otherVariable(var)] if constraint.isSatisfied(val, value)])
        pairs.append((value, count))
    return [item[0] for item in sorted(pairs, key=lambda x: x[1])]
    raise_undefined_error()


def noInferences(assignment, csp, var, value):
    """
    Trivial method for making no inferences.
    """
    return set([])


# = = = = = = = QUESTION 4  = = = = = = = #


def forwardChecking(assignment, csp, var, value):
    """
    Implements the forward checking algorithm.
    Each inference should take the form of (variable, value)
    where the value is being removed from the domain of variable.
    This format is important so that the inferences can be reversed
    if they result in a conflicting partial assignment.
    If the algorithm reveals an inconsistency,
    any inferences made should be reversed before ending the function.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
        var (string): the variable that has just been assigned a value
        value (string): the value that has just been assigned
    Returns:
        set< tuple<variable, value> >
        the inferences made in this call or None if inconsistent assignment
    """
    inferences = set([])

    # TODO: Question 4
    if not consistent(assignment, csp, var, value):
        return None
    connectedConstraints = [constraint for constraint in csp.binaryConstraints if constraint.affects(var)]
    for constraint in connectedConstraints:
        connectedVariable = constraint.otherVariable(var)
        if not assignment.varDomains[connectedVariable]:
            return None
        if assignment.isAssigned(connectedVariable):
            if not constraint.isSatisfied(value, assignment.assignedValues[connectedVariable]):
                return None
        else:
            domain = assignment.varDomains[connectedVariable].copy()
            count = 0
            for val in domain:
                if not constraint.isSatisfied(value, val):
                    inferences.add((connectedVariable, val))
                    count += 1
            if len(domain) == count:
                return None
    for inference in inferences:
        assignment.varDomains[inference[0]].remove(inference[1])
    return inferences
    raise_undefined_error()


# = = = = = = = QUESTION 5  = = = = = = = #


def revise(assignment, csp, var1, var2, constraint):
    """
    Helper function to maintainArcConsistency and AC3.
    Remove values from var2 domain if constraint cannot be satisfied.
    Each inference should take the form of (variable, value)
    where the value is being removed from the domain of variable.
    This format is important so that the inferences can be reversed
    if they result in a conflicting partial assignment.
    If the algorithm reveals an inconsistency,
    any inferences made should be reversed before ending the function.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
        var1 (string): the variable with consistent values
        var2 (string): the variable that should have inconsistent values removed
        constraint (BinaryConstraint): the constraint connecting var1 and var2
    Returns:
        set<tuple<variable, value>>
        the inferences made in this call or None if inconsistent assignment
    """
    inferences = set([])

    # TODO: Question 5
    revised = False
    domain2 = assignment.varDomains[var2].copy()
    for val2 in domain2:
        if sum([constraint.isSatisfied(val1, val2) for val1 in assignment.varDomains[var1]]) == 0:
            inferences.add((var2, val2))
            revised = True
    if len(inferences) == len(domain2):
        return None
    else:
        for inference in inferences:
            assignment.varDomains[inference[0]].remove(inference[1])
        return inferences
    raise_undefined_error()


def maintainArcConsistency(assignment, csp, var, value):
    """
    Implements the maintaining arc consistency algorithm.
    Inferences take the form of (variable, value)
    where the value is being removed from the domain of variable.
    This format is important so that the inferences can be reversed
    if they result in a conflicting partial assignment.
    If the algorithm reveals an inconsistency,
    and inferences made should be reversed before ending the function.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
        var (string): the variable that has just been assigned a value
        value (string): the value that has just been assigned
    Returns:
        set<<variable, value>>
        the inferences made in this call or None if inconsistent assignment
    """
    inferences = set([])
    domains = assignment.varDomains

    # TODO: Question 5
    if not consistent(assignment, csp, var, value):
        return None
    if len(domains) == 0:
        return None
    queue = []
    for var in assignment.varDomains.keys():
        queue += [(var, constraint.otherVariable(var)) for constraint in csp.binaryConstraints if (constraint.affects(var)) and (not assignment.isAssigned(constraint.otherVariable(var)))]
    while queue != []:
        (var1, var2) = queue.pop(0)
        for constraint in csp.binaryConstraints:
            inf = set([])
            if constraint.affects(var1) and constraint.affects(var2):
                inf = revise(assignment, csp, var1, var2, constraint)
                if inf != None:
                    if len(inf) != 0:
                        inferences = inferences.union(inf)
                        for otherConstraint in csp.binaryConstraints:
                            if (otherConstraint.affects(var2)):
                                if len(assignment.varDomains[otherConstraint.otherVariable(var2)]) == 0:
                                    for inference in inferences:
                                        assignment.varDomains[inference[0]].add(inference[1])
                                    return None
                                queue.append((var2, otherConstraint.otherVariable(var2)))
                else:
                    for inference in inferences:
                        assignment.varDomains[inference[0]].add(inference[1])
                    return None
    return inferences
    
    raise_undefined_error()


# = = = = = = = QUESTION 6  = = = = = = = #


def AC3(assignment, csp):
    """
    AC3 algorithm for constraint propagation.
    Used as a pre-processing step to reduce the problem
    before running recursive backtracking.

    Args:
        assignment (Assignment): the partial assignment to expand
        csp (ConstraintSatisfactionProblem): the problem description
    Returns:
        Assignment
        the updated assignment after inferences are made or None if an inconsistent assignment
    """
    inferences = set([])

    # TODO: Question 6
    #  Hint: implement revise first and use it as a helper function"""
    queue = []
    for var in assignment.varDomains.keys():
        queue += [(var, constraint.otherVariable(var)) for constraint in csp.binaryConstraints if constraint.affects(var)]
    while queue != []:
        var1, var2 = queue.pop(0)
        for constraint in csp.binaryConstraints:
            inf = set([])
            if constraint.affects(var1) and constraint.affects(var2):
                inf = revise(assignment, csp, var1, var2, constraint)
            if inf != None:
                if len(inf) != 0:
                    inferences.union(inf)
                    for otherConstraint in csp.binaryConstraints:
                        if (otherConstraint.affects(var2)) and (otherConstraint.otherVariable(var2) != var1):
                            queue.append((var2, otherConstraint.otherVariable(var2)))
            else:
                for inference in inferences:
                    assignment.varDomains[inference[0]].add(inference[1])
                return None
    return assignment
    raise_undefined_error()


def solve(csp, orderValuesMethod=leastConstrainingValuesHeuristic,
          selectVariableMethod=minimumRemainingValuesHeuristic,
          inferenceMethod=forwardChecking, useAC3=True):
    """
    Solves a binary constraint satisfaction problem.

    Args:
        csp (ConstraintSatisfactionProblem): a CSP to be solved
        orderValuesMethod (function): a function to decide the next value to try
        selectVariableMethod (function): a function to decide which variable to assign next
        inferenceMethod (function): a function to specify what type of inferences to use
        useAC3 (boolean): specifies whether to use the AC3 pre-processing step or not
    Returns:
        dictionary<string, value>
        A map from variables to their assigned values. None if no solution exists.
    """
    assignment = Assignment(csp)

    assignment = eliminateUnaryConstraints(assignment, csp)
    if assignment is None:
        return assignment

    if useAC3:
        assignment = AC3(assignment, csp)
        if assignment is None:
            return assignment

    assignment = recursiveBacktracking(
        assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod)
    if assignment is None:
        return assignment

    return assignment.extractSolution()
