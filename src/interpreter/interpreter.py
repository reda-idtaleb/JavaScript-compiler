from interpreter.intExpression import abstract_expression
from utils.delimiters import *
from utils.absTypes import *
from .intDeclaration import abstract_declaration
from .intStatement import abstract_statement
from . import intExpression as e
from . import intDeclaration as d

# Main function: pretty-printer
def interpreter(body):
    """
        Browse the list of dictionaries 'body' to analyse each part of the AST.
        :param body: (list) a list of dictionaries containing the AST informations
        :return: (str) return the source code corresponding to the AST(body)
    """
    stmt = ""
    for node in body:
        e.objects_properties = {}
        e.functions_calls = []
        d.paramsValues = {}
        d.localVariables = {}
        
        if absStmt in node['type']:
            stmt += abstract_statement(node) + br

        elif absDecl in node['type']:
            stmt += abstract_declaration(node) + br
    return stmt

