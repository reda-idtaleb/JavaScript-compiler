import os
from utils.delimiters import *
from utils.absTypes import *
from utils.registers import *
from utils.assemblyFunctions import *
from .compStatement import abstract_statement
from .compDeclaration import abstract_declaration

# Main function: compilation
def compile(body, filename):
    """
        Browse the list of dictionaries 'body' to analyse each part of the AST.
        :param body: (list) a list of dictionaries containing the AST informations
        :param filename: (string) The asm filename to be generated.
        :return: (str) return the compiled file corresponding to the AST
    """
    global func_stack
    global indexParamVar
    global localVariables
    global indexLocalVar
    file = open("c-asm/%s" % (filename), "w")
    stmt = asmHeader() + br*2
    stmt += asmMainDec() + blockOpDelimiter + bTab(4)
    stmt += initStack(8192, 0, 8192) + br + bTab(4)
    for node in body:
        func_stack = []
        indexParamVar = 3
        localVariables = {}
        indexLocalVar -= 1
        if absStmt in node['type']:
            stmt += abstract_statement(node)
        elif absDecl in node['type']:
            stmt += abstract_declaration(node)
        stmt += convertASMStmt("debug_reg", r1) + br + bTab(4)
        stmt += "printf(\"\\n\");" + bTab(4)
    stmt += convertASMStmt("debug_reg", r1) + br + bTab(4)
    stmt += exitMain() + br
    stmt += blockClDelimiter
    file.write(stmt)
    file.close()
    return os.path.abspath(file.name)
