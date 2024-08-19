def mbn2str(bn):
    lst = list(bn.items())
    functions=[]
    variables=[]
    for i in range(len(lst)):
        variables.append(list(bn.items())[i][0])
        functions.append(repr(list(bn.items())[i][1]).replace("Symbol('","").replace("')","").replace("AND","And").replace("NOT","Not").replace("OR","Or"))
    return variables,functions
