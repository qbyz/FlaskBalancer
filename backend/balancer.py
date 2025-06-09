from sympy import Matrix, lcm
from itertools import product
import time


# ========== Core Logic ==========

def parse_equation(ogString, race):
    if '=' not in ogString:
        return "Invalid Equation (No '=')", "", "Invalid Equation (No '=')", "", "", ""

    if race:
        startTime = time.time()
    sides = ogString.split('=')
    reactants = sides[0].split('+')
    products = sides[1].split('+')

    def oneSide(side):
        sideSplit = []
        sideVals = []

        for i in range(len(side)):
            sideSplit.append(list(side[i].replace(" ", "")))
            sideVals.append(dict())

        for counter, comp in enumerate(sideSplit):
            i = 0
            const = 1
            stack = []
            temp_dict = {}

            while i < len(comp):
                if comp[i] == '(':
                    stack.append(temp_dict)
                    temp_dict = {}
                    i += 1
                elif comp[i] == ')':
                    i += 1
                    polydig = ''
                    if i < len(comp) and comp[i] == '^':
                        i += 1
                        while i < len(comp) and comp[i].isdigit():
                            polydig += comp[i]
                            i += 1
                    polydig = int(polydig) if polydig else 1
                    for key in temp_dict:
                        temp_dict[key] *= polydig
                    formDict = stack.pop()
                    for key in temp_dict:
                        if key in formDict:
                            formDict[key] += temp_dict[key]
                        else:
                            formDict[key] = temp_dict[key]
                    temp_dict = formDict
                elif comp[i].isdigit():
                    const = ''
                    while i < len(comp) and comp[i].isdigit():
                        const += comp[i]
                        i += 1
                    const = int(const) if const else 1
                elif comp[i].isupper():
                    element = comp[i]
                    if i + 1 < len(comp) and comp[i + 1].islower():
                        i += 1
                        element += comp[i]
                    i += 1
                    subscript = ''
                    if i < len(comp) and comp[i] == '^':
                        i += 1
                        while i < len(comp) and comp[i].isdigit():
                            subscript += comp[i]
                            i += 1
                    subscript = int(subscript) if subscript else 1
                    if element in temp_dict:
                        temp_dict[element] += const * subscript
                    else:
                        temp_dict[element] = const * subscript
                else:
                    i += 1
            sideVals[counter] = temp_dict
        print(sideVals)
        return sideVals

    def mergeDicts(dicts):
        result = dict()
        for i in dicts:
            for j in i:
                result[j] = result.get(j, 0) + i[j]
        return result

    def createEquation(reacts, prods):
        compoundList = reacts + prods
        uniqueElements = list(mergeDicts(compoundList).keys())
        equations = [[] for _ in range(len(uniqueElements))]
        for i, elem in enumerate(uniqueElements):
            for j in range(len(compoundList)):
                coeff = compoundList[j].get(elem, 0)
                if j >= len(reacts):  # If it's a product, negate it
                    coeff *= -1
                equations[i].append(coeff)
        print(equations)
        return equations, uniqueElements, compoundList

    def solver(eqs):
        matrix = Matrix(eqs)
        nullSpace = matrix.nullspace()
        if not nullSpace:
            return False

        max_coeff = 10  # Increase if needed (Brute Forces so try not to)
        for coeffs in product(range(1, max_coeff + 1), repeat=len(nullSpace)):
            # Initialize candidate with the first scaled null space vector
            candidate = coeffs[0] * nullSpace[0]

            # Add the remaining scaled null space vectors
            for i in range(1, len(coeffs)):
                candidate += coeffs[i] * nullSpace[i]

            # Now candidate is a sympy matrix. Extract the elements as a list
            candidate_list = candidate.tolist()  # Convert the matrix to a list of lists
            # If the null space vectors are column vectors, candidate will be a list of lists like [[val1], [val2], ...]
            # We want a single list of values.
            candidate_values = [item for sublist in candidate_list for item in sublist]

            l = lcm([i.q for i in candidate_values])
            candidate_ints = [int(v * l) for v in candidate_values]

            if all(x > 0 for x in candidate_ints):
                return candidate_ints

        return None

    reacts = oneSide(reactants)
    prods = oneSide(products)
    matrix, elements, compoundList = createEquation(reacts, prods)

    coeffs = solver(matrix)

    if not coeffs:
        return "Could not balance the equation.", "", "", ""

    balanced_eq = ""
    for i in range(len(coeffs)):
        compound = reactants[i] if i < len(reacts) else products[i - len(reacts)]
        balanced_eq += f"{coeffs[i]}{compound}"
        if i == len(reacts) - 1:
            balanced_eq += " = "
        elif i < len(coeffs) - 1:
            balanced_eq += " + "

    matrix_str = "\n".join(str(row) for row in matrix)
    react_str = "\n".join(f"{k}: {v}" for k, v in mergeDicts(reacts).items())
    prod_str = "\n".join(f"{k}: {v}" for k, v in mergeDicts(prods).items())
    element_info = f"Reactants:\n{react_str}\n\nProducts:\n{prod_str}"

    if race:
        endTime = time.time()
        runTime = endTime - startTime
    else:
        runTime = None
    return ogString, matrix_str, balanced_eq, element_info, runTime, coeffs