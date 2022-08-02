from utils.delimiters import *
from utils.absTypes import absLiteral
from . import literal as l

# --- BinaryExpression & LogicalExpression ---
def binary_and_logical_expression(exp):
    """
        A Binary and Logical Expression is an Expression + Operator + Expression
    """
    res =  parentOpDelimiter + abstract_expression(exp['left']) + parentClDelimiter
    res += exp['operator']
    res += parentOpDelimiter + abstract_expression(exp['right']) + parentClDelimiter
    return res
# --- End of BinaryExpression & LogicalExpression ---

# --- CallExpression ---
def call_expression(exp):
    """
        A CallExpression is a call: (Expression | super | import) + args: [Expression]
    """
    res =  abstract_expression(exp["callee"]) + parentOpDelimiter
    res += commaDelimiter.join([abstract_expression(arg) for arg in exp['arguments']]) + parentClDelimiter
    return res 
# --- End of CallExpression ---

# --- UpdateExpression & UnaryExpression ---
def update_and_unary_expression(exp):
    """
        an Update & Unary Expression is an Operator(as prefix if true) + arg: Expression
    """
    e = abstract_expression(exp['argument']) 
    op = exp['operator']
    res = (op + e) if exp['prefix'] else (e + op)
    return parentOpDelimiter + res + parentClDelimiter
# --- End of UpdateExpression & UnaryExpression ---

# --- AssignmentExpression ---
def assignment_expression(exp):
    """
        an AssignmentExpression is an Expression + Operator + Expression
    """
    return abstract_expression(exp['left']) + exp['operator'] + abstract_expression(exp['right'])
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

def object_property(propNode):
    return abstract_expression(propNode['key']) + colonDelimiter + abstract_expression(propNode['value'])

def object_method(propNode):
    """
    @unimplementedMethod
    :param propNode: a property Node
    :return: (str) return an empty string
    """
    return tab(0)

def spread_element(prop):
    return spreadDelimiter + abstract_expression(prop['argument'])

def object_member(prop):
    property, method = 'Property', 'Method'
    if property in prop['type']:
        return object_property(prop)
    elif method in prop['type']:
        return object_method(prop)
    elif prop['type'] == 'SpreadElement':
        return spread_element(prop)

def object_expression(properties):
    """
        An ObjectExpression is a [ObjectProperty | ObjectMethod | SpreadElement]
    """
    res = commaDelimiter.join([object_member(prop) for prop in properties])
    return blockOpDelimiter + res + blockClDelimiter
# --- End of ObjectExpression ---

# --- ThisExpression ---
def this_super_expression(expType):
    return 'super' if expType == 'Super' else 'this'
# --- End of ThisExpression ---

# --- NewExpression ---
def new_expression(exp):
    """
        a NewExpression is a specified CallExpression
    """
    return 'new ' + call_expression(exp)
# --- End of NewExpression ---

# --- Abstract method ---
def abstract_expression(exp):
    if absLiteral in exp['type']:
        return l.abstract_literal(exp)
    elif exp['type'] == 'Identifier':
        return exp['name']
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
    elif (exp['type'] == 'ThisExpression') or (exp['type'] == 'Super'):
        return this_super_expression(exp['type'])
    elif exp['type'] == 'NewExpression':
        return new_expression(exp)