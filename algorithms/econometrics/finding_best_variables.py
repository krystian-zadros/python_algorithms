from pandas import DataFrame
import pandas as pd
import algorithms.combinations as combinatory_algorithms

# Method finds the best set of variables, that can be used in making an econometric model.
# Input file has to have columns where first denotes labels, second denotes
# independent variable and other ones denote dependent variables.
def hellwigs_method(csv_filepath):
    df = pd.read_csv(csv_filepath, index_col=0, header=0)
    headers = df.columns.get_values()
    headersDependent = headers[1:]
    headerIndependent = headers[0]

    R0 = []
    for variable in headersDependent:
        correlation = df[headerIndependent].corr(df[variable])
        R0 += [correlation]
    R0 = pd.Series(R0, index=headersDependent)

    corrsMatrix = df.corr()[headersDependent][:].loc[headersDependent]

    print("df:", df, sep="\n", end="\n\n")
    print("headerIndependent", headerIndependent)
    print("headersDependent:", headersDependent)
    print("Correlations matrix: ", corrsMatrix, sep="\n", end="\n\n")
    print("Correlations R0: ", R0, sep="\n", end="\n\n")

    Combinations = []
    for i in range(1, len(headersDependent) + 1):
        combination = combinatory_algorithms.getCombinationsSortedLexicographically(headersDependent, i)
        for c in combination:
            Combinations.append(c)
    print("Combinations: ", Combinations, sep="\n", end="\n\n")
    print("Combinations size: ", len(Combinations), sep="\n", end="\n\n")
    print("Theoretical amount of unique combinations (2^m-1)={amount} for m={m} with current {now} combinations is {is_ok}.\n".format(
        m=len(headersDependent),
        amount=2**(len(headersDependent))-1,
        now=len(Combinations),
        is_ok="ok" if (len(Combinations) == (2**(len(headersDependent))-1)) else "wrong"
    )
    )

    listOfCapacities = []
    combinationId = 0
    functionDependentVariableIdToName = lambda id: headersDependent[id]
    for combination in Combinations:
        capacity = 0
        variablesNameInCurrentCombination = functionDependentVariableIdToName(combination)

        # Count integral informational capacity.
        for variableId in combination:
            currentVariableName = headersDependent[variableId]
            corrWithInd = R0.loc[currentVariableName]

            # Count individual informational capacity.
            corrsWithDepSum = corrsMatrix[variablesNameInCurrentCombination] \
                .loc[currentVariableName] \
                .drop(currentVariableName) \
                .abs() \
                .sum()
            capacity += (corrWithInd ** 2) / (corrsWithDepSum + 1)
        print('Combination ', combination, ', id: ', combinationId, ', capacity: ', capacity)

        listOfCapacities.append([combination, capacity])
        combinationId += 1

    print()
    listOfCapacities = DataFrame(listOfCapacities, columns=['combination', 'capacity'])
    print("List of capacities: ", listOfCapacities, sep="\n", end="\n\n")

    bestCombination = listOfCapacities.sort_values(by='capacity', ascending=0).iloc[0]['combination']
    translateCombinationNames = lambda x: headersDependent[x]
    print('Best combination:\n\tas numbers: {}\n\tmeans: {}'.format(
        bestCombination,
        translateCombinationNames(bestCombination)
    )
    )
