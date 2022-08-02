from utils.delimiters import *
from utils.absTypes import *
from . import intExpression as e
from . import intDeclaration as d

# --- ExpressionStatement ---
def expression_statement(expStmt):
    """
        ExpressionStatement it's an expression
    """
    return  "ExpressionStatement: " + str(e.abstract_expression(expStmt))
# --- End of ExpressionStatement ---

# --- BlockStatement ---
def block_statement(bodyNode):
    """
        The BlockStatement it's a list of statement
    """
    return  bTab(1).join([abstract_statement(block) for block in bodyNode])
# --- End of BlockStatement ---

# --- WhileStatement ---
def while_test(testNode):
    """
        WhileTest it's an expression
    """
    return e.abstract_expression(testNode)

def while_body(bodyNode):
    """
       The body of a WhileStatement is a Statement
    """
    return abstract_statement(bodyNode)

def while_statement(node):
    res = "WhileStatement: " + str(while_test(node['test'])) + bTab(1)
    while (while_test(node['test'])):
        res += while_body(node['body']) + bTab(1)
    return res



# --- End of WhileStatement ---

# --- IfStatement ---
def if_test(testNode):
    """
        a condition test it's an expression
    """
    res = e.abstract_expression(testNode)
    if type(res) == bool :
        return res
    else :
        raise NameError("None Boolean Expression")

def if_consequent(consequentNode):
    """
        a consequent of a condition it's a statement
    """
    return abstract_statement(consequentNode)

def if_alternate(alternateNode):
    """
        an alternative it's a statement or a None
    """
    return None if alternateNode is None else abstract_statement(alternateNode) 

def if_statement(node):
    res = ''
    try :
        testValue = if_test(node['test'])

        if (testValue):
            res += 'IfStatement: ' + str(testValue) + br 
            res += if_consequent(node['consequent'])
        elif (not testValue and node['alternate'] != None):
            res += 'IfStatement: ' + str(testValue) + br
            res += if_alternate(node['alternate'])
    except NameError : 
        print ("Couldn't resolve IfStatment : None boolean expression")
    
    return res

# --- End of IfStatement ---

# --- ForStatement ---
def for_init(initNode):
    """
        A 'For' initialisation is None | VarDeclaration | Expression
    """
    if not initNode:
        return ""
    elif absDecl in initNode['type']:
        return d.abstract_declaration(initNode) 
    elif absExp in initNode['type']:
        return e.abstract_expression(initNode) 

def for_test(testNode):
    """
        A 'For' test is None | Expression
    """
    # si la condition est absente elle est considérée comme true
    if not testNode:
        return True
    return e.abstract_expression(testNode)

def for_update(updateNode):
    """
        A 'For' update is None | Expression
    """
    if not updateNode:
        return ""
    return e.abstract_expression(updateNode)

def for_body(bodyNode):
    """
        A 'For' body is a Statement
    """
    return abstract_statement(bodyNode)

def for_statement(node):
    res = "ForStatement: " + bTab(1)

    for_init(node["init"])
    while (for_test(node['test'])):
        res += for_body(node['body']) + bTab(1)
        for_update(node['update'])

    return res

    
# --- End of ForStatement ---
 
# --- ReturnStatement ---
def return_statement(arg):
    """
        a returnStatement is None | Expression
    """
    res = " ReturnStatement : "
    retr = None
    if not arg:
        return None
    else :
        if (arg["type"] == "Identifier"):
            retr = d.getIdentifierValue(arg["name"])
        else :
            retr = e.abstract_expression(arg)
        if e.functions_calls:
            func_name = list(e.functions_calls[-1].keys())[0]
            e.set_func_return(func_name, e.functions_calls, retr)
            e.set_is_finished(func_name, True)   
        return res + str(retr)

# --- End of ReturnStatement ---   

# --- Abstract method ---
def abstract_statement(node, level=0):
    if node['type'] == 'EmptyStatement':
        return 'EmptyStatement' + bTab(1)
    elif node['type'] == 'ExpressionStatement':
        return expression_statement(node['expression'])
    elif node['type'] == 'BlockStatement':
        return block_statement(node['body']) 
    elif node['type'] == 'WhileStatement': 
        return while_statement(node)
    elif node['type'] == 'IfStatement':
        return if_statement(node)
    elif node['type'] == 'ForStatement':
        return for_statement(node)
    elif node['type'] == 'ReturnStatement':
        return return_statement(node['argument']) 
    elif absDecl in node['type'] :  # a declaration is also a statement 
        return d.abstract_declaration(node, level)
