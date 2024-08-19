def ComputeReducedBN(variables,functions,aggregation_functions):
    
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

    visible_variables = [variable for variable in variables if variable not in merged_variables]
    lst_visible_variables = [[variable] for variable in variables if variable not in merged_variables]


    lst = list_of_merged_components + lst_visible_variables

    BN_dictionary = dict(zip(variables, functions))
    #here we define the hatF; the abstract update functions of the Definition "Reduced BN"
    visible=int(len(visible_variables))
    lst_hatF=[]
    for i in range(len(list_of_merged_components)):
        lst_hatF.append('hatfx' + str(i))
    for variable in visible_variables:
        lst_hatF.append('hatf_' + variable)

    lst_hatX=[]
    for i in range(len(list_of_merged_components)):
        lst_hatX.append('hatx' + str(i))
    for variable in visible_variables:
        lst_hatX.append('hatx_' + variable)

    dictionary_1 = dict(zip(lst_hatF, aggregation_functions+visible_variables))
    dictionary_2 = dict(zip(lst_hatX, list_of_merged_components+lst_visible_variables))
    dictionary_3 = dict(zip(lst_hatF, list_of_merged_components+lst_visible_variables))
    dictionary_4 = dict(zip(lst_hatF, lst_hatX))

    new_dict={}
    for key in dictionary_2:
        for z in dictionary_2[key]:
            new_dict[z]=key
    #print(new_dict)

    Red_BN_dictionary={}
    for hatf in lst_hatF:
        Red_BN_dictionary[hatf] = dictionary_1[hatf]
        for variable in dictionary_3[hatf]:
            Red_BN_dictionary[hatf]=Red_BN_dictionary[hatf].replace(variable,BN_dictionary[variable])
    for key in Red_BN_dictionary:
        #print(key)
        for variable in variables:
            #print(variable)
            if variable in X_plus:
                Red_BN_dictionary[key] = Red_BN_dictionary[key].replace(variable,new_dict[variable])
            else:
                Red_BN_dictionary[key] = Red_BN_dictionary[key].replace(variable,'Not('+new_dict[variable]+')')
    return Red_BN_dictionary