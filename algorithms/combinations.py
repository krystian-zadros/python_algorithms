# The function is implementation of an algorithm of creating a list of combinations without repetitions.
# Wordy description was found in the book:
# Z.J.Czech, S.Deorowicz, P.Fabian, "Algorytmy i struktury danych. Wybrane zagadnienia". Wydawnictwo Politechniki Slaskiej, Gliwice 2007, s. 197.
# Function returns list of algorithms, represented as lists. Each combination has "length" elements.
# Each element in combination denotes position of variable in list variables.
# For example for arguments variables=["A","B","C","D"] and length=3 one of algorithms
# will be [0,2,3] that denotes ["A',"C","D"].
def getCombinationsSortedLexicographically(variables, length):
    maxVal = len(variables) - 1
    Combinations = []
    c = []

    # Prepare inital combination.
    for i in range(length):
        c.append(i)
    Combinations.append(c)
    c = c[:]

    i = length - 1
    while i >= 0:
        if c[i] > maxVal:
            i -= 1
            continue

        while c[i] <= maxVal:
            j = length - 1
            if j > i:
                c = initNextVals(c, i)
                if c[length - 1] <= maxVal:
                    c = addSingleCombination(Combinations, c)
            while j > i:
                if c[j] + 1 > maxVal:
                    break
                c[j] += 1
                j -= 1
                c = addSingleCombination(Combinations, c)
            c[i] += 1
            if c[i] <= maxVal and i == (length - 1):
                c = addSingleCombination(Combinations, c)
        i -= 1
        if i >= 0:
            c[i] += 1
    return Combinations


def initNextVals(c, i):
    added = 1
    for j in range(i + 1, len(c)):
        c[j] = c[i] + added
        added += 1
    return c


def addSingleCombination(Combinations, combination):
    Combinations.append(combination)
    return Combinations[-1][:]
