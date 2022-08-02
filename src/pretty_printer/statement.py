from utils.delimiters import *
from utils.absTypes import *
from . import expression as e
from . import declaration as d

# --- ExpressionStatement ---
def expression_statement(expStmt):
    """
        ExpressionStatement it's an expression
    """
    return  e.abstract_expression(expStmt)
# --- End of ExpressionStatement ---

# --- BlockStatement ---
def block_statement(bodyNode, level):
    """
        The BlockStatement it's a list of statement
    """
    return  bTab(level).join([abstract_statement(block, level) for block in bodyNode])
# --- End of BlockStatement ---

# --- WhileStatement ---
def while_test(testNode):
    """
        WhileTest it's an expression
    """
    return e.abstract_expression(testNode)

def while_body(bodyNode, level):
    """
       The body of a WhileStatement is a Statement
    """
    return abstract_statement(bodyNode, level)

def while_statement(node, level):
    res = parentOpDelimiter + while_test(node['test']) + parentClDelimiter
    res += blockOpDelimiter + bTab(level) + while_body(node['body'], level-2) + tab(level-2) + blockClDelimiter
    return 'while ' + res
# --- End of WhileStatement ---

# --- IfStatement ---
def if_test(testNode):
    """
        a condition test it's an expression
    """
    return e.abstract_expression(testNode)

def if_consequent(consequentNode, level):
    """
        a consequent of a condition it's a statement
    """
    return abstract_statement(consequentNode, level)

def if_alternate(alternateNode, level):
    """
        an alternative it's a statement or a None
    """
    return tab(level-2)+'else ' + blockOpDelimiter + bTab(level) + abstract_statement(alternateNode, level) + blockClDelimiter
    
def if_statement(node, level):
    res = parentOpDelimiter + if_test(node['test']) + parentClDelimiter
    res += blockOpDelimiter + bTab(level) + if_consequent(node['consequent'], level) + blockClDelimiter
    return 'if' + (res if (not node['alternate']) else (res + br + if_alternate(node['alternate'], level)))
# --- End of IfStatement ---

# --- ForStatement ---
def for_init(initNode):
    """
        A 'For' initialisation is None | VarDeclaration | Expression
    """
    if not initNode:
        return "" + delimiter
    elif absDecl in initNode['type']:
        return d.abstract_declaration(initNode) 
    elif absExp in initNode['type']:
        return e.abstract_expression(initNode) + delimiter

def for_test(testNode):
    """
        A 'For' test is None | Expression
    """
    if not testNode:
        return ""
    return e.abstract_expression(testNode)

def for_update(updateNode):
    """
        A 'For' update is None | Expression
    """
    if not updateNode:
        return ""
    return e.abstract_expression(updateNode)

def for_body(bodyNode, level):
    """
        A 'For' body is a Statement
    """
    return abstract_statement(bodyNode, level)

def for_statement(node, level):
    res =  parentOpDelimiter 
    res += for_init(node['init'])
    res += for_test(node['test']) + delimiter
    res += for_update(node['update']) 
    res += parentClDelimiter
    res += blockOpDelimiter + bTab(level) + for_body(node['body'], level-2) + tab(level-2) + blockClDelimiter
    return 'for ' + res
# --- End of ForStatement ---

# --- BreakStatement & ContinueStatement ---
def break_continue_statement(node):
    """
        a label of a continue or break statement is None | Identifier(Expression)
    """
    nType = node['type'].lower()
    breakSt, continueSt = 'break', 'continue'
    res = breakSt if (breakSt in nType) else continueSt
    return res + ("" if not node['label'] else tab(1) + e.abstract_expression(node['label']))
# --- End of BreakStatement & ContinueStatement ---   

# --- ReturnStatement ---
def return_statement(arg):
    """
        a returnStatement is None | Expression
    """
    return 'return' + ("" if not arg else (tab(1) + e.abstract_expression(arg)))
# --- End of ReturnStatement ---   

# --- SwitchStatement ---
def switch_case(case, level):
    res = ("default" if not case['test'] else 'case ' + e.abstract_expression(case['test'])) + colonDelimiter
    res += bTab(level) + bTab(level).join([abstract_statement(conseq) for conseq in case['consequent']])
    return res
    
def switch_statement(node, level):
    """
        a switchStatement is an Expression + cases: [SwitchCase]
    """
    res = parentOpDelimiter + e.abstract_expression(node['discriminant']) + parentClDelimiter
    res += blockOpDelimiter + bTab(level) + bTab(level).join([switch_case(case, level+2) for case in node['cases']]) + bTab(level-2) + blockClDelimiter
    return 'switch' + res
# --- End of SwitchStatement --- 

# --- Abstract method ---
def abstract_statement(node, level=0):
    if node['type'] == 'EmptyStatement':
        return ""
    elif node['type'] == 'ExpressionStatement':
        return expression_statement(node['expression']) + delimiter
    elif node['type'] == 'BlockStatement':
        return block_statement(node['body'], level+2) + bTab(level-2)
    elif node['type'] == 'WhileStatement': 
        return while_statement(node, level+2)
    elif node['type'] == 'IfStatement':
        return if_statement(node, level+2)
    elif node['type'] == 'ForStatement':
        return for_statement(node, level+2)
    elif (node['type'] == 'BreakStatement') or (node['type'] == 'ContinueStatement'):
        return break_continue_statement(node) + delimiter
    elif node['type'] == 'ReturnStatement':
        return return_statement(node['argument']) + delimiter
    elif node['type'] == 'SwitchStatement':
        return switch_statement(node, level+2)
    elif absDecl in node['type'] :  # a declaration is also a statement 
        return d.abstract_declaration(node, level)