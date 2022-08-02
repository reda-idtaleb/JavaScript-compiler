from utils.delimiters import *
from utils.absTypes import absLiteral
from utils.registers import *
from utils.assemblyFunctions import *
from . import compLiteral as l
from . import compDeclaration as d

# --- Identifier --- 
def identifier_expression(exp):
    # on récupère la valeur de l'indentifiant s'il est présent, sinon on renvoie son nom
    return d.getIdentifierValue(exp['name'])
# --- End of Identifier ---

# --- BinaryExpression & LogicalExpression ---
def binary_and_logical_expression(exp):
    """
        A Binary and Logical Expression is an Expression + Operator + Expression
    """
    # on empile gauche et droite
    # si gauche ou/et droite est un Identifier donc on récupère sa valeur dans globalVariables
    # Sinon, on explore l'expression
    res  = abstract_expression(exp['left']) 
    res += abstract_expression(exp['right'])
    # on dépile les valeurs dans les deux registres r1/r2
    res += convertASMStmt("pop", r1) 
    res += convertASMStmt("pop", r2) 
    # on effectue l'opération entre les valeurs des 2 registres, on stocke le resultat dans r1
    if exp['operator'] == '+':
        res += convertASMStmt("iadd", r1, r2, r1) 
    elif exp['operator'] == '-':
        res += convertASMStmt("isub", r1, r2, r1) 
    elif exp['operator'] == '*':
        res += convertASMStmt("imul", r1, r2, r1) 
    elif exp['operator'] == '/':
        res += convertASMStmt("idiv", r1, r2, r1) 
    elif exp['operator'] == '%':
        res += convertASMStmt("imod", r1, r2, r1) 
    elif exp['operator'] == '<':
        res += convertASMStmt("ilt", r1, r2, r1) 
    elif exp['operator'] == '<=':
        res += convertASMStmt("ile", r1, r2, r1) 
    elif exp['operator'] == '==':
        res += convertASMStmt("ieq", r1, r2, r1)
    elif exp['operator'] == '!=':
        res += convertASMStmt("ieq", r1, r2, r1)
        res += convertASMStmt("push", r1)
        res += convertASMStmt("pop", r2)
        res += convertASMStmt("lneg", r1, r2)
    elif exp['operator'] == '>':
        res += convertASMStmt("ilt", r1, r1, r2) 
    elif exp['operator'] == '>=':
        res += convertASMStmt("ile", r1, r1, r2) 
    elif exp['operator'] == "||":
        res += convertASMStmt("lor", r1, r1, r2)
    # on empile le resulat contenu dans r1
    res += convertASMStmt("push", r1) + bTab(4)
    return res 
# --- End of BinaryExpression & LogicalExpression ---

# --- UpdateExpression & UnaryExpression ---
def update_and_unary_expression(exp):
    """
        an Update & Unary Expression is an Operator(as prefix if true) + arg: Expression
    """
    # on explore l'argument
    res = abstract_expression(exp['argument'])      
    if exp['operator'] == '!':
        # on pop le sommet de la pile qui contient une valeur, puis on effecture la négation et on push le resultat
        res += convertASMStmt("pop", r2)
        res += convertASMStmt("lneg", r1, r2)
        res += convertASMStmt("push", r1)
    elif exp['operator'] == '-':
        res += convertASMStmt("push", convertASMExpression("uconst", -1))
        res += convertASMStmt("pop", r1)
        res += convertASMStmt("pop", r2) 
        res += convertASMStmt("mul", r1, r2, r1)
        res += convertASMStmt("push", r1)
    elif exp['operator'] == '+':
        res += convertASMStmt("push", convertASMExpression("uconst", 1))
        res += convertASMStmt("pop", r1)
        res += convertASMStmt("pop", r2) 
        res += convertASMStmt("mul", r1, r2, r1)
        res += convertASMStmt("push", r1)
    elif exp['operator'] == '++':
        # on suppose que les opérateur ++ et -- s'effectue comme += et -= du C
        # On considère aussi que ces opérations sont procédées par des identifieurs reférant aux variables globales.  
        res += asmUpdateVariable(d.variable_val, word_t_i, "+=", 1)
    elif exp['operator'] == '--':
        res += asmUpdateVariable(d.variable_val, word_t_i, "-=", 1)
    return res
# --- End of UpdateExpression & UnaryExpression ---

# --- CallExpression ---
print_counter = 0
def printCall(func_label):
    res = labelDeclaration(func_label)
    res += convertASMStmt("debug_reg", bp(3))
    return res
    
def call_expression(exp):
    """
        A CallExpression is a call: (Expression | super | import) + args: [Expression]
    """
    global print_counter
    res = ""
    args = exp['arguments']
    # on récupère l'identifiant de la fonction à laquelle on fait appel
    call_name = abstract_expression(exp['callee'])
    res += tab(0).join([abstract_expression(args[i]) for i in range(len(args)-1, -1, -1)]) # parcours des arguments dans le sens inverse
    func_label = createLabel("funct_" + call_name) if call_name != 'print' else createLabel("funct_" + call_name, print_counter)
    res += convertASMStmt("call", func_label)
    if call_name == "print":
        res += printCall(func_label)
        print_counter += 1
    else:
        # on est forcément dans le cas d'une fonction qui a retourné qlq et donc on récupère le résultat dans r1
        res += convertASMStmt("pop", r1)
    # on supprime les arguments de la pile
    res += convertASMStmt("drop", len(args))
    res += convertASMStmt("push", r1)
    return res 
# --- End of CallExpression ---

# --- AssignmentExpression ---
def assignment_expression(exp):
    """
        an AssignmentExpression is an Expression + Operator + Expression
    """
    res = abstract_expression(exp['right']) # on evalue d'abord la partie de droite
    res += convertASMStmt('pop', r1) # on dépile le résultat dans r1
    res += abstract_expression(exp['left']) # on évalue la partie gauche(identifier)
    res += asmUpdateVariable(d.variable_val, word_t_i, exp['operator'], getWordtField(r1, word_t_i))
    return res
# --- End of AssignmentExpression ---

# --- Abstract method ---
def abstract_expression(exp):
    if absLiteral in exp['type']:
        return convertASMStmt("push", l.abstract_literal(exp)) 
    elif exp['type'] == 'Identifier':
        return identifier_expression(exp)
    elif exp['type'] == 'BinaryExpression' or exp['type'] == 'LogicalExpression':
        return binary_and_logical_expression(exp)
    elif (exp['type'] == 'UpdateExpression') or (exp['type'] == 'UnaryExpression') :
        return update_and_unary_expression(exp)
    elif exp['type'] == 'CallExpression':
        return call_expression(exp)
    elif exp['type'] == 'AssignmentExpression':
        return assignment_expression(exp)
    
