from utils.delimiters import *
from utils.absTypes import *
from utils.assemblyFunctions import *
from utils.registers import *
from . import compDeclaration as d
from . import compExpression as e

# indicates how many times a while/for statement is declared
# so that we can identify each while/for statement by using labels 
# The use of this common counter is to facilitate the 'continue'/'break' statement compilation,
# when referencing to a label.
loop_stmt_counter = 0

# indicates how many if we have, so that we can have unique labels for each ifStatement
if_counter = 0

# Indicates a common label of the invariant for the while/for loops.
# The use of a common label is to facilitate the 'continue' statement compilation.
test_stmt = "test_stmt"

# indicates a common end label of a while/for loops.
# same as test_label: to facilitate the 'break' statement compilation.
end_stmt = "end_stmt"

# --- ExpressionStatement ---
def expression_statement(expNode):
    return e.abstract_expression(expNode)
# --- End of ExpressionStatement ---

# --- WhileStatement ---
def while_test(testNode, label):
    """
        WhileTest it's an expression
    """
    res = labelDeclaration(label)
    return res + e.abstract_expression(testNode)

def while_body(bodyNode, label):
    """
       The body of a WhileStatement is a Statement
    """
    res = labelDeclaration(label)
    return res + abstract_statement(bodyNode)

def while_statement(node):
    """
        res = "WhileStatement: " + str(while_test(node['test'])) + bTab(1)
        while (while_test(node['test'])):
            res += while_body(node['body']) + bTab(1)
        return res
    """
    global loop_stmt_counter
    loop_stmt_counter += 1
    # while labels
    test_label = createLabel(test_stmt, loop_stmt_counter)
    body_label = createLabel("while_body", loop_stmt_counter)
    end_label  = createLabel(end_stmt, loop_stmt_counter)
    # while invariant
    res = goto(test_label)
    res += while_test(node['test'], test_label)
    res += convertASMStmt("pop", r1);
    # while check invariant
    res += convertASMExpression("if", convertASMExpression("asbool", r1)) + tab(1)  
    res += goto(body_label) 
    res += goto(end_label)
    # while body
    res += while_body(node['body'], body_label)
    # while loop
    res += goto(test_label)
    # end of while
    res += labelDeclaration(end_label)
    return res
# --- End of WhileStatement ---

# --- BlockStatement ---
def block_statement(bodyNode):
    """
        The BlockStatement it's a list of statement
    """
    return bTab(4).join([abstract_statement(block) for block in bodyNode])
# --- End of BlockStatement ---

# --- IfStatement ---
def if_test(testNode, label):
    """
        a condition test it's an expression
    """
    res = labelDeclaration(label)
    return res + e.abstract_expression(testNode)

def if_consequent(consequentNode, label):
    """
        a consequent of a condition it's a statement
    """
    return labelDeclaration(label) + abstract_statement(consequentNode)

def if_alternate(alternateNode, label):
    """
        an alternative it's a statement or a None
    """
    res = labelDeclaration(label)
    # if alternate exist so we explore the node
    if alternateNode is not None:
        res += abstract_statement(alternateNode) 
    return res

def if_statement(node):
    global if_counter
    if_counter += 1
    # labels
    test_label = createLabel("if_test", if_counter)
    conseq_label = createLabel("if_consequent", if_counter)
    altern_label = createLabel("if_alternate", if_counter)
    end_label = createLabel("if_end", if_counter)
    # if invariant 
    res = goto(test_label)
    res += if_test(node['test'], test_label)
    res += convertASMStmt("pop", r1);
    # if check invariant
    res += convertASMExpression("if", convertASMExpression("asbool", r1)) + tab(1)  
    res += goto(conseq_label) 
    res += goto(altern_label)
    # we execute the consequent body
    res += if_consequent(node['consequent'], conseq_label)
    # we finished with the if
    res += goto(end_label)
    # we execute the if alternate
    res += if_alternate(node['alternate'], altern_label)
    res += goto(end_label)
    # end if stamt
    res += labelDeclaration(end_label)
    return res
# --- End of IfStatement ---

# --- ForStatement ---
def for_init(initNode, init_label):
    """
        A 'For' initialisation is None | VarDeclaration | Expression
    """
    # init n'est pas présent, donc pas de label à se référencier
    if initNode is None:
        return ""
    # ici forcément y a init, donc on crée son label
    res = goto(init_label)
    res += labelDeclaration(init_label)
    if absDecl in initNode['type']:
        res += d.abstract_declaration(initNode) 
    elif absExp in initNode['type']:
        res += e.abstract_expression(initNode)
    return res

def for_test(testNode, test_label):
    """
        A 'For' test is None | Expression
    """
    # test n'est pâs présent
    if testNode is None:
        return ""
    res = goto(test_label) 
    res += labelDeclaration(test_label)
    res += e.abstract_expression(testNode)
    res += convertASMStmt("pop", r1)
    return res

def for_update(updateNode):
    """
        A 'For' update is None | Expression
    """
    if updateNode is None:
        return ""
    return e.abstract_expression(updateNode)

def for_body(bodyNode, label):
    """
        A 'For' body is a Statement
    """
    res = labelDeclaration(label)
    res += abstract_statement(bodyNode)
    return res

def for_statement(node):
    global loop_stmt_counter
    loop_stmt_counter += 1
    # 'for' labels
    init_label = createLabel("for_init", loop_stmt_counter)
    test_label = createLabel(test_stmt, loop_stmt_counter)
    body_label = createLabel("for_body", loop_stmt_counter)
    end_label  = createLabel(end_stmt, loop_stmt_counter)
    res =  ""
    # On commence par l'initialisation
    res += for_init(node['init'], init_label)
    # on calcule la valeur du test(invariant)
    res += for_test(node['test'], test_label)
    # test checking -> on vérifie si l'invariant est vrai ou non(boucle terminé)
    res += convertASMExpression("if", convertASMExpression("asbool", r1)) + tab(1)
    # si l'invariant est vérifé alors en execute le corps de la boucle
    res += goto(body_label) 
    # si l'invariant n'est pas vérifé alors on doit quitter la boucle
    res += goto(end_label)
    # l'execution du corp de la boucle
    res += for_body(node['body'], body_label)
    # après l'execution du corps, on met à jour l'itérateur de la boucle
    res += for_update(node['update'])
    # passer à l'itération suivante 
    res += goto(test_label)
    # fin de la boucle -> terminé
    res += labelDeclaration(end_label)
    return res
# --- End of ForStatement ---

# --- BreakStatement ---
def break_statement(node):
    """
        a label of a break statement is None | Identifier(Expression)
    """
    end_label = createLabel(end_stmt, loop_stmt_counter)
    return goto(end_label)
# --- End of BreakStatement --- 

# --- ContinueStatement ---
def continue_statement(node):
    """
        a label of a continue statement is None | Identifier(Expression)
    """
    test_label = createLabel(test_stmt, loop_stmt_counter)
    return goto(test_label)
# --- End of ContinueStatement --- 

# --- ReturnStatement ---
def return_statement(node):
    """
        a returnStatement is None | Expression
    """
    global func_stack
    stmt = e.abstract_expression(node['argument'])
    # dépile le résultat du return dans r1
    stmt += convertASMStmt("pop", r1)
    name = get_declared_funcs_name(func_stack)[-1]
    res = stmt
    # supprime tous ce qui a été empilé durant l'execution de la fonction
    last_pushed = func_stack[-1]
    pushed_stmt = getNumberOfPushedStmt(last_pushed[name]['localStack'])
    res += convertASMStmt("drop", pushed_stmt) if pushed_stmt > 0 else ""
    # renvoyer la valeur contenu dans r1
    res += convertASMStmt("ret", r1)
    # tous les chemins doivent passer par un ret
    res += convertASMStmt("assert", 0)
    return res
# --- End of ContinueStatement --- 

# --- Abstract method ---
def abstract_statement(node):
    if node['type'] == 'EmptyStatement':
        return ""
    elif node['type'] == 'ExpressionStatement':
        return expression_statement(node['expression']) 
    elif node['type'] == 'WhileStatement':
        return while_statement(node) 
    elif node['type'] == 'BlockStatement':
        return block_statement(node['body']) 
    elif node['type'] == 'IfStatement':
        return if_statement(node)
    elif node['type'] == 'ForStatement':
        return for_statement(node)
    elif node['type'] == 'BreakStatement':
        return break_statement(node)
    elif node['type'] == 'ContinueStatement':
        return continue_statement(node)
    elif absDecl in node['type'] :  # a declaration is also a statement 
        return d.abstract_declaration(node)
    elif node['type'] == 'ReturnStatement':
        return return_statement(node)
