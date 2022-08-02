from utils.delimiters import *
from . import intExpression as e


# Environement pour associer à chaque variable sa valeur actuelle 
globalVariables = {}

localVariables = {}

paramsValues = {}

functions = {}

# --- VariableDeclaration ---
def var_declarator(varDec):
    """les expressions arithmétiques (donc définir une façon de représenter les valeurs numériques),
les déclarations de variables (globales) : cela nécessite de mettre en place un environnement pour associer à chaque variable sa valeur actuelle en utilisant un dictionnaire,

        a Variable declarator is an Identifier(Expression) + Expression | None
        :return: (tuple) return the identifier and it's value  
    """
    id = e.abstract_expression(varDec["id"])
    init = None if varDec["init"] is None else e.abstract_expression(varDec["init"])
    return (id, init)

def variable_declaration(node):
    d = node['declarations'] # liste de VariableDeclarator
    res = ''
    for varDec in d:
        varID, varInit = var_declarator(varDec)
        if (e.functions_calls != []):
            localVariables[varID] = varInit
        else:
            globalVariables[varID] = varInit 
        res += 'VariableDeclaration: '+ varID + tab(1) + str(getIdentifierValue(varID)) +br

    return  res
# --- End of VariableDeclaration ---

# --- FunctionDeclaration ---
     
def function_declaration(node):
    funcName = node['id']['name']
    functions[funcName] = node
    res = "FunctionDeclaration: " + funcName 
    res += function_params(node['params']) + bTab(1)
    return res

def function_params(params):
    res = commaDelimiter.join([e.abstract_expression(arg) for arg in params]) 
    return parentOpDelimiter + res + parentClDelimiter



# --- End of FunctionDeclaration ---


# --- Identifier Value
def getIdentifierValue(name):
    if name in paramsValues.keys():
        return paramsValues[name]
    if name in localVariables.keys():
        return localVariables[name]
    elif name in globalVariables.keys():
        return globalVariables[name]
    else :
        raise NameError ("Undefined variable")

# --- Abstract method ---
def abstract_declaration(node, level=0):
    if node['type'] == 'VariableDeclaration':
        return variable_declaration(node) 
    elif node['type'] == 'FunctionDeclaration':
        return function_declaration(node) 

