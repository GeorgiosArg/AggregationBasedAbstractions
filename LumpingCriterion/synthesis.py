def synthesis(variables,functions,aggregation_functions):
    
    list_of_merged_components = []
    X_minus = set()
    for function in aggregation_functions:
        list_of_merged_variables_fun = []
        for variable in variables:
            if variable in function:
                list_of_merged_variables_fun.append(variable)
            if 'Not('+variable+')' in function:
                X_minus.add(variable)
        list_of_merged_components.append(list_of_merged_variables_fun)

    X_plus = set(variables)-X_minus
    
    merged_variables=[]
    for l in list_of_merged_components:
        for variable in l:
            merged_variables.append(variable)


    #the size of the reduced BN is the following
    m = len(variables)-len(merged_variables)+len(list_of_merged_components)

    #the size of the original BN
    n = len(variables)

    output = ""

    visible_variables = [variable for variable in variables if variable not in merged_variables]
    lst_visible_variables = [[variable] for variable in variables if variable not in merged_variables]


    lst = lst_visible_variables + list_of_merged_components
    print(list_of_merged_components)

    output += "# Install z3 for python as explained here\n"
    output += "# https://github.com/Z3Prover/z3\n"
    output += "from z3 import *\n"
    output += "\n"
    output += "# The solver\n"
    output += "solver = Solver()\n"
    output += "\n"

    #here we declare the variables of the original BN
    for i in range(len(variables)):
        output += variables[i]
        if i<len(variables)-1: output+=','

    output +=" = Bools('"
    for i in range(len(variables)):
        output += variables[i]
        if i<len(variables)-1: output +=' '
    output += "')"
    output += "\n"

    #here we declare the functions of the original BN
    lst_F = []
    for i in range(len(variables)):
        output += 'f' + variables[i]
        lst_F.append('f' + variables[i])
        if i<len(variables)-1: output+=','
    #print(lst_F)

    output +=" = Bools('"
    for i in range(len(variables)):
        output += 'f' + variables[i]
        if i<len(variables)-1: output +=' '
    output += "')"
    output += "\n"

    output += '\n'
    output += '\n'
    output += '\n'

    #here we DEFINE the functions of the original BN
    for i in range(len(variables)):
        output += 'f' + variables[i] + '=' + functions[i]
        output += '\n'

    output += "\n"
    output += "\n"

    #here we define the variables of the reduced BN
    lst_y = []
    for i in range(len(visible_variables)+len(list_of_merged_components)):
        output += 'y' + str(i)
        lst_y.append('y' + str(i))
        if i<len(variables)-1: output+=','

    output +=" = Bools('"
    for i in range(len(visible_variables)+len(list_of_merged_components)):
        output += 'y' + str(i)
        if i<m-1: output +=' '
    output += "')"
    output += "\n"
    #print('the variables of the reduced BN are',lst_y)
    output += "\n"
    output += "\n"

    dictionary = dict(zip(lst_y, lst))

    #here we define the aggregation functions
    visible=int(len(visible_variables))
    lst_G=[]
    for i in range(len(visible_variables)+len(list_of_merged_components)):
        if i<visible:
            output += 'g' + str(i) +'='+visible_variables[i]
            output += '\n'
            lst_G.append('g' + str(i))
        else:
            output += 'g' + str(i) +'='+aggregation_functions[i-visible]
            output += '\n'
            lst_G.append('g' + str(i))
    output += '\n'
    output += '\n'

    dictionary
    new_dict={}
    for key in dictionary:
        for z in dictionary[key]:
            new_dict[z]=key
    print(new_dict)

    #here we define the G(F); the aggregation of the functions (= the aggregated values at the next time step)
    lst_GF=[]
    visible=int(len(visible_variables))
    for i in range(len(visible_variables)+len(list_of_merged_components)):
        lst_GF.append('g' + str(i) + 'f')
        output += 'g' + str(i) + 'f' +'='+'substitute(' + 'g' + str(i) + ','+'*'+'['
        #output += '\n'
        for i in range(len(variables)):
            output +='('+variables[i]+','+lst_F[i]+')'+' '#+','
            if i<len(variables)-1: output +=','
            #output += '\n'



        output += ']'
        output += ')'
        output += '\n'
    output += '\n'
    output += '\n'

    #here we define the hatF; the abstract update functions of the Definition "Reduced BN"
    lst_hatF=[]
    for i in range(len(visible_variables)+len(list_of_merged_components)):
        output += 'hatfx' + str(i) +'='+'substitute(' + 'g' + str(i)+ 'f' + ','+'*'+'['
        lst_hatF.append('hatfx' + str(i)) 
        for i in range(len(variables)):
            if variables[i] in X_plus:
                output +='('+variables[i]+','+new_dict[variables[i]]+')'+' '+','
            else:
                output +='('+variables[i]+','+"Not("+new_dict[variables[i]]+')'+')'+' '+','
        output += ']'
        output += ')'
        output += '\n'
    output += '\n'
    output += '\n'
    output += '\n'
    output += 's=Solver()'
    output += '\n'
    output += '\n'

    #The lumping criterion
    output += 's.add(Not('
    output += '\n'
    output += 'Implies('

    output += 'And('
    for i in range(m):
        output += lst_y[i] +'=='+lst_G[i]
        if i<m-1: output +=','
    output += ')'
    output += '\n'
    output +=','
    output += '\n'
    output += 'And('
    for i in range(m):
        output += lst_GF[i] +'=='+lst_hatF[i]
        if i<m-1: output +=','

    output += ')'
    output += '\n'
    output += ')'
    output += '\n'
    output += ')'
    output += '\n'
    output += ')'
    output += '\n'

    output += 'print(s.check())'
    output += '\n'
    return output
