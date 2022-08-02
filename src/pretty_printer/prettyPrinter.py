from utils.delimiters import *
from utils.absTypes import *
from .declaration import abstract_declaration
from .statement import abstract_statement

# Main function: pretty-printer
def pretty_print(body):
    """
        Browse the list of dictionaries 'body' to analyse each part of the AST.
        :param body: (list) a list of dictionaries containing the AST informations
        :return: (str) return the source code corresponding to the AST(body)
    """
    stmt = ""
    for node in body:
        if absStmt in node['type']:
            stmt += abstract_statement(node) + br
        elif absDecl in node['type']:
            stmt += abstract_declaration(node) + br
    return stmt
