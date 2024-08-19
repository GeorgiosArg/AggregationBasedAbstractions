def synthesis(variables,functions, merged_variables):
    # Size of abstracted BN = M
	
    output = ""
    # Size of abstracted BN = M
    M = len(variables)-len(merged_variables)+1
    
    visible_variables = [variable for variable in variables if variable not in merged_variables]

    output += "# Install z3 for python as explained here\n"
    output += "# https://github.com/Z3Prover/z3\n"
    output += "from z3 import *\n"
    output += "\n"

    output += "# The solver\n"
    output += "solver = Solver()\n"
    output += "\n"

    output += "# Original BN update function F = f0..fn-1\n"
    for variable in variables:
        output += "f" + variable + " = Function('f" + variable + "', "
        for j in range(len(variables)):
            output += "BoolSort(),"
        output += "BoolSort())\n"
    output += "\n"

    output += "# Some Boolean variables for original BN\n"
    for variable in variables:
        output += variable + " = Const( '" + variable + "' , BoolSort())"
        output += "\n"
    output += "\n"
    
    output += "# Abstraction function G = g0..gn-1\n"
    for variable in visible_variables:
        output += "g" + variable + " = Function('g" + variable + "', "
        for j in range(len(variables)):
            output+="BoolSort()"
            if j<(len(variables)-1): output+=","
        output += ",BoolSort())\n"
    output += "\n"
    
    output += "g" + " = Function('g', "
    for j in range(len(variables)):
        output+="BoolSort(),"
    output += "BoolSort())\n"
    output += "\n"
    output += "\n"
    output += "# Abstract BN update function H = h1..hn-1\n"
    for i in range(M-1):
        output += "h" + str(i) + " = Function('h" + str(i) + "', "
        for j in range(M):
            output += "BoolSort(),"
        output += "BoolSort())\n"
    output += "h"+ "= Function('h',"
    for j in range(M):
        output += "BoolSort(),"
    output += "BoolSort())\n"
    output += "\n"
    
    output += "# Some Boolean variables\n"
    for i in range(M):
        output += "y" + str(i) + " = Const('y" + str(i) + "' , BoolSort())"
        output += "\n"
    output += "\n"
    
    output += "# Constraints (partially) defining F, G and H\n"
    output += "solver.add(\n"
    output+="\t# Vacuous constraints for f to serve as placehoders\n"
    output+="\t# Replace rhs with actual constraints\n"
    
    for i in range(len(variables)):
        output += "\tForAll(["
        for j in range(len(variables)):
            output+=variables[j]
            if j<(len(variables)-1): output+=","
        output+="],f" + variables[i] + "("
        for j in range(len(variables)):
            output+=variables[j]
            if j<(len(variables)-1): output+=","
        output+=") ==" 
        output+=functions[i]
        output+="),\n"
        
        
    output+="\t# Vacuous constraints for g to serve as placehoders\n"
    output+="\t# Replace rhs with actual constraints\n"
    
    for variable in visible_variables:
        output += "\tForAll(["
        for j in range(len(variables)):
            output+=variables[j]
            if j<(len(variables)-1): output+=","
        output+="],g" + variable + '('
        for j in range(len(variables)):
            output+=variables[j]
            if j<(len(variables)-1): output+=","
        output +=')' +'=='+variable+')'
        output += ","
        output += "\n"
    output += "\n"
    output += "\n"
    
    
    
    output+= "\tForAll(["
    for j in range(len(variables)):
        output+=variables[j]
        if j<(len(variables)-1): output+=","
    output += '],'
    output +='g('
    for j in range(len(variables)):
        output+=variables[j]
        if j<(len(variables)-1): output+=","
    output +=')==g('
    for j in range(len(variables)):
        output+=variables[j]
        if j<(len(variables)-1): output+=","
    output += ")"
    output += ")"
    output += ","
    
    output += "\n"
    output += "\n"
    output+="\t# Vacuous constraints for h to serve as placehoders\n"
    output+="\t# Replace rhs with actual constraints\n"
    for i in range(M-1):
        output += "\tForAll(["
        for j in range(M):
            output+="y" + str(j)
            if j<(M-1): output+=","
        output+="],h" + str(i) + "("
        for j in range(M):
            output+="y" + str(j)
            if j<(M-1): output+=","
        output+=") == h" + str(i) + "("
        for j in range(M):
            output+="y" + str(j)
            if j<(M-1): output+=","
        output+=")),\n"
        
    
    output += "\n"
    output += "\n"
    
    
    
    output+= "\tForAll(["
    for j in range(M):
        output+="y" + str(j)
        if j<(M-1): output+=","
    output+="],h" + "("
    for j in range(M):
        output+="y" + str(j)
        if j<(M-1): output+=","
    output+=") == h" + "("
    for j in range(M):
        output+="y" + str(j)
        if j<(M-1): output+=","
    output+=")),\n"
    
    output += "\n"
    output += "\n"
    output += "\n"
    output += "\n"
    
    output+="\t#Determinism condition (i.e. existence of abstract bisimilar deterministic/synchronous BN)\n"
    output += "\tForAll(["
    for i in range(len(variables)):
            output+=variables[i]
            if i<(len(variables)-1): output+=","
    output += "]"
    output += ", And(\n"
    for k in range(len(visible_variables)):
        output += "\tg" + visible_variables[k] + "("
        for l in range(len(variables)):
            output += "f" + variables[l] + "("
            for j in range(len(variables)):
                output+=variables[j]
                if j<(len(variables)-1): output+=","
                else: output+=")"
            if l<(len(variables)-1): output+=","
        output+=")"
        output += " == h" + str(k) + "("
        output += 'g'+'('
        for z in range(len(variables)):
            output += variables[z]
            if z<(len(variables)-1): output+=","
        output += ")"
        output += ","
        for l in range(len(visible_variables)):
            output += "g" + visible_variables[l] + "("
            for j in range(len(variables)):
                output+=variables[j]
                if j<(len(variables)-1): output+=","
                else: output+=")"
            if l<(len(visible_variables)-1): output+=","
        output += ")"
        if k<(M-1): output += ",\n"
    
    output+= "\n#the aggregation function"
    output+= "\n"
    output += '\tg('
    for k in range(len(variables)):
        output += 'f'+variables[k]+'('
        for j in range(len(variables)):
            output += variables[j]
            if j<(len(variables)-1): output+=","
        output +=')'
        if k<(len(variables)-1): output+=","
    output+=')'
    output+='=='
    output+='h'+ "("
    output += 'g'+'('
    for z in range(len(variables)):
        output += variables[z]
        if z<(len(variables)-1): output+=","
    output += ")"
    output += ","
    for l in range(len(visible_variables)):
        output += "g" + visible_variables[l] + "("
        for j in range(len(variables)):
            output += variables[j]
            if j<(len(variables)-1): output+=","
        output += ")"
        if l<(len(visible_variables)-1): output+=","
    output += ")"
    output+='\n'
    output += ")\n\n"
    

    output += "\n\t))\n"
    
    output += "#If loop providing solutions\n"
    output += "if solver.check() == sat:\n"
    output += "\tm = solver.model()\n"
    output += "\tprint(\"Hoorray! Here is a possible solution:\")\n"
    output += "\tprint(m)\n"
    output += "else:\n"
    output += "\tprint(\"No solution, sorry!\")\n"

    return output

    
    
