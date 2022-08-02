from .delimiters import *
from .registers import *

# the value of the current variable
variable_val = ""

# var x = 0; 
# var y = 0;
# globalVariables = {'x': "globals[0]", 'y': "globals[1]"}
globalVariables = {}
# indicates the index of a global variable in the globals dictionnary
indexGlobalVar = 0

# localVariables = {'x': "bp[-1]", 'y': "bp[-2]"}
localVariables = {}
# indicates the index of a local variable in the base pointer pb[]
indexLocalVar = -1

# save all declared functions -> there adresses 
declared_functions = {}

# func_params = {'x': "bp[3]", 'y': "bp[4]"}
func_params = {}
# indicates the index of a function paramater in the base pointer pb[]
indexParamVar = 3

# execution stack -> func_stack = {'func_1': {'local': [], 'params': [], 'stack':[]}}
func_stack = []

# asm word_t types
word_t_d = "d" # double
word_t_i = "i" # long int
word_t_u = "u" # unsigned long int
word_t_a = "a" # address

# c code-source header
def asmHeader():
    return "#include \"base.h\""

# main declaration
def asmMainDec():
    return "int main()"

# the main return
def exitMain():
    return "return 0;"

# init stack
def initStack(stackSize, heapSize, globalsSize):
    """ 
        initialization (allocation of stack, heap and global variables) 
    """
    return convertASMStmt("init", stackSize, heapSize, globalsSize)

# get a value of a global variable specified by its index
def fromGlobalsGetValue(index):
    """
        get a value of a global variable specified by its index
    """
    return "globals[%d]" % (index)

# get a value of a local variable specified by its index from ebp
def fromLocalsGetValue(index):
    """
        get a value of a local variable specified by its index from ebp
    """
    return bp(index)

# add a global variable into globals[] table
def addToGlobals(indexVar, value):
    """
        Push into globals the value of the global variable specified by it's index
    """
    return "globals[%s] = %s" % (indexVar, value) + delimiter + bTab(4)

# convert to assembly statement
def convertASMStmt(op, *args):
    """
        Build an assembly statement. An ASM statments ends with the delimiter ';'
        :param op:(str) the assembly operation
        :param *args: (list::str) a list of arguments of the assembly operation. T
                                  This paramater can be not specefied.
        :return: (str) return the assembly operation with arguments
        
        :Examples:
        >>> convertASMStmt("pop") 
        'pop();'
        >>> convertASMStmt("push", "iConst(1)")
        'push(iConst(1));'
        >>> convertASMStmt("iadd", "r1", "r1", "r2") 
        'iadd(r1, r1, r2);'  
    """
    if func_stack != []:
        func_name = get_declared_funcs_name(func_stack)[-1]
        func_stack[-1][func_name]['localStack'].append(op if (op == "push" or op == "pop") else "")
    res = op + parentOpDelimiter
    if not args:
        res += ""
    else:
        res += commaDelimiter.join([str(arg) for arg in args])
    res += parentClDelimiter
    return res + delimiter + bTab(4)

def get_declared_funcs_name(stack):
    """
        return a list of declared functions(their names) pushed in the functions stack
    """
    return [list(d.keys())[0] for d in stack]

def getNumberOfPushedStmt(func_local_stack):
    """
        return how many instructions are still in the top of the function stack
    """
    pushed = func_local_stack.count("push")
    popped = func_local_stack.count("pop")
    return abs(pushed-popped)

# assembly expression translation
def convertASMExpression(op, *arg):
    """
        Get an ASM expression. This function doesn't add the delimiter ';' to the expression as 
        the convertASMStmt() do.
        
        :Examples: 
        >>> convertASMExpression('iconst', 10)
        'iconst(10)'
        >>> convertASMExpression('if', convertASMExpression('asbool', r1))
        'if(asbool(r1))'
    """
    asm = convertASMStmt(op, *arg)
    return asm[:len(asm) - len(delimiter + bTab(4))]

# assembly 'goto' instruction
def goto(label):
    """
        return the goto asm instruction "goto label;"
    """
    return "goto " + label + delimiter + bTab(4)

# assembly labels declaration
def labelDeclaration(label):
    """
        return the asm label declaration as "label:"
    """
    return bTab(-4) + label + colonDelimiter + bTab(4)

# get a member of a field of the asm structures
def getWordtField(var, varType):
    """
        get a member of a field of the asm structures
    """
    return var + memberDelimiter + varType

# update an ASM variable
def asmUpdateVariable(var, varType, op, value):
    """
        update an ASM variable of type varType.
        
        :Examples:
        >>> asmUpdateVariable("globals[0]", "i", "+=", 1)
        "globals[0].i += 1;"
    """
    return getWordtField(var, varType) + tab(1) + op + tab(1) + str(value) + delimiter + bTab(4)

# create a unique label 
def createLabel(name, index=None):
    """
        create a unique label using an number as an identifier
    """
    return name if index is None else name + "_%s" % (str(index))

def get_saved_functions():
    return declared_functions

# execution stack -> func_stack = [{'func_1': {'params': dict(),
#                                              'localVar': dict(), 
#                                              'rbp': bp[0],
#                                              'localStack': []
#                                              }}]
def addToFunctionStack(func_name, params, local_var, rbp=bp(0)):
    """
        Add a function to the stack. 
        We save the following information: 
            - The name of the function
            - It's arguments (a dictionary)
            - It's local variable (a dictionary)
            - It's base pointer (set to bp[0])
            - It's own stack (A list of all the pushed and/or popped instructions from the the base pointer.)
    """
    global func_stack
    func_stack.append({func_name: {'params': params,
                             'localVar': local_var,
                             'localStack': [],
                             'rbp': rbp
                            }})
    # save the address of the declared function
    declared_functions[func_name] = {'params': params,
                             'rbp': rbp
                            }
    
