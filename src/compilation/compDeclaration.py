from utils.assemblyFunctions import *
from utils.delimiters import *
from utils.registers import *
from . import compExpression as e
from . import compStatement as s

# --- VariableDeclaration ---
def variable_declaration(node):
    global indexGlobalVar
    global indexLocalVar
    declarations = node['declarations'] # liste de VariableDeclarator
    res = ""
    for varDec in declarations:
        varID = varDec['id']['name']
        # si la variable n'est pas initialisé alors sa valeur est 0(NULL), sinon on l'explore. Enfin, on push sur la pile le résultat
        res += convertASMStmt("push", convertASMExpression("aconst", 0)) if not varDec["init"] else e.abstract_expression(varDec["init"]) 
        # si on est dans le cadre d'une var locale
        if func_stack != []:
            # on enregistre la variable et son indice ebp dans le dict localVariables
            localVariables[varID] = fromLocalsGetValue(indexLocalVar)
            # on décrémente dans la pile: bp[-1] -> 1ère var local; bp[-2] -> 2ème var local
            indexLocalVar -= 1
        else:
            # on dépile dans r1 le valeur de l'init d'une variable
            res += convertASMStmt("pop", r1)
            # la valeur contenu dans r1 est associée à la variable globale(identifiée par son indice).
            res += addToGlobals(indexGlobalVar, r1)
            # on enreigtre cette variable(avec sa valeur) dans le dict de variable globale
            globalVariables[varID] = fromGlobalsGetValue(indexGlobalVar)
            # on incrémente le nombre de variable globale -> indice de la proc
            # aine var globale dans globals[]
            indexGlobalVar += 1
    return  res
# --- End of VariableDeclaration ---

# --- FunctionDeclaration ---
def function_params(params):
    global indexParamVar
    func_params = {}
    for param in params:
        func_params[param["name"]] = bp(indexParamVar)
        indexParamVar += 1
    return func_params

def function_declaration(node):
    global func_stack
    func_name = e.abstract_expression(node['id'])
    # stocker les paramètres de la fonction: leurs noms(clé) -> leurs indices dans epb(valeur)
    params = function_params(node['params'])
    # on crée le label de la fonction avec son nom
    func_label = createLabel("funct_" + func_name)
    # on essaye d'ignorer la fonction et d'aller à son invocation
    end_func = createLabel("functend_" + func_name)
    res = goto(end_func)
    # on déclare le label de la fonction
    res += labelDeclaration(func_label) 
    # on ajoute à la pile des fonctions le nom de la fonction, ses param, ses var locales
    addToFunctionStack(func_name, params, localVariables) 
    # on explore le body
    body = s.abstract_statement(node['body'])
    res += body
    # on déclare la fin de la fonction
    res += labelDeclaration(end_func)
    return res

# --- End of FunctionDeclaration ---

# --- Identifier Value ---
def getIdentifierValue(name, level=-1):
    global variable_val
    # si la stack des fonctions n'est pas vide et que le nom n'est pas une variable global 
    #  -> donc c'est une variable locale ou un parametre
    if func_stack != [] and not name in globalVariables.keys():
        func_name = get_declared_funcs_name(func_stack)[level]
        last = func_stack[level]
        if name in last[func_name]["localVar"].keys():
            variable_val = last[func_name]["localVar"][name]
            return convertASMStmt("push", last[func_name]["localVar"][name]) 
        elif name in last[func_name]["params"].keys():
            variable_val = last[func_name]["params"][name]
            return convertASMStmt("push", last[func_name]["params"][name])
        elif name not in get_declared_funcs_name(func_stack) and name in get_saved_functions().keys():
            return convertASMStmt("push", declared_functions[name]['rbp'])
        else:
            # optimisation -> recherche des variables locales dans les fonctions imbriquées
            # Si on ne trouve pas une variable local alors on remonte dans la stack en augmentant le level
            if abs(level) < len(func_stack):
                level -= 1
                return getIdentifierValue(name, level)
            else:
                return name
    elif name in globalVariables.keys():
        variable_val = globalVariables[name]
        return convertASMStmt("push", globalVariables[name])
    else:
        return name

def abstract_declaration(node):
    if node['type'] == 'VariableDeclaration':
        return variable_declaration(node) 
    elif node['type'] == "FunctionDeclaration":
        return function_declaration(node)
