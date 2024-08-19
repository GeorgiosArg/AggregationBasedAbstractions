def pretty_printing(variables,m):
    dict_original={}
    dict_abstract={}
    dict_aggregations={}
    for j in range(len(m)):
        key = str(m[j])
        value = str(m[m[j]]).strip()
        value = value.replace('[','').replace(']','').replace('\n','').replace(' ','')
        for i in range(len(variables)):
            v = 'Var('+str(i)+')'
            if key[0] == 'f':
                value = value.replace(v,variables[i]).replace('else->','')
                dict_original[key] = value
            elif key[0] == 'g':
                value = value.replace(v,variables[i]).replace('else->','')
                dict_aggregations[key] = value
            elif key[0] == 'h':
                dict_abstract[key] = value
    return dict_original, dict_abstract, dict_aggregations
