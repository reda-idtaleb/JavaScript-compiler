from utils.delimiters import *
from . import expression as e

# --- VariableDeclaration ---
def var_declarator(varDec):
    """
        a Variable declarator is an Identifier(Expression) + Expression | None
    """
    if varDec['type'] == 'Identifier':
        return varDec['name']   
    id = var_declarator(varDec["id"])
    return id if (not varDec['init']) else (id + assignDelimiter + e.abstract_expression(varDec["init"]))

def variable_declaration(node):
    e = node["kind"] + " "
    d = node['declarations'] # liste de VariableDeclarator
    e += commaDelimiter.join([var_declarator(var) for var in d])
    return e 
# --- End of VariableDeclaration ---

# --- FunctionDeclaration ---
def function_params(params):
    res = commaDelimiter.join([e.abstract_expression(arg) for arg in params]) 
    return parentOpDelimiter + res + parentClDelimiter
    
def function_body(body, level) :
    from . import statement as s
    return s.abstract_statement(body, level)
     
def function_declaration(node, level):
    res = node['id']['name']
    res += function_params(node['params'])
    res += blockOpDelimiter + bTab(level+2) + function_body(node['body'], level) + tab(level) + blockClDelimiter
    return tab(level-2) + 'function ' + res
# --- End of FunctionDeclaration ---

# --- Abstract method ---
def abstract_declaration(node, level=0):
    if node['type'] == 'VariableDeclaration':
        return variable_declaration(node) + delimiter 
    elif node['type'] == 'FunctionDeclaration':
        return function_declaration(node, level) + delimiter
