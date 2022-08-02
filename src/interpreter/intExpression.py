from utils.delimiters import *
from . import intDeclaration as d
from . import intStatement as s

from utils.absTypes import absLiteral
from . import intLiteral as l

functions_calls = []

# --- BinaryExpression & LogicalExpression ---
def binary_and_logical_expression(exp):
    """
        A Binary and Logical Expression is an Expression + Operator + Expression
    """
    if exp['left']['type'] == 'Identifier' :
        a = d.getIdentifierValue(exp['left']['name'])
    else :
        a = abstract_expression(exp['left'])

    if exp['right']['type'] == 'Identifier' :
        b = d.getIdentifierValue(exp['right']['name'])
    else :
        b = abstract_expression(exp['right'])
    if exp['operator'] == '+':
        return a + b
    elif exp['operator'] == '-':
        return a - b
    elif exp['operator'] == '*':
        return a * b
    elif exp['operator'] == '/':
        return a / b
    elif exp['operator'] == '%':
        return a % b
    elif exp['operator'] == '**':
        return a ** b
    elif exp['operator'] == '&':
        return a & b
    elif exp['operator'] == '|':
        return a | b
    elif exp['operator'] == '&&':
        return a and b
    elif exp['operator'] == '||':
        return a or b
    elif exp['operator'] == '==':
        return a == b
    elif exp['operator'] == '!=':
        return a != b
    elif exp['operator'] == '<':
        return a < b
    elif exp['operator'] == '>':
        return a > b
    elif exp['operator'] == '<=':
        return a <= b
    elif exp['operator'] == '>=':
        return a >= b

# --- End of BinaryExpression & LogicalExpression ---

# --- CallExpression ---
def call_expression(exp):
    """
        A CallExpression is a call: (Expression | super | import) + args: [Expression]
    """

    func_name = abstract_expression(exp["callee"])
    func_args = exp['arguments']

    res = "CallExpression: "
    if func_name == "print":
        res += "Print: "
        for arg in func_args:
            if arg["type"] == 'Identifier':
                res += str(d.globalVariables[arg["name"]])
            else:
                res += str(abstract_expression(arg))
        return res
    else :
        if (func_name in d.functions):
            node = d.functions[func_name]
            fill_params_Values(node["params"], func_args)
            if (functions_calls == [] or not is_finished(func_name)):
                function_call = {func_name: {'return' : None, 'isFinished' : False}}
                functions_calls.append(function_call)               
                res += func_name + " " + bTab(2) + s.abstract_statement(node["body"])     
                last_pushed = functions_calls[-1]
            elif is_finished(func_name):
                last_pushed = functions_calls[-1]
            return get_func_return(func_name, last_pushed)
        else :
            return "Undefined function: "+func_name

def fill_params_Values(params, args):
    i = 0
    for p in params :
        if p["type"] == "Identifier":
            pName = abstract_expression(p)
            if (args[i]["type"] == "Identifier"):
                d.paramsValues[pName] = d.getIdentifierValue(args[i])
            else :
                d.paramsValues[pName] = abstract_expression(args[i])
        i = i+1

def get_func_return(func_name: str, function: dict):
    return function[func_name]['return']

def set_func_return(func_name: str, function: dict, value):
    function[-1][func_name]['return'] = value
    
def is_finished(func_name: str):
    return functions_calls[-1][func_name]['isFinished']

def set_is_finished(func_name: str, value: bool):
    functions_calls[-1][func_name]['isFinished'] = value   
# --- End of CallExpression ---

# --- UpdateExpression & UnaryExpression ---
def update_and_unary_expression(exp):
    """
        an Update & Unary Expression is an Operator(as prefix if true) + arg: Expression
    """
    e = abstract_expression(exp['argument']) 
    if exp['argument']['type'] == 'Identifier':
        id = e
        e = d.getIdentifierValue(e)

    if exp['operator'] == '!':
        if e:
            not e
        else : e = True
    elif exp['operator'] == '-':
        e = - e
    elif exp['operator'] == '+':
        e = + e
    elif exp['operator'] == '++':
        e = e + 1
    elif exp['operator'] == '--':
        e = e - 1

    if exp['argument']['type'] == 'Identifier':
        d.globalVariables[id] = e

    return e
           
# --- End of UpdateExpression & UnaryExpression ---

# --- AssignmentExpression ---
def assignment_expression(exp):
    """
        an AssignmentExpression is an Expression + Operator + Expression
    """   
    id = abstract_expression(exp['left'])
    right = abstract_expression(exp['right'])
    rightVal = d.getIdentifierValue(right) if exp['right']['type'] == 'Identifier' else right
    leftVal = d.getIdentifierValue(id)

    res = 'AssignmentExpression: ' + id + tab(1)
    if exp['operator'] == '=':
        d.globalVariables[id] = rightVal 
        return res + str(rightVal)
        
    elif exp['operator'] == '+=':
        d.globalVariables[id] = leftVal + rightVal
        return res + str(leftVal + rightVal)
    elif exp['operator'] == '-=':
        d.globalVariables[id] = leftVal - rightVal
        return res + str(leftVal - rightVal)
    elif exp['operator'] == '*=':
        d.globalVariables[id] = leftVal * rightVal
        return res + str(leftVal * rightVal)
    elif exp['operator'] == '/=':
        d.globalVariables[id] = leftVal / rightVal
        return res + str(leftVal / rightVal)


# --- End of AssignmentExpression ---

# --- MemberExpression ---
def member_object(objNode):
    return abstract_expression(objNode)

def member_property(propNode):
    return abstract_expression(propNode)

def member_computed(obj, prop, compNode):
    return (obj + bracketOpDel + prop + bracketClDel) if compNode else (obj + memberDelimiter + prop)
    
def member_expression(exp):
    obj =  member_object(exp['object'])
    prop = member_property(exp['property'])
    return member_computed(obj, prop, exp['computed']) 
# --- End of MemberExpression ---

# --- ObjectExpression ---
objects_properties = {}

def object_property(propNode):
    key = abstract_expression(propNode['key'])
    value = abstract_expression(propNode['value'])
    objects_properties[key] = value
    
def object_expression(properties):
    """
        An ObjectExpression is a [ObjectProperty | ObjectMethod | SpreadElement]
    """
    [object_property(prop) for prop in properties] 
    return objects_properties
# --- End of ObjectExpression ---

# --- Abstract method ---
def abstract_expression(exp):
    if absLiteral in exp['type']:
        return l.abstract_literal(exp)
    elif exp['type'] == 'Identifier':
        return exp["name"]
    elif exp['type'] == 'BinaryExpression':
        return binary_and_logical_expression(exp)
    elif (exp['type'] == 'UnaryExpression') or (exp['type'] == 'UpdateExpression'):
        return update_and_unary_expression(exp)
    elif exp['type'] == 'CallExpression':
        return call_expression(exp)
    elif exp['type'] == 'AssignmentExpression':
        return assignment_expression(exp)
    elif exp['type'] == 'MemberExpression':
        return member_expression(exp) 
    elif exp['type'] == 'LogicalExpression':
        return binary_and_logical_expression(exp)
    elif exp['type'] == 'ObjectExpression':
        return object_expression(exp['properties'])
